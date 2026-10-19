from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,zipfile,sys
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
DEST=D/'Phase 01-A/02_분석작업/2026-10-19_전체디자인_기록보강'
ACTIVE=D/'Phase 01-A/03_분석스킬/company-video-grammar-analyzer'
BACK=D/'99_백업/2026-10-19_draft9_수정전'
NOTICE=D/'Phase 01-A/00_진행안내/2026-10-19_스킬수정_현재작업본.md'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def copy(s,d):
 d.parent.mkdir(parents=True,exist_ok=True)
 if d.exists():assert sha(s)==sha(d),'existing different file: '+str(d)
 else:
  with s.open('rb') as a,d.open('xb') as b:shutil.copyfileobj(a,b)
 assert sha(s)==sha(d)
 return {'source':str(s),'destination':str(d),'sha256':sha(d)}
for p in [DEST,ACTIVE,BACK,NOTICE]:assert p.resolve().is_relative_to(D) and p.resolve()!=D
assert load(OUT/'validation.json')['passed'] and load(OUT/'report-qa.json')['visual_review']['state']=='passed'
oldfiles=load(OUT/'inputs.json')['draft8_source_files']
for f in oldfiles:assert sha(ACTIVE/f['relative'])==f['sha256']
prior=load(ROOT/'case-benchmarks-20261019/publication-receipt.json')
for f in prior['published_files']:assert sha(f['source'])==sha(f['destination'])==f['sha256']
backupfiles=[]
for f in oldfiles:backupfiles.append(copy(ACTIVE/f['relative'],BACK/'원본폴더/company-video-grammar-analyzer_draft8'/f['relative']))
zipdest=BACK/'draft8-before-design-density.zip'
if not zipdest.exists():
 with zipfile.ZipFile(zipdest,'x',compression=zipfile.ZIP_DEFLATED) as z:
  for f in oldfiles:z.write(ACTIVE/f['relative'],arcname='company-video-grammar-analyzer/'+f['relative'])
with zipfile.ZipFile(zipdest) as z:
 for f in oldfiles:assert hashlib.sha256(z.read('company-video-grammar-analyzer/'+f['relative'])).hexdigest()==f['sha256']
copy(NOTICE,BACK/'진행안내_draft8_디자인보강전.md')
print('draft8 backed up as folder and verified ZIP before active writes',flush=True)
candidate=OUT/'candidate/company-video-grammar-analyzer';newfiles=[]
oldmap={f['relative']:f for f in oldfiles}
for p in candidate.rglob('*'):
 if not p.is_file() or '__pycache__' in p.parts:continue
 rel=p.relative_to(candidate).as_posix();target=ACTIVE/rel
 if target.exists():assert rel in oldmap and sha(target)==oldmap[rel]['sha256']
 target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);assert sha(p)==sha(target)
 newfiles.append({'relative':rel,'sha256':sha(target)})
operations=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts and p.name!='publication-receipt.json':operations.append(copy(p,DEST/p.relative_to(OUT)))
print('draft9 active working copy and design records copied with hash checks',flush=True)
NOTICE.write_text('''# 분석 스킬 현재 작업본

2026-10-19 전체 디자인 기록 보강: **0.1.0-draft.9 개발 작업본**. 이전 draft.8은99_백업/2026-10-19_draft9_수정전에 원본 폴더와검증 ZIP으로 보존.

- 사용자 선택: 현재 패턴 분류 유지, 글자 크기 관계·영역 비율·여백·프레임/선/배경층 보강. 수치는 재사용에 필요한 관계부터 측정.
- 두 사례 새판본·디자인 상세 파일, 원본 크기 ROI/수치/방법·오차·시점 기록. 기존 패턴18개/연결 번호·정의 해시 유지. 폰트 원값/opacity/AE설정은 미확정.
- 새 발견: PG47→53초 정책 패널은약85%크기,카드 크기는 유사. 전체 묶음 이동과 하위 패널 크기 변화를 분리. 정확 축소 시작/가감속은 새 열린 쟁점. 기존 노듈러 화살표 강도/원본 동기화 쟁점도 남음.
- 상세 기록 창28초,창 밖602.272초(약10분2초). 이번 보강은 연속 분석 시간 확장이 아님. 다른2~3장면 적용·전문가 판단·재제작 검증은 남음.
- 새52개 검사는 구조/출처/수치 일관성/오류 거부/보존 확인이며 영상 품질52회 합격이 아님. PDF4쪽 전체 렌더 확인.
- 외부 조사41항목의 지침10/일부코드21/미구현4/직접이식제외·참고6 상태를 전체 적용으로 승격하지 않음.
- 최신 결과:02_분석작업/2026-10-19_전체디자인_기록보강/00_전체디자인_보강결과와_현재위치.md
- 제출PDF:작업 보고서(pdf)/01_제출보고서/Phase 01-A/2026-10-19_전체디자인_기록보강

다음 큰 묶음은 현재 상태/남은 범위를 채팅에 설명하고 추천 포함 사지선다로 사용자 선택을 받은 뒤 진행한다. 작업본 반영은 회사 승인·전체 완성·독립 평가를 뜻하지 않는다.
''',encoding='utf-8')
sys.path.insert(0,str(ROOT/'tools'));from archive_pdf import archive_pdf
pdf=archive_pdf(ROOT/'output/pdf/20261019_design_density_draft9.pdf',category='01_제출보고서/Phase 01-A/2026-10-19_전체디자인_기록보강',name='2026-10-19_전체디자인_기록보강과_draft9_반영.pdf')
receipt={'utc':datetime.now(timezone.utc).isoformat(),'records':str(DEST),'working_skill':str(ACTIVE),'working_skill_version':'0.1.0-draft.9','working_files':newfiles,
 'backup_files':backupfiles,'backup_zip':str(zipdest),'backup_zip_sha256':sha(zipdest),'notice':str(NOTICE),
 'previous415_files_unchanged':True,'pattern_ids_and_hashes_retained':True,'published_file_count':len(operations),'published_files':operations,'pdf':pdf,
 'detailed_window_seconds':28,'outside_window_seconds':602.272,'whole_video_complete':False,'whole_skill_pipeline_complete':False}
save(OUT/'publication-receipt.json',receipt);copy(OUT/'publication-receipt.json',DEST/'publication-receipt.json')
print(json.dumps({k:v for k,v in receipt.items() if k not in ('published_files','working_files','backup_files')},ensure_ascii=False),flush=True)
