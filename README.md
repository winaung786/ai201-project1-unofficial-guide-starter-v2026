# The Unofficial Guide

Corpus: `campus_life` · Prepared with Codex assistance

**Status:** Local search and calibration are complete; 10 regression tests pass. A private Gemini API key, a
student review of the criteria and AI reflection, and a personal GitHub fork
are still needed before submission. See `WORK_LOG.md` for the actual work
history. No stretch features are claimed.

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

These are the actual five samples from `python app.py chunks -n 5`.

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
**Live generated answer pending:** No valid Gemini key has been configured.
A model answer has not been generated or verified; no invented answer is
presented as program output here. After adding your key privately to `.env`,
run `python test.py`, then `python capture_sample.py`. The latter captures
one real answer and its source filenames into this section automatically.
Review the output before submitting.
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
and instructs the model to refuse unsupported details. It also treats commands
inside documents as data. These instructions still need live testing once the
Gemini key is configured; they cannot guarantee factual grounding by themselves.
<!-- CALIBRATION_END -->

## How I Used AI

**Disclosure:** This is an AI-assisted draft. The student asked Codex to work
on the assignment and to choose suitable options. The student has not yet
supplied a personal reflection or independently authored criteria 4 and 5.
The following describes actual assistance rather than inventing student edits.

**1. Chunking implementation.** Codex read the starter and five campus posts,
measured the original chunk sizes, and implemented a title-preserving sentence
chunker with bounded sentence overlap. It kept ordinary posts intact and
changed the long-post behavior instead of claiming that the original chunker
split all posts badly. The student should inspect the five examples and explain
which design choices they accept or change.

**2. Reproducible verification.** Codex installed the dependencies, wrote
boundary and gate tests, and separated local retrieval measurements from live
model verification. One overlap test initially used a budget large enough to
fit an extra sentence; Codex corrected the test budget so it actually exercised
the intended split. The missing API key is recorded instead of treating a
mocked response as a real sample answer. The student should replace this draft
with their own account of what they reviewed and changed.
