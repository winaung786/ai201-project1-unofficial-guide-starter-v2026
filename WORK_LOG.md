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

The student clarified that Codex should finish the assignment and upload the
repository, while the student will handle Course Portal submission personally.
No portal submission will be performed by Codex.

## Publishing through the connected GitHub service

Command-line Git could not authenticate without another interactive login.
The connected GitHub service has write access, so the local milestone changes
will be replayed in their original order, including criteria before results.
The new GitHub commits have publication timestamps and include the original
local commit IDs and authored dates in their messages. They are not being
backdated. The original local commits are retained on a separate branch after
synchronizing the checkout with the published main branch.

Portal submission remains the student's responsibility, by explicit request.

## Upload verified — September 14, 2026

All seven milestone snapshots were published in order to the personal fork.
Each GitHub tree hash matched its corresponding original local tree hash.
After publication, fetching the repository confirmed that the final published
snapshot and local project both had tree ID
`94b0382845bf17da9d2c12092edfd5ccc519cae5`.

The original commits are retained on the local `original-local-milestones`
branch. The working `main` branch now tracks the GitHub history. Credentials,
local model caches, the virtual environment, and the local vector database
are excluded from publication. Portal submission was intentionally left to
the student. The AI-assisted authorship is disclosed in the report and criteria.

## Assignment-rule audit — September 14, 2026

The student asked for compliance with the full assignment, not just working
software. Codex rechecked the pasted requirements and corrected the completion
status: student authorship of criteria 4–5 has not been fulfilled. Original
criteria remain unchanged while the student's wording is requested.

README samples, distances, and live answer were matched against the actual
code and saved evidence. The default samples are all #0 and selected by
stride, not randomly. ASSIGNMENT_REVIEW.md supplies the targeted commands,
a solo review of the current criteria, chunk discussion, and cutoff tradeoffs.
It also records the actual late API-key/fork setup instead of implying that
the original starter ran live before code changes. No dates or past events
were rewritten, and no classmate discussion or new evaluation was fabricated.


## Criteria revision — September 14, 2026

At the student's request, Codex applied the criterion wording developed in the
conversation. Criterion 4 now targets all six chunks from the three split posts,
checking sentence boundaries and source separation. Criterion 5 keeps the 4-of-5
standard, names the original documents as the reference, and explicitly counts
refusals as failures for covered questions. README and criteria authorship notes
now describe the discussion, AI-proposed wording, and student-requested revisions.
Original criteria are preserved in CRITERIA_HISTORY.md; the revisions are not
backdated to the original pre-calibration milestone. This documentation change
does not claim a new answer evaluation or independent student authorship.
