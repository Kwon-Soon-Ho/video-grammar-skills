"""Preserve the active development skill, publish the bounded update and archive PDF."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json,shutil,os,sys
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
ACTIVE=D/'Phase 01-A/03_분석스킬/company-video-grammar-analyzer'
STAGED=D/'Phase 01-A/03_분석스킬/draft8_준비_20261019'
BACKUP=D/'99_백업/2026-10-19_draft8_수정전'
PRIOR=BACKUP/'원본폴더/company-video-grammar-analyzer_draft7'
CANDIDATE=D/'Phase 01-A/03_분석스킬/수정후보/2026-10-19_draft8/company-video-grammar-analyzer'
RECORDS=D/'Phase 01-A/02_분석작업/2026-10-19_전체개요와_지도화살표_검수정정'
NOTICE=D/'Phase 01-A/00_진행안내/2026-10-19_스킬수정_현재작업본.md'
def digest(p):
    h=sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()
def load(p):return json.loads(Path(p).read_text('utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def copy(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists():assert digest(dst)==digest(src),dst
    else:
        with src.open('rb') as i,dst.open('xb') as o:shutil.copyfileobj(i,o)
    assert digest(src)==digest(dst)
    return {'source':str(src),'destination':str(dst),'sha256':digest(dst)}
for p in [ACTIVE,STAGED,BACKUP,PRIOR,CANDIDATE,RECORDS,NOTICE]:assert p.resolve().is_relative_to(D) and p.resolve()!=D
assert ACTIVE.is_dir() and not STAGED.exists() and not PRIOR.exists()
assert load(HERE/'validation/results.json')['all_passed'] and load(HERE/'report-qa.json')['visual_review']['state']=='passed'
prior_receipt=load(WORK/'analysis-reliability-20261019/publication-receipt.json')
for entry in prior_receipt['published_files']:
    assert digest(entry['source'])==entry['sha256'],entry['source']
    assert digest(entry['destination'])==entry['sha256'],entry['destination']
print('Prior 394 published files verified before update.',flush=True)
backup=load(HERE/'backup/manifest.json')
for entry in backup['files']:assert digest(ACTIVE/entry['relative'])==entry['sha256']
copy(HERE/'backup/draft7-before-coverage.zip',BACKUP/'draft7-before-coverage.zip');copy(HERE/'backup/manifest.json',BACKUP/'manifest.json')
oldfiles=[{'relative':p.relative_to(ACTIVE).as_posix(),'sha256':digest(p)} for p in ACTIVE.rglob('*') if p.is_file()]
operations=[]
for p in sorted(HERE.rglob('*')):
    if not p.is_file() or '__pycache__' in p.parts or p.name=='publication-receipt.json':continue
    rel=p.relative_to(HERE)
    dest=CANDIDATE/Path(*rel.parts[2:]) if rel.parts[0]=='candidate' else RECORDS/rel
    operations.append(copy(p,dest))
print('New evidence and candidate snapshot copied with hashes.',flush=True)
newfiles=[]
for p in (HERE/'candidate/company-video-grammar-analyzer').rglob('*'):
    if p.is_file() and '__pycache__' not in p.parts:
        rel=p.relative_to(HERE/'candidate/company-video-grammar-analyzer');copy(p,STAGED/rel);newfiles.append({'relative':rel.as_posix(),'sha256':digest(p)})
PRIOR.parent.mkdir(parents=True,exist_ok=True)
# Both resolved rename endpoints are checked above and inside the explicit project root.
os.rename(ACTIVE,PRIOR)
try:os.rename(STAGED,ACTIVE)
except BaseException:
    if not ACTIVE.exists():os.rename(PRIOR,ACTIVE)
    raise
for item in oldfiles:assert digest(PRIOR/item['relative'])==item['sha256']
for item in newfiles:assert digest(ACTIVE/item['relative'])==item['sha256']
if NOTICE.exists():copy(NOTICE,BACKUP/'진행안내_draft7.md')
notice='''# 분석 스킬 현재 작업본과 남은 범위

2026-10-19 갱신: 현재 이 프로젝트의 `03_분석스킬/company-video-grammar-analyzer`는 **0.1.0-draft.8 개발 작업본**이다. 전역 설치·최종 검증 완료가 아니다.

- 이전 draft.7 본체는 `99_백업/2026-10-19_draft8_수정전/원본폴더/company-video-grammar-analyzer_draft7`와 ZIP·SHA 목록으로 보존했다. draft.3·이전 후보·A5b 동결 실패 기록도 유지한다.
- 이번 변경: 공통 변환과 개별 등장 구분, 화살 모양과 실제 이동 구분, 원본 전체와 기록 창의 범위 집계. PG 줌 추정은 이전 문장을 기각으로 보존하고 실제 좌표 근거로 정정.
- 두 원본을 5초 개요 129장으로 훑어 잠정 작업 묶음 29개를 계획했다. 이 중 2개 묶음에 각각 8초 기록. 기록 창 밖 614.272초와 현재 창 안 미해결 5개가 남는다. 정밀 검수 완료율은 산정하지 않았다.
- 바로 다음: 노듈러 왼쪽 설명의 174초 이후 완성 상태, 배경·화살표의 연속 변화, PG 연결선 생성/퇴장·정책 강조 동기화를 보완한 뒤 미기록 묶음으로 확장.
- 전체 단계: 분석 신뢰성 보완 중 / 패턴 검색·재사용 일부 / 전문가 대안·비평은 문서·연결 형식 중심 / 편집 가능한 재제작·렌더 비교·내용 변경 검증 미구현.
- 새 기록: `02_분석작업/2026-10-19_전체개요와_지도화살표_검수정정/00_현재위치와_다음작업.md`. 제출 PDF는 `작업 보고서(pdf)/01_제출보고서/Phase 01-A/2026-10-19_전체개요와_지도화살표_검수정정`.

사용자 보고 지시: 중간에 멈추면 채팅에 현재 위치·바로 다음 단계·남은 양을 함께 적는다. 보고서 링크만 남기지 않는다.
'''
NOTICE.write_text(notice,encoding='utf-8')
rules=D/'AGENTS.md';copy(rules,BACKUP/'AGENTS.before-progress-report-policy.md');rules.write_bytes((WORK/'AGENTS.md').read_bytes());assert digest(rules)==digest(WORK/'AGENTS.md')
for entry in prior_receipt['published_files']:
    target=Path(entry['destination'])
    if target.resolve().is_relative_to(ACTIVE):target=PRIOR/target.resolve().relative_to(ACTIVE)
    elif target.resolve()==NOTICE.resolve():target=BACKUP/'진행안내_draft7.md'
    assert digest(target)==entry['sha256'],target
    assert digest(entry['source'])==entry['sha256']
print('draft.8 working copy active; prior bytes preserved.',flush=True)
sys.path.insert(0,str(WORK/'tools'))
from archive_pdf import archive_pdf
pdf=archive_pdf(WORK/'output/pdf/20261019_internal_video_scope_and_motion_correction.pdf',category='01_제출보고서/Phase 01-A/2026-10-19_전체개요와_지도화살표_검수정정',name='2026-10-19_사내영상_전체범위와_지도화살표_검수정정.pdf')
receipt={'utc':datetime.now(timezone.utc).isoformat(),'working_skill':str(ACTIVE),'working_version':'0.1.0-draft.8','prior_working_copy':str(PRIOR),'backup_zip':str(BACKUP/'draft7-before-coverage.zip'),'backup_zip_sha256':digest(BACKUP/'draft7-before-coverage.zip'),'old_working_files_preserved':oldfiles,'new_working_files':newfiles,'candidate_snapshot':str(CANDIDATE),'records':str(RECORDS),'current_notice':str(NOTICE),'prior_394_local_sources_unchanged':True,'prior_394_published_bytes_preserved':True,'published_files':operations,'published_file_count':len(operations),'pdf':pdf,'whole_research_completed':False,'whole_internal_video_analysis_complete':False,'global_skill_installed':False,'coverage':load(HERE/'coverage-result.json'),'tests':{'new':23,'core':38,'composition':34,'visual_accuracy_score':None},'project_rules_updated':True}
write(HERE/'publication-receipt.json',receipt);write(RECORDS/'publication-receipt.json',receipt)
assert digest(HERE/'publication-receipt.json')==digest(RECORDS/'publication-receipt.json')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['old_working_files_preserved','new_working_files','published_files','coverage']},ensure_ascii=False),flush=True)
