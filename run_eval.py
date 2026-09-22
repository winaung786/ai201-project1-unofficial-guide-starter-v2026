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
import json
import sys

import config
import questions as qs


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


def main():
    parser = argparse.ArgumentParser(description="Run the test questions and log the results.")
    parser.add_argument("--runs", type=int, default=3, help="runs per question (default 3)")
    parser.add_argument("--label", default="", help="a name for this run, e.g. 'before'")
    parser.add_argument("--corpus", default=None)
    parser.add_argument("--variant", default="default")
    parser.add_argument("--top-k", type=int, default=None)
    parser.add_argument("--threshold", type=float, default=None)
    args = parser.parse_args()

    corpus = args.corpus or config.CORPUS
    top_k = args.top_k or config.TOP_K
    threshold = config.THRESHOLD if args.threshold is None else args.threshold

    items = qs.answered()
    if not items:
        print(
            "questions.py has no questions in it yet.\n"
            "Milestone 2 asks you to write five. Fill them in and run this again.",
            file=sys.stderr,
        )
        sys.exit(1)

    judge = load_scorer()
    if judge is None:
        print("No scorer.py found — running unscored. Verdict column will be blank.")
        print("You'll build scorer.py in class in week 2.\n")

    if args.runs < 3:
        print(f"⚠️  {args.runs} run(s). The submission asks for three.\n")

    transcript = []
    rows = []

    for item in items:
        question = item["question"]
        expects = item.get("expects", "")
        print(f"\n{question}")

        run_results = []
        for run in range(1, args.runs + 1):
            outcome, results, decision, model_answer = run_once(
                question, top_k, threshold, corpus, args.variant
            )
            passed = judge(question, expects, outcome["answer"], results) if judge else None
            run_results.append(passed)

            mark = {True: "pass", False: "fail", None: "—"}[passed]
            print(f"  run {run}: {mark}  (best distance {decision.best_distance:.3f})")

            entry = evidence(outcome, results, decision, model_answer, run)
            entry["scorer_passed"] = passed
            transcript.append(entry)

        rows.append({"question": question, "expects": expects, "runs": run_results})

    gate_rows = check_out_of_scope(top_k, threshold, corpus, args.variant, args.runs)

    write_report(
        rows, transcript, gate_rows, args, corpus, top_k, threshold,
        scored=judge is not None,
    )


def check_out_of_scope(top_k, threshold, corpus, variant, runs=1):
    """Put every OUT_OF_SCOPE question through retrieval and the gate.

    Criterion 3 in criteria.md is about questions the corpus doesn't cover, and
    it needs evidence in the run log like the other four. Gate-refused
    questions cost no model calls; every trial is recorded separately.
    """
    questions = getattr(qs, "OUT_OF_SCOPE", [])
    if not questions:
        return []

    print("\nOut-of-scope questions (the gate should refuse these):")
    rows = []
    for run in range(1, runs + 1):
        for question in questions:
            outcome, results, decision, model_answer = run_once(
                question, top_k, threshold, corpus, variant
            )
            row = evidence(outcome, results, decision, model_answer, run)
            row["gate_refused"] = not decision.passed
            rows.append(row)
            print(f"  run {run}: {'gate refused' if row['gate_refused'] else 'gate LET THROUGH'}  "
                  f"(best distance {decision.best_distance:.3f})  {question}")

    kept = sum(r["gate_refused"] for r in rows)
    print(f"  -> gate refused {kept} of {len(rows)} trials")
    return rows


def write_report(rows, transcript, gate_rows, args, corpus, top_k, threshold, scored):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{label}.md"
    json_path = path.with_suffix(".json")

    n = len(rows[0]["runs"]) if rows else 0
    run_headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    run_divider = "|".join(["---"] * n)

    lines = [
        f"# Run log{f' — {args.label}' if args.label else ''}",
        "",
        f"- Produced by: `run_eval.py::main`",
        f"- Retrieval: `store.py::search`, chunks from `chunker.py::split_documents`",
        f"- Corpus: `{corpus}` (index variant `{args.variant}`)",
        f"- top-k: {top_k} · relevance cutoff: {threshold}",
        f"- Runs per question: {n}, caching off",
        f"- When: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
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
            cells.append({True: "pass", False: "fail", None: " "}[passed])
        question = row["question"].replace("|", "\\|")
        lines.append(f"| {question} | {' | '.join(cells)} |")

    if not scored:
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
            f"Produced by `run_eval.py::check_out_of_scope`, cutoff {threshold}. "
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

    for entry in transcript:
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

    path.write_text("\n".join(lines), encoding="utf-8")

    import generate as gen

    json_path.write_text(json.dumps({
        "label": args.label, "when_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "corpus": corpus, "variant": args.variant,
        "embedding_model": config.EMBEDDING_MODEL, "generation_model": config.MODEL,
        "top_k": top_k, "threshold": threshold, "runs": n,
        "answer_cache": False, "scored": scored,
        "covered_trials": transcript, "out_of_scope_trials": gate_rows,
        "model_calls": gen.call_count(), "token_counts": gen.token_counts(),
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nWrote {path.relative_to(config.ROOT)} and {json_path.relative_to(config.ROOT)}")
    print(gen.usage())
    print("\nCommit this file. It's the evidence the run actually happened.")


if __name__ == "__main__":
    main()
