# DEV-NEW-P-FIRST-20261019 분석 기록

판본: 0.1.0-draft.7 / video-observation-0.4
원본: D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\한맥 영상\PG 착공식_자율주행영상\250609-1_PG착공식_A-combineAll.mp4
구간: [40, 48]초
방법: 사전에 고정한 새 사내 영상 구간을 0.5초 간격 표본 17장으로 추출. 개요 시트를 시간순·정착 상태 역추적으로 확인하고 선택 native 및 검증된 좌우 분할을 대조했다. 기존 정답/원고는 읽지 않음. 동일 AI 개발 실행, 독립 평가 아님. 끝 경계 프레임은 문맥 근거.
음성 검수: False

구조 검사와 시각 내용 확인·회사 승인은 별개다.

## 전체 디자인

### map-composite / [40, 48]
어두운 지형·행정 경계 위 왼쪽 노랑 경찰청 설명 묶음과 중앙 위 분홍 지역 설명 묶음. 횡성은 아래 중앙 청록 강조, 바다는 오른쪽 여백. 하단 검은 자막은 두 설명과 별도.
전체 요소: map, region, police, policy-panel, police-link, gangwon, regional-frame, regional-row1, regional-row2, regional-link, caption
근거: f14

- hierarchy: 지역 지도·횡성 강조를 배경 맥락으로 두고 기관 카드와 연결된 정책 설명을 위에 겹친다. 아래 자막은 별도 정보층. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037'])
- alignment: 기관별 카드 → 세로 연결선 → 위쪽 설명 프레임. 두 기관 묶음을 나란히 배치하고 각 프레임 안 가로 문구 띠를 수직으로 쌓는다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037'])
- spacing: 지도와 지명을 일부 보이게 둔 반투명 패널, 오른쪽 바다의 넓은 여백, 아래 자막과 횡성 강조 사이 간격. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037'])
- typography: 카드의 기관 로고 서체와 설명·자막의 한글 산세리프를 구분한다. 지도 지명은 어둡고 외곽이 있으며 정확 글꼴·크기 미측정. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037'])
- color: 어두운 녹갈색 지도·짙은 남청 바다, 횡성 청록, 경찰청 노랑/연두, 지역 설명 붉은색/분홍, 밝은 로고 카드. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037'])
- background: 위성 지형 질감과 행정 경계·지명. 정보 프레임은 반투명해 지도가 일부 비친다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037'])
- shapes: 화살촉 양끝 문구 띠, 직사각 반투명 면, 가는 모서리·프레임, 세로 화살 무늬·원형 접점, 지역 경계 면과 검은 자막 바. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030', 'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037'])

## 전체 흐름과 세부 모션

### flow: 기존 경찰청 묶음·횡성 지도 유지 → 지역 로고 카드 전개 → 위 프레임·첫 줄 → 둘째 줄과 강조 → 자막 교체·밝기 진행 / [40, 48]
- [c002] 40초와 48초 사이 지도와 기존 기관·설명 묶음의 보이는 크기·배치가 소폭 달라져 전체 구도가 넓어지는 듯하다. 정확 공통 카메라·부모 스케일 변환은 미확정이며 모든 카드가 고정이라고 단정하지 않는다.
- [c008] 40초 구간 시작부터 왼쪽 기관 카드와 위 설명 패널이 보인다. 이 구간만으로 최초 등장 과정을 기록하지 않는다.
- [c017] 41.5~42초 작은 일부 로고가 보이고 42.5초 좁은 밝은 면과 글자, 43초에는 가로로 펼쳐진 기관 카드가 보인다. 정확 문자별·면별 리빌 방식은 미확정.
- [c019] 43초 위쪽에 좁고 세로로 긴 반투명 면과 빈 붉은 띠가 보이고 43.5~44초 가로 폭과 첫 줄 문구가 갖춰진다.
- [c020] 43초의 좁은 배경 프레임이 44초 더 넓은 사각 범위로 보인다. 실제 레이어 폭·회전·마스크 중 무엇인지는 미확정.
- [c023] 43초 빈 붉은 띠 뒤 43.5초 첫 줄 글자가 읽힌다. 배경 면과 글자 완료를 같은 사건으로 뭉치지 않는다.
- [c027] 46초에는 첫 줄만 있고 46.5초 둘째 줄의 어두운 띠가 나타나며 47초 문구가 읽힌다. 첫 줄 등장 뒤 두 번째 줄을 추가한다.
- [c030] 43초 이후 중앙 기관 카드에서 위 프레임으로 이어지는 분홍 연결선이 보인다. 선 내부 무늬의 이동 방향은 연속 확인하지 않았다.
- [c036] 41.5~42초 사이 첫 문구에서 두 번째로, 46~46.5초 사이 두 번째에서 세 번째로 교체되는 표본이 보인다.
반복 패턴 참조: []

### detail: 기관별 프레임·글자·연결선 분리, 첫째·둘째 줄 순서와 강조 강약, 자막 내용과 밝기 진행 구분 / [40, 48]
- [c002] 40초와 48초 사이 지도와 기존 기관·설명 묶음의 보이는 크기·배치가 소폭 달라져 전체 구도가 넓어지는 듯하다. 정확 공통 카메라·부모 스케일 변환은 미확정이며 모든 카드가 고정이라고 단정하지 않는다.
- [c004] 횡성
- [c005] 어두운 지도 안에서 횡성 영역을 청록색 채움과 밝은 외곽으로 강조한다. 이 색은 정책·기관 설명의 노랑/분홍과 별도다.
- [c007] 경찰청
- [c008] 40초 구간 시작부터 왼쪽 기관 카드와 위 설명 패널이 보인다. 이 구간만으로 최초 등장 과정을 기록하지 않는다.
- [c010] 자율주행자동차 운행 안전관리를 위한 도로교통법 개정 추진
- [c011] 완전 자율주행시대에 대비한 도로교통안전 추진 전략 수립
- [c012] 노랑·연두 띠의 밝기와 테두리 강도가 선택 시점에서 달라 보인다. 정확 반복 주기·행별 동기화는 미확정.
- [c014] 경찰청 카드 위쪽에서 노란 연결선이 설명 패널 아래 접점으로 이어져 카드와 위 두 문구의 소속 관계를 시각적으로 묶는다.
- [c016] 강원특별자치도
- [c017] 41.5~42초 작은 일부 로고가 보이고 42.5초 좁은 밝은 면과 글자, 43초에는 가로로 펼쳐진 기관 카드가 보인다. 정확 문자별·면별 리빌 방식은 미확정.
- [c019] 43초 위쪽에 좁고 세로로 긴 반투명 면과 빈 붉은 띠가 보이고 43.5~44초 가로 폭과 첫 줄 문구가 갖춰진다.
- [c020] 43초의 좁은 배경 프레임이 44초 더 넓은 사각 범위로 보인다. 실제 레이어 폭·회전·마스크 중 무엇인지는 미확정.
- [c022] 강원특별자치도 미래산업글로벌도시 조성
- [c023] 43초 빈 붉은 띠 뒤 43.5초 첫 줄 글자가 읽힌다. 배경 면과 글자 완료를 같은 사건으로 뭉치지 않는다.
- [c024] 첫 줄 띠는 43초 어둡게 보이다 44~44.5초 더 밝은 분홍 강조가 보이고 47초에는 두 번째 줄보다 어둡다.
- [c026] 미래차 전체 주기 기업지원 생태계 구축
- [c027] 46초에는 첫 줄만 있고 46.5초 둘째 줄의 어두운 띠가 나타나며 47초 문구가 읽힌다. 첫 줄 등장 뒤 두 번째 줄을 추가한다.
- [c028] 47초와 48초 둘째 줄은 첫 줄보다 밝은 분홍으로 강조돼 있다. 행별 강조의 전체 주기는 이 구간만으로 확정하지 않는다.
- [c030] 43초 이후 중앙 기관 카드에서 위 프레임으로 이어지는 분홍 연결선이 보인다. 선 내부 무늬의 이동 방향은 연속 확인하지 않았다.
- [c031] 분홍 기관 카드와 위 붉은 설명 프레임을 연결한다. 노란 경찰청 설명과 구분되는 소속 묶음이다.
- [c033] 교통사고로부터 안전한 국민의 일상을 만들어가고 있습니다
- [c034] 강원특별자치도는 5대 첨단산업 클러스터를 조성하여
- [c035] 전기차, 자율주행차 등 첨단산업의 활성화를 추진하고 있습니다
- [c036] 41.5~42초 사이 첫 문구에서 두 번째로, 46~46.5초 사이 두 번째에서 세 번째로 교체되는 표본이 보인다.
- [c037] 42.5초 두 번째 문구의 왼쪽 부분이 더 밝고 뒤는 어두우며 뒤 시점에는 밝은 구간이 늘어난다. 47초 세 번째 문구의 앞부분이 밝고 뒤는 어둡지만 48초 경계에는 더 넓게 밝다. 음성을 듣지 않아 발화와 싱크한다고 판정하지 않는다.
반복 패턴 참조: []

## 대상 식별과 고유 주장

### map: 지역 지도 배경
어두운 위성 지형, 경계선과 회색 지명, 오른쪽 바다
식별: reviewed / 지역 지도 배경; 후보 []

- [c001] identity/identity/visible-form: 구간 안에서 관측된 형태: 어두운 위성 지형, 경계선과 회색 지명, 오른쪽 바다 (observed; 내용 supported; 근거 ['f00'])
- [c002] size/direction/global-framing: 40초와 48초 사이 지도와 기존 기관·설명 묶음의 보이는 크기·배치가 소폭 달라져 전체 구도가 넓어지는 듯하다. 정확 공통 카메라·부모 스케일 변환은 미확정이며 모든 카드가 고정이라고 단정하지 않는다. (observed; 내용 supported; 근거 ['f00', 'f06', 'f16'])

### region: 횡성 강조 영역
청록색 면과 밝은 외곽·흰 횡성 글자
식별: reviewed / 횡성 강조 영역; 후보 []

- [c003] identity/identity/visible-form: 구간 안에서 관측된 형태: 청록색 면과 밝은 외곽·흰 횡성 글자 (observed; 내용 supported; 근거 ['f00'])
- [c004] text/value/label: 횡성 (observed; 내용 supported; 근거 ['f00', 'f06', 'f14'])
- [c005] color/value/highlight: 어두운 지도 안에서 횡성 영역을 청록색 채움과 밝은 외곽으로 강조한다. 이 색은 정책·기관 설명의 노랑/분홍과 별도다. (observed; 내용 supported; 근거 ['f00', 'f06', 'f14'])

### police: 왼쪽 경찰청 로고 카드
노란 독수리 문양·파란 경찰청 글자, 밝은 사각 면과 가는 모서리 선
식별: reviewed / 왼쪽 경찰청 로고 카드; 후보 []

- [c006] identity/identity/visible-form: 구간 안에서 관측된 형태: 노란 독수리 문양·파란 경찰청 글자, 밝은 사각 면과 가는 모서리 선 (observed; 내용 supported; 근거 ['f00'])
- [c007] text/value/agency: 경찰청 (observed; 내용 supported; 근거 ['f00', 'f06'])
- [c008] visibility/presence/already-present: 40초 구간 시작부터 왼쪽 기관 카드와 위 설명 패널이 보인다. 이 구간만으로 최초 등장 과정을 기록하지 않는다. (observed; 내용 supported; 근거 ['f00', 'f06', 'f14'])

### policy-panel: 왼쪽 정책 설명 패널
노랑·연두 가로 화살촉 띠 두 줄, 반투명 사각 면과 바깥 모서리 선
식별: reviewed / 왼쪽 정책 설명 패널; 후보 []

- [c009] identity/identity/visible-form: 구간 안에서 관측된 형태: 노랑·연두 가로 화살촉 띠 두 줄, 반투명 사각 면과 바깥 모서리 선 (observed; 내용 supported; 근거 ['f00'])
- [c010] text/value/policy-1: 자율주행자동차 운행 안전관리를 위한 도로교통법 개정 추진 (observed; 내용 supported; 근거 ['f00', 'f06'])
- [c011] text/value/policy-2: 완전 자율주행시대에 대비한 도로교통안전 추진 전략 수립 (observed; 내용 supported; 근거 ['f00', 'f06'])
- [c012] color/value/row-emphasis: 노랑·연두 띠의 밝기와 테두리 강도가 선택 시점에서 달라 보인다. 정확 반복 주기·행별 동기화는 미확정. (observed; 내용 supported; 근거 ['f00', 'f06', 'f14'])

### police-link: 왼쪽 연결선
기관 카드와 위 패널을 잇는 가는 노란 세로선·반복 화살 모양과 원형 접점
식별: reviewed / 왼쪽 연결선; 후보 []

- [c013] identity/identity/visible-form: 구간 안에서 관측된 형태: 기관 카드와 위 패널을 잇는 가는 노란 세로선·반복 화살 모양과 원형 접점 (observed; 내용 supported; 근거 ['f06'])
- [c014] relation/relation/card-panel-link: 경찰청 카드 위쪽에서 노란 연결선이 설명 패널 아래 접점으로 이어져 카드와 위 두 문구의 소속 관계를 시각적으로 묶는다. (observed; 내용 supported; 근거 ['f06', 'f14'])

### gangwon: 중앙 강원특별자치도 카드
분홍·회색 로고 글자와 밝은 사각 면·모서리 선
식별: reviewed / 중앙 강원특별자치도 카드; 후보 []

- [c015] identity/identity/visible-form: 구간 안에서 관측된 형태: 분홍·회색 로고 글자와 밝은 사각 면·모서리 선 (observed; 내용 supported; 근거 ['f06'])
- [c016] text/value/agency: 강원특별자치도 (observed; 내용 supported; 근거 ['f06', 'f14'])
- [c017] visibility/order/logo-assembly: 41.5~42초 작은 일부 로고가 보이고 42.5초 좁은 밝은 면과 글자, 43초에는 가로로 펼쳐진 기관 카드가 보인다. 정확 문자별·면별 리빌 방식은 미확정. (observed; 내용 supported; 근거 ['f02', 'f03', 'f04', 'f05', 'f06'])

### regional-frame: 오른쪽 지역 설명 프레임
분홍 가는 외곽 모서리, 반투명 사각 면과 붉은 가로 띠
식별: reviewed / 오른쪽 지역 설명 프레임; 후보 []

- [c018] identity/identity/visible-form: 구간 안에서 관측된 형태: 분홍 가는 외곽 모서리, 반투명 사각 면과 붉은 가로 띠 (observed; 내용 supported; 근거 ['f06'])
- [c019] visibility/order/frame-enter: 43초 위쪽에 좁고 세로로 긴 반투명 면과 빈 붉은 띠가 보이고 43.5~44초 가로 폭과 첫 줄 문구가 갖춰진다. (observed; 내용 supported; 근거 ['f05', 'f06', 'f07', 'f08'])
- [c020] size/direction/frame-width: 43초의 좁은 배경 프레임이 44초 더 넓은 사각 범위로 보인다. 실제 레이어 폭·회전·마스크 중 무엇인지는 미확정. (observed; 내용 supported; 근거 ['f06', 'f07', 'f08'])

### regional-row1: 지역 설명 첫 줄
붉은 가로 화살촉 띠와 흰 한글
식별: reviewed / 지역 설명 첫 줄; 후보 []

- [c021] identity/identity/visible-form: 구간 안에서 관측된 형태: 붉은 가로 화살촉 띠와 흰 한글 (observed; 내용 supported; 근거 ['f14'])
- [c022] text/value/copy: 강원특별자치도 미래산업글로벌도시 조성 (observed; 내용 supported; 근거 ['f07', 'f14'])
- [c023] visibility/order/copy-after-band: 43초 빈 붉은 띠 뒤 43.5초 첫 줄 글자가 읽힌다. 배경 면과 글자 완료를 같은 사건으로 뭉치지 않는다. (observed; 내용 supported; 근거 ['f06', 'f07', 'f08'])
- [c024] color/value/red-to-pink: 첫 줄 띠는 43초 어둡게 보이다 44~44.5초 더 밝은 분홍 강조가 보이고 47초에는 두 번째 줄보다 어둡다. (observed; 내용 supported; 근거 ['f06', 'f08', 'f09', 'f14'])

### regional-row2: 지역 설명 둘째 줄
첫 줄 아래의 분홍 가로 화살촉 띠와 흰 한글
식별: reviewed / 지역 설명 둘째 줄; 후보 []

- [c025] identity/identity/visible-form: 구간 안에서 관측된 형태: 첫 줄 아래의 분홍 가로 화살촉 띠와 흰 한글 (observed; 내용 supported; 근거 ['f14'])
- [c026] text/value/copy: 미래차 전체 주기 기업지원 생태계 구축 (observed; 내용 supported; 근거 ['f14', 'f16'])
- [c027] visibility/order/second-row-enter: 46초에는 첫 줄만 있고 46.5초 둘째 줄의 어두운 띠가 나타나며 47초 문구가 읽힌다. 첫 줄 등장 뒤 두 번째 줄을 추가한다. (observed; 내용 supported; 근거 ['f12', 'f13', 'f14'])
- [c028] color/value/emphasis: 47초와 48초 둘째 줄은 첫 줄보다 밝은 분홍으로 강조돼 있다. 행별 강조의 전체 주기는 이 구간만으로 확정하지 않는다. (observed; 내용 supported; 근거 ['f14', 'f16'])

### regional-link: 지역 기관과 설명 연결선
분홍 세로 화살 모양 선·흰 원형 접점
식별: reviewed / 지역 기관과 설명 연결선; 후보 []

- [c029] identity/identity/visible-form: 구간 안에서 관측된 형태: 분홍 세로 화살 모양 선·흰 원형 접점 (observed; 내용 supported; 근거 ['f06'])
- [c030] visibility/presence/visible: 43초 이후 중앙 기관 카드에서 위 프레임으로 이어지는 분홍 연결선이 보인다. 선 내부 무늬의 이동 방향은 연속 확인하지 않았다. (observed; 내용 supported; 근거 ['f06', 'f14'])
- [c031] relation/relation/agency-panel-link: 분홍 기관 카드와 위 붉은 설명 프레임을 연결한다. 노란 경찰청 설명과 구분되는 소속 묶음이다. (observed; 내용 supported; 근거 ['f06', 'f14'])

### caption: 하단 진행 자막
검은 반투명 가로 면, 회색 문구 중 일부가 흰색으로 밝아짐
식별: reviewed / 하단 진행 자막; 후보 []

- [c032] identity/identity/visible-form: 구간 안에서 관측된 형태: 검은 반투명 가로 면, 회색 문구 중 일부가 흰색으로 밝아짐 (observed; 내용 supported; 근거 ['f00'])
- [c033] text/value/copy-1: 교통사고로부터 안전한 국민의 일상을 만들어가고 있습니다 (observed; 내용 supported; 근거 ['f00'])
- [c034] text/value/copy-2: 강원특별자치도는 5대 첨단산업 클러스터를 조성하여 (observed; 내용 supported; 근거 ['f06'])
- [c035] text/value/copy-3: 전기차, 자율주행차 등 첨단산업의 활성화를 추진하고 있습니다 (observed; 내용 supported; 근거 ['f16'])
- [c036] visibility/order/copy-changes: 41.5~42초 사이 첫 문구에서 두 번째로, 46~46.5초 사이 두 번째에서 세 번째로 교체되는 표본이 보인다. (observed; 내용 supported; 근거 ['f03', 'f04', 'f12', 'f13'])
- [c037] color/direction/progressive-brightening: 42.5초 두 번째 문구의 왼쪽 부분이 더 밝고 뒤는 어두우며 뒤 시점에는 밝은 구간이 늘어난다. 47초 세 번째 문구의 앞부분이 밝고 뒤는 어둡지만 48초 경계에는 더 넓게 밝다. 음성을 듣지 않아 발화와 싱크한다고 판정하지 않는다. (observed; 내용 supported; 근거 ['f05', 'f06', 'f10', 'f14', 'f16'])

## 검토 행과 미해결

- map/identity [40, 48]: reviewed, unchanged; 주장 ['c001']; 미해결 []
- map/size [40, 48]: reviewed, changed; 주장 ['c002']; 미해결 []
- region/identity [40, 48]: reviewed, unchanged; 주장 ['c003']; 미해결 []
- region/text [40, 48]: reviewed, unchanged; 주장 ['c004']; 미해결 []
- region/color [40, 48]: reviewed, unchanged; 주장 ['c005']; 미해결 []
- police/identity [40, 48]: reviewed, unchanged; 주장 ['c006']; 미해결 []
- police/text [40, 48]: reviewed, unchanged; 주장 ['c007']; 미해결 []
- police/visibility [40, 48]: reviewed, unchanged; 주장 ['c008']; 미해결 []
- policy-panel/identity [40, 48]: reviewed, unchanged; 주장 ['c009']; 미해결 []
- policy-panel/text [40, 48]: reviewed, unchanged; 주장 ['c010', 'c011']; 미해결 []
- policy-panel/color [40, 48]: reviewed, unchanged; 주장 ['c012']; 미해결 []
- police-link/identity [40, 48]: reviewed, unchanged; 주장 ['c013']; 미해결 []
- police-link/relation [40, 48]: reviewed, unchanged; 주장 ['c014']; 미해결 []
- gangwon/identity [40, 48]: reviewed, unchanged; 주장 ['c015']; 미해결 []
- gangwon/text [40, 48]: reviewed, unchanged; 주장 ['c016']; 미해결 []
- gangwon/visibility [40, 48]: reviewed, changed; 주장 ['c017']; 미해결 []
- regional-frame/identity [40, 48]: reviewed, unchanged; 주장 ['c018']; 미해결 []
- regional-frame/visibility [40, 48]: reviewed, changed; 주장 ['c019']; 미해결 []
- regional-frame/size [40, 48]: reviewed, changed; 주장 ['c020']; 미해결 []
- regional-row1/identity [40, 48]: reviewed, unchanged; 주장 ['c021']; 미해결 []
- regional-row1/text [40, 48]: reviewed, unchanged; 주장 ['c022']; 미해결 []
- regional-row1/visibility [40, 48]: reviewed, changed; 주장 ['c023']; 미해결 []
- regional-row1/color [40, 48]: reviewed, unchanged; 주장 ['c024']; 미해결 []
- regional-row2/identity [40, 48]: reviewed, unchanged; 주장 ['c025']; 미해결 []
- regional-row2/text [40, 48]: reviewed, unchanged; 주장 ['c026']; 미해결 []
- regional-row2/visibility [40, 48]: reviewed, changed; 주장 ['c027']; 미해결 []
- regional-row2/color [40, 48]: reviewed, unchanged; 주장 ['c028']; 미해결 []
- regional-link/identity [40, 48]: reviewed, unchanged; 주장 ['c029']; 미해결 []
- regional-link/visibility [40, 48]: reviewed, unchanged; 주장 ['c030']; 미해결 []
- regional-link/relation [40, 48]: reviewed, unchanged; 주장 ['c031']; 미해결 []
- caption/identity [40, 48]: reviewed, unchanged; 주장 ['c032']; 미해결 []
- caption/text [40, 48]: reviewed, unchanged; 주장 ['c033', 'c034', 'c035']; 미해결 []
- caption/color [40, 48]: reviewed, changed; 주장 ['c037']; 미해결 []
- caption/visibility [40, 48]: reviewed, changed; 주장 ['c036']; 미해결 []
- [u01] open: 지도·카드 구도의 공통 변환과 개별 요소의 이동을 어떻게 분리할까? / 선택 표본에서 구도 차이는 보이나 같은 기준점의 좌표 추적은 미실행 / 다음 확인: 사용 목적에 필요한 부분의 native ROI·시간 표본을 보강하고, 구현값이 필요하면 원본 프로젝트 확인
- [u02] open: 연결선 내부 화살 무늬가 어느 방향으로 움직이는가? / 무늬와 접점은 보이지만 대표 표본만으로 이동 방향을 확정하지 않음 / 다음 확인: 사용 목적에 필요한 부분의 native ROI·시간 표본을 보강하고, 구현값이 필요하면 원본 프로젝트 확인
- [u03] open: 행별 강조의 정확 주기와 지역 패널 강조와의 동기화는? / 강약은 관측했지만 전체 주기·파형은 측정하지 않음 / 다음 확인: 사용 목적에 필요한 부분의 native ROI·시간 표본을 보강하고, 구현값이 필요하면 원본 프로젝트 확인

## 재사용 패턴


## 내용 검수 범위
- 검수한 고유 주장: 37/37
- 주장 분모 검토 완료: False
- 남은 범위: ['동일 AI의 첫 관측. 독립 정답·전수 주장 채점·미발견 요소 분모 없음.']
- 한계: ['정확한 글꼴·색·좌표·키프레임·이징·주기·제작 의도는 미확정.', '0.5초 간격 표본 사이 사건·가림·미세 변화가 남을 수 있음.', '화면 속 홍보 문구의 기술적·정책적 사실성을 검증한 것이 아님.', '선택 표본을 통한 전체 디자인의 정성 기록이며 모든 속성의 연속 측정은 아님.']


## 근거 파일

- [f00] 40초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01200_040.000.png
- [f01] 81/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01215_040.500.png
- [f02] 41초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01230_041.000.png
- [f03] 83/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01245_041.500.png
- [f04] 42초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01260_042.000.png
- [f05] 85/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01275_042.500.png
- [f06] 43초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01290_043.000.png
- [f07] 87/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01305_043.500.png
- [f08] 44초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01320_044.000.png
- [f09] 89/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01335_044.500.png
- [f10] 45초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01350_045.000.png
- [f11] 91/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01365_045.500.png
- [f12] 46초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01380_046.000.png
- [f13] 93/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01395_046.500.png
- [f14] 47초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01410_047.000.png
- [f15] 95/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01425_047.500.png
- [f16] 48초 / context_after: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\window\f_01440_048.000.png
