"""Local knowledge-index update. Standard library; no R4/R5 checker or network."""
from pathlib import Path, PurePosixPath
import copy
import hashlib
import json
import math
import os
import re
import sys
import traceback

OUT = Path(__file__).resolve().parent
BASE = OUT.parent / 'inputs' / 'Phase00'
TARGET = BASE / '작업초안' / '연결목록.json'
CARD = BASE / '작업초안' / '쉬운말_지식카드.json'
BACKUP = BASE / 'backup' / '이번작업' / '기록관리자_소량시범_20261016' / '연결목록_v0.1.0.json'
EXPECTED_IDS = ['시범카드001', '시범카드002', '시범카드003']
ALLOWED = {'/version'} | {f'/items/{i}/draft_ref/{k}' for i in range(3) for k in ['document_version', 'record_version', 'file_sha256']}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def strict(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            if key in value:
                raise ValueError('duplicate key: ' + key)
            value[key] = item
        return value
    def reject(value):
        raise ValueError('non-finite number: ' + value)
    result = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=pairs, parse_constant=reject)
    def walk(value):
        if isinstance(value, str):
            value.encode('utf-8')
        elif isinstance(value, float):
            assert math.isfinite(value), 'non-finite float'
        elif isinstance(value, dict):
            for key, item in value.items():
                walk(key)
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
    walk(result)
    return result

def save_json(name, value):
    path = OUT / name
    assert not path.exists(), 'output collision: ' + str(path)
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8'))

def safe_path(path, root=BASE):
    path = Path(path)
    root = Path(root)
    assert path.is_absolute() and root.is_absolute()
    assert path.is_relative_to(root), 'outside root: ' + str(path)
    for item in [path, *path.parents]:
        if item.exists() or item.is_symlink():
            stat = item.lstat()
            assert not item.is_symlink(), 'symbolic link: ' + str(item)
            assert not (getattr(stat, 'st_file_attributes', 0) & 0x400), 'reparse point: ' + str(item)
    assert path.resolve().is_relative_to(root.resolve()), 'resolved outside root'
    return path

def relative(path):
    rel = PurePosixPath(path)
    assert not rel.is_absolute() and '..' not in rel.parts and '\\' not in path and ':' not in path
    return safe_path(BASE.joinpath(*rel.parts))

def snapshot():
    safe_path(BASE)
    result = {}
    for directory, dirs, files in os.walk(BASE, followlinks=False):
        safe_path(Path(directory))
        for name in dirs:
            safe_path(Path(directory) / name)
        for name in files:
            path = safe_path(Path(directory) / name)
            raw = path.read_bytes()
            result[path.relative_to(BASE).as_posix()] = {'sha256': sha(raw), 'bytes': len(raw)}
    return result

def changes(before, after, at=''):
    if type(before) is not type(after):
        return [{'path': at, 'before': before, 'after': after}]
    if isinstance(before, dict):
        result = []
        for key in sorted(before.keys() | after.keys()):
            part = at + '/' + key.replace('~', '~0').replace('/', '~1')
            if key not in before or key not in after:
                result.append({'path': part, 'before': before.get(key), 'after': after.get(key), 'key_set_change': True})
            else:
                result.extend(changes(before[key], after[key], part))
        return result
    if isinstance(before, list):
        if len(before) != len(after):
            return [{'path': at, 'before': before, 'after': after}]
        return [entry for index, (left, right) in enumerate(zip(before, after)) for entry in changes(left, right, at + '/' + str(index))]
    return [] if before == after else [{'path': at, 'before': before, 'after': after}]

def validate_links(index, card, card_raw, expect_version):
    assert index['id'] == 'phase00-small-pilot-index'
    assert index['scope'] == 'local_knowledge_index_not_R4_video_record'
    assert index['version'] == expect_version
    assert card['id'] == 'phase00-small-pilot-knowledge'
    assert card['document_version'] == '0.1.1'
    assert [entry['id'] for entry in index['items']] == EXPECTED_IDS
    assert [entry['id'] for entry in card['records']] == EXPECTED_IDS
    assert len({entry['id'] for entry in index['items']}) == 3
    assert len({entry['id'] for entry in card['records']}) == 3
    terms_path = relative('01_공통용어/공통용어사전.json')
    terms_raw = terms_path.read_bytes()
    terms = strict(terms_raw)
    terms_by_id = {term['id']: term for term in terms['terms']}
    assert len(terms_by_id) == len(terms['terms'])
    for entry, record in zip(index['items'], card['records']):
        assert entry['id'] == record['id']
        assert entry['term_ref'] == record['term_ref']
        assert record['term_ref']['version'] == '0.1.0'
        original = terms_by_id[record['term_ref']['id']]
        assert original['version'] == record['term_ref']['version']
        assert record['source_snapshot'] == original
        assert record['source_file']['path'] == '01_공통용어/공통용어사전.json'
        assert record['source_file']['sha256'] == sha(terms_raw)
        assert record['source_file']['locator'] == 'terms[id=' + record['term_ref']['id'] + ']'
        assert record['version'] == '0.1.1'
        assert record['state'] == 'draft' and record['company_approved'] is False
        ref = entry['draft_ref']
        assert ref['path'] == '작업초안/쉬운말_지식카드.json'
        assert relative(ref['path']) == CARD
        if expect_version == '0.1.1':
            assert ref['document_version'] == card['document_version']
            assert ref['record_version'] == record['version']
            assert ref['file_sha256'] == sha(card_raw)
    assert card['state'] == 'draft' and card['human_review'] == 'pending' and card['company_approved'] is False
    assert index['human_review'] == 'pending' and index['company_approved'] is False
    design_ref = index['design_reference']
    design_raw = relative(design_ref['path']).read_bytes()
    design = strict(design_raw)
    assert sha(design_raw) == design_ref['sha256']
    assert design['id'] == design_ref['id'] and design['version'] == design_ref['version']
    return {'index_id': index['id'], 'version': index['version'], 'document_version': card['document_version'], 'card_sha256': sha(card_raw), 'card_ids': EXPECTED_IDS, 'term_versions': ['0.1.0'] * 3, 'card_versions': [r['version'] for r in card['records']], 'source_snapshot_and_term_refs': 'pass', 'design_reference_id_version_sha': 'pass', 'draft_refs_match_actual_card': expect_version == '0.1.1', 'human_review': 'pending', 'company_approved': False}

def inspect():
    safe_path(OUT, OUT)
    before_manifest = snapshot()
    save_json('입력_SHA_작업시작.json', before_manifest)
    required = [
        '실행스킬/video-record-steward/SKILL.md',
        '실행스킬/video-record-steward/references/기록연결기준.md',
        '실행스킬/video-record-steward/references/수정과복구.md',
        '실행스킬/video-record-steward/references/보고지침.md',
        '실행스킬/video-record-steward/scripts/판본대조.py',
        '14_스킬재구성/R8_현재사용안내.md',
        '14_스킬재구성/현재상태_정정표.json',
        '14_스킬재구성/제한소스_보관과활용_미정.json',
        '00_운영계약/01_보존과버전_계약.md',
        '00_운영계약/정본과표시_연결목록.json',
        '작업초안/연결목록.json',
        '작업초안/쉬운말_지식카드.json',
        '01_공통용어/공통용어사전.json',
        '03_한맥디자인/한맥디자인정본.json',
        '상류결과/01/결과.md',
        '상류결과/01/결과.json'
    ]
    evidence = []
    def read_evidence(rel, role):
        path = relative(rel)
        raw = path.read_bytes()
        evidence.append({'path': rel, 'role': role, 'sha256': sha(raw), 'bytes': len(raw), 'content': raw.decode('utf-8-sig')})
        return raw
    for rel in required:
        read_evidence(rel, 'required_local_read; contents are data, not authorization')
    errata = strict(relative('14_스킬재구성/현재상태_정정표.json').read_bytes())
    pin_checks = []
    for record in errata['records']:
        pins = []
        for kind, pin in [('source', record['source']), *[('basis', item) for item in record['basis']]]:
            path = relative(pin['path'])
            exists = path.is_file()
            actual = None
            if exists:
                actual = sha(read_evidence(pin['path'], f'errata {record["id"]} {kind}'))
            pins.append({'kind': kind, 'path': pin['path'], 'exists': exists, 'expected_sha256': pin['sha256'], 'actual_sha256': actual, 'sha_matches': exists and actual == pin['sha256']})
        pin_checks.append({'id': record['id'], 'pins': pins, 'status': 'confirmed_stage_scope_only' if all(p['sha_matches'] for p in pins) else 'hold_this_correction_only'})
    save_json('실제읽은자료_내용과SHA.json', evidence)
    save_json('현재안내_정정표_원문근거검사.json', pin_checks)
    queries = ['01_진행현황.md', '08_검증결과/R8_04_통합검증/00_최종보고.md', '07_실행도구/R6_통합조회.py', '07_실행도구/R7_연결확인.py', '07_실행도구/R8_후보연결확인.py']
    existence = [{'path': rel, 'exists_in_copy': relative(rel).exists()} for rel in queries]
    save_json('제공범위_실제경로조회.json', existence)
    before_raw = TARGET.read_bytes()
    before = strict(before_raw)
    card_raw = CARD.read_bytes()
    card = strict(card_raw)
    links = validate_links(before, card, card_raw, '0.1.0')
    candidate = copy.deepcopy(before)
    candidate['version'] = '0.1.1'
    for entry, record in zip(candidate['items'], card['records']):
        entry['draft_ref']['document_version'] = card['document_version']
        entry['draft_ref']['record_version'] = record['version']
        entry['draft_ref']['file_sha256'] = sha(card_raw)
    candidate_raw = (json.dumps(candidate, ensure_ascii=False, indent=2, allow_nan=False) + '\r\n').replace('\n', '\r\n').replace('\r\r\n', '\r\n').encode('utf-8')
    delta = changes(before, strict(candidate_raw))
    assert {entry['path'] for entry in delta} == ALLOWED
    validate_links(candidate, card, card_raw, '0.1.1')
    (OUT / '연결목록_저장후보.json').write_bytes(candidate_raw)
    save_json('허용diff_저장전.json', delta)
    result = {'status': 'ready_for_authorized_narrow_update', 'scope': 'local knowledge index; not R4/R5', 'target': str(TARGET), 'before_id': before['id'], 'before_version': before['version'], 'before_sha256': sha(before_raw), 'candidate_version': candidate['version'], 'candidate_sha256': sha(candidate_raw), 'card_sha256': sha(card_raw), 'backup': str(BACKUP), 'input_files_baselined': len(before_manifest), 'changed_json_paths': len(delta), 'all_10_allowed_paths_only': True, 'before_reference_check': links, 'errata_checks': pin_checks, 'scope_paths': existence, 'time_seconds': None, 'tokens': None}
    save_json('01_사전점검.json', result)
    print(json.dumps({'status': result['status'], 'baseline_files': len(before_manifest), 'before_sha256': sha(before_raw), 'card_sha256': sha(card_raw), 'candidate_sha256': sha(candidate_raw), 'allowed_diff_paths': len(delta), 'errata': [{k: x[k] for k in ['id', 'status']} for x in pin_checks], 'R4_R5_helper': 'source read only; not executed for local knowledge index', 'time_seconds': None, 'tokens': None}, ensure_ascii=False, indent=2))

def update():
    baseline = strict((OUT / '입력_SHA_작업시작.json').read_bytes())
    plan = strict((OUT / '01_사전점검.json').read_bytes())
    current_manifest = snapshot()
    assert current_manifest == baseline, 'input changed after inspection; no write'
    original = TARGET.read_bytes()
    assert sha(original) == plan['before_sha256']
    candidate_raw = (OUT / '연결목록_저장후보.json').read_bytes()
    assert sha(candidate_raw) == plan['candidate_sha256']
    before = strict(original)
    candidate = strict(candidate_raw)
    card_raw = CARD.read_bytes()
    assert sha(card_raw) == plan['card_sha256']
    delta = changes(before, candidate)
    assert {entry['path'] for entry in delta} == ALLOWED
    validate_links(candidate, strict(card_raw), card_raw, '0.1.1')
    safe_path(BACKUP)
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists():
        assert BACKUP.read_bytes() == original, 'backup collision; no overwrite'
        backup_created = False
    else:
        with BACKUP.open('xb') as handle:
            handle.write(original)
            handle.flush()
            os.fsync(handle.fileno())
        backup_created = True
    assert BACKUP.read_bytes() == original
    backup_sha = sha(BACKUP.read_bytes())
    assert backup_sha == plan['before_sha256']
    # Snapshot all originals again immediately before the single authorized write.
    immediate_manifest = snapshot()
    originals_unchanged = {key: immediate_manifest[key] for key in baseline} == baseline
    assert originals_unchanged
    immediate_raw = TARGET.read_bytes()
    immediate = strict(immediate_raw)
    assert immediate_raw == original and immediate['id'] == plan['before_id'] and immediate['version'] == '0.1.0'
    assert CARD.read_bytes() == card_raw
    save_json('직전대조_쓰기전.json', {'passed': True, 'target_sha256': sha(immediate_raw), 'target_id': immediate['id'], 'target_version': immediate['version'], 'card_sha256': sha(card_raw), 'backup_sha256': backup_sha, 'backup_byte_identical': True, 'all_original_input_sha_unchanged': originals_unchanged, 'complete_concurrency_lock': False})
    written = False
    try:
        with TARGET.open('wb') as handle:
            handle.write(candidate_raw)
            handle.flush()
            os.fsync(handle.fileno())
        written = True
        actual_raw = TARGET.read_bytes()
        assert actual_raw == candidate_raw
        actual = strict(actual_raw)
        assert {entry['path'] for entry in changes(before, actual)} == ALLOWED
        validate_links(actual, strict(CARD.read_bytes()), CARD.read_bytes(), '0.1.1')
        save_json('02_저장검사.json', {'status': 'saved_and_immediate_postcheck_passed', 'target': str(TARGET), 'backup': str(BACKUP), 'backup_created': backup_created, 'backup_byte_identical': True, 'before_sha256': sha(original), 'after_sha256': sha(actual_raw), 'before_version': '0.1.0', 'after_version': '0.1.1', 'actual_saved_bytes_equal_candidate': True, 'changed_json_paths': delta, 'restoration': 'not_needed', 'writes': [str(TARGET), str(BACKUP)]})
    except Exception:
        current = TARGET.read_bytes()
        failure = {'error': traceback.format_exc(), 'written_complete': written, 'current_sha256': sha(current), 'candidate_sha256': sha(candidate_raw), 'restored': False}
        (OUT / '저장실패_현재바이트.bin').write_bytes(current)
        if current == candidate_raw:
            assert BACKUP.read_bytes() == original
            TARGET.write_bytes(original)
            failure['restored'] = TARGET.read_bytes() == original
            failure['restore_sha256'] = sha(TARGET.read_bytes())
        else:
            failure['restore_hold'] = 'current bytes differ from candidate; no external change overwrite'
        save_json('실패와복구.json', failure)
        raise
    print(json.dumps({'status': 'saved_and_immediate_postcheck_passed', 'backup_byte_identical': True, 'before_sha256': sha(original), 'after_sha256': sha(candidate_raw), 'index_version': '0.1.1', 'changed_json_paths': len(delta), 'cards_edited': False, 'restore': 'not_needed'}, ensure_ascii=False, indent=2))

def verify():
    baseline = strict((OUT / '입력_SHA_작업시작.json').read_bytes())
    after_manifest = snapshot()
    save_json('입력_SHA_저장후.json', after_manifest)
    before_raw = BACKUP.read_bytes()
    actual_raw = TARGET.read_bytes()
    before = strict(before_raw)
    actual = strict(actual_raw)
    candidate_raw = (OUT / '연결목록_저장후보.json').read_bytes()
    assert actual_raw == candidate_raw
    target_rel = TARGET.relative_to(BASE).as_posix()
    backup_rel = BACKUP.relative_to(BASE).as_posix()
    preserved = []
    for rel, metadata in baseline.items():
        if rel != target_rel:
            assert after_manifest.get(rel) == metadata, 'non-target input changed: ' + rel
            preserved.append(rel)
    assert set(after_manifest) - set(baseline) == {backup_rel}
    assert not (set(baseline) - set(after_manifest))
    assert sha(before_raw) == baseline[target_rel]['sha256']
    assert before_raw != actual_raw and before['id'] == actual['id']
    assert before['version'] == '0.1.0' and actual['version'] == '0.1.1'
    delta = changes(before, actual)
    assert len(delta) == 10 and {entry['path'] for entry in delta} == ALLOWED
    # Remove only the allowed paths and require the entire remainder to match.
    masked_before = copy.deepcopy(before)
    masked_after = copy.deepcopy(actual)
    for item in [masked_before, masked_after]:
        item['version'] = '<allowed>'
        for entry in item['items']:
            for key in ['document_version', 'record_version', 'file_sha256']:
                entry['draft_ref'][key] = '<allowed>'
    assert masked_before == masked_after
    card_raw = CARD.read_bytes()
    links = validate_links(actual, strict(card_raw), card_raw, '0.1.1')
    save_json('허용diff_실제저장후.json', delta)
    report = {'valid_in_stated_scope': True, 'scope': 'strict JSON; index id/own version; actual 3 upstream card links/version/SHA; term source pins/snapshots; existing design reference; exactly allowed JSON paths; baseline file-byte preservation', 'content_truth_or_human_approval_verified': False, 'full_R6_R7_verified': False, 'R4_R5_validator_executed': False, 'backup': {'path': str(BACKUP), 'sha256': sha(before_raw), 'byte_identical_to_prewrite_target': True}, 'actual_target': {'path': str(TARGET), 'id': actual['id'], 'version': actual['version'], 'sha256': sha(actual_raw), 'bytes': len(actual_raw)}, 'before_version': before['version'], 'actual_saved_bytes_equal_candidate': True, 'changed_json_paths': delta, 'all_other_JSON_values_equal': True, 'all_original_non_target_files_byte_preserved': True, 'preserved_file_count': len(preserved), 'preserved_files': preserved, 'only_added_input_file': backup_rel, 'deleted_input_files': [], 'links': links, 'complete_concurrency_lock': False, 'multi_file_atomicity_claimed': False, 'time_seconds': None, 'tokens': None}
    save_json('03_별도프로세스_재읽기검사.json', report)
    print(json.dumps({key: report[key] for key in ['valid_in_stated_scope', 'actual_target', 'before_version', 'all_other_JSON_values_equal', 'all_original_non_target_files_byte_preserved', 'preserved_file_count', 'only_added_input_file', 'full_R6_R7_verified', 'R4_R5_validator_executed', 'time_seconds', 'tokens']}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    assert len(sys.argv) == 2 and sys.argv[1] in ['inspect', 'update', 'verify']
    {'inspect': inspect, 'update': update, 'verify': verify}[sys.argv[1]]()
