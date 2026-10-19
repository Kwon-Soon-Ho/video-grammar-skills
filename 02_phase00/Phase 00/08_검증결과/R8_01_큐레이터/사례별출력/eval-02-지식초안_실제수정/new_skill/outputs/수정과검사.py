from pathlib import Path
import json, hashlib, re, difflib, importlib.util, copy
from jsonschema import Draft202012Validator

RUN = Path(__file__).resolve().parents[1]
BASE = RUN / 'inputs' / 'Phase00'
OUT = RUN / 'outputs'
TARGET = BASE / '작업초안/레이아웃지식_초안.json'
ID = 'KNOW-LAYOUT-SINGLE-FOCUS'
OLD = '반드시 중앙 배치 아님'
NEW = '단일 초점이 반드시 중앙 배치를 뜻하는 것은 아님'

def sha(raw): return hashlib.sha256(raw).hexdigest()
def strict(raw):
    def pairs(rows):
        obj = {}
        for k, v in rows:
            if k in obj: raise ValueError('중복 JSON key: ' + k)
            obj[k] = v
        return obj
    return json.loads(raw.decode('utf-8-sig'), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
def read(rel): return strict((BASE / rel).read_bytes())
def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')
def load_tool(name):
    p = BASE / '07_실행도구' / name
    spec = importlib.util.spec_from_file_location('curator_'+name.replace('.py',''), p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

protected = [
 '00_운영계약/정본과표시_연결목록.json', '00_운영계약/01_보존과버전_계약.md',
 '01_공통용어/공통용어사전.json', '02_원칙과레이아웃/레이아웃지식.json',
 '02_원칙과레이아웃/레이아웃_심화지식.json', '02_원칙과레이아웃/화면설계원칙.json',
 '02_원칙과레이아웃/모션과정보전달원칙.json', '02_원칙과레이아웃/07_레이아웃별_선택조건과반례.md',
 '03_한맥디자인/한맥디자인정본.json', '05_출처와검토/출처목록.json',
 '04_기록규격/레이아웃지식_스키마.json', '04_기록규격/공통용어_스키마.json',
 '04_기록규격/출처목록_스키마.json', '04_기록규격/원칙지식_스키마.json',
 '07_실행도구/자료검증.py', '07_실행도구/구형기록_보존검사.py', '입력메모.json'
]
protected_before = {p: sha((BASE/p).read_bytes()) for p in protected}
original = TARGET.read_bytes()
before = strict(original)
assert before['version'] == '0.1.1'
assert sum(r['id'] == ID for r in before['layouts']) == 1
row = next(r for r in before['layouts'] if r['id'] == ID)
assert row['limits'] == OLD and row['version'] == '0.1.1'
parent = read('02_원칙과레이아웃/레이아웃지식.json')
parent_raw = (BASE/'02_원칙과레이아웃/레이아웃지식.json').read_bytes()
memo_parent = read('입력메모.json')['draft_parent']
assert parent['version'] == memo_parent['version'] == '0.1.1'
assert sha(parent_raw) == memo_parent['sha256']
manifest = read('00_운영계약/정본과표시_연결목록.json')
entry = next(x for x in manifest['canonical_entries'] if x['path'] == memo_parent['path'])
assert entry['version'] == parent['version'] and entry['sha256'] == sha(parent_raw)
assert before == parent
registered = any(x.get('path','').replace('\\','/') == '작업초안/레이아웃지식_초안.json' for x in manifest['canonical_entries'])
assert not registered

backup = OUT/'backup/지식문구수정_01/레이아웃지식_초안_v0.1.1.json'
backup.parent.mkdir(parents=True, exist_ok=True)
with backup.open('xb') as f: f.write(original)
assert backup.read_bytes() == original
backup_hash = sha(backup.read_bytes())

# UTF-8 인코딩, BOM, 줄바꿈 및 비대상 바이트는 유지한다.
text = original.decode('utf-8')
assert text.count('"limits": "'+OLD+'"') == 1
text = text.replace('"limits": "'+OLD+'"', '"limits": "'+NEW+'"', 1)
text, n1 = re.subn(r'("version"\s*:\s*")0\.1\.1(")', r'\g<1>0.1.2\2', text, count=1)
pattern = r'("id"\s*:\s*"KNOW-LAYOUT-SINGLE-FOCUS"(?:(?!"id"\s*:).)*?"version"\s*:\s*")0\.1\.1(")'
text, n2 = re.subn(pattern, r'\g<1>0.1.2\2', text, count=1, flags=re.S)
assert n1 == n2 == 1
candidate_raw = text.encode('utf-8')
candidate = strict(candidate_raw)
expected = copy.deepcopy(before)
expected['version'] = '0.1.2'
expected_row = next(x for x in expected['layouts'] if x['id'] == ID)
expected_row.update(limits=NEW, version='0.1.2')
assert candidate == expected

# 기존 목록 검사에 layout 입력만 메모리 대체한다. 정본 파일은 쓰지 않는다.
legacy = load_tool('구형기록_보존검사.py')
entrypoint = load_tool('자료검증.py')
canonical_errors = entrypoint.validate_catalogs()
original_catalogs = legacy.catalogs
catalogs = original_catalogs()
def candidate_catalogs(): return (*catalogs[:4], candidate, catalogs[5])
legacy.catalogs = candidate_catalogs
candidate_errors = legacy.validate_catalogs()
legacy.catalogs = original_catalogs
schema = read('04_기록규격/레이아웃지식_스키마.json')
Draft202012Validator.check_schema(schema)
schema_errors = [str(list(e.path))+': '+e.message for e in Draft202012Validator(schema).iter_errors(candidate)]
assert not canonical_errors, canonical_errors
assert not candidate_errors, candidate_errors
assert not schema_errors, schema_errors

# 검사한 후보 바이트를 지정 초안에 저장하고 새 판본 사본도 남긴다.
TARGET.write_bytes(candidate_raw)
versioned = OUT/'레이아웃지식_초안_v0.1.2.json'
with versioned.open('xb') as f: f.write(candidate_raw)
after_raw = TARGET.read_bytes()
after = strict(after_raw)
assert after == expected and after_raw == candidate_raw == versioned.read_bytes()
assert backup.read_bytes() == original
post_catalogs = (*catalogs[:4], after, catalogs[5])
legacy.catalogs = lambda: post_catalogs
post_errors = legacy.validate_catalogs()
legacy.catalogs = original_catalogs
assert not post_errors, post_errors
protected_after = {p: sha((BASE/p).read_bytes()) for p in protected}
assert protected_before == protected_after

patch = ''.join(difflib.unified_diff(original.decode('utf-8-sig').splitlines(True),
            after_raw.decode('utf-8-sig').splitlines(True),
            fromfile='작업초안/레이아웃지식_초안.json (v0.1.1)',
            tofile='작업초안/레이아웃지식_초안.json (v0.1.2)'))
(OUT/'변경.diff').write_text(patch, encoding='utf-8')
changes = [
 {'path':'/version','before':'0.1.1','after':'0.1.2'},
 {'path':'/layouts/0/limits','id':ID,'before':OLD,'after':NEW},
 {'path':'/layouts/0/version','id':ID,'before':'0.1.1','after':'0.1.2'}
]
result = {
 'status':'draft_modified_and_narrow_checks_passed',
 'requested_target':'작업초안/레이아웃지식_초안.json', 'target_id':ID,
 'actual_modified_file':str(TARGET), 'versioned_copy':str(versioned),
 'before':{'file_version':'0.1.1','item_version':'0.1.1','sha256':sha(original)},
 'after':{'file_version':after['version'],'item_version':after['layouts'][0]['version'],'sha256':sha(after_raw)},
 'backup':{'path':str(backup),'sha256':backup_hash,'identical_to_original':True},
 'parent':memo_parent, 'parent_bytes_match_input_memo_and_canonical_manifest':True,
 'changes':changes, 'diff_file':str(OUT/'변경.diff'),
 'checks':{
   'strict_json_parse_before_and_after':True, 'duplicate_json_keys':False,
   'layout_count':len(after['layouts']), 'duplicate_layout_ids':len({x['id'] for x in after['layouts']})!=len(after['layouts']),
   'exact_expected_object_and_only_allowed_byte_replacements':True,
   'all_other_items_unchanged':before['layouts'][1:]==after['layouts'][1:],
   'target_id_status_sources_related_ids_company_examples_unchanged':all(row[k]==after['layouts'][0][k] for k in row if k not in ('limits','version')),
   'existing_validate_catalogs_original_canonical':{'executed':True,'errors':canonical_errors},
   'existing_validate_catalogs_candidate_in_memory':{'executed':True,'errors':candidate_errors},
   'layout_json_schema_candidate':{'executed':True,'errors':schema_errors},
   'existing_validate_catalogs_saved_draft_in_memory':{'executed':True,'errors':post_errors},
   'saved_draft_matches_versioned_copy':True,
   'protected_file_hashes':{p:{'before':protected_before[p],'after':protected_after[p],'unchanged':True} for p in protected}
 },
 'meaning_review':{
  'basis':'기존 limits의 생략된 주어를 명시한 문장 정리. 단일 초점은 중앙 배치를 의무화하지 않는다는 의미 유지.',
  'deep_card':'02_원칙과레이아웃/레이아웃_심화지식.json#layout_cards/KNOW-LAYOUT-SINGLE-FOCUS',
  'read_depth':'로컬 대상 카드 전체 및 07_레이아웃별_선택조건과반례.md 단일 초점 절. 외부 원문/실제 영상 미열람.',
  'composition_decisions':'초점 위치는 중앙·삼분할 모두 후보다.',
  'example_and_counterexample_role':'기존 심화지식의 설명용 사례만 대조; 새 실제 사례·효과·관측을 생성하지 않음.'
 },
 'operational_release':False, 'canonical_modified':False,
 'registration':{'registered_in_operational_manifest':registered,'action':'미등록 초안 상태 유지. 정본 등록/기본 전환/생성문서 갱신 없음.'},
 'not_executed':[
  'R3_레이아웃자료검사 전체: 외부 스킬 원문·사본 밖 경로를 읽으므로 실행하지 않음.',
  'R4 영상기록 검사: 이 파일은 지식 초안이므로 대상 아님.',
  'R6 통합 조회 전체 원문/자산 검사 및 R7 연결검사: 이 초안 수정 검증으로 주장하지 않음.',
  '영상 분석, AE/CU, 외부 네트워크/API, 설치, 사람 검수·회사 승인, 운영 정본 반영'
 ],
 'source_limits':'출처목록의 기존 ID/권한 선언을 로컬에서 확인. 외부 원문 본문·권리·회사 승인·실제 영상 효과 검증 아님.',
 'questions':[], 'token_usage':None, 'total_elapsed_time':None
}
write_json(OUT/'실제결과.json', result)
(OUT/'설명.md').write_text(
 '# 초안 문구 수정 결과\n\n'
 '지정 초안의 KNOW-LAYOUT-SINGLE-FOCUS limits를 “단일 초점이 반드시 중앙 배치를 뜻하는 것은 아님”으로 실제 저장했습니다. '
 '파일과 해당 항목 버전은 0.1.1 → 0.1.2로 구분했으며 다른 13개 항목·상태·출처·ID는 유지했습니다.\n\n'
 'backup 바이트 일치, JSON 파싱·중복 키/ID, 기존 지식 목록 검사(후보를 메모리로 대입), 레이아웃 스키마, 허용 diff, 저장 후 재검사를 실행했습니다. '
 '기존 검사 오류는 0개이고 보호한 17개 파일의 전후 SHA가 같습니다. 자세한 값은 실제결과.json, 변경 내용은 변경.diff에 있습니다.\n\n'
 '이 초안은 운영 연결목록 미등록 상태이며 정본/기본 전환은 하지 않았습니다. R3 전체 외부 원문, R4 영상 기록, R6 전체 원문·자산, R7 및 사람 검수·회사 승인은 수행하지 않았습니다. '
 '외부 원문을 새로 읽거나 실제 영상 효과를 검증했다는 뜻이 아닙니다.\n', encoding='utf-8')
print(json.dumps({'status':result['status'],'target':str(TARGET),'before_sha256':sha(original),'after_sha256':sha(after_raw),
 'backup_sha256':backup_hash,'changed_fields':changes,'checks_error_count':len(canonical_errors)+len(candidate_errors)+len(schema_errors)+len(post_errors),
 'protected_files_unchanged':len(protected),'outputs':['실제결과.json','설명.md','변경.diff','레이아웃지식_초안_v0.1.2.json']}, ensure_ascii=True, indent=2))
