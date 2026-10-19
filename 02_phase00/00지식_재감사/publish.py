from pathlib import Path
import hashlib,json,shutil,datetime
R=Path(__file__).resolve().parent
W=Path('C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기')
PROJECT=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
DEST=PROJECT/'Phase 01-A/05_결과보고/2026-10-19_Phase00_지식연결_재감사'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.rstrip()+'\n',encoding='utf-8')
pins=json.loads((R/'data/protected-source-pins.json').read_text(encoding='utf-8'))
assert all(sha(Path(p['path']))==p['sha256'] for p in pins)
assert DEST.resolve().is_relative_to(PROJECT) and not DEST.exists(), 'new dedicated destination required'
DEST.mkdir(parents=True)
copied=[]
for f in sorted(R.rglob('*')):
    if not f.is_file() or '__pycache__' in f.parts:continue
    rel=f.relative_to(R)
    if rel.name=='publication-receipt.json':continue
    target=DEST/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
    assert sha(target)==sha(f)
    copied.append({'path':rel.as_posix(),'sha256':sha(f),'bytes':f.stat().st_size})
guide=f'''# 00 지식에서 분석 수집까지 — 최신 연결 안내

2026-10-19 추가 감사/인계다. 기존 정본·과거 보고서/평가·R6/R7/R8 pin을 수정하지 않았다.

- [핵심 결론과 읽는 순서](<{(DEST/'00_읽는순서와_현재상태.md').as_posix()}>)
- [권장 기록 구조·134/172초·모션 예](<{(DEST/'04_권장_기록구조.md').as_posix()}>)
- [00 전체 연결과 R4 이관 경계](<{(DEST/'05_R1-R8_연결과_수집계약.md').as_posix()}>)
- [문법별 목차와 실제 사용처](<{(DEST/'문법색인/00_읽는순서.md').as_posix()}>)

43원칙/8화면기준/14레이아웃은 유지할 참고 지식이며 전체 문법 DB를 대신하지 않는다. 현재 새 색인은 한 영상의 제한된 사용처에 대한 추가 조회 초안이다. 실제 사용판 draft.10, 후보 draft.12 보존. 정본 등록·기본판 교체·전편 수집·새 화면 제작은 수행하지 않았다. PDF 생성 없음.
'''
notices=[PROJECT/'Phase 00/00_분석단계_지식연결_추가안내.md',PROJECT/'Phase 00/09_다음단계인계/2026-10-19_분석단계_지식연결_추가안내.md',PROJECT/'Phase 01-A/00_진행안내/2026-10-19_Phase00_지식연결_재감사.md']
for p in notices:
    assert p.resolve().is_relative_to(PROJECT) and not p.exists()
    write(p,guide)
heading='## Phase 00 지식과 실제 수집의 연결'
block=f'''{heading}

2026-10-19 사용자 지시: 기존43원칙/8화면기준/14레이아웃을 정답으로 고정하지 않고 00의 스킬 조사/판면·표현·시간·근거/검수 지식을 실제 수집에 연결한다. 현재 안내는 `{(DEST/'00_읽는순서와_현재상태.md').as_posix()}`이며 R1–R8 연결과 조회 색인을 먼저 확인한다.

후속 수집은 필요한 기존 개념/조건/사례를 조회하고, 사례·구역·동작의 범위와 분류 이유·사용처·현재 근거/차이를 연결한다. 격자/정보관계 유형/표현언어/모션 역할/품질 질문을 같은 종류로 취급하지 않는다. 관측 태그와 기능 해석·검토 관련 원칙·실제 판정은 구분한다. 모든65원칙을 매 장면 의무 적용하거나 미관측 동작/원제작 의도/회사 승인을 만들지 않는다.

새 구조와 R4v0.2 이관은 검토/구현 후속이며 이 안내만으로 구현 완료라고 보고하지 않는다. 실제 분석기 draft.10과 후보 draft.12는 유지한다.
'''
backup=PROJECT/'99_백업/2026-10-19_Phase00_연결안내추가전'
root_changes=[]
for label,path in [('C작업공간',W/'AGENTS.md'),('D프로젝트',PROJECT/'AGENTS.md')]:
    old=path.read_bytes()
    assert heading not in old.decode('utf-8-sig')
    before=sha(path);bak=backup/(label+'_AGENTS.md')
    assert not bak.exists()
    bak.parent.mkdir(parents=True,exist_ok=True);bak.write_bytes(old)
    (R/'data'/('before_'+label+'_AGENTS.md')).write_bytes(old)
    text=old.decode('utf-8-sig').rstrip()+'\n\n'+block+'\n';path.write_text(text,encoding='utf-8')
    root_changes.append({'path':str(path),'before':before,'after':sha(path),'backup':str(bak)})
assert all(sha(Path(p['path']))==p['sha256'] for p in pins)
receipt={'published_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'destination':str(DEST),'files':copied,'notices':[str(p) for p in notices],'root_guidance':root_changes,'protected_source_pins_unchanged':True,'canonical_db_changed':False,'active_skill_replaced':False,'pdf_created':False}
for p in [R/'publication-receipt.json',DEST/'publication-receipt.json']:write(p,json.dumps(receipt,ensure_ascii=False,indent=2))
print(json.dumps({'destination':str(DEST),'copied_files':len(copied),'notices':len(notices),'protected_sources_unchanged':True},ensure_ascii=False))
