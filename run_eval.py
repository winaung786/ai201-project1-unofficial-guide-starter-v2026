#!/usr/bin/env python3
"""
Run your test questions repeatedly and write the results down.

    python run_eval.py                 three runs, the default
    python run_eval.py --runs 5        more runs
    python run_eval.py --label after   name this run, e.g. before/after a fix

This does the mechanical half of week 2 for you: it asks each of your questions
the same way three separate times, with caching turned off so you get three
real answers, and writes a Markdown table and full JSON evidence into results/.

It also puts every question in `OUT_OF_SCOPE` through retrieval and the gate
three times and records what happened. Gate-refused trials cost no model calls.

That table is the raw material for your run log, not the run log itself. The
submission template wants one row per *criterion* — aggregating your questions
up into your criteria is your work, not the script's.

⚠️ What it does NOT do is decide whether an answer was right.

That judgment is yours, and you'll build it in class in week 2 as `scorer.py`.
Until that file exists, the Run columns carry the raw answers and you read them
yourself. Once it exists — a file called `scorer.py`, with a function
`judge(question, expects, answer, results) -> bool` — this script finds it
automatically and the Run columns carry verdicts instead.

Deciding what counts as correct is the actual lesson. It would be easy to hand
you a scorer; you'd learn nothing from it.
"""

import argparse
import datetime as dt
import importlib.metadata
import json
from pathlib import Path
import re
import sys
from types import SimpleNamespace

import config
import questions as qs
import eval_checkpoint as checkpoint


def load_scorer():
    """Use scorer.py if the student has built it. Otherwise run unscored."""
    try:
        import scorer  # noqa: PLC0415
    except ImportError:
        return None
    judge = getattr(scorer, "judge", None)
    return judge if callable(judge) else None


def run_once(question: str, top_k, threshold, corpus, variant):
    """Measure the actual application answer and retain the raw model output."""
    from app import ask_pipeline

    observed = {"results": [], "decision": None, "model_answer": None}
    outcome = ask_pipeline(
        question, top_k=top_k, threshold=threshold, corpus=corpus,
        variant=variant, answer_cache=False,
        on_retrieval=lambda hits: observed.update(results=hits),
        on_gate=lambda decision: observed.update(decision=decision),
        on_model_answer=lambda answer: observed.update(model_answer=answer),
    )
    return outcome, observed["results"], observed["decision"], observed["model_answer"]


def evidence(outcome, results, decision, model_answer, run):
    """Keep all retrieved evidence used for this exact trial."""
    return {
        "question": outcome["question"], "run": run,
        "answer": outcome["answer"], "raw_model_answer": model_answer,
        "prompt": outcome.get("prompt"),
        "cited_sources": outcome["sources"],
        "retrieved_sources": outcome["retrieved_sources"],
        "best_distance": decision.best_distance,
        "gate_passed": decision.passed,
        "refused": outcome["refused"],
        "refusal_reason": outcome["refusal_reason"],
        "retrieved_chunks": [
            {"label": r.label, "source": r.source, "text": r.text,
             "distance": r.distance, "produced_by": r.produced_by}
            for r in results
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the test questions and log the results.")
    parser.add_argument("--runs", type=config.positive_int, default=None,
                        help="runs per question (default 3; recorded value on resume)")
    parser.add_argument("--label", default=None, help="a name for this run, e.g. 'before'")
    parser.add_argument("--corpus", default=None)
    parser.add_argument("--variant", default=None)
    parser.add_argument("--top-k", type=config.positive_int, default=None)
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--requests-per-minute", type=config.positive_int, default=None,
                        help="pacing override; otherwise AI201_REQUESTS_PER_MINUTE/default 30")
    parser.add_argument("--resume", type=Path, help="resume an interrupted checkpoint JSON")
    args = parser.parse_args(argv)

    recorded = {}
    if args.resume:
        recorded = json.loads(args.resume.read_text(encoding="utf-8"))

    def setting(name, default):
        value = getattr(args, name)
        return value if value is not None else recorded.get(name, default)

    corpus = setting("corpus", config.CORPUS)
    top_k = setting("top_k", config.TOP_K)
    threshold = setting("threshold", config.THRESHOLD)
    args.runs = setting("runs", 3)
    args.label = setting("label", "")
    args.variant = setting("variant", "default")
    config.REQUESTS_PER_MINUTE = (
        args.requests_per_minute if args.requests_per_minute is not None
        else recorded.get("requests_per_minute", config.REQUESTS_PER_MINUTE)
    )

    items = qs.answered()
    if not items:
        print(
            "questions.py has no questions in it yet.\n"
            "Milestone 2 asks you to write five. Fill them in and run this again.",
            file=sys.stderr,
        )
        return 1

    judge = load_scorer()
    if judge is None:
        print("No scorer.py found — running unscored. Verdict column will be blank.")
        print("You'll build scorer.py in class in week 2.\n")

    if args.runs < 3:
        print(f"⚠️  {args.runs} run(s). The submission asks for three.\n")

    runtime = {"python": sys.version.split()[0], "packages": {}}
    for name in ("chromadb", "onnxruntime", "google-genai", "python-dotenv"):
        try:
            runtime["packages"][name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            runtime["packages"][name] = None
    settings = {
        "label": args.label, "corpus": corpus, "variant": args.variant,
        "embedding_model": config.EMBEDDING_MODEL, "generation_model": config.MODEL,
        "top_k": top_k, "threshold": threshold, "runs": args.runs, "runtime": runtime,
    }
    question_set = {"covered": items, "out_of_scope": getattr(qs, "OUT_OF_SCOPE", [])}
    hashes = checkpoint.fingerprints(corpus)
    now = dt.datetime.now(dt.timezone.utc)
    if args.resume:
        state = checkpoint.load(args.resume, settings, question_set, hashes, judge is not None)
        json_path = args.resume
    else:
        label = re.sub(r"[^A-Za-z0-9_-]", "-", args.label)
        suffix = f"_{label}" if label else ""
        json_path = config.RESULTS_DIR / f"run_{now.strftime('%Y%m%dT%H%M%S%fZ')}{suffix}.json"
        if json_path.exists():
            raise FileExistsError(json_path)
        state = {
            "schema_version": 2, **settings, "when_utc": now.isoformat(),
            "status": "running", "answer_cache": False, "scored": judge is not None,
            "question_set": question_set, "fingerprints": hashes,
            "covered_trials": [], "out_of_scope_trials": [], "sessions": [],
            "errors": [], "model_calls": 0,
            "token_counts": {"prompt": 0, "output": 0, "total": 0},
        }

    import generate as gen

    session = {
        "when_utc": now.isoformat(), "requests_per_minute": config.REQUESTS_PER_MINUTE,
        "model_calls": 0, "token_counts": {"prompt": 0, "output": 0, "total": 0},
    }
    state["sessions"].append(session)
    state["requests_per_minute"] = config.REQUESTS_PER_MINUTE
    state["status"] = "running"
    last_calls, last_tokens = gen.call_count(), gen.token_counts()

    def persist():
        nonlocal last_calls, last_tokens
        calls, tokens = gen.call_count(), gen.token_counts()
        for destination in (state, session):
            destination["model_calls"] += calls - last_calls
            for key in tokens:
                destination["token_counts"][key] += tokens[key] - last_tokens[key]
        last_calls, last_tokens = calls, tokens
        state["updated_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
        # JSON is the canonical checkpoint; Markdown can always be regenerated.
        checkpoint.save(json_path, state)
        write_report(state, json_path.with_suffix(".md"))

    persist()
    print(f"Checkpoint: {json_path}", flush=True)
    trial_id, phase = None, "setup"
    try:
        for kind, questions in question_set.items():
            for index, item in enumerate(questions):
                question = item["question"] if kind == "covered" else item
                for run in range(1, args.runs + 1):
                    trial_id = f"{kind}:{index}:{run}"
                    entries = state[f"{kind}_trials"]
                    entry = next((e for e in entries if e["trial_id"] == trial_id), None)
                    if entry is not None and entry["scoring_complete"]:
                        continue
                    if entry is None:
                        phase = "application"
                        calls_before, tokens_before = gen.call_count(), gen.token_counts()
                        outcome, results, decision, raw = run_once(
                            question, top_k, threshold, corpus, args.variant
                        )
                        entry = evidence(outcome, results, decision, raw, run)
                        entry.update(
                            trial_id=trial_id, scoring_complete=kind != "covered",
                            model_calls=gen.call_count() - calls_before,
                            token_counts={key: value - tokens_before[key]
                                          for key, value in gen.token_counts().items()},
                        )
                        if kind == "covered":
                            entry["scorer_passed"] = None
                        else:
                            entry["gate_refused"] = not decision.passed
                        entries.append(entry)
                        # Save the raw response BEFORE invoking the scorer.
                        persist()
                    if kind == "covered":
                        phase = "scorer"
                        results = [SimpleNamespace(**hit) for hit in entry["retrieved_chunks"]]
                        entry["scorer_passed"] = (
                            judge(question, item.get("expects", ""), entry["answer"], results)
                            if judge else None
                        )
                        entry["scoring_complete"] = True
                        persist()
                    print(f"  {trial_id}: recorded — {question}", flush=True)
    except (Exception, KeyboardInterrupt) as exc:
        state["status"] = "interrupted"
        state["errors"].append({
            "when_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "trial_id": trial_id, "phase": phase, "error_type": type(exc).__name__,
        })
        persist()
        print(f"Interrupted at {trial_id} ({type(exc).__name__}); completed outputs are saved.",
              file=sys.stderr)
        print(f"Resume: python run_eval.py --resume {json_path} --requests-per-minute 8",
              file=sys.stderr)
        return 1

    state["status"] = "complete"
    persist()
    print(f"Wrote {json_path} and {json_path.with_suffix('.md')}")
    print(f"Cumulative calls/tokens: {state['model_calls']} / {state['token_counts']}")
    return 0


def write_report(state, path):
    """Generate a readable view of the checkpoint; never imply partial trials passed."""
    n = state["runs"]
    transcript = state["covered_trials"]
    gate_rows = state["out_of_scope_trials"]
    rows = []
    for item in state["question_set"]["covered"]:
        trials = [entry for entry in transcript if entry["question"] == item["question"]]
        rows.append({"question": item["question"], "runs": [
            next((entry.get("scorer_passed") for entry in trials
                  if entry["run"] == run and entry["scoring_complete"]), "pending")
            for run in range(1, n + 1)
        ]})
    corpus, top_k, threshold = state["corpus"], state["top_k"], state["threshold"]
    run_headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    run_divider = "|".join(["---"] * n)

    lines = [
        f"# Run log — {state['label']}",
        "",
        f"**Status: {state['status'].upper()}**. Incomplete trials are pending, not passes.",
        f"Recorded trials: {len(transcript)} covered, {len(gate_rows)} out-of-scope.",
        f"Model request attempts: {state['model_calls']}; tokens: {state['token_counts']}.",
        f"Pacing for the latest session: {state['requests_per_minute']} requests/minute.",
        f"- Produced by: `run_eval.py::main`",
        f"- Retrieval: `store.py::search`, chunks from `chunker.py::split_documents`",
        f"- Corpus: `{corpus}` (index variant `{state['variant']}`)",
        f"- top-k: {top_k} · relevance cutoff: {threshold}",
        f"- Runs per question: {n}, caching off",
        f"- Started UTC: {state['when_utc']}",
        "",
        "This table is one row per QUESTION. The run log your README asks for is",
        "one row per CRITERION, so aggregate these into it — criterion 1 is how many",
        "of your questions had the answer in the retrieved chunks, and so on.",
        "",
        f"| Question | {run_headers} |",
        f"|---|{run_divider}|",
    ]

    for row in rows:
        cells = []
        for passed in row["runs"]:
            cells.append({True: "pass", False: "fail", None: "unscored", "pending": "pending"}[passed])
        question = row["question"].replace("|", "\\|")
        lines.append(f"| {question} | {' | '.join(cells)} |")

    if not state["scored"]:
        lines += [
            "",
            "> The Run columns are blank because `scorer.py` doesn't exist yet.",
            "> Judge each question yourself by reading the output below, or build",
            "> the scorer first and re-run.",
        ]

    if gate_rows:
        refused = sum(r["gate_refused"] for r in gate_rows)
        lines += [
            "",
            "---",
            "",
            "## The relevance gate on out-of-corpus questions",
            "",
            f"Produced by `run_eval.py::main` via `run_once`, cutoff {threshold}. "
            f"Refused {refused} of {len(gate_rows)}.",
            "",
            "Each fixed question was tested in every run. Gate refusals cost",
            "zero model calls; questions let through use the application answer.",
            "",
            "| Run | Out-of-scope question | Best distance | Gate |",
            "|---|---|---|---|",
        ]
        for row in gate_rows:
            question = row["question"].replace("|", "\\|")
            verdict = "refused" if row["gate_refused"] else "**let through**"
            lines.append(f"| {row['run']} | {question} | {row['best_distance']:.3f} | {verdict} |")

    lines += ["", "---", "", "## Real output", "",
              "This is what the system actually produced. Paste the relevant parts",
              "into your README underneath the table — the rubric asks for real",
              "output as text, not a description of it.", ""]

    for entry in transcript + gate_rows:
        lines += [
            f"### {entry['question']} — run {entry['run']}",
            "",
            f"- Best distance: {entry['best_distance']:.4f} "
            f"({'passed' if entry['gate_passed'] else 'refused by'} the gate)",
            f"- Sources retrieved: {', '.join(entry['retrieved_sources']) or 'none'}",
            f"- Sources cited: {', '.join(entry['cited_sources']) or 'none'}",
            "",
            "```",
            entry["answer"],
            "```",
            "",
        ]

    checkpoint.atomic_write(path, "\n".join(lines) + "\n")


if __name__ == "__main__":
    sys.exit(main())
