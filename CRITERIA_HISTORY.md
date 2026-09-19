# Criteria revision history

## Original criteria 4–5

These AI-drafted original targets were saved before retrieval calibration. They are
preserved verbatim below so later revisions do not erase the original standard.

## 4. Chunks preserve complete statements

All five chunks printed by `python app.py chunks -n 5` must include a topic
title and at least one complete factual statement; none may begin or end with
a sentence cut in half.

**Why this target:** Posts contain prices, times, and payment rules that can
become misleading when split mid-sentence. Requiring all five samples to be
readable fits this short-post corpus. Compare each with its original document;
a sample passes only if all three conditions hold.

## 5. Cited sources support the claims

For at least 4 of the 5 in-corpus test answers, every factual claim must be
supported by a document explicitly cited in that answer, including the correct
building or service name and any stated prices, times, or limits.

**Why this target:** Similar laundry and dining posts make an answer about the
wrong place a realistic failure. Four fully supported answers is more demanding
than merely finding a filename. Check every claim against the cited files; an
unsupported claim, wrong entity, or refusal fails that answer. This requires
human review, not just a match against the `expects` phrase.

## Revision — September 14, 2026

The student wrote the revised criteria 4–5 after reading the chunks and the
Aldridge Hall and Morrow House documents. Claude pressure-tested the student's
wording by asking how a grader would check each sentence and identifying weak
spots. The student then added the original-document comparison and the rule that
a refusal counts as a failure. The revisions were made after calibration and the
recorded sample answer.

Criterion 4 now checks every piece of the three split posts (six chunks) for
complete sentences and separation of source posts. This targets split boundaries
that the original five-sample command did not show. Criterion 5 keeps the 4-of-5
threshold and support for every factual claim, explicitly identifies the original
source documents as the reference, and counts an in-corpus refusal as a failure.
No new five-question answer evaluation is claimed by this revision.
