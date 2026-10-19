# DEV-NEW-P-FIRST-20261019 분석 기록

판본: 0.1.0-draft.8 / video-observation-0.4
원본: D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\한맥 영상\PG 착공식_자율주행영상\250609-1_PG착공식_A-combineAll.mp4
구간: [40, 48]초
방법: 사전에 고정한 새 사내 영상 구간을 0.5초 간격 표본 17장으로 추출. 개요 시트를 시간순·정착 상태 역추적으로 확인하고 선택 native 및 검증된 좌우 분할을 대조했다. 기존 정답/원고는 읽지 않음. 동일 AI 개발 실행, 독립 평가 아님. 끝 경계 프레임은 문맥 근거. 동일 문맥의 후속 정밀 검토에서 0.1초 간격 81개 추가 표본을 만들고, N의 오른쪽 설명 영역 또는 P의 지역 카드·프레임 영역을 전 시간순 ROI 시트로 대조했다. 추가 표본 81장을 모두 전체 화면 native로 읽은 것은 아니다. 후속 대상×속성 재대조에서 요약 행의 change를 주장 facet만으로 정하지 않고 실제 시간 변화·미확정에 맞춰 보완했다. 추가로 전체 개요 5초 표본과 지정 ROI, PG 연결선의 30fps 연속 10프레임을 검토했다. 지도 정합은 실제 native ROI와 별도 수치 진단을 대조했다. 동일 AI 후속 검수이며 정밀 검수 완료 아님.
음성 검수: False

구조 검사와 시각 내용 확인·회사 승인은 별개다.

## 전체 디자인

### map-composite / [40, 48]
어두운 지형·행정 경계 위 왼쪽 노랑 경찰청 설명 묶음과 중앙 위 분홍 지역 설명 묶음. 횡성은 아래 중앙 청록 강조, 바다는 오른쪽 여백. 하단 검은 자막은 두 설명과 별도.
전체 요소: map, region, police, policy-panel, police-link, gangwon, regional-frame, regional-row1, regional-row2, regional-link, caption, gangwon-face
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
- [c041] 40~48초의 0.5초 표본에서 지도 남서·남동의 서로 떨어진 지형 ROI와 기존 경찰청 카드의 같은 특징이 같은 원본 좌표에 유지된다. 40/48초 정합에서도 두 지도 ROI와 카드가 같은 위치에서 일치한다. 이 구간의 지도 줌·기존 묶음 축소 추정 c002는 기각한다. 새 기관 카드·패널의 개별 등장은 별도 동작이며 AE 카메라·부모 리그를 복원한 것이 아니다.
- [c008] 40초 구간 시작부터 왼쪽 기관 카드와 위 설명 패널이 보인다. 이 구간만으로 최초 등장 과정을 기록하지 않는다.
- [c017] 41.3초 선택 ROI에서 로고가 뚜렷하지 않고 41.4초 얇게 드러난 부분, 41.5초 일부 글자, 41.6초 강원 로고 형태가 보인다. 밝은 카드 면은 그 뒤 42.3초 가느다란 세로 범위로 생겨 42.4~42.8초 가로로 넓어진다. 로고 글자와 카드 면을 하나의 동시 등장으로 처리하지 않는다.
- [c019] 43초 위쪽에 좁고 세로로 긴 반투명 면과 빈 붉은 띠가 보이고 43.5~44초 가로 폭과 첫 줄 문구가 갖춰진다.
- [c020] 43초의 좁은 배경 프레임이 44초 더 넓은 사각 범위로 보인다. 실제 레이어 폭·회전·마스크 중 무엇인지는 미확정.
- [c023] 43초 빈 붉은 띠 뒤 43.5초 첫 줄 글자가 읽힌다. 배경 면과 글자 완료를 같은 사건으로 뭉치지 않는다.
- [c027] 46.0초에는 둘째 줄 띠가 뚜렷하지 않고 46.1초 작은 어두운 띠가 생겨 46.2~46.4초 가로로 넓어진다. 46.5초 옅은 글자가 나타나 46.6~47.0초 더 읽히고, 47.2초 이후 밝은 분홍 강조가 강해진다. 띠·글자·강조의 시작을 분리한다.
- [c030] 43초 이후 중앙 기관 카드에서 위 프레임으로 이어지는 분홍 연결선이 보인다. 선 내부 무늬의 이동 방향은 연속 확인하지 않았다.
- [c036] 41.5~42초 사이 첫 문구에서 두 번째로, 46~46.5초 사이 두 번째에서 세 번째로 교체되는 표본이 보인다.
- [c043] 연결선 ROI의 43.8~45.3초 선택 표본과 44.000~44.300초의 연속 10프레임에서 위를 향하는 화살 무늬의 위치는 같아 보이고 주로 밝기 차이가 보인다. 위를 향하는 모양을 위로 이동하는 애니메이션으로 쓰지 않는다. 검사하지 않은 시간의 흐름·초기 성장·주기는 이 결론에 포함하지 않는다.
반복 패턴 참조: []

### detail: 기관별 프레임·글자·연결선 분리, 첫째·둘째 줄 순서와 강조 강약, 자막 내용과 밝기 진행 구분 / [40, 48]
- [c041] 40~48초의 0.5초 표본에서 지도 남서·남동의 서로 떨어진 지형 ROI와 기존 경찰청 카드의 같은 특징이 같은 원본 좌표에 유지된다. 40/48초 정합에서도 두 지도 ROI와 카드가 같은 위치에서 일치한다. 이 구간의 지도 줌·기존 묶음 축소 추정 c002는 기각한다. 새 기관 카드·패널의 개별 등장은 별도 동작이며 AE 카메라·부모 리그를 복원한 것이 아니다.
- [c004] 횡성
- [c005] 어두운 지도 안에서 횡성 영역을 청록색 채움과 밝은 외곽으로 강조한다. 이 색은 정책·기관 설명의 노랑/분홍과 별도다.
- [c007] 경찰청
- [c008] 40초 구간 시작부터 왼쪽 기관 카드와 위 설명 패널이 보인다. 이 구간만으로 최초 등장 과정을 기록하지 않는다.
- [c010] 자율주행자동차 운행 안전관리를 위한 도로교통법 개정 추진
- [c011] 완전 자율주행시대에 대비한 도로교통안전 추진 전략 수립
- [c012] 노랑·연두 띠의 밝기와 테두리 강도가 선택 시점에서 달라 보인다. 정확 반복 주기·행별 동기화는 미확정.
- [c014] 경찰청 카드 위쪽에서 노란 연결선이 설명 패널 아래 접점으로 이어져 카드와 위 두 문구의 소속 관계를 시각적으로 묶는다.
- [c016] 강원특별자치도
- [c017] 41.3초 선택 ROI에서 로고가 뚜렷하지 않고 41.4초 얇게 드러난 부분, 41.5초 일부 글자, 41.6초 강원 로고 형태가 보인다. 밝은 카드 면은 그 뒤 42.3초 가느다란 세로 범위로 생겨 42.4~42.8초 가로로 넓어진다. 로고 글자와 카드 면을 하나의 동시 등장으로 처리하지 않는다.
- [c019] 43초 위쪽에 좁고 세로로 긴 반투명 면과 빈 붉은 띠가 보이고 43.5~44초 가로 폭과 첫 줄 문구가 갖춰진다.
- [c020] 43초의 좁은 배경 프레임이 44초 더 넓은 사각 범위로 보인다. 실제 레이어 폭·회전·마스크 중 무엇인지는 미확정.
- [c022] 강원특별자치도 미래산업글로벌도시 조성
- [c023] 43초 빈 붉은 띠 뒤 43.5초 첫 줄 글자가 읽힌다. 배경 면과 글자 완료를 같은 사건으로 뭉치지 않는다.
- [c024] 첫 줄 띠는 43초 어둡게 보이다 44~44.5초 더 밝은 분홍 강조가 보이고 47초에는 두 번째 줄보다 어둡다.
- [c026] 미래차 전체 주기 기업지원 생태계 구축
- [c027] 46.0초에는 둘째 줄 띠가 뚜렷하지 않고 46.1초 작은 어두운 띠가 생겨 46.2~46.4초 가로로 넓어진다. 46.5초 옅은 글자가 나타나 46.6~47.0초 더 읽히고, 47.2초 이후 밝은 분홍 강조가 강해진다. 띠·글자·강조의 시작을 분리한다.
- [c028] 47초와 48초 둘째 줄은 첫 줄보다 밝은 분홍으로 강조돼 있다. 행별 강조의 전체 주기는 이 구간만으로 확정하지 않는다.
- [c030] 43초 이후 중앙 기관 카드에서 위 프레임으로 이어지는 분홍 연결선이 보인다. 선 내부 무늬의 이동 방향은 연속 확인하지 않았다.
- [c031] 분홍 기관 카드와 위 붉은 설명 프레임을 연결한다. 노란 경찰청 설명과 구분되는 소속 묶음이다.
- [c033] 교통사고로부터 안전한 국민의 일상을 만들어가고 있습니다
- [c034] 강원특별자치도는 5대 첨단산업 클러스터를 조성하여
- [c035] 전기차, 자율주행차 등 첨단산업의 활성화를 추진하고 있습니다
- [c036] 41.5~42초 사이 첫 문구에서 두 번째로, 46~46.5초 사이 두 번째에서 세 번째로 교체되는 표본이 보인다.
- [c037] 42.5초 두 번째 문구의 왼쪽 부분이 더 밝고 뒤는 어두우며 뒤 시점에는 밝은 구간이 늘어난다. 47초 세 번째 문구의 앞부분이 밝고 뒤는 어둡지만 48초 경계에는 더 넓게 밝다. 음성을 듣지 않아 발화와 싱크한다고 판정하지 않는다.
- [c039] 41.6초 로고는 보이지만 밝은 직사각 면은 없고, 42.3초 뒤에 좁은 세로 면이 생겨 42.5초 이후 카드 바탕으로 보인다.
- [c040] 42.3초 좁은 세로 면에서 42.4~42.8초 넓은 가로 카드 면으로 변한다. 실제 스케일·마스크·회전 구현은 미확정.
- [c043] 연결선 ROI의 43.8~45.3초 선택 표본과 44.000~44.300초의 연속 10프레임에서 위를 향하는 화살 무늬의 위치는 같아 보이고 주로 밝기 차이가 보인다. 위를 향하는 모양을 위로 이동하는 애니메이션으로 쓰지 않는다. 검사하지 않은 시간의 흐름·초기 성장·주기는 이 결론에 포함하지 않는다.
반복 패턴 참조: []

## 대상 식별과 고유 주장

### map: 지역 지도 배경
어두운 위성 지형, 경계선과 회색 지명, 오른쪽 바다
식별: reviewed / 지역 지도 배경; 후보 []

- [c001] identity/identity/visible-form: 구간 안에서 관측된 형태: 어두운 위성 지형, 경계선과 회색 지명, 오른쪽 바다 (observed; 내용 supported; 근거 ['f00'])
- [c002] size/direction/global-framing: 40초와 48초 사이 지도와 기존 기관·설명 묶음의 보이는 크기·배치가 소폭 달라져 전체 구도가 넓어지는 듯하다. 정확 공통 카메라·부모 스케일 변환은 미확정이며 모든 카드가 고정이라고 단정하지 않는다. (observed; 내용 rejected; 근거 ['f00', 'f06', 'f16'])
- [c041] size/value/stable-map-anchors: 40~48초의 0.5초 표본에서 지도 남서·남동의 서로 떨어진 지형 ROI와 기존 경찰청 카드의 같은 특징이 같은 원본 좌표에 유지된다. 40/48초 정합에서도 두 지도 ROI와 카드가 같은 위치에서 일치한다. 이 구간의 지도 줌·기존 묶음 축소 추정 c002는 기각한다. 새 기관 카드·패널의 개별 등장은 별도 동작이며 AE 카메라·부모 리그를 복원한 것이 아니다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16'])
- [c042] size/value/native-roi-difference: 같은 native 좌표 ROI를 40초와 나머지 16개 표본에서 비교한 최대 평균 RGB 절대차는 지도 남서 0.10819/남동 0.05304(0~255 단위), 경찰청 카드 0.35044다. 40/48초의 1/4회색조 NCC는 두 지도 ROI 약1, 카드 0.99999이며 일치 위치는 동일하다. 4px 정합 해상도와 압축 차이를 포함한다. 가려진 북쪽 ROI(NCC .315)와 강조가 바뀐 정책 패널(.374)은 채택하지 않는다. 세 점 affine 잔차가 0에 가깝다는 사실은 독립 검증 근거로 사용하지 않는다. (calculated; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16'])

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
- [c017] visibility/order/logo-assembly: 41.3초 선택 ROI에서 로고가 뚜렷하지 않고 41.4초 얇게 드러난 부분, 41.5초 일부 글자, 41.6초 강원 로고 형태가 보인다. 밝은 카드 면은 그 뒤 42.3초 가느다란 세로 범위로 생겨 42.4~42.8초 가로로 넓어진다. 로고 글자와 카드 면을 하나의 동시 등장으로 처리하지 않는다. (observed; 내용 supported; 근거 ['x030', 'x031', 'x032', 'x033', 'x040', 'x041', 'x045'])

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
- [c027] visibility/order/second-row-enter: 46.0초에는 둘째 줄 띠가 뚜렷하지 않고 46.1초 작은 어두운 띠가 생겨 46.2~46.4초 가로로 넓어진다. 46.5초 옅은 글자가 나타나 46.6~47.0초 더 읽히고, 47.2초 이후 밝은 분홍 강조가 강해진다. 띠·글자·강조의 시작을 분리한다. (observed; 내용 supported; 근거 ['x077', 'x078', 'x080', 'x082', 'x085', 'x087', 'x089'])
- [c028] color/value/emphasis: 47초와 48초 둘째 줄은 첫 줄보다 밝은 분홍으로 강조돼 있다. 행별 강조의 전체 주기는 이 구간만으로 확정하지 않는다. (observed; 내용 supported; 근거 ['f14', 'f16'])

### regional-link: 지역 기관과 설명 연결선
분홍 세로 화살 모양 선·흰 원형 접점
식별: reviewed / 지역 기관과 설명 연결선; 후보 []

- [c029] identity/identity/visible-form: 구간 안에서 관측된 형태: 분홍 세로 화살 모양 선·흰 원형 접점 (observed; 내용 supported; 근거 ['f06'])
- [c030] visibility/presence/visible: 43초 이후 중앙 기관 카드에서 위 프레임으로 이어지는 분홍 연결선이 보인다. 선 내부 무늬의 이동 방향은 연속 확인하지 않았다. (observed; 내용 supported; 근거 ['f06', 'f14'])
- [c031] relation/relation/agency-panel-link: 분홍 기관 카드와 위 붉은 설명 프레임을 연결한다. 노란 경찰청 설명과 구분되는 소속 묶음이다. (observed; 내용 supported; 근거 ['f06', 'f14'])
- [c043] position/value/stationary-upward-glyph: 연결선 ROI의 43.8~45.3초 선택 표본과 44.000~44.300초의 연속 10프레임에서 위를 향하는 화살 무늬의 위치는 같아 보이고 주로 밝기 차이가 보인다. 위를 향하는 모양을 위로 이동하는 애니메이션으로 쓰지 않는다. 검사하지 않은 시간의 흐름·초기 성장·주기는 이 결론에 포함하지 않는다. (observed; 내용 supported; 근거 ['p098', 'p099', 'p100', 'p101', 'p102', 'p103', 'p104', 'p105', 'p106', 'p107', 'p108', 'p109', 'p110', 'p111', 'p112', 'p113', 'p114', 'p115', 'p116', 'p117', 'p118', 'p119'])

### caption: 하단 진행 자막
검은 반투명 가로 면, 회색 문구 중 일부가 흰색으로 밝아짐
식별: reviewed / 하단 진행 자막; 후보 []

- [c032] identity/identity/visible-form: 구간 안에서 관측된 형태: 검은 반투명 가로 면, 회색 문구 중 일부가 흰색으로 밝아짐 (observed; 내용 supported; 근거 ['f00'])
- [c033] text/value/copy-1: 교통사고로부터 안전한 국민의 일상을 만들어가고 있습니다 (observed; 내용 supported; 근거 ['f00'])
- [c034] text/value/copy-2: 강원특별자치도는 5대 첨단산업 클러스터를 조성하여 (observed; 내용 supported; 근거 ['f06'])
- [c035] text/value/copy-3: 전기차, 자율주행차 등 첨단산업의 활성화를 추진하고 있습니다 (observed; 내용 supported; 근거 ['f16'])
- [c036] visibility/order/copy-changes: 41.5~42초 사이 첫 문구에서 두 번째로, 46~46.5초 사이 두 번째에서 세 번째로 교체되는 표본이 보인다. (observed; 내용 supported; 근거 ['f03', 'f04', 'f12', 'f13'])
- [c037] color/direction/progressive-brightening: 42.5초 두 번째 문구의 왼쪽 부분이 더 밝고 뒤는 어두우며 뒤 시점에는 밝은 구간이 늘어난다. 47초 세 번째 문구의 앞부분이 밝고 뒤는 어둡지만 48초 경계에는 더 넓게 밝다. 음성을 듣지 않아 발화와 싱크한다고 판정하지 않는다. (observed; 내용 supported; 근거 ['f05', 'f06', 'f10', 'f14', 'f16'])

### gangwon-face: 강원 카드의 밝은 배경 면
로고 뒤에 나중에 펼쳐지는 흰색·연분홍 직사각 면과 가는 모서리 선
식별: reviewed / 강원 카드의 밝은 배경 면; 후보 []

- [c038] identity/identity/visible-form: 42.5초 로고 뒤의 밝은 직사각 면과 모서리 선을 구분한다. (observed; 내용 supported; 근거 ['x042'])
- [c039] visibility/order/face-after-logo: 41.6초 로고는 보이지만 밝은 직사각 면은 없고, 42.3초 뒤에 좁은 세로 면이 생겨 42.5초 이후 카드 바탕으로 보인다. (observed; 내용 supported; 근거 ['x033', 'x039', 'x040', 'x042'])
- [c040] size/direction/face-width: 42.3초 좁은 세로 면에서 42.4~42.8초 넓은 가로 카드 면으로 변한다. 실제 스케일·마스크·회전 구현은 미확정. (observed; 내용 supported; 근거 ['x040', 'x041', 'x042', 'x043', 'x045'])

## 검토 행과 미해결

- map/identity [40, 48]: reviewed, unchanged; 주장 ['c001']; 미해결 []
- map/size [40, 48]: reviewed, unchanged; 주장 ['c002', 'c041', 'c042']; 미해결 []
- region/identity [40, 48]: reviewed, unchanged; 주장 ['c003']; 미해결 []
- region/text [40, 48]: reviewed, unchanged; 주장 ['c004']; 미해결 []
- region/color [40, 48]: reviewed, unchanged; 주장 ['c005']; 미해결 []
- police/identity [40, 48]: reviewed, unchanged; 주장 ['c006']; 미해결 []
- police/text [40, 48]: reviewed, unchanged; 주장 ['c007']; 미해결 []
- police/visibility [40, 48]: reviewed, unchanged; 주장 ['c008']; 미해결 []
- policy-panel/identity [40, 48]: reviewed, unchanged; 주장 ['c009']; 미해결 []
- policy-panel/text [40, 48]: reviewed, unchanged; 주장 ['c010', 'c011']; 미해결 []
- policy-panel/color [40, 48]: reviewed, changed; 주장 ['c012']; 미해결 []
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
- regional-row1/color [40, 48]: reviewed, changed; 주장 ['c024']; 미해결 []
- regional-row2/identity [40, 48]: reviewed, unchanged; 주장 ['c025']; 미해결 []
- regional-row2/text [40, 48]: reviewed, unchanged; 주장 ['c026']; 미해결 []
- regional-row2/visibility [40, 48]: reviewed, changed; 주장 ['c027']; 미해결 []
- regional-row2/color [40, 48]: reviewed, changed; 주장 ['c028']; 미해결 []
- regional-link/identity [40, 48]: reviewed, unchanged; 주장 ['c029']; 미해결 []
- regional-link/visibility [40, 48]: reviewed, changed; 주장 ['c030']; 미해결 []
- regional-link/relation [40, 48]: reviewed, unchanged; 주장 ['c031']; 미해결 []
- caption/identity [40, 48]: reviewed, unchanged; 주장 ['c032']; 미해결 []
- caption/text [40, 48]: reviewed, changed; 주장 ['c033', 'c034', 'c035']; 미해결 []
- caption/color [40, 48]: reviewed, changed; 주장 ['c037']; 미해결 []
- caption/visibility [40, 48]: reviewed, changed; 주장 ['c036']; 미해결 []
- regional-link/internal_state [40, 48]: unresolved, unknown; 주장 []; 미해결 ['u02']
- gangwon-face/identity [40, 48]: reviewed, unchanged; 주장 ['c038']; 미해결 []
- gangwon-face/visibility [40, 48]: reviewed, changed; 주장 ['c039']; 미해결 []
- gangwon-face/size [40, 48]: reviewed, changed; 주장 ['c040']; 미해결 []
- regional-link/position [43.8, 45.3]: reviewed, unchanged; 주장 ['c043']; 미해결 []
- regional-link/position [40, 43.8]: not_reviewed, unknown; 주장 []; 미해결 ['u02']
- regional-link/position [45.3, 48]: not_reviewed, unknown; 주장 []; 미해결 ['u02']
- [u01] resolved: 지도·카드 구도의 공통 변환과 개별 요소의 이동을 어떻게 분리할까? / 기존 지도/카드의 서로 떨어진 고정 특징을 확인해 전체 줌 추정을 기각. 새 카드·패널 등장과 분리. 실제 리그·렌더 사이 숨은 움직임은 검증하지 않음. / 다음 확인: 
- [u02] open: 연결선 내부 화살 무늬가 어느 방향으로 움직이는가? / 선택 ROI와 연속 10프레임의 정착 구간에서는 위쪽 화살 모양이 같은 위치에 보임. 초기 생성/다른 시간대의 이동 여부는 아직 남음. / 다음 확인: 연결선 처음 생성~정착과 이후 퇴장까지 같은 무늬 특징을 연속 비교. 방향 형태와 실제 이동을 분리
- [u03] open: 행별 강조의 정확 주기와 지역 패널 강조와의 동기화는? / 강약은 관측했지만 전체 주기·파형은 측정하지 않음 / 다음 확인: 사용 목적에 필요한 부분의 native ROI·시간 표본을 보강하고, 구현값이 필요하면 원본 프로젝트 확인

## 재사용 패턴


## 내용 검수 범위
- 검수한 고유 주장: 43/43
- 주장 분모 검토 완료: False
- 남은 범위: ['동일 AI의 후속 검수. 원본 전체 정밀 분석·독립 정답·모든 미발견 요소의 분모는 미확인.', '열린 쟁점 u02, u03']
- 한계: ['정확한 글꼴·색·좌표·키프레임·이징·주기·제작 의도는 미확정.', '0.5초 간격 표본 사이 사건·가림·미세 변화가 남을 수 있음.', '화면 속 홍보 문구의 기술적·정책적 사실성을 검증한 것이 아님.', '선택 표본을 통한 전체 디자인의 정성 기록이며 모든 속성의 연속 측정은 아님.', '전체 원본 영상에서 확인한 구간은 8초. 원본 전체 분석 완료 아님.', '0.1초 보강은 지정 ROI의 상세 확인. 다른 대상·전체 프레임의 완전성을 보장하지 않음.']


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
- [x017] 40초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01200_040.000.png
- [x018] 401/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01203_040.100.png
- [x019] 201/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01206_040.200.png
- [x020] 403/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01209_040.300.png
- [x021] 202/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01212_040.400.png
- [x022] 81/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01215_040.500.png
- [x023] 203/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01218_040.600.png
- [x024] 407/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01221_040.700.png
- [x025] 204/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01224_040.800.png
- [x026] 409/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01227_040.900.png
- [x027] 41초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01230_041.000.png
- [x028] 411/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01233_041.100.png
- [x029] 206/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01236_041.200.png
- [x030] 413/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01239_041.300.png
- [x031] 207/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01242_041.400.png
- [x032] 83/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01245_041.500.png
- [x033] 208/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01248_041.600.png
- [x034] 417/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01251_041.700.png
- [x035] 209/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01254_041.800.png
- [x036] 419/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01257_041.900.png
- [x037] 42초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01260_042.000.png
- [x038] 421/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01263_042.100.png
- [x039] 211/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01266_042.200.png
- [x040] 423/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01269_042.300.png
- [x041] 212/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01272_042.400.png
- [x042] 85/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01275_042.500.png
- [x043] 213/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail1\f_01278_042.600.png
- [x044] 427/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01281_042.700.png
- [x045] 214/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01284_042.800.png
- [x046] 429/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01287_042.900.png
- [x047] 43초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01290_043.000.png
- [x048] 431/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01293_043.100.png
- [x049] 216/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01296_043.200.png
- [x050] 433/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01299_043.300.png
- [x051] 217/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01302_043.400.png
- [x052] 87/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01305_043.500.png
- [x053] 218/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01308_043.600.png
- [x054] 437/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01311_043.700.png
- [x055] 219/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01314_043.800.png
- [x056] 439/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01317_043.900.png
- [x057] 44초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01320_044.000.png
- [x058] 441/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01323_044.100.png
- [x059] 221/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01326_044.200.png
- [x060] 443/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01329_044.300.png
- [x061] 222/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01332_044.400.png
- [x062] 89/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01335_044.500.png
- [x063] 223/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01338_044.600.png
- [x064] 447/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01341_044.700.png
- [x065] 224/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01344_044.800.png
- [x066] 449/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01347_044.900.png
- [x067] 45초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01350_045.000.png
- [x068] 451/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01353_045.100.png
- [x069] 226/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01356_045.200.png
- [x070] 453/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail2\f_01359_045.300.png
- [x071] 227/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01362_045.400.png
- [x072] 91/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01365_045.500.png
- [x073] 228/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01368_045.600.png
- [x074] 457/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01371_045.700.png
- [x075] 229/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01374_045.800.png
- [x076] 459/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01377_045.900.png
- [x077] 46초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01380_046.000.png
- [x078] 461/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01383_046.100.png
- [x079] 231/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01386_046.200.png
- [x080] 463/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01389_046.300.png
- [x081] 232/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01392_046.400.png
- [x082] 93/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01395_046.500.png
- [x083] 233/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01398_046.600.png
- [x084] 467/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01401_046.700.png
- [x085] 234/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01404_046.800.png
- [x086] 469/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01407_046.900.png
- [x087] 47초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01410_047.000.png
- [x088] 471/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01413_047.100.png
- [x089] 236/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01416_047.200.png
- [x090] 473/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01419_047.300.png
- [x091] 237/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01422_047.400.png
- [x092] 95/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01425_047.500.png
- [x093] 238/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01428_047.600.png
- [x094] 477/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01431_047.700.png
- [x095] 239/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01434_047.800.png
- [x096] 479/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01437_047.900.png
- [x097] 48초 / context_after: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\fresh\cases\NEW-P\detail3\f_01440_048.000.png
- [p098] 44초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\line-frame-0.png
- [p099] 1321/30초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\line-frame-1.png
- [p100] 661/15초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\line-frame-2.png
- [p101] 441/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\line-frame-3.png
- [p102] 662/15초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\line-frame-4.png
- [p103] 265/6초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\line-frame-5.png
- [p104] 221/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\line-frame-6.png
- [p105] 1327/30초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\line-frame-7.png
- [p106] 664/15초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\line-frame-8.png
- [p107] 443/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\line-frame-9.png
- [p108] 219/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\P-connector-43.8.png
- [p109] 439/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\P-connector-43.9.png
- [p110] 44초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\P-connector-44.0.png
- [p111] 441/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\P-connector-44.1.png
- [p112] 221/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\P-connector-44.2.png
- [p113] 443/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\P-connector-44.3.png
- [p114] 222/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\P-connector-44.4.png
- [p115] 89/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\P-connector-44.5.png
- [p116] 45초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\P-connector-45.0.png
- [p117] 451/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\P-connector-45.1.png
- [p118] 226/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\P-connector-45.2.png
- [p119] 453/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\internal-video-audit-20261019\probes\P-connector-45.3.png
