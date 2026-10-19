from pathlib import Path
from datetime import datetime, timezone
import json, hashlib

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(name,v): (OUT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
decision=read(OUT/'decision.json')
def ev(phase,t):
 p=OUT/f'extraction/cases/VALUE/{phase}/f_{int(t*30):05d}_{t:07.3f}.png'
 assert p.exists(),p
 return {'source_seconds':t,'frame':str(p),'sha256':sha(p),'sampling_interval_seconds':2}

common={
 'status':'pilot proposal; not canonical pattern registration or company approval',
 'source_video':decision['video'],'target_scenario':decision['scenario'],
 'canonical_mapping':{'Case':'source case + evidence','Pattern':'LAY/FLOW/MOTION candidate','CasePatternLink':'order, co-occurrence and variant','DesignRule':'fit, protected/variable and negative input','Review':'proof, unresolved and user judgment'},
}
common['epistemic_rule']='관측 사실·기능 해석·새 설계 제안을 분리한다. 원제작 의도·제작 방법·미관측 곡선은 단정하지 않는다.'
common['source_visual_language']={
 'whole':'32:9의 넓은 화면. 밝은 여백과 상단 장 제목을 공통 골격으로 두고 장별 강조색, 입체적으로 보이는 업무 아이콘, 얇은 프레임의 정보면, 실적 사진을 결합한다.',
 'roles':['상단 장 라벨=현재 위치','큰 숫자=핵심 주장','밝은 정보면·가는 선=항목 묶음','실경·업무 이미지=맥락과 사례','입체적 아이콘=기술·경제활동 연상','장별 색=구분과 연속성'],
 'limits':'원본 폰트·3D 제작법·AE 효과·키프레임 원값은 미확인. 외형을 제작 방법으로 단정하지 않는다.'}
common['precision_policy']='전체 구성·요소 역할·상태와 전후 관계부터 기록한다. 정밀 측정은 차트 의미와 재사용 조건에 필요한 곳에 한정한다.'
common['migration']='기존 DB로 옮길 때의 대응안이다. 이번 ID는 로컬 후보이며 기존 패턴 18개를 등록·덮어쓰지 않았다.'
cases=[{
 'id':'VC-CASE-A','title':'계약: 산정에 쓰는 값과 참고값 구분','evidence_window':[78,116],
 'evidence':[ev('contract',t) for t in [78,84,96,102,110,112,116]],
 'observed':[
  '78~84초 표본: 수주·매출 막대와 금액, 문서·동전 계열 아이콘이 함께 나타난다. 원본 수주 17.5, 매출 12.9.',
  '86~96초 표본: 실경 배경 위 수주 구성 패널, 측량·R&D 도넛과 수치가 순차로 보강된다.',
  '98~112초 표본: 수주 정보가 왼쪽으로 정리되고 비용, 실제 매출 패널이 추가된다. 비용 100초 0.7→102초 8.7; 매출 110초 10.8→112초 12.9.',
  '112초 최종 표본: 수주·투입비용·실제 매출 세 묶음, 수주·매출 중복 제외 문구. 114초 이후 다음 BIM 맥락으로 전환.'],
 'design_inventory':{
  'layout':'초기 좌우 비교에서 정보 패널의 가로 확장으로 진행. 상단 장 제목, 가운데 주요 수치·구성, 배경 실경과 장식 아이콘의 층을 분리.',
  'typography':'제목/지표 이름/큰 금액/구성 비율/설명 문구의 위계. 원본 서체명·정확한 크기는 미확인.',
  'color_material':'녹색 장 강조, 흰 정보 패널, 얇은 프레임, 부드러운 입체 아이콘과 실경의 결합. 주황 계열 매출 막대도 관측.',
  'components':['장 라벨','금액+단위','수주 구성 도넛','비용 정보면','매출 정보면','중복 제외 문구','실경 배경','입체적 문서/동전/상승 화살표'],
  'spacing':'초광폭의 가로 여백을 정보 묶음 사이 경계로 사용. 세로 화면에서는 같은 가로 배열을 축소하지 않고 위계를 다시 배치해야 한다.'},
 'functional_interpretation':'금액을 늘어놓는 것보다 무엇을 성과로 셌는지 설명하는 장면으로 해석한다. 원제작 의도 확인이 아닌 새 설계를 위한 가설.',
 'links':[{'id':'VC-LAY-01','role':'주요 산정값과 참고값의 위계 분리'},{'id':'VC-FLOW-01','role':'맥락→주장→산정 기준→한계 설명'},{'id':'VC-MOTION-01','role':'숫자와 해당 시각 요소를 같은 의미 단위로 변화'},{'id':'VC-MOTION-02','role':'기존 핵심을 남기고 보조 정보 추가'}],
 'protected':['매출·수주·비용의 서로 다른 의미','실제 매출을 산정에 반영한다는 기준','금액의 단위·기간','합산·순이익 계산으로 읽히지 않는 관계'],
 'variable':['가로/세로 배치','색과 재질','아이콘·사진 사용 여부','도넛/막대/문장 중 적합한 수단','현재 과제에 불필요한 구성 내역 생략'],
 'target_brief':{'format':'16:9','task':'계약 부문 산정 기준 요약 한 화면. 원본 전체 계약 시퀀스의 대체 완성본은 아니다.','values':{'revenue':12.9,'orders_reference':17.6,'cost_separate':8.4},'decision':'실제 매출을 크게, 수주와 비용을 보조로 배치. 원본 녹색 계열과 밝은 정보면은 유지하되 입체 아이콘·실경·도넛은 이 요약안에서 유보.'},
 'alternatives':[{'candidate':'원본과 같은 동급 3패널','decision':'이번 요약에서는 제외','reason':'셋이 같은 성과값이거나 합산 대상처럼 읽힐 위험. 원본에는 순차 설명과 문구가 있지만 짧은 요약에는 그 맥락이 약함.'},{'candidate':'수주→비용→매출 화살표','decision':'제외','reason':'산식·변환·차감 관계로 오해할 여지. 이 자료는 손익 산정이 아님.'},{'candidate':'매출 중심+보조 지표','decision':'시범 선택','reason':'산정 역할을 위계로 드러냄. 숫자 정확성만으로 전달 성공을 입증하지는 못함.'}],
 'unresolved':[{'issue':'매출 구성 6.2+6.5=12.7인데 본문 총매출 12.9','blocks':'구성비 도넛의 확정 제작','action':'총액은 변경안 그대로 사용. 임의의 기타 0.2를 만들지 않고 이번 요약에서는 구성 도넛 유보.'},{'issue':'정확한 가감속·등장 시작 프레임 미확인','blocks':'원본 동작 복원','action':'이번은 의미 순서 기반 새 동작 제안. 필요 시 해당 짧은 구간만 추가 관측.'}]
},{
 'id':'VC-CASE-B','title':'프로젝트 지원: 같은 총액의 다른 분류','evidence_window':[126,174],
 'evidence':[ev('project',t) for t in [130,134,140,146,150,160,172]],
 'observed':[
  '128~136초 표본: 장 도입 뒤 가족사 로고, 프로젝트 요청/전문인력 지원 방향 화살표, 기술개발센터 업무 이미지가 연결된다.',
  '138~142초 표본: 큰 23.7억원·26건 수치 화면으로 바뀐다.',
  '144~154초 표본: 대각 분할 전환 뒤 왼쪽 업무 실경, 오른쪽 유형별 금액·건수와 BIM 설계 82% 도넛이 구성된다.',
  '156~174초 표본: 별도 매출이 아닌 비용절감 맥락을 사진과 문장으로 설명한 뒤 가족사·건축 이미지와 23.7억원을 다시 제시한다.'],
 'design_inventory':{
  'layout':'넓은 참가자 관계도→단일 큰 수치→사진/분류 정보의 분할→설명/실적 사진→요약. 장면의 역할이 바뀔 때 배치도 바뀜.',
  'typography':'큰 총액을 기준점으로 두고 분류 라벨·금액·건수를 구별. 건수와 금액은 다른 단위.',
  'color_material':'동색/구리색 장 강조, 밝은 바탕, 입체적으로 보이는 업무·건축 아이콘, 실제 프로젝트 사진, 얇은 정보 경계.',
  'components':['가족사 로고','요청/지원 연결 화살표','센터 업무 이미지','총액·건수','실적 사진','유형별 행과 막대','비중 도넛','비용절감 설명'],
  'spacing':'넓은 화면에서 실적 사진과 수치를 동시에 보여줌. 세로안은 총액 위치를 고정하고 분류를 순서대로 교체해 밀집을 줄임.'},
 'functional_interpretation':'누가 무엇을 지원했는지 맥락을 만든 뒤 총량, 구성, 산정의 의미를 설명하는 흐름으로 해석. 가족사별 분류는 변경 시나리오에서 새로 요구된 축.',
 'links':[{'id':'VC-LAY-02','role':'총액을 고정하고 하위 분류를 교체하는 새 변형'},{'id':'VC-FLOW-01','role':'맥락→주장→구성 근거→한계 설명'},{'id':'VC-MOTION-01','role':'금액/막대를 같은 의미 단위로 변화'},{'id':'VC-MOTION-03','role':'분류 기준이 바뀔 때 제목과 내용 동시 교체; 새 설계 제안'}],
 'protected':['총액 22.2억원과 27건은 다른 단위','가족사별과 업무유형별은 같은 총액의 두 분류','직접 매출이 아닌 실제 투입비용/외부 대체비용 관점','막대 비교의 공통 기준'],
 'variable':['한 번에 보여줄 분류 수','화면비와 패널 방향','사진·입체 아이콘 사용','장 색의 변형','세부 행 등장 간격'],
 'target_brief':{'format':'9:16','task':'수정된 총액과 두 분류를 작은 화면에서 순서대로 설명. 원본 32:9 단순 축소가 아니다.','values':{'total':22.2,'count':27,'companies':[15.5,6.7],'types':[18.2,1.5,1.2,1.3],'type_counts':[5,7,1,14]},'decision':'총액·단위를 고정하고 아래에서 가족사별→유형별 분류로 전환. 구리색 장 분위기와 명확한 수치 위계는 유지.'},
 'alternatives':[{'candidate':'가족사·업무유형 6행 한 번에 배치','decision':'이번 세로안에서 제외','reason':'서로 다른 분류를 한 목록으로 오해하거나 작은 글자가 될 위험.'},{'candidate':'각 분류마다 총액을 새로 크게 등장','decision':'제외','reason':'서로 다른 성과가 추가되는 인상을 줄 수 있음.'},{'candidate':'총액 고정+분류 교체','decision':'시범 선택','reason':'같은 값의 관점 변경을 공간적 연속성으로 설명. 실제 재생과 이해도는 미시험.'}],
 'unresolved':[{'issue':'두 분류 전환이 실제 재생에서 명료한지','blocks':'이해도 검증 완료 판정','action':'정지 스토리보드 검토 후 짧은 모션으로 확인.'},{'issue':'원본 전환·곡선의 정확한 타이밍','blocks':'원본 모션 복원','action':'현재 2초 표본으로는 단정하지 않는다.'}]
}]
patterns=[
 {'id':'VC-LAY-01','category':'layout','origin':'source-derived role, transformed layout','rule':'산정에 반영한 값을 중심에 두고 참고/별도값은 구역과 크기로 분리','fit':'동일 단위여도 산정 역할이 다른 지표 요약','negative_input':'매출·비용으로 순이익을 계산하는 공식 설명','negative_decision':'이 배치만 재사용하면 관계를 숨김. 명시적 산식/연결 구조를 새로 선택.'},
 {'id':'VC-LAY-02','category':'layout','origin':'new adaptation to revised script','rule':'같은 총액은 고정, 분류 패널만 교체','fit':'상호 다른 축으로 동일 집계를 설명','negative_input':'한맥 1~6월과 삼안 1~9월처럼 기간/모집단이 다름','negative_decision':'동일 총액 패턴 적용 거절. 기간/모집단을 먼저 분리.'},
 {'id':'VC-FLOW-01','category':'overall_flow','origin':'source sequence interpreted','rule':'맥락→주장→근거/구성→산정 한계→요약','fit':'성과 수치가 무슨 의미인지 설명하는 보고 장면','negative_input':'긴급 공지나 한 줄 슬로건만 전달하는 3초 장면','negative_decision':'모든 단계를 강제하지 않고 핵심 메시지 중심 흐름 선택.'},
 {'id':'VC-MOTION-01','category':'detail_motion','origin':'source samples show changing numbers and chart states','rule':'수치와 막대/비율/라벨을 같은 의미 상태로 맞춤','fit':'누적 변화나 구성 비중을 설명할 때','negative_input':'계약번호 0017 또는 날짜 2026-09-30','negative_decision':'중간 숫자가 거짓 의미를 만듦. 카운트업 제외, 확정 문자열로 등장.'},
 {'id':'VC-MOTION-02','category':'detail_motion','origin':'source panel addition; adapted semantic anchor','rule':'핵심 정보는 남기고 별도 정보가 들어오는 자리를 마련','fit':'동일 맥락에서 설명이 누적될 때','negative_input':'기간이 바뀌는데 이전 총액을 같은 위치에 계속 둠','negative_decision':'핵심값 고정 거절. 기간과 값의 교체를 함께 표시.'},
 {'id':'VC-MOTION-03','category':'detail_motion','origin':'new proposal, not source-observed','rule':'분류 제목과 그 분류에 속한 행을 함께 교체하고 총액 유지','fit':'동일 집계의 분류 기준을 바꾸는 새 세로안','negative_input':'가족사 합계와 유형 합계가 다른 자료','negative_decision':'제작 보류. 누락/범위 차이 확인 전 같은 총액으로 전환하지 않음.'}
]
write('knowledge-cards.json',{'common':common,'cases':cases,'pattern_candidates':patterns,'negative_case_status':'위 반례는 구체적 입력을 작성해 적용/거절을 논리 검토한 것. 실제 영상·독립 모델·사용자 시험은 미실행.'})
ledger=[('수주',17.5,17.6,'억 원'),('계약 투입비용',8.7,8.4,'억 원'),('계약 매출',12.9,12.9,'억 원'),('프로젝트 지원',23.7,22.2,'억 원'),('프로젝트 건수',26,27,'건'),('BIM 설계',19.4,18.2,'억 원'),('BIM 설계 건수',3,5,'건'),('BIM 지원',1.6,1.5,'억 원'),('해외사업 지원',1.3,1.2,'억 원'),('디자인 지원',1.4,1.3,'억 원'),('디자인 건수',15,14,'건'),('S/W 서비스',11.5,13.1,'억 원'),('경영지원',7.4,7.5,'억 원'),('전체',55.5,55.7,'억 원')]
write('numeric-baseline-ledger.json',{'policy':'원본 영상은 디자인·모션 근거. 새 화면 내용은 변경 시나리오 우선. 차이는 OCR 오류로 취급하지 않는다.','records':[dict(zip(['metric','observed_video','target_scenario','unit'],x)) for x in ledger],'input_issues':['계약 매출 구성 6.2+6.5=12.7, 총액 12.9와 차이. 기타 항목을 임의로 만들지 않음.','4부문 합 12.9+22.2+13.1+7.5=55.7. 이 보고서는 회사의 산정 방법 타당성을 별도 검증한 회계 보고서가 아님.']})
roles=read(ROOT/'direction-reassessment-20261019/source-role-reassessment.json')['records']
uses={
 'P1':'동급 3카드/화살표/매출 중심 후보를 비교해 작은 구조 변형을 선택. 쉬운 구현 자체를 선택 근거로 삼지 않음.',
 'P4':'어떤 배치가 합산/순이익 오해를 만드는지 구체적으로 비평.',
 'R1':'실제 원본 프레임과 기능 해석, 새 제안을 구분.',
 'R2':'미상마다 막히는 사용을 한정. 곡선 미상은 새 배치 시범을 막지 않음.',
 'R3':'원본·시나리오 버전, 프레임 근거와 수치 차이 원장을 유지.',
 'R6':'근거 있는 표본 범위와 새 결과의 시험 범위를 별개로 기록.',
 'I2':'전체 화면의 위계·맥락·재질·변형을 검토. 픽셀 목록을 디자인 판단의 대체물로 쓰지 않음.',
 'G1':'선택 대안과 제외 이유를 화면 수준으로 제시.',
 'M1':'Case/Pattern/연결/조건/검토의 기존 개념에 대응. 새 정본 DB를 중복 생성하지 않음.',
 'A1':'수치·관계의 논리 검토, 실제 가독성, 모션 재생, 사용자 이해 검증을 분리.'}
write('research-application.json',{'status':'이번 시범에서 적용한 판단 방식과 산출물 연결. 상류 코드 전수 실행이나 모든 조사 스킬 반영 완료가 아니다.','records':[{**r,'pilot_application':uses[r['source_id']]} for r in roles if r['source_id'] in uses],'excluded':['전역 훅/자동 활성화','코드 심볼 맵 구현','바이너리 역설계 절차의 영상 전면 이식','웹 UI의 고정 시간·요소 수 규칙','포니테일 벤치마크 절감률을 영상 효과로 사용','픽셀 차이만으로 응용 설계 성공 판정']})
write('motion-proposals.json',{'status':'static storyboard and new motion direction; not original timing or rendered animation','A':{'duration_proposed':14,'flow':'분류 기준→주 매출→참고 수주→별도 비용→중복/손익 한계→유지','detail':['핵심 매출 위치를 유지하고 보조 카드만 부드럽게 등장','장식성 카운트업 없이 확정 금액부터 제시하는 안을 우선','카드/라벨/금액은 같은 묶음으로 이동, 하단 설명은 읽을 시간을 확보'],'curve':'단조 감속 제안. 원본 곡선에서 측정한 값 아님. 튀는 반동은 현재 정보 역할에 근거가 없어 유보.'},'B':{'duration_proposed':20,'flow':'지원 맥락→총액/건수→가족사별→총액 유지하며 분류 교체→유형별→중복 제외 설명','detail':['제목과 해당 분류 행은 함께 교체','총액·단위·기간은 전환 동안 같은 위치에 유지','유형별 막대는 모두 22.2를 기준으로 비교, 건수는 막대 길이에 사용하지 않음'],'curve':'분류 패널의 짧은 교체와 행별 순차 등장 제안. 정확한 길이·겹침·음성 동기화 미확정.'},'scope':'두 요약 장면의 로컬 시간 제안. 변경 시나리오 전체를 14초/20초에 낭독하는 계획이 아님.'})

checks=[]
def check(name,ok):
 assert ok,name
 checks.append({'check':name,'result':'confirmed within stated scope'})
sc=read(OUT/'effective-scenario.json')
check('blue-right on pages 2/3/4; retain-left on 1/5/6',[x['decision'] for x in sc['pages']]==['retain_left_original']+['use_right_blue_revision']*3+['retain_left_original']*2)
check('project family and type sums match one total',round(sum([15.5,6.7]),1)==22.2 and round(sum([18.2,1.5,1.2,1.3]),1)==22.2)
check('project type count total',sum([5,7,1,14])==27)
check('contract breakdown inconsistency retained',round(6.2+6.5,1)!=12.9 and bool(cases[0]['unresolved']))
proof=read(OUT/'proof-index.json')
check('all 12 static proof frames pinned',len(proof['frames'])==12 and all(sha(x['path'])==x['sha256'] for x in proof['frames']))
check('actual animation not claimed',proof['actual_motion_rendered'] is False)
audit=read(ROOT/'direction-reassessment-20261019/current-audit.json')
check('protected draft9 skill files unchanged',all(sha(Path(audit['active_skill'])/x['relative'])==x['sha256'] for x in audit['protected_active_files']))
check('research evidence files remain pinned',all(sha(r['local_path'])==r['sha256'] for r in roles if r['source_id'] in uses))
write('validation.json',{'utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'meaning':'문서·수치 관계·보존 대상의 확인이다. 디자인의 독립 평가나 영상 이해도 시험은 아니다.','unverified':['전편 정밀 분석','음성 청취·전사','실제 모션·음성 동기화','사용자 이해도·브랜드 적합성','DB 검색을 통한 자동 선택'],'passed':True})
print('knowledge records, numeric ledger, research mapping and scoped validation written')
