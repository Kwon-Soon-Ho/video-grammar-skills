import difflib
import hashlib
import json
import os
import re
import sys
import traceback
from pathlib import Path

RUN = Path(__file__).resolve().parent.parent
BASE = RUN / 'inputs' / 'Phase00'
OUT = RUN / 'outputs'
REL = '작업초안/쉬운말_지식카드.json'
TARGET = (BASE / REL).resolve()
BACKUP = (BASE / 'backup/이번작업/큐레이터_소량시범_20261016/쉬운말_지식카드_v0.1.0.json').resolve()
FIELDS = ['plain_explanation', 'use_when', 'example', 'counterexample', 'caution']
CONTENT = [
    {
        'id': '시범카드001',
        'plain_explanation': '순서가 있는 단계를 선이나 화살표로 이어, 앞뒤 흐름을 보여 주는 화면 배치입니다.',
        'use_when': '업무나 공정에서 단계의 순서가 중요하고, 갈림길이 핵심 내용이 아닐 때 씁니다.',
        'example': '가상 예: 접수→검토→승인을 선으로 이어 보여 주고, 세로로 배치해도 단계 순서와 연결 방향을 유지합니다.',
        'counterexample': '동등한 항목을 가로로 나열했거나 연도를 축에 표시했다는 이유만으로 단계 흐름이라 부르면 오용입니다. 실제 분기나 되돌아감을 숨기고 한 줄로 잇는 것도 피합니다.',
        'caution': '가로·세로는 별도 방향 속성이며, 선의 길이가 실제 소요 시간을 뜻하지는 않습니다. 절차의 선후·분기 근거가 없으면 순서를 확정하지 않습니다.',
    },
    {
        'id': '시범카드002',
        'plain_explanation': '지금 설명하는 대상에 눈길을 돌리도록 안내하는 움직임의 역할입니다.',
        'use_when': '시간에 따라 강조가 어떻게 바뀌는지와 설명 내용을 함께 확인할 수 있고, 핵심 단계에서 설명 대상이 바뀔 때 씁니다.',
        'example': '가상 예: 절차를 설명하며 강조 테두리가 검토에서 다음 설명 대상인 승인으로 옮겨 갑니다.',
        'counterexample': '장식용 점이 움직였다는 사실만으로 주목 이동이라 부르는 것은 오용입니다.',
        'caution': '어느 대상으로 주목을 옮기는지 근거가 부족하면 후보로 남깁니다. 이런 표현이 실제 시청자의 시선을 옮겼는지는 별도 검토가 필요합니다.',
    },
    {
        'id': '시범카드003',
        'plain_explanation': '대상이 보이는 범위나 정도가 시간에 따라 달라지는 변화입니다.',
        'use_when': '같은 대상과 시간 범위를 확인하며 등장·퇴장, 가려짐·드러남의 변화를 볼 수 있을 때 씁니다.',
        'example': '가상 예: 희미하던 제목이 점차 잘 보이거나, 가려져 있던 글자가 드러납니다.',
        'counterexample': '글자가 드러났다는 이유만으로 불투명도 설정을 바꿨다고 단정하는 것은 오용입니다.',
        'caution': '불투명도 설정, 마스크(가림 영역), 합성, 배경 변화 중 무엇이 원인인지는 원본 근거 없이는 확정하지 않습니다. 변화가 충분히 보이면 가시성 변화는 기록하되 원인만 미확정으로 남깁니다.',
    },
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save_json(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result

def parse(raw):
    return json.loads(raw.decode('utf-8-sig'), object_pairs_hook=no_duplicate_keys)

def signature(doc):
    return {'id': doc['id'], 'document_version': doc['document_version'], 'records': [{'id': r['id'], 'version': r['version'], 'term_ref': r['term_ref']} for r in doc['records']]}

def diff(a, b, path=''):
    if type(a) is not type(b):
        return [{'path': path, 'before': a, 'after': b}]
    if isinstance(a, dict):
        changes = []
        for key in sorted(a.keys() | b.keys()):
            at = path + '/' + key
            if key not in a or key not in b:
                changes.append({'path': at, 'before': a.get(key), 'after': b.get(key), 'key_set_changed': True})
            else:
                changes.extend(diff(a[key], b[key], at))
        return changes
    if isinstance(a, list):
        if len(a) != len(b):
            return [{'path': path, 'before': a, 'after': b, 'array_length_changed': True}]
        return [change for i, (x, y) in enumerate(zip(a, b)) for change in diff(x, y, path + '/' + str(i))]
    return [] if a == b else [{'path': path, 'before': a, 'after': b}]

audit = {'scope': 'three illustrative knowledge cards; bounded direct checks, not R4/R6/R7 full validation or human/company approval', 'events': [], 'status': 'started', 'restore': 'not_needed'}
before_raw = None
candidate_raw = None
write_complete = False
try:
    assert TARGET.is_relative_to(BASE.resolve()) and BACKUP.is_relative_to((BASE / 'backup/이번작업').resolve())
    manifest = json.loads((OUT / '입력_SHA_작업시작.json').read_text(encoding='utf-8'))
    before_raw = TARGET.read_bytes()
    before_sha = sha(before_raw)
    assert before_sha == manifest[REL]['sha256'], 'target changed since inspection snapshot; hold'
    before = parse(before_raw)
    assert before['document_version'] == '0.1.0'
    assert len(before['records']) == 3
    assert [r['id'] for r in before['records']] == [r['id'] for r in CONTENT]
    assert all(r['version'] == '0.1.0' for r in before['records'])
    assert len({r['id'] for r in before['records']}) == 3
    assert all(r[field] == '' for r in before['records'] for field in FIELDS)
    assert before['state'] == 'draft' and before['human_review'] == 'pending' and before['company_approved'] is False

    taxonomy_raw = (BASE / '01_공통용어/공통용어사전.json').read_bytes()
    taxonomy = parse(taxonomy_raw)
    terms = {t['id']: t for t in taxonomy['terms']}
    assert len(terms) == len(taxonomy['terms']), 'duplicate canonical term IDs'
    for record in before['records']:
        term = terms[record['term_ref']['id']]
        assert record['term_ref']['version'] == term['version']
        assert record['source_snapshot'] == term
        assert record['source_file']['sha256'] == sha(taxonomy_raw)
        assert record['source_file']['path'] == '01_공통용어/공통용어사전.json'
        assert record['source_file']['locator'] == 'terms[id=' + term['id'] + ']'

    # Replace only the authorized scalar tokens, preserving unrelated bytes and whitespace.
    text = before_raw.decode('utf-8')
    assert text.count('"document_version": "0.1.0"') == 1
    text = text.replace('"document_version": "0.1.0"', '"document_version": "0.1.1"', 1)
    for field in FIELDS:
        assert text.count('"' + field + '": ""') == 3
    for record in CONTENT:
        expression = r'("id": "' + re.escape(record['id']) + r'",\r?\n      "version": )"0\.1\.0"'
        text, count = re.subn(expression, r'\g<1>"0.1.1"', text, count=1)
        assert count == 1
        for field in FIELDS:
            old_token = '"' + field + '": ""'
            new_token = '"' + field + '": ' + json.dumps(record[field], ensure_ascii=False)
            assert old_token in text
            text = text.replace(old_token, new_token, 1)
    candidate_raw = text.encode('utf-8')
    candidate = parse(candidate_raw)
    changes = diff(before, candidate)
    allowed = {'/document_version'} | {'/records/' + str(i) + '/' + f for i in range(3) for f in FIELDS + ['version']}
    assert {c['path'] for c in changes} == allowed and len(changes) == 19
    assert candidate['document_version'] == '0.1.1'
    assert all(r['version'] == '0.1.1' for r in candidate['records'])
    for rec in candidate['records']:
        for field in FIELDS:
            sentences = re.split(r'(?<=[.!?])\s+', rec[field].strip())
            assert 1 <= len(sentences) <= 2 and all(sentences)
        assert rec['example'].startswith('가상 예:')
        assert rec['example_kind'] == 'illustrative_not_actual_video'
    audit['events'].append({'event': 'candidate_validated_before_write', 'sha256': sha(candidate_raw), 'bytes': len(candidate_raw), 'changed_json_paths': len(changes)})
    (OUT / '쉬운말_지식카드_저장후보_v0.1.1.json').write_bytes(candidate_raw)
    save_json('변경diff.json', changes)
    patch = ''.join(difflib.unified_diff(before_raw.decode('utf-8').splitlines(True), candidate_raw.decode('utf-8').splitlines(True), fromfile=REL + '@0.1.0', tofile=REL + '@0.1.1'))
    (OUT / '변경diff.patch').write_bytes(patch.encode('utf-8'))
    save_json('작업전_snapshot.json', {'path': REL, 'sha256': before_sha, 'bytes': len(before_raw), 'signature': signature(before), 'allowed_json_paths': sorted(allowed)})

    # Back up the exact original bytes once; never overwrite a pre-existing backup.
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    with BACKUP.open('xb') as stream:
        n = stream.write(before_raw)
        stream.flush()
        os.fsync(stream.fileno())
    backup_raw = BACKUP.read_bytes()
    assert n == len(before_raw) and backup_raw == before_raw and sha(backup_raw) == before_sha
    audit['events'].append({'event': 'byte_identical_backup', 'path': str(BACKUP), 'sha256': sha(backup_raw), 'bytes': len(backup_raw), 'exact_byte_equal': True})

    # Immediately before the first target write, compare both SHA and identity/version signature.
    current_raw = TARGET.read_bytes()
    current = parse(current_raw)
    assert sha(current_raw) == before_sha and signature(current) == signature(before), 'concurrent target change; hold without overwrite'
    # Also detect changes in the sources actually read; do not silently repin any manifest.
    source_prewrite = []
    for rel, pin in manifest.items():
        if rel == REL:
            continue
        actual = sha((BASE / rel).read_bytes())
        source_prewrite.append({'path': rel, 'expected_sha256': pin['sha256'], 'actual_sha256': actual, 'unchanged': actual == pin['sha256']})
    assert all(item['unchanged'] for item in source_prewrite), 'read source changed; hold'
    # Recompare target again after source checks so this is the final operation before writing.
    immediate_raw = TARGET.read_bytes()
    assert sha(immediate_raw) == before_sha and signature(parse(immediate_raw)) == signature(before)
    audit['events'].append({'event': 'immediate_prewrite_recheck', 'sha256': sha(immediate_raw), 'signature_equal': True, 'all_read_sources_unchanged': True})
    save_json('쓰기직전_재대조.json', {'target_sha256': sha(immediate_raw), 'target_signature_unchanged': True, 'sources': source_prewrite})
    with TARGET.open('wb') as stream:
        written = stream.write(candidate_raw)
        stream.flush()
        os.fsync(stream.fileno())
    write_complete = True
    audit['events'].append({'event': 'target_write', 'path': str(TARGET), 'bytes_requested': len(candidate_raw), 'bytes_written': written, 'sha256_written_bytes': sha(candidate_raw), 'partial_file': False})
    assert written == len(candidate_raw)

    actual_raw = TARGET.read_bytes()
    actual = parse(actual_raw)
    assert actual_raw == candidate_raw
    post_changes = diff(before, actual)
    assert post_changes == changes and {c['path'] for c in post_changes} == allowed
    assert len({r['id'] for r in actual['records']}) == 3
    assert actual['document_version'] == '0.1.1' and all(r['version'] == '0.1.1' for r in actual['records'])
    source_post = []
    for rel, pin in manifest.items():
        if rel == REL:
            continue
        actual_sha = sha((BASE / rel).read_bytes())
        source_post.append({'path': rel, 'before_sha256': pin['sha256'], 'after_sha256': actual_sha, 'unchanged': actual_sha == pin['sha256']})
    assert all(item['unchanged'] for item in source_post)
    save_json('읽은입력_저장후_SHA보존검사.json', source_post)
    index_raw = (BASE / '작업초안/연결목록.json').read_bytes()
    index = parse(index_raw)
    stale_refs = [{'id': item['id'], 'recorded_document_version': item['draft_ref']['document_version'], 'recorded_record_version': item['draft_ref']['record_version'], 'recorded_file_sha256': item['draft_ref']['file_sha256'], 'actual_document_version': actual['document_version'], 'actual_record_version': next(r['version'] for r in actual['records'] if r['id'] == item['id']), 'actual_file_sha256': sha(actual_raw), 'action': 'unchanged_by_explicit_task; follow-up record steward update required'} for item in index['items']]
    save_json('연결목록_후속관리_차이.json', {'index_sha256': sha(index_raw), 'index_unchanged': sha(index_raw) == manifest['작업초안/연결목록.json']['sha256'], 'stale_refs': stale_refs})
    errata_checks = json.loads((OUT / '정정별_원문과근거_SHA검사.json').read_text(encoding='utf-8'))
    result = {
        'task_kind': 'normal_small_copy_knowledge_curation_not_performance_comparison',
        'status': 'draft_saved_bounded_direct_checks_passed',
        'target': str(TARGET),
        'ids': [r['id'] for r in actual['records']],
        'document_version': {'before': before['document_version'], 'after': actual['document_version']},
        'record_versions': [{'id': old['id'], 'before': old['version'], 'after': new['version']} for old, new in zip(before['records'], actual['records'])],
        'before_sha256': before_sha,
        'after_sha256': sha(actual_raw),
        'before_bytes': len(before_raw),
        'after_bytes': len(actual_raw),
        'backup': {'path': str(BACKUP), 'sha256': sha(backup_raw), 'byte_identical_to_before': backup_raw == before_raw},
        'checks': {
            'json_parse_and_duplicate_keys': 'pass',
            'three_unique_record_ids': 'pass',
            'canonical_term_refs_and_versions': 'pass',
            'source_snapshot_equals_current_three_original_terms': 'pass',
            'source_file_sha_and_locator': 'pass',
            'immediate_prewrite_sha_id_version_recheck': 'pass',
            'actual_saved_bytes_equal_candidate': 'pass',
            'only_allowed_json_paths_changed': 'pass',
            'changed_json_path_count': 19,
            'all_fifteen_explanatory_fields_one_or_two_sentences': 'pass',
            'three_examples_explicitly_illustrative': 'pass',
            'document_and_record_versions_0_1_1': 'pass',
            'read_only_input_sha_preservation': 'pass_for_' + str(len(source_post)) + '_read_inputs_only',
            'current_guide_and_errata_exists_and_read': 'pass',
            'errata_original_and_basis_pins': {c['id']: c['status'] for c in errata_checks},
        },
        'preserved_fields': ['source_snapshot', 'term_ref', 'id', 'source_file', 'state', 'example_kind', 'company_approved', 'human_review', 'all_other_non_allowed_fields'],
        'human_review': actual['human_review'],
        'company_approved': actual['company_approved'],
        'operational_release_performed': False,
        'meaning_change_or_taxonomy_merge': 'none_requested_or_performed',
        'source_read_depth': '내용근거_확인절과판본.json and 01/02 stdout; no external works fetched/read',
        'not_run': [
            'R4 integrated record validator: target is a separate knowledge draft, not a supported v0.2 video record',
            'validate_catalogs: source delegates to 구형기록_보존검사.py, which is not supplied in this copy; no forced source execution',
            'R6/R7 full query: full source archive/context not supplied; direct local source/term/allowed-diff checks only',
            'R8 candidate full connector query: not supplied; no candidate/default installation or switch',
            'actual video, API, network, CU, AE, 01-A, company approval, new human reply, performance/time/token/effect measurement',
        ],
        'missing_explicit_paths': json.loads((OUT / '참조범위_존재확인.json').read_text(encoding='utf-8')),
        'follow_up': {'index': '작업초안/연결목록.json deliberately unchanged and stale at 0.1.0; record steward must update the three draft refs in its authorized follow-up', 'registration': 'working draft absent from canonical/display generation entries; registration/default adoption not performed', 'human': 'three v0.1.1 cards remain pending; no new human decision or approval has been received'},
        'human_review_proposal_not_sent': {
            'target': '시범카드001/002/003@0.1.1 wording and meaning preservation only',
            'A_recommended': '세 카드 전체를 원문과 대조해 쉬운말과 의미 보존만 내용 검토한다.',
            'B': '선형 프로세스의 가로·세로, 분기와 시간축 구분 문구부터 검토하고 나머지는 미검수로 둔다.',
            'C': '주목 이동의 실제 시선 효과와 가시성 변화의 구현 원인 구분부터 검토하고 나머지는 미검수로 둔다.',
            'D': '현재 초안을 보류 상태로 두고, 문제되는 카드·문장과 추가로 필요한 원문을 지정한다.',
            'reason_for_A': '새 의미·정식 분류·승인을 추가하지 않고 이번에 작성한 세 카드의 범위 전체를 확인할 수 있다.',
        },
        'failure': None,
        'restore': 'not_needed; no failure encountered',
        'limitations': ['Single-file immediate recheck reduces stale overwrite risk but does not provide a cross-file atomic transaction or complete concurrent-write lock.', 'Automated checks establish parsing, identity/version/source pins and allowed changes; readability and content approval remain human review pending.'],
    }
    dependency = BASE / '07_실행도구/구형기록_보존검사.py'
    result['existing_catalog_validator_dependency_exists_in_copy'] = dependency.is_file()
    assert not dependency.is_file()
    save_json('결과.json', result)
    audit['status'] = result['status']
    audit['events'].append({'event': 'post_save_bounded_checks_passed', 'actual_sha256': sha(actual_raw), 'bytes': len(actual_raw), 'allowed_changed_paths': len(post_changes), 'preserved_read_input_count': len(source_post)})
    save_json('쓰기와검사_감사로그.json', audit)

    report = f'''# 큐레이터 소량 사본 시범 결과

제공된 원문 3개에 대한 쉬운 설명·사용 조건·가상 예·반례·주의점을 실제 작업초안에 작성했다. 이 결과는 정상 지식 정리 시범이며 성능 비교·실영상 시험·회사 승인이 아니다.

- 대상: `{REL}` / 시범카드001·002·003
- 문서 판본과 카드 3개의 판본: 0.1.0 → 0.1.1
- 변경 전 SHA256: `{before_sha}`
- 저장 후 SHA256: `{sha(actual_raw)}`
- 실제 쓰기 바이트: {len(actual_raw)}
- byte 동일 백업: `{BACKUP.relative_to(BASE).as_posix()}` / SHA256 `{sha(backup_raw)}`
- JSON 파싱·중복 키/ID·원문 참조/판본/SHA·저장 직전 재대조·실제 저장 후 대조·허용 diff 검사: 수행, 좁은 검사 범위 통과. 변경은 허용된 19개 JSON 경로뿐이다.
- source_snapshot·term_ref·ID·출처·상태·회사승인·미검수 값과 읽은 고정 입력 {len(source_post)}개는 보존했다. 직접 조회하지 않은 모든 입력의 무변경을 전수 검사했다고 주장하지 않는다.

## 카드에 남긴 의미

| 카드 | 원문의 축 | 쉬운말 정리에서 보존한 조건 |
|---|---|---|
| 선형 프로세스 | layout | 순서 있는 단계의 연결, 가로·세로 방향 별도 기록, 중요 분기·회귀를 숨기지 않음, 시간 길이와 구분, 선후 근거 부족 시 미확정 |
| 주목 이동 | motion_function | 현재 설명 대상에 주목을 옮기는 기능, 시간 변화와 설명 맥락 필요, 모든 이동과 구분, 실제 시선 효과는 별도 검토 |
| 가시성 변화 | motion_property | 보이는 범위·강도의 시간 변화, 동일 대상/시간 범위 확인, 관측과 불투명도·마스크·합성·배경 원인 추정을 분리 |

모든 예는 `가상 예:`로 표시했고 기존 example_kind를 유지했다. 회사 사례·실제 시청 효과·원본 키프레임이나 수치를 만들지 않았다.

## 확인한 근거

`내용근거_확인절과판본.json`에 공통용어사전 v0.1.1의 원문 3항목(각 term v0.1.0), 용어판정기준 v0.1.2의 관련 3항목, 레이아웃지식 v0.1.1 및 심화지식 v0.1.2의 선형 프로세스 카드를 기록했다. `07_레이아웃별_선택조건과반례.md`는 머리말과 선형 프로세스 절을 확인했다. 입력 파일의 실제 SHA는 `입력_SHA_작업시작.json`과 저장 후 보존검사에 있다. 외부 문헌 목록은 문헌 본문을 읽었다는 뜻으로 사용하지 않았다.

`14_스킬재구성/R8_현재사용안내.md`와 같은 폴더의 `현재상태_정정표.json`을 실제 읽었다. ST-R4·ST-R2·ST-R2-JSON·ST-HANDOFF·ST-R7-R8의 원문/근거 파일은 제공 사본에서 존재와 SHA가 모두 일치했다. 이는 과거 단계 표시의 국소 정정 확인이다. R8 안내가 링크한 최신 진행현황·통합 최종보고는 사본의 해당 경로에서 없음을 직접 확인했으므로 최신 전체 종료를 독립 재확인했다고 보고하지 않는다. 정정의 과거 사람 회신은 이번 카드의 승인으로 사용하지 않았다.

## 미실시와 후속

이 사본에는 전체 R6/R7 원문·출처보관소가 없다. R6/R7 full 조회 통과나 R4 전체 스키마 통과를 보고하지 않는다. 자료검증.py는 소스만 확인했으며 이 지식 초안에 실행하지 않았다. validate_catalogs가 위임하는 구형기록_보존검사.py도 사본에 없음을 직접 확인했다. 설치·네트워크·API·영상·CU·AE·01-A·새 스킬 변경/기본 전환과 시간/토큰/효과 측정은 하지 않았다.

`작업초안/연결목록.json`은 요청에 따라 바꾸지 않았다. 세 draft_ref가 이전 0.1.0/이전 SHA를 계속 가리키므로 후속 기록 관리자가 갱신해야 한다. 차이는 `연결목록_후속관리_차이.json`에 있다. 이 작업초안은 정본/표시 생성물 목록에도 등록되지 않아 등록·기본 전환을 완료했다고 보고하지 않는다.

human_review=pending과 company_approved=false를 유지했다. 이번 쉬운말 정리에 새 의미 변경·분류 병합은 필요하지 않아 새 사람 질문을 접수하거나 회신을 꾸미지 않았다. 후속 사람 내용 검토의 구체 선택지는 다음과 같으며 승인 요청은 보내지 않았다.

- A (추천): v0.1.1 세 카드 전체를 원문과 대조해 쉬운말과 의미 보존만 내용 검토한다.
- B: 선형 프로세스의 가로·세로, 분기와 시간축 구분부터 검토하고 나머지는 미검수로 둔다.
- C: 주목 이동의 시선 효과와 가시성 변화의 구현 원인 구분부터 검토하고 나머지는 미검수로 둔다.
- D: 초안을 보류 상태로 두고 문제 카드·문장과 추가로 필요한 원문을 지정한다.

A는 이번 3카드 범위를 빠뜨리지 않으면서 의미 변경이나 회사 승인을 추가하지 않는다. 실제 사람 검토는 아직 수행되지 않았다.

실제 오류·부분 저장·복구는 발생하지 않았다. 저장 전 재대조는 완전한 동시성 잠금이나 여러 파일의 원자성을 보장하지 않는다. 실행 코드·명령·stdout/stderr·exit는 01/02/03 실행 파일과 로그, transcript에 보존했다.
'''
    (OUT / '결과.md').write_text(report, encoding='utf-8')
    print(json.dumps({'status': result['status'], 'target': str(TARGET), 'before_sha256': before_sha, 'after_sha256': sha(actual_raw), 'bytes_written': len(actual_raw), 'backup': str(BACKUP), 'backup_sha256': sha(backup_raw), 'allowed_changes': 19, 'checks': result['checks'], 'human_review': result['human_review'], 'company_approved': False, 'follow_up': result['follow_up']}, ensure_ascii=False, indent=2))
except Exception as exc:
    audit['status'] = 'failed_or_held'
    audit['failure'] = {'type': type(exc).__name__, 'message': str(exc), 'traceback': traceback.format_exc()}
    if write_complete and candidate_raw is not None and TARGET.read_bytes() == candidate_raw and before_raw is not None:
        with TARGET.open('wb') as stream:
            stream.write(before_raw)
            stream.flush()
            os.fsync(stream.fileno())
        restored = TARGET.read_bytes()
        audit['restore'] = {'status': 'restored_only_after_own_bytes_match', 'sha256': sha(restored), 'matches_original': restored == before_raw}
    else:
        audit['restore'] = 'not_attempted_without_confirmed_own_complete_bytes; inspect actual target before further use'
    save_json('쓰기와검사_감사로그.json', audit)
    save_json('실패또는보류.json', audit)
    print(json.dumps(audit, ensure_ascii=False, indent=2), file=sys.stderr)
    raise
