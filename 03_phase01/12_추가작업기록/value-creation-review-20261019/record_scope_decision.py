from pathlib import Path
from datetime import datetime, timezone
import json, copy, hashlib
O=Path(__file__).resolve().parent;R=O.parent
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
decision={
 'utc':datetime.now(timezone.utc).isoformat(),
 'user_answer':'1과 3 혼합. 지금 하는 테스트가 만든 스킬을 가지고 화면 분석을 하고 그걸 새롭게 만들어보는 작업을 하는거야? 왜 db 수집에서 끝내지 않고 화면 재구축까지 하는거지?',
 'accepted_meaning':'원본 디자인 언어와 구성/모션은 충실히 수집한다. 이후 활용은 원본 언어 유지 또는 새 스타일로의 변형 모두 가능하도록 조건을 기록한다. 모든 디자인 요소를 회사 공통 강제 규칙으로 등록하지 않는다.',
 'scope_correction':'추가 화면 재구축과 모션 제작은 현재 DB 수집의 범위에서 제외한다. 실제 제작/응용 시험은 사용자가 별도 요청할 때 진행한다.',
 'why_proof_happened':'이전 두 사례의 새 기록+새 브리프 시범 선택에 따라 새 화면안을 만들었다. 이를 DB 수집의 필수 선행 검증으로 확대하거나 계속 디자인 방향 질문으로 끌고 간 것은 작업 진행상의 판단 오류다.',
 'actual_work_status':'draft.9를 유지한 상태에서 에이전트가 원본 표본을 관찰하고 기록 구조/판단 기준을 보정했으며 새 화면은 별도로 그린 개발 시범이다. 완성 스킬을 독립 실행하는 성능 평가나 정본 DB 수집 완료가 아니다.',
 'retain':['원본 영상과 시나리오 핀','관측/기능 해석/새 제안 구분','전체 사례와 레이아웃·디자인 언어·부품·전체 흐름·세부 동작 연결','표현/배치/재질/강조 관계와 사용 조건','누락/미상/미검수 범위와 보강 조건'],
 'exclude_from_collection_completion':['새 화면 이미지 생성','원본 재구축','다른 주제 새 브리프 제작','AE 제작·모션 렌더','새 시안 사용자 승인'],
 'collection_acceptance_proposed':['관측 구간에서 중요한 요소·상태·변화가 기록에 대응하는지','부품이 어디에 어떤 관계로 배치되고 어떤 역할인지','전체 흐름과 독립 세부 동작을 구별하고 반복 시 근거·차이로 연결하는지','원본 고유 표현과 일반적 적용 조건을 구별하는지','확인하지 않은 구간·원값을 명시하는지'],
 'boundaries':['일부 원본 표본의 기록을 전편 정밀 검수 완료로 확대하지 않음','2초 표본의 후보를 상세 모션 템플릿으로 승격하지 않음','수치 관계 검사나 문서 검사 통과를 디자인 이해/스킬 성능으로 확대하지 않음'],
 'next_work':'두 사례의 수집 기록에서 재사용에 필요한 시각 구성·조합·모션 관측의 누락과 정밀 보강 필요점을 정리한다. 새 시안 제작을 종료 기준으로 두지 않는다.',
 'active_skill_modified':False,'canonical_db_modified':False,'additional_visual_proof_generated':False,
 'supersedes':'원본 언어 유지 범위를 하나의 강제 스타일로 선택하는 기존 4지선다. ①+③ 혼합으로 기록. 같은 조건 두 스타일 비교는 선택되지 않음.'}
write(O/'scope-decision.json',decision)
cards=copy.deepcopy(read(O/'knowledge-cards.review-r1.json'))
cards['review_revision']['id']='review-r2'
cards['review_revision']['status']='DB 수집 범위 보정안; 실제 스킬/정본 반영 아님'
cards['review_revision']['pending_design_language_choice']=False
cards['review_revision']['preservation_policy']=decision['accepted_meaning']
cards['review_revision']['collection_completion_excludes']=decision['exclude_from_collection_completion']
for c in cards['cases']:
 c['proof_use']='이전 시범의 설계 가설 기록. DB 수집 완료/원본 분석 정확도의 증거로 사용하지 않음.'
 c['style_transfer_status']='원본의 구성·시각 언어를 수집하되 이후 활용 스타일을 강제하지 않음. 새 화면 제작은 현재 수집 범위에서 제외.'
write(O/'knowledge-cards.review-r2.json',cards)
(O/'00_현재방향.md').write_text('''# 현재 방향: 원본을 충실히 수집하고 활용 방식은 열어두기

사용자 답변: ①+③ 혼합. DB 수집에서 왜 재구축까지 하는지 범위 재확인.

현재 작업은 완성 스킬의 독립 성능 평가가 아니다. 스킬 draft.9와 정본 DB는 변경하지 않은 상태에서 에이전트가 원본을 관찰하고 기록 구조와 판단 기준을 보정한 개발 작업이다.

이전 새 기록+새 브리프 시범 선택으로 화면안을 만들었지만, 새 화면을 DB 수집의 필수 종료 조건으로 확대하지 않는다. 추가 화면/모션 제작을 중단한다. 기존 결과는 이전 가설/시범으로 보존한다.

원본의 레이아웃·디자인 언어·구성 부품·전체 흐름·세부 동작을 조건과 함께 수집한다. 나중에 원본 언어를 유지하거나 다른 스타일로 응용하는 것은 별도 활용 단계에서 정한다.

현재 최신 보정안은 knowledge-cards.review-r2.json과 scope-decision.json이다. review-r1은 사용자 답변 이전 검토안으로 보존한다. 이 자료들이 기존 정본 DB에 등록됐다는 뜻은 아니다.

다음: 두 사례 기록의 누락/미상과 필요한 모션 관측 보강점을 정리한다. 사용자 피드백을 계속 받을 때에도 새 화면 제작 선택부터 묻지 않는다.
''',encoding='utf-8')
assert not decision['additional_visual_proof_generated']
print('Hybrid preservation policy and DB-only collection scope recorded. Prior proof retained as historical proposal.')
