from pathlib import Path
import json,hashlib,re,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]/'R8_04_시험'
def read(p):return p.read_text(encoding='utf-8-sig')
def js(p):return json.loads(read(p))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def diff(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return sum((diff(a.get(k),b.get(k),p+'/'+k) for k in a.keys()|b.keys()),[])
 if isinstance(a,list):return [p] if len(a)!=len(b) else sum((diff(x,y,p+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [p]
expected=js(ROOT/'5_실행전기대항목.json');fixed=js(ROOT/'5_고정기록.json');assert sha(ROOT/'5_실행전기대항목.json')==fixed['expectations_sha256']
limit=3 if '--all-complete' in sys.argv else 2
rows=[]
for k,case in expected['cases'].items():
 if int(k)>limit:continue
 run=Path(case['run']);db=run/'inputs/Phase00';out=run/'outputs';before=js(run/'fixture_before.json');checks=[]
 def ck(n,b,e):checks.append({'name':n,'passed':bool(b),'evidence':e})
 for label,p,h in [('task',run/'task.txt',case['task_sha256']),('IO',run/'시험IO.py',case['io_sha256']),('config',run/'시험설정.json',case['config_sha256'])]:ck('frozen '+label,sha(p)==h,{'actual':sha(p),'frozen':h})
 skillfiles={}
 for rel,h in case['skill_hashes'].items():
  p=db/'실행스킬'/case['skill']/rel;ck('frozen skill '+rel,sha(p)==h,{'actual':sha(p),'frozen':h});skillfiles[rel]={'sha':sha(p),'text':read(p)}
 changed=[{'path':p,'before':h,'after':sha(db/p) if (db/p).is_file() else None} for p,h in before.items() if not (db/p).is_file() or sha(db/p)!=h];extra=[p.relative_to(db).as_posix() for p in db.rglob('*') if p.is_file() and p.relative_to(db).as_posix() not in before]
 ck('non-target final preservation',all(x['path'] in case['allowed'] for x in changed),{'changed':changed,'extra':extra})
 coverage=[{'path':str(p.relative_to(run)),'sha':sha(p),'bytes':p.stat().st_size} for base in [out,run/'서비스이벤트'] for p in base.rglob('*') if p.is_file()]
 trans=read(out/'transcript.md');(HERE/f'{int(k):02}_transcript_narrative.txt').write_text(re.sub(r'(?:```[^\n]*\n.*?```|~~~[^\n]*\n.*?~~~)','[원문기계블록은개별CLI로직접대조]',trans,flags=re.S),encoding='utf-8')
 events=[js(p) for p in sorted((run/'서비스이벤트').glob('*.json'))];candidate_rows=[]
 for e in events:
  req=e['request'];matches=[]
  for q in out.glob('*.request.json'):
   if js(q)!=req:continue
   label=q.name.removesuffix('.request.json');p=next((out/(label+s) for s in ['.exit.json','.command.json','.execution.json','.process.json'] if (out/(label+s)).is_file()),None)
   if not p:continue
   d=js(p);argv=d.get('argv',d.get('args',[]));code=d.get('exit_code',d.get('exit'));stdout=js(out/(label+'.stdout.txt'));stderr=(out/(label+'.stderr.txt')).read_bytes()
   matches.append({'file':p.name,'argv':argv,'exit':code,'response_equal':stdout==e['response'],'stderr_bytes':len(stderr),'passed':stdout==e['response'] and code==(0 if stdout['ok'] else 2) and str(run/'시험IO.py') in argv and argv[-1]==str(q) and not stderr})
  ck('event '+str(e['sequence'])+' actual CLI correlation',any(m['passed'] for m in matches),matches)
  if req['op']=='backup' and e['status']=='ok':ck('backup exact '+req['path'],sha(db/req['backup_path'])==before[req['path']],{'backup':str(db/req['backup_path']),'sha':sha(db/req['backup_path'])})
  if req['op']=='write':
   cp=run/req['candidate_path'];ck('candidate exact event SHA',sha(cp)==e.get('requested_sha256'),sha(cp));back=next(db/x['request']['backup_path'] for x in events if x['request']['op']=='backup' and x['request']['path']==req['path'])
   candidate_rows.append({'path':req['path'],'candidate_sha':sha(cp),'changed_fields':diff(js(back),js(cp)),'final_sha':sha(db/req['path'])})
 tablepath=db/'14_스킬재구성/현재상태_정정표.json';guidepath=db/'14_스킬재구성/R8_현재사용안내.md';table=js(tablepath)
 lookupfile=next((p for p in [out/'현재상태_실제조회.json',out/'현재상태조회.json',out/'현재상태확인.json',out/'현재상태_경로확인.json'] if p.exists()),None)
 lookup=js(lookupfile) if lookupfile else None
 current=[]
 for r in table['records']:
  links=[{'kind':'source',**r['source']}]+[{'kind':'basis',**b} for b in r['basis']];refs=[]
  for x in links:
   p=db/x['path'];refs.append({'kind':x['kind'],'path':x['path'],'exists':p.is_file(),'actual_sha':sha(p) if p.is_file() else None,'expected_sha':x['sha256'],'match':p.is_file() and sha(p)==x['sha256']})
  current.append({'id':r['id'],'all_match':all(x['match'] for x in refs),'refs':refs})
 # Independently check the executor's lookup records where a consistent shape exists.
 if lookup:
  guide_records=lookup.get('guidance_files_and_tools',lookup.get('guidance',lookup.get('notice_paths',[])))
  for p in [guidepath,tablepath]:
   found=next((x for x in guide_records if x.get('path',x.get('queried_path'))==str(p)),None)
   ck('actual guidance lookup '+p.name,found is not None and found['exists'] and (found.get('sha256') is None or found['sha256']==sha(p)),{'actual_sha':sha(p),'reported':found,'note':'case3존재기록에SHA는없음;실제자료독립SHA대조로보완'})
  corrections=lookup.get('errata',lookup.get('corrections',lookup.get('records',[])))
  for c in current:
   rep=next((x for x in corrections if x['id']==c['id']),None)
   if rep:
    reported=rep.get('applicable',rep.get('applied',rep.get('applicability')=='apply' if 'applicability' in rep else None));ck('local correction '+c['id'],reported==c['all_match'],{'actual_all_match':c['all_match'],'reported':reported})
 if case['mode']=='restore_denied':
  denial=next((e for e in events if 'RESTORE_DENIED' in e.get('error','')),None)
  ck('restore denial and no bypass after',denial and not any(e['sequence']>denial['sequence'] and e['request']['op'] in ['write','restore'] for e in events),[{'seq':e['sequence'],'op':e['request']['op'],'status':e['status']} for e in events])
  ck('postsave validation fault active',any('POSTSAVE_VALIDATION_FAILED' in e.get('error','') for e in events),[e.get('error') for e in events])
  ck('full candidate retained after denial',(db/case['allowed'][0]).read_bytes()==(out/'후보.json').read_bytes(),sha(db/case['allowed'][0]))
 if case['mode']=='partial_second_write':
  w=[e for e in events if e['request']['op']=='write'];part=out/'R5_복구직전.bytes';cp=out/'R5_후보.json';r4=out/'R4_후보.json';r5=js(cp)
  ck('partial active and exact prefix',len(w)==2 and w[0]['status']=='ok' and 'PARTIAL_WRITE' in w[1].get('error','') and part.read_bytes()==cp.read_bytes()[:cp.stat().st_size//3] and sha(part)==w[1]['service_owned_written_sha256'],{'part_bytes':part.stat().st_size,'part_sha':sha(part)})
  ck('R5 actual R4 reference',r5['version']==js(r4)['version']=='0.1.1' and r5['linked_r4_record']['sha256']==sha(r4)==w[0]['service_owned_written_sha256'],r5['linked_r4_record'])
  for rel in case['allowed']:ck('final exact restored '+rel,sha(db/rel)==before[rel],sha(db/rel))
 if case['mode']=='external_after_write':
  ext=next((e for e in events if 'external_actor_sha256' in e),None)
  ck('external full write/final exact/no later overwrites',ext is not None and ext['status']=='ok' and sha(db/ext['request']['path'])==ext['external_actor_sha256'] and not any(e['sequence']>ext['sequence'] and e['request']['op'] in ['write','restore'] for e in events),ext)
 rows.append({'case':int(k),'run':str(run),'mode':case['mode'],'checks':checks,'skill':skillfiles,'changed':changed,'extra':extra,'candidates':candidate_rows,'events':events,'guidance':{'guide_sha':sha(guidepath),'table_sha':sha(tablepath),'actual_corrections':current,'reported_lookup':lookup},'coverage':coverage,'transcript_sha':sha(out/'transcript.md'),'result':read(out/'결과.md'),'task':read(run/'task.txt'),'timing':js(run/'timing.json') if (run/'timing.json').exists() else None})
(HERE/'direct_audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'case':r['case'],'checks':len(r['checks']),'failures':[x for x in r['checks'] if not x['passed']],'changed':r['changed'],'corrections':[(c['id'],c['all_match']) for c in r['guidance']['actual_corrections']]} for r in rows],ensure_ascii=False,indent=2))
