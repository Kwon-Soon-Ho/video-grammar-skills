from pathlib import Path
import json,re

O=Path(__file__).resolve().parent
def read(n):return json.loads((O/n).read_text(encoding='utf-8'))
def write(n,s):(O/n).write_text(s,encoding='utf-8')
def dump(n,d):write(n,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def link(label,p):return f'[{label}](<{Path(p).as_posix()}>)'
def local(label,n):return link(label,O/n)
K=read('knowledge_snapshot.json'); E=read('evidence.json')
C1='RC-CASE-001';C2='RC-CASE-002'
L1='RC-LAYOUT-001@v1'; L2='RC-LAYOUT-002@v1'
def comp(n):return f'RC-COMP-{n:03d}@v1'
cases=[
{'id':C1,'time_seconds':134,'title':'역할판 사이의 프로젝트 요청·전문인력 지원','evidence_ids':['E1'],
 'information_relation':'가족사 사업 → 기술개발센터 전문인력 참여: 프로젝트 요청. 반대 방향: 전문인력 지원. 화살촉·문구로 확인되는 도식 관계이며 움직임 방향이 아니다.',
 'composition':'크림 공간의 좌우 흰 유광 역할판과 중앙 관계 여백. 좌 2열×4행 회사 타일, 우 역할 헤더→BIM 두 항목→모니터 업무 묶음. 청색/녹색 모서리와 도상, 가는 구분선, 바닥 반사로 묶인다.',
 'inferred_function':'두 주체의 다른 역할과 요청·지원의 상호 관계를 읽게 하는 구성이라는 기능 해석. 원제작 의도 확인 없음.',
 'unknowns':['U-MOTION','U-INTENT','U-IMPLEMENTATION','U-DISPLAY'], 'layout_id':L1},
{'id':C2,'time_seconds':172,'title':'23.7억원 성과값·회사열·센터 건물 무대','evidence_ids':['E2'],
 'information_relation':'실제 투입한 인력과 비용을 기준으로 23.7억 원을 가치창출성과로 산정했다는 화면 설명. 회사별 배분액·매출액이나 산정 타당성의 근거는 아니다.',
 'composition':'왼쪽 금색 대형 수치와 설명, 중앙 원근 8회사열/투명판/곡선 받침, 오른쪽 건물/원형 기단과 위·좌·우·앞 명찰. 크림·금색 실내, 짙은 녹색 유리와 따뜻한 창빛, 바닥 반사·금빛 곡선.',
 'inferred_function':'성과 규모·관련 회사 집단·센터 지원 범위를 함께 읽게 한다는 추론. 회사열과 수치의 산술 관계는 미확정.',
 'unknowns':['U-MOTION','U-INTENT','U-IMPLEMENTATION','U-DISPLAY','U-ASSET','U-LOGO'], 'layout_id':L2}]

nodes=[]
def node(id,name,kind,definition,aliases,conditions,unverified,subcomponents=None):
 nodes.append(dict(id=id,name=name,kind=kind,definition=definition,aliases=aliases,conditions=conditions,unverified=unverified,subcomponents=subcomponents or [],status='local_candidate_not_canonical',definition_source='preserved/01_부품과조합.md',detail_source='preserved/02_전체상세.md'))
node(L1,'좌우 역할판과 요청·지원 관계','layout','양쪽 역할판과 중앙 반대 방향 화살표. 상부 장 표식·제목, 판 내부 역할 도상·설명·회사격자/업무 묶음의 위계를 보존한다.',['역할판','역할 패널','가족사 사업','전문인력 참여','요청 지원'],'주체·방향·문구를 함께 유지. 단방향 절차·순위표로 바꾸면 관계가 달라진다.','다른 화면비·항목 수·실제 모션 적용 미시험')
node(L2,'성과값·회사열·기관의 가로 무대','layout','좌 성과수치·중앙 회사열·우 건물/명찰. 투명 판·곡선 받침·단상·빛으로 깊이를 구성한다.',['성과 무대','기관 배치'],'수치 단위와 산정 설명 보존. 회사별 기여액 비교로 읽지 않는다.','단일 관측, 회사 수 증가·새 화면비의 가독성 미시험')
node(comp(1),'장 표식','component','금갈색 육각 배지의 2/TDC와 오른쪽 장 문구.',['장 배지','TDC'],'작은 상위 맥락 표식과 주정보 위계를 구분한다.','픽셀 완전 동일·지속 표시·전 장 통일 규칙 미확인')
node(comp(2),'회사 로고 타일','component','흰 유광 둥근 판 위 고유색 도상과 회사명. 타일과 그 배치 컨테이너를 구분한다.',['로고','8회사','HALLA','피티씨','2열 4행','원근 가로열'],'명칭·정체 보존, 배치/문구/타일 비율을 변형 조건으로 관리.','동일 편집 자산·정식 법인명·사용 권한·E2 작은 부속문구 일부 미확정')
node(comp(3),'역할 헤더','component','광택 원형 도상 왼쪽+굵은 역할명 오른쪽+가는 밑선+작은 회색 설명.',['역할판','역할 헤더','건물 도상','사람 3명'],'좌 청색 건물/가족사와 우 녹색 세 사람/전문인력의 도상·문구 차이 보존.','같은 헤더 구성 가족이며 동일 아이콘·모핑·자산은 미확인')
node(comp(4),'방향 라벨 화살표','component','곡선 몸체·화살촉·흰 알약 라벨·광택 테두리.',['프로젝트 요청','전문인력 지원','파랑 오른쪽','녹색 왼쪽'],'방향 변경 시 주체와 문구를 함께 대조.','이동·드로온·밝기 변화·주기·이징 모두 미관측')
node(comp(5),'지원 서비스 명찰','component','건물 주변에 독립 배치된 흰 유광 둥근 사각 명찰.',['지원 명찰','서비스판','BIM 지원','BIM 설계','디자인 지원','해외사업 지원'],'중심 기관의 서비스 범주 표식 후보. 건물/기단에 내부 구성으로 흡수하지 않는다.','전체 업무 목록·서비스 순위·건물의 실제 업무 위치·시간 중첩 미확인')
node(comp(6),'성과 수치 조형','component','금색 입체 23.7억원+뒤 큰 옅은 동일 윤곽+잎 가지+바닥 반사.',['23.7','수치','금색'],'단위·화면 설명 보존. 수치가 강조용 주정보인 경우 후보.','단일 사용처, 값/단위 교체·카운트업·잔상 동작 미시험/미관측')
node(comp(7),'업무 이미지 묶음','bundle','모니터 3대·선반·책 2묶음·양끝 화분 2개의 조합. 중앙 모니터가 크고 앞으로 겹친다.',['업무 묶음','업무이미지','모니터 묶음','업무 이미지 묶음'],'업무 장면을 보여주는 후보라는 추론. 화면 이미지·소품을 바꾸어도 중심/보조 관계와 정보판 하부의 배치 대응 검토.','특정 소프트웨어·프로젝트 정체·분리 자산·교체 가독성 미확인', ['왼쪽 평면 도면 모니터/받침','중앙 건물 와이어프레임 모니터/받침','오른쪽 지도·건축 이미지 모니터/받침','선반','책 더미 2묶음','화분 2개'])
node(comp(8),'기관 건물·기단 묶음','bundle','흰색·짙은 녹색 유리의 TDC/기술개발센터 건물과 원형 단상.',['건물/기단','건물 기단','기관 묶음','센터 건물','건물·기단'],'기관을 중심으로 서비스 명찰을 따로 배치. 기관과 지원 범위를 묶어 읽게 하는 후보라는 추론.','실제 사옥 재현·같은 자산·창 내부 동작·기관 교체 적합성 미확인',['건물 매스/외벽','창과 따뜻한 내부빛/실루엣','기관 표기','출입부','옥상·주변 조경','원형 기단'])

uses=[]
def use(n,c,e,where,diff,relations,knowledge):
 uses.append(dict(id=f'USE-{len(uses)+1:03d}',definition_id=n,case_id=c,evidence_ids=e,scope=where,current_difference=diff,spatial_relations=relations,knowledge_ids=knowledge,temporal_relation='unobserved',same_asset='unverified'))
use(L1,C1,['E1'],'전체','E2의 가로 무대와는 다른 레이아웃. 한 번 본 후보.',['contains 회사격자·역할헤더·중앙화살표·업무묶음'],['LAYOUT-SPLIT','LAYOUT-NETWORK','KNOW-LAYOUT-SPLIT','KNOW-LAYOUT-NETWORK','STYLE-DIAGRAM','STYLE-3D'])
use(L2,C2,['E2'],'전체','E1과 크림/유광 외형 가족을 공유하나 동일 레이아웃 아님.',['contains 수치·회사열·건물/기단·주변명찰'],['KNOW-LAYOUT-SPACE-CALLOUT','STYLE-3D','SCREEN-DATA'])
for c,e in [(C1,'E1'),(C2,'E2')]:use(comp(1),c,[e],'좌상','2/TDC와 장 문구 외형 반복. 지속 표시 과정은 모름.',['accompanies 전체 배치'],['IP-02','SCREEN-HIERARCHY'])
use(comp(2),C1,['E1','e1_logos'],'왼쪽 역할판','2열×4행, 행 우선 5번째 피티씨·6번째 HALLA. 가로형 타일.',['anchors_to 왼쪽 정보판 내부'],['LAYOUT-CARD-GROUP','KNOW-LAYOUT-CARD-GROUP','REL-PARALLEL','SCREEN-GROUP'])
use(comp(2),C2,['E2','e2_logos'],'중앙 회사열','왼쪽→오른쪽 5번째 HALLA·6번째 피티씨로 교환. 세로형 타일·원근 가로열·금색 받침. 작은 부속문구는 일부 흐림.',['anchors_to 곡선 받침','overlaps 잎·투명판'],['KNOW-LAYOUT-CARD-GROUP','SCREEN-GROUP','MR-03','Q-BRAND-01'])
use(comp(3),C1,['E1','e1_roles'],'양쪽 역할판 상부','좌 건물 도상/청색/가족사 사업, 우 3명/녹색/전문인력 참여. BIM 두 항목은 우 헤더 아래 별도 하위 영역.',['anchors_to 판 내부 상부','accompanies 업무묶음'],['SCREEN-HIERARCHY','SCREEN-GROUP','AP-03'])
use(comp(4),C1,['E1','e1_arrows'],'두 판 사이','위 파랑 요청→오른쪽, 아래 녹색 지원→왼쪽. 문구가 각 몸체 위 흰 라벨에 귀속.',['anchors_to 중앙 여백','accompanies 양쪽 역할판'],['KNOW-LAYOUT-NETWORK','SCREEN-COLOR','Q-INFO-02'])
use(comp(5),C2,['E2','e2_building'],'건물 위/좌/우/앞','위 BIM 지원·좌 BIM 설계·우 디자인 지원·앞 해외사업 지원. E1의 BIM 도상+아래 문구와 같은 부품으로 합치지 않음.',['anchors_to 건물','overlaps 건물 외곽 일부','accompanies 건물/기단'],['LAYOUT-SPACE-CALLOUT','KNOW-LAYOUT-SPACE-CALLOUT','IP-04','SCREEN-GROUP'])
use(comp(6),C2,['E2','e2_value','e2_number'],'왼쪽 수치 전경','한 시각의 23.7억원과 뒤 옅은 윤곽. 윤곽의 시간 변화 해석 유보.',['accompanies 설명문·잎가지','overlaps 바닥 반사'],['AP-03','SCREEN-DATA','MR-08','Q-INFO-04'])
use(comp(7),C1,['E1','e1_work'],'오른쪽 정보판 하부 전경','중앙 큰 모니터가 양옆보다 강조되고 선반/소품이 판 하부와 겹침. E2에는 이 묶음이 보이지 않음.',['anchors_to 오른쪽 정보판 하부','accompanies 역할헤더','overlaps 정보판 하부'],['SCREEN-HIERARCHY','SCREEN-GROUP','AP-03','KNOW-LAYOUT-UI-ANNOTATION'])
use(comp(8),C2,['E2','e2_building'],'오른쪽 중심 대상','건물과 기단의 단일 관측. 4명찰은 별도 RC-COMP-005@v1이고 E1 업무 묶음과 같은 대상으로 분류하지 않음. 원자산 동일성 검증은 아님.',['anchors_to 원형 기단','accompanies 지원명찰'],['STYLE-3D','LAYOUT-SPACE-CALLOUT','KNOW-LAYOUT-SPACE-CALLOUT','IP-04'])

reviews=[]
def review(id,target,criteria,ev,verdict,confirmed,remaining):
 reviews.append(dict(id=id,target_ids=target,criteria_ids=criteria,evidence_ids=ev,review_object='analysis_record',reviewer='this execution analysis agent; self review',method='provided PNG full view plus crop readback where listed',progress='reviewed_with_scope',verdict=verdict,confirmed=confirmed,remaining=remaining,company_approval=False))
review('REV-01',[C1,comp(4)],['Q-INFO-02'],['E1','e1_arrows'],'통과','파랑 프로젝트 요청의 오른쪽 화살촉과 녹색 전문인력 지원의 왼쪽 화살촉·문구가 기록과 대응한다.','정적 도식 귀속에 한정. 이동·순환·이징은 미관측.')
review('REV-02',[C2,comp(6)],['Q-INFO-02'],['e2_value','e2_number'],'통과','실제 투입한 인력과 비용 기준, 23.7억 원, 가치창출성과로 산정했다는 화면 문구와 큰 수치 대응 확인.','실제 산정의 타당성·최종 확정액·시나리오/음성 일치는 미검수.')
review('REV-03',[C1,comp(3)],['Q-INFO-02','Q-TEXT-01'],['E1','e1_roles'],'통과','우 역할명/설명, 3명 도상, 큐브 BIM 설계/모니터 BIM 지원이 기존 기록과 대응한다. 좌 헤더는 전체 PNG에서 확인.','전체 영상의 모든 문자·법인 등기명·폰트명 검수 아님.')
review('REV-04',[C2,comp(5),comp(8)],['Q-INFO-02','Q-SCREEN-01'],['e2_building'],'통과','정면 TDC/기술개발센터 및 위 BIM 지원·좌 BIM 설계·우 디자인 지원·앞 해외사업 지원과 주변 배치가 기록에 대응한다.','서비스의 실제 범위·우선순위·건물 업무 위치는 미확인.')
review('REV-05',[C1,C2,comp(2)],['Q-TEXT-01'],['e1_logos','e2_logos'],'통과','8개 핵심 도상/이름 대응과 피티씨/HALLA 5·6번째 순서 교환, 격자→원근 가로열 차이를 확인. 장헌과 장헌산업을 구별한다.','E2 작은 부속문구는 일부 흐림. E1 전체 전사를 E2 독립 판독으로 옮기지 않음.')
review('REV-06',[C1,C2,comp(2)],['Q-BRAND-01'],['e1_logos','e2_logos'],'판단보류','화면상의 고유색 로고·명칭은 수집했다.','편집 원본 자산ID/허용 사용형/보호공간과 현재 적용 버전 대조가 없어 회사 CI 준수 확정 불가. 기존 자료 최신성 재질문은 하지 않음.')
review('REV-07',[C1,comp(7)],['Q-SCREEN-01'],['E1','e1_work'],'통과','3모니터·큰 중앙 화면·선반·2화분·책 2묶음·판 하부 겹침이 기존 묶음 정의와 대응한다.','수집 기록의 관계 정확성에 한정. 실제 대상 시선·전달 성공이나 교체 가독성 검증은 아님.')
review('REV-08',[C1,comp(7)],['Q-SCREEN-06'],['e1_work'],'판단보류','왼쪽 도면·중앙 건물 와이어프레임·오른쪽 지도/건축 이미지의 형태 관측은 유지.','제품 버전/실제 UI/프로젝트 출처가 없어 특정 소프트웨어 조작·기능 데모로 확정하지 않음.')
review('REV-09',[C1,L1],['Q-INFO-03'],['E1'],'통과','두 판은 다른 주체의 요청·지원 관계. 공통 항목·척도의 우열 비교 또는 단방향 절차로 기록하지 않았다.','공간 도식의 의미 분류에 한정. 현실 업무 인과·실제 절차 전체는 미확인.')
review('REV-10',[C2,L2,comp(6)],['Q-INFO-03'],['E2','e2_value'],'판단보류','성과액·회사열·기관이 동반하며 산정 기준 설명이 보임.','회사별 금액 분배·순위·금액의 실증 근거는 미제공. 금빛 선만으로 재정/업무 인과를 확정할 수 없음.')
review('REV-11',[C1,C2],['Q-TRUST-01'],['E1','E2'],'통과','두 PNG 7680×2160과 SHA 확인, 8개 ROI의 원본 좌표와 crop-only 변환 보존. 제공된 PNG/기록 대조 범위의 출처 연결 확인.','MP4 해시·PTS 매핑·오디오/시나리오 독립 확인은 보류. 입력의 시각 메타데이터를 신뢰한 정적 사례이다.')
review('REV-12',[C1,C2],['Q-TRUST-02'],['E1','E2'],'통과','관측·기능 추론·미관측을 구분하고 단일 사례 후보·반복 외형·동일 자산·정본 등록을 분리한다.','제작 의도/AE 구현/회사 공통 규칙은 현재 확정하지 않음. 사람 검수·독립 검수 아님.')
review('REV-13',[C1,C2,L1,L2],['Q-MOTION-01'],['E1','E2'],'판단보류','38초 떨어진 두 표본의 정적 구도를 보존함.','등장/완성/유지/퇴장 시간·음성·실제 시청 환경이 없어 충분한 읽기 시간과 전체 흐름을 판정할 수 없음.')
review('REV-14',[C2,comp(6)],['Q-INFO-04'],['e2_number'],'판단보류','23.7억원과 큰 옅은 윤곽의 동시 가시성 확인.','수치 시간 변화·실측/연출 중간값·잔상/카운트업 여부가 미관측.')
review('REV-15',[C1,C2,L1,L2],['Q-SCREEN-07'],['E1','E2'],'판단보류','제공 PNG 32:9의 전체 구도를 유지하며 ROI는 보조로 연결함.','최종 출력/재생 환경·오버레이·다른 화면비가 없어 해당 환경의 잘림/가림·최종 가독성 판정 보류.')

connections=[]
def conn(target,ids,axis,reason,result,limits):
 connections.append(dict(id=f'KL-{len(connections)+1:03d}',target_id=target,knowledge_ids=ids,axis=axis,classification_reason=reason,current_result=result,limits=limits,basis_kind='analyst_classification_or_review_link_not_source_intent'))
conn(L1,['LAYOUT-SPLIT','LAYOUT-NETWORK','KNOW-LAYOUT-SPLIT','KNOW-LAYOUT-NETWORK'],'layout','다른 역할의 좌우 두 판이 중앙 요청/지원 연결을 공유한다.','분할+연결 복합 후보. 단순 반반 모양보다 관계를 우선함.','분할 비교 조건인 동등 항목/척도가 없어 KNOW-LAYOUT-SPLIT-COMPARE는 이번 분류에서 제외. 시간 절차로도 확정하지 않음.')
conn(comp(2),['REL-PARALLEL','LAYOUT-CARD-GROUP','KNOW-LAYOUT-CARD-GROUP'],'information_relation_and_layout_separate','회사들을 같은 역할의 타일로 나열하며 순위·정량척도는 표시하지 않음.','회사 목록의 병렬 관계 후보와 카드 외형 분류를 별도 축으로 연결. 2×4는 격자 형태 설명이며 별도 정보관계 ID가 아님.','병렬 정보가 동시 등장함을 뜻하지 않으며 순서 교환이 이동 모션의 증거가 아님.')
conn(comp(3),['SCREEN-HIERARCHY','SCREEN-GROUP','AP-03'],'review_knowledge','도상→큰 역할명→설명/구분선→하부 내용의 위계가 관측됨.','REV-03에서 문구/도상 귀속, REV-07에서 업무묶음과의 공간 조합을 확인.','관련 원칙 연결을 원본 디자인 전체 품질 통과나 시선 효과 확인으로 확대하지 않음.')
conn(comp(4),['KNOW-LAYOUT-NETWORK','SCREEN-COLOR','Q-INFO-02'],'layout_and_quality','방향·색·문구가 다른 두 요청/지원 관계를 표현함.','REV-01의 화살촉/문구 귀속 통과.','색의 역할 관측은 대비 계산·CI색 공식 확인이 아님. 미관측 모션 역할은 부여하지 않음.')
conn(comp(7),['AP-03','SCREEN-HIERARCHY','SCREEN-GROUP'],'review_knowledge','중앙 큰 모니터와 좌우 보조 모니터·소품을 한 전경 묶음으로 찾을 가치가 있음.','독립 검색 후보는 기존 RC-COMP-007@v1 유지. 소품은 하위 구성. REV-07 관계 대조.','기능 해석은 업무 역량의 시각화 후보라는 추론. 전달 효과나 동일 자산을 입증하지 않음.')
conn(comp(7),['KNOW-LAYOUT-UI-ANNOTATION','Q-SCREEN-06'],'rejected_or_held_classification','모니터가 있어 실제 제품 UI인지 검토했으나 출처/버전이 없음.','실제 UI와 설명 분류는 확정하지 않음. REV-08 판단보류.','도면/와이어프레임/지도·건축 이미지의 보이는 내용은 삭제하지 않음.')
conn(comp(8),['STYLE-3D'],'art_direction','입체 건물·기단·원근·반사·창빛이 보임.','3D 표현의 외관 후보.','렌더 도구·실제 3D 모델·AE 카메라·실재 사옥 확인 아님. 등각 투영이라고 단정하지 않음.')
conn(comp(5),['LAYOUT-SPACE-CALLOUT','KNOW-LAYOUT-SPACE-CALLOUT','IP-04','SCREEN-GROUP'],'layout_and_review','명찰이 한 기관 대상 주변에 대응되어 배치됨.','공간+설명표식의 배치 후보. REV-04 네 문구/위치 대조.','REL-SPACE의 시설 실제 위치 관계로는 태그하지 않음. 각 명찰의 실제 층/업무 위치가 아니라 화면 배치임.')
conn(L2,['KNOW-LAYOUT-SPACE-CALLOUT','SCREEN-DATA'],'composite_layout_and_review','큰 성과값·회사열·기관/서비스가 역할을 나누어 동반함.','금액 강조+회사 목록+기관 설명의 복합 무대, REV-02 전사 대응/REV-10 산술 관계 보류.','KNOW-LAYOUT-DATA-CHART는 축·분포·정량 부호가 없어 확정하지 않음. 수치가 있다는 이유로 차트로 분류하지 않음.')
conn(comp(6),['MR-08','Q-INFO-04'],'pending_motion_question','옅은 동일 숫자 윤곽이 시간 효과인지 검토가 필요함.','REV-14 판단보류 및 Q-MOTION-003으로 연결.','실제 숫자 변화·카운트업·잔상 모션 관측 없음.')
conn(L1,['STYLE-DIAGRAM','STYLE-3D'],'art_direction','주체·화살표 도식에 광택 판/바닥 깊이가 겹친 표현.','도식 구조+입체 외관의 복합 표현 후보.','표현언어는 정보관계·모션 기능 분류와 별개.')
conn(L2,['SCREEN-TIME-READ','AP-06','MP-02','MR-03','MR-07'],'unobserved_motion_questions','읽기 유지·동일 대상 연속성·연동·이징은 시간 표본이 필요함.','현재 Q-FLOW-001 및 Q-MOTION-001~003 조사 번호 유지. 적용 원칙 연결만 남기고 판정 보류.','모든 원칙을 의무 적용하거나 전체 흐름/FLOW 정의를 새로 만들지 않음.')

unknowns=[
{'id':'U-MOTION','kind':'미관측','scope':'두 시각 사이/앞뒤와 모든 대상의 등장·내부·주변·정착·퇴장','blocks':'FLOW/동작 패턴·시간 가독성·이징 판정','next':'MP4·시간 매핑을 확보할 때 기존 Q 조사 범위의 인접·경계 표본과 연속 재생 대조'},
{'id':'U-INTENT','kind':'미확인','scope':'원제작 의도·회사 문법','blocks':'공식 의도/회사 규칙 확정','next':'필요 시 제작자/권한 있는 담당자의 해당 버전/주장 확인'},
{'id':'U-IMPLEMENTATION','kind':'정밀 원값 미상','scope':'폰트·정확 색/효과·AE 키프레임·카메라/자산 분리','blocks':'원본 구현 복원/정확 자산 재활용','next':'편집 프로젝트·자산·선언된 디자인 자료 확보. 현재 외형 관측은 유지'},
{'id':'U-DISPLAY','kind':'미제공','scope':'실제 시청 환경·화면비 변환·오버레이·읽기 유지·오디오','blocks':'최종 가독성·자막/음향 싱크·새 화면비 적합성','next':'후속 제작/실영상 검수 요청 시 해당 출력 조건 확보'},
{'id':'U-ASSET','kind':'미확인','scope':'건물 실재 정체·업무묶음 소프트웨어·동일 원본 자산·지원 완전 목록','blocks':'실제 기관/기능 사실·자산 동일성','next':'원자산 또는 내용 담당 근거 필요'},
{'id':'U-LOGO','kind':'부분 판독 제한','scope':'E2 작은 로고 부속 글자','blocks':'E2 부속문구의 정밀 전사','next':'원자산/다른 선명 표본 확보. 8개 핵심 정체·배치는 현재 유지'}]
investigations=[{'id':id,'source':'preserved/04_모션조사.md','status':'investigation_not_registered_motion','case_ids':cs,'targets':ts} for id,cs,ts in [('Q-FLOW-001',[C1,C2],[L1,L2]),('Q-MOTION-001',[C1],[comp(4)]),('Q-MOTION-002',[C1,C2],[comp(2)]),('Q-MOTION-003',[C2],[comp(6),comp(8)])]]
data={'schema':'local-collection-lookup-1.0','status':'draft_local_collection_not_R4_registration','source_scope':'provided PNG at 134/172 seconds; prior records; no MP4/audio/continuous interval','canonical_write':False,'cases':cases,'definitions':nodes,'occurrences':uses,'knowledge_links':connections,'reviews':reviews,'unknowns':unknowns,'investigations':investigations,'evidence':E,'knowledge':K}
dump('index.json',data)

intro='# 134·172초 수집 기록과 조회 안내\n\n2026-10-19. 지정 draft.12로 수행한 동일 기존 자료의 제한 실행이다. **제공 PNG 두 화면의 정적 기록 대조와 지식 연결 초안**이며, 전편/연속 모션/회사 규칙/사람 승인/일반화 결과가 아니다. R4 정본 등록·스킬 변경 없음.\n\n읽는 순서: 사례 요약 → '+local('전체 상세와 기존 번호','01_수집기록.md')+' → '+local('현재 근거와 검수','02_지식연결과검수.md')+'. 검색은 '+local('조회 안내','03_조회색인.md')+'.\n'
for c in cases:
 intro+=f'\n## {c["id"]} — {c["title"]}\n\n- 정보 관계: {c["information_relation"]}\n- 전체 구도/디자인: {c["composition"]}\n- 기능 해석: {c["inferred_function"]}\n- 핵심 미상: 시간 흐름/동작/정확 구현 원값/실제 시청 효과.\n\n'+link('전체 PNG',next(e['path'] for e in E if e['id']==c['evidence_ids'][0]))+' · '+local('상세/번호','01_수집기록.md')+' · '+local('근거/검수','02_지식연결과검수.md')+'\n'
intro+='\n기존 5개 상세/조합/근거/모션 문서는 `preserved/`에 바이트 단위로 복사했고 원본과 SHA-256이 같다. 보존 문서 안의 예전 절대 경로와 미제공 `original/collection.md` 링크는 이력으로 남아 있다. 이번 실제 접근 경로는 `evidence.json`과 위의 제공 PNG 링크를 사용한다. 과거 문서의 “확인했다”는 이번 실행의 검사 주장으로 자동 승계하지 않았으며 현재 결과는 REV 번호에 따로 남겼다.\n'
write('00_읽는순서.md',intro)

s='# 전체 상세·번호·현재 사용처\n\n'+local('사례 요약','00_읽는순서.md')+' → '+local('원래 전체 상세(보존)','preserved/02_전체상세.md')+' → '+local('원래 부품/조합(보존)','preserved/01_부품과조합.md')+' → '+local('현재 근거/검수','02_지식연결과검수.md')+'. 원기록의 의미·번호·판본은 유지하며 아래는 현재 연결을 추가한 것이다.\n\n역할판은 RC-LAYOUT-001@v1의 전체 배치, RC-COMP-003@v1의 헤더, RC-COMP-007@v1의 업무 묶음으로 조회한다. 역할판 전체를 헤더 하나로 축소하지 않는다. 건물 주변 지원 명찰은 RC-COMP-005@v1이며 역할판과 동일 부품으로 합치지 않는다.\n'
for n in nodes:
 s+=f'\n<a id="{n["id"]}"></a>\n\n## {n["id"]} — {n["name"]}\n\n정의: {n["definition"]}\n\n조건: {n["conditions"]}\n\n미확인: {n["unverified"]}\n'
 if n['subcomponents']:s+='\n하위 구성: '+'; '.join(n['subcomponents'])+'。 개별 소품에 새 번호를 발급하지 않는다.\n'
 for u in uses:
  if u['definition_id']==n['id']:
   s+=f'\n- {u["id"]} / {u["case_id"]} / {u["scope"]}: {u["current_difference"]} 관계: '+', '.join(u['spatial_relations'])+'. 근거: '+', '.join(link(eid,next(e['path'] for e in E if e['id']==eid)) for eid in u['evidence_ids'])+'.\n'
 s+='\n'+local('기존 상세','preserved/02_전체상세.md')+' · '+local('기존 정의와 판본','preserved/01_부품과조합.md')+' · '+local('현재 검수/지식 연결','02_지식연결과검수.md')+'\n'
s+='\n## 보강 관측과 이력\n\nE1 업무 ROI에서 책등의 `BIM`, `ENGINEERING`, `GLOBAL PROJECTS`, `DESIGN SOLUTIONS`가 보인다. 이는 이번 crop 재대조의 추가 정적 관측이며 특정 제품·프로젝트명을 뜻한다고 확정하지 않는다. 원래 “책 2묶음” 기록은 보존한다.\n\n회사열 상세 순서와 두 화면의 제목·도상·빛·반사·배경 구조는 위의 보존 전체 상세에 유지되어 있다. 신규 번호나 레이아웃을 생성하지 않았다. 모든 후보는 로컬이며, 반복 외형 확인/동일 자산/회사 공식 규칙을 별도 상태로 유지한다.\n'
write('01_수집기록.md',s)

s='# Phase 00 지식 연결과 이번 실제 검토\n\n대상은 분석 기록이다. 정본 지식은 검토 질문/분류 조건이며 PNG 사실의 근거가 아니다. `knowledge_snapshot.json`은 정본 경로·파일 SHA·버전·JSON pointer·선택한 원문 객체를 담는다. `reviews`만 이번 실행의 제한 판정이다. 통과는 그 행에 선언한 정적 전사/관계 대조 범위에 한정한다.\n\n## 지식이 현재 기록을 바꾼 판단\n'
for x in connections:
 s+=f'\n### {x["id"]} — {x["target_id"]} ({x["axis"]})\n\n- 관련 지식: '+', '.join(x['knowledge_ids'])+f'\n- 분류/연결 이유: {x["classification_reason"]}\n- 이번 결과: {x["current_result"]}\n- 경계: {x["limits"]}\n'
s+='\n선택적으로 읽은 STYLE-PIP는 deprecated이고 LAYOUT-PIP로 대체됨을 확인했다. 이번 업무 묶음을 이 폐기 태그로 등록하지 않는다. 미분류/복합을 허용하고 격자 형태·정보관계·표현언어·모션 역할·품질 질문을 같은 종류로 합치지 않는다.\n\n## 현재 자기 재대조 결과\n'
for r in reviews:
 s+=f'\n### {r["id"]} — {r["verdict"]}\n\n대상: '+', '.join(r['target_ids'])+' / 관련 기준: '+', '.join(r['criteria_ids'])+f'\n\n확인: {r["confirmed"]}\n\n미확인/제한: {r["remaining"]}\n\n근거: '+', '.join(link(eid,next(e['path'] for e in E if e['id']==eid)) for eid in r['evidence_ids'])+'\n'
s+='\n## 근거 계약·관측 방법\n\n원본명은 가치창출성과 영상_260923_v3.mp4, 제공 원본 SHA는 be78fc4f2f94c6b3cbd31339a1a1ccc84b91613d56c0e485d5dd1296839f56fa, 제공 434.4초/30fps/7680×2160. MP4/오디오/시나리오/편집 프로젝트는 미제공. 32:9는 제공 PNG 치수 계산이다. 시각은 공통 입력의 134·172초 표시를 사용하며 새 PTS 매핑을 검증한 것은 아니다. 표본 2장이며 38초 연속 관측이 아니다.\n\n실제 관찰은 전체 2장(각 2048×576 축소 표시)과 아래 8개 crop의 시각 재대조다. 원본 좌상 원점/x 오른쪽/y 아래쪽/px, right/bottom 제외. crop 외 resize/color/rotation은 하지 않았다. 뷰어 자동 축소: e1_work 2048×544, e2_value 2048×290, e2_building 2048×889, e2_logos 2048×534, e2_number 2048×660. e1_roles/e1_arrows/e1_logos는 원 크기로 표시. 확대는 새 시점의 증거가 아니다.\n\n| 근거 | 크기 | 원본 crop 좌표 | SHA-256 |\n|---|---|---|---|\n'
for e in E:s+='| '+link(e['id'],e['path'])+' | '+str(e['size'])+' | '+str(e.get('bbox_ltrb_exclusive','전체'))+' | '+e['sha256']+' |\n'
s+='\n## 미상과 다음 확인\n'
for u in unknowns:s+=f'\n- {u["id"]} ({u["kind"]}): {u["scope"]}. 막는 판단: {u["blocks"]}. 다음: {u["next"]}.\n'
s+='\n기존 Q-FLOW-001·Q-MOTION-001~003은 조사 항목으로 '+local('원문','preserved/04_모션조사.md')+'에 보존했다. 등록 FLOW/동작 패턴으로 바꾸지 않았다. 실제 정지 확인·관측되지 않음·해당 없음은 다르다. 이번 2장만으로 시간에 걸친 정지는 확인하지 않았다.\n'
write('02_지식연결과검수.md',s)

s='# 실제 조회 색인\n\n`index.json`이 이 출력의 로컬 DB 조회용 원본이다. R4 v0.2 이관/정본 등록/별도 스키마 검증 완료를 뜻하지 않는다. Markdown 수집의 의미·관측 근거는 상세와 자기 재대조로 유지한다.\n\n단위 이름/별칭/ID·사례·지식·검토 ID로 조회하면 정의, 이번 사용처·차이, 사례 요약, 원본·ROI, 관련 지식 원문/출처/포인터, 실제 검토, 미상을 같이 반환한다. 검색은 문자열 포함이며 의미 유사도 판정이 아니다. `--knowledge`는 관련 지식에서 현재 사용처로, `--review`는 실제 판정에서 대상으로, `--case`는 사례에서 후보와 근거로 돌아간다.\n\n| 찾을 내용 | ID | 사용처 | 현재 차이 |\n|---|---|---|---|\n'
for n in nodes:
 us=[u for u in uses if u['definition_id']==n['id']]
 s+=f'| {n["name"]} | {n["id"]} | '+', '.join(u['case_id'] for u in us)+' | '+' / '.join(u['current_difference'] for u in us)+' |\n'
s+='\n명령은 PowerShell에서 이 outputs 폴더를 작업 경로로 실행한다. 번들 Python 절대 경로는 `C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`.\n\n```powershell\n& "C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe" ./query.py --query "업무 이미지 묶음" --out query_results/work.json\n& "C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe" ./query.py --id RC-COMP-008@v1 --out query_results/building.json\n& "C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe" ./query.py --query "역할판" --out query_results/role.json\n& "C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe" ./query.py --knowledge IP-04 --out query_results/knowledge_ip04.json\n& "C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe" ./query.py --review REV-04 --out query_results/review04.json\n& "C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe" ./query.py --case RC-CASE-002 --out query_results/case002.json\n& "C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe" ./query.py --validate --out query_results/validation.json\n```\n\n위 명령의 실제 결과는 `query_results/`에 저장했다. validation은 ID/참조·파일 존재·해시·원본 보존·지식 포인터와 고정 객체의 일치를 검사한다. 실제 정적 관측 정확성은 REV 자기 대조 범위에서만 판단하며 자동 검증이 시각 검수를 대신하지 않는다.\n'
write('03_조회색인.md',s)
print(json.dumps({'cases':len(cases),'definitions':len(nodes),'occurrences':len(uses),'knowledge_links':len(connections),'reviews':len(reviews),'unknowns':len(unknowns)},ensure_ascii=False))
