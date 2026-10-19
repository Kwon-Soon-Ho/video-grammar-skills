from pathlib import Path
import json,hashlib,subprocess,sys,uuid,os
from datetime import datetime,timezone
run=Path(__file__).resolve().parents[1]
base=run/'inputs/Phase00'
out=run/'outputs'
log=run/'transcript.md'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def note(s):
 with log.open('a',encoding='utf-8') as f:f.write(s+'\n')
log.write_text('# 실제 수행 기록\n\n사용 스킬: inputs/Phase00/실행스킬/video-record-steward/SKILL.md 및 references/작업기준.md.\n범위: own run의 합성 사본. 복구 대상 초안만 변경. 구형 자료는 읽기 검사만 수행.\n시간/token 추정값은 기록하지 않음.\n\n초기 PowerShell 파일 읽기에서 InitializeDefaultDrives 경고가 표시됐으나 명령 종료코드는 0이고 요청 파일 내용이 반환됨. 파일 목록 출력은 길어 일부 잘렸으며 필요한 파일은 개별 재조회함.\n',encoding='utf-8')
before={p.relative_to(base).as_posix():sha(p.read_bytes()) for p in base.rglob('*') if p.is_file()}
write(out/'입력_검사전_해시.json',before)
req=json.loads((base/'복구요청.json').read_text(encoding='utf-8-sig'))
def scoped(rel):
 p=(base/rel).resolve()
 assert p.is_relative_to(base.resolve()),'범위 밖 경로'
 return p
target=scoped(req['target_path']);checkpoint=scoped(req['checkpoint_path']);legacy=base/'작업초안/구형_추가자료.json'
assert req['target_path']=='12_통합기록/통합기록_작업초안.json'
failed=target.read_bytes();normal=checkpoint.read_bytes();legacy_raw=legacy.read_bytes()
checks={'failed_current_expected':req['failed_current_sha256'],'failed_current_actual':sha(failed),'checkpoint_expected':req['checkpoint_sha256'],'checkpoint_actual':sha(normal)}
write(out/'복구전_확인.json',checks)
assert sha(failed)==req['failed_current_sha256'],'현재 파일 hash 불일치: 복구 중단'
assert sha(normal)==req['checkpoint_sha256'],'체크포인트 hash 불일치: 복구 중단'
note('\n지정 대상/체크포인트의 실제 SHA256이 복구요청과 모두 일치함.\n'+json.dumps(checks,ensure_ascii=False,indent=2))
validator=base/'07_실행도구/자료검증.py'
def validate(label,path):
 cmd=[sys.executable,'-B','-X','utf8',str(validator),'--record',str(path)]
 p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',cwd=base)
 (out/(label+'_stdout.txt')).write_text(p.stdout,encoding='utf-8');(out/(label+'_stderr.txt')).write_text(p.stderr,encoding='utf-8')
 try:result=json.loads(p.stdout)
 except Exception:result={'valid':False,'status':'tool_execution_failed','stderr':p.stderr}
 write(out/(label+'.json'),{'command':cmd,'exit_code':p.returncode,'result':result})
 note('\n실행: '+json.dumps(cmd,ensure_ascii=False)+'\n종료코드: '+str(p.returncode)+'\nstdout/stderr: outputs/'+label+'_stdout.txt, '+label+'_stderr.txt\n'+json.dumps(result,ensure_ascii=False,indent=2))
 return p.returncode,result
pre_code,pre=validate('복구전_초안검사',target)
folder=base/'backup'/('복구_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True,exist_ok=False)
backup=folder/'실패한_통합기록_작업초안.json'
with backup.open('xb') as f:f.write(failed)
assert backup.read_bytes()==failed and sha(backup.read_bytes())==sha(failed)
note('\n현재 실패 파일을 '+backup.relative_to(base).as_posix()+' 에 배타 생성하여 보존했고 바이트/hash 일치를 재확인함. 기존 backup은 덮어쓰지 않음.')
assert target.read_bytes()==failed,'작업 중 대상 변경'
assert checkpoint.read_bytes()==normal,'작업 중 체크포인트 변경'
tmp=target.with_name(target.name+'.restore-'+uuid.uuid4().hex+'.tmp')
with tmp.open('xb') as f:f.write(normal);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==normal
os.replace(tmp,target)
restored=target.read_bytes()
assert restored==normal and sha(restored)==req['checkpoint_sha256']
note('\n정상 체크포인트의 바이트를 임시 파일에 기록·확인한 뒤 지정 초안에 교체. JSON 재직렬화/필드 수정/버전 증가 없음. 복구 후 바이트와 SHA256 일치 확인.')
post_code,post=validate('복구후_초안검사',target)
legacy_code,legacy_result=validate('구형_추가자료_읽기검사',legacy)
after={p.relative_to(base).as_posix():sha(p.read_bytes()) for p in base.rglob('*') if p.is_file()}
changed=[k for k in before if after.get(k)!=before[k]]
added=[k for k in after if k not in before]
assert changed==[req['target_path']],changed
assert added==[backup.relative_to(base).as_posix()],added
assert legacy.read_bytes()==legacy_raw
preservation={'changed_existing_paths':changed,'added_paths':added,'existing_non_target_files_unchanged':all(after.get(k)==v for k,v in before.items() if k!=req['target_path']),'legacy_bytes_unchanged':legacy.read_bytes()==legacy_raw,'existing_backup_unchanged':all(after.get(k)==v for k,v in before.items() if k.startswith('backup/'))}
write(out/'보존_검증.json',preservation)
result={'recovery_status':'restored_exact_checkpoint','target_path':req['target_path'],'expected_sha256':req['checkpoint_sha256'],'actual_sha256':sha(restored),'byte_equal_to_checkpoint':restored==normal,'restored_byte_length':len(restored),'failed_current_backup_path':backup.relative_to(base).as_posix(),'failed_current_backup_sha256':sha(backup.read_bytes()),'preservation':preservation,'restored_structure_check':{'exit_code':post_code,'result_file':'복구후_초안검사.json','status':post.get('status'),'valid':post.get('valid')},'legacy_inspection':{'exit_code':legacy_code,'status':legacy_result.get('status'),'valid':legacy_result.get('valid'),'result_file':'구형_추가자료_읽기검사.json','intake_performed':False,'migration_performed':False,'modified':False},'limits':['R6/R7 전체 연결/운영 검증 미수행','합성 자료이며 실제 영상 관측·사람 신원·회사 승인·운영 반영 확인 아님'],'fact_verified':False,'company_approved':False,'operational_release':False}
write(out/'검사결과.json',result)
(out/'결과설명.md').write_text('지정 정상 체크포인트의 SHA256을 확인하고 통합기록_작업초안.json을 바이트 그대로 복구했습니다. 실패 파일은 새 backup 폴더에 보존했고, 기존 백업 및 다른 입력 파일은 hash 불변을 확인했습니다.\n\n복구 후 구조 검사 상태: '+str(post.get('status'))+' (종료코드 '+str(post_code)+'). 남은 미정/검수 항목은 복구후_초안검사.json을 참조하세요.\n\n구형 추가자료는 읽기 검사 결과 '+str(legacy_result.get('status'))+'이며 현재 통합 규격 통과 자료가 아닙니다. 원본 영상 version·hash·재생 길이, 새 시간 계약, 4단위 대상·버전, 근거 역할/범위, 태그 범위, 실제 run, 새 검수 context 연결이 부족합니다. 실제 원본은 없으므로 값을 추정하지 않았습니다. 접수·이관·수정은 수행하지 않았습니다.\n\n합성 범위의 구조/참조 검사이며 실제 영상·회사 승인·R6/R7 전체 검증은 확인하지 않았습니다.\n',encoding='utf-8')
note('\n최종 보존 검증:\n'+json.dumps(preservation,ensure_ascii=False,indent=2)+'\n최종 결과: outputs/검사결과.json. 모든 assert 통과. 구형 접수/이관 도구 main 및 receive는 호출하지 않음. 외부앱/미디어해석/웹/실제 DB 접근 없음.')
print(json.dumps(result,ensure_ascii=False,indent=2))
