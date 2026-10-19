from pathlib import Path
import sys, os, json, re, hashlib, difflib, subprocess, importlib.util, traceback

RUN = Path(__file__).resolve().parents[1]
BASE = RUN / 'inputs/Phase00'
OUT = RUN / 'outputs'
R4 = BASE / '12_통합기록/통합기록_작업초안.json'
R5 = BASE / '작업초안/디자인적용_초안.json'
events = []
written = []
before = {}
candidates = {}
report = {'status': 'in_progress', 'scope': '합성 작업사본의 요청된 두 초안 수정 및 구조/참조 검사', 'db_root': str(BASE), 'elapsed_time': None, 'tokens': None, 'telemetry': '미수집'}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def strict(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            if key in value:
                raise ValueError('중복 JSON 키: ' + key)
            value[key] = item
        return value
    def reject(value):
        raise ValueError('비유한 JSON 수: ' + value)
    return json.loads(raw.decode('utf-8-sig'), object_pairs_hook=pairs, parse_constant=reject)

def guarded(path):
    path = Path(path)
    if not path.resolve().is_relative_to(RUN):
        raise ValueError('run 외부 경로 금지: ' + str(path))
    for ancestor in [path] + list(path.parents):
        if ancestor == RUN.parent:
            break
        if ancestor.exists() and (ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)()):
            raise ValueError('연결점 경로 금지: ' + str(ancestor))
    return path

def new(path, raw):
    path = guarded(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == raw:
            events.append({'action': 'existing_identical_output', 'path': str(path)})
            return
        raise FileExistsError('출력 충돌: ' + str(path))
    with path.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if path.read_bytes() != raw:
        raise OSError('저장 byte 검증 실패: ' + str(path))

def save_json(name, data):
    new(OUT / name, (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8'))

def diff(a, b, path=''):
    if type(a) is not type(b):
        return [{'path': path, 'before': a, 'after': b}]
    if isinstance(a, dict):
        assert a.keys() == b.keys(), '키 추가/삭제 금지'
        return [row for key in a for row in diff(a[key], b[key], path + '/' + key)]
    if isinstance(a, list):
        assert len(a) == len(b), '목록 길이 변경 금지'
        return [row for i, (av, bv) in enumerate(zip(a, b)) for row in diff(av, bv, path + '/' + str(i))]
    return [] if a == b else [{'path': path, 'before': a, 'after': b}]

def cli(label, tool, record, r4=False):
    cmd = [sys.executable, '-B', '-X', 'utf8', str(BASE / '07_실행도구' / tool)]
    if r4:
        cmd.append('--record')
    cmd.append(str(record))
    proc = subprocess.run(cmd, cwd=BASE, capture_output=True, encoding='utf-8', errors='strict')
    new(OUT / (label + '.stdout.txt'), proc.stdout.encode('utf-8'))
    new(OUT / (label + '.stderr.txt'), proc.stderr.encode('utf-8'))
    event = {'action': 'validator_cli', 'label': label, 'command': cmd, 'cwd': str(BASE), 'exit_code': proc.returncode, 'stdout': str(OUT / (label + '.stdout.txt')), 'stderr': str(OUT / (label + '.stderr.txt'))}
    events.append(event)
    result = strict(proc.stdout.encode('utf-8'))
    save_json(label + '.json', result)
    return {'exit_code': proc.returncode, 'result': result}

def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, BASE / '07_실행도구' / filename)
    item = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(item)
    assert item.BASE.resolve() == BASE.resolve()
    return item

def commit(path, expected, raw, label):
    guarded(path)
    assert path.read_bytes() == expected, '쓰기 직전 외부 변경 감지: ' + str(path)
    stage = OUT / (label + '.stage')
    new(stage, raw)
    assert path.read_bytes() == expected, '교체 직전 외부 변경 감지'
    os.replace(stage, path)
    written.append(path)
    assert path.read_bytes() == raw, '실제 저장 byte 불일치'
    events.append({'action': 'stored', 'path': str(path), 'sha256': sha(path.read_bytes()), 'method': '허용 outputs 내 임시파일을 os.replace로 교체; 여러 파일 transaction 보장 아님'})

try:
    assert sys.flags.dont_write_bytecode and sys.flags.utf8_mode
    for path in [R4, R5]:
        before[path] = guarded(path).read_bytes()
        strict(before[path])
    a, b = strict(before[R4]), strict(before[R5])
    assert a['record_id'] == b['linked_r4_record']['record_id']
    states = [x for x in a['spatial_contract']['evidence_contract']['targets'] if x['id'] == 'TG-STATE']
    units = [(i, x) for i, x in enumerate(a['units']) if x['target_ref']['id'] == 'TG-STATE']
    assert len(states) == len(units) == 1
    index, unit = units[0]
    target_version = states[0]['version']
    assert target_version == '0.1.0' and unit['target_ref']['version'] == '0.9.9'
    assert a['version'] == '0.1.0'
    report['baseline'] = {'r4': cli('before_r4', '자료검증.py', R4, True), 'r5': cli('before_r5', 'R5_디자인적용검사.py', R5)}
    for path in [R4, R5]:
        backup = OUT / 'backup' / path.relative_to(BASE)
        new(backup, before[path])
        assert backup.read_bytes() == before[path]
        events.append({'action': 'backup_verified_before_mutation', 'path': str(backup), 'sha256': sha(before[path]), 'byte_equal': True})

    raw = before[R4]
    raw, n = re.subn(rb'("record_id"\s*:\s*"R8-DEV-STEW-01"\s*,\s*"version"\s*:\s*")0\.1\.0(")', rb'\g<1>0.1.1\2', raw)
    assert n == 1
    raw, n = re.subn(rb'("target_ref"\s*:\s*\{\s*"id"\s*:\s*"TG-STATE"\s*,\s*"version"\s*:\s*")0\.9\.9(")', rb'\g<1>0.1.0\2', raw)
    assert n == 1
    candidates[R4] = raw
    updated = strict(raw)
    r4_diff = diff(a, updated)
    assert {v['path'] for v in r4_diff} == {'/version', '/units/' + str(index) + '/target_ref/version'}

    def update_link(match):
        block = match.group()
        block, n1 = re.subn(rb'("version"\s*:\s*")[^"]+(")', rb'\g<1>0.1.1\2', block)
        block, n2 = re.subn(rb'("sha256"\s*:\s*")[0-9a-f]{64}(")', lambda m: m[1] + sha(raw).encode('ascii') + m[2], block)
        assert n1 == n2 == 1
        return block
    # Existing JSON bytes and numeric spellings remain intact; only link fields change.
    link_raw, n = re.subn(rb'"linked_r4_record"\s*:\s*\{[^{}]*\}', update_link, before[R5])
    assert n == 1
    candidates[R5] = link_raw
    updated_r5 = strict(link_raw)
    r5_diff = diff(b, updated_r5)
    assert {v['path'] for v in r5_diff} == {'/linked_r4_record/version', '/linked_r4_record/sha256'}
    assert updated_r5['version'] == b['version'], 'R5는 연결만 갱신'
    for path in [R4, R5]:
        new(OUT / 'candidates' / path.name, candidates[path])
        new(OUT / (('r4' if path == R4 else 'r5') + '.diff'), ''.join(difflib.unified_diff(before[path].decode('utf-8').splitlines(keepends=True), candidates[path].decode('utf-8').splitlines(keepends=True), fromfile=str(path) + ':before', tofile=str(path) + ':after')).encode('utf-8'))
    save_json('field_diff.json', {'r4': r4_diff, 'r5': r5_diff, 'all_other_json_values_and_types_unchanged': True, 'serialization': '기존 바이트에 제한 치환; 시간/좌표/수치 표기도 보존'})
    r4mod = module('local_r4_entry', '자료검증.py')
    pre = r4mod.inspect_record(updated)
    save_json('candidate_r4.json', pre)
    events.append({'action': 'candidate_r4_api', 'call': '자료검증.inspect_record(candidate)', 'valid': pre['valid'], 'base': str(r4mod.BASE)})
    assert pre['valid'], 'R4 후보 검사 실패'
    r5mod = module('local_r5_entry', 'R5_디자인적용검사.py')
    from jsonschema import Draft202012Validator, FormatChecker
    schema = strict((BASE / '03_한맥디자인/디자인적용_기록규격.json').read_bytes())
    errors = [str(e) for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(updated_r5)]
    save_json('candidate_r5_schema.json', {'valid': not errors, 'errors': errors, 'scope': '후보 JSON 구조; 새 R4 실제 파일 참조 검사는 R4 저장 직후 및 R5 저장 후 수행'})
    assert not errors
    assert report['baseline']['r5']['result']['valid'], '기존 R5 참조 검사 실패'
    assert R4.read_bytes() == before[R4] and R5.read_bytes() == before[R5], '첫 쓰기 전 외부 변경 감지'
    commit(R4, before[R4], candidates[R4], 'r4_write')
    actual_sha = sha(R4.read_bytes())
    assert actual_sha == updated_r5['linked_r4_record']['sha256']
    linked_candidate = r5mod.inspect(updated_r5, base=BASE)
    save_json('candidate_r5_with_saved_r4.json', linked_candidate)
    events.append({'action': 'candidate_r5_api', 'call': 'R5_디자인적용검사.inspect(candidate,base=BASE)', 'valid': linked_candidate['valid']})
    assert linked_candidate['valid'], '실저장 R4에 대한 R5 후보 검사 실패'
    commit(R5, before[R5], candidates[R5], 'r5_write')
    report['final'] = {'r4': cli('after_r4', '자료검증.py', R4, True), 'r5': cli('after_r5', 'R5_디자인적용검사.py', R5)}
    assert all(x['exit_code'] == 0 and x['result']['valid'] for x in report['final'].values()), '저장 후 검사 실패'
    assert R4.read_bytes() == candidates[R4] and R5.read_bytes() == candidates[R5]
    assert diff(a, strict(R4.read_bytes())) == r4_diff and diff(b, strict(R5.read_bytes())) == r5_diff
    report['status'] = 'applied_structure_reference_pass'
    report['files'] = [{'path': str(path), 'id': strict(before[path]).get('record_id', strict(before[path]).get('application_id')), 'before_version': strict(before[path])['version'], 'after_version': strict(path.read_bytes())['version'], 'before_sha256': sha(before[path]), 'after_sha256': sha(path.read_bytes()), 'backup': str(OUT / 'backup' / path.relative_to(BASE)), 'backup_byte_equal': (OUT / 'backup' / path.relative_to(BASE)).read_bytes() == before[path]} for path in [R4, R5]]
    report['link_check'] = {'record_id_equal': updated_r5['linked_r4_record']['record_id'] == updated['record_id'], 'version_equal': updated_r5['linked_r4_record']['version'] == updated['version'], 'actual_saved_r4_sha256_equal': updated_r5['linked_r4_record']['sha256'] == sha(R4.read_bytes()), 'path_unchanged': True}
    report['preservation'] = {'allowed_diff_only': True, 'r4_schema_version_unchanged': True, 'tg_state_target_definition_unchanged': True, 'time_coordinates_numeric_values_company_color_review_status_unchanged': True, 'r5_own_version_unchanged_connection_only': True, 'canonical_and_manifest_writes': [], 'pending_review_fields_unchanged': True}
    report['recovery'] = {'needed': False, 'performed': False, 'reason': '저장/후검사 실패 없음'}
except Exception as error:
    report['status'] = 'failed'
    report['failure'] = {'type': type(error).__name__, 'message': str(error), 'traceback': traceback.format_exc()}
    events.append({'action': 'failure', **report['failure']})
    recovery = []
    for path in reversed(written):
        try:
            current = path.read_bytes()
            new(OUT / 'failed' / path.name, current)
            if current != candidates[path]:
                recovery.append({'path': str(path), 'status': 'external_change_do_not_overwrite'})
                continue
            stage = OUT / ('restore_' + path.name + '.stage')
            new(stage, before[path])
            assert path.read_bytes() == candidates[path]
            os.replace(stage, path)
            assert path.read_bytes() == before[path]
            recovery.append({'path': str(path), 'status': 'byte_restored', 'sha256': sha(path.read_bytes())})
        except Exception as restore_error:
            recovery.append({'path': str(path), 'status': 'restore_failed', 'error': str(restore_error)})
    report['recovery'] = recovery
finally:
    report['limitations'] = ['실제 영상·미디어·측정·회사/선택자 승인 검증 없음', 'R4 unresolved와 R5 human_review_queue는 검사 JSON에 원문 그대로 보존', 'R6/R7 full 자료가 생략된 사본이므로 full 현재성/연결 검사 미실시', '합성 spec_test/spec_example 범위이며 운영 등록/승인 아님', '다중 파일 원자 transaction·완전 동시성 제어를 주장하지 않음']
    report['events'] = events
    save_json('result.json', report)
    save_json('execution_log.json', events)
    success = report['status'] == 'applied_structure_reference_pass'
    text = ('두 초안에 실제 반영 완료. TG-STATE 단위 참조 0.9.9→0.1.0, R4 기록 판본 0.1.0→0.1.1. R5 연결 판본·실저장 R4 SHA만 갱신했으며 R5 자체 판본은 유지했습니다.\nR4/R5 저장 후 각각 CLI 종료 0·구조/참조 valid=true입니다. 변경 전 byte 일치 사본, 필드/텍스트 diff, 전후 검사 결과와 실행 로그를 outputs에 보존했습니다.\n' if success else '작업 실패 또는 일부 보류. result.json의 failure/recovery와 execution_log.json을 확인하세요.\n')
    text += '시간·좌표·수치·회사/색·검수 상태 및 다른 값은 허용 diff 비교로 보존 확인했습니다. 미정/사람 대기는 그대로이며 구조 통과는 내용 진실성·회사 승인·운영 완료가 아닙니다. R6/R7 full 검사는 자료 생략으로 미실시했습니다. 시간/token telemetry는 미수집입니다.\n'
    new(OUT / '결과설명.txt', text.encode('utf-8'))
    transcript = '# 실행 기록\n\n지정 task.txt, 수행사본_범위.json, video-record-steward 본문과 필요한 3개 참조를 읽고 지정 DB의 도구만 사용했습니다. 다른 run/스킬/평가/운영 D 자료/인터넷/영상 도구를 사용하지 않았습니다.\n\n초기 PowerShell 읽기 명령은 exit 0이었으나 세션 시작 시 다음 경고가 출력됐습니다: `Attempting to perform the InitializeDefaultDrives operation on the FileSystem provider failed.` 대상 파일 읽기는 성공했습니다.\n\n실행 명령: 지정 Python 실행파일에 `-B -X utf8 outputs/perform_update.py`; 코드와 실제 CLI 명령/종료코드/출력 경로는 execution_log.json에 보존했습니다. 후보 검사 API와 DB BASE도 그 로그에 남겼습니다.\n\n' + text + '\n각 실행/오류/복구 사건:\n\n```json\n' + json.dumps(events, ensure_ascii=False, indent=2) + '\n```\n'
    new(RUN / 'transcript.md', transcript.encode('utf-8'))
    print(json.dumps({'status': report['status'], 'result': str(OUT / 'result.json'), 'transcript': str(RUN / 'transcript.md')}, ensure_ascii=False))
    sys.exit(0 if success else 1)
