"""Capture one real generated answer into the README after adding a private key.

Run: python capture_sample.py
Does not invent an answer when setup or generation fails. This may use one
Gemini request; the starter's ordinary response cache remains enabled.
"""
import json
from datetime import datetime, timezone

import config
from app import ask_pipeline
from questions import QUESTIONS


def main():
    question = QUESTIONS[0]['question']
    outcome = ask_pipeline(question)
    if outcome['refused']:
        raise SystemExit('The gate refused the sample. Inspect retrieval before capturing it.')
    citations = [source for source in outcome['sources'] if source in outcome['answer']]
    if not citations:
        raise SystemExit('The model supplied no retrieved filename citation. No sample was saved; inspect the prompt and answer.')
    config.RESULTS_DIR.mkdir(exist_ok=True)
    record = dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),
                  model=config.MODEL, corpus=config.CORPUS, cited_sources=citations, **outcome)
    path = config.RESULTS_DIR / 'sample_answer.json'
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding='utf-8')
    sample = (f"**Question:** {question}\n\n**Answer (actual application output):**\n\n"
              f"```text\n{outcome['answer']}\n\nSources cited in answer: {', '.join(citations)}\n```\n\n"
              'Captured by `capture_sample.py::main` through `app.py::ask_pipeline`; '
              'raw output is in `results/sample_answer.json`. '
              'A human still needs to verify that the cited files support every claim.\n')
    readme = config.ROOT / 'README.md'
    text = readme.read_text(encoding='utf-8-sig')
    start, end = '<!-- LIVE_SAMPLE_START -->', '<!-- LIVE_SAMPLE_END -->'
    if text.count(start) != 1 or text.count(end) != 1:
        raise SystemExit(f'Saved {path}, but README sample markers are missing or duplicated.')
    before, remainder = text.split(start, 1)
    _, after = remainder.split(end, 1)
    readme.write_text(before + start + '\n' + sample + end + after, encoding='utf-8')
    print(sample)
    print('Saved the actual sample. Review the answer, README status, and remaining submission tasks.')


if __name__ == '__main__':
    main()
