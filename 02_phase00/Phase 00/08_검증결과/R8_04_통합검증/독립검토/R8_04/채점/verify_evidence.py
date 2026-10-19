from pathlib import Path
import json,hashlib,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]/'R8_04_시험'
def txt(p):return p.read_text(encoding='utf-8-sig')
def js(p):return json.loads(txt(p))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def changes(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return sum((changes(a.get(k),b.get(k),p+'/'+k) for k in a.keys()|b.keys()),[])
 if isinstance(a,list):return [p] if len(a)!=len(b) else sum((changes(x,y,p+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [p]
rows=[]
for group in ['1_새사례','2_실제쓰기']:
 for run in sorted((ROOT/group).glob('*/candidate')):
  out=run/'outputs';db=run/'inputs/Phase00';r={'run':str(run),'checks':[],'command_checks':[],'observations':[]}
  def check(name,result,ev):r['checks'].append({'name':name,'passed':bool(result),'evidence':ev})
  if group=='2_실제쓰기':
   events=[js(p) for p in sorted((run/'서비스이벤트').glob('*.json'))]
   for e in events:
    req=e['request'];matches=[]
    for q in out.glob('*.request.json'):
     if js(q)==req:
      label=q.name[:-len('.request.json')];logs=list(out.glob(label+'.execution.json'))+list(out.glob(label+'.command.json'))
      if not logs:continue
      rec=js(logs[0]);argv=rec.get('args',rec.get('argv'));exitcode=rec.get('exit_code',rec.get('exit'))
      stdout=js(out/(label+'.stdout.txt'));stderr=(out/(label+'.stderr.txt')).read_bytes()
      ok=stdout==e['response'] and exitcode==(0 if stdout['ok'] else 2) and str(run/'시험IO.py') in argv and argv[-1]==str(q) and not stderr
      matches.append({'label':label,'execution':logs[0].name,'exit':exitcode,'stdout_equals_event_response':stdout==e['response'],'stderr_bytes':len(stderr),'correct_cli_and_request':str(run/'시험IO.py') in argv and argv[-1]==str(q),'passed':ok})
    check('event '+str(e['sequence'])+' actual CLI correlation',any(m['passed'] for m in matches),matches)
   for e in events:
    if e['request']['op']=='backup':
     p=db/e['request']['backup_path']; rel=e['request']['path'];h=js(run/'fixture_before.json')[rel]
     check('backup exact '+rel,sha(p)==h,{'backup_sha':sha(p),'fixture_sha':h})
    if e['request']['op']=='write':
     cand=run/e['request']['candidate_path'];target=e['request']['path'];back=next(db/x['request']['backup_path'] for x in events if x['request']['op']=='backup' and x['request']['path']==target)
     r['observations'].append({'target':target,'candidate_sha':sha(cand),'event_requested_sha':e['requested_sha256'],'candidate_json_changed_paths':changes(js(back),js(cand)),'final_sha':sha(db/target),'backup_sha':sha(back)})
     check('candidate request SHA '+target,sha(cand)==e['requested_sha256'],str(cand))
   writes=[e for e in events if e['request']['op']=='write'];restores=[e for e in events if e['request']['op']=='restore']
   r['event_order']=[{'seq':e['sequence'],'op':e['request']['op'],'status':e['status'],'error':e.get('error')} for e in events]
   if len(writes)==2:
    r4=out/'R4_후보.json';r5=js(out/'R5_후보.json')
    check('R5 link actual new R4 bytes',r5['linked_r4_record']['sha256']==sha(r4)==writes[0]['service_owned_written_sha256'] and r5['version']=='0.1.1' and r5['linked_r4_record']['version']=='0.1.1',r5['linked_r4_record'])
    part=out/'13-복구전실패본-R5.bin'
    check('partial actual prefix',part.read_bytes()==(out/'R5_후보.json').read_bytes()[:927] and sha(part)==writes[1]['service_owned_written_sha256'],{'bytes':part.stat().st_size,'sha':sha(part)})
   ext=[e for e in events if 'external_actor_sha256' in e]
   if ext:check('external final bytes preserved without restore',sha(db/ext[0]['request']['path'])==ext[0]['external_actor_sha256'] and not restores,{'final':sha(db/ext[0]['request']['path']),'external':ext[0]['external_actor_sha256'],'restore_count':len(restores)})
   denied=[e for e in restores if 'RESTORE_DENIED' in e.get('error','')]
   if denied:check('no write or restore after denied',not [e for e in events if e['sequence']>denied[0]['sequence'] and e['request']['op'] in ['write','restore']],r['event_order'])
  else:
   if 'eval-01-' in run.parent.name:
    back=next((out/'backup').rglob('*.json'));target=db/'작업초안/연결설명_지식초안.json';h=js(run/'fixture_before.json')['작업초안/연결설명_지식초안.json']
    check('original backup fixture SHA',sha(back)==h,{'backup_sha':sha(back),'fixture_sha':h})
    check('candidate actual bytes',target.read_bytes()==(out/'수정후_후보.json').read_bytes(),sha(target))
    r['observations'].append({'candidate_changes':changes(js(back),js(target))})
   if 'eval-02-' in run.parent.name:
    for label in ['r4','r5']:
     d=js(out/(label+'.stdout.json'));check(label+' structural stdout',d['valid'] and not d['errors'] and (out/(label+'.stderr.txt')).stat().st_size==0,{'valid':d['valid'],'errors':d['errors'],'human_review_queue_count':len(d.get('human_review_queue',[]))})
   if 'eval-03-' in run.parent.name:
    src=js(db/'자료/등록출처.json');check('registered source exact SHA',sha(db/src['path'])==src['sha256'],src)
    r['observations'].append({'quality_cards_total':len(js(db/'13_품질검수/품질항목_정본.json')['cards']),'report_selected_criteria':len(re.findall(r'^\| Q-',txt(out/'검토결과.md'),flags=re.M))})
  # Hashes preserve every relevant original; no executor or service is rerun.
  r['transcript_sha']=sha(out/'transcript.md');r['timing']=js(run/'timing.json')
  rows.append(r)
(HERE/'verified_evidence.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'run':Path(r['run']).parent.name,'checks':len(r['checks']),'failures':[x for x in r['checks'] if not x['passed']],'observations':r['observations']} for r in rows],ensure_ascii=False,indent=2))
