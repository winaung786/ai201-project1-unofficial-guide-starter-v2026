# Acceptance criteria — The Unofficial Guide

Corpus: `campus_life`. Questions and expected phrases are recorded in
`questions.py` before retrieval calibration or answer evaluation.

**Authorship note:** Criteria 1–3 come from the assignment. The questions and
rationales for criteria 1–3 were drafted with Codex. I wrote criteria 4 and 5
myself on September 14, 2026, after reading my chunks and the Aldridge Hall and
Morrow House documents. I used Claude to pressure-test them: it asked how a
grader would check each sentence and pointed out weak spots, and I then added
the comparison against the original documents and the rule that a refusal counts
as a failure. The wording of 4 and 5 is mine.

The original targets were recorded before calibration; revisions 4–5 below were
made afterward on September 14, 2026, before Unit 2. Their earlier wording and
reasons are preserved here and in [CRITERIA_HISTORY.md](CRITERIA_HISTORY.md).
Unit 2 tested the already-established revised wording below; it did not revise
either target after seeing Unit 2 results. These are standards to test against,
not claims that the system has already passed.

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** The questions cover five specific campus topics, but many
dorm posts use almost identical wording with different building names. Four
of five allows one retrieval miss without accepting frequent confusion between
buildings. Inspect the top five chunks for each question; a keyword alone is
not proof that the chunk answers all parts of the question.

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** Every chunk carries a filename, so a substantive answer
should always identify its evidence. Four of five would excuse an untraceable
answer. Refusals are assessed under criterion 3 and must not invent a source.

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that"
— in at least 4 of 5 tries.

**Why this target:** Use the five fixed questions in `OUT_OF_SCOPE`, once each.
An unrelated question can still share vocabulary with a campus post, so this
target tolerates one borderline match while requiring the code to block most
unsupported questions before generation. Select the cutoff using measured
distances later; do not lower this target after observing results.

## 4. Chunks preserve sentences and source boundaries

**Original criterion (pre-calibration wording, preserved verbatim):**

> All five chunks printed by `python app.py chunks -n 5` must include a topic
> title and at least one complete factual statement; none may begin or end with
> a sentence cut in half.

**Original reason (preserved verbatim):** Posts contain prices, times, and payment rules that can
become misleading when split mid-sentence. Requiring all five samples to be
readable fits this short-post corpus. Compare each with its original document;
a sample passes only if all three conditions hold.

**Revised measurable criterion (September 14, 2026; the Unit 2 target):**

When I run `python app.py chunks --from-doc FILENAME` for
`housing_innisfree_hall.txt`, `housing_morrow_house.txt`, and
`housing_old_brewhouse.txt`, all six resulting chunks must contain text from only
their named source post and must not cut any sentence in half, compared against
the originals in `corpora/campus_life/documents/`.

**Why this target:** I chose all six because these three posts actually get
split, so checking every piece tests the places where a sentence could be cut.
A chunk also fails if it mixes text from different posts.

**Reason for revision:** The five-sample command did not guarantee inspection
of the split boundaries. The revised test names all six pieces from three posts
that actually split and checks each against its own source. This change was
recorded in Unit 1, before the Unit 2 before/after evaluation.

## 5. Cited sources support the claims

**Original criterion (pre-calibration wording, preserved verbatim):**

> For at least 4 of the 5 in-corpus test answers, every factual claim must be
> supported by a document explicitly cited in that answer, including the correct
> building or service name and any stated prices, times, or limits.

**Original reason (preserved verbatim):** Similar laundry and dining posts make an answer about the
wrong place a realistic failure. Four fully supported answers is more demanding
than merely finding a filename. Check every claim against the cited files; an
unsupported claim, wrong entity, or refusal fails that answer. This requires
human review, not just a match against the `expects` phrase.

**Revised measurable criterion (September 14, 2026; the Unit 2 target):**

For at least 4 of my 5 test questions in `questions.py`, the answer must name the
correct place or service, give the correct numbers where needed, and cite source
files that support every factual claim, checked against the original documents
in `corpora/campus_life/documents/`.

**Why this target:** I chose 4 of 5 because similar posts could cause an
occasional mix-up, but more than one wrong answer would make the guide hard to
trust. A refusal counts as a failure because the documents cover these questions;
the `expects` phrase is only a quick first check, and the original document is
the reference for deciding whether an answer is correct.

**Reason for revision:** The revision explicitly names the fixed question set
and original corpus documents as the reference for checking every claim. It
keeps the 4-of-5 threshold and makes the existing refusal-fails rule explicit.
This change was recorded in Unit 1, before the Unit 2 before/after evaluation.

In week 2, preserve these targets and record any justified revisions beneath
the originals with a reason; do not erase a target because a result missed it.
