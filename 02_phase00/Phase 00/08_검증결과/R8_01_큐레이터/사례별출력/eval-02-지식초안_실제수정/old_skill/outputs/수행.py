from pathlib import Path
import sys, json, hashlib, copy, importlib.util, datetime
sys.dont_write_bytecode = True
RUN = Path(__file__).resolve().parents[1]
BASE = RUN / 'inputs' / 'Phase00'
OUT = RUN / 'outputs'
DRAFT = BASE / '작업초안/레이아웃지식_초안.json'
TARGET = 'KNOW-LAYOUT-SINGLE-FOCUS'
NEW_TEXT = '단일 초점이 반드시 중앙 배치를 뜻하는 것은 아님'
NEW_VERSION = '0.1.2-draft.1'
def digest(raw): return hashlib.sha256(raw).hexdigest()
def strict(raw):
    def pairs(items):
        d = {}
        for k,v in items:
            if k in d: raise ValueError('중복 키: '+k)
            d[k] = v
        return d
    def bad(x): raise ValueError('비유한 값: '+x)
    return json.loads(raw.decode('utf-8-sig'), object_pairs_hook=pairs, parse_constant=bad)
def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')
def diff(a,b,path=''):
    if type(a) is not type(b): return [{'path':path, 'before':a,'after':b}]
    if isinstance(a,dict):
        out=[]
        for k in a.keys() | b.keys():
            if k not in a or k not in b: out.append({'path':path+'/'+k,'before':a.get(k),'after':b.get(k)})
            else: out.extend(diff(a[k],b[k],path+'/'+k))
        return out
    if isinstance(a,list):
        if len(a)!=len(b): return [{'path':path,'before':a,'after':b}]
        return [d for i,(x,y) in enumerate(zip(a,b)) for d in diff(x,y,path+'/'+str(i))]
    return [] if a==b else [{'path':path,'before':a,'after':b}]
fixed = [
'02_원칙과레이아웃/레이아웃지식.json',
'01_공통용어/공통용어사전.json',
'05_출처와검토/출처목록.json',
'02_원칙과레이아웃/모션과정보전달원칙.json',
'02_원칙과레이아웃/화면설계원칙.json',
'03_한맥디자인/한맥디자인정본.json',
'04_기록규격/레이아웃지식_스키마.json',
'04_기록규격/공통용어_스키마.json',
'04_기록규격/출처목록_스키마.json',
'04_기록규격/원칙지식_스키마.json',
'07_실행도구/구형기록_보존검사.py'
]
before_hashes = {p:digest((BASE/p).read_bytes()) for p in fixed}
raw = DRAFT.read_bytes()
before = strict(raw)
assert len(before['layouts']) == 14
assert before['layouts'][0]['id'] == TARGET
assert before['layouts'][0]['limits'] == '반드시 중앙 배치 아님'
assert before['version'] == before['layouts'][0]['version'] == '0.1.1'
memo = strict((BASE/'입력메모.json').read_bytes())
assert before_hashes[memo['draft_parent']['path']] == memo['draft_parent']['sha256']
backup = RUN/'backup/2026-10-15_초안문구수정/레이아웃지식_초안_v0.1.1.json'
backup.parent.mkdir(parents=True, exist_ok=True)
assert not backup.exists(), '기존 백업 덮어쓰기 금지'
backup.write_bytes(raw)
assert backup.read_bytes() == raw
updated = raw.decode('utf-8')
old_phrase = '"limits": "반드시 중앙 배치 아님"'
assert updated.count(old_phrase) == 1
updated = updated.replace(old_phrase, '"limits": "'+NEW_TEXT+'"', 1)
updated = updated.replace('"version": "0.1.1"', '"version": "'+NEW_VERSION+'"', 2)
DRAFT.write_bytes(updated.encode('utf-8'))
after_raw = DRAFT.read_bytes()
after = strict(after_raw)
changes = sorted(diff(before,after), key=lambda x:x['path'])
expected = ['/layouts/0/limits','/layouts/0/version','/version']
assert [x['path'] for x in changes] == expected
assert after['layouts'][0]['limits'] == NEW_TEXT
assert before['layouts'][1:] == after['layouts'][1:]
# 기존 검사 모듈의 카탈로그 검사 함수에 레이아웃 읽기만 수정 초안으로 대체한다.
# 운영 정본 파일 또는 검사 코드에는 쓰지 않는다.
spec = importlib.util.spec_from_file_location('catalog_check', BASE/'07_실행도구/구형기록_보존검사.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
original_read = module.read
def draft_read(rel):
    return copy.deepcopy(after) if rel == '02_원칙과레이아웃/레이아웃지식.json' else original_read(rel)
module.read = draft_read
catalog_errors = module.validate_catalogs()
schema_errors = module.schema_errors(after, '레이아웃지식_스키마.json')
terms = original_read('01_공통용어/공통용어사전.json')
sources = original_read('05_출처와검토/출처목록.json')
target = after['layouts'][0]
term = next(x for x in terms['terms'] if x['id'] == target['term_id'])
refs = set(target['source_refs']+target.get('application_reference_refs',[]))
source_records = [{k:s.get(k) for k in ['id','kind','title','url','locator','review_status','limits']} for s in sources['sources'] if s['id'] in refs]
after_hashes = {p:digest((BASE/p).read_bytes()) for p in fixed}
assert before_hashes == after_hashes
versioned = OUT/'레이아웃지식_초안_v0.1.2-draft.1.json'
versioned.write_bytes(after_raw)
dump(OUT/'변경내역.json', {
 'scope':'요청한 초안 문구 정제. 운영 정본 반영 없음.',
 'draft_path':str(DRAFT), 'backup_path':str(backup), 'new_revision_path':str(versioned),
 'before_sha256':digest(raw),'after_sha256':digest(after_raw),
 'versions':{'before':'0.1.1','after':NEW_VERSION},
 'changes':changes,'other_layouts_unchanged':True,
 'status_policy':'초안 파일로 관리하며 기존 레코드 status와 나머지 항목은 유지. 승인 또는 회사 필수화 아님.',
 'meaning_review':'핵심 하나를 중심으로 구성한다는 정의를 유지하고, 중앙 배치가 필수라는 오해를 막는 동일 의미의 문구 정제.',
 'source_check':{'level':'로컬 용어·출처목록과 연결만 확인. 외부 원문 재검토·이론 신규 도입 없음.',
 'term':{k:term.get(k) for k in ['id','axis','name_ko','definition','status','replaced_by','source_refs']},
 'sources':source_records},
 'new_records':[],'deferred_records':[],'review_questions':[]
})
checks = {
 'performed':True,
 'valid':not schema_errors and not catalog_errors,
 'scope':'수정된 초안에 대한 JSON·스키마·카탈로그 ID/대체/분류축/관련항목/출처 연결 검사 및 변경 범위·바이트 불변 비교',
 'method':'기존 구형기록_보존검사.py의 schema_errors 및 validate_catalogs 함수 실행. read 함수의 레이아웃 입력만 수정 초안 객체로 대체. main/영상기록 진단 미실행.',
 'schema_errors':schema_errors,'catalog_errors':catalog_errors,
 'draft_reopened':True,'backup_byte_identical':True,'versioned_copy_byte_identical':versioned.read_bytes()==after_raw,
 'only_requested_text_and_version_changed':True,'other_13_layouts_identical':True,
 'source_parent_hash_matches_input_memo':True,
 'operational_files':{'unchanged':before_hashes==after_hashes,'before':before_hashes,'after':after_hashes},
 'not_performed':['R6 통합조회 전체 원문·CI 자산 검사','외부 원문·영상·시선·가독성·효과 검증','회사 규칙 승인·운영 반영','운영 조회문서 재생성'],
 'limits':['검사 함수는 기존 카탈로그의 구조와 연결을 검사하며 자연어 의미의 정답을 보증하지 않음.',
 '시험 사본에 포함되지 않은 외부 스킬 원문·CI 바이너리를 접근하거나 통과했다고 주장하지 않음.',
 '운영 정본과 조회문서는 미수정이며 수정 초안의 조회본만 outputs에 작성.']
}
dump(OUT/'확인결과.json', checks)
dump(OUT/'실제결과.json', {
 'status':'completed_draft_edit' if checks['valid'] else 'edited_with_validation_errors',
 'target_id':TARGET,'limits':NEW_TEXT,'draft_version':NEW_VERSION,
 'edited_draft':str(DRAFT),'backup':str(backup),'versioned_copy':str(versioned),
 'change_log':str(OUT/'변경내역.json'),'validation':str(OUT/'확인결과.json'),
 'readable_view':str(OUT/'초안조회.md'),
 'operational_release':False,'company_approved':False,'remaining_questions':[]
})
view = ['# 레이아웃 지식 초안 조회','',
'초안 판본: '+NEW_VERSION+' / 운영 정본 미반영',
'수정 초안 SHA256: '+digest(after_raw),'',
'| ID | 명칭 | 정의 | 적용 조건 | 한계 | 레코드 버전 |','|---|---|---|---|---|---|']
for x in after['layouts']:
    view.append('| '+' | '.join(str(x[k]).replace('|','\\|') for k in ['id','name_ko','definition','fit_conditions','limits','version'])+' |')
(OUT/'초안조회.md').write_text('\n'.join(view)+'\n', encoding='utf-8')
(OUT/'설명.md').write_text(
'초안의 KNOW-LAYOUT-SINGLE-FOCUS limits를 요청한 문구로 실제 수정했습니다. 파일 및 대상 항목 버전은 0.1.2-draft.1이며 나머지 13개 항목은 동일합니다.\n\n'
'수정 전 원본은 backup에 바이트 그대로 보존했습니다. 수정 파일에서 다시 읽어 비교했고 기존 검사 함수로 스키마와 카탈로그 연결을 확인했습니다. 검사 오류 '+str(len(schema_errors)+len(catalog_errors))+'개입니다.\n\n'
'운영 정본은 변경하지 않았습니다. R6 전체 원문·CI 자산 검사는 미실행이며 회사 승인·실영상 효과를 주장하지 않습니다. 변경내역.json과 확인결과.json, 초안조회.md에서 검토할 수 있습니다.\n', encoding='utf-8')
transcript = [
'# 수행 기록','',
'- 지정 task.txt, 실행스킬/SKILL.md, references/작업기준.md, 입력메모.json을 Get-Content -LiteralPath ... -Raw로 읽었다.',
'- 작업초안/레이아웃지식_초안.json, 02_원칙과레이아웃/레이아웃지식.json을 조회했다.',
'- 07_실행도구의 파일명 목록 및 자료검증.py, R3_레이아웃자료검사.py, R3_레이아웃도구안내.md, 지식조회.py, 구형기록_보존검사.py, 조회문서생성.py를 읽어 적용 범위를 확인했다.',
'- 05_출처와검토의 파일명 목록만 열거했으며 과거평가·실제 사례 내용은 열람하지 않았다.',
'- 04_기록규격/레이아웃지식_스키마.json 및 출처목록_스키마.json 첫 35줄을 조회했다.',
'',
'## 실제 실행 명령','',
"& 'D:\\00작업\\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\\Phase 00\\.환경\\Scripts\\python.exe' '"+str(OUT/'수행.py')+"'",
'',
'수행.py가 읽은 고정 운영 파일: '+', '.join(fixed),
'수행.py가 수정 전 백업 후 입력 초안 실제 파일에 쓰고, 파일을 다시 읽어 검증하고 결과 JSON/조회문서를 출력했다.',
'',
'## 실제 결과','',
'- 변경 JSON 경로: '+', '.join(x['path'] for x in changes),
'- 스키마 오류: '+str(schema_errors),
'- 기존 카탈로그 검사 함수 오류: '+str(catalog_errors),
'- 지정 11개 운영 파일 SHA256 전후 동일: '+str(before_hashes==after_hashes),
'- 백업 바이트 동일: True; 나머지 13개 레코드 동일: True.',
'',
'## 오류와 한계','',
'- PowerShell 호출 결과에 InitializeDefaultDrives / FileSystem provider 초기화 경고가 매번 있었으나 조회 명령은 exit_code 0과 파일 본문을 반환했다.',
'- 자료검증.py --record는 영상 통합기록용이므로 지식 초안 파일에 실행하지 않았다. 레이아웃 R3 검사는 심화 지식·미포함 외부 원문을 요구하므로 실행하지 않았다.',
'- 기존 구형기록 보존 모듈 전체 CLI 통과가 아니라 해당 모듈의 카탈로그 검사 함수 실행 결과만 보고한다.',
'- 운영 조회문서 생성기는 CI 자산도 읽고 운영 파일에 쓰므로 실행하지 않았다. 초안에서 읽기용 문서를 outputs에 새로 만들었다.',
'- 외부 네트워크/API/AE/CU/설치, 시험 루트 외 자료, 06/08 과거평가 열람은 수행하지 않았다.',
'- 시간·토큰 계측은 수행하지 않았으며 수치를 만들지 않았다. 자기채점 없음.',
]
(RUN/'transcript.md').write_text('\n'.join(transcript)+'\n', encoding='utf-8')
print(json.dumps({'status':'completed_draft_edit' if checks['valid'] else 'edited_with_validation_errors','changes':changes,'schema_errors':schema_errors,'catalog_errors':catalog_errors,'canonical_unchanged':True,'outputs':str(OUT)}, ensure_ascii=True))
raise SystemExit(0 if checks['valid'] else 1)

