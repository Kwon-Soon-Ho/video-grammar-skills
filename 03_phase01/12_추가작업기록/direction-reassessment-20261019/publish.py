from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,sys
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
DEST=D/'00기획/검토안/2026-10-19_목적복원과_스킬적용_재기획'
NOTICE=D/'Phase 01-A/00_진행안내/2026-10-19_스킬수정_현재작업본.md'
BACK=D/'99_백업/2026-10-19_목적복원_재검토전'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def copy(s,d):
 d.parent.mkdir(parents=True,exist_ok=True)
 if d.exists():assert sha(s)==sha(d),'existing different file '+str(d)
 else:
  with s.open('rb') as a,d.open('xb') as b:shutil.copyfileobj(a,b)
 assert sha(s)==sha(d);return {'source':str(s),'destination':str(d),'sha256':sha(d)}
for p in [DEST,NOTICE,BACK]:assert p.resolve().is_relative_to(D) and p.resolve()!=D
assert load(OUT/'validation.json')['passed'] and load(OUT/'report-qa.json')['visual_review']['state']=='passed'
a=load(OUT/'current-audit.json')
for f in a['protected_active_files']:assert sha(Path(a['active_skill'])/f['relative'])==f['sha256']
operations=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts and p.name!='publication-receipt.json':operations.append(copy(p,DEST/p.relative_to(OUT)))
notice_before=copy(NOTICE,BACK/'진행안내_draft9_재기획검토전.md')
NOTICE.write_text('''# 현재 작업 상태 - 목적 복원과 재기획 검토

2026-10-19 사용자 요청에 따라 초기v5·수정v6·조사 소스·현재 구현을 대조했다. 최근 작업이 관측 정밀도/근거/수치 보강에 치우치고 새 설계의 선택·변형과 연결되지 못한 문제를 확인했다.

- 스킬 폴더의 판본은 **draft.9 개발 작업본 그대로**다. 이번에는 스킬·관측·패턴·Phase00 정본·기존 A5b STOP/잠금 기준을 수정하지 않았다. 운영/회사 승인 아님.
- 현재 두 사례의handoff=null,새12개 패턴의 동일한 일반 적용조건,반례 대신미시험 안내가 있는 빈틈을 확인.앞선 디자인 밀도①~④ 질문은 이번 재기획 요청으로 대체되며 사용자 승인으로 처리하지 않음.
- 지향: 사내 영상의 전체 레이아웃·디자인 언어·구성 부품·모션 문법을 가변/보호/적용/제외 조건과 연결하여 새내용의 설계에 응용.원본 관측과 수치 자료는 정밀 근거로 보존.
- 이번 산출물: 기획 감사,기존41소스 항목 역할 재정리,두사례의 지식카드 제안,큰4범주의 실행/평가 계획,8쪽 제출PDF.새시안/영상제작/효과시험/전체소스전수재감사는 미실행.
- 상세 관측창28초/창밖602.272초는원본범위지표이지프로젝트남은양/완료율이아님.전편의모든효과원값복원을새기획시범의선행종료조건으로두지않음.
- 검토안:00기획/검토안/2026-10-19_목적복원과_스킬적용_재기획
- 제출PDF:작업 보고서(pdf)/01_제출보고서/공통 기획/2026-10-19_목적복원과_스킬적용_재기획

다음 큰 묶음은 새기록+새브리프시안시범(추천),디자인DB우선,모션DB우선,판단스킬최소비교의사지선다에서사용자선택후진행.현재검토안이자동으로새회사규칙이나기존스킬수정완료를뜻하지않는다.
''',encoding='utf-8')
sys.path.insert(0,str(ROOT/'tools'));from archive_pdf import archive_pdf
pdf=archive_pdf(ROOT/'output/pdf/20261019_video_knowledge_purpose_replanning.pdf',category='01_제출보고서/공통 기획/2026-10-19_목적복원과_스킬적용_재기획',name='2026-10-19_영상지식DB_목적복원과_스킬적용_재기획검토안.pdf')
receipt={'utc':datetime.now(timezone.utc).isoformat(),'records':str(DEST),'published_file_count':len(operations),'published_files':operations,'pdf':pdf,'previous_notice_backup':notice_before,
 'current_notice':str(NOTICE),'active_skill_version':'0.1.0-draft.9','active_skill_changed':False,'original_plans_changed':False,'pattern_library_changed':False,'previous71_files_preserved':True,
 'replanning_status':'proposal_pending_user_choice','new_design_or_motion_transfer_test_run':False}
(OUT/'publication-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8');copy(OUT/'publication-receipt.json',DEST/'publication-receipt.json')
print(json.dumps({k:v for k,v in receipt.items() if k!='published_files'},ensure_ascii=False))
