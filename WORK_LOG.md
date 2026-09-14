# Project work log

## Local setup — September 13, 2026

- Cloned the official `codepath/ai201-project1-unofficial-guide-starter-v2026`
  repository, preserving its history. No personal GitHub fork exists yet.
- Selected the provided `campus_life` corpus. It contains fictional student
  posts written for this course, not verified advice about a real college.
- Read the housing lottery, Kestrel Commons, Aldridge Hall laundry, group
  study rooms, and printing quota documents.
- Created a Python 3.12 virtual environment and a git-ignored `.env` template.
- Dependency installation is in progress. No live answer has been generated:
  the Gemini key has not been configured.

The first local commit records setup, not a claim that Milestone 1's live
model check has passed. Subsequent work will record questions and targets
before measuring retrieval. AI assistance is disclosed in the README.

## Chunking decision, recorded before implementation

The baseline produces 88 chunks from 88 documents: average 317 characters,
minimum 178, maximum 549. Most posts already fit in a complete chunk. Use a
450-character soft limit, counting the repeated title, to keep the ordinary
posts intact and split the few longest posts at sentence boundaries. Carry
up to 100 characters of complete trailing sentences across a split when they
fit with the next sentence. A sentence longer than the budget stays intact;
there must be no artificial trailing fragment or overlap-only chunk.

## Implementation and calibration completed locally

- Custom chunker: 91 chunks, average 309 characters, minimum 159, maximum 432.
  Five actual samples are in README.md, with source labels and function names.
- The questions and draft criteria were committed before retrieval calibration.
- Built the real ONNX/Chroma index. Covered questions scored 0.179727–0.372583;
  unrelated questions scored 0.824593–0.934011. Kept top-k 5 and chose 0.6,
  approximately the midpoint of the measured gap.
- Read all five results for each of the first three questions, including
  irrelevant lower-ranked building matches. Strengthened grounding instructions
  to preserve entities, exceptions, and per-claim source attribution.
- All five unrelated questions were refused by the real application pipeline;
  total generation calls: 0. Raw evidence is in results/local_verification.json.
- Ten regression tests pass; package dependency checks pass. The environment
  check passes eight checks, fails the missing-placeholder API key check, and
  skips the live model call. The model identifier has not been live-verified.
- No sample model answer, student-authored reflection, remote fork, push, or
  Course Portal submission is claimed. SUBMISSION_CHECKLIST.md names the
  remaining steps. capture_sample.py can save the actual answer after key setup.
- RUNNING.md and all provided corpus documents were left unchanged.
