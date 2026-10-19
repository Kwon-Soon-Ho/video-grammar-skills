# 기존6개 모션 창: 계약·프로젝트 지원 지식 연결

상태: draft.12로 수행한 기존기록 재검토 초안. 로컬 후보·조건부 지식이며 정본 등록/회사 승인 아님.

## 사례 요약

| 사례 | 정보 관계·전체 구도·디자인 언어 | 흐름·중요 미상 |
|---|---|---|
| VC-CASE-A / A-02 | 수주 구성 도넛둘→비용→중복 제외 실제 매출을 구별. 넓은 수주/좁은 비용/오른쪽 매출판 누적. 녹색 배지·민트/흰 정보판·도시 배경, 주황 매출·입체 경제 도상 | A-M1→A-M2→A-M3.12.9억원 뒤 도상 후속.112초는 prior-only, 곡선/음성 미상 |
| VC-CASE-B / B-02~05 | 요청↔지원 양판→23.7억원·26건→대각 업무영상→BIM 설계 주행+보조3카드·82% 도넛. 구리색 배지·아이보리/갈색 정보판·금속적 수치·지도/도로 | B-M1→B-M2→B-M3.퇴장/진입 중첩·82% 뒤 카드/도넛/막대 후속. 구현/읽기 충분성 미상 |

읽는 순서: 사례 요약 → 아래 전체 상세 → 근거. 기존 전체 디자인/상세는 [계약 원문](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/01_계약_수집기록.md>) 및 [지원 원문](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/02_프로젝트지원_수집기록.md>)에 원문 그대로 보존했다.

## 전체 흐름·조합

### LOCAL-FLOW-A-REVIEW-v1

사례/구역 VC-CASE-A/A-02. 이 흐름은 A-M1 → A-M2 → A-M3을 포함한다. 수주 구성→비용→실제 매출 누적. 미관측 간극 100~103, 106~108초는 보간하지 않는다. 전체 흐름 로컬 연결 ID이며 원본 전편 관측이나 기존 VC-FLOW-01의 대체가 아니다.

### LOCAL-FLOW-B-REVIEW-v1

사례/구역 VC-CASE-B/B-02→B-03→B-04→B-05. 이 흐름은 B-M1 → B-M2 → B-M3을 포함한다. 요청↔지원→총량→업무 영상→핵심 차트. 미관측 간극 140~143, 146~147초는 보간하지 않는다. 전체 흐름 로컬 연결 ID이며 원본 전편 관측이나 기존 VC-FLOW-01의 대체가 아니다.

전체 레이아웃은 원문의 A-02/B-02~05를 연결한다. 새 LAYOUT 정본 ID를 만들지 않았다. 독립6동작은 기존 ID를 유지하고, 하위 도상 단계마다 새 번호를 만들지 않았다.

## 전체 상세: 정의·현재 사용처

<a id="a-m1"></a>
### A-M1 — 수주 재배치와 비용 정보판 누적

- 정의/판본: 기존 A-M1 로컬 후보. 원문 SHA256 08c97ec66a4e4efe3d7e7f0bc5c5195aee1f4a3d753cfc1c8b174c1457950003, §4/A-M1. 명시 버전 없는 정의를 해시로 고정.
- 사례/구역/내용: VC-CASE-A / A-02 / 수주 총량/구성 다음에 계약 수행 투입비용을 구별해 설명
- 역할·분리 이유: CARD 후보; VC-MOTION-02 변형 검토. 기존 구역을 남기며 공간·새 내부 정보가 단계별 변화
- 전체 상세: [01_계약_수집기록.md](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/01_계약_수집기록.md>)
- 범위: 96~100초, 기존0.5초 표본/제공시트 재대조. 연속 관측 아님.

| 표본 초 | 상태 |
|---|---|
| 96 | 수주 정보판 중심 |
| 96.5 | 수주 판 왼쪽 재배치 중 |
| 97 | 비용 판 외형·제목 |
| 97.5 | 동전 일부 |
| 98 | 문서 포함 도상 |
| 99 | 현재까지 투입 캡슐 |
| 100 | 비용 숫자 가시; 모음에서는0.7억원으로 읽히며 최종8.7과 구별 |

| 대상 사건 | 관계 | 상대 사건 | 근거 |
|---|---|---|---|
| 수주 판 재배치 | overlaps | 비용 판 추가 | 96.5~97.5 표본; 두 시작 미상 |
| 비용 도상 | precedes | 캡슐 및 숫자 | 98→99→100 표본 |

- 관측 속성: PROPERTY-POSITION, PROPERTY-VISIBILITY, PROPERTY-VALUE; 시간 관계: TIME-SEQUENCE, TIME-OVERLAP.
- 기능 분류(추론): FUNCTION-REVEAL, FUNCTION-CONTEXT. 이유: 기존 구역을 남기며 공간·새 내부 정보가 단계별 변화. 원제작 의도 확인 아님.
- 검토 관련 원칙: MR-04, MR-07, AP-09. 원칙/효과 통과 선언 아님. 정본·심화 정확ID/판본/출처 위치는 [knowledge-pins.json](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/knowledge-pins.json>) 참조.
- 조건/제외: 관련 지표 누적 설명; 과밀하거나 기간/집계가 바뀌면 그대로 유지하지 않음
- 현재 차이: A-M2와 달리 기존 수주 판 위치도 변함. 동일 패턴 확정 아님
- 미검증: 100초는 최종 비용 정착 아님; 정확 AE 키프레임·원본 곡선·마스크/parent/3D 구현 미상; 음성·시나리오·연속 원본 미검수; 표본 사이 정확 시작/완료와 이후 퇴장 미관측; 가감속 분류 보류(변화율 측정 없음).
- 현재 시트: [contract-reflow.jpg](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/motion/evidence/contract-reflow.jpg>); 정확 시각·원본 프레임 경로·제공 SHA는 [05_근거와_실행기록.md](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/05_근거와_실행기록.md>)의 contract-reflow절 및 [evidence-manifest.json](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/evidence-manifest.json>) 참조.

<a id="a-m2"></a>
### A-M2 — 수주·비용을 유지하며 매출 판 진입

- 정의/판본: 기존 A-M2 로컬 후보. 원문 SHA256 08c97ec66a4e4efe3d7e7f0bc5c5195aee1f4a3d753cfc1c8b174c1457950003, §4/A-M2. 명시 버전 없는 정의를 해시로 고정.
- 사례/구역/내용: VC-CASE-A / A-02 / 수주17.5억원·비용8.7억원을 남기고 중복 제외 실제 매출 구역 추가
- 역할·분리 이유: CARD 후보; VC-MOTION-02의 다른 변형 검토. 기존 비교 구역 유지와 새 구역 진입 구별
- 전체 상세: [01_계약_수집기록.md](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/01_계약_수집기록.md>)
- 범위: 103~106초, 기존0.5초 표본/제공시트 재대조. 연속 관측 아님.

| 표본 초 | 상태 |
|---|---|
| 103.5 | 매출 판 미가시; 수주·비용 가시 |
| 104 | 오른쪽 매출 판 가시 |
| 104.5 | 더 안쪽 위치 |
| 105 | 실제 발생 매출 제목 |
| 106 | 중복 제외 설명 |

판 첫 가시성 (103.5,104]초는 표본 간 경계이며 정확 시작/길이가 아니다.

| 대상 사건 | 관계 | 상대 사건 | 근거 |
|---|---|---|---|
| 수주·비용 | accompanies | 매출 판 진입 | 103.5~106 표본 |
| 판 진입 | precedes | 제목·설명 | 104→105→106 |

- 관측 속성: PROPERTY-POSITION, PROPERTY-VISIBILITY; 시간 관계: TIME-SEQUENCE, TIME-HOLD.
- 기능 분류(추론): FUNCTION-REVEAL, FUNCTION-CONTEXT. 이유: 기존 비교 구역 유지와 새 구역 진입 구별. 원제작 의도 확인 아님.
- 검토 관련 원칙: MR-04, MR-07, AP-09. 원칙/효과 통과 선언 아님. 정본·심화 정확ID/판본/출처 위치는 [knowledge-pins.json](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/knowledge-pins.json>) 참조.
- 조건/제외: 비교 맥락을 남기는 추가 정보; 기간이 바뀌면 과거 값 유지 금지
- 현재 차이: A-M1처럼 모든 판을 다시 정렬한다고 확정하지 않음
- 미검증: 기존 판 미세 이동 미측정; 정확 AE 키프레임·원본 곡선·마스크/parent/3D 구현 미상; 음성·시나리오·연속 원본 미검수; 표본 사이 정확 시작/완료와 이후 퇴장 미관측; 가감속 분류 보류(변화율 측정 없음).
- 현재 시트: [contract-panel.jpg](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/motion/evidence/contract-panel.jpg>); 정확 시각·원본 프레임 경로·제공 SHA는 [05_근거와_실행기록.md](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/05_근거와_실행기록.md>)의 contract-panel절 및 [evidence-manifest.json](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/evidence-manifest.json>) 참조.

<a id="a-m3"></a>
### A-M3 — 매출 숫자 정착 후 상승 도상 후속

- 정의/판본: 기존 A-M3 로컬 후보. 원문 SHA256 08c97ec66a4e4efe3d7e7f0bc5c5195aee1f4a3d753cfc1c8b174c1457950003, §4/A-M3. 명시 버전 없는 정의를 해시로 고정.
- 사례/구역/내용: VC-CASE-A / A-02 / 중복 제외 실제 발생 매출12.9억원을 주황 금액·입체 막대·상승 화살표로 제시
- 역할·분리 이유: DETAIL 후보; 수치 증가와 도상 단계 조립. 같은 성과에 속하나 끝값 표시와 도상 완성 시각 분리
- 전체 상세: [01_계약_수집기록.md](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/01_계약_수집기록.md>)
- 범위: 108~111초, 기존0.5초 표본/제공시트 재대조. 연속 관측 아님.

| 표본 초 | 상태 |
|---|---|
| 108 | 받침 |
| 109 | 낮은 막대 |
| 109.5 | 0.8억원 |
| 110 | 10.8억원 |
| 110.5 | 12.9억원 |
| 111 | 12.9억원 유지; 도상 후속 비교 대상 |
| 112 | 기존 기록의 상승 화살표 완성 후속. 이번 sheet 바깥/직접 재열람 아님 |

금액 끝값 가시경계 (110,110.5]초는 표본 간 경계이며 정확 시작/길이가 아니다.

| 대상 사건 | 관계 | 상대 사건 | 근거 |
|---|---|---|---|
| 12.9 끝값 가시 | numeric-before-graphic | 상승 도상 후속 완성 | 110.5/111 sheet + 기존112초 기록; 최종 화살표 직접검수 보류 |
| 12.9억원 | holds | 111/112 표본 | 110.5/111 sheet;112 prior-only |
| 금액 증가 | overlaps | 막대 성장 | 109.5~110.5 |

- 관측 속성: PROPERTY-VALUE, PROPERTY-SIZE, PROPERTY-VISIBILITY; 시간 관계: TIME-SEQUENCE, TIME-OVERLAP, TIME-DELAY, TIME-HOLD.
- 기능 분류(추론): FUNCTION-REVEAL, FUNCTION-FOCUS. 이유: 같은 성과에 속하나 끝값 표시와 도상 완성 시각 분리. 원제작 의도 확인 아님.
- 검토 관련 원칙: AP-05, MP-07, AP-08, AP-09, MR-07, MR-08, IP-05. 원칙/효과 통과 선언 아님. 정본·심화 정확ID/판본/출처 위치는 [knowledge-pins.json](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/knowledge-pins.json>) 참조.
- 조건/제외: 확정 성과 금액 후보; 식별번호·날짜 카운트 제외
- 현재 차이: B-M3는 구성 비중/도넛/보조카드; A-M3는 금액/경제 도상. 동일 자산·곡선 아님
- 미검증: 112초 화살표는 제공 기존 기록만 유지; 이번 직접 검수 불가; 110.5 이후 모든 프레임 유지/정확 도상 완성 시각 미상; 정확 AE 키프레임·원본 곡선·마스크/parent/3D 구현 미상; 음성·시나리오·연속 원본 미검수; 표본 사이 정확 시작/완료와 이후 퇴장 미관측; 가감속 분류 보류(변화율 측정 없음).
- 현재 시트: [contract-number.jpg](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/motion/evidence/contract-number.jpg>); 정확 시각·원본 프레임 경로·제공 SHA는 [05_근거와_실행기록.md](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/05_근거와_실행기록.md>)의 contract-number절 및 [evidence-manifest.json](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/evidence-manifest.json>) 참조.

<a id="b-m1"></a>
### B-M1 — 관계도 분산 퇴장과 총액 중첩

- 정의/판본: 기존 B-M1 로컬 후보. 원문 SHA256 ce5da90fd1093198f9905933b2ba00d405b27eeee6c6bb08bf6b947839cee633, §4/B-M1. 명시 버전 없는 정의를 해시로 고정.
- 사례/구역/내용: VC-CASE-B / B-02→B-03 / 가족사 요청↔전문인력 지원에서 지원 총량23.7억원·26건 요약으로 전환
- 역할·분리 이유: TRANSITION 후보. 관계도에서 총량 요약; 완전 직렬 교체 아님
- 전체 상세: [02_프로젝트지원_수집기록.md](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/02_프로젝트지원_수집기록.md>)
- 범위: 136~140초, 기존0.5초 표본/제공시트 재대조. 연속 관측 아님.

| 표본 초 | 상태 |
|---|---|
| 136 | 두 판·반대 방향 화살표 |
| 137 | 두 판·화살표 가시 |
| 137.5 | 화살표/일부 요소 약화 |
| 138 | 옛 판 좌우 바깥 상태와 새 건수·금액 함께 가시 |
| 138.5 | 제목+새 수치 구도 |
| 140 | 23.7억원·26건 |

| 대상 사건 | 관계 | 상대 사건 | 근거 |
|---|---|---|---|
| 관계도 퇴장·약화 | overlaps | 새 총량 등장 | 138초 함께 가시 |

- 관측 속성: PROPERTY-POSITION, PROPERTY-VISIBILITY, PROPERTY-VALUE; 시간 관계: TIME-SEQUENCE, TIME-OVERLAP.
- 기능 분류(추론): FUNCTION-CHANGE, FUNCTION-FOCUS. 이유: 관계도에서 총량 요약; 완전 직렬 교체 아님. 원제작 의도 확인 아님.
- 검토 관련 원칙: MR-04, MR-07, AP-05, AP-09. 원칙/효과 통과 선언 아님. 정본·심화 정확ID/판본/출처 위치는 [knowledge-pins.json](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/knowledge-pins.json>) 참조.
- 조건/제외: 관계 맥락→요약; 양자 관계를 계속 읽어야 하면 퇴장 재검토
- 현재 차이: B-M2 대각 전개와 다르게 양판 외곽 이동/약화와 새 수치 중첩
- 미검증: 실제 opacity 속성 미상; 정확 AE 키프레임·원본 곡선·마스크/parent/3D 구현 미상; 음성·시나리오·연속 원본 미검수; 표본 사이 정확 시작/완료와 이후 퇴장 미관측; 가감속 분류 보류(변화율 측정 없음).
- 현재 시트: [project-reflow.jpg](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/motion/evidence/project-reflow.jpg>); 정확 시각·원본 프레임 경로·제공 SHA는 [05_근거와_실행기록.md](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/05_근거와_실행기록.md>)의 project-reflow절 및 [evidence-manifest.json](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/evidence-manifest.json>) 참조.

<a id="b-m2"></a>
### B-M2 — 총액에서 대각 분할 업무 영상 전개

- 정의/판본: 기존 B-M2 로컬 후보. 원문 SHA256 ce5da90fd1093198f9905933b2ba00d405b27eeee6c6bb08bf6b947839cee633, §4/B-M2. 명시 버전 없는 정의를 해시로 고정.
- 사례/구역/내용: VC-CASE-B / B-03→B-04 / 총량23.7억원·26건 뒤 지도/도로 업무 사례 영상 구획으로 전환
- 역할·분리 이유: TRANSITION 후보. 대각 경계·복수 구획이 전개. 내부 도로 시점/차량 변화와 외곽 경계 구별
- 전체 상세: [02_프로젝트지원_수집기록.md](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/02_프로젝트지원_수집기록.md>)
- 범위: 143~146초, 기존0.5초 표본/제공시트 재대조. 연속 관측 아님.

| 표본 초 | 상태 |
|---|---|
| 143.5 | 총액 화면 |
| 144 | 왼쪽 지도·도로 대각 경계; 옛 총량 오른쪽 가시 |
| 144.5 | 업무 영상 중심 중간 구성 |
| 145 | 여러 도로 영상 분할 |
| 145.5 | 여러 영상·하단 라벨 |
| 146 | 세 구획·하단 라벨 |

첫 영상층 가시경계 (143.5,144]초는 표본 간 경계이며 정확 시작/길이가 아니다.

| 대상 사건 | 관계 | 상대 사건 | 근거 |
|---|---|---|---|
| 첫 영상층 공개 | overlaps | 옛 총량 잔존 | 144초 |
| 첫 영상층 | precedes | 복수 구획·라벨 | 144→145.5/146 |

- 관측 속성: PROPERTY-POSITION, PROPERTY-VISIBILITY; 시간 관계: TIME-SEQUENCE, TIME-OVERLAP.
- 기능 분류(추론): FUNCTION-CHANGE, FUNCTION-REVEAL. 이유: 대각 경계·복수 구획이 전개. 내부 도로 시점/차량 변화와 외곽 경계 구별. 원제작 의도 확인 아님.
- 검토 관련 원칙: MR-04, MR-07, AP-09. 원칙/효과 통과 선언 아님. 정본·심화 정확ID/판본/출처 위치는 [knowledge-pins.json](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/knowledge-pins.json>) 참조.
- 조건/제외: 복수 업무 소개; 다른 시기·범위 자료의 비교가능성 별도 확인
- 현재 차이: 정지화면 한 장 일괄 교체가 아니며 도로 내부 움직임 포함
- 미검증: 실제 마스크/트랙매트 미상; 내부 영상 연속 카메라 궤적 미관측; 정확 AE 키프레임·원본 곡선·마스크/parent/3D 구현 미상; 음성·시나리오·연속 원본 미검수; 표본 사이 정확 시작/완료와 이후 퇴장 미관측; 가감속 분류 보류(변화율 측정 없음).
- 현재 시트: [project-wipe.jpg](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/motion/evidence/project-wipe.jpg>); 정확 시각·원본 프레임 경로·제공 SHA는 [05_근거와_실행기록.md](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/05_근거와_실행기록.md>)의 project-wipe절 및 [evidence-manifest.json](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/evidence-manifest.json>) 참조.

<a id="b-m3"></a>
### B-M3 — 비중 숫자 이후 카드·도넛·막대 후속

- 정의/판본: 기존 B-M3 로컬 후보. 원문 SHA256 ce5da90fd1093198f9905933b2ba00d405b27eeee6c6bb08bf6b947839cee633, §4/B-M3. 명시 버전 없는 정의를 해시로 고정.
- 사례/구역/내용: VC-CASE-B / B-04→B-05 / 프로젝트 지원 주요 활동: BIM 설계19.4억원·3건·약82% 주행 + BIM 지원/해외사업 지원/디자인 지원 보조3카드
- 역할·분리 이유: CARD+DETAIL 복합 후보; 기존 B-M3 유지. 주비중/보조3개 위계·배경 재구성, 숫자 이후 시각 요소 진행
- 전체 상세: [02_프로젝트지원_수집기록.md](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/02_프로젝트지원_수집기록.md>)
- 범위: 147~150초, 기존0.5초 표본/제공시트 재대조. 연속 관측 아님.

| 표본 초 | 상태 |
|---|---|
| 147.5 | 영상3구획 |
| 148 | 오른쪽 정보판·불완전 제목·약44% |
| 148.5 | 약64%·첫 보조카드 |
| 149 | 약82%·추가 항목; 디자인 지원 카드 작게 가시 |
| 149.5 | 3카드 더 채움·디자인 지원 겉보기 크기 증가·도넛 다른 분할색 보강 |
| 150 | 대표구성; BIM 행·작은 카드 막대 후속 채움 비교 |

비중 끝값 가시경계 (148.5,149]초는 표본 간 경계이며 정확 시작/길이가 아니다.

| 대상 사건 | 관계 | 상대 사건 | 근거 |
|---|---|---|---|
| 82% 끝값 가시 | numeric-before-graphic | 카드/도넛 분할색/막대 후속 | 149→149.5→150 sheet |
| 82% | holds | 149.5/150 표본 | 149/149.5/150 |
| 오른쪽 판 등장 | overlaps | 다중영상→지도띠+주도로 재구성 | 148~149.5 |

- 관측 속성: PROPERTY-VALUE, PROPERTY-SIZE, PROPERTY-VISIBILITY; 시간 관계: TIME-SEQUENCE, TIME-OVERLAP, TIME-DELAY, TIME-HOLD.
- 기능 분류(추론): FUNCTION-REVEAL, FUNCTION-FOCUS, FUNCTION-CHANGE. 이유: 주비중/보조3개 위계·배경 재구성, 숫자 이후 시각 요소 진행. 원제작 의도 확인 아님.
- 검토 관련 원칙: AP-05, MP-07, AP-08, AP-09, MR-04, MR-07, MR-08, IP-05. 원칙/효과 통과 선언 아님. 정본·심화 정확ID/판본/출처 위치는 [knowledge-pins.json](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/knowledge-pins.json>) 참조.
- 조건/제외: 우세 항목·나머지 구성 설명; 우세가 없으면 같은 강조 부적합
- 현재 차이: A-M3 금액/경제도상과 달리 비중/구성 도넛/업무 카드. VC-MOTION-03 교체 제안과 구별
- 미검증: 모든 도상의 정확 완성시각·동기화 미확인; 막대 실제 분모/스케일·AE Scale·도넛 제작법 미상; 정확 AE 키프레임·원본 곡선·마스크/parent/3D 구현 미상; 음성·시나리오·연속 원본 미검수; 표본 사이 정확 시작/완료와 이후 퇴장 미관측; 가감속 분류 보류(변화율 측정 없음).
- 현재 시트: [project-panel.jpg](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/motion/evidence/project-panel.jpg>); 정확 시각·원본 프레임 경로·제공 SHA는 [05_근거와_실행기록.md](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/preserved-input/05_근거와_실행기록.md>)의 project-panel절 및 [evidence-manifest.json](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/evidence-manifest.json>) 참조.

## 지식의 종류와 출처

- R2 공통용어0.1.1: motion_property/timing은 관측 분류, motion_function은 기능 추론이다. 격자/정보관계/표현언어/품질 질문을 같은 분류로 섞지 않는다.
- R3 원칙파일0.1.2/선택 개별원칙0.1.1·심화카드0.1.2: AP-05/MP-07는 후속/겹침 질문이지만 관성을 확정하지 않는다. MR-04 단계/비교, MR-07 연동과 인과/parent 분리, MR-08 표시값과 실측 분리. AP-08 주목 경쟁 질문, AP-09/IP-05 읽기/음성대응은 보류.
- knowledge-pins.json은 정본경로/파일버전/SHA, terms/principles/cards의 정확ID, 심화 source_refs/source_locator/source_read_depth를 보존한다. MP-07은 원자료 독서가 public_course_outline 수준인 지식임을 유지. 이번 외부 원전 재열람은 없음.
- R1 자산 동일성·R5 CI 토큰·R6 사람 승인·R4v0.2 이관은 이번 수행 아님. 원칙은 미디어 근거가 아니며 로컬 JSON은 R4 인증이 아니다.

## 실제 검토·보류

검토자: 이번 실행 AI. 제공 기존기록/6모음만 검토했으며 사람의 실제 검수·회사 승인 없음. Q정본0.1.1 중 이 과제 쟁점만 선정, 전26항목 필수화 아님.

| ID·대상 | 기준 | 판정·이유 | 근거·제한 | 다음 확인 |
|---|---|---|---|---|
| RV-01/A-M3,B-M3 | Q-INFO-04 | 통과(분석 기록의 표시 중간값/끝값 분리만): 0.8/10.8/44/64를 시간별 표시값으로 보존; 실제 실적 시계열로 쓰지 않음 | contract-number109.5/110/110.5; project-panel148/148.5/149; 실측/연출 의도와 최종 데이터 출처 사실 검증은 판단보류 | 데이터 담당자에게 원자료/집계 판본 확인 |
| RV-02/A-M3,B-M3 | Q-MOTION-01 | 판단보류: 숫자 이후 도상 진행은 기록했으나 읽기 유지·발화·시청조건 근거 없음 | 110.5/111 +112 prior-only; 149/149.5/150; 창 길이를 읽기시간으로 쓰지 않음 | 별도 재검수에서 완성→퇴장·발화/시청조건을 디자인 검수자·대상 시청자와 확인 |
| RV-03/B-M1,B-M2,B-M3 | Q-MOTION-02 | 통과(기록의 중첩·대상 구분만): 138 옛판+새값,144 옛총량+영상층,148~149.5 배경/정보판을 따로 보존 | project-reflow138; project-wipe144; project-panel148~150; 실제 업무 인과·parenting·시청효과 판정 아님 | 기술 관계 적합성은 내용/모션 담당자 별도 확인 |
| RV-04/A-M1,A-M2,A-M3,B-M1,B-M2,B-M3 | Q-TRUST-01 | 통과(제공자료 참조 왕복만); 원본 시간/해시 검증 판단보류: 6모음 직접 열람/원문 해시표 연결; 원본 해시는 제공값 | evidence-manifest.json; preserved-input/05_근거와_실행기록.md; 112 prior-only; MP4/PTS/개별 원본 프레임 직접검수 아님 | 별도 검수에서112초·추출 로그·시간 매핑·원본 해시 확인 |
| RV-05/A-M3,B-M3 | Q-TRUST-02 | 통과(확대 주장 제한만): 정확 키프레임/마스크·회사규칙/시청효과 미상 유지 | collection.md; knowledge-pins.json; 제작법/의도 자체는 판단보류 | 필요 시 원본 프로젝트·제작자·회사규칙 담당자의 근거 확인 |
| RV-06/A-M1,A-M2,A-M3,B-M1,B-M2,B-M3 | IP-05 / Q-MOTION-01 | 미검수(음성 동기), 완료 판정 없음: MP4/오디오/시나리오 없음 | 공통 input.md; 비적용/통과로 바꾸지 않음 | 음성 검수 요청·실제 음성/시나리오 제공 시 대응 확인 |

## 근거·경계

- 제공 원본 메타데이터: 가치창출성과 영상_260923_v3.mp4 / SHA256 be78fc4f2f94c6b3cbd31339a1a1ccc84b91613d56c0e485d5dd1296839f56fa /434.4초/7680×2160/30fps. MP4 실제 절대경로는 입력에 없으며 해시 재계산 안 함.
- 제공 JPG6개를 직접 열람했다. 각2160×705는 원본 전체 비율 유지 축소+시각라벨/빈타일이며 도구 표시는2048×668로 리사이즈됨. 원본크기 ROI·모든 프레임 검수 아님. 시각은 기존 표본/추출기록 재사용; PTS/time_base 독립검증 없음.
- 6창은96~100,103~106,108~111,136~140,143~146,147~150초.112초는 창밖 prior-only. 창 끝을 모션 끝/영상 최종상태로 바꾸지 않는다.
- 보존 원문의 프레임 경로·SHA를 evidence-manifest.json에 연결했다. 원본 프레임 해시는 제공값이며 이번 재계산하지 않았다. 원본 크롭 좌표/원본 변환 로그 미확인; 이 기록은 픽셀 정밀 측정 없음.
- 기존기록 재사용/모음 대조/기능추론만 수행. 새 원본 연속재생/재추출·음성확인·화면/영상/PDF·정본/스킬 수정·등록 없음.
- VC-MOTION-03 가족사별→유형별은 과거 새 시안 제안으로 관측 검색에서 제외. 현재 관측 부재를 전편 부재로 확대하지 않음. VC-MOTION-01 의미/끝값 일치는 동시완료가 아니며 VC-MOTION-02와 A-M1/A-M2 동일성은 후보.

## 조회

query.py: 정확ID/개념/원칙/명시 관계 및 단순문자열 필터. 의미검색/추천 성능 검증 아님. 반환은 정의/사용처/내용/시각/근거/차이/미검증/검토를 포함한다. 실제 명령/결과는 query-results.md 및 query-results.json 참조.
