# Before submission

The local project has the pipeline, five questions, proposed criteria, five
actual sample chunks, and measured relevance distances. It is not yet ready
to submit because a live Gemini answer and student-authored reflection are
still missing, and no personal GitHub fork has been created.

1. Privately replace the placeholder in `.env` with your Gemini API key.
   Do not paste the key into chat. From this project folder run:

   ```powershell
   .\.venv\Scripts\python.exe -X utf8 test.py
   .\.venv\Scripts\python.exe -X utf8 capture_sample.py
   ```

   The first command must pass, including its real model call. The second
   saves a real answer and source filenames to the README. Verify every
   claim against the named source file. If a model name error occurs, use
   the course's current model setting in `.env` as `AI201_MODEL`; the starter
   default has been preserved and has not been verified without a key.

2. Read `criteria.md`. The assignment specifically asks you to author your
   criteria; criteria 4–5 and the rationales are AI-assisted drafts. Write
   your own defensible wording and disclose the assistance. Preserve the
   original drafts in history. Calibration has now occurred, so do not claim
   a later rewrite was authored before these measurements.

3. Review the README's two AI-use examples and replace the draft reflection
   with your actual experience: what you asked, what you received, and what
   you changed or accepted. Add your name. Update the status only after
   completing the outstanding items.

4. Create your own fork using the official starter's Fork button:
   https://github.com/codepath/ai201-project1-unofficial-guide-starter-v2026
   Connect this existing local checkout to it, preserving this history:

   ```powershell
   git remote rename origin upstream
   git remote add origin https://github.com/YOUR-USERNAME/ai201-project1-unofficial-guide-starter-v2026.git
   git add README.md criteria.md results/sample_answer.json
   git commit -m "Review criteria and add verified live answer"
   git push -u origin main
   ```

   Replace YOUR-USERNAME with your actual GitHub username. Run the rename
   only once. If GitHub says a branch has diverged, reconcile it without
   force-pushing or deleting history. No remote changes have been made by Codex.

5. Submit your fork's URL through the Course Portal. Keep this repository
   for the next unit. Do not run the week-2 evaluation or replace its targets
   just to fill in a report for the current assignment.

Local verification: `python -m unittest discover -s tests -v` and
`python calibrate.py` (after indexing). No key is required for these commands.
