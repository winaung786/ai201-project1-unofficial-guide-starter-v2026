#!/usr/bin/env python3
"""Repeatable retrieval/gate probe for the optional Unit 2 stretch iteration.

These supplemental questions were selected after the original Unit 2 work;
they do not replace the original questions or change the original verdicts.
No generation calls or response cache are involved.
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import config
from gate import check
from questions import OUT_OF_SCOPE, QUESTIONS as ORIGINAL_QUESTIONS
from store import search


# Original-source facts are checked in the retrieved chunk, not inferred from
# filename or from a generated answer.
SUPPLEMENTAL_COVERED = [
    {
        "question": "Can I pay cash for an Aldridge Hall wash?",
        "source": "housing_aldridge_hall_laundry.txt",
        "facts": ["card only"],
    },
    {
        "question": "How many study room blocks can one person reserve per week?",
        "source": "study_group_rooms.txt",
        "facts": ["maximum two blocks per person per week"],
    },
    {
        "question": "When does Kestrel Commons close on weekends?",
        "source": "dining_kestrel_commons.txt",
        "facts": ["9:00am to 8:00pm weekends"],
    },
    {
        "question": "Does semester printing credit carry into the next semester?",
        "source": "admin_printing_quota.txt",
        "facts": ["does not roll over"],
    },
    {
        "question": "Are housing lottery ties for juniors and seniors broken at random?",
        "source": "admin_housing_lottery.txt",
        "facts": ["only tie-break randomly"],
    },
    {
        "question": "What is the cost of a cash meal at Kestrel Commons?",
        "source": "dining_kestrel_commons.txt",
        "facts": ["$12.50 cash"],
    },
]

# Checked against the corpus: the requested closing time, cancellation fee,
# Friday-specific menu, refund deadline, and lottery application fee are absent.
SUPPLEMENTAL_UNANSWERABLE = [
    "What time does Aldridge Hall's laundry room close?",
    "What is the cancellation fee for a group study room?",
    "What is the Kestrel Commons dinner menu on Fridays?",
    "What is the deadline to request a refund of unused printing credit?",
    "How much is the housing lottery application fee?",
]


def summarize(question, source=None, facts=()):
    chosen = search(question, top_k=1)
    candidates = search(question, top_k=5)
    decision = check(chosen)
    first = chosen[0] if chosen else None
    supported = bool(
        decision.passed
        and first
        and first.source == source
        and all(fact.casefold() in first.text.casefold() for fact in facts)
    )
    return {
        "question": question,
        "expected_source": source,
        "required_facts": list(facts),
        "selected_source": first.source if first else None,
        "selected_text": first.text if first else None,
        "selected_distance": first.distance if first else None,
        "gate_passed": decision.passed,
        "supported_in_selected_chunk": supported if source else None,
        "candidate_sources": [
            {"source": r.source, "distance": r.distance, "text": r.text}
            for r in candidates
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True, choices=("before", "after"))
    args = parser.parse_args()
    covered = [
        summarize(row["question"], row["source"], row["facts"])
        for row in SUPPLEMENTAL_COVERED
    ]
    unsupported = [summarize(q) for q in SUPPLEMENTAL_UNANSWERABLE]
    original_covered = [summarize(row["question"]) for row in ORIGINAL_QUESTIONS]
    original_out = [summarize(q) for q in OUT_OF_SCOPE]
    data = {
        "label": f"stretch_{args.label}",
        "when_utc": datetime.now(timezone.utc).isoformat(),
        "corpus": config.CORPUS,
        "embedding_model": config.EMBEDDING_MODEL,
        "generation_model": config.MODEL,
        "top_k": config.TOP_K,
        "threshold": config.THRESHOLD,
        "generated_answers": 0,
        "supplemental_covered": covered,
        "supplemental_unanswerable": unsupported,
        "original_covered_retrieval": original_covered,
        "original_unanswerable_gate": original_out,
    }
    path = config.RESULTS_DIR / f"stretch_probe_{args.label}.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"Saved {path}")
    print(
        f"Supplemental answer-bearing top-1 chunks: "
        f"{sum(x['supported_in_selected_chunk'] for x in covered)}/{len(covered)}"
    )
    print(
        f"Supplemental unsupported questions refused by gate: "
        f"{sum(not x['gate_passed'] for x in unsupported)}/{len(unsupported)}"
    )
    for row in covered:
        print(
            f"{'PASS' if row['supported_in_selected_chunk'] else 'MISS'} "
            f"{row['selected_distance']:.3f} {row['selected_source']}: "
            f"{row['question']}"
        )


if __name__ == "__main__":
    main()
