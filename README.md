# The Unofficial Guide

Win Aung · Corpus: `campus_life` · Prepared with Codex assistance

Repository: https://github.com/winaung786/ai201-project1-unofficial-guide-starter-v2026

**Status:** The technical implementation and required README evidence are
complete, and real calibration and a sourced model answer are recorded.
Criteria 4–5 were written by the student and pressure-tested with Claude, with
the original targets preserved in [Criteria history](CRITERIA_HISTORY.md). See
[Assignment review](ASSIGNMENT_REVIEW.md)
for the requirement check, solo review, and recorded milestone-order limitations.
Passing development tests is not the grading standard for this unit.
No stretch features are claimed.

## What This Does

The Unofficial Guide searches 88 fictional student posts supplied by CodePath.
It handles questions about dining waits, housing, laundry, study rooms, and
campus administrative rules. It retrieves evidence with local embeddings and
Chroma, rejects distant matches before a model call, and asks Gemini to answer
only from retrieved documents with filenames. These course documents are
practice material, not verified advice about an actual university.

On this Windows machine, the virtual environment is already in `.venv`.
Run these commands from the project folder:

```powershell
.\.venv\Scripts\python.exe -X utf8 app.py index
.\.venv\Scripts\python.exe -X utf8 app.py retrieve "How are juniors and seniors ordered in the housing lottery?"
.\.venv\Scripts\python.exe -X utf8 app.py ask "How are juniors and seniors ordered in the housing lottery?"
```

Retrieval runs without a key. For generated answers, privately replace the
placeholder in `.env` with your Gemini key and run `python test.py` inside
the virtual environment. On a new machine, follow `RUNNING.md` to create the
environment and install `requirements.txt`. Never commit `.env`.

## Chunking Strategy

**Function:** `chunker.py::split_documents`  
**Chunk size:** 450 characters, a soft limit including the title.  
**Overlap:** Up to 100 characters of complete trailing sentences, when they
fit alongside the next sentence. Titles are repeated separately.

The starter produced 88 chunks from 88 posts at its original 800/120 settings:
average 317 characters, shortest 178, longest 549. Reading the laundry and
dining posts showed that prices, payment rules, and timing caveats belong
together. A 450-character limit leaves the typical 317-character post intact
while splitting the three longest housing posts into complete sentences.

Long posts repeat their title so a later chunk still identifies its building.
Sentence overlap is variable, including zero when no complete sentence fits;
it never copies an arbitrary half-sentence. An unusually long sentence may
exceed the soft limit to preserve its meaning. This lightweight sentence
heuristic suits these documents but can misread abbreviations in other corpora.
Rebuild the index if you change this strategy.

Measured custom output: 91 chunks, 309 characters on average (shortest 159, longest 432), produced by chunker.py::split_documents.

## Sample Chunks

These are the actual five samples from `python app.py chunks -n 5`. The command
uses a deterministic stride, not random sampling. All five printed examples
are first pieces (#0); they do not exercise the later pieces of split posts.
See [split-post inspection commands](ASSIGNMENT_REVIEW.md#inspecting-the-split-posts)
for a targeted check of those boundaries.

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```text
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160_exams.txt#0` — produced by: `chunker.py::split_documents`

```text
BIOL 160 Cell Biology — assessment

Four unit tests and a cumulative final. Not curved.

The unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_math_220_exams.txt#0` — produced by: `chunker.py::split_documents`

```text
MATH 220 Linear Algebra — assessment

Two midterms and a cumulative final. Curved to a b- median.

The problem sets are the course; the lectures make sense afterwards rather than during.
```

**Chunk 4** — source: `dining_the_ridgeway_cafe.txt#0` — produced by: `chunker.py::split_documents`

```text
The Ridgeway Café

Second-year here. Wait times: 10 to 15 minutes at 12:30, none after 2:00. The thing worth going for is the only place on campus with real espresso. The thing to know is that seating is tight; about 40 seats for a building of 900.

Hours are 7:00am to 4:00pm weekdays only. Costs declining balance only, no meal swipes.
```

**Chunk 5** — source: `housing_morrow_house.txt#0` — produced by: `chunker.py::split_documents`

```text
Morrow House — what it's actually like

Just finished a year in this building. Built 1954, partially renovated 2008. Rooms are singles and doubles, hall bathrooms. The good: cheapest housing tier by about $900 a year, and the singles are real singles. The bad: known damp problem on the ground floor; two rooms were taken offline in 2024. Laundry costs $1.50 wash, $1.25 dry, coin or card.
```

The samples answer, respectively: when adding/dropping is allowed; how BIOL
160 is assessed; how MATH 220 is assessed; when and how to eat at Ridgeway;
and what Morrow House offers and what its drawbacks are. Each has a topic
title and intact statements. This inspection is not the week-2 evaluation.

## Sample Answer

<!-- LIVE_SAMPLE_START -->
**Question:** How are juniors and seniors ordered in the housing lottery?

**Answer (actual application output):**

```text
Juniors and seniors are ordered by accumulated credit hours first, with ties broken randomly (`admin_housing_lottery.txt`).

Sources cited in answer: admin_housing_lottery.txt
```

Captured by `capture_sample.py::main` through `app.py::ask_pipeline`; raw output is in `results/sample_answer.json`. Codex checked the answer against `admin_housing_lottery.txt`: both credit-hour ordering and random tie-breaking are explicitly stated in that source.
<!-- LIVE_SAMPLE_END -->

<!-- CALIBRATION_START -->
**Chosen relevance cutoff:** `0.6` (cosine distance, strictly less than).
**Top-k:** `5`. **Embedding model:** `all-MiniLM-L6-v2` (real local ONNX model).

The covered questions ranged from 0.179727 to 0.372583; unrelated questions
ranged from 0.824593 to 0.934011. The gap is 0.452010. Its midpoint is about
0.598588, so the rounded cutoff of 0.6 keeps a similar margin on either side.
This happens to match the starter default, but is now backed by measurements.
All five covered questions pass and all five unrelated questions fail the gate.
These are calibration observations, not proof about unseen questions or model
answer quality. Near-topic questions remain a risk.

| Question | In corpus? | Best cosine distance | Gate |
|---|---|---:|---|
| How are juniors and seniors ordered in the housing lottery? | Yes | 0.224974 | Pass |
| How long is the lunch wait at Kestrel Commons between 12:15 and 1:00? | Yes | 0.179727 | Pass |
| How much does one wash cost in Aldridge Hall, and how do you pay? | Yes | 0.262307 | Pass |
| How far ahead can I book a group study room, and how many blocks can I book per week? | Yes | 0.195768 | Pass |
| How much printing credit does each student get per semester, and does it roll over? | Yes | 0.372583 | Pass |
| What is the capital of Mongolia? | No | 0.824593 | Refuse |
| How do I change the oil in a diesel engine? | No | 0.934011 | Refuse |
| Who won the 1994 World Cup? | No | 0.885860 | Refuse |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.844232 | Refuse |
| How do I write a for loop in Rust? | No | 0.895998 | Refuse |

Measured by `calibrate.py::main` via `store.py::search`; complete top-five
chunks and full-precision distances are in `results/calibration.json`.
Reproduce with `python app.py index`, then `python calibrate.py`.

Inspection of the first three questions found the answer in the top result
for housing lottery rules, Kestrel lunch waits, and Aldridge laundry prices.
The study-room and printing questions also have direct supporting top results.
Top-k remains 5 to retain corroborating posts (the original and follow-up
Kestrel posts, and both Aldridge posts). Lower-ranked results can concern other
buildings: the grounding instruction explicitly requires matching the named
building/service and preserving exact prices and exceptions. A cutoff on the
best result does not make every retrieved chunk relevant.

The prompt uses only retrieved documents, demands filenames next to claims,
and instructs the model to refuse unsupported details. The application also
checks the returned answer: a model refusal is reported as a refusal, and a
substantive answer without a retrieved filename is refused instead of being
presented as grounded. Cited sources and all retrieved sources remain separate
in the structured result. The prompt also treats commands inside documents as
data. The housing-lottery sample has now been tested live and checked against its
source. This single example does not establish grounding for every question;
the five-question repeated answer evaluation belongs to the next unit.
<!-- CALIBRATION_END -->

## How I Used AI

**Disclosure:** Codex helped implement the project and draft this report.
Criteria 1–3 come from the assignment; the questions and rationales for 1–3 were
drafted with Codex. I wrote criteria 4 and 5 myself on September 14, 2026, after
reading my chunks and the Aldridge Hall and Morrow House documents. I used Claude
to pressure-test them: it asked how a grader would check each sentence and pointed
out weak spots, and I then added the comparison against the original documents
and the rule that a refusal counts as a failure. The wording of 4 and 5 is mine.
The original criteria were saved before calibration; these revisions came
afterward and are documented in [CRITERIA_HISTORY.md](CRITERIA_HISTORY.md).

**1. Building and checking the chunker.** I gave Codex the assignment and asked
it to work on the project, then asked it to choose suitable options. It read
the campus posts and implemented a 450-character soft limit, complete-sentence
overlap up to 100 characters, and repeated titles. The result preserves normal
short posts while splitting the three longest ones. Codex also corrected an
overlap test whose initial budget allowed an extra sentence to fit. These were
AI implementation and test edits; I am not claiming I made them manually.

**2. Connecting the model and documenting a real answer.** When Codex reported
that a private Gemini key was required, I added it to `.env` and told it the
key was ready. Codex then ran the environment check, captured an actual answer
about housing-lottery ordering, and checked its claims against the named file.
The report changed from a clearly marked missing-key status to actual model
output and evidence. I also signed in to GitHub so the completed local history
could be uploaded to my fork. The source documents, real distance scores, and
saved answer are available for checking rather than relying on AI assurances.

## Unit 2 — Partial Baseline (September 22, 2026)

**Status: blocked before generated-answer evaluation.** This checkout was
cloned from the same Unit 1 repository. It has no private `.env` or
`GEMINI_API_KEY`, and the index was correctly excluded from Git. After installing
the documented dependencies and local SOCKS proxy support, the real ONNX
embedding model loaded and `python app.py index` rebuilt 91 chunks from the
unchanged 88-document `campus_life` corpus. The 13 regression tests passed.

The original five current Unit 1 criteria remain in `criteria.md`; earlier
versions of criteria 4 and 5 remain in `CRITERIA_HISTORY.md`. The three
credential-free baseline passes are saved with full retrieved chunk text,
distances, gate decisions, and chunk inspections in
[`results/unit2_offline_before.json`](results/unit2_offline_before.json).
`tools/unit2_offline_baseline.py` reproduces this partial measurement against
the current index. All three passes used the original questions and settings.

| Criterion | Original current target | Local pass 1 | Local pass 2 | Local pass 3 | Unit 2 verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | At least 4 of 5 covered questions | 5/5 | 5/5 | 5/5 | Pending complete evaluation |
| 2. Every answer names a source | Every substantive answer | No model answers | No model answers | No model answers | Not evaluated |
| 3. Relevance gate stops unrelated questions | At least 4 of 5 refused | 5/5 | 5/5 | 5/5 | Pending complete evaluation |
| 4. Chunks preserve sentences and source boundaries | All six chunks from three named posts | 6/6 | 6/6 | 6/6 | Pending complete evaluation |
| 5. Cited sources support the claims | At least 4 of 5 covered answers | No model answers | No model answers | No model answers | Not evaluated |

Representative **actual local pipeline output** from the partial baseline:

```text
Question: How much does one wash cost in Aldridge Hall, and how do you pay?
0.262307 housing_aldridge_hall_laundry.txt#0:
Laundry in Aldridge Hall

Machines take $1.75 wash, $1.50 dry, card only.

Question: What is the capital of Mongolia?
Best cosine distance: 0.824593; gate refused: True
Answer: I don't have enough information about that.
```

The first excerpt comes from `store.py::search` using a chunk produced by
`chunker.py::split_documents`. The second refusal comes from
`app.py::ask_pipeline` and `gate.py::check`/`gate.py::REFUSAL`. Full text and
full-precision distances for each local pass are in the JSON evidence file.

For criterion 1, the listed source chunk in each top-five retrieval contains
the necessary answer to every part of its question. For criterion 3, the real
`app.py::ask_pipeline` returned the exact refusal string before generation for
all five unrelated questions in every pass. For criterion 4, the six chunks
printed by `app.py chunks --from-doc` were inspected against their three source
posts, and the script checked their labels, titles, complete final sentences,
and presence of their segments in the corresponding originals. These checks
do not measure how Gemini answers or cites the retrieved material.

`python run_eval.py --label before` was attempted with caching disabled by its
existing implementation. It stopped at the first question in
`generate.py::_get_client` with `No valid GEMINI_API_KEY found`; it wrote no
before run log. Therefore there is no full baseline, no honest verdict on all
five criteria, no diagnosed generated-answer failure, no chosen improvement,
and no after run. The saved Unit 1 sample answer is historical evidence, not
a substitute for three new live responses. Once a private key is available in
the evaluation environment, run the unchanged full baseline before making
the one measured improvement. Never commit `.env` or a key.
