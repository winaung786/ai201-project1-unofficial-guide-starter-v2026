# Evaluation summary — generated from raw JSON

Canonical location for live-run counts and token totals. Regenerate with
`python tools/summarize_evaluations.py`; verify with the same command plus `--check`.
This script makes no retrieval or model calls and does not change raw logs.
Manual criterion verdicts and claim reviews remain in [README](../README.md#verdicts).
The substring scorer column reports only values already recorded in JSON.
Retrospective scoring is separately labeled in [scorer verification](scorer_verification.md).

Different live runs can have different output-token totals. The original pair
and the later scorer-enabled pair are separate measurements, each linked below.
No missing token metadata is estimated; these are the runner's recorded totals.
Request attempts include retries in checkpoint-enabled logs; failed requests may
have no returned token metadata. COMPLETE requires the full trial matrix and
disabled caching; it does not establish factual correctness or a passing criterion.

| Live evidence | Status | Top-k | Runs/question | Covered trials | Gate refused/trials | Scorer | Request attempts | Prompt | Output | Total |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| [before](run_2026-09-22_1250_before.json) | COMPLETE | 5 | 3 | 15 | 15/15 | not recorded | 15 | 10,299 | 543 | 10,842 |
| [after](run_2026-09-22_1252_after.json) | COMPLETE | 1 | 3 | 15 | 15/15 | not recorded | 15 | 4,557 | 490 | 5,047 |
| [before_scored_live](run_2026-09-23_1711_before_scored_live.json) | COMPLETE | 5 | 3 | 15 | 15/15 | 15/15 | 15 | 10,299 | 533 | 10,832 |
| [after_scored_live](run_2026-09-23_1713_after_scored_live.json) | COMPLETE | 1 | 3 | 15 | 15/15 | 15/15 | 15 | 4,557 | 493 | 5,050 |
| [after_stretch](run_20261001T031757487133Z_after_stretch.json) | COMPLETE | 1 | 3 | 15 | 15/15 | 15/15 | 15 | 4,557 | 470 | 5,027 |

## Provenance

| JSON file | Recorded UTC timestamp | SHA-256 |
|---|---|---|
| `run_2026-09-22_1250_before.json` | 2026-09-22T02:50:16.390858+00:00 | `43cc28f76d7bb6cfe02f673f3a6ee7e7a01a7df0e5862b21ce295e1a87d4b4e9` |
| `run_2026-09-22_1252_after.json` | 2026-09-22T02:52:59.040411+00:00 | `3e1a301ff3155b946b35a2060797030cc912376db11faa498cd9763b20ef5150` |
| `run_2026-09-23_1711_before_scored_live.json` | 2026-09-24T00:11:11.944261+00:00 | `e17e9bf128bb4076341f1527aa86acf9e3f4c5243b49c73d7ef1f8c3f0ba2a9f` |
| `run_2026-09-23_1713_after_scored_live.json` | 2026-09-24T00:13:40.318281+00:00 | `46c2072dc2c1d18a1b19157d994fc67a1590d05af9992beebcb869404b0093c9` |
| `run_20261001T031757487133Z_after_stretch.json` | 2026-10-01T03:17:57.487133+00:00 | `8c932b9076909ff10128f452fac72a8c361ebea69a01841c9390502f2d30cd36` |
