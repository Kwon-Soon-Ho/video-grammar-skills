"""Reviewed, bounded Phase00 R8-4 publication. No network, CU, API or shutdown."""
from 공통지원 import BASE,save as base_save,safe,check_links
from pathlib import Path
import hashlib,json,shutil,sys,subprocess,os,importlib.util
L=Path(__file__).parent.resolve();W=L/'R8_04_시험';RV=L/'R8_04_독립검토'
OUT='08_검증결과/R8_04_통합검증';F='14_스킬재구성';ST='2026-10-15_R8_04_최종정리'
BACK='backup/'+ST;FREEZE=L/'R8_04_최종게시_입력고정.json';OWN={};CTX={};ATTEMPTS={}
def io(p):
 p=Path(p);s=str(p)
 if s.startswith('\\\\?\\'):return p
 s=str(p.resolve())
 return Path('\\\\?\\UNC\\'+s[2:] if s.startswith('\\\\') else '\\\\?\\'+s)
sha=lambda p:hashlib.sha256(io(p).read_bytes()).hexdigest()
read=lambda p:json.loads(io(p).read_text(encoding='utf-8'))
current=lambda p:sha(p) if io(p).is_file() else None
def localwrite(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sources():
 rows=[]
 for folder,label,dest in [(W,'시험',BACK+'/실행원문'),(RV,'독립검토',OUT+'/독립검토/R8_04'),(L/'전체재검수','전체재검수',OUT+'/독립검토/전체재검수')]:
  for root,dirs,files in os.walk(io(folder)):
   dirs[:]=sorted(d for d in dirs if d not in {'__pycache__','고정문맥_검증전용','isolated','robustness','targeted_v3'})
   for name in sorted(files):
    p=Path(root)/name;rel=p.relative_to(io(folder))
    rows.append({'source':str(folder/rel),'destination':dest+'/'+rel.as_posix(),'sha256':sha(p)})
 for p in sorted(L.glob('R8_04*.py'))+[L/'R8_후보연결확인.py',L/'R8_01_뷰어작성.py',L/'공통지원.py',L/'R8_04_최종보고_초안.md']:
  rows.append({'source':str(p),'destination':BACK+'/작성도구/'+p.name,'sha256':sha(p)})
 return rows
def owned(rel,value):
 p=safe(BASE/rel)
 if rel in OWN:assert p.is_file() and sha(p)==OWN[rel],'Concurrent change: '+rel
 else:
  before=CTX['freeze']['D_before'].get(rel)
  assert (sha(p) if p.is_file() else None)==before,'Changed since final freeze: '+rel
 raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8') if not isinstance(value,str) else (value.strip()+'\n').encode('utf-8')
 ATTEMPTS[rel]={'before':sha(p) if p.is_file() else None,'intended_sha256':hashlib.sha256(raw).hexdigest(),'completed':False}
 localwrite(L/'R8_04_게시시도_진행기록.json',ATTEMPTS)
 base_save(rel,value,ST);OWN[rel]=sha(p)
 assert OWN[rel]==ATTEMPTS[rel]['intended_sha256'],'Unexpected saved bytes: '+rel
 ATTEMPTS[rel]['completed']=True;ATTEMPTS[rel]['saved_sha256']=OWN[rel];localwrite(L/'R8_04_게시시도_진행기록.json',ATTEMPTS)
def exact(src,rel,archive,expected=None):
 p=safe(BASE/rel);s=io(src);q=io(p);h=sha(s);q.parent.mkdir(parents=True,exist_ok=True)
 assert expected is not None and h==expected,'Source changed from frozen expectation: '+str(src)
 if q.exists():assert sha(q)==h,'Conflicting archive: '+rel
 else:shutil.copy2(s,q)
 assert sha(s)==h and sha(q)==h,'Copy/source mismatch: '+rel
 archive[rel]=h
def record_failure(exc):
 if not CTX.get('started'):return
 actual={p:{'attempt':a,'last_owned':OWN.get(p),'actual':sha(BASE/p) if (BASE/p).is_file() else None} for p,a in ATTEMPTS.items()}
 for rel in [F+'/진행상태.json',OUT+'/00_최종보고.md']:
  p=BASE/rel
  if rel in OWN and p.is_file() and sha(p)==OWN[rel]:
   v=read(p) if p.suffix=='.json' else p.read_text(encoding='utf-8')
   if isinstance(v,dict):v['stages']['R8-4']='publication_failed_not_complete';v['R8_4_technical_complete']=False
   else:v='# 게시 실패 — 완료 아님\n\n게시상태와 부분 기록을 확인한다.\n\n'+v
   base_save(rel,v,ST)
 marker=OUT+'/게시상태.json';p=BASE/marker
 if marker in OWN and p.is_file() and sha(p)==OWN[marker]:
  base_save(marker,{'publication_state':'failed','error':str(exc),'error_type':type(exc).__name__,'partial_owned_files':actual,'archive_completed':len(CTX.get('archive',{})),'R8_4_technical_complete':False,'not_atomic_or_complete_concurrency_control':True},ST)
 else:
  localwrite(L/'R8_04_게시실패_로컬.json',{'error':str(exc),'owned':actual,'reason':'completion marker changed externally or not owned; do not overwrite'})
def prepare():
 assert not FREEZE.exists(),'Preserve freeze; do not overwrite'
 assert not (BASE/OUT/'게시상태.json').exists()
 ledger=read(W/'실행완료_기록.json');assert len(ledger['runs'])==24 and all(v['status']=='completed' for v in ledger['runs'].values())
 scores={k:read(RV/rel)['summary'] for k,rel in [('original','채점/종합채점.json'),('post1','채점/보완후/종합채점.json'),('handoff','채점/순차인계/종합채점.json'),('post2','채점/경로회귀/종합채점.json')]}
 assert scores['original']=={'passed':38,'failed':0,'total':38,'pass_rate':1.0}
 assert scores['post1']['passed']==42 and scores['post1']['total']==43
 assert scores['handoff']['passed']==8 and scores['handoff']['total']==8
 assert scores['post2']['passed']==12 and scores['post2']['total']==12
 facts=read(W/'파일사실검사.json');assert facts['runs_checked']==22
 assert all(not r['unexpected_changed_originals'] and not r['unexpected_new_input_paths'] and not r['missing_originals'] and r['task_sha_matches'] for r in facts['rows'])
 hand=read(W/'인계사실검사.json');assert hand['stages_checked']==2 and all(not r['unexpected_changed_originals'] and not r['unexpected_new_input_paths'] and r['item_ref_matches_exact_knowledge_bytes'] for r in hand['rows'])
 public=[OUT+'/00_최종보고.md',OUT+'/01_실행과판본.json',OUT+'/게시상태.json',OUT+'/保全.json',OUT+'/보존목록.json',OUT+'/보존과최종연결_확인.json',F+'/현재후보_입력고정.json',F+'/진행상태.json',F+'/R8_현재사용안내.md','00_시작안내.md','01_진행현황.md',F+'/검증문맥/후보판본_보존연결.json']
 public.remove(OUT+'/保全.json')
 for i,n in [(1,'큐레이터'),(2,'기록관리자'),(3,'적용성검토자')]:public.append(f'08_검증결과/R8_0{i}_{n}/01_회신이후_현재안내.md')
 protected=set(read(BASE/'08_검증결과/R8_04_입력보존.json')['files'])
 protected|={p.relative_to(BASE).as_posix() for p in (BASE/F).rglob('*') if p.is_file()}
 for i,n in [(1,'큐레이터'),(2,'기록관리자'),(3,'적용성검토자')]:
  protected|={f'08_검증결과/R8_0{i}_{n}/'+x for x in ['00_결과안내.md','보존과최종연결_확인.json','게시상태.json','01_회신이후_현재안내.md']}
 localwrite(FREEZE,{'id':'r8-4-final-publication-freeze','source_files':sources(),'D_before':{r:current(BASE/r) for r in public},'D_read_snapshot':{r:current(BASE/r) for r in sorted(protected)},'scores':scores,'ledger_sha256':sha(W/'실행완료_기록.json'),'scope':'explicit source snapshots; excludes full/isolated copies, no source deletion','candidate_hashes':{p.relative_to(BASE).as_posix():sha(p) for p in (BASE/'06_맞춤스킬/재구성후보').rglob('*') if p.is_file()}})
 print(json.dumps({'frozen':len(read(FREEZE)['source_files']),'model_runs':24},ensure_ascii=False))
def main():
 frozen_bytes=io(FREEZE).read_bytes();f=json.loads(frozen_bytes.decode('utf-8'));CTX['freeze']=f
 audit_path=RV/'최종출고_독립판정.json';audit_bytes=io(audit_path).read_bytes();audit=json.loads(audit_bytes.decode('utf-8'))
 judgment_hashes={str(audit_path):hashlib.sha256(audit_bytes).hexdigest(),str(RV/'최종출고_독립판정.md'):sha(RV/'최종출고_독립판정.md')}
 assert audit['limited_technical_closure_supported'] is True and not audit['unresolved_blocking_findings']
 assert audit['publication_script_sha256']==sha(Path(__file__)) and audit['freeze_sha256']==hashlib.sha256(frozen_bytes).hexdigest()
 for r in f['source_files']:assert sha(Path(r['source']))==r['sha256'],'C changed after freeze: '+r['source']
 for r,h in f['candidate_hashes'].items():assert sha(BASE/r)==h
 for r,h in f['D_read_snapshot'].items():assert current(BASE/r)==h,'D read input changed since freeze: '+r
 # Protect all startup tracked domain inputs except our declared backed-up changes/restores.
 init=read(BASE/'08_검증결과/R8_04_입력보존.json')['files'];allowed=set()
 for n in ['1차보완_확인.json','2차보완_확인.json','2차행동보완_확인.json']:
  d=read(BASE/OUT/n)
  for x in d.get('changes',[]):allowed.add(x['path'])
  for x in d.get('restored_reports',[]):allowed.add(x['report'])
 # Restoration record key may vary, but only those exact sealed reports are permitted.
 allowed|={f'08_검증결과/R8_0{i}_{n}/00_결과안내.md' for i,n in [(1,'큐레이터'),(2,'기록관리자'),(3,'적용성검토자')]}
 allowed|={'00_시작안내.md','01_진행현황.md',F+'/진행상태.json'}
 changed={r for r,h in init.items() if sha(BASE/r)!=h};assert changed<=allowed,'Undeclared domain change: '+str(changed-allowed)
 CTX['started']=True;owned(OUT+'/게시상태.json',{'publication_state':'in_progress','completion_receipt_written':False})
 archive={};CTX['archive']=archive
 frozen={r['source']:r['sha256'] for r in f['source_files']}
 def frozen_exact(src,dest):exact(src,dest,archive,frozen.get(str(src)))
 for r in f['source_files']:exact(Path(r['source']),r['destination'],archive,r['sha256'])
 exact(FREEZE,BACK+'/최종입력고정.json',archive,audit['freeze_sha256'])
 for src,h in judgment_hashes.items():exact(Path(src),OUT+'/독립검토/'+Path(src).name,archive,h)
 # Human-facing viewer copies retain official raw+LICENSE+display provenance.
 for cat in ['1_새사례','2_실제쓰기','3_스킬인계','4_보완후재시험','5_경로보완회귀']:
  folder=W/'뷰어'/(cat+'_독립채점후')
  for p in folder.iterdir():
   if p.is_file():frozen_exact(p,OUT+'/출력뷰어/'+cat+'/'+p.name)
 frozen_exact(L/'R8_후보연결확인.py','07_실행도구/R8_후보연결확인.py')
 frozen_exact(RV/'현재문맥/full_copy_structure_receipt.json',F+'/검증문맥/기존문맥구조조회_영수증.json')
 frozen_exact(RV/'현재문맥/full_R6_R7_copy_set.json',F+'/검증문맥/구조조회_파일목록.json')
 summary={'actual_model_runs':24,'cohorts':{'new_requests':3,'original_real_write_fault':5,'post_first_correction':11,'sequential_handoff':2,'post_second_path_correction':3},'prepared_unexecuted_2b':2,'actual_video_runs':0,'scores':f['scores'],'candidate_versions':{},'candidate_hashes':f['candidate_hashes'],'timing':{'total_tokens':None,'duration_ms':None},'not_old_new_comparison_or_generalization_proof':True}
 for name in ['video-knowledge-curator','video-record-steward','video-guidance-reviewer']:
  import re
  summary['candidate_versions'][name]=re.search(r'(?m)^  version: "([^"]+)"',(BASE/'06_맞춤스킬/재구성후보'/name/'SKILL.md').read_text(encoding='utf-8')).group(1)
 owned(OUT+'/01_실행과판본.json',summary)
 table='| 시험 묶음 | 실제 시행 | 독립 조건 판정 |\n|---|---:|---|\n| 새 요청3 + 원래 쓰기·실패5 | 8 | 38/38, 보호 계약/오기 한계 별도 |\n| 1차 보완 후 정상·실패 분기 | 11 | 42/43, 안내 부재 오보고1건 실패 보존 |\n| 큐레이터 → 기록 관리자 → 검토자 실제 순차 인계 | 2 | 8/8, 독립 효과 비교 아님 |\n| 2차 경로·상태 보완 표적 회귀 | 3 | 12/12, 이전 자료 재사용 회귀 |'
 report=(L/'R8_04_최종보고_초안.md').read_text(encoding='utf-8').replace('{{RESULT_TABLE}}',table);owned(OUT+'/00_최종보고.md',report)
 guide=(BASE/F/'R8_현재사용안내.md').read_text(encoding='utf-8');start=guide.index('2026-10-15');end=guide.index('\n\n',start)
 guide=guide[:start]+'2026-10-15 · R8-1/2/3 출력 구성 유지 회신을 접수했고, R8-4와 전체 재검수/2차 보완의 한정 기술검수를 종료했다. [최종 결과](../'+OUT+'/00_최종보고.md)를 확인한다. 후보 기본 전환·회사 승인·실영상 효과/포괄 Phase00 승인은 별도이며 01-A 구현은 시작하지 않았다.'+guide[end:]
 guide+='\n\n## R8 후보 연결 확인\n\n[별도 R8 문맥](현재후보_입력고정.json)과 `07_실행도구/R8_후보연결확인.py`는 후보11파일·현재 정정의 원문/근거·기존 구조조회 영수증을 읽기 전용으로 대조한다. 기존 R6/R7 pin을 바꾸지 않으며 live 재실행·내용/권리/영상/채택 승인 기능이 아니다. `python -B <도구> --base <Phase 00 루트>`로 실행하고 stdout을 결과 폴더에 보존한다.\n'
 owned(F+'/R8_현재사용안내.md',guide)
 state=read(BASE/F/'진행상태.json');state['version']='0.1.11';state['R8_4_technical_complete']=True;state['R8_complete']=False;state['Phase00_complete']=False;state['stages']['R8-4']='bounded_technical_closure_complete_not_adopted';state['required_independent_followup_in_R8_4']='completed_with_preserved_failures_and_targeted_corrections';state['whole_phase_reaudit']={'first_correction':'applied_independently_rechecked','second_correction':'document_and_behavior_fixes_rechecked','overall_semantic_or_production_approval':False};state['R8_4_substages']={x:'bounded_execution_and_independent_review_complete' for x in state['R8_4_substages']};state['R8_4_results']=summary
 for k in ['R8-1','R8-2','R8-3']:state['stages'][k]='user_feedback_received_R8_4_followup_complete_not_adopted'
 owned(F+'/진행상태.json',state)
 intro='# Phase 00 시작 안내\n\n2026-10-15 · R1~R7의 한정 설계·기록 기반과 R8-4 기술검수/전체 재검수·2차 보완을 정리했다. [최종 보고]('+OUT+'/00_최종보고.md) → [현재 스킬 사용 안내]('+F+'/R8_현재사용안내.md) → [01-A 자료 준비](09_다음단계인계/01-A_자료준비안내.md)를 읽는다.\n\n후보 기본 전환·회사 승인·실제 영상 성능·포괄 Phase00 최종 승인은 아직이다. 기존 시범 운영 권한은 유지하고 01-A 구현은 시작하지 않았다. 고정 원문의 옛 단계 상태는 [별도 정정표]('+F+'/현재상태_정정표.json)의 원문/근거 SHA와 함께 확인한다.\n'
 owned('00_시작안내.md',intro)
 owned('01_진행현황.md','# 현재 진행 현황\n\n2026-10-15 · [최종 결과]('+OUT+'/00_최종보고.md)\n\n| 범위 | 상태 |\n|---|---|\n| R1~R7 | 한정 설계/기록/지식/검수/평가계획 정리 및 이번 전체 재검수 |\n| R8-1/2/3 | 구성 유지·후속 진행 회신 접수 |\n| R8-4 | 새 요청·실제 쓰기/실패·순차 인계·전체 재검수/2차 보완의 한정 기술검수 종료 |\n| 기본 전환/회사 승인/포괄 Phase00 최종 승인 | 미실시·별도 판단 |\n| 실제 영상 분석·01-A 구현 | 미시작 |\n\n[기계 상태]('+F+'/진행상태.json), [현재 사용 안내]('+F+'/R8_현재사용안내.md), [자료 준비](09_다음단계인계/01-A_자료준비안내.md)를 따른다. 과거 봉인보고는 당시 상태이며 회신 이후 안내와 분리해 보존했다.\n')
 oldmap=[]
 initial=read(BASE/'08_검증결과/R8_04_입력보존.json')['files']
 for name in summary['candidate_versions']:
  prefix=f'06_맞춤스킬/재구성후보/{name}/';files={r:h for r,h in initial.items() if r.startswith(prefix)}
  for r,h in files.items():assert sha(BASE/'backup/2026-10-15_R8_04_착수/입력정본'/r)==h
  oldmap.append({'skill':name,'original_report_candidate_snapshot':'backup/2026-10-15_R8_04_착수/입력정본/'+prefix,'files':files,'current_candidate_version':summary['candidate_versions'][name]})
 owned(F+'/검증문맥/후보판본_보존연결.json',{'scope':'historical_report_candidate_links_are_not_current_version_proof','records':oldmap,'per_trial_exact_supplied_versions':'final archive fixture_before and skill_hashes; no retroactive replacement'})
 for i,n in [(1,'큐레이터'),(2,'기록관리자'),(3,'적용성검토자')]:
  rel=f'08_검증결과/R8_0{i}_{n}/01_회신이후_현재안내.md';t=(BASE/rel).read_text(encoding='utf-8');t+='\n\nR8-4 기술검수는 [최종 보고](../R8_04_통합검증/00_최종보고.md)에 정리했다. 봉인보고의 후보 링크는 현재 파일을 열 수 있으므로 당시 판본은 [보존 연결](../../14_스킬재구성/검증문맥/후보판본_보존연결.json)과 해당 시행 입력으로 확인한다.\n';owned(rel,t)
 spec=importlib.util.spec_from_file_location('r8context',L/'R8_후보연결확인.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 contextfiles=set(m.FOUNDATION)|set(m.EXTRA)|{f'06_맞춤스킬/재구성후보/{n}/{r}' for n,rs in m.SKILLS.items() for r in rs}
 owned(F+'/현재후보_입력고정.json',{'id':'r8-candidate-link-context','version':'0.1.0','scope':'R8_candidate_references_and_errata_only','candidate_only':True,'candidate_adopted':False,'company_approved':False,'operational_release':False,'files':{r:sha(BASE/r) for r in sorted(contextfiles)},'candidate_versions':summary['candidate_versions']})
 py=BASE/'.환경/Scripts/python.exe';env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8');queries=[]
 for tool in ['R6_출처사용검사.py','R6_사람검수.py','R6_통합조회.py','R7_연결확인.py','R8_후보연결확인.py']:
  args=[str(py),'-B',str(BASE/'07_실행도구'/tool),'--base',str(BASE)];r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',env=env,timeout=60)
  queries.append({'tool':tool,'args':args,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr});assert r.returncode==0,(tool,r.stdout,r.stderr)
 owned(OUT+'/보존목록.json',{'files':archive,'excluded_duplicate_trees':['C full800 fixed copy','technical isolated/robustness/targeted_v3 copies'],'exclusion_policy':'existing C originals untouched; receipts/inventories/code/audit logs archived; no additional restricted-source bulk copies'})
 docs=[BASE/r for r in OWN if r.endswith('.md')];bad=check_links(docs);assert not bad,bad
 assert all(sha(BASE/r)==h for r,h in f['candidate_hashes'].items())
 for r,h in archive.items():assert sha(BASE/r)==h
 for r,h in m.FOUNDATION.items():assert sha(BASE/r)==h
 def final_integrity():
  for r,h in OWN.items():assert sha(BASE/r)==h,'Owned publication changed: '+r
  for row in f['source_files']:assert sha(Path(row['source']))==row['sha256'],'C source changed after copying: '+row['source']
  assert sha(FREEZE)==audit['freeze_sha256']
  for src,h in judgment_hashes.items():assert sha(Path(src))==h
  for r,h in f['candidate_hashes'].items():assert sha(BASE/r)==h
  actual_candidates={p.relative_to(BASE).as_posix() for p in (BASE/'06_맞춤스킬/재구성후보').rglob('*') if p.is_file()}
  assert actual_candidates==set(f['candidate_hashes']),'Candidate file set changed after freeze'
  for r,h in f['D_read_snapshot'].items():
   assert current(BASE/r)==OWN.get(r,h),'D read input changed: '+r
  for r,h in read(BASE/F/'현재후보_입력고정.json')['files'].items():assert sha(BASE/r)==h,'R8 referenced file changed: '+r
  for r,h in init.items():
   if r not in allowed:assert sha(BASE/r)==h,'Protected initial source changed: '+r
  for r,h in archive.items():assert sha(BASE/r)==h,'Archive changed: '+r
 final_integrity()
 receipt={'id':'r8-4-final-publication-receipt','publication_script_sha256':sha(Path(__file__)),'freeze_sha256':sha(FREEZE),'report_sha256':sha(BASE/OUT/'00_최종보고.md'),'summary_sha256':sha(BASE/OUT/'01_실행과판본.json'),'archive_manifest_sha256':sha(BASE/OUT/'보존목록.json'),'archive_file_count':len(archive),'current_candidate_context_sha256':sha(BASE/F/'현재후보_입력고정.json'),'owned_content_hashes':{r:h for r,h in OWN.items() if r!=OUT+'/게시상태.json'},'source_initial_changed_paths':sorted(changed),'read_only_final_queries':queries,'local_link_errors':bad,'R8_4_technical_complete':True,'R8_complete':False,'Phase00_complete':False,'phase01a_started':False,'candidate_adopted':False,'company_approved':False,'actual_video_runs':0,'not_atomic_snapshot_or_all_OS_IO_proof':True}
 owned(OUT+'/보존과최종연결_확인.json',receipt)
 final_integrity()
 owned(OUT+'/게시상태.json',{'publication_state':'complete','receipt':'보존과최종연결_확인.json','receipt_sha256':sha(BASE/OUT/'보존과최종연결_확인.json'),'R8_4_technical_complete':True,'candidate_adopted':False,'R8_complete':False,'Phase00_complete':False,'phase01a_started':False})
 print(json.dumps({'publication':'complete','archive_files':len(archive),'runs':24,'read_checks':len(queries)},ensure_ascii=False))
if __name__=='__main__':
 try:
  if len(sys.argv)>1 and sys.argv[1]=='--freeze':prepare()
  else:main()
 except Exception as e:record_failure(e);raise
