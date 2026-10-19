from pathlib import Path
import json,hashlib,sys,shutil,datetime,re
B=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
pair=sys.argv[1];cid=pair.split('-')[0];sealed=read(B/'reference/seal.json');ref=read(B/'reference/reference.json')
assert hashlib.sha256((B/'reference/reference.json').read_bytes()).hexdigest()==sealed['reference_sha256']
rows=[x for x in read(B/'run-matrix.json') if x['run_id'].startswith(pair+'-')];assert len(rows)==2
rows.sort(key=lambda x:hashlib.sha256((sealed['reference_sha256']+x['run_id']).encode()).hexdigest())
D=B/'blind'/pair;assert not D.exists(),'preserve blind snapshot';D.mkdir(parents=True)
mapping={};q=[]
for r,label in zip(rows,['sample-A','sample-B']):
 rid=r['run_id'];root=B/'trials'/rid;seal=read(root/'seal.json');o=read(root/'outputs/observations.json');v=read(root/'validation.json')
 for n,h in seal['files'].items():assert hashlib.sha256((root/'outputs'/n).read_bytes()).hexdigest()==h
 mapping[label]=rid;paths={};proof=D/label/'evidence';proof.mkdir(parents=True)
 for e in o['evidence']:
  p=Path(e['path']);key=str(p)
  if key not in paths:
   to=proof/f'evidence-{len(paths)+1:03}.png';shutil.copy2(p,to)
   assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(to.read_bytes()).digest();paths[key]=str(to)
 def scrub(x):
  if isinstance(x,dict):return {k:scrub(val) for k,val in x.items() if k!='files_read'}
  if isinstance(x,list):return [scrub(a) for a in x]
  if isinstance(x,str):
   if x in paths:return paths[x]
   s=x.replace(rid,label)
   s=s.replace('without_skill','masked-condition').replace('with_skill','masked-condition')
   s=re.sub(r'(?i)SKILL\.md|company-video-grammar-analyzer|스킬','[condition-masked]',s)
   return s
  return x
 save(D/label/'observations.json',scrub(o))
 md=(root/'outputs/observations.md').read_text(encoding='utf-8')
 for p,to in paths.items():md=md.replace(p,to)
 (D/label/'observations.md').write_text(scrub(md),encoding='utf-8')
 save(D/label/'validation.json',v)
 q.append({'label':label,'structure_passed':v['structure_passed'],'evidence_provenance_checked':v['evidence_provenance_checked']})
save(D/'reference.json',{'criteria':next(x for x in ref['criteria'] if x['case_id']==cid),'reference_sha256':sealed['reference_sha256'],'human_gold':False})
save(D/'metadata.json',{'pair_id':pair,'samples':q,'blinding':'condition names/path components hidden; evidence byte-identical copies. Style may still suggest condition. Grader fresh context, no mapping access.','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
save(B/'blind-mappings'/f'{pair}.json',mapping)
print(str(D))
