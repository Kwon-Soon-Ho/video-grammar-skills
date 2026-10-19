from pathlib import Path
import json,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
checks=[]
def check(name,value):
 if not value:raise AssertionError(name)
 checks.append({'name':name,'passed':True})
a=load(OUT/'current-audit.json');m=load(OUT/'source-role-reassessment.json');cards=load(OUT/'knowledge-card-proposals.json');p=load(OUT/'replanning-proposal.json')
check('41 unique source dispositions',len(m['records'])==len({r['source_id'] for r in m['records']})==41)
check('all41 source file pins',all(sha(r['local_path'])==r['sha256'] for r in m['records']))
check('17 full24 selected historical scope preserved',dict(__import__('collections').Counter(r['original_review_scope'] for r in m['records']))=={'full':17,'selected':24})
check('two handoffs null',a['handoff_is_null']=={'NEW-N':True,'NEW-P':True})
check('two existing case proposals with positive and negative inputs',len(cards['cards'])==2 and all(x['fit_example']['type']=='synthetic planning test' and x['counterexample']['type']=='synthetic negative input' and x['new_use_results']=='not tested' for x in cards['cards']))
check('source vs author intent vs new proposal separated',all('unknown' in x['designer_intent'] and x['status'].startswith('proposed') for x in cards['cards']))
check('no new registration IDs',all('No replacement/merge/new production IDs' in x['ids'] for x in cards['cards']))
check('four work categories and next options',len(p['work_categories'])==4 and len(p['next_options'])==4)
check('existing active19 files unchanged',all(sha(Path(a['active_skill'])/f['relative'])==f['sha256'] for f in a['protected_active_files']))
prior=load(ROOT/'design-record-enrichment-20261019/publication-receipt.json')
check('previous71 source and published files unchanged',all(sha(f['source'])==sha(f['destination'])==f['sha256'] for f in prior['published_files']))
check('sourcePDF bytes unchanged',all(sha(f['path'])==f['sha256'] for f in load(OUT/'source-pdfs.json')))
check('library definition unchanged',sha(a['library_pin']['path'])==a['library_pin']['sha256'])
qa=load(OUT/'report-qa.json');check('report8pages',qa['pages']==8)
qa['visual_review']={'state':'passed','method':'PDFium render all8 pages and inspect for Korean glyphs, legibility, overflow, overlap, cropping and image/text alignment','reviewer':'same AI context; no independent judgment or company acceptance'}
(OUT/'report-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
result={'passed':True,'checks':checks,'count':len(checks),'method':'document/source/data inspection and preservation; NOT new video/design transfer/benchmark test'}
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'passed':True,'checks':len(checks),'active_skill_changed':False},ensure_ascii=False))
