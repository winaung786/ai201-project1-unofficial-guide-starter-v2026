# The Unofficial Guide

Win Aung · Corpus: `campus_life` · Prepared with Codex assistance

Repository: https://github.com/winaung786/ai201-project1-unofficial-guide-starter-v2026

**Status:** The original Unit 1/2 evidence is preserved. The current feedback
follow-up is documented below, including evaluation recovery and a separate
post-stretch live evaluation. Real calibration and a sourced model answer are recorded.
Criteria 4–5 were written by the student and pressure-tested with Claude, with
the original targets preserved in [Criteria history](CRITERIA_HISTORY.md). See
[Assignment review](ASSIGNMENT_REVIEW.md)
for the requirement check, solo review, and recorded milestone-order limitations.
Passing development tests is not the grading standard for this unit.
One optional post-evaluation stretch iteration is documented at the end of
the Unit 2 section. It does not replace the original before/after evidence.

## Unit 2 grading feedback — reviewer guide

The latest instructor feedback awards 13 points. It accepts the original
five-criterion before/after evidence and identifies two uncredited rubric items:

| Rubric item | Evidence in the current submission | Scope and limitation |
|---|---|---|
| Every miss names a pipeline stage | All five original criteria passed. [Supplemental diagnoses](#individual-supplemental-misses-and-pipeline-stages) remain documented separately | The instructor explicitly awarded zero for an empty original miss list. Passing criteria cannot honestly be relabeled as failures to obtain these points. |
| A second measured improvement | [Optional stretch iteration](#optional-stretch-iteration--additional-retrieval-diagnosis-and-change) records the lexical change and retrieval-only before/after evidence. A full post-stretch evaluation is documented in the follow-up below | The instructor correctly identified that retrieval probes alone did not supply a third five-criterion, three-run log. Only completed live trials plus source/chunk review count as that missing evidence. |

The original five-criterion tables, targets, and live model transcripts remain
unchanged. This guide requests review of the evidence; it does not claim that
the instructor has awarded additional points or that the grade is now 17/17.
Earlier telemetry-limited attempts remain in the [historical retry record](#telemetry-disabled-retry--recorded-results-and-execution-limit).
Live-run counts and token totals have one generated canonical location:
[evaluation summary](results/evaluation_summary.md). The original and later
scorer-enabled runs are distinct measurements, not interchangeable totals.
README is the canonical location for manual criterion verdicts and diagnoses;
other review/checklist documents link here instead of restating those facts.
The [October 1 follow-up](#october-1-feedback-follow-up) now supplies the third
full criterion table and fresh paired probes. Its [automated test output](results/tests_recovery_20261001.txt)
records all 27 tests passing, including the new recovery checks.

## What This Does

The Unofficial Guide searches 88 fictional student posts supplied by CodePath.
It handles questions about dining waits, housing, laundry, study rooms, and
campus administrative rules. It retrieves evidence with local embeddings and
Chroma, rejects distant matches before a model call, and asks Gemini to answer
only from retrieved documents with filenames. These course documents are
practice material, not verified advice about an actual university.

On Windows, after creating the environment as described in `RUNNING.md`,
run these commands from the project folder:

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
tables. These are **retrospective scores, not fresh model runs**. A separate
scorer-enabled live rerun was subsequently completed and is documented below.

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

#### Individual supplemental misses and pipeline stages

These later diagnostics are separate from the five original acceptance
criteria. Every row below represents an observed supplemental failure in
[`stretch_probe_before.json`](results/stretch_probe_before.json), not a
fabricated original-criterion miss. The corresponding
[after evidence](results/stretch_probe_after.json) records the outcome.

| Supplemental question | Pipeline stage | Observed failure mechanism | Outcome after the stretch change |
|---|---|---|---|
| When does Kestrel Commons close on weekends? | **Retrieval** (`store.py::search`) | Top-1 selected the follow-up at distance 0.428, which lacks weekend hours. The main Kestrel post, present among candidates at 0.505, contains `9:00am to 8:00pm weekends`. The failure is before generation. | Correct main post selected; requested fact present. |
| What is the cost of a cash meal at Kestrel Commons? | **Retrieval** (`store.py::search`) | A North Kitchen post ranked first at 0.472 despite being the wrong location. The Kestrel post at 0.541 contains `$12.50 cash`. Similar dining/payment language outranked the requested location. | Correct Kestrel post selected; requested fact present. |
| What time does Aldridge Hall's laundry room close? | **Relevance gate** (`gate.py::check`) | The laundry post discusses prices and busy periods, not a closing time. Its 0.392 distance passes the 0.6 cutoff because the topic matches. | Still passes the gate: unresolved gate false positive. |
| What is the cancellation fee for a group study room? | **Relevance gate** (`gate.py::check`) | The room post provides reservation limits, not a cancellation fee. Distance 0.396 passes the cutoff without checking whether the fee exists. | Still passes the gate: unresolved gate false positive. |
| What is the Kestrel Commons dinner menu on Fridays? | **Relevance gate** (`gate.py::check`) | The Kestrel post mentions general dining options, not a Friday dinner menu. Topic similarity gives distance 0.422, below the cutoff. | Still passes the gate: unresolved gate false positive. |
| How much is the housing lottery application fee? | **Relevance gate** (`gate.py::check`) | The lottery post explains ordering and dates, not an application fee. Distance 0.515 passes the cutoff even though the requested fact is absent. | Still passes the gate: unresolved gate false positive. |

The four gate failures do **not** establish that Gemini hallucinated: these
probes stopped at retrieval/gating and made zero generation calls. Tightening
the cutoff without further testing could also reject valid paraphrases. That
additional gate change was not made.

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

Model-reported prompt/output/total token counts are generated directly from
each JSON in the [canonical evaluation summary](results/evaluation_summary.md),
under the original `before` and `after` rows. They show reduced token use for
this pair; the later scorer-enabled pair has its own separate rows.

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
the required assignment phase called for exactly one measured improvement and
a repeated test of the same five original criteria. A separate, subsequent
optional stretch iteration is recorded below. The sample does not prove that
all future answers will be grounded.

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
this Unit 2 text is claimed. Codex also prepared the supplemental probe,
retrieval change, and evidence discussion in the optional stretch iteration
below after the grading feedback.

### Scorer-enabled live rerun (September 24, 2026 UTC)

After `scorer.py` was added, I rebuilt the existing index (88 documents, 91
chunks), ran `python test.py` (10/10), and repeated the complete before/after
evaluation using the same fixed questions, `campus_life` corpus,
`gemini-3.5-flash-lite` model, MiniLM embeddings, 0.6 relevance cutoff, and
original targets. These are **new live model runs**, not the retrospective
scores above. `run_eval.py::main` saved the full retrieved text, distances,
gate decisions, generated answers, cited filenames, per-answer scorer results,
and model-reported tokens to these [before JSON](results/run_2026-09-23_1711_before_scored_live.json)
and [after JSON](results/run_2026-09-23_1713_after_scored_live.json), with
readable [before](results/run_2026-09-23_1711_before_scored_live.md) and
[after](results/run_2026-09-23_1713_after_scored_live.md) transcripts.
There were three separate uncached trials per covered question (15 model calls
per phase) and three gate checks per unrelated question (15 refusals per phase).

The first scorer-enabled baseline attempt hit Gemini's request rate limit after
14 answers and saved no complete run log; it is **not** counted in either table.
The successful historical commands below paced calls at eight per minute by
overriding only `config.REQUESTS_PER_MINUTE` in the evaluation process. These
are recorded provenance, not the recommended command today. The supported
`--requests-per-minute 8` option now replaces this ad hoc override:

```bash
.venv/bin/python -c 'import config; config.REQUESTS_PER_MINUTE=8; import run_eval; run_eval.main()' --label before_scored_live --top-k 5
.venv/bin/python -c 'import config; config.REQUESTS_PER_MINUTE=8; import run_eval; run_eval.main()' --label after_scored_live --top-k 1
```

The manual review of this later pair produced the same per-run criterion
counts and verdicts as the [original before table](#run-log--before) and
[original after table](#run-log--after). The automatic counts and model usage
for this separate live pair are in the [generated summary](results/evaluation_summary.md).

For criterion 1, every retrieved context contained the requested facts.
For criterion 2, every substantive answer cited a retrieved source. For
criterion 3, every out-of-scope trial returned the exact gate refusal without
a model call. Criterion 4 is deterministic: the unchanged `chunker.py` was
checked three times in the earlier [before](results/unit2_offline_before.json)
and [after](results/unit2_chunks_after.json) chunk inspections; it was **not**
newly measured by the scorer-enabled answer runner. For criterion 5, I
compared all 30 new answers against their cited original corpus files and
found the requested details and any other factual claims supported. The
simple `scorer.py::judge` also passed all 15 answers in each phase, but its
substring check alone is not proof of criterion 5. No target was lowered.

Representative **real output** for the Aldridge question, run 1, from
`run_eval.py::run_once` through `app.py::ask_pipeline` and
`generate.py::answer_from_chunks` (best cosine distance 0.262307; gate passed
in both phases):

```text
Before, top-k 5: One wash in Aldridge Hall costs $1.75, and it is card only (housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt).
After, top-k 1: One wash in Aldridge Hall costs $1.75, and you must pay by card only (housing_aldridge_hall_laundry.txt).
```

Both answers cite source text containing the price and card-only rule. In
these new trials the five criterion verdicts stayed MET, while top-k 1 again
removed four lower-ranked chunks per covered question. The generated summary's
`before_scored_live` and `after_scored_live` rows record this pair's token
reduction. These totals differ from the original pair because the output
lengths differ. The scorer-enabled rerun supports the
original diagnosis of unnecessary context, not an increase in pass rate.
The separate optional probe below tests near-topic gate behavior; questions
requiring facts from multiple documents remain untested.

### Optional stretch iteration — additional retrieval diagnosis and change

This section was added **after** the required Unit 2 before/after evaluation
and the scorer-enabled rerun. It is a separate supplemental experiment, not a
revision of the five original questions, targets, or historical MET verdicts.
The prior top-k reduction remains the first change. This is a **second,
optional** measured retrieval change, made in response to the grading
feedback's stretch category. Its retrieval-only probes made **zero model
calls**; no new answer or scorer outcomes are claimed.

I selected six additional answerable questions and five near-topic questions
whose requested facts are absent from the same `campus_life` corpus. The
repeatable probe is [`tools/stretch_probe.py`](tools/stretch_probe.py). It
records each selected chunk's full text and cosine distance, five candidate
chunks, gate decision, expected source, and required source phrase in the
[before](results/stretch_probe_before.json) and
[after](results/stretch_probe_after.json) JSON logs. The required source
phrases are compared directly with the retrieved text, not generated answers.

| Supplemental measurement | Before stretch | After stretch |
|---|---:|---:|
| Answerable questions with the required fact in the single selected chunk | 4/6 | 6/6 |
| Near-topic unsupported questions refused by the relevance gate | 1/5 | 1/5 |
| Original five covered questions passing the gate | 5/5 | 5/5 |
| Original five unrelated questions refused by the gate | 5/5 | 5/5 |

**Actual supplemental misses and pipeline stages:**

| Question or group | Before evidence | Stage and mechanism | After |
|---|---|---|---|
| Kestrel weekend closing time | Top-1 `dining_kestrel_commons_followup.txt`, distance 0.428, has no weekend hours; the answer-bearing `dining_kestrel_commons.txt` was among five candidates at distance 0.505 | **Retrieval:** semantic top-1 preferred a short, same-name follow-up over the source with the `weekends` hours sentence | Answer-bearing source selected at 0.505; retrieval miss fixed |
| Kestrel cash meal price | Top-1 `dining_north_kitchen.txt`, distance 0.472, is the wrong location; the answer-bearing Kestrel source was among five candidates at 0.541 | **Retrieval:** similar dining/payment wording outranked the exact named location | Kestrel source with `$12.50 cash` selected at 0.541; retrieval miss fixed |
| Four of five new near-topic unsupported questions | Distances 0.392, 0.396, 0.422, and 0.515 all passed the 0.6 cutoff despite the requested facts being absent; the fifth, at 0.647, was refused | **Relevance gate:** a best cosine distance under 0.6 measures topical similarity, not whether the requested fact exists. This is a supplemental gate false positive; no generation outcome was tested | Still four gate false positives; **not fixed** by the retrieval change |

Observed retrieval failure → diagnosis → change: the correct Kestrel chunks
were present among five semantic candidates but were not ranked first →
`store.py::search` now fetches up to five nearby vector candidates and
reranks them by the fraction of distinct question content words found in each
chunk. The rerank has a 0.15 cosine-distance window and leaves the original
distance visible; the application still returns just one chunk with the
unchanged model, corpus, and 0.6 gate. This is a modest lexical rerank within
the existing vector retrieval system, not a new RAG application. These
particular supplemental questions helped choose the 0.35 lexical weight, so
the 6/6 is a measured result on this small set, **not** independent proof of
general reliability.

Commands run on the same rebuilt 91-chunk index:

```bash
.venv/bin/python tools/stretch_probe.py --label before
.venv/bin/python tools/stretch_probe.py --label after
.venv/bin/python -m unittest discover -s tests -v
```

The stretch result improved **retrieval evidence**, not an answer-quality
score: 4/6 became 6/6 while the two Kestrel distances remained their actual
cosine values. The original fixed questions retained the same selected source
and gate outcome in this retrieval-only check. At the time of this probe,
no full Gemini evaluation had been rerun after the optional change. The
later full evaluation is recorded separately below; historical verdicts
still describe their original runs. Near-topic gate
false positives and possible regressions on unseen questions remain. Next I
would test a separate fixed unsupported and multi-document set with actual
answer review before modifying the gate, since that would be another change.

### September 29 reproducibility check

The previous probe's `--label before` only labeled its output; after the
stretch implementation it would still use the reranker. That is now corrected:
`before` explicitly calls `store.py::search(..., lexical_rerank=False)`, and
`after` enables the existing reranker. Ordinary application retrieval keeps
its existing behavior. New probe runs default to three trials and use
timestamped, exclusively created files so historical evidence cannot be
overwritten. A regression test guards the mode switch; all **20 automated
tests passed** in this recheck.

The index rebuilt with 88 documents and 91 chunks. The new
[unpaired baseline file](results/stretch_probe_before_20260929T164944840663Z.json)
records vector-only retrieval at 4/6 and near-topic gate refusals at 1/5 in
each of three trials. The command sequence was then blocked by the execution
environment because the embedding runtime attempted an unidentified telemetry
request to a Microsoft host. It was not bypassed. No matching new after log
was produced, so this is **not a completed new paired evaluation**. The
completed September 27 supplemental before/after files linked above remain
the evidence for 4/6 → 6/6. No live Gemini rerun or new answer-score claim is
made here.

### Telemetry-disabled retry — recorded results and execution limit

With the user's approval, `store.py::_OnnxEmbedder.__init__` now calls
`onnxruntime.disable_telemetry_events()` before creating an embedding session.
Chroma's separate anonymized telemetry setting was already off. This runtime
setting does not change the corpus, model weights, retrieval scoring, gate,
or questions; it is not a third RAG improvement.

The retry wrote both complete three-trial data files:
[vector-only before](results/stretch_probe_before_20260929T171033457577Z.json)
and [lexical-reranked after](results/stretch_probe_after_20260929T171041558516Z.json).
The console reported every row below, and the saved JSON was checked for all
trial records. These are retrieval/gate executions with **zero generated
answers**, not live Gemini answer evaluations.

| Measurement | Before run 1 | Before run 2 | Before run 3 | After run 1 | After run 2 | After run 3 |
|---|---:|---:|---:|---:|---:|---:|
| Supplemental answer-bearing top-1 chunks | 4/6 | 4/6 | 4/6 | 6/6 | 6/6 | 6/6 |
| Supplemental unsupported questions refused by gate | 1/5 | 1/5 | 1/5 | 1/5 | 1/5 | 1/5 |
| Original covered questions passing gate | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| Original unrelated questions refused by gate | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |

The remaining four near-topic gate false positives are unchanged. Repeated
deterministic retrieval on the same questions checks repeatability; it does
not establish performance on unseen questions. All **20 automated tests
passed** separately, with a successful test-process exit.

**Execution limitation:** after both files and their summaries were written,
the execution environment again denied an unidentified runtime telemetry
request to an untrusted Microsoft endpoint. The ONNX opt-out therefore did
not establish that all runtime telemetry was disabled. No clean final exit
was confirmed for the paired evaluation command. The saved measurements are
preserved as observed output, but this run is **not** described as a cleanly
completed process or a resolved telemetry issue. The blocked request was not
bypassed or authorized for disclosure. The earlier unpaired attempt above
is retained as history, and the original Unit 2 live logs remain unchanged.

### October 1 feedback follow-up

The instructor requested recoverable evaluation, reproducible pacing,
consistent summary numbers, and a third full log after the lexical rerank.
This follow-up changes evaluation/setup reliability and documentation. It
does not add another RAG algorithm change or alter the original five targets.

**Harness reliability.** `run_eval.py` now saves JSON and readable Markdown
after each completed trial. JSON is flushed and atomically replaced before
scoring; a scorer error therefore cannot discard its saved raw answer.
`--resume PATH` skips completed trials, retains earlier usage, and rejects
changes to questions, code, corpus, models, scorer availability, configuration,
or recorded dependency versions. An unfinished request can still need to be
repeated after a crash. `generate.py` has bounded 429 retries; exhausted
retries leave an interrupted checkpoint instead of discarding earlier trials.
Incomplete runs are labeled incomplete and cannot be finalized by `score_saved.py`.

Pacing is now `--requests-per-minute 8`, or `AI201_REQUESTS_PER_MINUTE` through
`config.py`. Each session records its actual rate. The tests inject failure
after 14 synthetic answers, resume only remaining trials, retain raw output
when scoring fails, verify atomic-write failure preserves prior evidence,
and simulate bounded 429 retries. These fixtures are automated tests, not
new model answers or evaluation scores.

**Runtime verification.** The API-only telemetry switch used on September 29
was insufficient for initialization events. The official ONNX Runtime
[privacy documentation](https://github.com/microsoft/onnxruntime/blob/main/docs/Privacy.md)
describes `ORT_DISABLE_TELEMETRY=1` before import as the process-lifetime
non-Windows opt-out. The project and environment check now apply that switch
before runtime imports, alongside Chroma's opt-out. The earlier failed and
unconfirmed runs remain historical evidence. The new commands below all
completed with successful process exits; this is an observed runtime outcome,
not a claim that packet tracing proved absence of all network telemetry.
System call tracing was unavailable in this workspace.

The [automated regression log](results/tests_recovery_20261001.txt) records
the existing and newly added tests with a successful exit. After collecting
the new evidence, `python tools/summarize_evaluations.py --check` confirmed
that the saved summary matches its source JSON.

Setup initially needed the workspace SOCKS dependency (`socksio`) and the
embedding download timed out. Downloading the same Chroma MiniLM archive
from its existing CDN succeeded and matched the SHA-256 required by the
installed embedding code. No model or corpus was substituted. Then
[`python test.py`](results/runtime_check_20261001.txt) passed all environment
checks, and the [index command](results/index_build_20261001.txt) rebuilt the
existing 88-document, 91-chunk collection.

**Canonical documentation.** [evaluation_summary.md](results/evaluation_summary.md)
is generated from JSON and includes source hashes, per-run counts, and token
totals. `--check` detects stale numbers. The original baseline and later
scorer-enabled baseline have different real output-token totals; each has
its own row. Those measurements were not rewritten. README retains manual
verdicts/diagnoses, `criteria.md` retains targets, and the checklist and
historical review point to those canonical locations.

#### Run Log — After Stretch (third full evaluation)

Commands actually executed, using the same corpus, model, original questions,
original five criteria, top-k 1, and cutoff 0.6:

```bash
ORT_DISABLE_TELEMETRY=1 ANONYMIZED_TELEMETRY=False .venv/bin/python test.py
ORT_DISABLE_TELEMETRY=1 ANONYMIZED_TELEMETRY=False .venv/bin/python app.py index
ORT_DISABLE_TELEMETRY=1 ANONYMIZED_TELEMETRY=False .venv/bin/python run_eval.py --label after_stretch --runs 3 --requests-per-minute 8
.venv/bin/python tools/check_split_chunks.py --label after_stretch
```

Actual evidence: [live JSON](results/run_20261001T031757487133Z_after_stretch.json),
[live Markdown](results/run_20261001T031757487133Z_after_stretch.md),
[console output](results/after_stretch_console_20261001.txt), and
[fresh three-trial chunk log](results/chunks_20261001T031759129002Z_after_stretch.json).
The live runner made separate uncached model calls for every covered trial.
The full [manual review](results/after_stretch_review_20261001.md) checks all
answers against their cited originals and all six chunk pieces against their
own posts. Criterion 4 was freshly measured separately; the answer runner
does not automatically measure it.

| Criterion | Original Unit 1 target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---:|---:|---:|---|
| 1. Retrieved chunks contain the answer | At least 4 of 5 covered questions | 5/5 | 5/5 | 5/5 | MET |
| 2. Every substantive answer names a source | Every answer produced | 5/5 | 5/5 | 5/5 | MET |
| 3. Relevance gate stops unrelated questions | At least 4 of 5 refused | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks preserve sentences and source boundaries | All six chunks from the three named posts | 6/6 | 6/6 | 6/6 | MET |
| 5. Cited sources support the claims | At least 4 of 5 covered answers | 5/5 | 5/5 | 5/5 | MET |

**Decision sentences:**

1. **MET:** Each of the five retrieved top-1 chunks contained all requested
   facts in every run, exceeding the 4-of-5 target each time.
2. **MET:** Every substantive answer named its retrieved source filename;
   no covered answer failed the application's citation check.
3. **MET:** All five fixed unrelated questions were stopped before generation
   in every run, with the exact refusal text and no model calls for those trials.
4. **MET:** All six newly recorded chunks retained complete source sentences
   and their own source boundaries in every inspection repeat.
5. **MET:** Every factual claim in all five covered answers per run was
   supported by its explicitly cited original source, including the correct
   entity and numerical restrictions. The manual review notes Aldridge run 2's
   reliance on its filename for location identification; no wrong-location
   claim or unsupported extra fact was found. The substring scorer is only
   a supplementary check.

Representative actual output, produced by `run_eval.py::run_once` through
`app.py::ask_pipeline`, `store.py::search`, `gate.py::check`, and
`generate.py::answer_from_chunks`, Aldridge run 1:

```text
Question: How much does one wash cost in Aldridge Hall, and how do you pay?
Best cosine distance: 0.2623065848537246; relevance gate: passed
Retrieved source: housing_aldridge_hall_laundry.txt
Answer: One wash in Aldridge Hall costs $1.75, and you can pay using a card only (housing_aldridge_hall_laundry.txt).
```

The comparison with the earlier top-k-1 after run shows no original criterion
score increase or decrease. The third full log closes the missing full-test
evidence gap; it does not prove that lexical reranking improved generated
answers. Its model usage is the `after_stretch` row in the generated summary.
Output-token variation between live runs is not an isolated retrieval benefit.

The supplemental retrieval-only pair was also repeated on this rebuilt index
with three trials per question, using explicit vector-only `before` and lexical
`after` modes. Both commands completed successfully; raw files are
[before](results/stretch_probe_before_20261001T032137765435Z.json) and
[after](results/stretch_probe_after_20261001T032237698683Z.json), with saved
[before stdout](results/stretch_probe_before_console_20261001.txt) and
[after stdout](results/stretch_probe_after_console_20261001.txt).

```bash
ORT_DISABLE_TELEMETRY=1 ANONYMIZED_TELEMETRY=False .venv/bin/python tools/stretch_probe.py --label before --runs 3
ORT_DISABLE_TELEMETRY=1 ANONYMIZED_TELEMETRY=False .venv/bin/python tools/stretch_probe.py --label after --runs 3
```

| Supplemental measurement | Before run 1 | Before run 2 | Before run 3 | After run 1 | After run 2 | After run 3 |
|---|---:|---:|---:|---:|---:|---:|
| Answer-bearing selected chunks | 4/6 | 4/6 | 4/6 | 6/6 | 6/6 | 6/6 |
| Unsupported near-topic questions refused by gate | 1/5 | 1/5 | 1/5 | 1/5 | 1/5 | 1/5 |

The lexical change again fixed the two diagnosed Kestrel retrieval misses;
the gate weakness stayed the same. This is a measured retrieval improvement
with an unchanged full original-criterion evaluation, not a measured increase
in generated-answer accuracy. No deterioration was measured on these fixed
sets; wider performance remains unknown. These supplemental questions still
do not replace the original criterion questions or turn historical passes
into misses.

**What's still broken:** No original criterion is MISSED in the third log.
The supplemental near-topic gate false positives and the lack of a separate
multi-document answer evaluation remain limitations. The gate measures topic
similarity rather than availability of the requested fact. I would next review
live answers on a fixed unsupported/multi-document set before changing that
gate; it would be another independent RAG change and is outside this follow-up.

**What I'd Do Differently:** In addition to the original reflections above,
I would specify whether the correct place must appear in ordinary answer prose
or whether an exact identifying source filename suffices. That distinction
should be settled before evaluation, not used afterward to manufacture a miss.
I would also test checkpoint recovery before spending the live-call quota.

ChatGPT helped implement and test recovery, inspect the official telemetry
setting, run the fresh evaluation, compare each answer with source text, and
consolidate documentation. Raw runtime output is separate from that review.
The instructor decides whether the new stretch evidence earns additional
points. The original empty miss list cannot justify claiming the previously
unawarded diagnosis points.
