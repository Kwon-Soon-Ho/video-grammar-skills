from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def save(name,x):(OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

source=load(ROOT/'research/ponytail-rea-20261019/source-audit.json')
trace=load(ROOT/'case-benchmarks-20261019/adoption-trace-draft8.json')
prior=load(ROOT/'design-record-enrichment-20261019/publication-receipt.json')
active=Path(prior['working_skill'])
for f in prior['working_files']:assert sha(active/f['relative'])==f['sha256']
library=load(ROOT/'case-benchmarks-20261019/knowledge/pattern-library.json')
cases={c:load(ROOT/'design-record-enrichment-20261019/records'/c/'observations.json') for c in ['NEW-N','NEW-P']}
newpatterns=[p for p in library['patterns'] if p['id'] in {'PAT-LAYOUT-0002','PAT-LAYOUT-0003','PAT-FLOW-0002','PAT-FLOW-0003','PAT-TEXT-0002','PAT-TEXT-0003','PAT-DETAIL-0002','PAT-DETAIL-0003','PAT-DETAIL-0004','PAT-DETAIL-0005','PAT-DETAIL-0006','PAT-CARD-0003'}]
save('current-audit.json',{'utc':datetime.now(timezone.utc).isoformat(),'method':'planning and data inspection; no new video decoding, upstream tests, user comprehension test, renderer or skill runtime mutation',
 'handoff_is_null':{k:v['handoff'] is None for k,v in cases.items()},'library_entries':len(library['patterns']),
 'latest12_unique_applicability_strings':len(set(p['applicability'] for p in newpatterns)),
 'latest12_counterexamples':list({s for p in newpatterns for s in p['counterexamples']}),
 'findings':[
  '두 최신 사례의 판단 인계값이null이다. 원본 관측과 목적/조건을 연결하는 실제 기록이 채워지지 않았다.',
  '최신12개 패턴의applicability가 같은 일반 문장이다. 반례 칸은 미시험/미확정 안내이며 구체적인 부적합 입력이 아니다.',
  '현재 지침은 인계를 요청받으면 judgment-handoff를 읽도록 해 목적 연결이 기본 산출물에서 빠질 수 있다.',
  '패턴 검색은 정의/이름/조건의 단순 키워드 교집합이다. 정보 관계·사용 제약에 따른 적합/부적합 필터를 구현한 것이 아니다.',
  '근거/해시/구간 검사와 디자인 밀도 검사는 유용하나 새 내용의 표현 선택 성공을 판정하지 않는다.',
  '노듈러LAYOUT-0002의 비교 배치라는 이름은 동일 대상의 복수 시점/기능 설명과 서로 다른 제품의 우열 비교를 구분해 주지 못한다. 해석을 확인할 필요가 있다.'],
 'root_cause':'식별·누락 실패를 고치며 근거 원자화와 수치 보강이 계속 늘었다. 분석→재사용 문법→새 목적의 선택을 실제 최소 사례로 연결하는 검증이 늦어졌고, 조건·반례가 형식 칸으로 남았다.',
 'not_claimed':['모든 관측이 무가치/오답','모든 원본 재현 가능','전체 외부 스킬 전수분해 완료','최신12개 정의의 회사승인','전체 원본 정밀 분석이 파일럿 종료 조건'],
 'protected_active_files':prior['working_files'],'active_skill':str(active),'protected_publication':pin(ROOT/'design-record-enrichment-20261019/publication-receipt.json'),
 'record_pins':[pin(ROOT/'design-record-enrichment-20261019/records'/c/'observations.json') for c in cases],
 'library_pin':pin(ROOT/'case-benchmarks-20261019/knowledge/pattern-library.json')})

family={
 'P':('조건에 맞는 기존 표현→작은 변형→필요한 새 표현의 선택 순서, 정밀 보강의 재개 조건','전역 활성화·코드 심볼 색인·최소 요소 수를 영상 정답으로 도입하지 않음'),
 'R':('관측·근거·미해결·판본과 검증 범위 연결','원본 전체 픽셀 복원과 모든 미상 해소를 문법 추출의 종료 조건으로 삼지 않음'),
 'T':('원본 이해와 표현 평가를 나누고 가정/관계의 근거를 확인','보안 감사의 함수 전수 추적을 모든 프레임/장식 정밀 측정 의무로 치환하지 않음'),
 'S':('관측 오류와 다른 종류인 잘못된 출력 구조를 실제 사용 과제로 시험','금지문·검사 수만 늘리는 개선을 피하고 참고 검색/적용 실패를 확인'),
 'I':('목적에 맞는 시각 언어·정보 위계·모션 기능과 전체 비평','웹UI 모드/시간표/브라우저 검사/서브에이전트 절차를 직접 설치하지 않음'),
 'G':('기획안의 구체 결함→대안→선택→수정 결과 확인','10점 만점까지 반복 질문·웹 화면 금지 목록·모든 이슈별 승인 루프 제외'),
 'A':('평가 기준 자체의 허점과 과제 밖 주장을 검토,실제 결과를 평가','JSON 형식 검사/해시/파일 수로 디자인 전이 성공을 대신하지 않음'),
 'M':('목적/정보 관계/배치/스타일/동작을 구분하는 용어와 중요한 결정 기록','모든 미세 변경을ADR로 늘리지 않음'),
 'E':('사용자 수정→조건부 규칙 후보→다른 사례 확인','반복 횟수/모델 신뢰도만으로 회사 공통 규칙 자동 승격하지 않음'),
 'V':('조건·영향·긍정 예·부정 예를 묶은 짧은 판단 규칙','React 성능 규칙을 영상 디자인 기준으로 복사하지 않음')}
overrides={
 'P1':('설계에 우선 반영','새 브리프의 필수 관계와 가독성을 먼저 확인하고,맞는 내부 표현이 없으면 변형/새구조로 넘어가는 실제 선택 절차를 시범 실행'),
 'P2':('역할 조정','스타일/정보 관계/요소 역할/모션 기능별 가벼운 인덱스와 상세 조회. 코드맵 코드는 제외'),
 'P3':('직접 이식 제외','전역 훅/자동 활성화를 설치하지 않음'),
 'P4':('설계에 우선 반영','실제 시안의 어느 구성/동작이 어떤 이해 실패를 만드는지 구체적으로 비평'),
 'P5':('역할 조정','각 미상에 어떤 사용을 막는지와 재개 조건을 붙임. 광선 원값 미상이 일반 레이아웃 기록을 전부 막지 않도록 함'),
 'P6':('평가 참고','상류 벤치마크 절감률을 영상 효과로 가져오지 않음'),
 'P7':('평가 참고','새 브리프/다른 프로젝트와 기준선 오염을 분리'),
 'R6':('역할 조정','검증 경계를 기능/구조 재사용,시각 재현,정밀 물리설명으로 구분. 각 경계에 필요한 주장만 종료 의무로 설정'),
 'R9':('후속 보류','상충 판단/최신 검수 묶음 처리는 실제 중복/충돌 사례가 생길 때 범위를 정해 구현'),
 'R10':('역할 조정','한정된 표현의 편집 가능한 시범과 변경 시험에 사용. 동일 픽셀 재현은 별도 요구일 때만'),
 'R12':('직접 이식 제외','정지 픽셀 차이를 정보 전달/디자인/모션의 성공 판정으로 사용하지 않음'),
 'R13':('직접 이식 제외','애니메이션을 멈추는 브라우저 캡처를 영상 모션 분석의 검증법으로 이식하지 않음'),
 'T2':('후속 보류','대량 분석 배치/예산 실행기는 대표 기록의 재사용 효용 확인 후 필요할 때 검토'),
 'S1':('설계에 우선 반영','새 실패는 세부 누락뿐 아니라 목적과 다른 출력 형태. 목적→구성 원리→가변/보호→적용/제외→새입력 적용의 긍정 예시로 수정'),
 'I1':('설계에 우선 반영','설명/비교/설득/공간 이해 등 영상의 전달 과제로 목적을 구분하고 스타일·배치 선택에 연결'),
 'I2':('설계에 우선 반영','표현 적합성·전체 인상과 기계적 오류 검사를 별도 기록. 이 검토는 같은 AI 문맥이며 독립 평가라고 주장하지 않음'),
 'I3':('설계에 우선 반영','모션을 주목·관계·연속성·상태 설명의 역할로 기록. 등장/읽기/강조/유지/정리의 흐름과 재사용 가능한 세부를 연결'),
 'G1':('설계에 우선 반영','원본을 베껴야 한다는 가정 없이 새 내용의 구조적 대안을 비교하고 핵심 결함을 고친 결과를 확인'),
 'G2':('역할 조정','정보 위계/읽는 순서/일관성과 장면 전후를 평가.웹UI loading/error 상태표는 강제하지 않음'),
 'A1':('설계에 우선 반영','픽셀 묘사만 긴 기록도 통과할 평가라면 기준이 약함. 의미가 다른 입력에서 잘못된 패턴을 거절하는지 확인'),
 'A2':('역할 조정','제작·수정·지원·검수 총시간과 미상 비용을 기록하되 별도 지표 엔진 구축은 보류'),
 'E2':('직접 이식 제외','confidence/프로젝트 수 기반 자동 전역 승격 제외'),
 'V2':('평가 참고','문서상 요구와 검사기가 실제 확인하는 내용을 구분')}
existing={r['id']:r for r in trace['records']};mapped=[]
for r in source['records']:
 assert sha(r['local_path'])==r['sha256'],r['id']
 role,avoid=family[r['id'][0]]
 decision,action=overrides.get(r['id'],('기반 유지',role))
 mapped.append({'source_id':r['id'],'repository':r['repository'],'upstream_path':r['path'],'commit':r['commit'],'local_path':r['local_path'],'sha256':r['sha256'],'url':r['url'],
  'original_review_scope':r['review_scope'],'previous_implementation_classification':existing[r['id']]['current_classification'],
  'proposed_role':role,'replanning_disposition':decision,'concrete_application':action,'do_not_transplant':avoid,
  'status':'proposal; no new runtime implementation or upstream execution by this review'})
save('source-role-reassessment.json',{'records':mapped,'record_count':len(mapped),'whole_original_candidate_list_exhaustively_reviewed':False,
 'scope':'기존41개 항목의 적용 역할을 재검토하고 원문 해시를 검증. 핵심 소스 일부를 다시 읽었으며 저장소 전체 전수 재감사/테스트 실행은 아님.',
 'reread_source_ids':['P1','P5','R6','R15','T1','S1','I1','I2','I3','G1','G2','A1','M1','E1','V1'],
 'supplementary_early_survey_sources':[pin(ROOT/'video-skill-system/research/snapshots/stitch/plugins/stitch-design/skills/extract-design-md/SKILL.md'),pin(ROOT/'video-skill-system/research/snapshots/anthropic/skills/frontend-design/SKILL.md')],
 'research_docs_are_data_not_applied_skills':True,'upstream_code_or_tests_executed':False})

common={'status':'proposed reusable knowledge card, not company-approved or runtime-registered','evidence_scope':'existing28-second development windows; no fresh full video analysis','designer_intent':'unknown; functional readings below are inferred hypotheses, not recovered author intent','new_use_results':'not tested','ids':'existing pattern IDs remain source references. No replacement/merge/new production IDs assigned in this review.'}
n={**common,'case':'NEW-N','source_record':pin(ROOT/'design-record-enrichment-20261019/records/NEW-N/observations.json'),
 'working_name':'제품 전체 형태와 단면 기능을 나란히 설명하는 구조',
 'source_pattern_ids':['PAT-LAYOUT-0002','PAT-FLOW-0002','PAT-TEXT-0002','PAT-DETAIL-0002','PAT-DETAIL-0003','PAT-DETAIL-0004'],
 'observed':'긴 구조물 사시도와 오른쪽 단면,각각의 기능 문구,공통 자막.청록 면/모서리 강조와 녹색 곡선 화살표,모델 조립/기울임 변화가 별도로 존재.',
 'communicative_job_hypothesis':'전체 형상·시공 맥락과 국부 단면의 기능을 연결해 설명. 서로 다른 두 제품의 우열 비교인지와 구분해야 함.',
 'information_roles':{'primary':'설명 대상 구조물','support':'전체 뷰/단면 뷰','claim':'각 뷰와 대응하는 기능 문구','context':'제목/자막/회사표시'},
 'visual_language':{'composition':'긴 원근 모델과 정면 단면의 비대칭 병치,위쪽 기능 라벨과 아래 공통 자막','typography':'핵심 용어의 굵기 대비,설명/자막의 역할 분리','color':'어두운 기술 배경과 밝은 재료,청록 구성 강조·녹색 방향 강조','surface':'기술 설명 띠/선 끝표식,배경의 점/망/곡선. 정확 효과값은 원본 관측 부록에 보존'},
 'template_contract':{'inputs':['같은 대상의 전체/상세 자료','각 뷰의 설명 문구','강조할 부위와 사실 근거','출력 화면비·최소 읽기 조건'],
  'preserve':['문구-대상 대응','전체와 상세의 관계','강조 부위가 정확한 구조를 가리킴','읽는 동안 핵심 상태 유지'],
  'variable':['두 영역의 배치/비중','라벨 형식·내용·강조 단어','배경/재료/팔레트','전체/상세 전환 방식','강조 동작의 크기와 유지시간'],
  'adaptation_rules':['긴 모델 때문에 여백이 부족하면 전체/상세를 순차 장면으로 나누는 후보','설명이 길면 띠를 억지로 축소하지 않고 설명 영역/장면 분할 검토','화면비 변경은 고정 좌표 스케일보다 정보 그룹 재배치로 검토'],
  'unknown_valid_ranges':'허용 문구 길이·요소 수·폰트 최솟값·유지시간 범위는 아직 시험하지 않음'},
 'motion_grammar':{'flow':'전체 맥락을 제시→설명 부위/기능을 차례로 강조→읽을 상태 유지→다음 구성/공정으로 연결하는 재구성 후보.원본의 실제 사건 순서는FLOW-0002를 별도 참조.',
  'detail':'TEXT-0002의 선 분리/문구 공개는 설명 라벨 한 구현 사례. 모델 기울임·주변 방향 화살표·밀착 하이라이트는 서로 다른 기능 후보.',
  'parameters':['주목 이동 순서','뷰 간 동시/순차 제시','문구 유지시간','대상 강조 범위','가감속 성격'],
  'nonblocker':'화살표 원본 강도 곡선 미상은 밝기 재현 프리셋에 영향을 주며 전체/상세 배치 후보 자체를 없애지는 않음'},
 'fit_example':{'type':'synthetic planning test','brief':'방음 패널의 전체 설치 모습과 내부 단면의 소음 저감 원리를 설명한다.','transfer':'같은 대상의 전체/단면 역할을 유지하되 밝은 배경과 적층 단면·연결 콜아웃으로 새 디자인 제안 가능','result':'not rendered or evaluated'},
 'counterexample':{'type':'synthetic negative input','brief':'서로 다른 두 제품의 가격과 성능을 동일 축으로 비교한다.','why_not_fit':'전체/상세 관계가 아니다.좌우 모습만 비슷하다고 이 문법을 적용하지 말고 공통 항목 비교 구조를 검토.'},
 'alternative_proposals':['전체/상세 병치','전체→단면 순차 전개','하나의 모델 위 국부 확대 콜아웃'],
 'precision_policy':'글자 역할·대비·영역 관계·대상 연동을 기본 기록. 기존1474px/강도곡선은 사례 부록/정밀 재현 요청용. 새 디자인의 기본값으로 복사하지 않음'}
p={**common,'case':'NEW-P','source_record':pin(ROOT/'design-record-enrichment-20261019/records/NEW-P/observations.json'),
 'working_name':'지도 맥락 위 기관과 소속 정책을 연결하고 순차 강조하는 구조',
 'source_pattern_ids':['PAT-LAYOUT-0003','PAT-FLOW-0003','PAT-CARD-0003','PAT-TEXT-0003','PAT-DETAIL-0005','PAT-DETAIL-0006'],
 'observed':'어두운 지도/횡성 강조 위 기관 로고 카드와 두 정책 행,연결선/접점,기관별 색.강원 묶음 오른쪽 이동과 하위 정책 패널 크기 변화가 함께 보임.',
 'communicative_job_hypothesis':'기관 정체와 정책의 소속을 묶어 읽게 하고 지도에서 공간 맥락을 유지.기관 사이 인과·협업·자금 흐름은 화면만으로 확정하지 않음.',
 'information_roles':{'owner':'기관','items':'그 기관에 대응하는 정책','context':'지역/지도','group_cue':'색/연결선/프레임/근접성'},
 'visual_language':{'composition':'소속 정책을 위에,기관을 아래에 두고 세로 축으로 연결.행별 강조와 묶음 여백 활용','typography':'기관 로고와 정책 문구 분리,현재 문구의 밝기/굵기 대비','color':'기관별색을 카드/선/띠/모서리에 일관되게 사용','surface':'반투명 판·가는 선틀·색 모서리·화살촉 띠의 기술적 외관.새 작업에서는 형태 단순화/대체 가능'},
 'template_contract':{'inputs':['기관별 정책 묶음','기관 식별 자료','지도/지리 정보가 필요한 이유','문구량·기관 수·화면비·읽기 조건'],
  'preserve':['기관-정책 소속 정확성','색/근접/선이 같은 묶음을 가리킴','기관을 구별할 수 있는 상태 유지','한 정책을 읽는 동안 경쟁 강조를 제어'],
  'variable':['기관 수/정책 수/문구','지도 사용 여부','위아래/좌우/세로 목록 배치','프레임/모서리/띠 스타일','기관색','정책 강조 순서·읽기시간·묶음 재배치'],
  'adaptation_rules':['지리 정보가 핵심이 아니면 지도 대신 소속 그룹만 표현','문구량/기관 수가 많으면 순차 장면 또는 열/목록으로 재구성','확정되지 않은 관계를 연결선/화살표로 새로 만들지 않음'],
  'unknown_valid_ranges':'행 수·문구량·좁은 화면의 적합 범위는 미시험;원본 두행을 보편 상한으로 선언하지 않음'},
 'motion_grammar':{'flow':'기관을 식별 가능하게 제시→소속 관계 연결→정책을 차례로 강조→전체 관계 유지/재배치.이는 새 설계를 위한 후보이며 원본 순서는FLOW-0003을 참조.',
  'detail':'로고/카드 등장,연결선 채움,정책 행 강조,묶음 이동과 하위 패널 축소를 구분.색/굵기/크기와 읽기 상태의 연동을 기록.',
  'parameters':['기관과 정책의 선후·겹침','정책별 유지시간','전후 강조의 중첩','공간 재배치와 하위 크기 변화의 관계'],
  'nonblocker':'정확 축소곡선 미상은 해당 크기 애니메이션 재현의 미확정이며 기관-정책 소속 문법 후보는 따로 검토 가능'},
 'fit_example':{'type':'synthetic planning test','brief':'세 사업부별 핵심 업무를 설명한다.지리 위치는 중요하지 않다.','transfer':'지도는 제거하고 사업부-업무 관계를 세로 그룹/열로 표현.기관색 역할과순차 주목 이동을 변형 적용','result':'not rendered or evaluated'},
 'counterexample':{'type':'synthetic negative input','brief':'여러 기관 사이의 자금이동 경로와 규모를 설명한다.','why_not_fit':'소속과흐름은다름.관계선이 소유/대응을 뜻하는 원본 구조만으로 흐름 방향·양을 표현할 수 없어 다른 문법 검토.'},
 'alternative_proposals':['지도+소속 콜아웃','지도 없는 그룹형 편집 레이아웃','기관별 순차 소개와 전체 관계 회수'],
 'precision_policy':'소속 그룹·기관색 역할·글자/지도 위계·정책 읽기 상태·연결선 기능을 기본 기록.선틀/모서리는 기술적 스타일 부품의 특징으로 묶고 모든 픽셀을 독립 지식 항목으로 만들지 않음'}
save('knowledge-card-proposals.json',{'note':'현재 역할을 보이기 위한 실제 사례 기반 기획 시범.새 기획 예/반례는 합성 입력이며 실영상 사례/회사 규칙/검증 결과로 등록하지 않음.','cards':[n,p]})

plan={'status':'replanning proposal; user review pending','anchor_goal':'회사 영상의 레이아웃·디자인 언어·디자인 부품과 모션 문법을 검색·변형 가능한 지식으로 축적하고 새 브리프의 설계·제작·수정에 도움이 되는지 검증',
 'layers':[
  {'layer':'원본 근거','contents':'영상·대표 상태·실제 문구/대상/모션·시간/ROI·수치·미확정','storage_mapping':'Asset/Segment/StateFrame/MotionBeat/Evidence/Claim/AnalysisRun','visibility':'기본 화면에서는 요약,정밀 근거는 필요할 때 펼침'},
  {'layer':'재사용 가능한 지식','contents':'전달 과제·정보 관계·디자인 언어·구성 단위·전체 흐름/세부·가변/보호·적용/제외 조건','storage_mapping':'Pattern/CasePatternLink/DesignRule + 보조 제안 기록.새정본DB를 중복 생성하지 않음','visibility':'검색/활용의 중심.회사 규칙 승격은 별도'},
  {'layer':'새 기획과 적용 결과','contents':'새브리프·후보·선택/제외 이유·화면/모션안·수정·검수·실제공수','storage_mapping':'Scene Planner/Composer/Motion Director의 기획 산출물과Review/근거 참조','visibility':'원제작 의도나 원본 관측과 분리'}],
 'search_contract':{'query':['정보 관계','전달 과제','자료 종류','정보량/문구길이','시청환경/화면비','시각 톤','원하는 모션 기능'],
 'result':['맞는 후보와대표화면','사용조건/안맞는이유','레이아웃/스타일/모션을 각각 적용할 범위','바꿀 항목/보호할 관계','관련 원본 근거와 미확정'],
 'suitability_order':'의미/관계와 필수제약→레이아웃/가독성→프로젝트 시각언어→모션기능/시간→필요한 세부기법.실제우선순위는브리프제약에따라조정'},
 'minimal_card_recipe':['이 사례가 해결하는 전달 과제와 근거 수준','전체 구도/시각언어/구성 부품','전체 모션흐름과 독립 세부의 역할·행동','바꿔도 되는 입력과 지켜야 할 관계','맞는 입력/맞지 않는 입력/대체안','원본 근거/미확정과 사용 결과'],
 'precision_rule':'먼저 어떤 재사용 결정을 바꾸는 값인지 적는다.정보 소속/읽기 실패/식별 오류는 보완한다.정확한 재현이나 물리설명·특정효과 프리셋에 필요한 경우 정밀 측정을 보강.장식의 존재/특징 기록은 유지하되수치 의무화하지 않음.',
 'skill_roles':{'analyzer':'원본 구성/문구/모션과 근거를 기록하며 중립적인 역할 후보를 인계.의도 확인 못했다고 기능 분석까지 비워두지 않음.',
 'curation':'관측을 참조해 디자인/모션 문법 후보·템플릿 계약·반례를 작성.기존DB/용어/ID와 연결하고 새역할이기존단계01-B에해당함을명시.',
 'planning':'새 목적에 맞는 구조적 대안 비교·선택/제외·표현설계.기존레이아웃확대복사를 창의적선택으로 대체하지 않음.',
 'review':'내용/기술 정확성과 전체 디자인/전달 적합성을 나눠 검토.그후 실제 변경·전이 결과로 기준 개선.'},
 'work_categories':[
  {'name':'1 목적과 기록 구조 시범','scope':'기존 두 사례를 새로운지식카드로 재구성하고 적합/부적합새브리프를 연결','done_this_turn':'문서/코드감사,두 카드 제안,구조/시험계획 작성','not_done':'사용자 판단·새 시안/애니메이션 제작·효과 검증'},
  {'name':'2 DB와 스킬의 역할 조정','scope':'사용자가검토한카드를기준으로분석출력/문법인계/검색/조건·반례를최소수정','exit':'대표화면/조건으로찾고 필요한 근거를 조회하며 부적합 입력을 구분','constraint':'기존 ID/정본/실패기록 보존,일괄재분석/거대신규DB개발없음'},
  {'name':'3 새 입력의 선택·변형 시험','scope':'문구·정보량·화면비·스타일·정보관계를바꾼브리프에서화면안/모션스토리보드대조','exit':'단순외형복사와구분되는조건적응·부적합거절·전체디자인일관성','constraint':'일반AI동일조건비교.문서상좋은이유만으로통과하지않음'},
  {'name':'4 한 제작 경로의 실용 검증','scope':'선정한짧은표현을한도구에서제작/렌더후내용교체·수정시험','exit':'품질·독립수행·총공수·전이와유지부담의비교','constraint':'영상전편/복수엔진동시개발로확대하지않음'}],
 'tests_proposed':[
  {'id':'T-purpose','input':'같은 모양의 카드지만 정보 관계는소속/비교/순서/흐름으로다름','check':'관계에맞는후보를선택하고부적합후보의이유를설명·시안에반영'},
  {'id':'T-design','input':'내용관계는유지하고문구길이/요소수/화면비를변경','check':'위계·그룹·읽기조건을지키며재배치/분할.고정좌표확대복사에의존하지않음'},
  {'id':'T-style','input':'같은전달과제에다른프로젝트톤/자산','check':'배치원리/모션기능은전이하고특정남청배경/프레임을무조건복사하지않음'},
  {'id':'T-motion','input':'순서·주목·읽기시간제약변경','check':'전체흐름과세부가메시지와맞는지실제클립에서대조.정확곡선/색차만으로평가하지않음'},
  {'id':'T-value','input':'같은브리프/자료/도구/자원한도에서일반AI와비교','check':'내용·디자인·모션·수정·전문가도움·지원/유지포함총공수.실제수치기준은사전합의'}],
 'migration':{'keep':['기존 원본/프레임/전체구성/모션 발견/정정/근거/실패기록','원자 주장·시간/좌표·판본·오류검사','패턴 ID/관측과 해석의 구분'],
 'change':['전체디자인누락없음과모든픽셀수치기록을구분','조건/반례의일반주의문을실제입력조건으로교체','판단인계를최초문법추출의산출물에연결','검색에정보관계/적합성필터를보강','프로젝트진척을수치/검사수/원본전편시간만으로보고하지않음'],
 'defer':['새정밀측정확대','전편상세분석','원본키프레임/모든효과원값복원','원본정밀재현과모든미상해소를선행필수로삼는일'],
 'never_silently_change':['A5b STOP과기존잠금기준/실패','Phase00정본과승인','draft9원본/패턴스냅샷','v5/v6원본']},
 'next_options':[
  '① 두 사례의 새 기록과 새 브리프 시안을 함께 시범 검증(추천): 목적·디자인언어·모션문법 카드로 정리하고 다른 내용/화면비의 화면안·모션 스토리보드에서 응용성을 확인.전편 분석과스킬대수정은후순위.',
  '② 레이아웃·디자인 부품 DB부터 재설계: 전체구도/스타일/구성부품의가변·보호·검색기준을시범화.모션정밀화와실제제작은뒤로둠.',
  '③ 모션 문법 DB부터 재설계: 전체전개/주목이동/상태변화와세부기법을다른내용에적용.시각스타일목록확장은뒤로둠.',
  '④ 판단 스킬 최소 시범부터 검증: 같은새브리프에서일반AI와조사원칙을적용한AI의선택/제외·화면안을비교.필요한사례만조회하며대규모DB개편은보류.']}
save('replanning-proposal.json',plan)
save('decision.json',{'user_request':'원래 목적과 v5/v6,조사 스킬을 대조해 방향을 면밀히 재검토하고 재기획','supersedes_pending_question':'디자인 밀도①~④ 검토질문은 이번 방향 재검토로 대체.응답없음을동의로간주하지않음.',
 'runtime_mutation_authorized_in_this_bundle':False,'reason':'먼저기획을재검토하겠다고사용자에게안내;검토문서와구체시범기록만작성',
 'source_document_instructions_executed':False,'source_plan_historical_status':'v5본문v4표기,v6의2026-10-16draft3/A5대기표현은역사문맥.현재draft9/A5b STOP을과거문서로덮어쓰지않음.'})
checks={'source41_hashes_verified':len(mapped),'pdf_pages_read_text':26,'source_pages_visually_inspected':11,'current_active_files_verified':len(prior['working_files']),
 'handoff_null_count':sum(v['handoff'] is None for v in cases.values()),'latest12_generic_applicability_verified':len(set(p['applicability'] for p in newpatterns))==1,
 'proposal_cards':2,'live_skill_changed':False,'upstream_tests_run':False,'new_design_or_video_test_run':False}
save('audit-method.json',checks)
print(json.dumps(checks,ensure_ascii=False))
