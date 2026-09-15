# Acceptance criteria — The Unofficial Guide

Corpus: `campus_life`. Questions and expected phrases are recorded in
`questions.py` before retrieval calibration or answer evaluation.

**Authorship note:** Criteria 1–3 come from the assignment. The questions and
rationales for criteria 1–3 were drafted with Codex. Criteria 4–5 were revised
through discussion with Codex about the chunks and source documents: Codex
proposed wording, and I requested revisions and adoption. They are AI-assisted,
not independently student-written.

The original targets were recorded before calibration; revisions 4–5 below were
made afterward on September 14, 2026. The original wording and reasons for the
changes are preserved in [CRITERIA_HISTORY.md](CRITERIA_HISTORY.md). These are
standards to test against, not claims that the system has already passed.

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

When I run `python app.py chunks --from-doc FILENAME` for
`housing_innisfree_hall.txt`, `housing_morrow_house.txt`, and
`housing_old_brewhouse.txt`, all six resulting chunks must contain text from only
their named source post and must not cut any sentence in half, compared against
the originals in `corpora/campus_life/documents/`.

**Why this target:** I chose all six because these three posts actually get
split, so checking every piece tests the places where a sentence could be cut.
A chunk also fails if it mixes text from different posts.

## 5. Cited sources support the claims

For at least 4 of my 5 test questions in `questions.py`, the answer must name the
correct place or service, give the correct numbers where needed, and cite source
files that support every factual claim, checked against the original documents
in `corpora/campus_life/documents/`.

**Why this target:** I chose 4 of 5 because similar posts could cause an
occasional mix-up, but more than one wrong answer would make the guide hard to
trust. A refusal counts as a failure because the documents cover these questions;
the `expects` phrase is only a quick first check, and the original document is
the reference for deciding whether an answer is correct.

In week 2, preserve these targets and record any justified revisions with their
original wording in `CRITERIA_HISTORY.md`; do not erase a target because a result
missed it.
