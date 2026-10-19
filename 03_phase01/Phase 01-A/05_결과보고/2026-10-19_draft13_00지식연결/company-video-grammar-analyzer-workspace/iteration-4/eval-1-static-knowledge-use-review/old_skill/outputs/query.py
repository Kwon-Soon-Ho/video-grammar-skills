"""Read-only lookup of the local collection. Optional output stays within this folder."""
from pathlib import Path
import argparse,json,hashlib,sys
P=Path(__file__).resolve().parent
D=json.loads((P/'index.json').read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n):return json.loads((P/n).read_text(encoding='utf-8'))
def validate():
 errors=[];checks=0
 def test(ok,message):
  nonlocal checks
  checks+=1
  if not ok:errors.append(message)
 tables={name:{x['id']:x for x in D[name]} for name in ['definitions','cases','evidence','knowledge','reviews','unknowns']}
 for name,t in tables.items():test(len(t)==len(D[name]),f'duplicate {name} ID')
 for u in D['occurrences']:
  test(u['definition_id'] in tables['definitions'],f'unknown definition {u["id"]}')
  test(u['case_id'] in tables['cases'],f'unknown case {u["id"]}')
  for e in u['evidence_ids']:test(e in tables['evidence'],f'unknown evidence {u["id"]}: {e}')
  for k in u['knowledge_ids']:test(k in tables['knowledge'],f'unknown knowledge {u["id"]}: {k}')
 for n in D['definitions']:
  test(any(u['definition_id']==n['id'] for u in D['occurrences']),f'no usage {n["id"]}')
  for key in ['definition_source','detail_source']:test((P/n[key]).is_file(),f'missing source {n[key]}')
 for c in D['cases']:
  test(c['layout_id'] in tables['definitions'],f'case layout missing {c["id"]}')
  for uid in c['unknowns']:test(uid in tables['unknowns'],f'unknown unresolved {uid}')
 for x in D['knowledge_links']:
  test(x['target_id'] in tables['definitions'],f'unknown target {x["id"]}')
  for k in x['knowledge_ids']:test(k in tables['knowledge'],f'unknown link knowledge {k}')
 for r in D['reviews']:
  for tid in r['target_ids']:test(tid in tables['definitions'] or tid in tables['cases'],f'unknown review target {tid}')
  for k in r['criteria_ids']:test(k in tables['knowledge'],f'unknown criterion {k}')
  for e in r['evidence_ids']:test(e in tables['evidence'],f'unknown review evidence {e}')
 for e in D['evidence']:
  p=Path(e['path']);test(p.is_file(),f'missing evidence {e["id"]}')
  if p.is_file():test(sha(p)==e['sha256'],f'evidence hash changed {e["id"]}')
  if 'parent' in e:test(e['parent'] in tables['evidence'],f'unknown ROI parent {e["id"]}')
 for m in load('source_manifest.json'):
  p=Path(m['path']);test(p.is_file(),f'missing source {p}')
  if p.is_file():test(sha(p)==m['sha256'],f'source changed {p}')
  if 'copy' in m:test(sha(Path(m['copy']))==m['sha256'],f'preservation mismatch {m["copy"]}')
 for k in D['knowledge']:
  p=Path(k['source_path']);v=json.loads(p.read_text(encoding='utf-8-sig'))
  test(sha(p)==k['source_sha256'],f'knowledge source changed {k["id"]}')
  for item in k['json_pointer'].strip('/').split('/'):v=v[int(item)] if isinstance(v,list) else v[item]
  test(v==k['content'],f'knowledge pointer/content mismatch {k["id"]}')
 expected={'RC-LAYOUT-001@v1','RC-LAYOUT-002@v1'}|{f'RC-COMP-{i:03d}@v1' for i in range(1,9)}
 test(set(tables['definitions'])==expected,'existing definition IDs not preserved')
 return {'mode':'validation','passed':not errors,'checks':checks,'errors':errors,'cases':len(D['cases']),'definitions':len(D['definitions']),'occurrences':len(D['occurrences']),'scope':'reference integrity, files/hashes, prior-record preservation and pinned knowledge; not visual content correctness or R4 compliance'}
def query(a):
 nodes=D['definitions'];selected=set();matched_knowledge=[];matched_reviews=[]
 if a.query:
  q=a.query.casefold()
  for n in nodes:
   # Match node fields only, not all connected metadata, to keep local text search interpretable.
   if q in json.dumps(n,ensure_ascii=False).casefold():selected.add(n['id'])
 if a.id:selected|={n['id'] for n in nodes if n['id']==a.id}
 if a.case:selected|={u['definition_id'] for u in D['occurrences'] if u['case_id']==a.case}
 if a.knowledge:
  matched_knowledge=[k for k in D['knowledge'] if k['id']==a.knowledge]
  selected|={x['target_id'] for x in D['knowledge_links'] if a.knowledge in x['knowledge_ids']}
  selected|={u['definition_id'] for u in D['occurrences'] if a.knowledge in u['knowledge_ids']}
  for r in D['reviews']:
   if a.knowledge in r['criteria_ids']:
    matched_reviews.append(r)
    for t in r['target_ids']:
     if t in {n['id'] for n in nodes}:selected.add(t)
     elif t in {c['id'] for c in D['cases']}:selected|={u['definition_id'] for u in D['occurrences'] if u['case_id']==t}
 if a.review:
  matched_reviews=[r for r in D['reviews'] if r['id']==a.review]
  for r in matched_reviews:
   selected|={t for t in r['target_ids'] if t in {n['id'] for n in nodes}}
   for t in r['target_ids']:
    if t.startswith('RC-CASE-') and not selected:selected|={u['definition_id'] for u in D['occurrences'] if u['case_id']==t}
 results=[]
 for n in nodes:
  if n['id'] not in selected:continue
  us=[u for u in D['occurrences'] if u['definition_id']==n['id'] and (not a.case or u['case_id']==a.case)]
  cs=[c for c in D['cases'] if c['id'] in {u['case_id'] for u in us}]
  kl=[x for x in D['knowledge_links'] if x['target_id']==n['id']]
  # Case-scoped reviews are explicitly identified, rather than inherited as a component approval.
  rv=[dict(r,association='direct_target' if n['id'] in r['target_ids'] else 'case_context_only') for r in D['reviews'] if n['id'] in r['target_ids'] or {c['id'] for c in cs}.intersection(r['target_ids'])]
  eids={e for u in us for e in u['evidence_ids']}|{e for r in rv for e in r['evidence_ids']}
  kids={k for x in kl for k in x['knowledge_ids']}|{k for u in us for k in u['knowledge_ids']}|{k for r in rv for k in r['criteria_ids']}
  results.append({'definition':n,'occurrences':us,'cases':cs,'knowledge_links':kl,'knowledge':[k for k in D['knowledge'] if k['id'] in kids],'reviews':rv,'evidence':[e for e in D['evidence'] if e['id'] in eids],'unknowns':[u for u in D['unknowns'] if u['id'] in {x for c in cs for x in c['unknowns']}],'investigations':[x for x in D['investigations'] if n['id'] in x['targets']],'detail_path':str(P/'01_수집기록.md'),'preserved_detail_path':str(P/n['detail_source']),'preserved_definition_path':str(P/n['definition_source'])})
 return {'mode':'lookup','filters':{k:getattr(a,k) for k in ['query','id','case','knowledge','review'] if getattr(a,k)},'result_count':len(results),'matched_knowledge':matched_knowledge,'matched_reviews':matched_reviews,'results':results,'scope':D['source_scope'],'status':D['status']}
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__)
 g=ap.add_mutually_exclusive_group(required=True)
 for flag in ['query','id','case','knowledge','review']:g.add_argument('--'+flag)
 g.add_argument('--validate',action='store_true');ap.add_argument('--out')
 a=ap.parse_args();out=validate() if a.validate else query(a)
 if a.out:
  p=(P/a.out).resolve()
  if not p.is_relative_to(P):ap.error('--out must stay within outputs')
  p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print(json.dumps({'saved':str(p),'passed':out.get('passed'),'result_count':out.get('result_count'),'checks':out.get('checks')},ensure_ascii=False))
 else:print(json.dumps(out,ensure_ascii=False,indent=2))
 if a.validate and not out['passed']:sys.exit(1)
