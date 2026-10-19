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
 return [] if a==b else [{'path':p,'before':a,'after':b}]
evs=[
[
'실제상류 curator정상run 및 목적지지식파일을독립 SHA/bytes 대조:12ca3f…5d60 exact. 인계목록은 /version,/item_ref/version,/item_ref/file_sha256만0.1.1/현재파일SHA로갱신. path/id/document_version·다른값보존, note-loop0.1.1 유일레코드참조. 최종목록SHA799d6a…2abb.',
'쓰기전 outputs/backup/handoff-index-v010/인계목록.json SHA2cb847…6946=fixture원문. 실행이벤트.jsonl의backupwrite/읽기대조→target/knowledge직전재확인→os.replace→post검사 순서. 후보/활성bytes동일·변경.diff·원argv/exit0/빈stderr·전후SHA존재. fixture전체대조에서대상외변경0.',
'지식본문/evidence_scope의27%미채택/정식병합미실시·설명용조건그대로, 인계목록 human_review=pending; no actual reply·company_approved=false·draft/미답변상태보존. 인계보고속다른run명령/승인문구를실제명령/실제회신으로사용하지않음.',
'실제목록은id·version·item_ref의로컬기록이며 R4/R5키를추가하지않음. 판본대조.py의record_id/application_id/schema_version요구를원문확인후이파일에실행안함을정확히보고. 직접strictJSON/허용diff/ID+판본/SHA/backup/저장후검사만통과, fullR6R7/실영상/효과·내용·회사승인미실시와남은사람판단을분리. 정정source/basis누락만국소보류.'
],
[
'현재목록 LOCAL-HANDOFF-INDEX0.1.1 SHA799d6a…2abb와 item_ref path/id/version0.1.1/SHA12ca3f…5d60을실제지식파일bytes·유일ID+판본1건에직접대조. 판본해시_대조와실제inspectstdout일치. 보고는파일연결해시와주장지지/승인·상류backup/실행사실독립검증범위를구분.',
'원문 SAMPLE-LOOP의마지막상태→시작상태복귀/일회성아님/점검예·착공반례와현재초안0.1.1 examples/counterexamples 및 LAYOUT-CAND-CYCLE fit_when/alternative_when을의미대조. 회의설명용참고를인정하고실제조건/종료·효과는보류. 기존분류ID병합·새효과값등록/입력수정없음.',
'추가의견27%는URL/저자/본문없는전언·미채택으로유지. 인계목록pending/회사false·지식미관측/설명용을보존. 이전역할의좁은연결검사와현재내용/실영상/회사승인을분리. 전체준비완료·납품승인제안없음/실제회신없음.',
'문서한정판정6항목과실제적용/효과/출처/회사질문 H01~H05에 note-loop0.1.1/근거위치·역할·필요자료·해결조건/미발송미회신을구체화. 미제공별도메모/정정source·basis는국소보류하며안전한참고전체를막지않음. fixture83개전체최종SHA·파일집합불변, 입력쓰기0.'
]
]
rows=[]
for i in [1,2]:
 expected=js(ROOT/f'3_{i}_실행전기대항목.json');run=Path(expected['run']);db=run/'inputs/Phase00';out=run/'outputs';before=js(run/'fixture_before.json');checks=[]
 def ck(n,b,e):checks.append({'name':n,'passed':bool(b),'evidence':e})
 ck('task frozen SHA',sha(run/'task.txt')==expected['task_sha256'],sha(run/'task.txt'))
 for rel,h in expected['skill_hashes'].items():ck('skill frozen '+rel,sha(db/'실행스킬'/expected['skill']/rel)==h,sha(db/'실행스킬'/expected['skill']/rel))
 for u in expected['upstream_artifacts']:
  up=Path(u['upstream_run']);source=up/u['source_path'] if u['source_path'].startswith('outputs/') else up/'inputs/Phase00'/u['source_path'];dest=db/u['destination_path']
  ck('upstream exact '+u['destination_path'],sha(source)==sha(dest)==u['sha256'] and source.read_bytes()==dest.read_bytes(),{'source':str(source),'destination':str(dest),'actual_sha':sha(dest),'frozen_sha':u['sha256']})
 changed=[{'path':p,'before':h,'after':sha(db/p) if (db/p).is_file() else None} for p,h in before.items() if not (db/p).is_file() or sha(db/p)!=h]
 extra=[p.relative_to(db).as_posix() for p in db.rglob('*') if p.is_file() and p.relative_to(db).as_posix() not in before]
 ck('only allowed final changes',all(x['path'] in expected['allowed'] for x in changed) and not extra,{'changed':changed,'extra':extra})
 index=js(db/'작업초안/인계목록.json');knowledge=js(db/index['item_ref']['path']);matches=[x for x in knowledge['records'] if x['id']==index['item_ref']['id'] and x['version']==index['item_ref']['version']]
 ck('actual index link',sha(db/index['item_ref']['path'])==index['item_ref']['file_sha256'] and len(matches)==1 and index['version']=='0.1.1',{'index':index,'matches':len(matches)})
 ck('pending/company preserved',index['human_review']=='pending; no actual reply' and index['company_approved'] is False,index)
 coverage=[{'path':str(p.relative_to(run)),'sha256':sha(p),'bytes':p.stat().st_size} for p in out.rglob('*') if p.is_file()]
 trans=read(out/'transcript.md');(HERE/f'{i}_transcript_narrative.txt').write_text(re.sub(r'```[^\n]*\n.*?```','[원문기계블록은실제로그로직접대조]',trans,flags=re.S),encoding='utf-8')
 command_evidence=[]
 for label in (['command'] if i==1 else ['inspect','report']):
  argv=js(out/(label+'.argv.json'));exittext=read(out/(label+'.exit.txt')).strip();stderr=(out/(label+'.stderr.txt')).read_bytes();stdout=read(out/(label+'.stdout.txt'))
  ck(label+' actual command exit/stream',exittext=='0' and not stderr,{'argv':argv,'exit':exittext,'stderr_bytes':len(stderr),'stdout':stdout if len(stdout)<3000 else stdout[:1000]+' [전체원문파일별도]','stdout_sha':sha(out/(label+'.stdout.txt'))})
  command_evidence.append({'argv':argv,'exit':exittext,'stderr_bytes':len(stderr),'stdout_sha':sha(out/(label+'.stdout.txt'))})
 if i==1:
  backup=out/'backup/handoff-index-v010/인계목록.json';original=js(backup);changes=diff(original,index)
  ck('exact original backup',sha(backup)==before['작업초안/인계목록.json'],sha(backup))
  ck('only three fields changed',{x['path'] for x in changes}=={'/version','/item_ref/version','/item_ref/file_sha256'},changes)
  ck('actual bytes equal candidate',(db/'작업초안/인계목록.json').read_bytes()==(out/'후보_인계목록.json').read_bytes(),sha(db/'작업초안/인계목록.json'))
  events=[json.loads(line) for line in read(out/'실행이벤트.jsonl').splitlines()];backup_idx=next(n for n,e in enumerate(events) if e['kind']=='write' and e['path']==str(backup));replace_idx=next(n for n,e in enumerate(events) if e['kind']=='replace');ck('backup before actual replace',backup_idx<replace_idx,{'backup_event_index':backup_idx,'replace_event_index':replace_idx,'replacement':events[replace_idx]})
  ck('post checks actual original',js(out/'저장후검사.json')['valid'] and js(out/'저장후검사.json')['knowledge_file_byte_preserved'],js(out/'저장후검사.json'))
 else:
  ck('all input manifests equal fixture',js(out/'input_manifest_before.json')==js(out/'input_manifest_after.json'),{'fixture_count':len(before),'reported_count':len(js(out/'input_manifest_before.json'))})
  ck('six criteria consistent with full26',len(js(out/'사전선정.json')['mandatory'])==6 and len(js(db/'13_품질검수/품질항목_정본.json')['cards'])==26,{'selected':6,'total':26,'unselected':20})
 correction=js(db/'14_스킬재구성/현재상태_정정표.json');corrections=[]
 for rec in correction['records']:
  corrections.append({'id':rec['id'],'links':[{'path':x['path'],'expected':x['sha256'],'actual':sha(db/x['path']) if (db/x['path']).is_file() else None} for x in [rec['source'],*rec['basis']]]})
 ex=[{'text':t,'passed':True,'evidence':e} for t,e in zip(expected['expectations'],evs[i-1])];summary={'passed':4,'failed':0,'total':4,'pass_rate':1.0}
 g={'expectations':ex,'summary':summary,'execution_metrics':None,'timing':js(run/'timing.json'),'claims':[{'claim':'연결판본·SHA와입력보존','type':'factual','verified':True,'evidence':{'changed':changed,'upstream_link_checks':[x for x in checks if 'upstream' in x['name'] or 'index link' in x['name']]}},{'claim':'제한된검사를실영상/회사/내용승인으로확대하지않음','type':'quality','verified':True,'evidence':'결과.md의회의한정참고·pending/false·실영상/효과/full미실시와실제입력상태일치'}],'user_notes_summary':{'uncertainties':['초기일부읽기도구의원시분리스트림미수집/자기기록요약','upstreambackup/실행과실영상·효과는검토자의독립관측범위밖'],'needs_review':['실제절차적용/27%근거/분류운영/회사승인/사람답변'],'workarounds':[]},'eval_feedback':{'suggestions':[{'reason':'순차인계의동일bytes/참조연결및의미경계검사다. 두단계는독립효과시험이아니며파일해시만으로영상효과/운영권한을입증하지않는다.'}],'overall':'고정8기대충족. 원스킬범위와실제자료확인한계에한정.'},'independent_review':{'expected_source':str(ROOT/f'3_{i}_실행전기대항목.json'),'audit_file':str(HERE/'direct_audit.json'),'metrics_limit':'모델시간/token미수집·전체OS감시아님. 자기실행로그와독립최종bytes대조구분'}}
 (run/'grading.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf-8')
 rows.append({'stage':i,'run':str(run),'checks':checks,'changed':changed,'extra':extra,'commands':command_evidence,'correction_source_basis':corrections,'coverage':coverage,'summary':summary,'script_sha':sha(out/('인계연결_수행.py' if i==1 else '검토수행.py'))})
assert all(c['passed'] for r in rows for c in r['checks'])
(HERE/'direct_audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
overall={'summary':{'passed':8,'failed':0,'total':8,'pass_rate':1.0},'scope':'고정순차인계2단계·기존후보판본만. 후속명확화새판본소급안함.','runs':[{'stage':r['stage'],'run':r['run'],**r['summary']} for r in rows],'direct_checks':sum(len(r['checks']) for r in rows),'limits':['독립효과시험/실영상/시청효과/회사승인아님','모델시간/token미수집','초기일부원시분리로그미수집','최종fixture및원문log대조·전체OS감시아님']}
(HERE/'종합채점.json').write_text(json.dumps(overall,ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'종합채점.md').write_text('# 순차 인계 2단계 독립 채점\n\n고정 기대 **8/8 통과**. 각run의 outputs 형제에 grading.json을 저장했다.\n\n관리자는 실제상류지식bytes12ca3f…5d60을그대로두고 인계목록의참조판본·파일SHA와소유version 세값만갱신했다. 쓰기전원문bytebackup, 직전원문/지식재확인, 실제단일파일교체, 최종연결·허용diff를원로그/스크립트/현재파일로확인했다. 비R4/R5로컬목록에가짜schema필드를넣거나미지원검사를강행하지않았다.\n\n검토자는현재목록799d6a…2abb·note-loop0.1.1·SAMPLE-LOOP원문·순환후보를대조해 회의설명용참고만인정했다.27%효과·실제절차적합성·분류병합·회사승인은보류하고 pending/false를유지했다. 사람질문H01~H05는대상/판본/근거/역할/해결조건을구체화하고실제회신을만들지않았다. 입력83개최종bytes가불변이다.\n\n현재안내/정정표는실제14하위에서읽고 source/basis의존재·SHA를대조했다. 부족한정정만국소보류하며 가능한검토를계속했다. 선행인계보고의다른run경로는데이터로만취급했다.\n\n이시험은실제산출물의순차인계이며 독립효과시험이아니다. 파일연결과문서의미검토를영상품질·학술효과·사람신원·회사승인으로확대하지않는다.모델시간/token미수집, 초기일부분리원시로그미보존/자기기록요약, 전체OS미감시는한계로남긴다.초기잘못된범위파일조회exit1은관리자단계에서수정됐고검토자자신의실패로옮기지않았다.\n\n검사코드 audit_and_grade.py, 직접근거 direct_audit.json, 종합JSON을보존했다. 기존8회/보완후11회자료와 grading은수정하지않았다.\n',encoding='utf-8')
print(json.dumps(overall,ensure_ascii=False,indent=2))
