# 수행 기록

- 과제: task.txt의 삼안 메모 독립 검토. 합성 시험. 허용 DB와 지정 스킬만 사용.
- 적용 스킬: inputs/Phase00/실행스킬/video-guidance-reviewer/SKILL.md (0.2.0-draft.2) 및 그 안의 두 참조문서.
- 도구: functions.exec로 PowerShell exec_command 호출. Get-Content/ConvertFrom-Json/Select-Object/Where-Object로 제공본 조회, Get-FileHash로 로컬 SHA256 계산. 쓰기는 해당 run의 outputs 두 문서와 이 transcript.md로 한정.
- 실제 사람 질문/회신 생성·발송 없음. 질문은 결과문서의 제안으로만 남김. 추가 에이전트 사용 없음.

## 수행 순서

1. 지정 task.txt를 먼저 읽었다.
2. 지정 스킬, 수행사본_범위.json, 두 참조문서를 읽고 검토자료의 프로젝트메모.md를 확인했다.
3. 문서 초안 검토임을 정하고 회사 CI·관측색·회신 범위·총점/준비상태를 중심으로 필요한 문서만 조회했다.
4. R6 실제 원문·접수 이벤트·현재 확인현황을 대조했다. 이미 확인된 최신성과 산하AI부재는 재질문하지 않고, 공식화면자격·세부가이드·시안승인과 구분했다.
5. 항목 결과 작성 전 Q-BRAND-01/02, Q-TRUST-02, Q-SCREEN-03을 목적상 필수로 선정했다. 사후 제외/선정 변경 없음.
6. 삼안 회사/자산/색 레코드, 한맥 프로필 출처/토큰 범주, 해당 품질카드를 대조했다. 대형 JSON은 로컬 파싱 후 필요한 레코드/필드를 출력해 검토했다.
7. 제공본 SHA256을 계산해 source_manifest에 기록했다. 실제 원본 자산 파일·외부 원문은 열지 않았다.
8. 검토결과.md와 검토기록.json을 작성했다. 입력 수정은 제안만 남겼다.
9. 저장한 JSON 파싱과 산출물 존재/필수 내용 및 입력 hash 변화 여부를 확인한다. 검증 결과는 아래 후속 기재.

## 실제 읽은 파일

모든 아래 입력은 읽기 전용. 기준 루트: C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase00-build/R8_시험/video-guidance-reviewer-workspace/iteration-1/eval-02-회사CI_회신범위와_사용조건/new_skill/run-1/inputs/Phase00

- C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase00-build/R8_시험/video-guidance-reviewer-workspace/iteration-1/eval-02-회사CI_회신범위와_사용조건/new_skill/run-1/task.txt
- 수행사본_범위.json
- 검토자료/프로젝트메모.md
- 실행스킬/video-guidance-reviewer/SKILL.md
- 실행스킬/video-guidance-reviewer/references/근거찾기와적용조건.md
- 실행스킬/video-guidance-reviewer/references/판정과사람검수.md
- 03_한맥디자인/07_회사CI와_화면역할_연결규칙.md
- 05_출처와검토/검수와사용범위/06_사람검수_요청과답변_접수안내.md
- 05_출처와검토/검수와사용범위/07_한맥디자인과_CI_확인현황.md
- 05_출처와검토/검수와사용범위/08_R4_R5와_검수연결_사용안내.md
- 13_품질검수/03_판정운영기준.md
- 13_품질검수/항목별기준/06_브랜드와출처.md
- 13_품질검수/항목별기준/07_분석신뢰도.md
- 10_공용자산/회사목록.json
- 10_공용자산/CI색상목록.json
- 10_공용자산/자산목록.json
- 03_한맥디자인/한맥디자인정본.json
- 05_출처와검토/R5_적용정책_결정.json
- 05_출처와검토/검수와사용범위/사람검수_요청목록.json
- 05_출처와검토/검수와사용범위/사람검수_접수대장.json
- 05_출처와검토/검수와사용범위/사람답변원문/2026-10-15_8회사CI_최신자료와산하AI부재.json
- 13_품질검수/품질항목_정본.json
- 00_운영계약/03_CI와색상_기록절차.md

위 목록의 JSON은 전체 파일 bytes를 파싱/해시했으며 검토 내용은 출력된 관련 필드·레코드로 제한했다. 별도 DB/다른 run/다른 스킬/평가기준/부모대화는 조회하지 않았다.

## 디렉터리 목록 조회

- inputs/Phase00 최상위 항목: 범위 표식 확인.
- inputs/Phase00/검토자료 파일목록: 대상 식별.
- inputs/Phase00 재귀 파일명 목록: 제공 자료 위치 확인만. 목록에 보인 모든 파일을 내용 열람한 것은 아니다.
- 지정한 9개 JSON의 파일크기 메타데이터 조회.

## 실제 작성 파일

- C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase00-build/R8_시험/video-guidance-reviewer-workspace/iteration-1/eval-02-회사CI_회신범위와_사용조건/new_skill/run-1/outputs/검토결과.md
- C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase00-build/R8_시험/video-guidance-reviewer-workspace/iteration-1/eval-02-회사CI_회신범위와_사용조건/new_skill/run-1/outputs/검토기록.json
- C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/phase00-build/R8_시험/video-guidance-reviewer-workspace/iteration-1/eval-02-회사CI_회신범위와_사용조건/new_skill/run-1/transcript.md

## 실패·미실시·한계

- 첫 3개 파일 일괄 저장용 PowerShell 명령은 Windows CreateProcessInSandbox error206(명령줄 길이 제한)으로 프로세스 생성 전 실패했다. 이 호출은 파일을 쓰지 못했다. 이후 apply_patch로 허용 경로에 저장을 재시도했다.

- 각 PowerShell 호출 초기에 FileSystem provider InitializeDefaultDrives 경고가 출력됐으나 요청한 제공본 읽기/파싱/해시 작업은 종료코드0으로 실행됐다.
- 여러 문서를 한 번에 출력한 호출의 응답이 한 차례 잘렸다. 잘린 판정운영기준은 별도 호출로 전문을 재확인했다. 판정근거는 실제 출력/열람한 지정 위치에 한정했다.
- 전체 R4/R5/R6/R7 실행기·고정문맥은 제공 범위 밖이라 실행/통과를 보고하지 않았다.
- 실제 로고/AI/영상/프레임/오디오·정확 색선택/최종합성/시청조건 미제공. 대비수치·가독성·동기화·좌표·이징 측정값 생성 안 함.
- 네트워크·CU·AE·API·Claude CLI·추가 에이전트·실제 사람 질문 도구 미사용.
- 공식CI/권한/내용/시안 승인 및 사람신원 인증 미실시. 원본/정본/대장/회신/pin 무수정.

## 저장 후 확인 결과

- outputs/검토기록.json을 다시 읽어 JSON 파싱 성공. outputs/검토결과.md를 다시 읽어 B1/B5 포함 및 선언 별색 전사 확인.
- 선정 기준4개, 기록8개(수정필요5·판단보류2·기존근거 범위통과1), 사람 질문 제안4개, 생성한 실제 답변0개.
- 전체 준비완료 제안=false. 읽은 입력22개의 SHA256을 재계산해 저장 전 manifest와 모두 동일함을 확인했다. task.txt는 hash 재검증 대상에서 제외했다.
- 두 산출물과 transcript.md의 실제 존재/길이를 확인했다. 문서14535 bytes, JSON29921 bytes. 이 문단 추가 전 transcript6197 bytes.
- 이 검증은 자체 산출물 일관성/입력 무변경 확인이며 전체 R4/R5/R6/R7 검사나 실제 시청 품질 통과가 아니다.

