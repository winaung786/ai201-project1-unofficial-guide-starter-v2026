# Acceptance criteria — The Unofficial Guide

Corpus: `campus_life`. Questions and expected phrases are recorded in
`questions.py` before retrieval calibration or answer evaluation.

**Authorship note:** Criteria 1–3 come from the assignment. Codex drafted the
questions, rationales, and criteria 4–5 after being asked to choose suitable
targets. The assignment asks students to author their own criteria: review
these drafts and write your own final wording and reasoning before submission.
These are proposed targets, not claims that any test has passed.

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

## 4. Chunks preserve complete statements (student review needed)

All five chunks printed by `python app.py chunks -n 5` must include a topic
title and at least one complete factual statement; none may begin or end with
a sentence cut in half.

**Why this target:** Posts contain prices, times, and payment rules that can
become misleading when split mid-sentence. Requiring all five samples to be
readable fits this short-post corpus. Compare each with its original document;
a sample passes only if all three conditions hold.

## 5. Cited sources support the claims (student review needed)

For at least 4 of the 5 in-corpus test answers, every factual claim must be
supported by a document explicitly cited in that answer, including the correct
building or service name and any stated prices, times, or limits.

**Why this target:** Similar laundry and dining posts make an answer about the
wrong place a realistic failure. Four fully supported answers is more demanding
than merely finding a filename. Check every claim against the cited files; an
unsupported claim, wrong entity, or refusal fails that answer. This requires
human review, not just a match against the `expects` phrase.

In week 2, preserve these targets and add justified revisions underneath them.
Do not erase an original target because a result missed it.
