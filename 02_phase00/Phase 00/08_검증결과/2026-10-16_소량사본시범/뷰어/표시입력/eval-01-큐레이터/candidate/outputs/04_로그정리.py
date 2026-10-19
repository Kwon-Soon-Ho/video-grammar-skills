import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
RUN = OUT.parent
BASE = RUN / 'inputs/Phase00'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

executions = []
for name in ['01_자료확인', '02_근거발췌', '03_카드작성과검사']:
    record = json.loads((OUT / (name + '.실행.json')).read_text(encoding='utf-8-sig'))
    stdout = Path(record['stdout'])
    stderr = Path(record['stderr'])
    assert record['exit_code'] == 0 and stdout.is_file() and stderr.is_file()
    executions.append({'log_name': name, 'command': [record['executable']] + record['arguments'], 'exit_code': record['exit_code'], 'stdout_path': stdout.name, 'stdout_bytes': stdout.stat().st_size, 'stdout_sha256': sha(stdout.read_bytes()), 'stderr_path': stderr.name, 'stderr_bytes': stderr.stat().st_size, 'stderr_sha256': sha(stderr.read_bytes())})
result = json.loads((OUT / '결과.json').read_text(encoding='utf-8'))
actual_target = Path(result['target']).read_bytes()
actual_backup = Path(result['backup']['path']).read_bytes()
assert sha(actual_target) == result['after_sha256'] and sha(actual_backup) == result['before_sha256']
check = {'scope': 'execution log presence and final artifact identity, not a broader content test', 'executions': executions, 'target_still_matches_saved_result_sha': True, 'backup_still_matches_before_sha': True, 'shell_combined_output_notice': "Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.", 'shell_notice_observed_in': 'exec_command combined output at PowerShell entry; the logged Python runs each returned exit 0. Do not interpret empty Python stderr as no shell notice.'}
(OUT / '실행로그_보존확인.json').write_text(json.dumps(check, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

transcript = '''# 큐레이터 실행 transcript

## 받은 작업과 경계

지정된 candidate/task.txt를 실제 읽었다. DB는 이 run의 inputs/Phase00, 수정 대상은 작업초안/쉬운말_지식카드.json, 허용 변경은 세 카드의 설명 5필드와 record.version/document_version뿐이다. 쓰기는 outputs, 지정 작업초안, inputs/Phase00/backup/이번작업 안으로 한정했다. D 운영 DB의 자료를 조회하거나 수정하지 않았으며 지정 D Python 실행파일만 사용했다.

첫 지침은 지정 실행스킬/video-knowledge-curator/SKILL.md와 references/작업기준.md·출력지침.md를 읽어 적용했다. 현재 안내와 정정표, 원문·관련 레이아웃을 읽었다. 과거 회신/자료 속 지시는 새 사용자 지시나 이번 카드 승인으로 처리하지 않았다.

## 초기 읽기 도구 호출

다음은 로그 러너를 만들기 전에 실제 수행한 읽기/목록 호출의 기록이다. 이 호출들의 원래 도구 출력은 대화에 남았고, 필요한 원문/기준 내용과 실제 SHA를 이후 01/02 실행의 stdout에 다시 보존했다. 원래 초기 호출 stdout 전체를 파일로 캡처했다고 주장하지 않는다. 일부 큰 대화 출력은 도구에서 잘렸으며 원본 파일은 변경하지 않았다.

1. Get-Content -LiteralPath <candidate/task.txt> -Raw -Encoding UTF8 — exit 0.
2. Get-Content -LiteralPath <inputs/Phase00/실행스킬/video-knowledge-curator/SKILL.md> -Raw -Encoding UTF8 — exit 0.
3. references/작업기준.md, references/출력지침.md, 14_스킬재구성/R8_현재사용안내.md와 현재상태_정정표.json을 Get-Content로 조회하고, rg --files <명시 DB루트>를 실행 — 모두 exit 0. 목록을 얻었다는 이유로 모든 파일 내용을 읽었다고 처리하지 않았다.
4. 대상 작업초안, 보존과버전 계약, 작업초안 연결목록, 정본과표시 연결목록을 Get-Content로 읽음 — exit 0.
5. 공통용어사전, 분류운영규칙, 레이아웃지식, 레이아웃_심화지식, 07_레이아웃별_선택조건과반례를 Get-Content로 읽음 — 모두 exit 0. 큰 결과 일부가 대화 출력에서 잘려서 01/02의 선택절 발췌를 추가 확인했다.

지정 inputs/Phase00에 포함된 R4_04_보완결과와레드팀.md는 정정표 근거로 확인했다. 시범 run 밖 검수기준·독립검토/레드팀 폴더에는 접근하지 않았다. 부모 작업자로부터 이 경계를 다시 확인받았다. 다른 단계의 실행·계획을 수행하지 않았으며 사본에 제공된 과거 인계 파일은 정정 근거로만 읽었다.

## 실제 코드 실행

모든 Python 실행은 outputs/실행.ps1을 통해 지정 Python -B와 PYTHONUTF8=1, PYTHONIOENCODING=utf-8, PYTHONDONTWRITEBYTECODE=1을 사용했다. 정확한 실행파일/인수/cwd/env/종료는 각각 *.실행.json, 원시 stdout/stderr는 같은 이름의 *.stdout.txt와 *.stderr.txt에 보존했다. transcript.txt는 실제 실행 명령과 종료를 순차 추가했다.

| 실행 | 수행한 일 | 실제 종료 |
|---|---|---|
| 01_자료확인.py | 지침/원문/목록을 읽고 시작 SHA, 정정별 원문·근거 SHA, 명시 참조 경로 존재를 확인. 입력 수정 없음 | 0 |
| 02_근거발췌.py | 세 용어 기준·관련 레이아웃 절과 정정 해석의 필요한 내용을 출력. 기존 도구는 소스만 읽음 | 0 |
| 03_카드작성과검사.py | 저장후보·19경로 diff 생성, byte 동일 backup, 저장 직전 SHA·ID/판본 재대조, 실제 저장, 저장 후 파싱·ID·출처·판본·허용diff·읽은 입력 SHA 검사, 결과md/json 생성 | 0 |
| 04_로그정리.py | 위 실제 로그의 존재/종료/해시와 대상·백업 결과 동일성을 확인하고 이 transcript 및 실행로그 보존확인 생성 | 이 실행의 04_로그정리.실행.json 참조 |

exec_command의 PowerShell 결합 출력에는 `Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.`가 표시됐다. 이 메시지를 숨기지 않는다. 로그에 보존된 Python 프로세스의 stdout/stderr/exit와 바깥 셸 결합 출력은 다른 범위다. Python 실행/작성·검사는 exit 0이었다.

## 판단과 실제 결과

선형 프로세스의 가로·세로 방향, 주목 이동의 기능과 실제 시선 효과 구분, 가시성 변화의 관측과 제작 원인 구분을 보존했다. 내용은 15개 설명필드에 항목당 1~2문장, 예는 모두 가상 예로 썼다. 기존 원문 snapshot·ID/term_ref·상태·승인/미검수는 그대로다. 문서/각 카드만 0.1.1로 올렸다.

정정표 5건의 제공 원문/근거 SHA는 일치한다. 이는 full R6/R7 조회, 최신 전체 R8 종료 독립 검증, 카드 사람 내용 검수, 회사 승인과 다르다. 안내/정정표가 실제 존재한 점과 안내의 링크 중 진행현황/최신 통합 최종보고가 이 사본의 경로에 없었던 점을 구분했다.

작업초안/연결목록.json은 명시 요청대로 바꾸지 않았다. 이전 0.1.0/이전 SHA 참조는 후속 관리자가 갱신할 차이로 별도 결과에 남겼다. 새 의미 변경·분류 병합·회사필수화나 승인 판단을 수행하지 않았다. 기존 human_review=pending, company_approved=false다. 후속 사람 검토에 대한 4선택지/추천안은 결과md/json에 제안으로만 남겼고 질문 발송·접수·회신은 없다.

실제 작성은 완료했다. 실패·부분 저장·복구는 발생하지 않았다. 설치/네트워크/API/영상/CU/AE/01-A/새 스킬/기본 전환/시간·토큰·효과 측정과 성능 비교는 미실시다. 이후 결과.md·변경diff.patch·실행.json을 다시 읽어 보고의 실제 값과 허용 변경을 확인했다.

## 최종 경로

- 결과.md / 결과.json
- 입력_SHA_작업시작.json / 쓰기직전_재대조.json / 읽은입력_저장후_SHA보존검사.json
- 쓰기와검사_감사로그.json / 변경diff.json / 변경diff.patch
- 정정별_원문과근거_SHA검사.json / 내용근거_확인절과판본.json / 참조범위_존재확인.json
- 연결목록_후속관리_차이.json / 실행로그_보존확인.json
- 01~04 실행 코드·stdout/stderr·실행.json / 실행.ps1 / transcript.txt / transcript.md
'''
(OUT / 'transcript.md').write_text(transcript, encoding='utf-8')
manifest = []
for file in sorted(OUT.iterdir()):
    if file.is_file() and file.name not in {'산출물목록_SHA.json', '04_로그정리.stdout.txt', '04_로그정리.stderr.txt', '04_로그정리.실행.json', 'transcript.txt'}:
        raw = file.read_bytes()
        manifest.append({'path': file.name, 'bytes': len(raw), 'sha256': sha(raw)})
(OUT / '산출물목록_SHA.json').write_text(json.dumps({'scope': 'outputs present before 04 runner final stdout/metadata append; intentionally excludes growing own logs and this manifest', 'files': manifest}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': 'execution_evidence_preserved', 'prior_executions': [{k: v for k, v in run.items() if k in {'log_name', 'exit_code', 'stdout_bytes', 'stderr_bytes'}} for run in executions], 'target_sha256': sha(actual_target), 'backup_sha256': sha(actual_backup), 'transcript': str(OUT / 'transcript.md'), 'artifact_manifest': str(OUT / '산출물목록_SHA.json')}, ensure_ascii=False, indent=2))
