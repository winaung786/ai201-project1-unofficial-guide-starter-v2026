# Submission status

Repository: https://github.com/winaung786/ai201-project1-unofficial-guide-starter-v2026

- Complete: document ingestion, custom chunks, embeddings, vector search,
  relevance gate, grounded prompt, and command-line interface.
- Complete: five fixed questions and five acceptance targets with rationales;
  criteria 4–5 are explicitly disclosed as AI-assisted. Their original
  numerical targets remain unchanged from the pre-calibration commit.
- Complete: README with the five required sections, five real sample chunks,
  ten real calibration distances, and a real sourced Gemini answer.
- Complete: 10 regression tests, 10 environment checks, and verification that
  all five out-of-scope questions are refused with zero model calls.
- Complete: personal fork created under winaung786. Local project history
  includes more than the four required milestone commits.
- Publication: the connected GitHub service is publishing the local milestones
  in their original order because command-line Git has no saved credentials.
  Original local commit IDs and dates are recorded in the GitHub commit
  messages; the original local history is retained separately.
- Course Portal submission will be handled by the student, as requested.

The AI-use report describes the actual assistance and student actions. It does
not invent independent authorship of the criteria or student code edits. The
assignment's student-authorship requirement still merits the student's review.

Keep this same repository for the next unit. The week-2 repeated evaluation
has not been run or fabricated.

To reproduce locally from this folder on Windows:

```powershell
.\.venv\Scripts\python.exe -X utf8 test.py
.\.venv\Scripts\python.exe -X utf8 app.py index
.\.venv\Scripts\python.exe -X utf8 app.py ask "How are juniors and seniors ordered in the housing lottery?"
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
```

The private key remains in `.env`, which Git ignores. `RUNNING.md` contains
instructions for recreating the environment on another machine.
