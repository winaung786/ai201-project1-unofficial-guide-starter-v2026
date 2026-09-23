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

## Unit 2 — September 22, 2026

- Complete: same repository, unchanged original five criteria and five fixed
  questions; earlier Unit 1 criterion wording retained in CRITERIA_HISTORY.md.
- Complete: three uncached live answers per covered question both before and
  after one measured retrieval change, with real logs and full JSON evidence
  in results/; the five unrelated questions were checked three times per run.
- Complete: one criterion-level row per original criterion, honest MET/MISSED
  decisions, source-backed reasoning, and representative real system output
  in README.md. All five criteria were MET in both evaluations.
- Complete: retrieval diagnosis based on other-building distractor chunks;
  only config.TOP_K changed from 5 to 1 for the RAG pipeline.
- Complete: after comparison, remaining limitations, What I'd Do Differently,
  and an accurate AI-assistance disclosure in README.md.
- Complete: existing regression tests pass (14). The actual Gemini model was
  used and the private .env remains ignored by Git.
- Complete: multiple Unit 2 commits keep baseline evidence earlier than the
  retrieval change and after evidence later. No Unit 1 history was rewritten.
- The student handles Course Portal submission, as previously requested.

The five fixed questions all passed before improvement; lower-ranked
other-building context and excess prompt tokens were the measured weakness.
Top-k 1 removed those chunks in these trials, but wider multi-document and
near-topic cases remain untested. No score increase is claimed.

### Week 2 final evidence audit — September 23, 2026

- The required `scorer.py::judge` is present. All 17 automated tests pass in
  the fresh checkout.
- The original three-run before/after JSON files are unchanged. Their
  question-level Markdown score columns are blank because those live runs
  predate `scorer.py`. `score_saved.py` now produces separate, clearly labeled
  retrospective scorer reports from those real answers: 15/15 before and
  15/15 after. It does not make a new model call or claim a fresh live rerun.
- The five criterion-level run rows, original Unit 1 targets, source-backed
  review, single top-k improvement, comparison, and limitations remain in
  `README.md`. The earlier pre-calibration wording for criteria 4 and 5 now
  also appears directly underneath those criteria in `criteria.md`.
- The final scorer and retrospective reports are published to this same GitHub
  repository. A new live rerun with scorer-enabled raw logs would require a
  Gemini key and rebuilt local index in this fresh checkout; it was not done.

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
