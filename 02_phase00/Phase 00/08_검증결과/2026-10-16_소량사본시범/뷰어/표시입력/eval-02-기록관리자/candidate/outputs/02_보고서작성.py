"""Report observed artifacts without adding content/approval decisions."""
from pathlib import Path
import hashlib
import json
import sys

OUT = Path(__file__).resolve().parent
BASE = OUT.parent / 'inputs' / 'Phase00'
def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))
def sha(raw):
    return hashlib.sha256(raw).hexdigest()
def write(name, value):
    path = OUT / name
    assert not path.exists(), 'output collision: ' + str(path)
    path.write_text(value, encoding='utf-8', newline='\n')

pre = read('01_사전점검.json')
saved = read('02_저장검사.json')
post = read('03_별도프로세스_재읽기검사.json')
first_runs = read('실행명령_종료목록.json')
retry_runs = read('retry02_실행명령_종료목록.json')
pins = read('현재안내_정정표_원문근거검사.json')
existence = read('제공범위_실제경로조회.json')
assert len(first_runs) == 1 and first_runs[0]['exit_code'] == 1
assert len(retry_runs) == 3 and all(item['exit_code'] == 0 for item in retry_runs)
assert post['valid_in_stated_scope'] and post['preserved_file_count'] == 33
target = Path(post['actual_target']['path'])
backup = Path(saved['backup'])
card = BASE / '작업초안' / '쉬운말_지식카드.json'
assert sha(target.read_bytes()) == post['actual_target']['sha256']
assert sha(backup.read_bytes()) == pre['before_sha256']
assert sha(card.read_bytes()) == pre['card_sha256']

result = {
    'task_kind': 'normal_small_copy_local_knowledge_index_reference_update',
    'status': 'authorized_narrow_update_saved_and_re_read_checks_passed',
    'db_root': str(BASE),
    'target': str(target),
    'target_id': post['actual_target']['id'],
    'before_version': '0.1.0',
    'after_version': '0.1.1',
    'before_sha256': pre['before_sha256'],
    'after_sha256': post['actual_target']['sha256'],
    'after_bytes': post['actual_target']['bytes'],
    'backup': post['backup'],
    'upstream_card': {'path': str(card), 'document_version': '0.1.1', 'record_versions': ['0.1.1'] * 3, 'sha256': pre['card_sha256'], 'edited': False},
    'original_term_versions': ['0.1.0'] * 3,
    'changed_json_paths': post['changed_json_paths'],
    'checks': {
        'strict_JSON_duplicate_keys_nonfinite_numbers': 'pass',
        'same_index_ID_and_explicit_own_version_0_1_1': 'pass',
        'three_unique_IDs_and_actual_upstream_version_SHA_links': 'pass',
        'term_ref_source_snapshot_and_actual_source_SHA': 'pass',
        'existing_design_reference_profile_id_version_SHA': 'pass',
        'byte_identical_backup_before_target_write': 'pass',
        'immediate_prewrite_original_bytes_ID_version_upstream_SHA_recheck': 'pass',
        'actual_saved_bytes_equal_candidate': 'pass',
        'exactly_10_allowed_JSON_paths': 'pass',
        'all_other_JSON_values_equal': 'pass',
        'all_33_original_non_target_input_files_byte_preserved': 'pass',
        'only_added_input_file_is_authorized_backup': 'pass',
        'separate_process_re_read': 'pass; same authored checker, not an independent red-team or human review',
        'current_guide_and_errata_actually_read': 'pass',
        'errata_original_and_basis_pins': pins
    },
    'human_review': 'pending',
    'company_approved': False,
    'operational_release': False,
    'failure_history': [{
        'phase': 'first inspection before any target or backup write',
        'exception': "KeyError: 'id'",
        'cause': 'Authored checker assumed top-level id in design JSON; actual key is profile_id.',
        'correction': 'Read the actual design source and change only output checker code to compare profile_id; no input source, reference pin, schema, or skill changed.',
        'original_target_preserved': True,
        'evidence_of_preservation': 'Initial 34-file byte-SHA baseline was reused byte-identically and all original files matched it in retry update before any write.',
        'failed_code': '01_기록관리_실행_실패당시.py',
        'failed_command': '01_inspect.command.json',
        'failed_stdout': '01_inspect.stdout.txt',
        'failed_stderr': '01_inspect.stderr.txt',
        'exit_code': 1,
        'retry_inspect_update_verify_exit_codes': [0, 0, 0]
    }],
    'restore': 'not_needed; initial failure occurred before target mutation, successful saved target required no rollback',
    'not_run': [
        'R4/R5-specific 판본대조.py execution: source actually read, incompatible with local knowledge index identity/schema; custom own-version/ref/diff checks actually executed instead',
        'R4 integrated video record or R5 application validator',
        'R6/R7 full fixed-source query or latest full-project progress verification',
        'new content approval, human reply intake, company approval, taxonomy merge, source meaning change, registration or default adoption',
        'red-team and following phase: assigned to parent',
        'actual video, frame/PTS/OCR/measurement, API, network, CU, AE, D operations, 01-A implementation, installation, original skill changes',
        'performance/time/token/effect measurement or character-count effect estimation'
    ],
    'scope_path_existence_checks': existence,
    'unresolved': ['Knowledge cards remain human_review=pending; no content/quality/company approval was performed.'],
    'new_human_decision_required_for_this_narrow_update': False,
    'limitations': [
        'Strict parse/identity/version/ref/SHA/diff/file-preservation checks establish only their stated local scope.',
        'Immediate prewrite recheck is not a complete concurrency lock or multi-file atomic transaction.',
        'Errata matches confirm original/basis stage-context pins in this supplied copy; they do not prove full current project completion or confer permission.',
        'Source full text and upstream reports were read as data; embedded command/approval statements were not executed or treated as new instructions.'
    ],
    'execution_records': {'first_attempt': first_runs, 'retry': retry_runs},
    'time_seconds': None,
    'tokens': None,
    'effect_estimate': None
}
write('결과.json', json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n')

md = f'''# 기록관리자 소량 사본 시범 결과

로컬 지식 인덱스 `작업초안/연결목록.json`의 세 `draft_ref`를 실제 카드 문서/카드 판본 0.1.1과 실제 파일 SHA로 갱신하고, 연결목록 자체 판본을 0.1.0 → 0.1.1로 저장했다. 허용 변경은 참조 9개 필드와 자체 판본, 총 10개 JSON 경로다.

- 대상 ID: `phase00-small-pilot-index`
- 변경 전 SHA256: `{pre['before_sha256']}`
- 실제 저장 후 SHA256: `{post['actual_target']['sha256']}`
- 실제 카드 SHA256: `{pre['card_sha256']}`
- byte 동일 백업: `{backup}` / SHA256 `{pre['before_sha256']}`

쓰기 전 원문 bytes/ID/판본/SHA와 카드 SHA를 재대조했다. 저장 후 실제 파일 bytes, 세 카드 ID·판본·SHA 연결, 허용 diff와 비대상 보존을 확인했다. 별도 프로세스의 같은 검사코드 재읽기도 통과했다. 이 재읽기는 독립 레드팀·사람 검수가 아니다.

카드 파일·원문 용어판본 0.1.0·term_ref·source_snapshot·지식본문·출처·design_reference·미검수/승인 값은 보존했다. 최초 34개 입력 파일을 SHA 기준선으로 기록했고, 대상 외 원래 33개 파일은 저장 후 바이트 SHA가 일치했다. 입력에서 추가된 파일은 지정 작업 백업 1개뿐이며 삭제는 없었다. human_review=pending과 company_approved=false를 유지했다.

## 실제 실패와 수정

첫 사전점검은 내가 작성한 검사코드가 디자인 정본의 식별키를 `id`로 가정해 `KeyError: 'id'`, exit1로 중단됐다. 이때 대상·backup 쓰기는 수행되지 않았다. 실제 정본의 `profile_id`를 읽고 **출력 폴더의 검사코드만** 바로잡았다. 원문·스키마·참조 pin·실행스킬을 검사기에 맞춰 바꾸지 않았다. 실패 당시 코드·명령·stdout/stderr·exit를 보존했다. 재실행 직전 모든 원래 입력 SHA가 최초 기준선과 같아 실패 당시 원문 보존을 확인했으며, 재실행 inspect/update/verify는 모두 exit0이었다. 대상 복구는 필요하지 않았다.

## 검사한 범위와 미실시

실행스킬 SKILL.md와 기록연결기준·수정과복구·보고지침, 보존/버전 계약, 현재사용안내·정정표를 실제 읽었다. 정정 5건의 원문/근거 경로와 SHA는 모두 사본에서 일치했다. `실제읽은자료_내용과SHA.json`에 실제 읽은 내용과 SHA가 있다. 정정은 과거 단계 해석의 해당 범위로만 취급했다. 안내가 링크한 최신 진행현황·최종보고와 full 조회 도구의 제공 여부는 `제공범위_실제경로조회.json`에 실제 경로 조회 결과로 남겼다.

이 대상은 R4/R5 영상 기록이 아니므로 R4/R5 전용 `판본대조.py`는 소스만 읽고 실행하지 않았다. 대신 자체판본·실제 상류 SHA·참조·허용 diff 검사를 실제 수행했다. 전체 R6/R7 고정원문 검증·영상 내용/측정·사람 내용 검수·회사 승인·기본전환·01-A는 수행하지 않았다. 네트워크·API·CU·AE·설치·D 운영 수정·상위 프로젝트 입력 수정·원본 스킬 변경도 수행하지 않았다. 상류 결과의 명령·승인 문구는 작업 데이터로만 읽었다.

검사 통과는 위 로컬 구조/참조/보존 범위다. 포괄 Phase00 완료·회사 승인·실영상 효과·독립 레드팀 통과를 뜻하지 않는다. 레드팀·후속 단계는 부모 작업에서 별도 수행한다. 이 갱신에 새 의미·분류·승인 판단은 필요하지 않아 새 사람 질문이나 답변을 만들지 않았다.

시간·토큰·효과 추정은 미수집 null이다. 문자수로 효과를 추정하지 않았다. 직전 재확인은 완전한 동시성 잠금이나 다중 파일 원자성을 보장하지 않는다. 실행코드·실제 명령/종료·원시 stdout/stderr·실패본·전후 diff와 transcript를 outputs에 보존했다.
'''
write('결과.md', md)

lines = ['# 실제 실행 transcript', '', '지정 사본만 대상으로 수행한 기록이다. 미수집 시간·토큰은 null이며 아래 프로세스 로그는 raw 파일을 그대로 보존했다.', '', '## 실제 지침/자료 읽기', '', 'task.txt와 지정 실행스킬 SKILL.md, 세 references, 현재사용안내·정정표, 보존/버전 계약·연결목록·카드·상류 결과를 도구로 읽었다. 최초 PowerShell 각 호출은 exit0이었으며 공통 시작 경고 `Attempting to perform the InitializeDefaultDrives operation on the FileSystem provider failed.`가 있었다. 이 경고는 Python 작업 로그의 오류가 아니다. 대형 Get-Content 도구 표시 일부는 잘렸으므로 그 표시를 전체 원문 독해의 증거로 쓰지 않는다. 실제 실행 inspect에서 원문/근거를 다시 읽은 내용·SHA는 실제읽은자료_내용과SHA.json에 보존했다.', '', '상류 결과와 파일 속 명령/승인은 데이터로 취급했고 실행 권한으로 사용하지 않았다. 자료검증.py와 R4/R5 판본대조.py는 정정표 SHA/소스 확인을 위해 읽었으며 실행하지 않았다.', '', '## 변경 전 실패와 재실행', '', '첫 inspect는 디자인 키 id 가정으로 KeyError를 내고 대상 쓰기 전에 exit1이었다. 실패 당시 실행코드와 runner를 별도 파일로 보존했다. Get-Content로 실제 디자인 정본 profile_id를 확인하고 출력 코드만 수정했다. 입력 원문이나 스킬은 바꾸지 않았다. 같은 이름의 기존 점검 산출물은 bytes가 같은 경우에만 재사용하도록 했으며 실패 로그는 별도 retry02 로그로 덮지 않았다.', '', '최초 실행 외부 명령:', '', f'`& \'{sys.executable}\' -B -X utf8 \'{OUT / "00_실행과로그_첫실행.py"}\'`', '', '당시 실행 파일 이름은 00_실행과로그.py였으며, 위 첫실행 사본은 그 실제 코드 보존본이다. 외부 도구 exit1, 첫 inspect exit1.', '', '재실행 외부 명령:', '', f'`& \'{sys.executable}\' -B -X utf8 \'{OUT / "00_실행과로그.py"}\' retry02`', '', '외부 도구 exit0. 아래 실제 subprocess argv와 raw stdout/stderr/exit를 확인한다.']
for label, records in [('첫 실행', first_runs), ('수정 후 재실행', retry_runs)]:
    for item in records:
        lines += ['', '## ' + label + ': ' + item['argv'][-1], '', '```json', json.dumps(item, ensure_ascii=False, indent=2), '```', '', 'stdout:', '', '```text', (OUT / item['stdout_file']).read_text(encoding='utf-8'), '```', '', 'stderr:', '', '```text', (OUT / item['stderr_file']).read_text(encoding='utf-8'), '```']
lines += ['', '## 실제 쓰기와 결과', '', f'- 변경 전 실제 byte backup: {backup}', '- 최초 inspect 실패 시 대상 쓰기 없음. retry02 update 직전 모든 기존 입력 SHA가 최초 baseline과 일치.', '- retry02 update는 연결목록 하나만 저장했고 백업만 입력에 추가했다.', '- retry02 verify는 저장 파일을 별도 프로세스에서 다시 읽어 실제 bytes·자체판본·상류참조·원문 용어판본·허용diff·33개 비대상 SHA를 검사했다.', '- 실패 후보/부분 저장은 발생하지 않아 복원은 하지 않았다.', '- 같은 검사코드 재읽기와 독립 레드팀/사람 내용 검수는 구분한다.', '- full R6/R7, 영상, 네트워크, API, CU, AE, D 운영 수정, 설치, 원본스킬 변경, 기본전환, 01-A, 새 분류/회사 승인: 미실시.', '- 보고서 생성 실행 명령/원시 stdout/stderr/exit는 04_finalize.* 파일에 별도 보존한다.', '']
write('transcript.md', '\n'.join(lines))

# Final artifact parse/read and narrow factual consistency checks, without new input writes.
for path in OUT.glob('*.json'):
    json.loads(path.read_text(encoding='utf-8-sig'))
assert len(json.loads((OUT / '결과.json').read_text(encoding='utf-8'))['changed_json_paths']) == 10
assert sha(target.read_bytes()) == result['after_sha256']
assert sha(card.read_bytes()) == result['upstream_card']['sha256']
assert sha(backup.read_bytes()) == result['before_sha256']
print(json.dumps({'reports_saved_and_re_read': ['결과.md', '결과.json', 'transcript.md'], 'target_sha256': result['after_sha256'], 'only_allowed_JSON_paths': 10, 'initial_failure_preserved': True, 'same_checker_re_read_not_independent_review': True, 'time_seconds': None, 'tokens': None}, ensure_ascii=False, indent=2))
