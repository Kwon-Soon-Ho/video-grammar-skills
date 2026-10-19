import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent.parent
BASE = RUN / 'inputs' / 'Phase00'
OUT = RUN / 'outputs'
TARGET = '작업초안/쉬운말_지식카드.json'
TERMS = {'LAYOUT-PROCESS-LINE', 'FUNCTION-FOCUS', 'PROPERTY-VISIBILITY'}
FILES = [
    '실행스킬/video-knowledge-curator/SKILL.md',
    '실행스킬/video-knowledge-curator/references/작업기준.md',
    '실행스킬/video-knowledge-curator/references/출력지침.md',
    '00_운영계약/01_보존과버전_계약.md',
    '00_운영계약/정본과표시_연결목록.json',
    '14_스킬재구성/R8_현재사용안내.md',
    '14_스킬재구성/현재상태_정정표.json',
    '01_공통용어/공통용어사전.json',
    '01_공통용어/분류운영규칙.json',
    '01_공통용어/용어판정기준.json',
    '02_원칙과레이아웃/레이아웃지식.json',
    '02_원칙과레이아웃/레이아웃_심화지식.json',
    '02_원칙과레이아웃/07_레이아웃별_선택조건과반례.md',
    TARGET,
    '작업초안/연결목록.json',
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def safe(rel):
    path = (BASE / rel).resolve()
    if not path.is_relative_to(BASE.resolve()):
        raise ValueError(f'outside input: {rel}')
    return path

manifest = {}
payloads = {}
for rel in FILES:
    path = safe(rel)
    raw = path.read_bytes()
    manifest[rel] = {'sha256': sha(raw), 'bytes': len(raw)}
    payloads[rel] = raw.decode('utf-8-sig')

# Read precisely the correction originals and bases supplied in this copy.
errata = json.loads(payloads['14_스킬재구성/현재상태_정정표.json'])
checks = []
for correction in errata['records']:
    entries = [('source', correction['source'])] + [('basis', b) for b in correction['basis']]
    checked = []
    for role, entry in entries:
        path = safe(entry['path'])
        if not path.is_file():
            checked.append({'role': role, 'path': entry['path'], 'exists': False, 'match': False})
            continue
        raw = path.read_bytes()
        actual = sha(raw)
        manifest.setdefault(entry['path'], {'sha256': actual, 'bytes': len(raw)})
        payloads.setdefault(entry['path'], raw.decode('utf-8-sig'))
        checked.append({'role': role, 'path': entry['path'], 'exists': True, 'expected_sha256': entry['sha256'], 'actual_sha256': actual, 'match': actual == entry['sha256']})
    checks.append({'id': correction['id'], 'status': 'confirmed_bounded_current_stage_correction' if all(c['match'] for c in checked) else 'hold_this_correction', 'scope': correction['scope'], 'files': checked})

write_json(OUT / '입력_SHA_작업시작.json', manifest)
write_json(OUT / '정정별_원문과근거_SHA검사.json', checks)

print('READ SCOPE: only explicit inputs/Phase00 files; no external DB, evaluation criteria, network or source code execution.')
for rel in FILES:
    print(f'\nFILE {rel}\nSHA256 {manifest[rel]["sha256"]}\nBYTES {manifest[rel]["bytes"]}')
    text = payloads[rel]
    if rel.endswith('공통용어사전.json'):
        doc = json.loads(text)
        print(json.dumps({'taxonomy_id': doc.get('taxonomy_id'), 'version': doc.get('version'), 'authority': doc.get('authority'), 'axes': doc.get('axes'), 'terms': [t for t in doc['terms'] if t['id'] in TERMS], 'source_metadata': {k: v for k, v in doc.items() if k not in {'terms', 'axes'}}}, ensure_ascii=False, indent=2))
    elif rel.endswith(('레이아웃지식.json', '레이아웃_심화지식.json')):
        doc = json.loads(text)
        print('ROOT KEYS', list(doc))
        print('ROOT METADATA', json.dumps({k: v for k, v in doc.items() if not isinstance(v, (dict, list))}, ensure_ascii=False))
        def find(obj, location='$'):
            if isinstance(obj, dict):
                direct = {k: v for k, v in obj.items() if isinstance(v, str)}
                if any('LAYOUT-PROCESS-LINE' == v or '선형 프로세스' == v for v in direct.values()):
                    print('SELECTED', location, json.dumps(obj, ensure_ascii=False, indent=2))
                for k, v in obj.items():
                    find(v, location + '/' + k)
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    find(v, location + '/' + str(i))
        find(doc)
    elif rel.endswith('07_레이아웃별_선택조건과반례.md'):
        sections = text.split('\n## ')
        print(sections[0])
        for section in sections[1:]:
            if section.split('\n', 1)[0].find('LAYOUT-PROCESS-LINE') >= 0:
                print('\n## ' + section)
    elif rel.endswith('정본과표시_연결목록.json'):
        doc = json.loads(text)
        selected = [c for c in doc.get('canonical_entries', []) if c.get('path') in FILES or '쉬운말_지식카드' in c.get('path', '')]
        print(json.dumps({'version': doc['version'], 'selected_canonical_entries': selected, 'target_registered_in_canonical_entries': any('쉬운말_지식카드' in c.get('path', '') for c in doc.get('canonical_entries', [])), 'display_groups_for_target': [g for g in doc.get('display_groups', []) if '쉬운말_지식카드' in json.dumps(g, ensure_ascii=False)]}, ensure_ascii=False, indent=2))
    else:
        print(text)

print('\nCORRECTION CHECKS')
print(json.dumps(checks, ensure_ascii=False, indent=2))
for rel in dict.fromkeys(item['path'] for c in checks for item in c['files'] if item.get('exists')):
    print(f'\nCORRECTION SOURCE/BASIS CONTENT {rel}')
    text = payloads[rel]
    if rel.endswith('자료검증.py'):
        # Source inspected; never imported or executed. Show root, entry point and validator declarations.
        lines = text.splitlines()
        hits = set()
        needles = ('BASE', '__main__', 'argparse', 'def validate_catalogs', 'def main', 'validate_integrated')
        for i, line in enumerate(lines):
            if any(n in line for n in needles):
                hits.update(range(max(0, i-2), min(len(lines), i+9)))
        for i in sorted(hits):
            print(f'{i+1}: {lines[i]}')
        print('READ DEPTH: selected source excerpts; no existing validator executed.')
    elif rel not in FILES:
        print(text)

guide_refs = ['01_진행현황.md', '08_검증결과/R8_04_통합검증/00_최종보고.md', '07_실행도구/R6_통합조회.py', '07_실행도구/R7_연결확인.py', '07_실행도구/지식조회.py']
missing_checked = [{'path': rel, 'exists_in_copy': safe(rel).is_file()} for rel in guide_refs]
write_json(OUT / '참조범위_존재확인.json', missing_checked)
print('\nEXPLICIT REFERENCED PATH PRESENCE', json.dumps(missing_checked, ensure_ascii=False))
print('\nINSPECTION COMPLETE. No input changed. SHA manifest is file identity, not content or company approval.')
