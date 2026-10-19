"""정적 읽기/hash 감사. 검사기·후보·시험을 실행하지 않으며 D에 쓰지 않는다."""
from pathlib import Path
import hashlib, json, re

BASE = Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
OUT = Path(__file__).resolve().parent
seen = {}
def raw(rel):
    p = BASE / rel
    value = p.read_bytes()
    seen[rel] = {'sha256': hashlib.sha256(value).hexdigest(), 'bytes':len(value)}
    return value
def obj(rel):
    return json.loads(raw(rel).decode('utf-8-sig'))

explicit = [
'06_맞춤스킬/video-record-steward/SKILL.md',
'06_맞춤스킬/video-record-steward/references/작업기준.md',
'09_다음단계인계/R4_통합규격_스킬호환_인계.md',
'09_다음단계인계/R7_R8_스킬재구성_인계.md',
'07_실행도구/R4_통합기록_사용안내.md',
'04_기록규격/06_통합최소기록_규격_v0.2.md',
'09_다음단계인계/R5_디자인연결_인계.md',
'09_다음단계인계/R6_검수연결_인계.md',
'09_다음단계인계/R7_사람판단과_남은준비.md',
'07_실행도구/자료검증.py',
'07_실행도구/R5_조회와적용_사용안내.md',
'13_품질검수/연결과인계/00_R7-4_진행안내.md',
'04_기록규격/07_구형기록_접수와이관규칙.md',
'07_실행도구/R7_연결확인.py',
'13_품질검수/연결과인계/01_현재기반과_연결범위.md',
'13_품질검수/연결과인계/연결방식_사용자결정.json',
'13_품질검수/연결과인계/03_검수와보류_연결규칙.md',
'07_실행도구/R6_통합조회.py',
'07_실행도구/R5_디자인적용검사.py',
'00_운영계약/정본과표시_연결목록.json',
'13_품질검수/연결과인계/04_연결확인_사용안내.md',
'14_스킬재구성/R8-2_기록관리자_구성안내.md',
]
for rel in explicit: raw(rel)
confirmation = obj('08_검증결과/R8_02_후보작성확인.json')
revision = obj('08_검증결과/R8_02_정적보완확인.json')
preservation = obj('08_검증결과/R8_02_입력보존.json')
candidate = {}
candidate_text = {}
for rel, expected in confirmation['candidate_files'].items():
    expected = revision['after_hashes'].get(rel,expected)
    value = raw(rel)
    candidate_text[rel] = value.decode('utf-8-sig')
    candidate[rel] = {'expected':expected, 'actual':seen[rel]['sha256'], 'matches':expected==seen[rel]['sha256']}
changed = {}
for rel, expected in preservation['source_hashes'].items():
    raw(rel)
    if seen[rel]['sha256'] != expected:
        changed[rel] = {'before':expected, 'after':seen[rel]['sha256']}
pins = obj('13_품질검수/연결과인계/현재연결_입력고정.json')
pin_failures=[]
for pin in pins['pins']:
    rel=pin['path'];raw(rel)
    if seen[rel]['sha256']!=pin['sha256']:pin_failures.append(rel)
missing_links=[]
for rel, text in candidate_text.items():
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if '://' not in target and not (BASE/rel).parent.joinpath(target).is_file():missing_links.append({'file':rel,'link':target})
revision_backup = {}
for p in (BASE/'backup/2026-10-15_R8_02_정적보완').rglob('*'):
    if p.is_file():
        rel = p.relative_to(BASE).as_posix();raw(rel)
        revision_backup[rel]=seen[rel]['sha256']
evidence = {
 'scope':'static file reads/hash comparisons only; no checker or task execution',
 'candidate_confirmation':candidate,
 'candidate_version':revision['candidate_version'],
 'revision_backup_hashes':revision_backup,
 'all_previous_candidate_bytes_found_in_revision_backup':all(v in revision_backup.values() for v in revision['before_hashes'].values()),
 'baseline_file_count':len(preservation['source_hashes']),
 'baseline_changed':changed,
 'baseline_changes_match_confirmation':changed==confirmation['prior_input_changes_only'],
 'old_skill_file_count':sum(rel.startswith('06_맞춤스킬/') and not rel.startswith('06_맞춤스킬/재구성후보/') for rel in preservation['source_hashes']),
 'old_skill_hash_failures':[rel for rel in changed if rel.startswith('06_맞춤스킬/') and not rel.startswith('06_맞춤스킬/재구성후보/')],
 'r7_static_pin_count':len(pins['pins']),
 'r7_static_pin_failures':pin_failures,
 'r7_live_checker_executed':False,
 'r6_live_checker_executed':False,
 'missing_candidate_markdown_links':missing_links,
 'D_files_read':seen,
}
(OUT/'R8_02_읽은D파일hash.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in evidence.items() if k!='D_files_read'},ensure_ascii=True))
