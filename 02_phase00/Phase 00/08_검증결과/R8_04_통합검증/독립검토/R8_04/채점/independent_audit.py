from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[2]/'R8_04_시험'
OUT=Path(__file__).resolve().parent
def read(p): return p.read_text(encoding='utf-8-sig')
def js(p): return json.loads(read(p))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def diff(a,b,p=''):
 if type(a)!=type(b): return [{'path':p,'before':a,'after':b}]
 if isinstance(a,dict):
  return sum((diff(a.get(k),b.get(k),p+'/'+k) for k in a.keys()|b.keys()),[])
 if isinstance(a,list):
  if len(a)!=len(b): return [{'path':p,'before':a,'after':b}]
  return sum((diff(x,y,p+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [{'path':p,'before':a,'after':b}]
allruns=[]
for group in ['1_새사례','2_실제쓰기']:
 for run in sorted((ROOT/group).glob('*/candidate')):
  inp=run/'inputs'/'Phase00'; out=run/'outputs'; before=js(run/'fixture_before.json')
  changed=[{'path':p,'before':h,'after':sha(inp/p) if (inp/p).exists() else None} for p,h in before.items() if not (inp/p).exists() or sha(inp/p)!=h]
  extra=[p.relative_to(inp).as_posix() for p in inp.rglob('*') if p.is_file() and p.relative_to(inp).as_posix() not in before]
  skill=next((inp/'실행스킬').glob('*/SKILL.md'))
  # Read every output / transcript / supplied skill resource for coverage; preserve hashes only.
  coverage=[]
  for p in sorted(out.rglob('*')):
   if p.is_file():
    data=p.read_bytes(); coverage.append({'path':str(p.relative_to(run)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
  commands=[]
  for p in sorted(out.glob('*.json')):
   if p.name.endswith(('.execution.json','.command.json')):
    o=js(p); commands.append({'file':p.name,'data':o})
  events=[]
  if (run/'서비스이벤트').exists():
   for p in sorted((run/'서비스이벤트').glob('*.json')):
    o=js(p); events.append({'file':p.name,**{k:v for k,v in o.items() if k not in ['response']},'response':{k:v for k,v in o.get('response',{}).items() if k not in ['text','content','bytes','data']}})
  r={'run':str(run),'task_sha256':sha(run/'task.txt'),'skill_sha256':sha(skill),'skill':read(skill),'changed':changed,'extra':extra,'events':events,'commands':commands,'coverage':coverage}
  narrative=re.sub(r'(?:```[^\n]*\n.*?```|~~~[^\n]*\n.*?~~~)','[원문 코드/JSON 블록은 별도 로그와 대조]',read(out/'transcript.md'),flags=re.S)
  (OUT/(group+'_'+run.parent.name+'_transcript_narrative.txt')).write_text(narrative,encoding='utf-8')
  allruns.append(r)
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'direct_audit.json').write_text(json.dumps(allruns,ensure_ascii=False,indent=2),encoding='utf-8')
for r in allruns:
 print('\nRUN',Path(r['run']).parent.name)
 print('SKILL',r['skill_sha256']);print('CHANGED',json.dumps(r['changed'],ensure_ascii=False));print('EXTRA',r['extra'])
 for e in r['events']:
  print('EVENT',json.dumps(e,ensure_ascii=False))
