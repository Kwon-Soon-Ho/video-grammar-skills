from pathlib import Path
import json,hashlib,shutil,datetime,subprocess
R=Path(__file__).resolve().parent;W=R.parent
PROJECT=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.rstrip()+'\n',encoding='utf-8')
def files(base):return {f.relative_to(base).as_posix():sha(f) for f in sorted(base.rglob('*')) if f.is_file() and '__pycache__' not in f.parts}
new=R/'candidate/company-video-grammar-analyzer';old=R/'backup/draft12/company-video-grammar-analyzer'
candidate=read(R/'candidate-manifest.json');assert files(new)==candidate
previous=read(W/'collection-skill-structure-20261019/publication-receipt.json');dold=Path(previous['stage'])/'company-video-grammar-analyzer';assert files(dold)==files(old)
pins=read(R/'protected-before.json');assert all(sha(Path(p['path']))==p['sha256'] for p in pins)
for p in (R/'company-video-grammar-analyzer-workspace/iteration-4').glob('eval-*'):
    for config in ['with_skill','old_skill']:assert (p/config/'grading.json').is_file()
tag=hashlib.sha256(json.dumps(candidate,sort_keys=True).encode()).hexdigest()[:12]
backup=PROJECT/'99_백업/2026-10-19_draft12_00지식연결전'/tag
stage=PROJECT/'Phase 01-A/03_분석스킬/후보보관'/('2026-10-19_draft13_'+tag)/'company-video-grammar-analyzer'
dest=PROJECT/'Phase 01-A/05_결과보고/2026-10-19_draft13_00지식연결'
for p in [backup,stage,dest]:assert p.resolve().is_relative_to(PROJECT) and not p.exists(),str(p)
shutil.copytree(dold,backup/'company-video-grammar-analyzer');shutil.copytree(new,stage)
shutil.copy2(dold.parent/'publication-receipt.json',backup/'draft12-publication-receipt.json')
assert files(backup/'company-video-grammar-analyzer')==files(old) and files(stage)==candidate
copied=[]
dest.mkdir(parents=True)
for f in sorted(R.rglob('*')):
    if not f.is_file() or '__pycache__' in f.parts or f.name=='publication-receipt.json':continue
    rel=f.relative_to(R);target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
    assert sha(target)==sha(f);copied.append({'path':rel.as_posix(),'sha256':sha(f)})
notice=PROJECT/'Phase 01-A/00_진행안내/2026-10-19_draft13_00지식연결.md'
write(notice,f'''# draft.13 후보 — 00 지식 연결

사용자 선택에 따라 draft.12 백업 후 00 지식 조회→사례→사용처→검수 연결을 별도 draft.13 후보에 구현했다. 실제 사용판 draft.10과 기존 후보/정본은 유지한다.

- [현재 결과와 읽는 순서](<{(dest/'00_현재결과와_읽는순서.md').as_posix()}>)
- [원본134초 연결 기록](<{(dest/'pilot/case-134.md').as_posix()}>) / [172초](<{(dest/'pilot/case-172.md').as_posix()}>) / [모션6창](<{(dest/'pilot/motion-windows.md').as_posix()}>)
- [실제 실행 비교](<{(dest/'review.html').as_posix()}>) / [정정과 평가 한계](<{(dest/'03_실행결과_정정과_평가한계.md').as_posix()}>)

후보: `{stage}`. 백업: `{backup}`. PDF/새 화면·영상/전편 확장/회사 승인/R4정본 자동 이관은 수행하지 않았다.
''')
handoff=PROJECT/'Phase 00/09_다음단계인계/2026-10-19_draft13_분석기_지식연결.md'
assert not handoff.exists()
write(handoff,notice.read_text(encoding='utf-8'))
heading='## draft.13 지식 연결 후보의 현재 범위'
block=f'''{heading}

2026-10-19 사용자 선택으로 draft.12 백업 후 draft.13 후보에 00 조회→사례 기록→사용처→검수 연결을 구현했다. 현재 안내는 `{(dest/'00_현재결과와_읽는순서.md').as_posix()}`. 위의 ‘후보draft.12 유지’는 당시 감사 상태이며 최신 개발 후보는 별도draft.13이다. 실제 사용판은 draft.10 유지, 전편 확장/정본 등록/기본판 교체는 보류한다.

지식 분류·정의·사용처·검토 관련성·실제 판정을 구분하고 원본/기존 실패 기록을 보존한다. 새 연결 검사는 R4통합v0.2 적합성·시각 진실성·회사 승인 검사가 아니다. 같은 영상2과제의 점수와 자기보고/판본 설명 오류를 분리해 읽고 사용자 검토 결과를 받은 뒤 다음 묶음을 선택한다.
'''
root_changes=[]
for label,p in [('C작업공간',W/'AGENTS.md'),('D프로젝트',PROJECT/'AGENTS.md')]:
    before=p.read_bytes();assert heading not in before.decode('utf-8-sig')
    bak=backup/(label+'_AGENTS.md');bak.write_bytes(before)
    write(p,before.decode('utf-8-sig').rstrip()+'\n\n'+block)
    root_changes.append({'path':str(p),'before':hashlib.sha256(before).hexdigest(),'after':sha(p),'backup':str(bak)})
assert all(sha(Path(p['path']))==p['sha256'] for p in pins)
receipt={'client_date':'2026-10-19','published_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'report':str(dest),'candidate':str(stage),'backup':str(backup),'files':copied,'notices':[str(notice),str(handoff)],'root_guidance':root_changes,'protected_sources_unchanged':True,'active_version':'draft.10','candidate_version':'draft.13','canonical_registered':False,'whole_video_expansion':False,'pdf_created':False}
for p in [R/'publication-receipt.json',dest/'publication-receipt.json']:write(p,json.dumps(receipt,ensure_ascii=False,indent=2))
print(json.dumps({'report':str(dest),'candidate':str(stage),'backup':str(backup),'files':len(copied),'active_draft10_unchanged':True},ensure_ascii=False))
