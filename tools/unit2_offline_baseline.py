"""Record credential-free Unit 2 baseline evidence from the existing pipeline.

Run from the repository root after `python app.py index`. This intentionally
does not score generated answers or change the application configuration.
"""

import datetime
import json
import re
import subprocess
from pathlib import Path
import app, config, gate, questions
from chunker import split_documents
from ingest import load_documents
from store import search

checks = [
    ('admin_housing_lottery.txt', ['juniors and seniors are ordered by accumulated credit hours first', 'only tie-break randomly']),
    ('dining_kestrel_commons.txt', ['20 to 25 minutes between 12:15 and 1:00']),
    ('housing_aldridge_hall_laundry.txt', ['$1.75 wash', 'card only']),
    ('study_group_rooms.txt', ['two weeks ahead', 'maximum two blocks per person per week']),
    ('admin_printing_quota.txt', ['$30 of printing per semester', 'does not roll over']),
]
records = {'status':'PARTIAL BASELINE: no Gemini key; no generated answer trials',
           'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'revision':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
           'corpus':config.CORPUS,'embedding_model':config.EMBEDDING_MODEL,
           'generation_model_configured':config.MODEL,'top_k':config.TOP_K,
           'threshold':config.THRESHOLD,'covered':[],'out_of_scope':[],'chunk_boundaries':[],
           'unmeasured':['criterion 2: generated answer source naming','criterion 5: generated answer factual grounding','full three-run before evaluation','after evaluation']}
for run in range(1,4):
    count=0
    for item, (source, phrases) in zip(questions.QUESTIONS, checks):
        q=item['question']; hits=search(q); dec=gate.check(hits)
        present=any(r.source==source and all(p.lower() in r.text.lower() for p in phrases) for r in hits)
        count+=present
        records['covered'].append({'run':run,'question':q,'answer_present_in_retrieved_chunk':present,
            'expected_source':source,'checked_phrases':phrases,'gate_passed':dec.passed,
            'best_distance':dec.best_distance,
            'retrieved':[{'label':r.label,'source':r.source,'distance':r.distance,'text':r.text,'produced_by':r.produced_by} for r in hits]})
    print('run',run,'covered retrieval',count,'of',len(questions.QUESTIONS),flush=True)
    blocked=0
    for q in questions.OUT_OF_SCOPE:
        hits=search(q); outcome=app.ask_pipeline(q)
        blocked+=bool(outcome['refused'] and outcome['refusal_reason']=='relevance_gate' and outcome['answer']==gate.REFUSAL)
        records['out_of_scope'].append({'run':run,'question':q,'answer':outcome['answer'],
            'refused':outcome['refused'],'reason':outcome['refusal_reason'],'best_distance':outcome['best_distance'],
            'retrieved':[{'label':r.label,'source':r.source,'distance':r.distance,'text':r.text} for r in hits]})
    print('run',run,'out-of-scope gate refusal',blocked,'of',len(questions.OUT_OF_SCOPE),flush=True)
    documents=load_documents(config.CORPUS)
    for source in ['housing_innisfree_hall.txt','housing_morrow_house.txt','housing_old_brewhouse.txt']:
        doc=next(d for d in documents if d.source==source)
        title,_,body=doc.text.partition('\n\n')
        normalized=' '.join(body.split())
        pieces=split_documents([doc]); validations=[]
        for piece in pieces:
            part=piece.text.partition('\n\n')[2]
            validations.append({'label':piece.label,'source':piece.source,'text':piece.text,
                'produced_by':piece.produced_by,'title_matches':piece.text.startswith(title+'\n\n'),
                'body_ends_sentence':part.endswith(('.', '!', '?')),
                'all_output_segments_are_in_original':all(segment.strip() in normalized for segment in re.split(r'(?<=[.!?])\s+(?=[A-Z“"\'])',part))})
        records['chunk_boundaries'].append({'run':run,'source':source,'expected_chunks':2,'actual_chunks':len(pieces),
            'chunks':validations,'passes_structural_checks':len(pieces)==2 and all(all(x[k] for k in ('title_matches','body_ends_sentence','all_output_segments_are_in_original')) for x in validations)})
    print('run',run,'chunk boundaries',sum(x['passes_structural_checks'] for x in records['chunk_boundaries'] if x['run']==run),'of 3 documents',flush=True)
path=Path('results/unit2_offline_before.json')
path.write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('wrote',path,flush=True)
