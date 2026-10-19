from pathlib import Path
import json, hashlib, copy, subprocess, sys, os
run=Path.cwd().resolve(); db=run/'inputs/Phase00'; out=run/'outputs'
assert db.is_relative_to(run) and out.resolve().is_relative_to(run)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def strict(raw):
 def pairs(xs):
  d={}
  for k,v in xs:
   if k in d:raise ValueError('duplicate key: '+k)
   d[k]=v
  return d
 def reject(x):raise ValueError('nonfinite: '+x)
 return json.loads(raw.decode('utf-8-sig'),object_pairs_hook=pairs,parse_constant=reject)
def write(name,obj):
 p=out/name
 assert not p.exists(),str(p)
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
source=db/'작업초안/디자인적용_초안.json'; backup=db/'backup/사용자지정백업'
for p in [db,source.parent,backup.parent,out]:
 assert p.resolve().is_relative_to(run),str(p)
 assert not (p.stat().st_file_attributes & 1024),str(p)
raw=source.read_bytes(); original=strict(raw); blocker=backup.read_bytes()
assert backup.is_file() and not backup.is_symlink()
backup_error=None
try:
 backup.mkdir(exist_ok=False)
except OSError as e:backup_error={'type':type(e).__name__,'message':str(e),'errno':e.errno,'winerror':getattr(e,'winerror',None)}
assert backup_error is not None,'Expected preexisting conflict; no target writes permitted'
proposal=copy.deepcopy(original)
proposal['purpose']='삼안 강조색 후보를 비교하는 검토용 초안.'
proposal['version']='0.1.1'
changes=[{'pointer':'/'+k,'before':original.get(k),'after':proposal.get(k)} for k in original if original.get(k)!=proposal.get(k)]
assert {x['pointer'] for x in changes}=={'/purpose','/version'}
write('디자인적용_미반영수정안_v0.1.1.json',proposal)
write('변경제안_diff.json',{'applied':False,'changes':changes,'all_other_values_equal':all(original[k]==proposal[k] for k in original if k not in ['purpose','version'])})
checks=[]
def check(label,args):
 cp=subprocess.run([sys.executable,'-B','-X','utf8',*map(str,args)],cwd=run,capture_output=True,text=True,encoding='utf-8')
 (out/(label+'_stdout.json')).write_text(cp.stdout,encoding='utf-8')
 (out/(label+'_stderr.txt')).write_text(cp.stderr,encoding='utf-8')
 try:result=strict(cp.stdout.encode('utf-8'))
 except Exception as e:result={'parse_error':str(e)}
 row={'name':label,'command':[sys.executable,'-B','-X','utf8',*map(str,args)],'exit_code':cp.returncode,'stdout':label+'_stdout.json','stderr':label+'_stderr.txt','result':result}
 checks.append(row);return row
checker=db/'07_실행도구/R5_디자인적용검사.py'
before=check('R5_現초안검사',[checker,source])
candidate=check('R5_수정안검사',[checker,out/'디자인적용_미반영수정안_v0.1.1.json'])
version=check('판본대조_원초안대미반영안',[db/'실행스킬/video-record-steward/scripts/판본대조.py','--before',source,'--after',out/'디자인적용_미반영수정안_v0.1.1.json'])
replypath=db/'05_출처와검토/검수와사용범위/사람답변원문/2026-10-15_8회사CI_최신자료와산하AI부재.json'
replyraw=replypath.read_bytes(); reply=strict(replyraw)
ledger=strict((db/'05_출처와검토/검수와사용범위/사람검수_접수대장.json').read_bytes())
event=ledger['events'][0]
requests=strict((db/'05_출처와검토/검수와사용범위/사람검수_요청목록.json').read_bytes())
request=next(x for x in requests['requests'] if x['request_id']==event['request_id'])
reply_check={'scope':'부분 원문/질문/대장 대조. full R6 현재문맥 검증 아님','reply_id':reply['id'],'reply_version':reply['version'],'actual_reply_sha256':sha(replyraw),'ledger_reply_pin_matches':event['reply_evidence_pin']['sha256']==sha(replyraw) and event['reply_evidence_pin']['version']==reply['version'],'raw_reply_matches':event['raw_reply']==reply['reply'],'request_id':request['request_id'],'request_version_matches':request['version']==event['request_version'],'question_matches':request['question']==reply['question'],'question_wording_note':'대장의 질문은 요약형이며 원문은 별도 질문 전사. 문자열 일치는 보장하지 않고 대상/범위를 읽어 대조함.','covered_scope_ids':event['covered_scope_ids'],'unresolved_scope_ids':event['unresolved_scope_ids'],'not_confirmed':reply['not_confirmed'],'authority_scope':event['authority_scope'],'identity_authenticated':False,'company_approved':False,'permission_granted':False}
write('R6_부분원문대조.json',reply_check)
final_raw=source.read_bytes(); final_blocker=backup.read_bytes(); proposal_raw=(out/'디자인적용_미반영수정안_v0.1.1.json').read_bytes()
assert final_raw==raw and final_blocker==blocker
question={'status':'제안만; 미접수·미회신','target':{'application_id':original['application_id'],'current_version':original['version'],'current_sha256':sha(raw),'proposed_version':proposal['version'],'proposed_sha256':sha(proposal_raw),'proposal_applied':False},'question':'실제 시안 검수에 필요한 화면·출력 조건·선택 근거를 확보한 후 어느 범위부터 판단할까요?','options':[{'key':'A','label':'자료를 확보한 뒤 해당 판본별 검수','recommended':True},{'key':'B','label':'관측색 역할 적합성만 우선 부분 검수','recommended':False},{'key':'C','label':'출력 배경·크기 조건부터 확정','recommended':False},{'key':'D','label':'확인 가능한 자료가 없어 기권·대기 유지','recommended':False}],'reason':'CI 최신성 회신은 새 시안/회사승인·R7 품질검수 답변이 아니며 선택자도 합성 역할이다.'}
write('사람판단_제안.json',question)
report={'status':'not_applied_backup_path_conflict','db_root':str(db),'data_scope':'spec_example','source':{'path':str(source),'application_id':original['application_id'],'version':original['version'],'sha256':sha(raw)},'actual_after':{'version':strict(final_raw)['version'],'sha256':sha(final_raw),'byte_unchanged':final_raw==raw},'proposal':{'path':str(out/'디자인적용_미반영수정안_v0.1.1.json'),'version':proposal['version'],'sha256':sha(proposal_raw),'applied':False,'changed_fields':['purpose','version'],'other_values_and_selection_review_statuses_preserved':True},'backup':{'path':str(backup),'existing_type':'regular_file','size_bytes':len(blocker),'sha256_before':sha(blocker),'sha256_after':sha(final_blocker),'existing_file_preserved':True,'creation_attempt':'Path.mkdir(exist_ok=False)','error':backup_error,'byte_matching_backup_created':False,'alternate_location_used':False},'checks':checks,'R6':{'partial_evidence_check':'R6_부분원문대조.json','full_current_context_validated':False,'reason':'수행사본에서 full 자료 생략; 고정목록 재작성/운영 D 이동하지 않음','latest_material_scope':'8회사 제공 CI 최신성에 관한 원문 진술 및 산하 AI 원본 부재','not_carried_over':['새 시안 승인','R7 품질검수 통과','회사/사용권한 승인','실제 디자이너 선택 인증']},'R7':{'status':'not_run_full_sources_omitted','read_rules':True,'actual_content_reviewed':False,'waiting_preserved':True},'rollback':{'needed':False,'performed':False,'reason':'원초안에 쓰지 않아 복구 불필요'},'actual_modified_input_files':[],'unresolved':['지정 backup 경로가 기존 일반 파일이므로 폴더로 사용 불가','수정안은 미반영','R6/R7 full 현재문맥 및 실제 품질 미검사','출력 크기/배경·실제 사람 선택 및 내용 검수 대기'],'company_approved':False,'operational_release':False,'actual_video_analyzed':False,'human_response_created':False,'elapsed_time':None,'token_usage':None}
write('검사결과.json',report)
summary='지정 백업 경로는 기존 일반 파일이어서 폴더 생성이 FileExistsError로 실패했습니다. 기존 파일과 원초안은 바이트 그대로 보존했고 우회 백업은 만들지 않았습니다. purpose와 자체 version(0.1.0→0.1.1)만 바꾼 미반영 수정안을 별도 저장했습니다. 다른 값·합성 선택·pending·company_approved=false·operational_release=false는 유지했습니다.\n\nR5 원초안·수정안의 실제 구조/참조 검사와 읽기 전용 판본대조를 실행했습니다. 각 종료코드와 원시 stdout/stderr는 검사결과.json에 연결했습니다. CI 최신성 원문과 대장의 부분 확인 범위를 대조했으며 새 시안 승인·회사 승인·R7 통과로 옮기지 않았습니다. full R6/R7 검증은 자료 생략 때문에 미실시입니다. 사람 질문은 최소 4선택지와 추천안을 결과에 제안만 했으며 접수나 회신을 만들지 않았습니다.\n'
(out/'결과설명.md').write_text(summary,encoding='utf-8')
transcript='''# 실제 수행 기록

- own task.txt, 수행사본_범위.json, 입력메모, 지정 SKILL.md 및 3개 참조, 보존/판본 계약, R5 회사CI 연결규칙, R6 연결안내, R7 연결규칙을 읽음. own inputs 파일명 목록만 열거했으며 미디어 해석은 수행하지 않음. 파일목록 및 긴 코드/대장 출력 일부는 도구 출력이 절단됨. 이후 작업에 필요한 원문은 별도 읽고 Python으로 실제 JSON을 파싱함.
- 지정 스킬을 적용함. 실제 D 데이터는 읽지 않고 task가 지정한 Python 런타임만 -B -X utf8로 실행. 글로벌 설정·웹·API·AE·CU·외부 앱·타 agent·질문 도구를 사용하지 않음.
- PowerShell 읽기 호출에서 `Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.` 초기화 경고가 반복 출력됐지만 요청 파일 읽기 결과가 반환됨. 잘못 입력한 선택 경로(사람答변원문)는 존재 여부 확인에서 읽지 않았고 올바른 사람답변원문 경로를 후속 명령으로 읽음.
- 원초안과 백업 충돌 파일의 실제 bytes/SHA를 읽어 보존 식별값을 기록. backup/사용자지정백업은 89바이트 일반 파일이며 기존 보존 안내문이 들어 있음. 연결점 경계와 실제 경로를 확인하고 Path.mkdir(exist_ok=False)를 실제 시도해 실패를 기록함. 기존 파일 삭제·이름변경·대체·다른 backup 위치 사용 없음.
- 대상 변경 전 byte 일치 backup을 만들 수 없어 대상 저장을 중단. 원초안은 0.1.0 그대로이며 purpose/version만 바꾼 0.1.1 후보는 outputs에 미반영 수정안으로 저장. 후보는 backup이나 활성 초안이 아님. 전후 JSON diff의 변경 필드는 정확히 purpose/version이며 나머지 값과 선택·검수 상태 동일함.
- 아래 실제 검사 명령/종료코드/원시 stdout/stderr를 출력 파일로 보존. R5 검사기는 own inputs/Phase00을 BASE로 쓰고 R1 자산검사를 호출해 등록 파일 참조/해시를 확인하며 미디어를 해석하지 않음. 판본대조는 backup이 없으므로 변경하지 않은 실제 원초안과 미반영 후보를 직접 비교한 좁은 검사임. 저장 완료 검증이나 backup 검증으로 보고하지 않음.
'''
for x in checks:transcript+='\n  - '+x['name']+': `'+subprocess.list2cmdline(x['command'])+'` 종료 '+str(x['exit_code'])+'; stdout='+x['stdout']+', stderr='+x['stderr']+'\n'
transcript+='\n- 원문 회신은 제공 8회사 CI 최신성 및 산하 AI 원본 부재 진술임. 대장의 reply pin SHA·원문·대상 버전을 실제 대조함. 원문 질문과 대장의 질문은 문구가 달라 문자열 동일로 표시하지 않으며, 질문 대상과 범위/제외 범위를 읽어 대조함. full R6 현재문맥·사람 신원·회사 직무 권한 인증은 하지 않음. R7은 제공 운영 규칙만 읽고 full 기반/실제 품질 검사는 하지 않음. 누락을 채우거나 manifest를 재작성하지 않음.\n- 입력메모는 참고 의견이며 실제 사용자 결정/새 회신이 아님. 이름을 추가하거나 통과·승인으로 기록하지 않았고 R7/검수 대기를 유지함. 필요한 판단은 outputs/사람판단_제안.json에 A–D 및 추천안으로 제안만 함.\n- 최종 원초안 bytes와 기존 충돌 파일 bytes가 최초와 동일함을 assert로 확인. 대상 쓰기·부분 저장·복구는 없고 복구할 대상도 없음. 출력 후보는 미반영으로 표시함. 수집하지 않은 수행시간/token은 null이며 시각을 만들지 않음.\n- 생성 산출물: outputs의 실행 스크립트, 미반영 수정안, diff, 3종 검사 stdout/stderr, R6 부분대조, 사람판단 제안, 검사결과, 결과설명 및 이 transcript.md.\n'
(run/'transcript.md').write_text(transcript,encoding='utf-8')
print(json.dumps({'status':report['status'],'backup_error':backup_error,'checks':[{k:x[k] for k in ['name','exit_code']} for x in checks],'input_unchanged':final_raw==raw,'outputs':str(out)},ensure_ascii=False))
