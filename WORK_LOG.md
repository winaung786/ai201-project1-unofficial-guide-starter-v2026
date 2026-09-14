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

## Live Gemini validation — September 13, 2026

The student added the API key privately to `.env`. All 10 environment checks
now pass, including real embeddings, the vector store, and a live response
from `gemini-3.5-flash-lite`. `capture_sample.py` produced this real answer:

> Juniors and seniors are ordered by accumulated credit hours first, with ties
> broken randomly (`admin_housing_lottery.txt`).

Codex opened that document and verified both claims against its text. The
answer and source line are saved in README.md; the full application result
is saved in results/sample_answer.json. This resolves the earlier missing-key
blocker; the historical no-key verification remains as a record of setup.

GitHub fork creation is waiting for browser sign-in. The GitHub connector is
connected but has no fork-creation operation. Student review of the criteria
and AI reflection remains pending, and nothing has been submitted to the portal.

## Publication preparation

GitHub sign-in succeeded, and the personal fork was created under winaung786.
The README now gives the repository URL and a finished, factual AI-use account,
including the student's key setup and GitHub sign-in. The numerical criteria
and original history are unchanged; AI authorship is explicitly disclosed.
The Course Portal URL has been requested so final submission can be completed.
