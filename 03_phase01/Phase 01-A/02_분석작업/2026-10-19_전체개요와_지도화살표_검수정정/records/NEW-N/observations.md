# DEV-NEW-N-FIRST-20261019 분석 기록

판본: 0.1.0-draft.8 / video-observation-0.4
원본: D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\한맥 영상\노듈러거더 홍보 영상\노듈러거더홍보영상_한맥(KR)_260622.mp4
구간: [166, 174]초
방법: 사전에 고정한 새 사내 영상 구간을 0.5초 간격 표본 17장으로 추출. 개요 시트를 시간순·정착 상태 역추적으로 확인하고 선택 native 및 검증된 좌우 분할을 대조했다. 기존 정답/원고는 읽지 않음. 동일 AI 개발 실행, 독립 평가 아님. 끝 경계 프레임은 문맥 근거. 동일 문맥의 후속 정밀 검토에서 0.1초 간격 81개 추가 표본을 만들고, N의 오른쪽 설명 영역 또는 P의 지역 카드·프레임 영역을 전 시간순 ROI 시트로 대조했다. 추가 표본 81장을 모두 전체 화면 native로 읽은 것은 아니다. 후속 대상×속성 재대조에서 요약 행의 change를 주장 facet만으로 정하지 않고 실제 시간 변화·미확정에 맞춰 보완했다. 추가로 전체 개요 5초 표본과 지정 ROI, PG 연결선의 30fps 연속 10프레임을 검토했다. 지도 정합은 실제 native ROI와 별도 수치 진단을 대조했다. 동일 AI 후속 검수이며 정밀 검수 완료 아님.
음성 검수: False

구조 검사와 시각 내용 확인·회사 승인은 별개다.

## 전체 디자인

### wide-composite / [166, 174]
7680x2160 전체를 하나의 배경으로 사용하되 왼쪽에는 길이 방향 구조, 오른쪽에는 단면·설명을 병렬 배치. 로고 리본은 좌상단, 공통 자막은 전체 중앙 아래. 후반 왼쪽 설명은 기존 오른쪽 설명과 별개로 추가된다.
전체 요소: background, header, girder, deck, front-arcs, rear-arcs, section, section-arcs, right-label, left-label, caption
근거: f08

- hierarchy: 좌상단 섹션 표제 → 왼쪽 큰 3D 구조와 오른쪽 단면 → 청록 강조·짧은 설명 → 하단 자막. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032'])
- alignment: 두 주 콘텐츠는 초광폭의 서로 다른 영역에 배치하고 설명은 각각의 도해 위에 맞춘다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032'])
- spacing: 구조물이 대각으로 깊이를 만들고 두 도해 사이에 어두운 여백을 남긴다. 자막은 두 영역 아래 중앙을 잇는다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032'])
- typography: 흰 산세리프 한글. 섹션 리본, 도해 설명, 공통 자막의 크기·배경 역할이 다르며 정확 서체·크기 미측정. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032'])
- color: 남청·청색 배경, 흰/회색 콘크리트·검은 안쪽, 청록 화살표·세로선. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032'])
- background: 점·선 망과 곡선·푸른 빛이 이어지는 넓은 기술 배경. 미세 배경 모션은 미해결. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032'])
- shapes: 사선 리본, 단면 구멍과 돌출 날개·철근, 양끝 화살촉 곡선, 세로선 양끝의 설명 띠와 사각 자막. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032'])

## 전체 흐름과 세부 모션

### flow: 긴 거더 시점·상판 조립 → 오른쪽 단면·설명 등장 → 두 영역 화살표 강조·기울기 → 왼쪽 새 설명 시작 / [166, 174]
- [c006] 166초에는 구조물이 왼쪽 아래부터 위쪽으로 크게 뻗고 167~167.5초 앞 단면이 더 드러나는 대각 구도로 정리된다. 171~171.5초에는 구조물의 기울어진 시점도 변한다. 카메라와 물체 변환의 기여는 분리 확정하지 않는다.
- [c007] 166초 화면 경계를 벗어나는 구조물에서 167.5초 전면과 길이 방향이 함께 보이는 범위로 바뀐다. 실제 모델 스케일 변경으로 단정하지 않는다.
- [c009] 167초 일부 흰 판이 구조물 위쪽에 분리되어 떠 있는 단계가 보이고 167.5~168초에는 긴 구조물 위를 더 연속으로 덮는 상태가 된다. 정확 이동 곡선·각 판 순서는 미확정.
- [c010] 166초 위쪽 안쪽이 열린 거더와 뒤 표본의 흰 판이 덮인 거더를 구분한다. 화면 전체 축소만으로 내부 변화 설명을 대체하지 않는다.
- [c012] 169초 희미한 곡선이 보이고 169.5~170초 더 선명해진다. 173.5초에는 같은 앞 단면의 화살표가 약해져 있다. 정확 점멸 주기는 미확정.
- [c015] 170초 원본 좌측 영역에는 앞 단면뿐 아니라 먼 뒤쪽 끝에도 작은 청록 곡선·화살표가 보인다. 앞쪽 효과와 별도 대상으로 연결한다.
- [c017] 167.5초에는 오른쪽 도해가 아직 뚜렷하지 않고 168초 오른쪽 중앙 아래에 작은 단면이 보인다. 168.5초 이후 단면과 상단 설명이 함께 자리 잡는다.
- [c018] 170초에 비해 171.5초 단면 상단이 오른쪽 위로 기울어져 보이고 172.5초 다시 더 수평에 가까워 보인다. 반복 여부·정확 각도는 미측정.
- [c020] 168.5초에는 오른쪽 단면 주변 곡선이 뚜렷하지 않고 169초 일부가 보이며 169.5~170초 더 선명하다.
- [c024] 167.2초 표본에서는 설명 세로선이 뚜렷하지 않고 167.3초 옅은 단일 세로선이 보인다. 167.9초 가까운 두 선, 168.2초 부분 글자, 168.6~168.7초 문구가 전체로 읽히는 상태가 된다. 두 선 사이 가로 범위 전개와 글자의 가시성은 서로 구분한다.
- [c025] 167.5~169초 양끝 청록선 사이의 가로로 보이는 범위가 커진다. 실제 폭·마스크·다른 리빌 구현 중 무엇인지는 미확정.
- [c027] 173초 작은 세로선 뒤 173.5초 부분 글자가 있는 띠가 나타난다. 174초 경계 표본은 더 읽히는 문맥이며 구간 밖 완성 과정을 관찰했다고 쓰지 않는다.
- [c032] 167~167.5초 사이 자막 내용이 바뀐다. 174초 끝 문맥에는 다음 문장으로 교체되므로 전체 영상의 최종 자막이라고 쓰지 않는다.
- [c033] 확인한 좌측 점·망사 ROI와 오른쪽 푸른 배경 ROI에서는 166→168→170초에 더 밝아지고 170/172/174초 표본은 유사한 밝기다. 같은 무늬의 위치는 대체로 유지된다. 전체 배경의 미세 이동·밝기 곡선·실제 opacity 구현은 이 표본으로 확정하지 않는다.
- [c034] 먼 끝 ROI는 168.5초에 곡선이 뚜렷하지 않고 169초에 희미한 일부, 169.5초에 더 분명한 곡선, 170~173초 표본에 청록 쌍 곡선이 보인다. 173.5초에는 약해지고 174초 문맥 표본에는 보이지 않는다. 정확 출현·소실 시각은 인접 표본 사이이며 전체 주기와 가감속은 미확정이다.
반복 패턴 참조: []

### detail: 앞·먼 끝·오른쪽 화살표 분리, 단면과 시점 변화 구분, 설명 띠의 중간 상태·자막 교체 / [166, 174]
- [c002] 두 영역에 남청색·청색 빛과 낮은 대비의 선·점이 이어지고 흰 구조물·청록 강조가 대비된다.
- [c004] 3. 노듈러거더 핵심기술
- [c006] 166초에는 구조물이 왼쪽 아래부터 위쪽으로 크게 뻗고 167~167.5초 앞 단면이 더 드러나는 대각 구도로 정리된다. 171~171.5초에는 구조물의 기울어진 시점도 변한다. 카메라와 물체 변환의 기여는 분리 확정하지 않는다.
- [c007] 166초 화면 경계를 벗어나는 구조물에서 167.5초 전면과 길이 방향이 함께 보이는 범위로 바뀐다. 실제 모델 스케일 변경으로 단정하지 않는다.
- [c009] 167초 일부 흰 판이 구조물 위쪽에 분리되어 떠 있는 단계가 보이고 167.5~168초에는 긴 구조물 위를 더 연속으로 덮는 상태가 된다. 정확 이동 곡선·각 판 순서는 미확정.
- [c010] 166초 위쪽 안쪽이 열린 거더와 뒤 표본의 흰 판이 덮인 거더를 구분한다. 화면 전체 축소만으로 내부 변화 설명을 대체하지 않는다.
- [c012] 169초 희미한 곡선이 보이고 169.5~170초 더 선명해진다. 173.5초에는 같은 앞 단면의 화살표가 약해져 있다. 정확 점멸 주기는 미확정.
- [c013] 앞 단면 좌우를 감싸는 두 곡선에 양끝 화살촉이 있다. 회전 의미를 암시하지만 실제 힘이나 물체 운동의 물리량은 판정하지 않는다.
- [c015] 170초 원본 좌측 영역에는 앞 단면뿐 아니라 먼 뒤쪽 끝에도 작은 청록 곡선·화살표가 보인다. 앞쪽 효과와 별도 대상으로 연결한다.
- [c017] 167.5초에는 오른쪽 도해가 아직 뚜렷하지 않고 168초 오른쪽 중앙 아래에 작은 단면이 보인다. 168.5초 이후 단면과 상단 설명이 함께 자리 잡는다.
- [c018] 170초에 비해 171.5초 단면 상단이 오른쪽 위로 기울어져 보이고 172.5초 다시 더 수평에 가까워 보인다. 반복 여부·정확 각도는 미측정.
- [c020] 168.5초에는 오른쪽 단면 주변 곡선이 뚜렷하지 않고 169초 일부가 보이며 169.5~170초 더 선명하다.
- [c021] 오른쪽 단면의 좌우에 각각 양끝 화살촉이 달린 청록 호가 있어 좌측 큰 구조물의 강조와 대응한다.
- [c023] 횡방향보강으로 단면 안정성 향상
- [c024] 167.2초 표본에서는 설명 세로선이 뚜렷하지 않고 167.3초 옅은 단일 세로선이 보인다. 167.9초 가까운 두 선, 168.2초 부분 글자, 168.6~168.7초 문구가 전체로 읽히는 상태가 된다. 두 선 사이 가로 범위 전개와 글자의 가시성은 서로 구분한다.
- [c025] 167.5~169초 양끝 청록선 사이의 가로로 보이는 범위가 커진다. 실제 폭·마스크·다른 리빌 구현 중 무엇인지는 미확정.
- [c027] 173초 작은 세로선 뒤 173.5초 부분 글자가 있는 띠가 나타난다. 174초 경계 표본은 더 읽히는 문맥이며 구간 밖 완성 과정을 관찰했다고 쓰지 않는다.
- [c028] 174초 경계 문맥에서 캔틸레버 바닥판 시공시 동바리 역할 수행이라는 문구가 읽힌다. 분석 창 안 173.5초에는 아직 부분 판독 상태다.
- [c030] 166~167초: 하부 바닥판을 타설하는 습식연결 방식을 가능하게 하는 구성요소이며,
- [c031] 167.5초 이후: 단면의 안정성을 높이는 횡방향 보강격벽이자,
- [c032] 167~167.5초 사이 자막 내용이 바뀐다. 174초 끝 문맥에는 다음 문장으로 교체되므로 전체 영상의 최종 자막이라고 쓰지 않는다.
- [c033] 확인한 좌측 점·망사 ROI와 오른쪽 푸른 배경 ROI에서는 166→168→170초에 더 밝아지고 170/172/174초 표본은 유사한 밝기다. 같은 무늬의 위치는 대체로 유지된다. 전체 배경의 미세 이동·밝기 곡선·실제 opacity 구현은 이 표본으로 확정하지 않는다.
- [c034] 먼 끝 ROI는 168.5초에 곡선이 뚜렷하지 않고 169초에 희미한 일부, 169.5초에 더 분명한 곡선, 170~173초 표본에 청록 쌍 곡선이 보인다. 173.5초에는 약해지고 174초 문맥 표본에는 보이지 않는다. 정확 출현·소실 시각은 인접 표본 사이이며 전체 주기와 가감속은 미확정이다.
반복 패턴 참조: []

## 대상 식별과 고유 주장

### background: 초광폭 기술 배경
어두운 남청색 바탕, 좌측 점·망사와 하단 곡선·작은 광점
식별: reviewed / 초광폭 기술 배경; 후보 []

- [c001] identity/identity/visible-form: 구간 안에서 관측된 형태: 어두운 남청색 바탕, 좌측 점·망사와 하단 곡선·작은 광점 (observed; 내용 supported; 근거 ['f00'])
- [c002] color/value/palette: 두 영역에 남청색·청색 빛과 낮은 대비의 선·점이 이어지고 흰 구조물·청록 강조가 대비된다. (observed; 내용 supported; 근거 ['f00', 'f08'])
- [c033] color/value/local-brightness-evolution: 확인한 좌측 점·망사 ROI와 오른쪽 푸른 배경 ROI에서는 166→168→170초에 더 밝아지고 170/172/174초 표본은 유사한 밝기다. 같은 무늬의 위치는 대체로 유지된다. 전체 배경의 미세 이동·밝기 곡선·실제 opacity 구현은 이 표본으로 확정하지 않는다. (observed; 내용 supported; 근거 ['p098', 'p099', 'p100', 'p101', 'p102', 'p103', 'p104', 'p105', 'p106', 'p107'])

### header: 좌상단 한맥 로고·섹션 리본
흰 로고 칸과 파란 사선 리본·흰 한글
식별: reviewed / 좌상단 한맥 로고·섹션 리본; 후보 []

- [c003] identity/identity/visible-form: 구간 안에서 관측된 형태: 흰 로고 칸과 파란 사선 리본·흰 한글 (observed; 내용 supported; 근거 ['f08'])
- [c004] text/value/section: 3. 노듈러거더 핵심기술 (observed; 내용 supported; 근거 ['f08'])

### girder: 왼쪽 긴 거더 구조
구멍과 철근이 있는 회색 장대 구조물, 앞쪽 단면과 뒤로 이어지는 반복 부재
식별: reviewed / 왼쪽 긴 거더 구조; 후보 []

- [c005] identity/identity/visible-form: 구간 안에서 관측된 형태: 구멍과 철근이 있는 회색 장대 구조물, 앞쪽 단면과 뒤로 이어지는 반복 부재 (observed; 내용 supported; 근거 ['f08'])
- [c006] position/direction/screen-view: 166초에는 구조물이 왼쪽 아래부터 위쪽으로 크게 뻗고 167~167.5초 앞 단면이 더 드러나는 대각 구도로 정리된다. 171~171.5초에는 구조물의 기울어진 시점도 변한다. 카메라와 물체 변환의 기여는 분리 확정하지 않는다. (observed; 내용 supported; 근거 ['f00', 'f02', 'f03', 'f10', 'f11'])
- [c007] size/direction/projected-extent: 166초 화면 경계를 벗어나는 구조물에서 167.5초 전면과 길이 방향이 함께 보이는 범위로 바뀐다. 실제 모델 스케일 변경으로 단정하지 않는다. (observed; 내용 supported; 근거 ['f00', 'f02', 'f03'])

### deck: 구조물 위 흰 상판 조각
검은 고리 모양 철근을 가진 흰 판들이 길이 방향으로 반복
식별: reviewed / 구조물 위 흰 상판 조각; 후보 []

- [c008] identity/identity/visible-form: 구간 안에서 관측된 형태: 검은 고리 모양 철근을 가진 흰 판들이 길이 방향으로 반복 (observed; 내용 supported; 근거 ['f02'])
- [c009] position/direction/assembly: 167초 일부 흰 판이 구조물 위쪽에 분리되어 떠 있는 단계가 보이고 167.5~168초에는 긴 구조물 위를 더 연속으로 덮는 상태가 된다. 정확 이동 곡선·각 판 순서는 미확정. (observed; 내용 supported; 근거 ['f01', 'f02', 'f03', 'f04'])
- [c010] internal_state/value/open-versus-covered: 166초 위쪽 안쪽이 열린 거더와 뒤 표본의 흰 판이 덮인 거더를 구분한다. 화면 전체 축소만으로 내부 변화 설명을 대체하지 않는다. (observed; 내용 supported; 근거 ['f00', 'f02', 'f04'])

### front-arcs: 왼쪽 거더 앞 단면 주변 청록 곡선 화살표
앞 단면 좌우에 위·아래 화살촉을 가진 굵은 청록 곡선
식별: reviewed / 왼쪽 거더 앞 단면 주변 청록 곡선 화살표; 후보 []

- [c011] identity/identity/visible-form: 구간 안에서 관측된 형태: 앞 단면 좌우에 위·아래 화살촉을 가진 굵은 청록 곡선 (observed; 내용 supported; 근거 ['f08'])
- [c012] visibility/direction/draw-and-fade: 169초 희미한 곡선이 보이고 169.5~170초 더 선명해진다. 173.5초에는 같은 앞 단면의 화살표가 약해져 있다. 정확 점멸 주기는 미확정. (observed; 내용 supported; 근거 ['f05', 'f06', 'f07', 'f08', 'f15'])
- [c013] shape/value/paired-arcs: 앞 단면 좌우를 감싸는 두 곡선에 양끝 화살촉이 있다. 회전 의미를 암시하지만 실제 힘이나 물체 운동의 물리량은 판정하지 않는다. (observed; 내용 supported; 근거 ['f08'])

### rear-arcs: 왼쪽 거더 먼 끝의 작은 화살표
긴 구조물 뒤쪽 끝 부근에도 작게 보이는 청록 곡선 한 쌍
식별: reviewed / 왼쪽 거더 먼 끝의 작은 화살표; 후보 []

- [c014] identity/identity/visible-form: 구간 안에서 관측된 형태: 긴 구조물 뒤쪽 끝 부근에도 작게 보이는 청록 곡선 한 쌍 (observed; 내용 supported; 근거 ['f08'])
- [c015] visibility/presence/far-end-effect: 170초 원본 좌측 영역에는 앞 단면뿐 아니라 먼 뒤쪽 끝에도 작은 청록 곡선·화살표가 보인다. 앞쪽 효과와 별도 대상으로 연결한다. (observed; 내용 supported; 근거 ['f08', 'f15'])
- [c034] visibility/value/sampled-onset-and-exit: 먼 끝 ROI는 168.5초에 곡선이 뚜렷하지 않고 169초에 희미한 일부, 169.5초에 더 분명한 곡선, 170~173초 표본에 청록 쌍 곡선이 보인다. 173.5초에는 약해지고 174초 문맥 표본에는 보이지 않는다. 정확 출현·소실 시각은 인접 표본 사이이며 전체 주기와 가감속은 미확정이다. (observed; 내용 supported; 근거 ['p108', 'p109', 'p110', 'p111', 'p112', 'p113', 'p114', 'p115', 'p116', 'p117', 'p118', 'p119'])

### section: 오른쪽 단면 도해
중앙 검은 구멍과 둥근 홈, 위로 넓은 회색 단면
식별: reviewed / 오른쪽 단면 도해; 후보 []

- [c016] identity/identity/visible-form: 구간 안에서 관측된 형태: 중앙 검은 구멍과 둥근 홈, 위로 넓은 회색 단면 (observed; 내용 supported; 근거 ['f08'])
- [c017] visibility/order/enter: 167.5초에는 오른쪽 도해가 아직 뚜렷하지 않고 168초 오른쪽 중앙 아래에 작은 단면이 보인다. 168.5초 이후 단면과 상단 설명이 함께 자리 잡는다. (observed; 내용 supported; 근거 ['f03', 'f04', 'f05', 'f08'])
- [c018] position/direction/tilt: 170초에 비해 171.5초 단면 상단이 오른쪽 위로 기울어져 보이고 172.5초 다시 더 수평에 가까워 보인다. 반복 여부·정확 각도는 미측정. (observed; 내용 supported; 근거 ['f08', 'f11', 'f13'])

### section-arcs: 오른쪽 단면 청록 곡선 화살표
오른쪽 단면 좌우를 감싸는 굵은 곡선과 양끝 화살촉
식별: reviewed / 오른쪽 단면 청록 곡선 화살표; 후보 []

- [c019] identity/identity/visible-form: 구간 안에서 관측된 형태: 오른쪽 단면 좌우를 감싸는 굵은 곡선과 양끝 화살촉 (observed; 내용 supported; 근거 ['f08'])
- [c020] visibility/direction/enter: 168.5초에는 오른쪽 단면 주변 곡선이 뚜렷하지 않고 169초 일부가 보이며 169.5~170초 더 선명하다. (observed; 내용 supported; 근거 ['f05', 'f06', 'f07', 'f08'])
- [c021] shape/value/paired-arcs: 오른쪽 단면의 좌우에 각각 양끝 화살촉이 달린 청록 호가 있어 좌측 큰 구조물의 강조와 대응한다. (observed; 내용 supported; 근거 ['f08'])

### right-label: 오른쪽 설명 띠와 글자
짙은 반투명 가로 띠, 양끝 청록 세로선, 흰 한글
식별: reviewed / 오른쪽 설명 띠와 글자; 후보 []

- [c022] identity/identity/visible-form: 구간 안에서 관측된 형태: 짙은 반투명 가로 띠, 양끝 청록 세로선, 흰 한글 (observed; 내용 supported; 근거 ['f08'])
- [c023] text/value/headline: 횡방향보강으로 단면 안정성 향상 (observed; 내용 supported; 근거 ['f08'])
- [c024] visibility/order/reveal: 167.2초 표본에서는 설명 세로선이 뚜렷하지 않고 167.3초 옅은 단일 세로선이 보인다. 167.9초 가까운 두 선, 168.2초 부분 글자, 168.6~168.7초 문구가 전체로 읽히는 상태가 된다. 두 선 사이 가로 범위 전개와 글자의 가시성은 서로 구분한다. (observed; 내용 supported; 근거 ['x029', 'x030', 'x036', 'x039', 'x043', 'x044'])
- [c025] size/direction/width: 167.5~169초 양끝 청록선 사이의 가로로 보이는 범위가 커진다. 실제 폭·마스크·다른 리빌 구현 중 무엇인지는 미확정. (observed; 내용 supported; 근거 ['f03', 'f04', 'f05', 'f06'])

### left-label: 후반 왼쪽 설명 띠
왼쪽 모델 위쪽에 새로 생기는 청록 양끝선·어두운 띠와 문구
식별: reviewed / 후반 왼쪽 설명 띠; 후보 []

- [c026] identity/identity/visible-form: 구간 안에서 관측된 형태: 왼쪽 모델 위쪽에 새로 생기는 청록 양끝선·어두운 띠와 문구 (observed; 내용 supported; 근거 ['f15'])
- [c027] visibility/direction/late-enter: 173초 작은 세로선 뒤 173.5초 부분 글자가 있는 띠가 나타난다. 174초 경계 표본은 더 읽히는 문맥이며 구간 밖 완성 과정을 관찰했다고 쓰지 않는다. (observed; 내용 supported; 근거 ['f14', 'f15', 'f16'])
- [c028] text/value/boundary-copy: 174초 경계 문맥에서 캔틸레버 바닥판 시공시 동바리 역할 수행이라는 문구가 읽힌다. 분석 창 안 173.5초에는 아직 부분 판독 상태다. (observed; 내용 supported; 근거 ['f15', 'f16'])

### caption: 화면 하단 공통 자막
초광폭 중앙 아래의 짙은 청색 바탕과 흰 한글
식별: reviewed / 화면 하단 공통 자막; 후보 []

- [c029] identity/identity/visible-form: 구간 안에서 관측된 형태: 초광폭 중앙 아래의 짙은 청색 바탕과 흰 한글 (observed; 내용 supported; 근거 ['f00'])
- [c030] text/value/copy-before: 166~167초: 하부 바닥판을 타설하는 습식연결 방식을 가능하게 하는 구성요소이며, (observed; 내용 supported; 근거 ['f00', 'f02'])
- [c031] text/value/copy-middle: 167.5초 이후: 단면의 안정성을 높이는 횡방향 보강격벽이자, (observed; 내용 supported; 근거 ['f05', 'f08'])
- [c032] visibility/order/copy-change: 167~167.5초 사이 자막 내용이 바뀐다. 174초 끝 문맥에는 다음 문장으로 교체되므로 전체 영상의 최종 자막이라고 쓰지 않는다. (observed; 내용 supported; 근거 ['f02', 'f03', 'f15', 'f16'])

## 검토 행과 미해결

- background/identity [166, 174]: reviewed, unchanged; 주장 ['c001']; 미해결 []
- background/color [166, 174]: reviewed, changed; 주장 ['c002', 'c033']; 미해결 []
- header/identity [166, 174]: reviewed, unchanged; 주장 ['c003']; 미해결 []
- header/text [166, 174]: reviewed, unchanged; 주장 ['c004']; 미해결 []
- girder/identity [166, 174]: reviewed, unchanged; 주장 ['c005']; 미해결 []
- girder/position [166, 174]: reviewed, changed; 주장 ['c006']; 미해결 []
- girder/size [166, 174]: reviewed, changed; 주장 ['c007']; 미해결 []
- deck/identity [166, 174]: reviewed, unchanged; 주장 ['c008']; 미해결 []
- deck/position [166, 174]: reviewed, changed; 주장 ['c009']; 미해결 []
- deck/internal_state [166, 174]: reviewed, unchanged; 주장 ['c010']; 미해결 []
- front-arcs/identity [166, 174]: reviewed, unchanged; 주장 ['c011']; 미해결 []
- front-arcs/visibility [166, 174]: reviewed, changed; 주장 ['c012']; 미해결 []
- front-arcs/shape [166, 174]: reviewed, unchanged; 주장 ['c013']; 미해결 []
- rear-arcs/identity [166, 174]: reviewed, unchanged; 주장 ['c014']; 미해결 []
- rear-arcs/visibility [166, 174]: reviewed, changed; 주장 ['c015', 'c034']; 미해결 []
- section/identity [166, 174]: reviewed, unchanged; 주장 ['c016']; 미해결 []
- section/visibility [166, 174]: reviewed, changed; 주장 ['c017']; 미해결 []
- section/position [166, 174]: reviewed, changed; 주장 ['c018']; 미해결 []
- section-arcs/identity [166, 174]: reviewed, unchanged; 주장 ['c019']; 미해결 []
- section-arcs/visibility [166, 174]: reviewed, changed; 주장 ['c020']; 미해결 []
- section-arcs/shape [166, 174]: reviewed, unchanged; 주장 ['c021']; 미해결 []
- right-label/identity [166, 174]: reviewed, unchanged; 주장 ['c022']; 미해결 []
- right-label/text [166, 174]: reviewed, unchanged; 주장 ['c023']; 미해결 []
- right-label/visibility [166, 174]: reviewed, changed; 주장 ['c024']; 미해결 []
- right-label/size [166, 174]: reviewed, changed; 주장 ['c025']; 미해결 []
- left-label/identity [166, 174]: reviewed, unchanged; 주장 ['c026']; 미해결 []
- left-label/visibility [166, 174]: reviewed, changed; 주장 ['c027']; 미해결 []
- left-label/text [166, 174]: reviewed, unchanged; 주장 ['c028']; 미해결 []
- caption/identity [166, 174]: reviewed, unchanged; 주장 ['c029']; 미해결 []
- caption/text [166, 174]: reviewed, changed; 주장 ['c030', 'c031']; 미해결 []
- caption/visibility [166, 174]: reviewed, changed; 주장 ['c032']; 미해결 []
- background/internal_state [166, 174]: unresolved, unknown; 주장 []; 미해결 ['u01']
- [u01] open: 배경의 작은 점·선·빛에 독립적인 변화가 있는가? / 양측 ROI 166/168/170/172/174초에서 밝기 변화와 위치 유사를 확인함. 연속 미세 변화와 전체 배경 영역의 독립성·정확 곡선은 남음. / 다음 확인: 같은 배경 ROI의 진행 중 연속 프레임과 하단 곡선 영역을 비교해 밝기/위치 변화 및 다른 요소의 겹침을 분리
- [u02] open: 화살표의 정확 주기·가감속과 앞뒤 강조의 동기화는? / 존재·차이는 보았지만 각 효과를 연속 추적하지 않음 / 다음 확인: 사용 목적에 필요한 부분의 native ROI·시간 표본을 보강하고, 구현값이 필요하면 원본 프로젝트 확인
- [u03] open: 왼쪽 설명의 완성 이후 전체 상태와 정확 리빌 방식은? / 분석 창 끝에서 등장 중이며 끝 이후 표본은 문맥 1장뿐임 / 다음 확인: 사용 목적에 필요한 부분의 native ROI·시간 표본을 보강하고, 구현값이 필요하면 원본 프로젝트 확인
- [u04] resolved: 먼 끝의 작은 화살표는 어느 시각부터 어떤 강약으로 변하는가? / 0.5초 표본의 출현 범위·강약·소실을 추가 관측. 정확 프레임 경계·반복 파형은 u02에 남음. / 다음 확인: 

## 재사용 패턴


## 내용 검수 범위
- 검수한 고유 주장: 34/34
- 주장 분모 검토 완료: False
- 남은 범위: ['동일 AI의 후속 검수. 원본 전체 정밀 분석·독립 정답·모든 미발견 요소의 분모는 미확인.', '열린 쟁점 u01, u02, u03']
- 한계: ['정확한 글꼴·색·좌표·키프레임·이징·주기·제작 의도는 미확정.', '0.5초 간격 표본 사이 사건·가림·미세 변화가 남을 수 있음.', '화면 속 홍보 문구의 기술적·정책적 사실성을 검증한 것이 아님.', '선택 표본을 통한 전체 디자인의 정성 기록이며 모든 속성의 연속 측정은 아님.', '전체 원본 영상에서 확인한 구간은 8초. 원본 전체 분석 완료 아님.', '0.1초 보강은 지정 ROI의 상세 확인. 다른 대상·전체 프레임의 완전성을 보장하지 않음.']


## 근거 파일

- [f00] 166초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_04980_166.000.png
- [f01] 333/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_04995_166.500.png
- [f02] 167초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05010_167.000.png
- [f03] 335/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05025_167.500.png
- [f04] 168초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05040_168.000.png
- [f05] 337/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05055_168.500.png
- [f06] 169초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05070_169.000.png
- [f07] 339/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05085_169.500.png
- [f08] 170초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05100_170.000.png
- [f09] 341/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05115_170.500.png
- [f10] 171초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05130_171.000.png
- [f11] 343/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05145_171.500.png
- [f12] 172초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05160_172.000.png
- [f13] 345/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05175_172.500.png
- [f14] 173초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05190_173.000.png
- [f15] 347/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05205_173.500.png
- [f16] 174초 / context_after: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\window\f_05220_174.000.png
- [x017] 166초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_04980_166.000.png
- [x018] 1661/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_04983_166.100.png
- [x019] 831/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_04986_166.200.png
- [x020] 1663/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_04989_166.300.png
- [x021] 832/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_04992_166.400.png
- [x022] 333/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_04995_166.500.png
- [x023] 833/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_04998_166.600.png
- [x024] 1667/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05001_166.700.png
- [x025] 834/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05004_166.800.png
- [x026] 1669/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05007_166.900.png
- [x027] 167초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05010_167.000.png
- [x028] 1671/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05013_167.100.png
- [x029] 836/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05016_167.200.png
- [x030] 1673/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05019_167.300.png
- [x031] 837/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05022_167.400.png
- [x032] 335/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05025_167.500.png
- [x033] 838/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05028_167.600.png
- [x034] 1677/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05031_167.700.png
- [x035] 839/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05034_167.800.png
- [x036] 1679/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05037_167.900.png
- [x037] 168초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05040_168.000.png
- [x038] 1681/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05043_168.100.png
- [x039] 841/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05046_168.200.png
- [x040] 1683/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05049_168.300.png
- [x041] 842/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05052_168.400.png
- [x042] 337/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05055_168.500.png
- [x043] 843/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail1\f_05058_168.600.png
- [x044] 1687/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05061_168.700.png
- [x045] 844/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05064_168.800.png
- [x046] 1689/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05067_168.900.png
- [x047] 169초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05070_169.000.png
- [x048] 1691/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05073_169.100.png
- [x049] 846/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05076_169.200.png
- [x050] 1693/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05079_169.300.png
- [x051] 847/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05082_169.400.png
- [x052] 339/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05085_169.500.png
- [x053] 848/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05088_169.600.png
- [x054] 1697/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05091_169.700.png
- [x055] 849/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05094_169.800.png
- [x056] 1699/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05097_169.900.png
- [x057] 170초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05100_170.000.png
- [x058] 1701/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05103_170.100.png
- [x059] 851/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05106_170.200.png
- [x060] 1703/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05109_170.300.png
- [x061] 852/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05112_170.400.png
- [x062] 341/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05115_170.500.png
- [x063] 853/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05118_170.600.png
- [x064] 1707/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05121_170.700.png
- [x065] 854/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05124_170.800.png
- [x066] 1709/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05127_170.900.png
- [x067] 171초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05130_171.000.png
- [x068] 1711/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05133_171.100.png
- [x069] 856/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05136_171.200.png
- [x070] 1713/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail2\f_05139_171.300.png
- [x071] 857/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05142_171.400.png
- [x072] 343/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05145_171.500.png
- [x073] 858/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05148_171.600.png
- [x074] 1717/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05151_171.700.png
- [x075] 859/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05154_171.800.png
- [x076] 1719/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05157_171.900.png
- [x077] 172초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05160_172.000.png
- [x078] 1721/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05163_172.100.png
- [x079] 861/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05166_172.200.png
- [x080] 1723/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05169_172.300.png
- [x081] 862/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05172_172.400.png
- [x082] 345/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05175_172.500.png
- [x083] 863/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05178_172.600.png
- [x084] 1727/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05181_172.700.png
- [x085] 864/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05184_172.800.png
- [x086] 1729/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05187_172.900.png
- [x087] 173초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05190_173.000.png
- [x088] 1731/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05193_173.100.png
- [x089] 866/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05196_173.200.png
- [x090] 1733/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05199_173.300.png
- [x091] 867/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05202_173.400.png
- [x092] 347/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05205_173.500.png
- [x093] 868/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05208_173.600.png
- [x094] 1737/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05211_173.700.png
- [x095] 869/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05214_173.800.png
- [x096] 1739/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05217_173.900.png
- [x097] 174초 / context_after: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-N\detail3\f_05220_174.000.png
- [p098] 166초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-background-left-166.0.png
- [p099] 168초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-background-left-168.0.png
- [p100] 170초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-background-left-170.0.png
- [p101] 172초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-background-left-172.0.png
- [p102] 174초 / context_after: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-background-left-174.0.png
- [p103] 166초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-background-right-166.0.png
- [p104] 168초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-background-right-168.0.png
- [p105] 170초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-background-right-170.0.png
- [p106] 172초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-background-right-172.0.png
- [p107] 174초 / context_after: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-background-right-174.0.png
- [p108] 337/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-rear-168.5.png
- [p109] 169초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-rear-169.0.png
- [p110] 339/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-rear-169.5.png
- [p111] 170초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-rear-170.0.png
- [p112] 341/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-rear-170.5.png
- [p113] 171초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-rear-171.0.png
- [p114] 343/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-rear-171.5.png
- [p115] 172초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-rear-172.0.png
- [p116] 345/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-rear-172.5.png
- [p117] 173초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-rear-173.0.png
- [p118] 347/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-rear-173.5.png
- [p119] 174초 / context_after: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\N-rear-174.0.png
