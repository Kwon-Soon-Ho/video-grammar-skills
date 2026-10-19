from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, copy
O=Path(__file__).resolve().parent;R=O.parent;P=R/'value-creation-pilot-20261019'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
old=load(P/'knowledge-cards.json')
pins=[{'path':str(p),'sha256':sha(p)} for p in [P/'knowledge-cards.json',P/'proof-index.json',P/'motion-proposals.json',P/'report-build.json']]
findings=[
 {'id':'REV-01','kind':'record correction','finding':'원본 계약 화면을 동급 3패널로 단순화한 설명은 부정확하다.','evidence':'112초: 원본 실제 매출은 주황색 큰 숫자와 상승 아이콘으로 강조된다. 수주 구성 패널도 정보량이 많고, 비용 패널은 좁다.','correction':'원본도 위계가 있다. 새 안은 매출을 먼저 읽게 하는 다른 위계로 재구성한 제안이다. 기존 대비 이해도 향상을 입증하지는 못했다.','user_choice_required':False},
 {'id':'REV-02','kind':'source style transfer gap','finding':'원본 디자인 언어를 기록했지만 새 시안에서는 색·밝은 바탕 외에 적용 근거가 약하다.','evidence':'장 배지·제목 리본·입체감 있는 숫자/프레임/차트·업무 이미지와 정보면의 조합이 평면 텍스트와 카드로 바뀜.','correction':'현재 시안은 정보 구조 검토용으로 한정한다. 원본 언어의 기본 유지 여부는 사용자 판단 대기.','user_choice_required':True},
 {'id':'REV-03','kind':'hierarchy transfer gap','finding':'프로젝트 지원의 핵심 강조가 충분히 옮겨지지 않았다.','evidence':'150초 원본은 BIM 설계 큰 행+약82% 도넛을 강조하고 나머지 세 분야를 작은 카드로 묶는다. 새 세로안은 네 행이 같은 구획 크기이며 82%를 직접 말하지 않음.','correction':'BIM 설계가 금액의 대부분이라는 핵심과 전체 분류 열람 중 무엇을 우선할지 브리프에 명시한다. 원본의 핵심 강조와 대안 위계 모두 비교 검토해야 한다.','user_choice_required':True},
 {'id':'REV-04','kind':'source/proposal distinction','finding':'수치 역할 구분·새 분류 전환·원본 모션 후보를 같은 수준의 재사용 검증으로 취급할 수 없다.','evidence':'지원의 가족사별→유형별 전환과 총액 고정은 새 제안이다. 원본 표본은 2초 간격이며 정확한 시작·겹침·곡선은 미관측.','correction':'사실/기능 해석/새 제안과 기록 성숙도를 각각 표시한다. 현재 모션 후보는 제작용 타이밍 템플릿으로 승격하지 않는다.','user_choice_required':False},
 {'id':'REV-05','kind':'comparison limitation','finding':'내용·화면비·정보량·스타일이 동시에 바뀌어 현재 비교만으로 좋은 디자인 방향을 고를 수 없다.','evidence':'계약 32:9→16:9, 지원 32:9→9:16. 숫자도 변경안으로 교체했고 구성 항목/실경을 일부 유보함.','correction':'이 비교는 무엇을 보존/유보했는지 찾는 용도이다. 가독성 우열·브랜드 적합성을 결론내리지 않는다. 같은 조건 비교는 별도 선택지로 둔다.','user_choice_required':False}
]
grammar=[
 {'id':'VC-GRAMMAR-01','topic':'장 식별 체계','observed':'상단 왼쪽 번호/TDC 육각 배지와 짧은 장 제목 띠. 계약 녹색, 프로젝트 지원 구리색 계열.','role_hypothesis':'현재 장과 연속성을 알려준다.','variation_rule_proposed':'화면비가 달라도 장의 위치/번호/명칭을 일관되게 인식할 수 있게 조합. 배지의 정확한 좌표는 공통 원리가 아니다.','omission_cost':'색만 남기면 시리즈 표식이 약해질 수 있음.'},
 {'id':'VC-GRAMMAR-02','topic':'실경과 정보면의 층','observed':'계약은 연한 도시 실경을 배경층으로, 지원은 왼쪽 도로/지도 업무 영상과 오른쪽 정보판으로 사용.','role_hypothesis':'실적·업무 맥락과 수치 설명을 연결한다. 장면에 따라 배경과 주증거의 역할이 다르다.','variation_rule_proposed':'역할을 먼저 선택해 배경형/분할형/순차 노출형으로 변형. 실제 프로젝트 이미지는 새 내용과 맞는 것을 사용.','omission_cost':'전부 삭제하면 어느 업무의 성과인지 보여주는 구체성이 약해질 수 있음.'},
 {'id':'VC-GRAMMAR-03','topic':'프레임·재질의 묶음','observed':'계약의 밝은 둥근 정보면·가는 경계·은은한 그림자·일부 헤더 띠. 지원의 아이보리 정보판·갈색 경계·점무늬와 도시 실루엣.','role_hypothesis':'정보를 묶으면서 장의 분위기를 구별한다.','variation_rule_proposed':'정보판의 바탕/경계/헤더/배경 모티프를 함께 선택하고 글자와 충돌하면 약화. 모든 장에 같은 평면 카드를 강제하지 않음.','omission_cost':'색만 바꾼 공통 카드로는 장별 시각 언어가 소실될 수 있음.'},
 {'id':'VC-GRAMMAR-04','topic':'핵심 수치와 차트 강조','observed':'계약 매출은 주황색으로 구별. 지원은 BIM 설계의 큰 구획과 약82% 도넛을 함께 강조.','role_hypothesis':'한 장면에서 기억할 핵심과 나머지 내역을 구분한다.','variation_rule_proposed':'금액 총량/구성 우세/산정 기준 중 현재 장면의 주장을 먼저 정하고 면적·색·차트를 함께 조절. 차트 종류를 무조건 고정하지 않음.','omission_cost':'동일 크기의 행 목록은 핵심 구성 비중을 약하게 만들 수 있음.'},
 {'id':'VC-GRAMMAR-05','topic':'입체적 도상과 수치','observed':'계약의 동전·문서·상승 막대/화살표와 윤곽·명암이 있는 큰 금액. 실제 3D 제작 여부는 모름.','role_hypothesis':'경제성과·계약업무를 빠르게 연상시키고 밝은 기술 홍보 분위기를 만든다.','variation_rule_proposed':'의미에 맞는 도상과 일관된 입체감/명암을 선택. 수치를 가리거나 과장하는 위치는 피함. 원본 제작법을 확인 없이 지정하지 않음.','omission_cost':'평면 숫자만 남기면 정보는 남아도 원본의 시각적 성격은 달라짐.'}
]
write(O/'review-decision.json',{'utc':datetime.now(timezone.utc).isoformat(),'user_selection':'원본 기록과 새 화면 함께 검토. 피드백으로 기준 보정. 실제 영상 제작 보류.','status':'review prepared; style preservation choice pending','protected_prior_files':pins,'active_skill_modified':False,'canonical_db_modified':False,'new_visual_proof_generated':False,'findings':findings,'source_grammar_candidates':grammar,'question':'원본 언어를 기본 유지 / 배치·표현 강하게 유지 / 정보 구조만 이식 / 같은 조건 두 스타일 비교','choice_status':'pending; no answer inferred'})
revised=copy.deepcopy(old)
revised['review_revision']={'id':'review-r1','parent_sha256':pins[0]['sha256'],'status':'proposed records for user review; does not replace original pilot','source_grammar_candidates':grammar,'pending_design_language_choice':True}
revised['cases'][0]['alternatives'][0]={'candidate':'원본의 가로 3구역을 16:9에 재사용','decision':'이전 시범에서 미선택; 일반적인 부적합 판정은 철회','reason':'원본도 매출을 주황색으로 강조하고 구역 너비/정보량이 다르다. 현재의 새 요약안과 전달 우열은 미검증.'}
revised['cases'][0]['review_note']='원본에 없던 매출 중심 위계라고 말하지 않는다. 새 배치는 원본의 위계를 다른 화면비와 요약 목적에 맞춰 바꾼 제안이다.'
revised['cases'][1]['review_note']='원본의 BIM 설계 약82% 강조를 별도로 보존한다. 현재 평면 4행안은 전체 내역 열람에 치우쳤으며 핵심 강조 전이는 미검증이다.'
for c in revised['cases']:
 c['source_grammar_links']=[g['id'] for g in grammar]
 c['style_transfer_status']='시각 언어의 기능/조합 기록 보완. 새 화면에서 그 언어를 구현·검증한 상태는 아님.'
 for link in c['links']:
  link['review_scope']='source role/flow interpretation and/or proposed adaptation; not an approved production template'
for p in revised['pattern_candidates']:
 p['readiness']='기록 후보. 사용 조건과 의미 관계의 논리 검토이며 자동 선택/실모션 재현 검증은 미완료.'
 if p['id']=='VC-MOTION-02':
  p['variant_distinction']={'source_observed':'원본 계약의 정보 구역 재배치와 보조 패널 추가','new_proposal':'핵심 매출의 위치 고정과 보조 카드 추가','not_equated':'같은 좌표/타이밍/곡선의 반복으로 검증하지 않음'}
write(O/'knowledge-cards.review-r1.json',revised)
write(O/'review-source-pins.json',{'files':pins,'evidence':[{'path':str(p),'sha256':sha(p)} for p in [P/'extraction/cases/VALUE/contract/f_03360_112.000.png',P/'extraction/cases/VALUE/project/f_04500_150.000.png',P/'proofs/A-state-5.png',P/'proofs/B-state-5.png']]})
assert all(sha(x['path'])==x['sha256'] for x in pins)
print('Review findings, grammar candidates and separate record revision saved; previous pilot unchanged.')
