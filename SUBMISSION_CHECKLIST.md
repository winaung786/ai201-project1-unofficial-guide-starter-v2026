# Submission status

Repository: https://github.com/winaung786/ai201-project1-unofficial-guide-starter-v2026

- Complete: document ingestion, custom chunks, embeddings, vector search,
  relevance gate, grounded prompt, and command-line interface.
- Present: five fixed questions and five numbered targets with rationales.
- Revised: the student wrote criteria 4–5 and used Claude only to pressure-test
  how a grader would check them; the original wording and later revision date
  are preserved in CRITERIA_HISTORY.md.
- Complete: README with the five required sections, five real sample chunks,
  ten real calibration distances, and a real sourced Gemini answer.
- Complete: 13 regression tests, 10 environment checks, and verification that
  all five out-of-scope questions are refused with zero model calls.
- Complete: personal fork created under winaung786. Local project history
  includes more than the four required milestone commits.
- Complete: all seven local milestones were published through the connected
  GitHub service in their original order. The published file tree exactly
  matches the original final local snapshot. Original local IDs and dates
  are recorded in commit messages, and the original commits are retained
  on the local `original-local-milestones` branch. The working `main` branch
  tracks the published GitHub history.
- Course Portal submission will be handled by the student, as requested.

The AI-use report describes the actual assistance and student actions. The
student's authorship note identifies criteria 4–5 as their own wording and
describes Claude's pressure-testing role.

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

Detailed evidence, solo checks, and milestone-order limitations are recorded
in [ASSIGNMENT_REVIEW.md](ASSIGNMENT_REVIEW.md).
