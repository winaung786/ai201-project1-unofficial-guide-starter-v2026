"""Measure the ten fixed calibration questions without making model calls.

Run after indexing: python calibrate.py
Writes distances, complete retrieved chunks, and gate decisions to results/.
This is milestone-4 calibration, not the next unit's answer evaluation.
"""
import json
import os
from dataclasses import asdict
from datetime import datetime, timezone

import config
import gate
from questions import QUESTIONS, OUT_OF_SCOPE
from store import search


def main():
    if os.getenv("AI201_FAKE_EMBEDDINGS") == "1":
        raise SystemExit("Calibration requires real embeddings; remove AI201_FAKE_EMBEDDINGS.")
    if len(QUESTIONS) != 5 or any(not q['question'].strip() or not q['expects'].strip() for q in QUESTIONS):
        raise SystemExit("Record all five questions and expects phrases before calibration.")
    rows = []
    for in_corpus, questions in [(True, [q['question'] for q in QUESTIONS]), (False, OUT_OF_SCOPE)]:
        for question in questions:
            hits = search(question)
            if not hits:
                raise SystemExit("No chunks retrieved; rebuild the index before calibration.")
            decision = gate.check(hits)
            row = dict(question=question, in_corpus=in_corpus,
                       best_distance=decision.best_distance, gate_passed=decision.passed,
                       retrieved=[asdict(hit) for hit in hits])
            rows.append(row)
            print(f"{'IN ' if in_corpus else 'OUT'} {decision.best_distance:.6f}  {question}")
    inside = [r['best_distance'] for r in rows if r['in_corpus']]
    outside = [r['best_distance'] for r in rows if not r['in_corpus']]
    gap = min(outside) - max(inside)
    suggested = round((max(inside) + min(outside)) / 2, 3) if gap > 0 else None
    report = dict(timestamp_utc=datetime.now(timezone.utc).isoformat(), corpus=config.CORPUS,
                  embedding_model=config.EMBEDDING_MODEL, metric='cosine', top_k=config.TOP_K,
                  chunk_size=config.CHUNK_SIZE, overlap=config.CHUNK_OVERLAP,
                  threshold=config.THRESHOLD, gap=gap, suggested_threshold=suggested,
                  note='Retrieval calibration only; no generated answers or week-2 verdicts.', rows=rows)
    config.RESULTS_DIR.mkdir(exist_ok=True)
    path = config.RESULTS_DIR / 'calibration.json'
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\nIn-corpus range: {min(inside):.6f}–{max(inside):.6f}")
    print(f"Out-of-corpus range: {min(outside):.6f}–{max(outside):.6f}")
    print(f"Gap: {gap:.6f}; midpoint suggestion: {suggested}")
    print(f"Wrote {path}")
    if suggested is None:
        print('The groups overlap. Inspect false accepts/refusals before choosing a cutoff.')


if __name__ == '__main__':
    main()
