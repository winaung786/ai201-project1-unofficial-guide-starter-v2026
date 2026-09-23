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

## Unit 2 — Testing the Same RAG System (September 22, 2026)

This unit uses the unchanged `campus_life` corpus, original five fixed questions,
MiniLM embeddings, Gemini model, chunker, cutoff 0.6, and original criteria in
[`criteria.md`](criteria.md). Earlier Unit 1 wording for criteria 4 and 5 is
preserved in [`CRITERIA_HISTORY.md`](CRITERIA_HISTORY.md). The Unit 2 evaluation
harness records actual application answers, including post-generation citation
checks, with caching disabled for all model trials. This logging change does not
change how ordinary questions are answered.

The required Week 2 scorer is implemented in [`scorer.py`](scorer.py) with the
exact `judge(question, expects, answer, results) -> bool` interface used by
`run_eval.py`. It performs the class's deliberately simple, case-insensitive
substring check. The criterion-level source and grounding judgments below
remain manual because that scorer cannot detect an unsupported extra claim.
The scorer was also applied to the saved real evaluation answers: all 15 before
answers and all 15 after answers passed. The per-question record is in
[`results/scorer_verification.md`](results/scorer_verification.md). This
verification did not regenerate or change the original uncached model runs.
The original before/after Markdown files still show blank automatic scorer
columns because they were generated before `scorer.py` existed. To make this
timing clear, `score_saved.py` applies the scorer to the saved live answers and
writes separate [before](results/run_2026-09-22_1250_before_scored.md) and
[after](results/run_2026-09-22_1252_after_scored.md) question-level score
tables. These are **retrospective scores, not fresh model runs**. A fresh live
rerun with the scorer active still requires a configured Gemini key and index.

### Run Log — Before

Commands: `.venv/bin/python app.py index` and
`.venv/bin/python run_eval.py --label before` after `python test.py` and the
regression suite. The index contained 91 chunks from 88 documents. The full
before log is in [`results/run_2026-09-22_1250_before.md`](results/run_2026-09-22_1250_before.md);
its [JSON evidence](results/run_2026-09-22_1250_before.json) contains all
retrieved chunks, full distances, gate decisions, raw model answers, answers
shown by the application, and cited sources. Fifteen separate Gemini answers
were generated without cache; the gate blocked all 15 out-of-scope trials
before a model call. The three deterministic chunk checks are recorded in
[`results/unit2_offline_before.json`](results/unit2_offline_before.json).

| Criterion | Original Unit 1 target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---:|---:|---:|---|
| 1. Retrieved chunks contain the answer | At least 4 of 5 covered questions | 5/5 | 5/5 | 5/5 | MET |
| 2. Every substantive answer names a source | Every answer produced | 5/5 | 5/5 | 5/5 | MET |
| 3. Relevance gate stops unrelated questions | At least 4 of 5 refused | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks preserve sentences and source boundaries | All six chunks from the three named posts | 6/6 | 6/6 | 6/6 | MET |
| 5. Cited sources support the claims | At least 4 of 5 covered answers | 5/5 | 5/5 | 5/5 | MET |

Representative **real system output**, produced by `run_eval.py::run_once`
through `app.py::ask_pipeline`, `store.py::search`, `gate.py::check`, and
`generate.py::answer_from_chunks` (covered question, run 1):

```text
Question: How much does one wash cost in Aldridge Hall, and how do you pay?
Best cosine distance: 0.262307; relevance gate: passed
Retrieved: housing_aldridge_hall_laundry.txt#0 — Machines take $1.75 wash, $1.50 dry, card only.
Answer: In Aldridge Hall, a wash costs $1.75 and is card only. (housing_aldridge_hall_laundry.txt and housing_aldridge_hall.txt)
```

Both cited Aldridge files state the same price and payment rule. The chunks
were produced by `chunker.py::split_documents`. The full retrieved chunk text
and precise distance are in the before JSON. A real refusal (out-of-scope run
1, `app.py::ask_pipeline` / `gate.py::REFUSAL`):

```text
Question: What is the capital of Mongolia?
Best cosine distance: 0.824593; relevance gate: refused
Answer: I don't have enough information about that.
```

### Verdicts

1. **MET:** For each of the five covered questions, at least one of the top
   five chunks contained all requested facts, in each of three retrieval runs.
   The housing lottery, Kestrel Commons wait, Aldridge laundry, study room
   limits, and printing credit were each present in a correctly named source.
2. **MET:** All 15 substantive answers named at least one retrieved filename.
   No covered answer was rejected by the application's citation check. Gate
   refusals did not invent citations and belong under criterion 3.
3. **MET:** The gate refused all five fixed unrelated questions in each of
   three runs (15/15) with the required exact refusal text and zero model
   calls for those questions.
4. **MET:** `python app.py chunks --from-doc FILENAME` showed two pieces from
   each of Innisfree Hall, Morrow House, and Old Brewhouse. All six had their
   own post's title and complete sentences. The six pieces were inspected
   against their original posts; no foreign post text appeared.
5. **MET:** Manual review of each of the 15 answers against the original
   cited documents found the correct named service/place and all requested
   values: credit-hour order with random ties, 20–25 minutes at Kestrel,
   $1.75/card only at Aldridge, two weeks/two blocks for study rooms, and
   $30/no rollover for printing. Other factual details in these concise
   answers were also supported by their cited source(s). No refusal was
   counted as a successful covered answer. The `expects` strings alone were
   not used as proof.

### Diagnoses

**No original criterion was missed**, so there is no failed criterion to
relabel, revise, or explain away. The original targets remain unchanged.
There is nevertheless a measurable retrieval weakness: the top-five context
includes unrelated, same-topic posts. For Kestrel, ranks 3–5 describe
Ridgeway Café, Halden Hall, and North Kitchen with different waits; for
Aldridge, ranks 2, 4, and 5 describe Innisfree or Old Brewhouse laundry with
other payment methods and prices. This originates in **retrieval**: semantic
similarity favors nearby dining/laundry terms even for different named places.
`app.py::ask_pipeline` hands all five chunks to generation once the best hit
passes the gate; the model then must distinguish the named location itself.
The before answers happened to distinguish them correctly in all 15 trials.
This is an observed context-quality defect and a future answer-confusion risk,
not a fabricated missed criterion.

### The Improvement — Selected Before Implementation

Observed failure → diagnosis → chosen improvement: irrelevant other-building
chunks enter the prompt → top-five semantic retrieval includes lower-ranked
same-topic posts → reduce only `config.TOP_K` from **5 to 1**. Each original
question's highest-ranked chunk already contains the full answer, including
Kestrel's corroborating follow-up, so this should remove misleading context
while keeping the required facts. It also removes corroborating documents and
might make answers worse; the unchanged five questions, model, corpus, cutoff,
and criteria must be rerun to find out. This is the **only planned primary RAG
change**; evidence logging is evaluation infrastructure, not an answer change.

### Run Log — After

After the single change to `config.TOP_K`, I ran the **same** command with a
new label: `.venv/bin/python run_eval.py --label after`. No question, corpus,
model, chunking rule, relevance cutoff, or original target changed. The
[after run log](results/run_2026-09-22_1252_after.md) and its [full JSON
transcript](results/run_2026-09-22_1252_after.json) record another 15 uncached
Gemini answers, all retrieved chunks/distances, and 15 gate trials. The
[after chunk checks](results/unit2_chunks_after.json) repeated the six
named-chunk inspections three times using the unchanged chunker.

| Criterion | Original Unit 1 target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---:|---:|---:|---|
| 1. Retrieved chunks contain the answer | At least 4 of 5 covered questions | 5/5 | 5/5 | 5/5 | MET |
| 2. Every substantive answer names a source | Every answer produced | 5/5 | 5/5 | 5/5 | MET |
| 3. Relevance gate stops unrelated questions | At least 4 of 5 refused | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks preserve sentences and source boundaries | All six chunks from the three named posts | 6/6 | 6/6 | 6/6 | MET |
| 5. Cited sources support the claims | At least 4 of 5 covered answers | 5/5 | 5/5 | 5/5 | MET |

Representative **real after output** (`run_eval.py::run_once` through
`app.py::ask_pipeline`; the retrieved chunk is from
`chunker.py::split_documents` and `store.py::search`):

```text
Question: How much does one wash cost in Aldridge Hall, and how do you pay?
Best cosine distance: 0.262307; relevance gate: passed
Only retrieved chunk: housing_aldridge_hall_laundry.txt#0
Answer: One wash in Aldridge Hall costs $1.75, and you can pay by card only (housing_aldridge_hall_laundry.txt).
```

**Verdicts:** Each criterion was judged the same way as before. Every covered
question had all requested facts in its sole retrieved chunk in each run; all
15 produced answers named a retrieved source; all 15 unrelated questions were
blocked by the gate with the required refusal; all six named chunks preserved
sentences and source boundaries in each repeat; and manual review found all
15 answers' factual claims supported by their cited original documents. No
covered refusal or borderline result was counted as a pass.

### Before vs. After

| Measured item | Before | After | Interpretation |
|---|---:|---:|---|
| Covered answers passing source-backed manual review | 15/15 | 15/15 | Unchanged on these fixed questions |
| Gate refusals for unrelated questions | 15/15 | 15/15 | Unchanged |
| Retrieved chunks handed to generation per covered question | 5 | 1 | Four lower-ranked chunks no longer reach the model |
| Model calls for 15 covered questions | 15 | 15 | Both are uncached live runs |
| Prompt tokens reported by the model | 10,299 | 4,557 | 5,742 fewer |
| Total tokens reported by the model | 10,842 | 5,047 | 5,795 fewer, about 53% |

The selected change **succeeded at its measured target**: the other-building
chunks no longer entered the prompt and model-reported token use fell. It did
not improve the five criterion scores because all five already met their
original targets in the baseline. Nothing became worse on these five fixed
questions in three trials, but reducing the evidence to one chunk could harm
questions that require combining sources; these trials do not measure that.
Both model runs can also vary naturally, so the token difference is a measured
comparison for these trials, not a universal cost guarantee.

### What's Still Broken

**No original criterion remains MISSED after the change.** The evaluation is
limited to five covered questions and five clearly unrelated ones. A near-topic
unsupported question might pass the distance gate, and a question requiring
facts from multiple source documents might suffer under top-k 1. Next I would
try a separate, fixed multi-document and near-topic test set before adopting
top-k 1 for wider use. I did not make another RAG change in this unit because
the assignment calls for exactly one measured improvement and a repeated test
of the same five original criteria. The sample does not prove that all future
answers will be grounded.

### What I'd Do Differently

Next time I would make **criterion 5** more repeatable before seeing any
answers: write a claim-level answer key for each fixed question, with the
required place, exact numbers or limits, acceptable cited filenames, and an
explicit rule for any extra factual claim. The existing original-document
comparison made manual scoring possible here, but two reviewers could still
disagree about whether an extra clause is fully supported. I would also state
clearly in criterion 2 that its source-name requirement applies to substantive
answers, while an honest refusal is assessed under criterion 3. I would keep
criterion 4's source-boundary check but specify its sentence test in advance.
These are suggestions for a future test plan; the Unit 1 criteria and their
recorded history were not retroactively rewritten.

### How ChatGPT Helped in Unit 2

Codex inspected the existing pipeline and original criteria, prepared logging
that captures the actual application answer and complete retrieved evidence,
ran the live before and after evaluations, checked claims against the original
posts, identified unrelated lower-ranked chunks, made the single retrieval
setting change, and drafted this evidence-based comparison. The model's real
outputs and usage measurements are saved separately from Codex's judgment.
No student-only work, class discussion, or independent student authorship of
this Unit 2 text is claimed.
