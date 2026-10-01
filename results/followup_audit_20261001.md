# Feedback follow-up audit — October 1, 2026 UTC

Status: work completed locally and prepared for publication to the same GitHub
repository. Publication is verified separately by comparing Git trees.

The required original Unit 2 work remains historically intact. The newly
requested harness/documentation fixes and missing full post-stretch evidence
are present. The instructor must reassess the submission; no new grade is
claimed. The rubric's empty-original-miss-list rule remains applicable.

## Evidence checks performed

- Compared the original corpus, criteria/history, fixed questions, core app,
  loader/chunker/gate, requirements, and all pre-existing JSON evidence against
  the previous published head `85cab01e6b2a62188f36d2bff5f6481eda28051e`.
  All 176 checked files were byte-identical.
- Verified the fresh live log's complete covered/out-of-scope trial matrices,
  disabled response caching, successful status, absence of recorded errors,
  per-trial request accounting, and matching pipeline/corpus fingerprints.
- Reviewed every new answer against its cited original source, and the six
  source/chunk boundaries against their originals. Detailed qualitative
  findings are in [manual review](after_stretch_review_20261001.md); canonical
  verdicts and remaining limitations are in [README](../README.md#october-1-feedback-follow-up).
- Confirmed the fresh paired supplemental probes use explicit vector-only
  and lexical modes, the same rebuilt index, and three trials each; these
  probes make no generation calls. The original questions were not replaced.
- Confirmed the required README sections and three criterion-level tables
  (original before, original after, post-stretch), and checked local evidence
  links and `git diff --check`.
- Confirmed the generated numeric summary matches raw JSON using `--check`.
  Token totals and automatic counts are canonical in
  [evaluation_summary.md](evaluation_summary.md), not duplicated here.
- Confirmed `.env` and the rebuilt local index are ignored by Git. The private
  key is excluded from commits; no secret file is part of this manifest.
- Original primary top-k reduction and later optional lexical rerank are
  clearly separated. This follow-up changes harness/setup reliability and
  documentation; it adds no new retrieval, gate, prompt, model, or UI feature.

## Successfully executed checks/evaluations

Commands used `.venv/bin/python`. Live commands set
`ORT_DISABLE_TELEMETRY=1 ANONYMIZED_TELEMETRY=False` before launch.

```text
python test.py
python app.py index
python run_eval.py --label after_stretch --runs 3 --requests-per-minute 8
python tools/check_split_chunks.py --label after_stretch
python tools/stretch_probe.py --label before --runs 3
python tools/stretch_probe.py --label after --runs 3
python -m unittest discover -s tests -v
python tools/summarize_evaluations.py
python tools/summarize_evaluations.py --check
git diff --check
```

Actual runtime/test stdout is saved in the files listed below. Recovery and
429 tests use labeled synthetic fixtures; they do not supply live scores.
Initial setup encountered a missing SOCKS dependency and an embedding-download
timeout; both were resolved before the successful environment check. System
call tracing was unavailable, and no network tracing success is claimed.

## Files created or modified in this follow-up

Tracked changes compared with the previous published head:

```text
.env.example
ASSIGNMENT_REVIEW.md
README.md
RUNNING.md
SUBMISSION_CHECKLIST.md
WORK_LOG.md
config.py
eval_checkpoint.py
generate.py
run_eval.py
score_saved.py
store.py
test.py
tests/test_eval_recovery.py
tests/test_eval_summary.py
tests/test_evaluation.py
tools/check_split_chunks.py
tools/summarize_evaluations.py
results/after_stretch_console_20261001.txt
results/after_stretch_review_20261001.md
results/chunks_20261001T031759129002Z_after_stretch.json
results/evaluation_summary.md
results/followup_audit_20261001.md
results/index_build_20261001.txt
results/run_20261001T031757487133Z_after_stretch.json
results/run_20261001T031757487133Z_after_stretch.md
results/runtime_check_20261001.txt
results/stretch_probe_after_20261001T032237698683Z.json
results/stretch_probe_after_console_20261001.txt
results/stretch_probe_before_20261001T032137765435Z.json
results/stretch_probe_before_console_20261001.txt
results/tests_recovery_20261001.txt
```

Local setup also created the ignored `.env`, virtual environment, embedding
cache, and rebuilt index. Those are setup assets, not submitted evidence or
a second repository.

## Remaining user actions

Review the new evidence and submit the same repository URL through the Course
Portal. Request instructor reassessment if resubmissions are permitted. Replace
the chat-shared key as the student already planned. No GitHub sign-in or new
repository is required for this work.
