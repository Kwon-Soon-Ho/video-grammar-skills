from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,sys
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
DEST=D/'Phase 01-A/02_분석작업/2026-10-19_기준사례_보완과_스킬채택추적'
BACKUP=D/'99_백업/2026-10-19_기준사례_보완전'
NOTICE=D/'Phase 01-A/00_진행안내/2026-10-19_스킬수정_현재작업본.md'
def load(p):return json.loads(Path(p).read_text('utf-8'))
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def copy(s,d):
 d.parent.mkdir(parents=True,exist_ok=True)
 if d.exists():assert digest(d)==digest(s),d
 else:
  with s.open('rb') as i,d.open('xb') as o:shutil.copyfileobj(i,o)
 assert digest(s)==digest(d)
 return {'source':str(s),'destination':str(d),'sha256':digest(d)}
for p in [DEST,BACKUP,NOTICE]:assert p.resolve().is_relative_to(D) and p.resolve()!=D
assert load(HERE/'validation.json')['all_passed'] and load(HERE/'report-qa.json')['visual_review']['state']=='passed'
prior=load(WORK/'internal-video-audit-20261019/publication-receipt.json')
for f in prior['published_files']:assert digest(f['source'])==digest(f['destination'])==f['sha256']
for f in prior['new_working_files']:assert digest(Path(prior['working_skill'])/f['relative'])==f['sha256']
operations=[]
for p in sorted(HERE.rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts and p.name!='publication-receipt.json':operations.append(copy(p,DEST/p.relative_to(HERE)))
print('Case records, source trace, native evidence and pattern snapshots copied with hashes.',flush=True)
copy(NOTICE,BACKUP/'진행안내_draft8_기존상태.md')
notice='''# 분석 스킬 현재 작업본과 기준 사례

2026-10-19 갱신: 스킬 본체는 **0.1.0-draft.8 개발 작업본**을 유지한다. 이번 묶음은 실제 사례·패턴 초안·스킬 반영 추적 자료를 추가했으며 스킬 본체를 다시 수정하거나 전체 제작을 완료한 것이 아니다.

- 사용자 선택: 현재 두 장면의 미해결과 전후를 보완해 기준 사례 후보로 정리.
- 노듈러166~181초15초, PG40~53초13초. 합계28초에 상세 기록 창이 있으며, 원본 전체 약630.272초 중 창 밖602.272초가 남음. 전후 문맥 표본은 상세 분석 시간에 넣지 않음.
- 기존 미해결5개 중4개는 관측 범위 한정 답변,1개는 부분 보완. 화살표 정확 강도 곡선/원본 동기화 설정은 미해결로 유지.
- 각 사례3개 화면 상태, 전체 흐름/세부 연결. 기존6개 패턴을 보존하고 새12개 초안을 등록. 좌우 설명 띠/두 정책 행은 같은 번호에 현재 근거와 차이를 연결. 전 항목 candidate이며 재제작 성공·회사 승인 아님.
- 조사41개 항목을 draft.8 파일과 다시 대조함. full17/selected24 정적 검토로, 최초 대화의 모든 후보 전수 분해·원본 테스트 실행·전체 반영 완료가 아님.
- 현재 큰 단계: 분석 신뢰성 보완 중. 패턴 재사용 적합성, 전문가 대안/선택/비평/재평가, 편집 가능한 재제작/렌더 비교/내용 변경 검증은 여전히 남음.
- 최신 기록: `02_분석작업/2026-10-19_기준사례_보완과_스킬채택추적/00_기준사례_검토안과_현재위치.md`
- 제출 PDF: `작업 보고서(pdf)/01_제출보고서/Phase 01-A/2026-10-19_두기준사례_보완과_채택추적`

다음 묶음은 현재 결과·남은 범위를 채팅에서 설명하고 추천안 포함 사지선다를 제공한 뒤 사용자 선택을 받아 착수한다. 이미 승인된 묶음 안의 세부 작업은 재승인받지 않는다.
'''
NOTICE.write_text(notice,encoding='utf-8')
sys.path.insert(0,str(WORK/'tools'));from archive_pdf import archive_pdf
pdf=archive_pdf(WORK/'output/pdf/20261019_two_reference_cases_and_adoption_trace.pdf',category='01_제출보고서/Phase 01-A/2026-10-19_두기준사례_보완과_채택추적',name='2026-10-19_두기준사례_보완과_외부스킬_반영추적.pdf')
receipt={'utc':datetime.now(timezone.utc).isoformat(),'records':str(DEST),'working_skill':prior['working_skill'],'working_skill_version':'0.1.0-draft.8','working_skill_changed':False,'active_working_files_unchanged':True,'prior_335_source_and_destination_files_unchanged':True,'prior_notice_preserved_at':str(BACKUP/'진행안내_draft8_기존상태.md'),'current_notice':str(NOTICE),'published_file_count':len(operations),'published_files':operations,'pdf':pdf,'expanded_issues':{'addressed_with_limits':4,'partial':1},'recorded_window_seconds':28,'outside_recorded_window_seconds':602.272,'new_pattern_drafts':12,'whole_case_pattern_occurrences':14,'original_pattern_entries_preserved':6,'whole_video_fine_analysis_complete':False,'whole_external_skill_adoption_complete':False,'independent_video_quality_evaluation':False}
data=json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf-8');(HERE/'publication-receipt.json').write_bytes(data);(DEST/'publication-receipt.json').write_bytes(data)
assert digest(HERE/'publication-receipt.json')==digest(DEST/'publication-receipt.json')
print(json.dumps({k:v for k,v in receipt.items() if k!='published_files'},ensure_ascii=False),flush=True)
