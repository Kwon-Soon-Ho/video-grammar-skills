from pathlib import Path
import json,hashlib,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]/'R8_04_시험'
def read(p):return p.read_text(encoding='utf-8-sig')
def js(p):return json.loads(read(p))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def diff(a,b,p=''):
 if type(a)!=type(b):return [{'path':p,'before':a,'after':b}]
 if isinstance(a,dict):return sum((diff(a.get(k),b.get(k),p+'/'+k) for k in a.keys()|b.keys()),[])
 if isinstance(a,list):return [{'path':p,'before':a,'after':b}] if len(a)!=len(b) else sum((diff(x,y,p+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [{'path':p,'before':a,'after':b}]
expect=js(ROOT/'4_실행전기대항목.json');fixed=js(ROOT/'4_고정기록.json');rows=[]
assert sha(ROOT/'4_실행전기대항목.json')==fixed['expectations_sha256']
for k,case in expect['cases'].items():
 run=Path(case['run']);db=run/'inputs/Phase00';out=run/'outputs';before=js(run/'fixture_before.json');checks=[]
 def ck(n,b,ev):checks.append({'name':n,'passed':bool(b),'evidence':ev})
 for label,file,key in [('task',run/'task.txt','task_sha256'),('config',run/'시험설정.json','config_sha256'),('IO',run/'시험IO.py','io_sha256')]:ck(label+' frozen SHA',sha(file)==case[key],{'actual':sha(file),'frozen':case[key]})
 skills={}
 for rel,h in case['skill_hashes'].items():
  p=db/'실행스킬'/case['skill']/rel;skills[rel]={'sha256':sha(p),'text':read(p)};ck('skill '+rel+' frozen SHA',sha(p)==h,{'actual':sha(p),'frozen':h})
 ck('fixture frozen SHA',sha(run/'fixture_before.json')==fixed['transforms'][int(k)-1]['before_map_sha256'],sha(run/'fixture_before.json'))
 changed=[{'path':p,'before':h,'after':sha(db/p) if (db/p).is_file() else None} for p,h in before.items() if not (db/p).is_file() or sha(db/p)!=h]
 extra=[p.relative_to(db).as_posix() for p in db.rglob('*') if p.is_file() and p.relative_to(db).as_posix() not in before]
 ck('non-target final preservation',all(x['path'] in case['allowed'] for x in changed),changed)
 coverage=[{'path':str(p.relative_to(run)),'bytes':p.stat().st_size,'sha256':sha(p)} for base in [out,run/'서비스이벤트'] for p in base.rglob('*') if p.is_file()]
 # The transcript and all logs are read in full; narrative strips repeated machine blocks for review.
 trans=read(out/'transcript.md');narrative=re.sub(r'(?:```[^\n]*\n.*?```|~~~[^\n]*\n.*?~~~)','[실제 원문 기계 블록은 개별 CLI·이벤트로 대조]',trans,flags=re.S)
 (HERE/(k.zfill(2)+'_transcript_narrative.txt')).write_text(narrative,encoding='utf-8')
 # Correlate every event, never infer mode activation from config alone.
 raw_events=[js(p) for p in sorted((run/'서비스이벤트').glob('*.json'))];events=[]
 for e in raw_events:
  req=e['request'];matched=[]
  for q in out.glob('*.json'):
   if not (q.name.endswith('.request.json') or q.name.endswith('_request.json')):continue
   if js(q)!=req:continue
   label=q.name.removesuffix('.request.json').removesuffix('_request.json')
   cmdfiles=[out/(label+s) for s in ['.command.json','.execution.json','_execution.json'] if (out/(label+s)).is_file()]
   if not cmdfiles:continue
   cmd=js(cmdfiles[0]);argv=cmd.get('args',cmd.get('argv',cmd.get('command')));exitcode=cmd.get('exit_code',cmd.get('exit',cmd.get('returncode')))
   sp=next((out/(label+s) for s in ['.stdout.txt','_stdout.txt'] if (out/(label+s)).is_file()),None)
   ep=next((out/(label+s) for s in ['.stderr.txt','_stderr.txt'] if (out/(label+s)).is_file()),None)
   stdout=js(sp) if sp else None;err=ep.read_bytes() if ep else None
   ok=stdout==e['response'] and exitcode==(0 if e['response']['ok'] else 2) and isinstance(argv,list) and str(run/'시험IO.py') in argv and argv[-1]==str(q) and err==b''
   matched.append({'file':cmdfiles[0].name,'argv':argv,'exit':exitcode,'stdout_event_equal':stdout==e['response'],'stderr_bytes':len(err) if err is not None else None,'passed':ok})
  ck('event '+str(e['sequence'])+' CLI original correlation',any(m['passed'] for m in matched),matched)
  events.append({k:v for k,v in e.items() if k!='response'}|{'response':{k:v for k,v in e.get('response',{}).items() if k!='text'}})
  if req['op']=='backup' and e['status']=='ok':ck('backup '+req['path']+' exact frozen bytes',sha(db/req['backup_path'])==before[req['path']],{'actual':sha(db/req['backup_path']),'frozen':before[req['path']]})
  if req['op']=='write' and 'requested_sha256' in e:ck('requested candidate exact SHA',sha(run/req['candidate_path'])==e['requested_sha256'],{'actual':sha(run/req['candidate_path']),'event':e['requested_sha256']})
 candidates=[]
 for e in raw_events:
  req=e['request']
  if req['op']=='write':
   cp=run/req['candidate_path']; backupreq=next((x['request'] for x in raw_events if x['request']['op']=='backup' and x['request']['path']==req['path'] and x['status']=='ok'),None)
   if backupreq:
    b=db/backupreq['backup_path'];candidates.append({'path':req['path'],'candidate':str(cp),'before':sha(b),'candidate_sha':sha(cp),'final':sha(db/req['path']),'diff':diff(js(b),js(cp))})
 if case['mode']=='backup_denied':
  ck('backup denial active',any('BACKUP_DENIED' in x.get('error','') for x in raw_events),events)
  ck('no write after backup denial',not any(x['request']['op'] in ['write','restore'] for x in raw_events),events)
 if case['mode'].startswith('external_'):
  e=next((x for x in raw_events if 'external_actor_sha256' in x),None)
  ck('external actual and final preserved',e is not None and sha(db/e['request']['path'])==e['external_actor_sha256'],{'event':e['sequence'] if e else None,'external_sha':e.get('external_actor_sha256') if e else None,'final_sha':sha(db/case['allowed'][0])})
  ck('no re-write or restore after external conflict',e is not None and not any(x['sequence']>e['sequence'] and x['request']['op'] in ['write','restore'] for x in raw_events),events)
 if case['mode']=='restore_denied':
  e=next((x for x in raw_events if 'RESTORE_DENIED' in x.get('error','')),None)
  ck('restore denial active/no op bypass',e is not None and not any(x['sequence']>e['sequence'] and x['request']['op'] in ['write','restore'] for x in raw_events),events)
 if case['mode']=='partial_second_write':
  w=[x for x in raw_events if x['request']['op']=='write'];ck('partial write active',len(w)==2 and 'PARTIAL_WRITE' in w[1].get('error','') and w[0]['status']=='ok',events)
  for rel in case['allowed']:ck('restored final '+rel,sha(db/rel)==before[rel],sha(db/rel))
 if case['mode']=='validation_after_write':ck('postsave failure and final restore',any('POSTSAVE_VALIDATION_FAILED' in x.get('error','') for x in raw_events) and any(x['request']['op']=='restore' and x['status']=='ok' for x in raw_events) and all(sha(db/p)==before[p] for p in case['allowed']),events)
 docs={p.relative_to(db).as_posix():read(p) for p in (db/'14_스킬재구성').glob('*') if p.is_file() and p.suffix in ['.md','.json']}
 r={'case':int(k),'name':case['name'],'run':str(run),'mode':case['mode'],'classification':case['classification'],'checks':checks,'provided_skill':skills,'current_guidance':docs,'changed':changed,'extra':extra,'candidates':candidates,'events':events,'coverage':coverage,'transcript_sha':sha(out/'transcript.md'),'task':read(run/'task.txt'),'result':read(out/'결과.md'),'timing':js(run/'timing.json') if (run/'timing.json').exists() else None}
 rows.append(r)
(HERE/'direct_audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for r in rows:
 print('CASE',r['case'],r['mode'],'CHANGED',json.dumps(r['changed'],ensure_ascii=False),'EXTRA',r['extra'])
 print('CHECKS',len(r['checks']),'FAILURES',json.dumps([x for x in r['checks'] if not x['passed']],ensure_ascii=False))
 print('EVENTS',json.dumps([{k:v for k,v in e.items() if k not in ['response']} for e in r['events']],ensure_ascii=False))
