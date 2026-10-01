"""Durable evaluation state. No retrieval or model calls happen in this module."""

import hashlib
import json
import os
from pathlib import Path
import tempfile

import config


def fingerprints(corpus):
    """Reject mixing trials across changed pipeline code or source documents.

    Hash relevant files only; credentials, caches, and prior results are excluded.
    Index variant and embedding/chunk settings are recorded by the runner too.
    """
    names = (
        "app.py", "ingest.py", "chunker.py", "store.py", "gate.py", "generate.py",
        "config.py", "questions.py", "scorer.py", "criteria.md", "requirements.txt",
        "run_eval.py", "eval_checkpoint.py",
    )
    paths = [config.ROOT / name for name in names]
    paths += sorted(config.corpus_path(corpus).rglob("*"))
    return {
        str(path.relative_to(config.ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths if path.is_file()
    }


def atomic_write(path, text):
    """Replace a checkpoint only after the complete new file is flushed to disk."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False,
        ) as stream:
            temporary = Path(stream.name)
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def save(path, state):
    atomic_write(path, json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def load(path, settings, question_set, hashes, scored):
    state = json.loads(Path(path).read_text(encoding="utf-8"))
    if state.get("schema_version") != 2:
        raise ValueError("Only new checkpoint logs can be resumed; historical logs are immutable.")
    if state.get("status") == "complete":
        raise ValueError("This evaluation is already complete; start a new labeled run.")
    for key, value in settings.items():
        if state.get(key) != value:
            raise ValueError(f"Cannot resume: {key} differs from the recorded evaluation.")
    if state.get("question_set") != question_set:
        raise ValueError("Cannot resume: question set differs from the recorded evaluation.")
    if state.get("fingerprints") != hashes:
        raise ValueError("Cannot resume: pipeline code or corpus changed.")
    if state.get("scored") != scored or state.get("answer_cache") is not False:
        raise ValueError("Cannot resume: scorer availability or cache setting changed.")

    expected = {
        (kind, f"{kind}:{index}:{run}", item["question"] if kind == "covered" else item, run)
        for kind, items in (("covered", question_set["covered"]),
                            ("out_of_scope", question_set["out_of_scope"]))
        for index, item in enumerate(items)
        for run in range(1, settings["runs"] + 1)
    }
    seen = set()
    for kind in ("covered", "out_of_scope"):
        for entry in state[f"{kind}_trials"]:
            identity = (kind, entry["trial_id"], entry["question"], entry["run"])
            if identity not in expected or identity in seen:
                raise ValueError("Cannot resume: unexpected or duplicate recorded trial.")
            seen.add(identity)
    return state
