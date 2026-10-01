#!/usr/bin/env python3
"""Derive canonical run counts/usage from saved JSON, without any model calls."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import questions


def trial_matrix(trials, expected, runs):
    pairs = [(row["question"], row["run"]) for row in trials]
    target = {(question, run) for question in expected for run in range(1, runs + 1)}
    return len(pairs) == len(target) and len(set(pairs)) == len(pairs) and set(pairs) == target


def summarize(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    covered, gate = data["covered_trials"], data["out_of_scope_trials"]
    runs = data["runs"]
    complete = (
        data.get("status", "complete") == "complete"
        and data.get("answer_cache") is False
        and trial_matrix(covered, [q["question"] for q in questions.answered()], runs)
        and trial_matrix(gate, questions.OUT_OF_SCOPE, runs)
        and all(row.get("scoring_complete", True) for row in covered)
    )
    tokens = data["token_counts"]
    if tokens["total"] != tokens["prompt"] + tokens["output"]:
        raise ValueError(f"Inconsistent token arithmetic in {path.name}")
    scores = [row.get("scorer_passed") for row in covered]
    scored = f"{sum(s is True for s in scores)}/{len(scores)}" if (
        scores and all(isinstance(s, bool) for s in scores)
    ) else "not recorded"
    return {
        "path": path, "label": data["label"], "when": data["when_utc"],
        "status": "COMPLETE" if complete else "INCOMPLETE",
        "runs": runs, "covered": len(covered), "gate_trials": len(gate),
        "gate_refused": sum(row["gate_refused"] for row in gate),
        "scorer": scored, "top_k": data["top_k"], "calls": data["model_calls"],
        "tokens": tokens, "sha256": hashlib.sha256(raw).hexdigest(),
    }


def render(paths):
    rows = [summarize(path) for path in sorted(paths)]
    lines = [
        "# Evaluation summary — generated from raw JSON", "",
        "Canonical location for live-run counts and token totals. Regenerate with",
        "`python tools/summarize_evaluations.py`; verify with the same command plus `--check`.",
        "This script makes no retrieval or model calls and does not change raw logs.",
        "Manual criterion verdicts and claim reviews remain in [README](../README.md#verdicts).",
        "The substring scorer column reports only values already recorded in JSON.",
        "Retrospective scoring is separately labeled in [scorer verification](scorer_verification.md).",
        "", "Different live runs can have different output-token totals. The original pair",
        "and the later scorer-enabled pair are separate measurements, each linked below.",
        "No missing token metadata is estimated; these are the runner's recorded totals.",
        "Request attempts include retries in checkpoint-enabled logs; failed requests may",
        "have no returned token metadata. COMPLETE requires the full trial matrix and",
        "disabled caching; it does not establish factual correctness or a passing criterion.",
        "",
        "| Live evidence | Status | Top-k | Runs/question | Covered trials | Gate refused/trials | Scorer | Request attempts | Prompt | Output | Total |",
        "|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        tokens = row["tokens"]
        lines.append(
            f"| [{row['label']}]({row['path'].name}) | {row['status']} | {row['top_k']} | "
            f"{row['runs']} | {row['covered']} | {row['gate_refused']}/{row['gate_trials']} | "
            f"{row['scorer']} | {row['calls']} | {tokens['prompt']:,} | "
            f"{tokens['output']:,} | {tokens['total']:,} |"
        )
    lines += ["", "## Provenance", "", "| JSON file | Recorded UTC timestamp | SHA-256 |", "|---|---|---|"]
    for row in rows:
        lines.append(f"| `{row['path'].name}` | {row['when']} | `{row['sha256']}` |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the saved summary is stale")
    args = parser.parse_args()
    output = ROOT / "results" / "evaluation_summary.md"
    text = render((ROOT / "results").glob("run_*.json"))
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != text:
            parser.exit(1, "Evaluation summary is stale; regenerate it from the JSON logs.\n")
        print("Evaluation summary matches the JSON logs.")
    else:
        output.write_text(text, encoding="utf-8")
        print(f"Wrote {output}")


if __name__ == "__main__":
    main()
