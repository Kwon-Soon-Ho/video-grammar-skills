# DEV-KGEO-H03-20261019 분석 기록

판본: 0.1.0-draft.6 / video-observation-0.4
원본: D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\한맥 영상\K-GEO FESTA 1핵심 홍보동영상\K-GEO FESTA_250919_3.mp4
구간: [25, 35]초
방법: 기존 base native 프레임의 전체 개요 시트를 시간순·역순으로 보고 26.2/31.4초 또는 66/72.8초 native를 세부 재대조한 실제 개발 분석. 과거 기준답안 준비 노출 이력 있음. 독립 비교·전 프레임 관찰 아님.
음성 검수: False

구조 검사와 시각 내용 확인·회사 승인은 별개다.

## 전체 디자인

### comparison / [25, 30.2]
상단 수신기 세 개와 하단 비교표가 같은 열 관계를 이룬다.
전체 요소: header, receivers, table, highlight
근거: f03

- hierarchy: 좌상단 섹션 표제, 주 콘텐츠, 하단 표/조건 문구를 구분. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019'])
- alignment: 수신기 이미지/이름표/표 열을 대응시키고 지도 패널은 위·아래 변을 대체로 맞춘다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019'])
- spacing: 상하 여백을 둔 비교 화면에서 작은 패널 간격을 둔 두 지도 화면으로 바뀐다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019'])
- typography: 한글 산세리프, 비교표와 이름표는 짙은 글자, 섹션 제목은 흰 글자. 정확 서체·크기 미상. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019'])
- color: 밝은 회청 배경, 청색/청록 머리글, 주황 강조, 지도 위 노랑 경로·보라 핀. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019'])
- background: 연한 회청 단색 계열 배경 위 사진·표·지도 패널. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019'])
- shapes: 사선 리본 표제, 둥근 표, 사각 장비 이름표, 둥근 모서리 지도 패널과 핀. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019'])

### maps / [29.8, 35]
왼쪽 좁은 세로 패널과 오른쪽 넓은 패널을 병렬로 배치한다.
전체 요소: header, left-panel, right-panel, left-route, left-marker, right-route, right-marker, caption
근거: f16

- hierarchy: 좌상단 섹션 표제, 주 콘텐츠, 하단 표/조건 문구를 구분. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037', 'c038', 'c039'])
- alignment: 수신기 이미지/이름표/표 열을 대응시키고 지도 패널은 위·아래 변을 대체로 맞춘다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037', 'c038', 'c039'])
- spacing: 상하 여백을 둔 비교 화면에서 작은 패널 간격을 둔 두 지도 화면으로 바뀐다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037', 'c038', 'c039'])
- typography: 한글 산세리프, 비교표와 이름표는 짙은 글자, 섹션 제목은 흰 글자. 정확 서체·크기 미상. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037', 'c038', 'c039'])
- color: 밝은 회청 배경, 청색/청록 머리글, 주황 강조, 지도 위 노랑 경로·보라 핀. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037', 'c038', 'c039'])
- background: 연한 회청 단색 계열 배경 위 사진·표·지도 패널. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037', 'c038', 'c039'])
- shapes: 사선 리본 표제, 둥근 표, 사각 장비 이름표, 둥근 모서리 지도 패널과 핀. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037', 'c038', 'c039'])

## 전체 흐름과 세부 모션

### flow: 수신기 비교·강조 → 겹치는 화면 교체 → 두 지도와 드론 표시 이동·조건 문구 / [25, 35]
- [c004] 29.4~30.2초 사이 표제 내용이 전환되며 중첩 표본이 있다.
- [c009] 비교 화면이 29.8초 표본에서 흐려지고 지도 화면과 겹친 뒤 교체된다.
- [c017] 비교표가 29.8초의 새 지도와 중첩되며 약해진 뒤 보이지 않게 된다.
- [c019] 25초에는 약하거나 보이지 않던 강조가 25.4초 이후 표본에서 나타나 수신기 3을 두른다.
- [c021] 29.8초 작은 지도 패널이 비교 화면 위에 겹쳐 나타나 30.2초 이후 두 패널 화면이 된다.
- [c022] 전환 중 작게 보이는 왼쪽 패널이 커져 세로 패널로 정착한다. 정확 곡선 미상.
- [c024] 29.8초의 작은 오른쪽 지도 패널이 나타나 넓은 오른쪽 화면으로 전환된다.
- [c025] 전환 중 오른쪽 패널의 보이는 크기가 커져 정착한다. 정확 보간은 미확정.
- [c030] 왼쪽 패널 내부 드론 표시가 상단 오른쪽 쪽에서 오른쪽 경로를 따라 화면 아래쪽으로 옮겨 간다.
- [c034] 오른쪽 패널에서도 경로에 대한 드론 그림 위치가 표본마다 변한다. 정확 방문 순서는 미확정.
- [c039] 31.4초에는 옅은 문구/바가 시작되고 뒤 표본에서 비행 조건이 읽히게 된다.
반복 패턴 참조: []

### detail: 주황 외곽 강조, 두 패널 크기 변화, 패널 내부 드론 위치, 하단 문구 출현 / [25, 35]
- [c002] 데이터 분석 방법 표제.
- [c003] 데이터 취득 방법 소개 표제로 바뀐다.
- [c004] 29.4~30.2초 사이 표제 내용이 전환되며 중첩 표본이 있다.
- [c006] 수신기 1 이름표.
- [c007] 수신기 2 이름표.
- [c008] 수신기 3(저가형) 이름표.
- [c009] 비교 화면이 29.8초 표본에서 흐려지고 지도 화면과 겹친 뒤 교체된다.
- [c011] 드론 모델명은 Matrice 300 RTK.
- [c012] 드론 RTK 포지셔닝 정확도는 1cm + 1ppm.
- [c013] 수신기 1 정확도는 0.6cm+0.5ppm.
- [c014] 수신기 2 정확도는 1cm+1ppm.
- [c015] 수신기 3(저가형) 정확도는 1cm+1ppm.
- [c016] 드론 열은 청록 계열이고 수신기 열은 연한 파랑 계열이며 일부 수치·수신기3 문구는 주황으로 강조된다.
- [c017] 비교표가 29.8초의 새 지도와 중첩되며 약해진 뒤 보이지 않게 된다.
- [c019] 25초에는 약하거나 보이지 않던 강조가 25.4초 이후 표본에서 나타나 수신기 3을 두른다.
- [c021] 29.8초 작은 지도 패널이 비교 화면 위에 겹쳐 나타나 30.2초 이후 두 패널 화면이 된다.
- [c022] 전환 중 작게 보이는 왼쪽 패널이 커져 세로 패널로 정착한다. 정확 곡선 미상.
- [c024] 29.8초의 작은 오른쪽 지도 패널이 나타나 넓은 오른쪽 화면으로 전환된다.
- [c025] 전환 중 오른쪽 패널의 보이는 크기가 커져 정착한다. 정확 보간은 미확정.
- [c026] WP 1~WP 5 문구가 보라색 핀 근처에 표시된다.
- [c028] 아래와 좌우를 잇는 노란 선 및 상단의 꺾인 선과 보라색 핀 다섯 개가 보인다.
- [c030] 왼쪽 패널 내부 드론 표시가 상단 오른쪽 쪽에서 오른쪽 경로를 따라 화면 아래쪽으로 옮겨 간다.
- [c032] 비스듬한 사진 위에 노란 선과 보라색 핀들이 고정 기준으로 배치된다.
- [c034] 오른쪽 패널에서도 경로에 대한 드론 그림 위치가 표본마다 변한다. 정확 방문 순서는 미확정.
- [c036] 드론 비행 경로.
- [c037] 비행고도: 50m.
- [c038] 비행속도: 2m/s.
- [c039] 31.4초에는 옅은 문구/바가 시작되고 뒤 표본에서 비행 조건이 읽히게 된다.
반복 패턴 참조: []

## 대상 식별과 고유 주장

### header: 좌상단 파란 섹션 표제
흰 외곽의 청색 사선 리본과 흰 글씨
식별: reviewed / 좌상단 파란 섹션 표제; 후보 []

- [c001] identity/identity/visible-form: 좌상단 파란 섹션 표제의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f03'])
- [c002] text/value/section-before: 데이터 분석 방법 표제. (observed; 내용 supported; 근거 ['f03'])
- [c003] text/value/section-after: 데이터 취득 방법 소개 표제로 바뀐다. (observed; 내용 supported; 근거 ['f16'])
- [c004] visibility/order/section-transition: 29.4~30.2초 사이 표제 내용이 전환되며 중첩 표본이 있다. (observed; 내용 supported; 근거 ['f11', 'f12', 'f13'])

### receivers: 수신기 이미지 세 개
위쪽에 세 장비 사진/렌더와 각각의 이름표
식별: reviewed / 수신기 이미지 세 개; 후보 []

- [c005] identity/identity/visible-form: 수신기 이미지 세 개의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f03'])
- [c006] text/value/label-1: 수신기 1 이름표. (observed; 내용 supported; 근거 ['f03'])
- [c007] text/value/label-2: 수신기 2 이름표. (observed; 내용 supported; 근거 ['f03'])
- [c008] text/value/label-3: 수신기 3(저가형) 이름표. (observed; 내용 supported; 근거 ['f03'])
- [c009] visibility/direction/exit: 비교 화면이 29.8초 표본에서 흐려지고 지도 화면과 겹친 뒤 교체된다. (observed; 내용 supported; 근거 ['f11', 'f12', 'f13'])

### table: 하단 GNSS 장비 비교표
회색/청록/파랑 머리글과 표 셀
식별: reviewed / 하단 GNSS 장비 비교표; 후보 []

- [c010] identity/identity/visible-form: 하단 GNSS 장비 비교표의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f03'])
- [c011] text/value/drone-model: 드론 모델명은 Matrice 300 RTK. (observed; 내용 supported; 근거 ['f03'])
- [c012] text/value/drone-accuracy: 드론 RTK 포지셔닝 정확도는 1cm + 1ppm. (observed; 내용 supported; 근거 ['f03'])
- [c013] text/value/receiver1-accuracy: 수신기 1 정확도는 0.6cm+0.5ppm. (observed; 내용 supported; 근거 ['f03'])
- [c014] text/value/receiver2-accuracy: 수신기 2 정확도는 1cm+1ppm. (observed; 내용 supported; 근거 ['f03'])
- [c015] text/value/receiver3-accuracy: 수신기 3(저가형) 정확도는 1cm+1ppm. (observed; 내용 supported; 근거 ['f03'])
- [c016] color/value/column-style: 드론 열은 청록 계열이고 수신기 열은 연한 파랑 계열이며 일부 수치·수신기3 문구는 주황으로 강조된다. (observed; 내용 supported; 근거 ['f03'])
- [c017] visibility/direction/crossfade: 비교표가 29.8초의 새 지도와 중첩되며 약해진 뒤 보이지 않게 된다. (observed; 내용 supported; 근거 ['f11', 'f12', 'f13'])

### highlight: 수신기 3의 주황 외곽 강조
오른쪽 검정 장비 둘레의 주황 선
식별: reviewed / 수신기 3의 주황 외곽 강조; 후보 []

- [c018] identity/identity/visible-form: 수신기 3의 주황 외곽 강조의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f03'])
- [c019] visibility/direction/emphasis: 25초에는 약하거나 보이지 않던 강조가 25.4초 이후 표본에서 나타나 수신기 3을 두른다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f03'])

### left-panel: 왼쪽 세로 운동장 패널
흰 둥근 테두리의 긴 운동장 사진
식별: reviewed / 왼쪽 세로 운동장 패널; 후보 []

- [c020] identity/identity/visible-form: 왼쪽 세로 운동장 패널의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f16'])
- [c021] visibility/direction/enter: 29.8초 작은 지도 패널이 비교 화면 위에 겹쳐 나타나 30.2초 이후 두 패널 화면이 된다. (observed; 내용 supported; 근거 ['f12', 'f13', 'f16'])
- [c022] size/direction/growth: 전환 중 작게 보이는 왼쪽 패널이 커져 세로 패널로 정착한다. 정확 곡선 미상. (observed; 내용 supported; 근거 ['f12', 'f13', 'f14'])

### right-panel: 오른쪽 넓은 운동장 지도 패널
흰 둥근 테두리의 비스듬한 넓은 사진
식별: reviewed / 오른쪽 넓은 운동장 지도 패널; 후보 []

- [c023] identity/identity/visible-form: 오른쪽 넓은 운동장 지도 패널의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f16'])
- [c024] visibility/direction/enter: 29.8초의 작은 오른쪽 지도 패널이 나타나 넓은 오른쪽 화면으로 전환된다. (observed; 내용 supported; 근거 ['f12', 'f13', 'f16'])
- [c025] size/direction/growth: 전환 중 오른쪽 패널의 보이는 크기가 커져 정착한다. 정확 보간은 미확정. (observed; 내용 supported; 근거 ['f12', 'f13', 'f14'])
- [c026] text/value/waypoints: WP 1~WP 5 문구가 보라색 핀 근처에 표시된다. (observed; 내용 supported; 근거 ['f16'])

### left-route: 왼쪽 패널의 노란 경로와 보라색 핀
운동장 위 고정 경로선과 다섯 핀
식별: reviewed / 왼쪽 패널의 노란 경로와 보라색 핀; 후보 []

- [c027] identity/identity/visible-form: 왼쪽 패널의 노란 경로와 보라색 핀의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f16'])
- [c028] shape/value/route-shape: 아래와 좌우를 잇는 노란 선 및 상단의 꺾인 선과 보라색 핀 다섯 개가 보인다. (observed; 내용 supported; 근거 ['f16'])

### left-marker: 왼쪽 패널의 드론 표시
흰/보라색 작은 드론 그림
식별: reviewed / 왼쪽 패널의 드론 표시; 후보 []

- [c029] identity/identity/visible-form: 왼쪽 패널의 드론 표시의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f16'])
- [c030] position/direction/panel-relative: 왼쪽 패널 내부 드론 표시가 상단 오른쪽 쪽에서 오른쪽 경로를 따라 화면 아래쪽으로 옮겨 간다. (observed; 내용 supported; 근거 ['f14', 'f16', 'f19', 'f24'])

### right-route: 오른쪽 패널의 경로와 핀
사진 위 노란 경로와 보라색 핀
식별: reviewed / 오른쪽 패널의 경로와 핀; 후보 []

- [c031] identity/identity/visible-form: 오른쪽 패널의 경로와 핀의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f16'])
- [c032] shape/value/route-shape: 비스듬한 사진 위에 노란 선과 보라색 핀들이 고정 기준으로 배치된다. (observed; 내용 supported; 근거 ['f16'])

### right-marker: 오른쪽 패널의 드론 표시
경로 위 작은 드론 그림
식별: reviewed / 오른쪽 패널의 드론 표시; 후보 []

- [c033] identity/identity/visible-form: 오른쪽 패널의 드론 표시의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f16'])
- [c034] position/direction/panel-relative: 오른쪽 패널에서도 경로에 대한 드론 그림 위치가 표본마다 변한다. 정확 방문 순서는 미확정. (observed; 내용 supported; 근거 ['f14', 'f16', 'f20', 'f24'])

### caption: 아래쪽 비행 조건 문구
흰 반투명 바탕의 짧은 문구 묶음
식별: reviewed / 아래쪽 비행 조건 문구; 후보 []

- [c035] identity/identity/visible-form: 아래쪽 비행 조건 문구의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f19'])
- [c036] text/value/caption-title: 드론 비행 경로. (observed; 내용 supported; 근거 ['f19'])
- [c037] text/value/height: 비행고도: 50m. (observed; 내용 supported; 근거 ['f19'])
- [c038] text/value/speed: 비행속도: 2m/s. (observed; 내용 supported; 근거 ['f19'])
- [c039] visibility/direction/enter: 31.4초에는 옅은 문구/바가 시작되고 뒤 표본에서 비행 조건이 읽히게 된다. (observed; 내용 supported; 근거 ['f16', 'f17', 'f19'])

## 검토 행과 미해결

- header/identity [25, 35]: reviewed, unchanged; 주장 ['c001']; 미해결 []
- header/text [25, 35]: reviewed, unchanged; 주장 ['c002', 'c003']; 미해결 []
- header/visibility [25, 35]: reviewed, changed; 주장 ['c004']; 미해결 []
- receivers/identity [30.2, 35]: not_applicable, not_applicable; 주장 []; 미해결 []
- receivers/identity [25, 30.2]: reviewed, unchanged; 주장 ['c005']; 미해결 []
- receivers/text [30.2, 35]: not_applicable, not_applicable; 주장 []; 미해결 []
- receivers/text [25, 30.2]: reviewed, unchanged; 주장 ['c006', 'c007', 'c008']; 미해결 []
- receivers/visibility [30.2, 35]: not_applicable, not_applicable; 주장 []; 미해결 []
- receivers/visibility [25, 30.2]: reviewed, changed; 주장 ['c009']; 미해결 []
- table/identity [30.2, 35]: not_applicable, not_applicable; 주장 []; 미해결 []
- table/identity [25, 30.2]: reviewed, unchanged; 주장 ['c010']; 미해결 []
- table/text [30.2, 35]: not_applicable, not_applicable; 주장 []; 미해결 []
- table/text [25, 30.2]: reviewed, unchanged; 주장 ['c011', 'c012', 'c013', 'c014', 'c015']; 미해결 []
- table/color [30.2, 35]: not_applicable, not_applicable; 주장 []; 미해결 []
- table/color [25, 30.2]: reviewed, unchanged; 주장 ['c016']; 미해결 []
- table/visibility [30.2, 35]: not_applicable, not_applicable; 주장 []; 미해결 []
- table/visibility [25, 30.2]: reviewed, changed; 주장 ['c017']; 미해결 []
- highlight/identity [30.2, 35]: not_applicable, not_applicable; 주장 []; 미해결 []
- highlight/identity [25, 30.2]: reviewed, unchanged; 주장 ['c018']; 미해결 []
- highlight/visibility [30.2, 35]: not_applicable, not_applicable; 주장 []; 미해결 []
- highlight/visibility [25, 30.2]: reviewed, changed; 주장 ['c019']; 미해결 []
- left-panel/identity [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- left-panel/identity [29.8, 35]: reviewed, unchanged; 주장 ['c020']; 미해결 []
- left-panel/visibility [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- left-panel/visibility [29.8, 35]: reviewed, changed; 주장 ['c021']; 미해결 []
- left-panel/size [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- left-panel/size [29.8, 35]: reviewed, changed; 주장 ['c022']; 미해결 []
- right-panel/identity [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- right-panel/identity [29.8, 35]: reviewed, unchanged; 주장 ['c023']; 미해결 []
- right-panel/visibility [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- right-panel/visibility [29.8, 35]: reviewed, changed; 주장 ['c024']; 미해결 []
- right-panel/size [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- right-panel/size [29.8, 35]: reviewed, changed; 주장 ['c025']; 미해결 []
- right-panel/text [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- right-panel/text [29.8, 35]: reviewed, unchanged; 주장 ['c026']; 미해결 []
- left-route/identity [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- left-route/identity [29.8, 35]: reviewed, unchanged; 주장 ['c027']; 미해결 []
- left-route/shape [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- left-route/shape [29.8, 35]: reviewed, unchanged; 주장 ['c028']; 미해결 []
- left-marker/identity [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- left-marker/identity [29.8, 35]: reviewed, unchanged; 주장 ['c029']; 미해결 []
- left-marker/position [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- left-marker/position [29.8, 35]: reviewed, changed; 주장 ['c030']; 미해결 []
- right-route/identity [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- right-route/identity [29.8, 35]: reviewed, unchanged; 주장 ['c031']; 미해결 []
- right-route/shape [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- right-route/shape [29.8, 35]: reviewed, unchanged; 주장 ['c032']; 미해결 []
- right-marker/identity [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- right-marker/identity [29.8, 35]: reviewed, unchanged; 주장 ['c033']; 미해결 []
- right-marker/position [25, 29.8]: not_applicable, not_applicable; 주장 []; 미해결 []
- right-marker/position [29.8, 35]: reviewed, changed; 주장 ['c034']; 미해결 []
- caption/identity [25, 31.4]: not_applicable, not_applicable; 주장 []; 미해결 []
- caption/identity [31.4, 35]: reviewed, unchanged; 주장 ['c035']; 미해결 []
- caption/text [25, 31.4]: not_applicable, not_applicable; 주장 []; 미해결 []
- caption/text [31.4, 35]: reviewed, unchanged; 주장 ['c036', 'c037', 'c038']; 미해결 []
- caption/visibility [25, 31.4]: not_applicable, not_applicable; 주장 []; 미해결 []
- caption/visibility [31.4, 35]: reviewed, changed; 주장 ['c039']; 미해결 []
- [u01] open: 두 지도 드론 표시의 정확 방문 순서·속도·회전은 무엇인가? / 현재 표본 또는 개발 검수 범위만으로 확정하지 않음 / 다음 확인: 해당 원본 ROI·구간 표본을 먼저 보강하고 같은 대상의 전후를 비교
- [u02] open: 패널 성장·전환의 정확 시작/끝·가감속은 무엇인가? / 현재 표본 또는 개발 검수 범위만으로 확정하지 않음 / 다음 확인: 해당 원본 ROI·구간 표본을 먼저 보강하고 같은 대상의 전후를 비교
- [u03] open: 정확한 글꼴·색·좌표 수치와 원고 대응은 무엇인가? / 현재 표본 또는 개발 검수 범위만으로 확정하지 않음 / 다음 확인: 해당 원본 ROI·구간 표본을 먼저 보강하고 같은 대상의 전후를 비교

## 재사용 패턴


## 내용 검수 범위
- 검수한 고유 주장: 39/39
- 주장 분모 검토 완료: False
- 남은 범위: ['지원 판정은 이 실행의 AI 재대조 상태이며 사람 정답 아님. 미세 모션·정확 수치·고유 주장 전수 분모는 미완료.']
- 한계: ['기존 추출 표본을 실제 열람한 AI 개발 실행. 새 홀드아웃·독립 채점 아님.', '오디오·시나리오 대응·원본 AE 값은 미검수.', '전체 디자인 기술을 원자 주장 분모에 모두 편입하는 전수 검수는 미완료.', '세계 좌표 비행과 화면상 움직임은 다르며 카메라·가림·영상 전환 영향을 분리한다.']


## 근거 파일

- [f00] 25초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00750_025.000.png
- [f01] 127/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00762_025.400.png
- [f02] 129/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00774_025.800.png
- [f03] 131/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00786_026.200.png
- [f04] 133/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00798_026.600.png
- [f05] 27초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00810_027.000.png
- [f06] 137/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00822_027.400.png
- [f07] 139/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00834_027.800.png
- [f08] 141/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00846_028.200.png
- [f09] 143/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00858_028.600.png
- [f10] 29초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00870_029.000.png
- [f11] 147/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00882_029.400.png
- [f12] 149/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00894_029.800.png
- [f13] 151/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00906_030.200.png
- [f14] 153/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00918_030.600.png
- [f15] 31초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00930_031.000.png
- [f16] 157/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00942_031.400.png
- [f17] 159/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00954_031.800.png
- [f18] 161/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00966_032.200.png
- [f19] 163/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00978_032.600.png
- [f20] 33초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_00990_033.000.png
- [f21] 167/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_01002_033.400.png
- [f22] 169/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_01014_033.800.png
- [f23] 171/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_01026_034.200.png
- [f24] 173/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_01038_034.600.png
- [f25] 35초 / context_after: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H03\f_01050_035.000.png
