#!/usr/bin/env python3
"""Score previously recorded live evaluation trials without calling the model.

This is retrospective scoring, not a new before/after evaluation. The original
uncached responses, retrieved chunks, and unscored logs remain unchanged.
"""

import argparse
import hashlib
import json
from pathlib import Path

import questions
from scorer import judge


def score_trials(data: dict) -> tuple[list[dict], int]:
    """Apply the Week 2 scorer to all recorded covered-question trials."""
    if data.get("answer_cache") is not False:
        raise ValueError("Source log does not prove answer caching was disabled")
    runs = data.get("runs")
    if not isinstance(runs, int) or runs < 3:
        raise ValueError("Source log must contain at least three runs")

    trials = data.get("covered_trials", [])
    expected = {item["question"]: item["expects"] for item in questions.answered()}
    if len(trials) != len(expected) * runs:
        raise ValueError("Source trial count does not match fixed questions and runs")

    rows = {question: {"question": question, "runs": {}} for question in expected}
    for trial in trials:
        question, run = trial["question"], trial["run"]
        if question not in rows or not isinstance(run, int) or not 1 <= run <= runs:
            raise ValueError("Source log contains an unknown question or run")
        if run in rows[question]["runs"]:
            raise ValueError("Source log contains a duplicate question/run")
        answer = trial["answer"]
        chunks = trial["retrieved_chunks"]
        rows[question]["runs"][run] = judge(question, expected[question], answer, chunks)

    for row in rows.values():
        if set(row["runs"]) != set(range(1, runs + 1)):
            raise ValueError("Source log is missing a question/run")
    return list(rows.values()), runs


def score_file(path: Path) -> Path:
    """Write a clearly labeled derived Markdown report beside a raw JSON log."""
    raw = path.read_bytes()
    data = json.loads(raw)
    rows, runs = score_trials(data)
    output = path.with_name(path.stem + "_scored.md")
    total = sum(sum(row["runs"].values()) for row in rows)
    lines = [
        f"# Retrospective scorer results — {data.get('label', 'unlabeled')}",
        "",
        "These pass/fail results were calculated by `score_saved.py` using",
        "`scorer.py::judge` on the real answers already saved by `run_eval.py`.",
        "**No model was called and no retrieval was rerun for this report.**",
        "The original JSON and Markdown run logs remain unchanged.",
        "",
        f"- Original live evidence: `{path.name}`",
        f"- Original JSON SHA-256: `{hashlib.sha256(raw).hexdigest()}`",
        f"- Original runs per question: {runs}; cache disabled in source log",
        f"- Substring scorer passed: {total}/{len(rows) * runs} saved covered trials",
        "",
        "| Question | " + " | ".join(f"Run {i}" for i in range(1, runs + 1)) + " |",
        "|---|" + "---|" * runs,
    ]
    for row in rows:
        question = row["question"].replace("|", "\\|")
        marks = ["pass" if row["runs"][i] else "fail" for i in range(1, runs + 1)]
        lines.append(f"| {question} | " + " | ".join(marks) + " |")
    lines += [
        "",
        "This quick substring check cannot detect unsupported extra claims.",
        "The criterion-level judgments and manual source checks are in `README.md`.",
        "",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"{path.name}: {total}/{len(rows) * runs} saved answers passed; wrote {output}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", nargs="+", type=Path, help="saved run_eval JSON files")
    args = parser.parse_args()
    for path in args.evidence:
        score_file(path)


if __name__ == "__main__":
    main()
