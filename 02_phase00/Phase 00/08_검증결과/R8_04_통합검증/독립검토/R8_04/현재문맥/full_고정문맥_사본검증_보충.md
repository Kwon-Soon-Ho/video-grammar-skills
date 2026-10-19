# R8-4 full 고정문맥 사본 실제 확인

2026-10-15 후속 확인. 앞선 `현재문맥_독립감사.md`의 읽기 전용 조사와 구분하여, 이번에는 허용된 C 작업영역에 고정조회 전용 사본을 생성했다. D의 원문·후보·고정 목록은 읽기만 했다. 이전 보고서의 ‘사본 생성 미실시’는 이전 시점의 사실이며 이 보충 확인으로 해소한다.

복사 위치는 `C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_04_시험\고정문맥_검증전용\Phase00`다. 확정한 800파일, 총 78,901,855 bytes만 상대 위치 그대로 복사했다. 각 원본 바이트를 복사 직전 고정 SHA/크기와 대조하고, C 사본과 복사 후 D를 다시 대조했다. 검사4개 실행이 끝난 뒤에도 모든 D/C 파일을 다시 고정값과 대조했다. 전부 일치했고 C 추가/누락 파일은 0이다. 기존 C 파일을 다른 바이트로 덮어쓰지 않도록 배타적 생성(`xb`)과 긴 경로 확장 IO를 썼다.

지정 D Python의 `-B -X utf8`로 **C 사본 안의 검사기**를 **C 사본 --base**로 실제 실행했다.

| 검사 | 종료코드 | 결과 |
|---|---:|---|
| C/R6_출처사용검사.py | 0 | structural_valid=true, artifact_rows_checked=544 |
| C/R6_사람검수.py | 0 | structural_valid=true, 현재 선언 답변 1개 |
| C/R6_통합조회.py | 0 | valid=true |
| C/R7_연결확인.py | 0 | valid=true, 130 pin/26항목/22필드 |

두 manifest의 D/C SHA도 각각 같았다. R6 `257971f59f01c3e834acb4b25ee789e78872dfc7ce29960801551f3052f46a57`, R7 `99cfb91c11ef43d57f5ffc1eb5dc35f67bc4e889e75f9dd515aee3222ceda855`다. R7 목록을 재생성하거나 후보로 바꾸지 않았다. 원래 호스트 절대경로 4개는 이 환경에서 부재하므로, 기존 R6 규칙대로 C 사본의 보존 snapshot을 사용한다.

증거 파일은 다음과 같다.

- `full_copy_structure_receipt.json`: 실행 시점·루트·800개 대조·manifest SHA·4개 결과·한계.
- `full_copy_read_api_commands.json`: 실제 args/stdout/stderr/종료코드, D/C 검사기 SHA.
- `full_copy_file_checks.json`: 원본 직전·복사·원본 직후 SHA/크기 800행.
- `copy_validate_context.py`: 복사/검사 실행 스크립트. 지정 Python으로 실제 실행한 최종 종료코드 0.

이는 **변경 없는 고정문맥 사본에 대한 구조·연결 조회**다. 역할별 행동 수행자가 이 전체 루트를 읽었다는 뜻이 아니다. 이 루트는 평가계획·과거 스킬·개발 결과도 포함하므로 역할별 수행 입력으로 제공하지 않는다. 행동시험과 연결하려면 고정문맥 조회 영수증과 역할별 입력 변환/실행 영수증을 명시적으로 별도 연결해야 한다. 실제 스킬 행동·내용·영상·사람 승인·전환을 통과시킨 것은 아니다. SHA 시작/끝 대조는 원자 스냅샷이나 OS 접근 격리를 증명하지 않는다.

## R8 별도 후보 문맥의 필수필드 제안

다음은 간략 계약 제안이며 새 검사기 구현/스키마 통과 결과가 아니다.

| 필수필드 | 필요한 내용과 제약 |
|---|---|
| `id`, `version`, `scope` | 기존 R7과 다른 ID/판본. scope는 candidate context 또는 bounded handoff. 후보 존재를 운영 전환으로 해석하지 않음 |
| `fixed_context_receipt` | 위 full receipt 경로·SHA, 고정목록 ID/판본/SHA, C 사본 루트, 검사기 SHA·실행 args/exit·결과/시점·한계. 구조 조회와 행동시험을 구분 |
| `candidate_pins` | 큐레이터/기록관리자/적용성검토자 세 이름을 정확히 한 번씩. 각 후보의 본문·모든 참조·보조도구 상대경로·SHA·판본. old/new 실행에는 선택한 한 버전만 전달 |
| `role_input_transformations` | 역할/사례/구성, 원본 path/SHA/pointer·변환 이유·제거/대체·수행본 path/SHA, 공통 동등성 검사, 평가자료 제외/간접 복제 검사 결과, 고정조회 영수증 연결. 과거 R6/R7 pin을 재고정하지 않음 |
| `handoff` | 송신/수신 역할, 대상 ID/판본/SHA, 실제 생성 출력 path/SHA·요청 범위·근거/깊이·검사영수증, 적용/보류/미해결 항목·구체 다음 역할. 예상 답안/채점표 전달 금지 |
| `human_reply_scopes` | 실제 요청/회신 원문 pin, 대상·판본·확인한 범위·유효/미결 범위. 기존 CI 최신성 회신이나 구성 유지 피드백을 새 내용/회사 승인으로 확대하지 않음. 없으면 빈 배열과 미수집 사유 |
| `transition` | 현행 기본 경로·후보 경로, 현재 상태(예: candidate_only), 검증 범위·미완료, 기본 전환 여부·결정 근거 pin. 후보 생성/조회 성공만으로 adopted=true 금지 |
| `limitations`, `claims` | 무영상/합성/지시상 격리/미수집 등 한계. `content_verified`, `company_approved`, `permission_granted`, `operational_release`는 실제 별도 근거 없으면 false |

가능한 기본 검증은 경로 경계·중복 ID/후보·SHA/판본·누락/변환 동등성·출력인계 대상 일치·역할 권한·회신 범위의 구조 대조다. 이런 구조검사가 실제 근거의 의미를 지지하는지, 미사용 사례에서 스킬이 적절히 행동했는지와 사람 판단을 대신하지 않는다.
