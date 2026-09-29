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
- A subsequent scorer-enabled **live** rerun used a rebuilt index and the
  existing Gemini model. The two complete new JSON/Markdown logs in `results/`
  record three uncached trials per fixed question, with `scored: true`,
  15/15 scorer passes and 15/15 gate refusals before and after. The first
  attempt hit a rate limit after 14 answers, produced no complete log, and
  is not included in the results. The successful runs used only an evaluation
  pacing override of eight requests per minute. `README.md` contains new
  criterion-level tables and exact provenance, while retaining the original
  run evidence and clearly labeled retrospective score reports.
- The private `.env` and rebuilt local index remain untracked.

To reproduce locally from this folder on Windows:

```powershell
.\.venv\Scripts\python.exe -X utf8 test.py
.\.venv\Scripts\python.exe -X utf8 app.py index
.\.venv\Scripts\python.exe -X utf8 app.py ask "How are juniors and seniors ordered in the housing lottery?"
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
```

A Gemini key is needed in a local `.env` to repeat live model runs; Git ignores
that file. `RUNNING.md` contains instructions for recreating the environment
on another machine.

### Optional post-evaluation stretch iteration

After the required one-change Unit 2 work, a separate retrieval-only probe
found two real answer-bearing chunk misses in six additional covered questions.
The optional lexical rerank of nearby semantic candidates changed that result
from 4/6 to 6/6. Both full chunk/distance logs are saved as
`results/stretch_probe_before.json` and `results/stretch_probe_after.json`.
Four of five near-topic unsupported questions still pass the relevance gate;
their failure stage and mechanism are stated in `README.md`. The original
five-criterion live verdicts remain historical and were not relabeled or
presented as a new Gemini run. The tests now include two focused rerank guards
in addition to the original 17.

### September 29 grading-feedback and reproducibility follow-up

- A reviewer guide at the top of `README.md` maps both uncredited rubric
  items to the existing measured stretch change and six individual
  supplemental failure diagnoses. It does not claim an awarded grade.
- Fixed the probe's before/after mode selection and prevented overwriting
  historical logs. Production retrieval behavior is unchanged. All 20
  automated tests passed, including a vector-only baseline regression test.
- A new three-trial vector-only baseline was saved. The execution environment
  then blocked unidentified embedding-runtime telemetry; no new paired after
  run completed. The unpaired file is labeled as such in the README. The
  earlier completed before/after logs remain unchanged and support the
  documented stretch measurement.
- The five original targets, original questions, corpus, and original live
  model transcripts remain unchanged. The instructor must determine whether
  the supplemental diagnoses satisfy the original-miss rubric item.

### User-approved telemetry opt-out and retry

- Added ONNX Runtime's explicit telemetry opt-out before embedding sessions;
  Chroma's existing telemetry opt-out remains in place.
- The retry saved both new three-trial probe files: before retrieval 4/6 in
  every trial, after 6/6 in every trial; near-topic gate refusals stayed 1/5.
  These are real saved retrieval/gate outputs with no generated answers.
- All 20 automated tests passed separately with a successful exit.
- The evaluation command's final completion was again blocked by automatic
  review of unidentified runtime telemetry. This remains an execution
  limitation, not a resolved blocker. The README distinguishes the complete
  saved trial records from the unconfirmed final process exit.

Detailed evidence, solo checks, and milestone-order limitations are recorded
in [ASSIGNMENT_REVIEW.md](ASSIGNMENT_REVIEW.md).
