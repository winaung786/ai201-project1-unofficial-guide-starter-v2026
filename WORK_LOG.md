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
