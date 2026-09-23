# Retrospective scorer results — before

These pass/fail results were calculated by `score_saved.py` using
`scorer.py::judge` on the real answers already saved by `run_eval.py`.
**No model was called and no retrieval was rerun for this report.**
The original JSON and Markdown run logs remain unchanged.

- Original live evidence: `run_2026-09-22_1250_before.json`
- Original JSON SHA-256: `43cc28f76d7bb6cfe02f673f3a6ee7e7a01a7df0e5862b21ce295e1a87d4b4e9`
- Original runs per question: 3; cache disabled in source log
- Substring scorer passed: 15/15 saved covered trials

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| How are juniors and seniors ordered in the housing lottery? | pass | pass | pass |
| How long is the lunch wait at Kestrel Commons between 12:15 and 1:00? | pass | pass | pass |
| How much does one wash cost in Aldridge Hall, and how do you pay? | pass | pass | pass |
| How far ahead can I book a group study room, and how many blocks can I book per week? | pass | pass | pass |
| How much printing credit does each student get per semester, and does it roll over? | pass | pass | pass |

This quick substring check cannot detect unsupported extra claims.
The criterion-level judgments and manual source checks are in `README.md`.
