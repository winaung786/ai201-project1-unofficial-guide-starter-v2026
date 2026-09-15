# Assignment review — September 14, 2026

**Later revision on September 14:** Criteria 4–5 were subsequently revised at the
student's request through discussion with Codex. Criterion 4 now checks all six
pieces of the three split posts; criterion 5 explicitly uses original documents
and counts refusals as failures. Authorship notes reflect the AI assistance.
See [CRITERIA_HISTORY.md](CRITERIA_HISTORY.md) for original wording and provenance.
The review below records the state before that revision; references to unchanged
original criteria or pending wording describe that earlier state.

This review uses the assignment pasted by the student on September 14 and the
current repository. It is a check of structure, documentation, and honesty,
not a claim about a grade or a substitute for the next unit's evaluation.

## Required deliverables

| Requirement | Evidence | Status |
|---|---|---|
| Load and clean a provided corpus | `ingest.py` loads 88 campus posts and normalizes whitespace and line endings; this supplied corpus is already plain text | Implemented; not a general HTML/ad cleaner |
| Deliberate chunking strategy | `chunker.py::split_documents`, 450-character soft size and up to 100 characters of whole-sentence overlap, explained in README | Implemented and documented |
| Embed, store, and retrieve | `store.py`, local MiniLM embeddings and cosine-distance Chroma search | Implemented; real calibration saved |
| Grounded answers with sources | `generate.py` and the real sourced answer in `results/sample_answer.json` | Implemented; one live answer checked, not a universal grounding guarantee |
| Gate before generation | `gate.py` and `app.py::ask_pipeline`; five actual refusals with zero model calls in `results/local_verification.json` | Implemented and observed |
| Interface usable independently | Commands in README and unchanged RUNNING.md | Present |
| Five questions with expected phrases | `questions.py` | Present; originally AI-drafted and disclosed |
| Five numbered acceptance criteria and rationales | `criteria.md` | Present, but criteria 4–5 remain AI-authored drafts |
| Student-authored criteria | Assignment says not to ask AI to write them | Not yet fulfilled; student's wording has been requested |
| Five README sections | What This Does, Chunking Strategy, Sample Chunks, Sample Answer, How I Used AI | Present |
| Five actual sample chunks and provenance | README text matches current `split_documents` output exactly | Verified |
| Cutoff and all ten distances | README values match `results/calibration.json` | Verified |
| Two honest AI-use moments | README describes delegation, key setup, generated output, and actual AI edits | Present; no invented student code edits |
| At least four commits in personal fork | Published project history has eight commits after the starter | Present |
| Preserve originals for the next unit | Local `original-local-milestones` branch and publication messages with original IDs/dates | Preserved |
| Course Portal submission | Student explicitly chose to handle this | Outside the assistant's current task |

## Historical requirements that cannot be recreated afterward

The first live answer was generated after the custom chunker was implemented,
because the private key was added later. The fork was also created after local
work had begun. Those steps do not follow the assignment's preferred milestone
order; the work log records the actual sequence. Running the original starter
now would not prove that it ran before the changes.

The original AI-drafted questions and targets were committed locally before
retrieval calibration. The GitHub connector replayed those snapshots in the
same order; its commits have publication dates, not backdated work dates.
New student wording must be dated as a revision after calibration and leave
the original criteria visible. Neither disclosure nor paraphrasing an AI draft
retroactively makes it independently student-authored.

## Solo criteria self-check

The assignment allows AI to describe how it would test existing criteria.
The following reviews the current sentences; it does not replace them or set
new targets. No new pass/fail evaluation is claimed here.

1. **Retrieval:** For each of the five fixed questions, inspect the retrieved
   chunks and count the question as passing if at least one contains enough
   information to answer it; compare the count with 4. The sentence alone does
   not specify the question list or top-k; the repository supplies questions.py
   and top-k 5, so those references are needed to reproduce the check.
2. **Source presence:** Inspect every substantive answer produced in the chosen
   run and verify that each names at least one source document. The rationale
   excludes refusals, but the criterion sentence itself does not say so. A
   finite run can check that run, not establish a universal claim for all future
   answers. This checks citation presence, not whether citations are correct.
3. **Out-of-scope refusal:** Ask five questions clearly absent from the corpus,
   confirm the code blocks generation, and count exact refusal responses;
   require at least four. The sentence alone leaves the questions unspecified;
   the rationale identifies OUT_OF_SCOPE. A final period is present in the
   application's refusal string. Record that punctuation convention when
   comparing text.
4. **Current five-chunk criterion:** Run `python app.py chunks -n 5`, then compare
   each sample with its source file for a topic title, a complete factual
   statement, and uncut sentences. Require all five samples to meet all three
   conditions. This is a reproducible sample check, but all sampled indices are
   #0; it does not inspect the later pieces of the split documents. It also
   does not explicitly prohibit mixing content from different source posts.
5. **Claim support:** For each of the five in-corpus answers, list its factual
   claims, open the documents explicitly cited in the answer, and check the
   claims against those documents, including entity names and numerical
   details. Count an answer as passing only when all its claims are supported;
   require four passing answers. This needs human semantic judgment, not just
   a filename or expects-phrase search. The rationale counts refusals as fails.

The six-piece alternative discussed in chat is also AI-drafted. It has not
been silently substituted for the original criterion. The student should
supply their own criterion and rationale before a dated revision is saved.

## Inspecting the split posts

The default five samples are selected by a deterministic stride, not randomly.
The three split source files each currently produce two pieces. The `--from-doc`
option is implemented in `app.py`; these commands show the actual split
boundaries, including later pieces:

```powershell
python app.py chunks --from-doc housing_innisfree_hall.txt
python app.py chunks --from-doc housing_morrow_house.txt
python app.py chunks --from-doc housing_old_brewhouse.txt
```

Run them after activating the virtual environment, or use
`.\.venv\Scripts\python.exe -X utf8` in place of `python`. These are inspection
instructions, not an invented result or a newly imposed acceptance target.

## Solo sample-chunk discussion

Using three existing README samples, each can answer a question independently:

- `admin_add_drop_deadline.txt#0`: When does adding a course stop, and when does
  dropping it create a W on the transcript?
- `course_biol_160_exams.txt#0`: What assessments does BIOL 160 use, and are they
  curved?
- `housing_morrow_house.txt#0`: What are Morrow House's housing types and damp
  problem, and how much are a wash and dry cycle?

The Morrow House sample does not include its later noise information; it must
not be used by itself to answer a noise question. These are AI observations,
not claims that a live breakout discussion with classmates took place.

## Solo cutoff discussion

The actual covered-question distances are 0.179727–0.372583; the unrelated
questions are 0.824593–0.934011. A cutoff of 0.6 lies in the gap and accepts all
five covered questions while rejecting all five unrelated questions in this
calibration set. A question about an uncovered detail of an otherwise covered
building could still get through, and an unusually phrased covered question
could still be refused. The cutoff does not guarantee accuracy, and a passing
best chunk does not make the other four chunks relevant.

The next unit's repeated answer evaluation and criterion verdicts remain to
be done against recorded targets. Passing development checks is not being
presented as this unit's grading standard.
