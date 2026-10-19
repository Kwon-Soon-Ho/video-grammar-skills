from pathlib import Path
import json,sys
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'phase01a-a2'))
from prepare import sha,write,ROOT
AXES=['이동','크기','형태와회전','가시성과공개','색과광량','내부변화','중첩','등퇴장과순서','가감속']
registry=[];rows=[]
def add(id,asset,name,window,role,evidence,prior,**axes):
    assert set(axes)<=set(AXES)
    base={'이동':'추가 독립 이동을 발견하지 못함. 장면 전환/상위 대상 움직임은 별도 기록.','크기':'추가 크기 변화를 발견하지 못함.','형태와회전':'추가 형태 변화·회전을 발견하지 못함.','가시성과공개':'정착 후 유지. 전환 시에는 상위 장면의 가시성 변화에 포함.','색과광량':'추가 독립 색/광량 변화를 발견하지 못함.','내부변화':'이 대상 내부의 추가 독립 동작을 발견하지 못함.','중첩':'배경 위에 배치. 별도 가림 동작을 발견하지 못함.','등퇴장과순서':'해당 장면과 함께 등장·유지.','가감속':'독립 변화 관측이 없어 비적용.'}
    base.update(axes)
    pins=[]
    for rel in evidence:
        p=HERE/rel
        if not p.exists():p=HERE.parent/rel
        assert p.is_file(),p
        pins.append({'path':str(p),'sha256':sha(p)})
    registry.append({'id':id,'asset':asset,'name':name,'window':window,'role':role})
    human_scope='AI_new_observation_not_human_approved' if prior in ['신규 누락 발견','추가 세분화','N4 세분화'] else ('prior_scope_only' if prior.startswith(('N','①','C','기존')) else 'AI_new_observation_not_human_approved')
    rows.append({'id':id,'axis_checks':base,'evidence':pins,'prior_relation':prior,'reviewer':'current Codex visual review; no independent reviewer','review_state':'reviewed_with_declared_limits','human_approval_scope':human_scope})
def j(id,name,window,evidence,prior,**axes):add(id,'자료005',name,window,'primary' if '차트' in name else 'support',evidence,prior,**axes)
def e(id,name,window,evidence,prior,role='support',**axes):add(id,'자료013',name,window,role,evidence,prior,**axes)
j('J-intro-text','도입 CI·연도·제목','0~6',['../phase01a-a2-fullmotion/자료005_전체동작_1.jpg','../phase01a-a2-fullmotion/장헌_정지와_전환곡선.json'],'①',등퇴장과순서='첫 관측 시점에 이미 배치. 6초 이후 전환과 함께 사라짐.')
j('J-intro-photo','도입 교량·제품·구름·수면','0~6',['../phase01a-a2-fullmotion/자료005_전체동작_1.jpg','../phase01a-a2-fullmotion/장헌_정지와_전환곡선.json'],'기존 정지 정정',내부변화='선택 원본 PNG와 480px 시계열에서 독립 구름·물결 동작을 발견하지 못함. 저해상도 픽셀차로 미세 정지까지 증명하지 않음.')
j('J-transition','장면 교체 전체','6~6.4 / 21~21.4',['../phase01a-a2-fullmotion/장헌_정지와_전환곡선.json','검수판/jh_all_1.jpg','검수판/jh_all_3.jpg'],'N1',가시성과공개='두 화면이 겹쳐 교체. 경계 이동 슬라이드로 해석하지 않음.',중첩='전환 동안 이전·다음 장면 중첩.',가감속='혼합 진행량 감속형(ease-out) 기존 근거 유지.')
j('J-base','실적 장면 배경·좌측 제목·하단 주석','6.4~21',['검수판/jh_all_1.jpg','검수판/jh_all_2.jpg','검수판/jh_all_3.jpg'],'①②',내부변화='도시·물·주석·장식선에 새 독립 동작을 발견하지 못함.')
j('J-cards','세 카드 테두리·제목·기준선','6.4~21',['검수판/jh_all_1.jpg','검수판/jh_all_2.jpg'],'N2',등퇴장과순서='세 카드 틀은 장면 전환으로 같이 드러남. 수주→매출→이익의 데이터 순서와 분리.')
for k,label,window in [('order','수주','8~9.3'),('sales','매출','15.5~16.7'),('profit','영업이익','16.8~17.8')]:
    ev=['검수판/jh_all_1.jpg','검수판/jh_all_2.jpg','../phase01a-a2-fullmotion/장헌_차트_시간곡선진단.json']
    j(f'J-{k}-goal',label+' 목표 막대·목표 수치','6.4~21',ev,'N2')
    j(f'J-{k}-actual',label+' 실적 막대',window,ev,'N2',크기='하단 기준에서 위로 성장.',등퇴장과순서='수주→매출→영업이익 순서. 각 카드 틀의 등장과 다름.',가감속='시각 대조상 감속형. 곡선 계량 근거는 원형 진행량이 중심이며 막대 원본 키프레임 복원 아님.')
    j(f'J-{k}-ring',label+' 원형 진행',window,ev,'N2',가시성과공개='12시 방향에서 시계방향으로 파랑 영역 증가. 회색 기준 원 유지.',가감속='파랑 영역 진행량 ease-out 곡선군. 기존 후보 피팅 유지.')
    j(f'J-{k}-numbers',label+' 금액과 퍼센트',window,ev,'N2',내부변화='막대 위 금액 및 원 안 비율이 증가. 금액 라벨은 자라는 막대 상단을 따름.',이동='금액 숫자는 막대 상단을 따라 위로. 퍼센트 중심 위치는 유지.',가감속='증가량이 끝에서 작아짐. 정수 반올림 때문에 값 변화의 계단을 별도 곡선으로 보지 않음.')
j('J-sector-bg','매출처·사업분야 배경·제목·주석','21.4~24',['검수판/jh_all_3.jpg','검수판/jh_all_4.jpg'],'③')
j('J-sector-ring','매출처 차트 색 영역','21.3~22.6',['검수판/jh_all_3.jpg','../phase01a-a2-fullmotion/장헌_차트_시간곡선진단.json'],'N3',가시성과공개='색 영역이 시계방향으로 채워짐. 도넛 중심 구멍 위치 유지.',가감속='채움 진행량 감속형 ease-out.')
j('J-sector-labels','매출처·사업분야 외부 라벨·연결선','21.4~24',['검수판/jh_all_3.jpg','검수판/jh_all_4.jpg'],'③',등퇴장과순서='장면 전환으로 보이고 자리 유지. 라벨이 도넛을 따라 회전하거나 따로 그려지는 동작을 발견하지 못함.')
j('J-sector-percent','가족사 비중 숫자·강조 화살표','21.3~22.6',['검수판/jh_all_3.jpg'],'N3',내부변화='비중 숫자 증가. 화살표와 설명문은 별도 이동/점멸을 발견하지 못함.',가감속='숫자 증가량 끝에서 감소. 정수 반올림 영향 존재.')
j('J-business-ring','사업분야 회색 원형','21.4~24',['검수판/jh_all_3.jpg','검수판/jh_all_4.jpg'],'기존 범위 한정',가시성과공개='이번 24초까지 회색 원 유지. 그 이후 진행 여부 판정 안 함.')
intro=['검수판/eg_intro_1.jpg','검수판/eg_intro_2.jpg','검수판/eg_intro_3.jpg','검수판/도입_작은요소_역순_1.jpg']
late=['검수판/eg_late_1.jpg','검수판/eg_late_2.jpg','검수판/eg_late_3.jpg']
e('E-glow','배경 광량·비네트','0~15.5',intro+late,'기존 일반 배경',role='ambient',색과광량='중앙 녹색광·주변 어둠이 형성되고 유지. 주 대상 전경과 다른 광량.',가감속='미분류: 낮은 대비와 전경 중첩. 색/밝기 이징과 위치 속도를 혼용하지 않음.')
e('E-grid','배경 격자·큰 사각 경계','0~15.5',intro+late,'기존 일반 배경',role='ambient',가시성과공개='도입에서 점차 선명해짐. 이후 배경으로 유지.',이동='도입 경계 자리/크기가 달라지는 부분은 있음. 동일 선의 전 구간 추적을 확정하지 않음.',가감속='미분류: 도입 가시성과 경계 이동 중첩. 존재 관측을 지우지 않고 경로·속도 보류.')
e('E-early-upper','도입 어두운 E 위쪽 조각','약0.2~1.2',intro,'추가 세분화',이동='화면 왼쪽에서 오른쪽으로 들어와 정착.',가시성과공개='어두운 조각이 배경 위에 드러남.',등퇴장과순서='작은 커서/큰 영문보다 먼저. 뒤의 금빛 E 재등장과 구분.',가감속='정착부 이동량이 줄어드는 감속 성향. 저대비 때문에 정확한 시작/곡선 미분류.')
e('E-early-middle','도입 어두운 E 가운데 조각','약0.2~1.2',intro,'추가 세분화',이동='왼쪽→오른쪽 정착.',등퇴장과순서='위·아래 조각과 시간차/중첩. 저대비로 프레임 단위 엄밀 선후는 보류.',가감속='감속 성향만 관측; 정확한 곡선 분류 보류.')
e('E-early-lower','도입 어두운 E 아래쪽 조각','약0.2~1.2',intro,'추가 세분화',이동='왼쪽→오른쪽 정착.',등퇴장과순서='도입 E 조립 단계. 3.5초 이후 전경 E 조립과 분리.',가감속='감속 성향만 관측; 정확한 곡선 분류 보류.')
e('E-outline-light','E 주변 얇은 선·수평 발광 부분','도입 및 배경 유지',intro+late,'C1',role='ambient',이동='빛이 E 주변을 통과하는 관측 유지. 고정 테두리와 이동 발광 부분의 완전 분리는 아직 못함.',색과광량='얇은 선·수평 발광 부분이 강해졌다 약해짐.',가감속='미분류: 동선 전체와 가시성 변화가 분리되지 않음.')
e('E-cursor','CAD 같은 십자 커서와 중앙 작은 사각형','약1~3.6',intro+['../phase01a-a2-correction2/십자커서_점선영역_확대와축소.jpg'],'C2',이동='왼쪽 위 부근에서 오른쪽 아래로 이동해 선택 영역의 반대 모서리를 따라감.',가시성과공개='적색 수평·녹색 수직·중앙 작은 사각형이 드러나고 이후 사라짐.',등퇴장과순서='큰 영문 공개 전부터 보임. 점선 확장과 겹침.',가감속='선택 영역 공개 경계와 관련되지만 커서 자체 전 구간 이징은 미분류.')
e('E-selection','점선 사각 선택 영역','약1.9~3.6',intro+['../phase01a-a2-correction2/십자커서_점선영역_확대와축소.jpg'],'C2',크기='좌상단에서 우하단으로 넓어져 큰 영문을 공개. 이후 왼쪽/위쪽 경계가 우하단으로 따라가며 영역 축소.',가시성과공개='점선 영역 안의 밝은 문구와 바깥의 연한 문구가 구분됨.',내부변화='점선 패턴의 이동/명멸과 영역 변화를 분리. 점선 질감 자체 주행 속도는 미분류.',가감속='공개 경계 가속후감속, 소실 경계 가속 기존 후보 유지. 점선 질감/커서/전체 opacity 곡선으로 확대 안 함.')
e('E-value','큰 Value of 밝은 글자와 연한 잔존 글자','약1.9~15.5',intro+late,'N4+C2',가시성과공개='선택 영역 확대에 따라 드러나고 영역 축소 후 연한 전체 문구가 배경에 남음.',중첩='밝은/연한 글자의 합성처럼 보이는 결과. 실제 AE 레이어 수는 미확인.',가감속='밝은 공개/소실 경계 곡선은 N4. 연한 원문 전체 opacity 곡선으로 확정하지 않음.')
e('E-title','작은 EG-BIM 개별 문자','약2.8~15.5',intro+['검수판/본문_등장순서_1.jpg']+late,'N4',이동='벌어진 문자가 중심 쪽으로 모여 자간이 좁아짐.',가시성과공개='문자별로 선명해짐.',등퇴장과순서='큰 Value of가 완전히 지워지기 전에 등장. 부제·본문보다 먼저 선명해짐.',가감속='기존 자간 수렴 ease-out 성향. 짧은 구간/가시성 중첩 한계 유지.')
e('E-subtitle','영문 부제','약3~15.5',['검수판/본문_등장순서_1.jpg']+late,'N4 세분화',가시성과공개='EG-BIM 수렴 중 부제가 선명해짐. 본문보다 앞서 나타남.',등퇴장과순서='주제명→영문 부제→한글 본문 순으로 중첩하며 선명해짐.',가감속='가시성 후보만 관찰. 배경/문자 경계 중첩으로 정확한 opacity 곡선 미분류.')
e('E-body-upper','한글 본문 위쪽 두 줄','약3.15~15.5',['검수판/본문_등장순서_1.jpg']+late,'N4 세분화',가시성과공개='위쪽 문장이 아래쪽 문장보다 먼저 선명해짐.',등퇴장과순서='부제 뒤, 아래 두 줄 앞. 완전히 분리된 컷이 아니라 일부 겹침.',가감속='위→아래 공개 순서 확인. 개별 줄 opacity/와이프 구현 및 곡선은 미분류.')
e('E-body-lower','한글 본문 아래쪽 두 줄','약3.3~15.5',['검수판/본문_등장순서_1.jpg']+late,'N4 세분화',가시성과공개='위쪽 두 줄이 보인 후 아래쪽 두 줄이 선명해짐.',등퇴장과순서='위→아래 순차 선명화. 3.6초에도 아래쪽이 상대적으로 약함; 이후 정착.',가감속='세부 밝기 곡선 미분류. 문자별 키프레임/타이핑으로 해석하지 않음.')
for part,label in [('upper','위쪽'),('middle','가운데'),('lower','아래쪽')]:
    e('E-hero-'+part,'전경 E '+label+' 조각','약3.5~5.5',intro,'기존 E 정정',role='primary',이동='왼쪽→오른쪽으로 들어와 조립.',색과광량='녹색 조각이 금색/갈색 계열로 전환되며 세부 선무늬 드러남.',등퇴장과순서='큰 영문 잔존·설명문 정착과 중첩. 조각별 시작이 달라 한 덩어리 색 변화로 적지 않음.',가감속='기존 측정된 E 경계 이동 감속/ease-out 유지. 세 조각의 원본 동일 곡선으로 단정하지 않음.')
e('E-hero-dim','정착 후 금빛 E의 광량','약5~8',['검수판/eg_intro_3.jpg','검수판/E내부_역순_3.jpg','검수판/E_광량과_내부질감진단.json'],'추가 세분화',색과광량='약5초에 밝게 보인 뒤 7~8초 쪽으로 갈수록 어두운 갈색 배경 역할로 약화. E 위치 이동과 다른 사건.',가감속='광량 전이 확인. 고정 ROI는 색·배경 혼합량이므로 정확한 AE opacity/easing으로 확정하지 않음.')
e('E-texture','E 내부 선무늬·격자','약4.2~15.5',['검수판/E내부_역순_1.jpg','검수판/E내부_역순_2.jpg','검수판/E내부_역순_3.jpg','검수판/E_광량과_내부질감진단.json'],'추가 세분화',가시성과공개='E 등장·발광에 따라 선무늬가 선명해졌다 약해짐.',내부변화='선무늬가 독립적으로 계속 흐른다고 확정할 근거를 찾지 못함. 고정 ROI 상관 비교는 참고만 사용.',가감속='독립 질감 이동 곡선 미분류. 광량 전이와 혼용하지 않음.')
e('E-ui1','첫 관리 UI 이미지와 노란 테두리','약6.9~15.5',late,'N5+N6',이동='오른쪽 이동 진입, 이후 우하단 이동·축소되어 뒷 창이 됨.',크기='첫 진입 시 폭 증가로 단정 안 함. 재배치 시 축소.',가시성과공개='진입하며 선명해짐.',중첩='다음 도면 창 뒤로 가려지고 나중 재배치 때 다시 노출.',등퇴장과순서='전경 E 정착 뒤 첫 UI, 그 뒤 도면 UI.',가감속='진입 ease-out, 재배치 ease-in-out 기존 후보.')
e('E-ui1-inside','첫 UI 안 목록·작은 도면·커서 여부','정착8~10.4',late+['검수판/추가발견_UI내부_선택변화.jpg'],'신규 누락 발견',내부변화='구역 변화 대조에서 내부 변화가 남아 확대 재검수. 상단 선택행과 하단 주황 선택영역이 순서대로 바뀜. 이 실행 초안의 내부 변화 없음 판단을 철회.',등퇴장과순서='아래 두 대상에서 별도 상태 교체를 기록. 실제 포인터 클릭/이벤트 실행은 영상만으로 확정하지 않음.')
e('E-ui1-row','첫 UI 상단 표의 선택행','약8.2~10.4',['검수판/추가발견_UI내부_선택변화.jpg'],'신규 누락 발견',이동='표 자체나 행이 연속 이동하는 것보다 선택 표시가 다음 행으로 교체됨.',가시성과공개='교체 중 이전/다음 표 내용과 선택행이 겹쳐 옅게 보임.',내부변화='첫 행에서 다음 행들로 선택 상태가 내려감.',등퇴장과순서='하단 도면 선택 변경과 함께 순차 교체.',가감속='행 선택은 상태 교체. 연속 위치 속도에 ease-in/out을 부여하지 않음. 화면 혼합 곡선은 미분류.')
e('E-ui1-thumb','첫 UI 하단 도면 미리보기의 주황 테두리','약7.7~10.4',['검수판/추가발견_UI내부_선택변화.jpg'],'신규 누락 발견',이동='맨 윗줄 도면 선택 표시가 첫째→둘째→셋째→넷째로 왼쪽에서 오른쪽으로 바뀜. 물리적인 커서 슬라이드로 확정하지 않음.',가시성과공개='교체 중 양쪽 선택 상태가 겹쳐 보이는 전환.',내부변화='주황 테두리/이름 바의 선택 대상이 바뀜.',등퇴장과순서='상단 선택행 변경과 동반. 창 전체의 오른쪽 진입/우하단 재배치와 별도 사건.',가감속='선택 상태 교체이며 이동속도 곡선 비적용. 전환 opacity 곡선은 미분류.')
e('E-ui2','두 번째 도면 UI와 노란 테두리','약11.2~15.5',late,'N6+N7',이동='오른쪽으로 진입. 모델 이후 우하단으로 재배치.',크기='재배치 때 축소되어 뒤 창이 더 드러남.',가시성과공개='이전 UI와 겹쳐 선명해짐.',중첩='첫 UI 앞, 모델 뒤. 테두리 중첩을 새 창 복제본 등장으로 오인하지 않음.',가감속='진입 ease-out, 재배치 ease-in-out 기존 후보.')
e('E-ui2-inside','두 번째 도면 내부 형상·주석·좌표','약12~15.5',['검수판/추가발견_모델_연결면.jpg']+late,'추가 세분화',내부변화='도면 내 원래 작은 형상은 남아 있고 별도 전경 모델이 커져 나옴. 화면 전체가 모델로 변형된 것은 아님.')
e('E-model','밖으로 나오는 철근 모델 본체','약12.9~15.5',['검수판/모델_원근형태_1.jpg','검수판/모델_원근형태_2.jpg','검수판/모델_원근형태_3.jpg','검수판/추가발견_모델_연결면.jpg'],'N7',role='primary',이동='도면 안 작은 지점 부근에서 우하단으로 커져 나옴.',크기='초반 빠르게 커진 후 끝에서 변화량 감소.',형태와회전='추가 회전 후보를 검토했으나 명확한 독립 회전 근거로 확정하지 않음. 작은 초기 블러·확대·연결면이 중첩.',중첩='도면 창보다 앞. 뒤 연결면과 나중 광점이 별도 요소.',가감속='기존 모델 면 확대 진행량 ease-out 후보 유지. 원본 Scale/카메라가 아님.')
e('E-connector','도면과 전경 모델 사이 반투명 연결면','약13~15.5',['검수판/추가발견_모델_연결면.jpg','검수판/모델_원근형태_1.jpg','검수판/모델_원근형태_2.jpg'],'신규 누락 발견',이동='도면의 작은 지점 부근에서 전경 모델 쪽 우하단으로 뻗음.',크기='모델이 멀어지고 커질수록 연결 영역이 넓어짐.',형태와회전='삼각/사다리꼴로 보이는 반투명 면. 모델 자체 회전과 분리.',가시성과공개='모델 확대와 함께 선명해져 뒤에 남음.',색과광량='어두운 도면 위를 밝히는 회색 반투명 면.',중첩='도면 위, 전경 모델 뒤. 14초대 후반 광점/수평 빛띠와도 다른 요소.',등퇴장과순서='모델 확대에 따라 펼쳐짐. 뒤 창 재배치 뒤에도 연결 유지.',가감속='모델 확대와 연동되어 끝에서 변화가 작아지는 성향. 면 경계 자체 곡선 미분류.')
e('E-flare','모델 광점·수평 빛띠','약14.3~15.5',late+['검수판/추가발견_모델_연결면.jpg'],'N8',가시성과공개='광점과 오른쪽 빛띠가 강해짐.',색과광량='노랑/흰색 발광 증가.',가감속='고정 영역 밝기 ease-in-out 성향. 위치 속도나 실제 opacity 커브로 확대 안 함.')
native=json.loads((HERE/'cases/자료013/eg_fine/실행기록.json').read_text(encoding='utf-8'))['frames']
for row in rows:
    times={'E-outline-light':['.5','1.2'],'E-cursor':['1.2','3.1'],'E-selection':['3.1','3.3'],'E-connector':['13.1','13.8'],'E-ui1-row':['8','9','10'],'E-ui1-thumb':['8','9','10']}.get(row['id'],[])
    for t in times:
        f=next(f for f in native if F(f['actual_playback_seconds'])==F(t))
        row['evidence'].append({'path':f['path'],'sha256':f['sha256'],'basis':'native 3840x2160 RGB frame; sample-table PTS checked'})
write(HERE/'01_대상목록.json',{'schema_version':'0.1','scope':{'자료005':[0,24],'자료013':[0,15.5]},'discovery_basis':'spatial partition, forward temporal sheets, reverse settled-state tracing; prior corrections used as known regressions, not blind tests','required_axes':AXES,'subjects':registry})
write(HERE/'02_속성검수표.json',{'schema_version':'0.1','rows':rows,'complete_video_or_no_omission_guarantee':False,'new_human_approval_requested':False,'A3_started':False})
write(HERE/'04_회귀확인_과거누락.json',{'known_not_blind':True,'cases':[{'omission':'E 조각 슬라이드','required_ids':['E-hero-upper','E-hero-middle','E-hero-lower']},{'omission':'얇은 빛 통과','required_ids':['E-outline-light']},{'omission':'십자 커서','required_ids':['E-cursor']},{'omission':'점선 영역 축소','required_ids':['E-selection']}],'scope':'checks linkage to actual reviewed evidence and populated axes, not recognition accuracy'})
print(json.dumps({'subjects':len(rows),'axis_cells':len(rows)*len(AXES),'per_asset':{aid:sum(s['asset']==aid for s in registry) for aid in ['자료005','자료013']}},ensure_ascii=False))
