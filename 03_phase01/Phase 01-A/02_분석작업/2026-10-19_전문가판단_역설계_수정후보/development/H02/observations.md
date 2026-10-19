# DEV-H02-20261019 분석 기록

판본: 0.1.0-draft.4 / video-observation-0.2
원본: D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\한맥 영상\SW 홈페이지 영상\TOVA\04_(A).mp4
구간: [12, 20]초
방법: 已노출 H02의 기존 전체 개요 시트 2장과 native 12.0/14.4초, 기존 ROI c01/c03/c06 재열람; 기존 기준답안 D01/D08도 읽은 개발 사례. 새 독립 시험 아님.
음성 검수: False

구조 검사와 시각 내용 확인·회사 승인은 별개다.

## 전체 디자인

### layout-settled / [12, 20]
12~20초 변화가 있는 구간의 전체 디자인 목록. 14.4초 native를 정착 대표로 삼고 전후 차이는 대상 주장·모션에 연결한다.
전체 요소: bg, glyph, english, headline, topic-body, orbit, main-ui, previous-ui, yellow-outline, feature-title, feature-body
근거: f00, f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, f26, f27, f28, f29, f30, f31, f32, f33, f34, f35, f36, f37, f38, f39, f40, f41, f42, f43, f44, f45, f46, f47, f48, f49, f50, f51, f52, f53, f54, f55, f56, f57, f58, f59, f60, f61, f62, f63, f64, f65, f66, f67, f68

- hierarchy: 열차 배경·큰 A·연한 영문 위에 흰 주제 제목을 두고, 왼쪽 전경 UI와 노란 기능 표제로 예시를 강조한다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030'])
- alignment: 주제 제목과 설명은 오른쪽에서 왼쪽 정렬, 기능 표제·본문은 왼쪽 지도 UI의 왼쪽 변에 맞춘다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030'])
- spacing: 화면을 좌측 UI와 우측 설명 두 덩어리로 나누고 UI 바로 아래 표제·세 줄 설명을 붙인다. 정확한 간격은 미측정. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030'])
- typography: 굵은 흰 한글 주제 제목, 더 큰 연한 영문 두 줄, 작은 흰 설명, 노란 바탕의 굵은 검정 기능 표제. 정확한 서체·pt는 미상. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030'])
- color: 청회색·검정의 어두운 배경, 흰 주요 문구와 가는 궤적, 노란 표제·테두리·노드, 지도 내부의 다색 노선. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030'])
- background: 열차 사진이 화면을 채우고 대형 A와 영문이 겹친다. 정확한 레이어 불투명도·합성 방식은 미상. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030'])
- shapes: 지도/표 직사각형 UI, 검정과 노란 외곽, 노란 직사각형 표제, 흰 곡선/타원과 원형 노드가 함께 보인다. (observed; qualitative; 주장 ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014', 'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022', 'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030'])

## 전체 흐름과 세부 모션

### flow: 기존 예시 축소 → 새 지도창 이동·확대 → 테두리/표제/설명 → 유지 → 축소 퇴장 / [12, 20]
- [c014] 12초대 좌상단의 지도창이 오른쪽·아래쪽으로 이동해 왼쪽 중앙에 정착한다.
- [c015] 12.4~13.6초 표본에서 같은 지도 UI의 가로·세로 외곽이 커진다.
- [c023] 지도 UI가 정착할 무렵 왼쪽·상단부터 노란 강조 테두리가 추가되어 둘레를 이룬다. 기존 ROI와 개요 표본을 대조한 범위다.
- [c026] 표제는 대중교통 요금 설정기능이다.
- [c029] 대중교통 수단&노선에 따라 / 기본 요금, 거리, 추가거리 및 요금, / 통합환승요금제를 쉽게 적용하도록 설계가 보인다.
- [c018] 17.6초 이후 UI가 오른쪽·아래쪽으로 가며 축소되고 18.8초 표본에는 주요 예시창이 보이지 않는다. 정확한 소실 시점은 미확정.
반복 패턴 참조: []

### detail: 크기 감속·노란 선 전개·내부 표·문구와 노드의 세부 변화 / [12, 20]
- [c016] 진행 중 확대 증가량이 후반에 줄어드는 감속 성격이다. 위치 감속과 별도로 크기에서 본 정성 판단이다.
- [c023] 지도 UI가 정착할 무렵 왼쪽·상단부터 노란 강조 테두리가 추가되어 둘레를 이룬다. 기존 ROI와 개요 표본을 대조한 범위다.
- [c011] 가는 궤적 선과 노드 형태/대상으로 식별한다.
- [c012] 개요 표본에서 선을 따라 원형 노드 위치가 달라진다. 세부 경로 속도는 확정하지 않는다.
- [c025] 대중교통 요금 설정기능 표제 형태/대상으로 식별한다.
- [c026] 표제는 대중교통 요금 설정기능이다.
- [c027] 지도 UI 아래에 표제가 나타나고 17초대에 본문보다 먼저 줄어들며 보이지 않게 된다. 정확한 리빌 방식은 미확정이다.
- [c028] 요금 설정 설명 세 줄 형태/대상으로 식별한다.
- [c029] 대중교통 수단&노선에 따라 / 기본 요금, 거리, 추가거리 및 요금, / 통합환승요금제를 쉽게 적용하도록 설계가 보인다.
- [c030] 표제 뒤에 세 줄 설명이 나타나고 예시창 퇴장 무렵 사라진다. 정확한 줄별 시작과 소실 경계는 추가 검수 대상이다.
반복 패턴 참조: []

## 대상 식별과 고유 주장

### bg: 열차 사진 배경
흰색·청색 열차와 역 플랫폼을 가로로 채운 사진; 화면 전반이 어둡게 조정됨
식별: reviewed / 열차 사진 배경; 후보 []

- [c001] identity/identity: 열차 사진 배경 형태/대상으로 식별한다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c002] color/value: 배경은 청회색·검정의 어두운 톤으로 전경 문구·UI와 구분된다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])

### glyph: 대형 영문 A
화면 왼쪽과 중앙 아래에 이어진 큰 대각 획·가로획·하부 벌어진 획; 숫자 4로 단정하지 않는다
식별: reviewed / 대형 영문 A; 후보 []

- [c003] identity/identity: 대형 영문 A 형태/대상으로 식별한다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c004] position/value: 대형 A가 왼쪽 화면 대부분에 걸치고 UI와 선 뒤의 배경층에 남는다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])

### english: Public Transport 영문
오른쪽 위 두 줄의 큰 반투명 산세리프 영문
식별: reviewed / Public Transport 영문; 후보 []

- [c005] identity/identity: Public Transport 영문 형태/대상으로 식별한다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c006] text/value: Public / Transport 두 줄이 큰 한글 제목 뒤에 겹쳐 있다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])

### headline: 대중교통 분석 제목
오른쪽 중앙의 굵은 흰색 한글
식별: reviewed / 대중교통 분석 제목; 후보 []

- [c007] identity/identity: 대중교통 분석 제목 형태/대상으로 식별한다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c008] text/value: 주제 제목은 대중교통 분석이며 선택한 구간의 뒤쪽까지 유지된다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])

### topic-body: 주제 설명 두 줄
대중교통 분석 제목 바로 아래 작은 흰 문구; 일부 구절 굵기 강조
식별: reviewed / 주제 설명 두 줄; 후보 []

- [c009] identity/identity: 주제 설명 두 줄 형태/대상으로 식별한다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c010] text/value: 현실적으로 이용가능한 모든 대중교통 경로를 탐색하여, / 대중교통 분석 결과의 현실적 설명력을 향상시킵니다.가 제목 아래에 배치된다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])

### orbit: 가는 궤적 선과 노드
흰 곡선/타원 궤적과 검정·노랑 원형 노드
식별: reviewed / 가는 궤적 선과 노드; 후보 []

- [c011] identity/identity: 가는 궤적 선과 노드 형태/대상으로 식별한다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c012] position/direction: 개요 표본에서 선을 따라 원형 노드 위치가 달라진다. 세부 경로 속도는 확정하지 않는다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])

### main-ui: 지도·표 UI 예시
검은 외곽의 지도 UI; 회색 바탕에 다색 노선과 표 창
식별: reviewed / 지도·표 UI 예시; 후보 []

- [c013] identity/identity: 지도·표 UI 예시 형태/대상으로 식별한다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c014] position/direction: 12초대 좌상단의 지도창이 오른쪽·아래쪽으로 이동해 왼쪽 중앙에 정착한다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c015] size/direction: 12.4~13.6초 표본에서 같은 지도 UI의 가로·세로 외곽이 커진다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c016] size/easing: 진행 중 확대 증가량이 후반에 줄어드는 감속 성격이다. 위치 감속과 별도로 크기에서 본 정성 판단이다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c017] internal_state/value: 진입 중 노선 지도 위 왼쪽에 표 형식 설정 창이 드러나며 정착 표본에는 노선 지도와 요금 표 창이 함께 보인다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c018] visibility/direction: 17.6초 이후 UI가 오른쪽·아래쪽으로 가며 축소되고 18.8초 표본에는 주요 예시창이 보이지 않는다. 정확한 소실 시점은 미확정. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])

### previous-ui: 기존 노란 테두리 UI와 작은 예시들
초반 중앙의 노란 테두리 창과 우하단의 작은 예시 창들
식별: reviewed / 기존 노란 테두리 UI와 작은 예시들; 후보 []

- [c019] identity/identity: 기존 노란 테두리 UI와 작은 예시들 형태/대상으로 식별한다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c020] position/direction: 초반 큰 노란 예시창이 우하단으로 이동한다. 겹치는 작은 예시들의 개별 교체·가림 경계는 미확정이다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c021] size/direction: 초반 큰 노란 예시창은 우하단으로 가면서 작아진다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])

### yellow-outline: 지도 UI의 노란 강조 테두리
지도 UI 바깥을 둘러싼 밝은 노란 선
식별: reviewed / 지도 UI의 노란 강조 테두리; 후보 []

- [c022] identity/identity: 지도 UI의 노란 강조 테두리 형태/대상으로 식별한다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c023] shape/order: 지도 UI가 정착할 무렵 왼쪽·상단부터 노란 강조 테두리가 추가되어 둘레를 이룬다. 기존 ROI와 개요 표본을 대조한 범위다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c024] visibility/presence: 정착한 지도 UI의 노란 둘레 강조는 유지 후 예시창 축소·소실과 함께 화면에서 사라진다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])

### feature-title: 대중교통 요금 설정기능 표제
지도 UI 아래 노란 직사각형 바탕의 굵은 검정 글씨
식별: reviewed / 대중교통 요금 설정기능 표제; 후보 []

- [c025] identity/identity: 대중교통 요금 설정기능 표제 형태/대상으로 식별한다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c026] text/value: 표제는 대중교통 요금 설정기능이다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c027] visibility/order: 지도 UI 아래에 표제가 나타나고 17초대에 본문보다 먼저 줄어들며 보이지 않게 된다. 정확한 리빌 방식은 미확정이다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])

### feature-body: 요금 설정 설명 세 줄
노란 표제 아래의 작은 흰색 세 줄 문구
식별: reviewed / 요금 설정 설명 세 줄; 후보 []

- [c028] identity/identity: 요금 설정 설명 세 줄 형태/대상으로 식별한다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c029] text/value: 대중교통 수단&노선에 따라 / 기본 요금, 거리, 추가거리 및 요금, / 통합환승요금제를 쉽게 적용하도록 설계가 보인다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])
- [c030] visibility/order: 표제 뒤에 세 줄 설명이 나타나고 예시창 퇴장 무렵 사라진다. 정확한 줄별 시작과 소실 경계는 추가 검수 대상이다. (observed; 내용 supported; 근거 ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68'])

## 검토 행과 미해결

- bg/identity [12, 20]: reviewed, unchanged; 주장 ['c001']; 미해결 []
- bg/color [12, 20]: reviewed, unchanged; 주장 ['c002']; 미해결 []
- glyph/identity [12, 20]: reviewed, unchanged; 주장 ['c003']; 미해결 []
- glyph/position [12, 20]: reviewed, unchanged; 주장 ['c004']; 미해결 []
- english/identity [12, 20]: reviewed, unchanged; 주장 ['c005']; 미해결 []
- english/text [12, 20]: reviewed, unchanged; 주장 ['c006']; 미해결 []
- headline/identity [12, 20]: reviewed, unchanged; 주장 ['c007']; 미해결 []
- headline/text [12, 20]: reviewed, unchanged; 주장 ['c008']; 미해결 []
- topic-body/identity [12, 20]: reviewed, unchanged; 주장 ['c009']; 미해결 []
- topic-body/text [12, 20]: reviewed, unchanged; 주장 ['c010']; 미해결 []
- orbit/identity [12, 20]: reviewed, unchanged; 주장 ['c011']; 미해결 []
- orbit/position [12, 20]: reviewed, changed; 주장 ['c012']; 미해결 []
- main-ui/identity [12, 20]: reviewed, unchanged; 주장 ['c013']; 미해결 []
- main-ui/position [12, 20]: reviewed, changed; 주장 ['c014']; 미해결 []
- main-ui/size [12, 20]: reviewed, changed; 주장 ['c015', 'c016']; 미해결 []
- main-ui/internal_state [12, 20]: reviewed, changed; 주장 ['c017']; 미해결 []
- main-ui/visibility [12, 20]: reviewed, changed; 주장 ['c018']; 미해결 []
- previous-ui/identity [12, 20]: reviewed, unchanged; 주장 ['c019']; 미해결 []
- previous-ui/position [12, 20]: reviewed, changed; 주장 ['c020']; 미해결 []
- previous-ui/size [12, 20]: reviewed, changed; 주장 ['c021']; 미해결 []
- yellow-outline/identity [12, 20]: reviewed, unchanged; 주장 ['c022']; 미해결 []
- yellow-outline/shape [12, 20]: reviewed, changed; 주장 ['c023']; 미해결 []
- yellow-outline/visibility [12, 20]: reviewed, changed; 주장 ['c024']; 미해결 []
- feature-title/identity [12, 20]: reviewed, unchanged; 주장 ['c025']; 미해결 []
- feature-title/text [12, 20]: reviewed, changed; 주장 ['c026']; 미해결 []
- feature-title/visibility [12, 20]: reviewed, changed; 주장 ['c027']; 미해결 []
- feature-body/identity [12, 20]: reviewed, unchanged; 주장 ['c028']; 미해결 []
- feature-body/text [12, 20]: reviewed, changed; 주장 ['c029']; 미해결 []
- feature-body/visibility [12, 20]: reviewed, changed; 주장 ['c030']; 미해결 []
- [u01] open: 정확한 확대율·속도 곡선·진입/퇴장 경계는 무엇인가? / 현재 개발 재열람의 표본·해상도 또는 검수 범위로 확정하지 않음 / 다음 확인: 해당 원본 ROI와 시간 경계의 기존 표본을 우선 보강·대조
- [u02] open: 겹친 우하단 작은 예시 창 각각의 정체와 가림/교체는 어떻게 다른가? / 현재 개발 재열람의 표본·해상도 또는 검수 범위로 확정하지 않음 / 다음 확인: 해당 원본 ROI와 시간 경계의 기존 표본을 우선 보강·대조
- [u03] open: 노드·궤적의 세부 이동과 배경 자체의 시간 변화는 무엇인가? / 현재 개발 재열람의 표본·해상도 또는 검수 범위로 확정하지 않음 / 다음 확인: 해당 원본 ROI와 시간 경계의 기존 표본을 우선 보강·대조
- [u04] open: 문구별 등장·퇴장 경계와 실제 원본 글꼴·색 값은 무엇인가? / 현재 개발 재열람의 표본·해상도 또는 검수 범위로 확정하지 않음 / 다음 확인: 해당 원본 ROI와 시간 경계의 기존 표본을 우선 보강·대조

## 재사용 패턴


## 내용 검수 범위
- 검수한 고유 주장: 30/30
- 주장 분모 검토 완료: False
- 남은 범위: ['선택한 주장은 기존 원본·표본에 수동 재대조. 디자인 서술 전체의 원자화와 개별 작은 예시 식별은 미완료.', '독립 새 자료 성능·반복 일치·전체 누락률·공수 절감 미검증.']
- 한계: ['이전 결과·기준답안이 알려진 개발 사례. AI 수동 재기록이며 독립 성능 개선 실험 아님.', '선택 개요 표본은 연속 재생·전 프레임 판독이 아님. 정확한 onset/offset·AE 값·오디오는 미검수.', '배경 정밀 움직임과 UI 내부의 모든 셀·버튼 문구, 서체·색의 정확한 값은 미검수.', '전체 디자인을 정성 기록했으나 고유 주장 분모 전수 확정·전체 내용 검수 완료를 주장하지 않음.']

## 다음 판단으로 인계

- purpose: {'text': '대중교통 분석이라는 주제 아래 요금 설정 UI를 기능 예시로 연결한다는 화면 해석', 'basis_kind': 'inferred', 'claim_ids': ['c026', 'c029']}
- information_relation: {'text': '오른쪽은 상위 주제, 왼쪽 UI·노란 표제·작은 본문은 구체 기능 예시라는 해석', 'basis_kind': 'inferred', 'claim_ids': ['c026', 'c029']}
- 원본 사실: ['c014', 'c015', 'c016', 'c023', 'c026', 'c029', 'c018']
- 보존할 특징: ['c023', 'c026', 'c029']
- 열린 쟁점: ['u01', 'u02', 'u03', 'u04']
- 조건 후보: {'condition': '상위 주제를 유지하며 작은 기능 UI와 설명을 함께 제시할 때의 후보', 'reason': '이 사례에서 주제 제목과 UI/기능 표제가 함께 보임', 'claim_ids': ['c026', 'c029'], 'counterexample': None, 'validation_state': 'untested'}
- 구현 제안: {'proposal': 'UI 프리컴프의 위치·크기를 따로 조절하고 테두리 리빌·문구를 별도 제어하는 방식의 새 구현 후보', 'basis_kind': 'inferred', 'claim_ids': ['c014', 'c015', 'c023'], 'verification_needed': '실제 편집·렌더 대조, 다른 문구 길이와 화면비에서 가독성·순서 검증'}

## 근거 파일

- [f00] 12초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_00720_012.000.png
- [f01] 121/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00726_012.100.png
- [f02] 61/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00732_012.200.png
- [f03] 123/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00738_012.300.png
- [f04] 62/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_00744_012.400.png
- [f05] 25/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00750_012.500.png
- [f06] 63/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00756_012.600.png
- [f07] 127/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00762_012.700.png
- [f08] 64/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_00768_012.800.png
- [f09] 129/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00774_012.900.png
- [f10] 13초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00780_013.000.png
- [f11] 131/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00786_013.100.png
- [f12] 66/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_00792_013.200.png
- [f13] 133/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00798_013.300.png
- [f14] 67/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00804_013.400.png
- [f15] 27/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00810_013.500.png
- [f16] 68/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_00816_013.600.png
- [f17] 137/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00822_013.700.png
- [f18] 69/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00828_013.800.png
- [f19] 14초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_00840_014.000.png
- [f20] 71/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00852_014.200.png
- [f21] 72/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_00864_014.400.png
- [f22] 73/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00876_014.600.png
- [f23] 74/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_00888_014.800.png
- [f24] 15초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00900_015.000.png
- [f25] 76/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_00912_015.200.png
- [f26] 77/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00924_015.400.png
- [f27] 78/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_00936_015.600.png
- [f28] 79/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00948_015.800.png
- [f29] 16초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_00960_016.000.png
- [f30] 81/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00972_016.200.png
- [f31] 82/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_00984_016.400.png
- [f32] 83/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_00996_016.600.png
- [f33] 84/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_01008_016.800.png
- [f34] 17초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_01020_017.000.png
- [f35] 171/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_01026_017.100.png
- [f36] 86/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_01032_017.200.png
- [f37] 173/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra1\f_01038_017.300.png
- [f38] 347/20초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01041_017.350.png
- [f39] 87/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01044_017.400.png
- [f40] 349/20초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01047_017.450.png
- [f41] 35/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01050_017.500.png
- [f42] 351/20초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01053_017.550.png
- [f43] 88/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_01056_017.600.png
- [f44] 353/20초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01059_017.650.png
- [f45] 177/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01062_017.700.png
- [f46] 71/4초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01065_017.750.png
- [f47] 89/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01068_017.800.png
- [f48] 357/20초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01071_017.850.png
- [f49] 179/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01074_017.900.png
- [f50] 359/20초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01077_017.950.png
- [f51] 18초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_01080_018.000.png
- [f52] 361/20초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01083_018.050.png
- [f53] 181/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01086_018.100.png
- [f54] 363/20초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01089_018.150.png
- [f55] 91/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01092_018.200.png
- [f56] 73/4초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01095_018.250.png
- [f57] 183/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01098_018.300.png
- [f58] 367/20초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01101_018.350.png
- [f59] 92/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_01104_018.400.png
- [f60] 369/20초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01107_018.450.png
- [f61] 37/2초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01110_018.500.png
- [f62] 371/20초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01113_018.550.png
- [f63] 93/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01116_018.600.png
- [f64] 187/10초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02-r1-with_skill-extra2\f_01122_018.700.png
- [f65] 94/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_01128_018.800.png
- [f66] 96/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_01152_019.200.png
- [f67] 98/5초 / within: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_01176_019.600.png
- [f68] 20초 / context_after: C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase01a-a5b\cases\A5-A\H02\f_01200_020.000.png
