# DEV-KGEO-H04-20261019 분석 기록

판본: 0.1.0-draft.7 / video-observation-0.4
원본: D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\한맥 영상\K-GEO FESTA 1핵심 홍보동영상\K-GEO FESTA_250919_3.mp4
구간: [66, 76]초
방법: 기존 base native 프레임의 전체 개요 시트를 시간순·역순으로 보고 26.2/31.4초 또는 66/72.8초 native를 세부 재대조한 실제 개발 분석. 과거 기준답안 준비 노출 이력 있음. 독립 비교·전 프레임 관찰 아님. 이번 보완은 2026-10-19 동일 AI 문맥의 개발 재검토. 전체 개요와 명시한 native/픽셀 동일 ROI를 재관찰하고, 이미 노출된 지적의 보완을 추적했다. 독립 검수나 새 홀드아웃 아님.
음성 검수: False

구조 검사와 시각 내용 확인·회사 승인은 별개다.

## 전체 디자인

### flight / [66, 73.2]
실사 배경 전체 위에 좌상단 제목, 우상단 경로 인셋, 하단 단계 문구를 겹친다.
전체 요소: header, footage, real-drone, mini-panel, mini-route, mini-marker, caption, mini-halo, red-light
근거: f00

- hierarchy: 실사 드론이 주 대상이며 섹션 제목·경로 인셋·하단 단계 문구가 보조한다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021'])
- alignment: 표제는 좌상단, 경로는 우상단, 단계 문구는 아래 중앙에 배치한다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021'])
- spacing: 실사 중앙을 가리지 않도록 보조 요소를 모서리와 아래에 둔다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021'])
- typography: 흰 한글 섹션 표제와 밝은 바탕 위의 짙은 단계 문구. 정확 서체·크기 미상. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021'])
- color: 청색 리본·흰 경계·노란 경로·보라 핀을 실사의 청회색 하늘·녹색 지면에 겹친다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021'])
- background: 하늘·드론·운동장 실사, 중간에 구도 전환. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021'])
- shapes: 사선 리본, 둥근 세로 인셋, 반투명 하단 바, 경로선·핀과 드론 표시. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021'])

### landing / [73.2, 76]
운동장과 사람이 보이는 실사 위에서 제목·경로 인셋·착륙 문구 배치를 유지한다.
전체 요소: header, footage, real-drone, mini-panel, mini-route, mini-marker, caption, person, mini-halo, red-light
근거: f24

- hierarchy: 실사 드론이 주 대상이며 섹션 제목·경로 인셋·하단 단계 문구가 보조한다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023'])
- alignment: 표제는 좌상단, 경로는 우상단, 단계 문구는 아래 중앙에 배치한다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023'])
- spacing: 실사 중앙을 가리지 않도록 보조 요소를 모서리와 아래에 둔다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023'])
- typography: 흰 한글 섹션 표제와 밝은 바탕 위의 짙은 단계 문구. 정확 서체·크기 미상. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023'])
- color: 청색 리본·흰 경계·노란 경로·보라 핀을 실사의 청회색 하늘·녹색 지면에 겹친다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023'])
- background: 하늘·드론·운동장 실사, 중간에 구도 전환. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023'])
- shapes: 사선 리본, 둥근 세로 인셋, 반투명 하단 바, 경로선·핀과 드론 표시. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023'])

## 전체 흐름과 세부 모션

### flow: 경로 비행 → 표제/문구 교체 → 실사 구도 전환 → 지면 쪽 드론과 착륙 문구 / [66, 76]
- [c004] 67.2초 좌상단에 이전 문구 대신 가느다란 청록 세로 띠가 보인다. 67.6초 좁은 면과 일부 글자가 보이고 68초 새 사선 리본과 드론 비행 시험 종료가 전체 폭으로 보인다. 실제 3D 회전·마스크 방식은 확정하지 않는다.
- [c008] 구간 후반 화면에서 드론이 지면 쪽으로 낮아져 보인다. 화면 이동만으로 세계 좌표의 정확 궤적을 복원하지 않는다.
- [c009] 71.4초와 71.5초 사이 드론의 보이는 크기와 배경 구도가 함께 크게 달라진다. 연속 스케일 애니메이션으로 단정하지 않는다.
- [c010] 선택 표본에서 드론은 계속 보이며 76초 경계에서도 보인다. 바닥 접촉 완료는 확인하지 않는다.
- [c012] 작은 경로 패널이 우상단에 고정된 배치로 유지된다.
- [c013] 인셋의 외곽 크기는 선택 전후 표본에서 대체로 유지된다. 정확 측정은 안 했다.
- [c017] 66.0→66.4→66.8→67.2초 인셋 안 드론 표시는 왼쪽 세로 노란 경로를 따라 위쪽 핀 부근으로 올라간다. 67.2초 이후 선택 표본에서는 그 부근에 머문다. 화면 전체 카메라 이동이나 실사 드론 궤적과 별도이며 정확 속도·정착 경계는 미확정.
- [c021] 67.2초 하단 착륙이 옅게 보이고 67.6초에는 읽히지만 같은 시각 상단 새 표제는 좁은 면·부분 글자 상태다. 68초 상단 표제가 전체 폭으로 보인다. 하단 착륙의 판독 가능 상태가 상단 새 표제 완성보다 먼저다.
- [c023] 후반 지면 구도에서 왼쪽 아래에 사람이 보인다. 정확 첫 등장 시점은 표본 간 범위다.
반복 패턴 참조: []

### detail: 우상단 인셋 내부 이동과 외곽 고정 분리, 문구 교체, 구도 전환에 의한 크기 변화 / [66, 76]
- [c002] 드론 비행 시험 진행 표제.
- [c003] 드론 비행 시험 종료 표제로 바뀐다.
- [c004] 67.2초 좌상단에 이전 문구 대신 가느다란 청록 세로 띠가 보인다. 67.6초 좁은 면과 일부 글자가 보이고 68초 새 사선 리본과 드론 비행 시험 종료가 전체 폭으로 보인다. 실제 3D 회전·마스크 방식은 확정하지 않는다.
- [c006] 하늘 위주 화면에서 지면이 더 드러나며, 71.4초 원거리 드론·운동장 구도에서 71.5초 크게 보이는 드론·하늘 구도로 급히 바뀐다. 기존 71.2~71.6초 범위를 보강한 경계이며 실제 소스 컷 편집 방식은 프로젝트 없이 확정하지 않는다.
- [c008] 구간 후반 화면에서 드론이 지면 쪽으로 낮아져 보인다. 화면 이동만으로 세계 좌표의 정확 궤적을 복원하지 않는다.
- [c009] 71.4초와 71.5초 사이 드론의 보이는 크기와 배경 구도가 함께 크게 달라진다. 연속 스케일 애니메이션으로 단정하지 않는다.
- [c010] 선택 표본에서 드론은 계속 보이며 76초 경계에서도 보인다. 바닥 접촉 완료는 확인하지 않는다.
- [c012] 작은 경로 패널이 우상단에 고정된 배치로 유지된다.
- [c013] 인셋의 외곽 크기는 선택 전후 표본에서 대체로 유지된다. 정확 측정은 안 했다.
- [c015] 다섯 보라 핀과 노란 경로가 내부 이동의 고정 기준으로 보인다.
- [c017] 66.0→66.4→66.8→67.2초 인셋 안 드론 표시는 왼쪽 세로 노란 경로를 따라 위쪽 핀 부근으로 올라간다. 67.2초 이후 선택 표본에서는 그 부근에 머문다. 화면 전체 카메라 이동이나 실사 드론 궤적과 별도이며 정확 속도·정착 경계는 미확정.
- [c019] 하단 문구는 경로 비행이다.
- [c020] 후반 하단 문구는 착륙이다.
- [c021] 67.2초 하단 착륙이 옅게 보이고 67.6초에는 읽히지만 같은 시각 상단 새 표제는 좁은 면·부분 글자 상태다. 68초 상단 표제가 전체 폭으로 보인다. 하단 착륙의 판독 가능 상태가 상단 새 표제 완성보다 먼저다.
- [c023] 후반 지면 구도에서 왼쪽 아래에 사람이 보인다. 정확 첫 등장 시점은 표본 간 범위다.
- [c024] 67.2초의 가느다란 세로 띠에서 67.6초 좁은 면, 68초 전체 폭 리본으로 가로로 보이는 범위가 커진다. 실제 레이어 폭 변경인지 회전·가림인지 미확정.
- [c026] 66.8·67.2·72.8초 인셋 드론 주변에 반투명 흰 원형 영역이 보인다. 드론 이동과 별도 주변 효과로 기록한다.
- [c027] 66.0초와 66.8·67.2·67.6·72.8초를 비교하면 원형 효과의 보이는 면적이 달라진다. 드론이 상단 부근에 머문 뒤에도 넓은 원이 다시 보인다. 정확 반경·주기·파형은 미확정.
- [c028] 원형 영역과 드론 주변 밝은 부분의 강도가 표본마다 달라 보인다. 드론 자체의 흰/보라 명암과 효과의 밝기를 같은 속성으로 확정하지 않는다.
- [c030] 71.5·72.8초 실사 드론 상단에 작은 붉은 광점이 보인다. 앞 원거리 구간에서 안 읽힌다는 이유로 없다고 판정하지 않는다.
- [c031] 71.5·72.8초 광점은 주변의 검은 드론 몸체와 구별되는 붉은색으로 보인다. 발광 원인·깜빡임 주기는 확인하지 않았다.
반복 패턴 참조: []

## 대상 식별과 고유 주장

### header: 좌상단 비행 단계 표제
파란 사선 리본과 흰 문구
식별: reviewed / 좌상단 비행 단계 표제; 후보 []

- [c001] identity/identity/visible-form: 좌상단 비행 단계 표제의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f00'])
- [c002] text/value/section-before: 드론 비행 시험 진행 표제. (observed; 내용 supported; 근거 ['f00'])
- [c003] text/value/section-after: 드론 비행 시험 종료 표제로 바뀐다. (observed; 내용 supported; 근거 ['f17'])
- [c004] visibility/order/replacement: 67.2초 좌상단에 이전 문구 대신 가느다란 청록 세로 띠가 보인다. 67.6초 좁은 면과 일부 글자가 보이고 68초 새 사선 리본과 드론 비행 시험 종료가 전체 폭으로 보인다. 실제 3D 회전·마스크 방식은 확정하지 않는다. (observed; 내용 supported; 근거 ['f03', 'f04', 'f05'])
- [c024] size/direction/transition-width: 67.2초의 가느다란 세로 띠에서 67.6초 좁은 면, 68초 전체 폭 리본으로 가로로 보이는 범위가 커진다. 실제 레이어 폭 변경인지 회전·가림인지 미확정. (observed; 내용 supported; 근거 ['f03', 'f04', 'f05'])

### footage: 하늘·운동장 실사 화면
하늘과 구름, 후반 운동장·수목·건물 배경
식별: reviewed / 하늘·운동장 실사 화면; 후보 []

- [c005] identity/identity/visible-form: 하늘·운동장 실사 화면의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f17'])
- [c006] internal_state/value/shot-change: 하늘 위주 화면에서 지면이 더 드러나며, 71.4초 원거리 드론·운동장 구도에서 71.5초 크게 보이는 드론·하늘 구도로 급히 바뀐다. 기존 71.2~71.6초 범위를 보강한 경계이며 실제 소스 컷 편집 방식은 프로젝트 없이 확정하지 않는다. (observed; 내용 supported; 근거 ['f00', 'f12', 'x035', 'x036', 'f17'])

### real-drone: 실사 드론
하늘의 검은 멀티로터 드론
식별: reviewed / 실사 드론; 후보 []

- [c007] identity/identity/visible-form: 실사 드론의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f17'])
- [c008] position/direction/screen-relative: 구간 후반 화면에서 드론이 지면 쪽으로 낮아져 보인다. 화면 이동만으로 세계 좌표의 정확 궤적을 복원하지 않는다. (observed; 내용 supported; 근거 ['f17', 'f20', 'f24'])
- [c009] size/value/shot-boundary: 71.4초와 71.5초 사이 드론의 보이는 크기와 배경 구도가 함께 크게 달라진다. 연속 스케일 애니메이션으로 단정하지 않는다. (observed; 내용 supported; 근거 ['x035', 'x036', 'f17'])
- [c010] visibility/presence/visible: 선택 표본에서 드론은 계속 보이며 76초 경계에서도 보인다. 바닥 접촉 완료는 확인하지 않는다. (observed; 내용 supported; 근거 ['f00', 'f17', 'f24', 'f25'])

### mini-panel: 우상단 경로 인셋
흰 둥근 테두리의 작은 세로 운동장 지도
식별: reviewed / 우상단 경로 인셋; 후보 []

- [c011] identity/identity/visible-form: 우상단 경로 인셋의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f00'])
- [c012] position/value/anchor: 작은 경로 패널이 우상단에 고정된 배치로 유지된다. (observed; 내용 supported; 근거 ['f00', 'f17', 'f24'])
- [c013] size/value/container-size: 인셋의 외곽 크기는 선택 전후 표본에서 대체로 유지된다. 정확 측정은 안 했다. (observed; 내용 supported; 근거 ['f00', 'f17', 'f24'])

### mini-route: 인셋의 노란 경로와 핀
지도 안 노란 선과 보라 핀
식별: reviewed / 인셋의 노란 경로와 핀; 후보 []

- [c014] identity/identity/visible-form: 인셋의 노란 경로와 핀의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f00'])
- [c015] shape/value/route-shape: 다섯 보라 핀과 노란 경로가 내부 이동의 고정 기준으로 보인다. (observed; 내용 supported; 근거 ['f00', 'f17'])

### mini-marker: 인셋의 드론 표시
노란 경로 위 흰/보라색 작은 드론 그림
식별: reviewed / 인셋의 드론 표시; 후보 []

- [c016] identity/identity/visible-form: 인셋의 드론 표시의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f00'])
- [c017] position/direction/panel-relative: 66.0→66.4→66.8→67.2초 인셋 안 드론 표시는 왼쪽 세로 노란 경로를 따라 위쪽 핀 부근으로 올라간다. 67.2초 이후 선택 표본에서는 그 부근에 머문다. 화면 전체 카메라 이동이나 실사 드론 궤적과 별도이며 정확 속도·정착 경계는 미확정. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f17', 'f24'])

### caption: 하단 비행 단계 문구
흰 반투명 가로 바탕과 짙은 글씨
식별: reviewed / 하단 비행 단계 문구; 후보 []

- [c018] identity/identity/visible-form: 하단 비행 단계 문구의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f00'])
- [c019] text/value/caption-before: 하단 문구는 경로 비행이다. (observed; 내용 supported; 근거 ['f00'])
- [c020] text/value/caption-after: 후반 하단 문구는 착륙이다. (observed; 내용 supported; 근거 ['f17'])
- [c021] visibility/order/replacement: 67.2초 하단 착륙이 옅게 보이고 67.6초에는 읽히지만 같은 시각 상단 새 표제는 좁은 면·부분 글자 상태다. 68초 상단 표제가 전체 폭으로 보인다. 하단 착륙의 판독 가능 상태가 상단 새 표제 완성보다 먼저다. (observed; 내용 supported; 근거 ['f03', 'f04', 'f05'])

### person: 후반 왼쪽 아래의 사람
검은 옷을 입고 장비를 든 사람
식별: reviewed / 후반 왼쪽 아래의 사람; 후보 []

- [c022] identity/identity/visible-form: 후반 왼쪽 아래의 사람의 보이는 형태를 식별한다. (observed; 내용 supported; 근거 ['f24'])
- [c023] visibility/presence/entry: 후반 지면 구도에서 왼쪽 아래에 사람이 보인다. 정확 첫 등장 시점은 표본 간 범위다. (observed; 내용 supported; 근거 ['f18', 'f20', 'f24'])

### mini-halo: 인셋 드론 주변의 원형 빛
인셋 드론 그림을 둘러싼 반투명 흰 원과 밝은 주변 영역
식별: reviewed / 인셋 드론 주변의 원형 빛; 후보 []

- [c025] identity/identity/visible-form: 인셋 드론 그림을 둘러싼 반투명 흰 원과 밝은 주변 영역 (observed; 내용 supported; 근거 ['f03'])
- [c026] visibility/presence/halo-visible: 66.8·67.2·72.8초 인셋 드론 주변에 반투명 흰 원형 영역이 보인다. 드론 이동과 별도 주변 효과로 기록한다. (observed; 내용 supported; 근거 ['f02', 'f03', 'f17'])
- [c027] size/direction/halo-area: 66.0초와 66.8·67.2·67.6·72.8초를 비교하면 원형 효과의 보이는 면적이 달라진다. 드론이 상단 부근에 머문 뒤에도 넓은 원이 다시 보인다. 정확 반경·주기·파형은 미확정. (observed; 내용 supported; 근거 ['f00', 'f02', 'f03', 'f04', 'f17'])
- [c028] color/value/halo-intensity: 원형 영역과 드론 주변 밝은 부분의 강도가 표본마다 달라 보인다. 드론 자체의 흰/보라 명암과 효과의 밝기를 같은 속성으로 확정하지 않는다. (observed; 내용 supported; 근거 ['f02', 'f03', 'f04', 'f17'])

### red-light: 실사 드론 상단 붉은 광점
실사 드론 상단 중앙 부근의 작은 붉은 밝은 점
식별: reviewed / 실사 드론 상단 붉은 광점; 후보 []

- [c029] identity/identity/visible-form: 실사 드론 상단 중앙 부근의 작은 붉은 밝은 점 (observed; 내용 supported; 근거 ['f17'])
- [c030] visibility/presence/visible-sample: 71.5·72.8초 실사 드론 상단에 작은 붉은 광점이 보인다. 앞 원거리 구간에서 안 읽힌다는 이유로 없다고 판정하지 않는다. (observed; 내용 supported; 근거 ['x036', 'f17'])
- [c031] color/value/red-appearance: 71.5·72.8초 광점은 주변의 검은 드론 몸체와 구별되는 붉은색으로 보인다. 발광 원인·깜빡임 주기는 확인하지 않았다. (observed; 내용 supported; 근거 ['x036', 'f17'])

## 검토 행과 미해결

- header/identity [66, 76]: reviewed, unchanged; 주장 ['c001']; 미해결 []
- header/text [66, 76]: reviewed, unchanged; 주장 ['c002', 'c003']; 미해결 []
- header/visibility [66, 76]: reviewed, changed; 주장 ['c004']; 미해결 []
- footage/identity [66, 76]: reviewed, unchanged; 주장 ['c005']; 미해결 []
- footage/internal_state [66, 76]: reviewed, changed; 주장 ['c006']; 미해결 []
- real-drone/identity [66, 76]: reviewed, unchanged; 주장 ['c007']; 미해결 []
- real-drone/position [66, 76]: reviewed, changed; 주장 ['c008']; 미해결 []
- real-drone/size [66, 76]: reviewed, changed; 주장 ['c009']; 미해결 []
- real-drone/visibility [66, 76]: reviewed, changed; 주장 ['c010']; 미해결 []
- mini-panel/identity [66, 76]: reviewed, unchanged; 주장 ['c011']; 미해결 []
- mini-panel/position [66, 76]: reviewed, changed; 주장 ['c012']; 미해결 []
- mini-panel/size [66, 76]: reviewed, changed; 주장 ['c013']; 미해결 []
- mini-route/identity [66, 76]: reviewed, unchanged; 주장 ['c014']; 미해결 []
- mini-route/shape [66, 76]: reviewed, unchanged; 주장 ['c015']; 미해결 []
- mini-marker/identity [66, 76]: reviewed, unchanged; 주장 ['c016']; 미해결 []
- mini-marker/position [66, 76]: reviewed, changed; 주장 ['c017']; 미해결 []
- caption/identity [66, 76]: reviewed, unchanged; 주장 ['c018']; 미해결 []
- caption/text [66, 76]: reviewed, unchanged; 주장 ['c019', 'c020']; 미해결 []
- caption/visibility [66, 76]: reviewed, changed; 주장 ['c021']; 미해결 []
- person/identity [66, 73.2]: not_applicable, not_applicable; 주장 []; 미해결 []
- person/identity [73.2, 76]: reviewed, unchanged; 주장 ['c022']; 미해결 []
- person/visibility [66, 73.2]: not_applicable, not_applicable; 주장 []; 미해결 []
- person/visibility [73.2, 76]: reviewed, changed; 주장 ['c023']; 미해결 []
- header/size [66, 76]: reviewed, changed; 주장 ['c024']; 미해결 []
- mini-halo/identity [66, 76]: reviewed, unchanged; 주장 ['c025']; 미해결 []
- mini-halo/visibility [66, 76]: reviewed, changed; 주장 ['c026']; 미해결 []
- mini-halo/size [66, 76]: reviewed, changed; 주장 ['c027']; 미해결 []
- mini-halo/color [66, 76]: reviewed, changed; 주장 ['c028']; 미해결 []
- red-light/identity [66, 71.5]: unresolved, unknown; 주장 []; 미해결 ['u05']
- red-light/identity [71.5, 76]: reviewed, unchanged; 주장 ['c029']; 미해결 []
- red-light/visibility [66, 71.5]: unresolved, unknown; 주장 []; 미해결 ['u06']
- red-light/visibility [71.5, 76]: reviewed, changed; 주장 ['c030']; 미해결 []
- red-light/color [66, 71.5]: unresolved, unknown; 주장 []; 미해결 ['u07']
- red-light/color [71.5, 76]: reviewed, changed; 주장 ['c031']; 미해결 []
- [u01] open: 인셋 드론의 전체 방문 순서·속도·회전은 무엇인가? / 현재 표본 또는 개발 검수 범위만으로 확정하지 않음 / 다음 확인: 해당 원본 ROI·구간 표본을 먼저 보강하고 같은 대상의 전후를 비교
- [u02] open: 실제 착지 완료 시점·고도·세계 좌표 궤적은 무엇인가? / 현재 표본 또는 개발 검수 범위만으로 확정하지 않음 / 다음 확인: 해당 원본 ROI·구간 표본을 먼저 보강하고 같은 대상의 전후를 비교
- [u03] open: 문구 교체의 정확 경계·리빌 방식과 오디오 대응은 무엇인가? / 현재 표본 또는 개발 검수 범위만으로 확정하지 않음 / 다음 확인: 해당 원본 ROI·구간 표본을 먼저 보강하고 같은 대상의 전후를 비교
- [u04] open: 원형 빛의 정확 반경·밝기·주기와 드론 자세 변화의 관계는 무엇인가? / 주변 효과의 존재와 표본 차이는 관측했으나 곡선·구현은 미측정 / 다음 확인: 결과를 사용하는 목적에 맞춰 해당 ROI의 시간 표본 또는 원본 프로젝트를 확인
- [u05] open: 새 대상의 앞 구간 존재·상태는 무엇인가? / 작게 보이거나 해당 요소가 아직 등장하지 않은 범위를 구분해 재검토해야 함 / 다음 확인: 결과를 사용하는 목적에 맞춰 해당 ROI의 시간 표본 또는 원본 프로젝트를 확인
- [u06] open: 새 대상의 앞 구간 존재·상태는 무엇인가? / 작게 보이거나 해당 요소가 아직 등장하지 않은 범위를 구분해 재검토해야 함 / 다음 확인: 결과를 사용하는 목적에 맞춰 해당 ROI의 시간 표본 또는 원본 프로젝트를 확인
- [u07] open: 새 대상의 앞 구간 존재·상태는 무엇인가? / 작게 보이거나 해당 요소가 아직 등장하지 않은 범위를 구분해 재검토해야 함 / 다음 확인: 결과를 사용하는 목적에 맞춰 해당 ROI의 시간 표본 또는 원본 프로젝트를 확인

## 재사용 패턴


## 내용 검수 범위
- 검수한 고유 주장: 31/31
- 주장 분모 검토 완료: False
- 남은 범위: ['지원 판정은 이 실행의 AI 재대조 상태이며 사람 정답 아님. 미세 모션·정확 수치·고유 주장 전수 분모는 미완료.', '등록 지적의 보완 연결만 확인. 새 자료의 누락률·독립 정밀도·회사 승인 미확인.']
- 한계: ['기존 추출 표본을 실제 열람한 AI 개발 실행. 새 홀드아웃·독립 채점 아님.', '오디오·시나리오 대응·원본 AE 값은 미검수.', '전체 디자인 기술을 원자 주장 분모에 모두 편입하는 전수 검수는 미완료.', '세계 좌표 비행과 화면상 움직임은 다르며 카메라·가림·영상 전환 영향을 분리한다.', '이번 지적 보완은 동일 문맥의 AI 재관찰이며, 미발견 대상·전체 프레임·의미 정확도 전수 검증을 입증하지 않는다.', '원형 빛·강조의 정확 주기·파형·실제 구현은 미확정.', '지원 주장과 같은 구간이라도 선택 표본 사이의 모든 프레임을 확인했다는 뜻은 아니다.']


## 근거 파일

- [f00] 66초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_01980_066.000.png
- [f01] 332/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_01992_066.400.png
- [f02] 334/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02004_066.800.png
- [f03] 336/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02016_067.200.png
- [f04] 338/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02028_067.600.png
- [f05] 68초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02040_068.000.png
- [f06] 342/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02052_068.400.png
- [f07] 344/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02064_068.800.png
- [f08] 346/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02076_069.200.png
- [f09] 348/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02088_069.600.png
- [f10] 70초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02100_070.000.png
- [f11] 352/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02112_070.400.png
- [f12] 354/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02124_070.800.png
- [f13] 356/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02136_071.200.png
- [f14] 358/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02148_071.600.png
- [f15] 72초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02160_072.000.png
- [f16] 362/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02172_072.400.png
- [f17] 364/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02184_072.800.png
- [f18] 366/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02196_073.200.png
- [f19] 368/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02208_073.600.png
- [f20] 74초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02220_074.000.png
- [f21] 372/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02232_074.400.png
- [f22] 374/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02244_074.800.png
- [f23] 376/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02256_075.200.png
- [f24] 378/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02268_075.600.png
- [f25] 76초 / context_after: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\H04\f_02280_076.000.png
- [x026] 67초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02010_067.000.png
- [x027] 671/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02013_067.100.png
- [x028] 673/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02019_067.300.png
- [x029] 337/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02022_067.400.png
- [x030] 135/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02025_067.500.png
- [x031] 677/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02031_067.700.png
- [x032] 339/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02034_067.800.png
- [x033] 679/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02037_067.900.png
- [x034] 713/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02139_071.300.png
- [x035] 357/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02142_071.400.png
- [x036] 143/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02145_071.500.png
- [x037] 361/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02166_072.200.png
- [x038] 73초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02190_073.000.png
- [x039] 371/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02226_074.200.png
- [x040] 75초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02250_075.000.png
- [x041] 379/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-K\REF-H04\f_02274_075.800.png
- [x042] 66초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\evidence\inset-066.000.png
- [x043] 332/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\evidence\inset-066.400.png
- [x044] 334/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\evidence\inset-066.800.png
- [x045] 336/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\evidence\inset-067.200.png
- [x046] 338/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\evidence\inset-067.600.png
- [x047] 364/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\evidence\inset-072.800.png
- [x048] 378/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\analysis-reliability-20261019\evidence\inset-075.600.png
