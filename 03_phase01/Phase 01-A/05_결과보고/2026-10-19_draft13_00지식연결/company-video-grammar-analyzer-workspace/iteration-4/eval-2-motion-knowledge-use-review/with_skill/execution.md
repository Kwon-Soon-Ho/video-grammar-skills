# 실제 실행 기록 — 모션6창 / 지정 candidate 실행

날짜:2026-10-19. 수행 범위는 eval_metadata.json의 prompt/files에 있는 기존 계약·프로젝트지원6개 모션 관측 창이다. 루트 AGENTS.md와 명시 candidate draft.13을 적용했다. 다른 평가 결과·이전 실행/답안은 열람·비교·채점하지 않았다. 원기록 prior analysis는 과제가 제공한 입력으로만 사용했다.

## 적용한 입력·도구·읽기 범위

- 작업 루트: `C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기`
- 출력 루트: `C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\knowledge-linked-skill-20261019\company-video-grammar-analyzer-workspace\iteration-4\eval-2-motion-knowledge-use-review\with_skill\outputs`
- 수집 스킬: candidate/company-video-grammar-analyzer/SKILL.md 및 references 8개(지식연결·수집기록·디자인패턴·모션·부속계약·근거·조합·원본재대조), scripts/knowledge_links.py를 실제 읽었다.
- 사용자 지정 AGENTS.md, eval_metadata.json, 공통 input.md, 모션01/02/03/05를 읽었다. 처음 묶음 읽기의 일부 출력이 잘려 필요한01/02/03과 스킬 참조를 다시 분리해서 읽었다. 05의6개 근거표·시각/기존 해시가 제공 원문으로 보존되어 있다.
- 6개 JPG를 view_image로 실제 열어 시트의 시작/중간/끝 및 내부/주변/배경 변화를 대조했다. 기존 원기록에서 링크한112초·150초 PNG도 열었다. 원본 MP4/오디오를 받거나 재생하지 않았고 새 추출/크롭은 하지 않았다.
- 실제 연 파일과 SHA: outputs/read_manifest.json. 이미지 실제 표시 축소와 대조 범위: outputs/01_근거대조.md.
- Phase00 정본 공통용어/기본지식/품질질문을 카탈로그로 읽고 18개 정확ID의 원문 정의·조건·반례를 조회했다. 167개 목록을 확인했지만167개 항목을 모두 의미 검토/적용한 것은 아니다.
- R8_현재사용안내·Phase00 루트01_진행현황·R7판정운영기준·공통 안내로 지정된 Phase01-A 지식연결 재감사의00_읽는순서와_현재상태.md만 읽었다. 감사의 다른 결과/사례/조회 색인은 열지 않았다.
- 심화카드는 AP-05/AP-06/AP-09/IP-05/MR-04/MR-08, 추가모션후보 rows는12개(및 목록 메타), 스킬심층검토정본은 local-chart-animation/local-animated-infographic/local-motion-art-direction3개를 선택해서 읽었다. 카탈로그의 다른 문맥은 경로·해시 확인이며 전문 의미검토라고 보고하지 않는다.

## 실제 명령과 결과

- powershell Get-Content로 위 입력/지정 참조를 읽었다. 쉘이 매회 출력한 InitializeDefaultDrives 경고에도 실제 C/D 지정 파일 읽기와 Python 명령은 실행되었다.
- tools 폴더의 python/knowledge 이름 탐색 rg --files는 런타임 위치를 찾지 못했다. load_workspace_dependencies로 번들 Python 경로를 확인했다.
- 실제 Python: `C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`.
- 첫 catalog 명령은 다음과 같았다(종료0,167개 개념·11개 문맥). R8 읽기 전 실행한 최초 명령에는 -B/-X가 없었다. 이후 Python은 -B -X utf8을 사용했다. 새 외부 패키지·전역 스킬 설치 없음.

```powershell
& 'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'knowledge-linked-skill-20261019/candidate/company-video-grammar-analyzer/scripts/knowledge_links.py' catalog --phase00 'D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00' --out 'knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/with_skill/outputs/catalog.json'
```

- catalog의 IDs·종류·이름을 Python으로 출력해 선택했다. 이후 knowledge_links.py query --catalog <catalog.json> --id <ID>를18회 실제 실행해 outputs/knowledge_queries.json에 정확 명령·반환 원문·종료0을 저장했다.
- 선택ID: TIME-SEQUENCE, TIME-OVERLAP, TIME-DELAY, TIME-HOLD, PROPERTY-VALUE, PROPERTY-VISIBILITY, PROPERTY-POSITION, PROPERTY-SIZE, FUNCTION-REVEAL, FUNCTION-CONTEXT, REL-PART, AP-05, AP-06, IP-05, MR-04, MR-08, Q-MOTION-01, Q-TRUST-01. Q-TRUST-01은 질문/필요 근거를 읽은 항목이며 실제 전체 원본 신뢰도 통과로 연결하지 않았다.
- 원문 심화/추가모션/source검토 JSON은 Python 선택 출력으로 읽었다. 전체 스킬 원문이나 외부 웹을 실행/설치/다운로드하지 않았다.
- R8의 ../01 링크를 처음 잘못 해석해 Phase00/14_스킬재구성/01_진행현황.md를 Get-Content한 것은 경로 없음 오류였다. 정확한 Phase00/01_진행현황.md를 읽어 보완했다. 이 실패를 자료 전체 접근 불가로 확대하지 않았다.
- outputs/build_outputs.py를 실행해 Markdown3개·관측/지식 부속 JSON·색인·명령/결과 JSON을 생성했다. 최초 실행 후 자기 검토에서 A-M1의 중첩 태그를 추가하고 B-M3 후속 사건 범위를 카드 등장148.5부터로 정정해 원문의 중첩을 보존했다. 이번 임시 산출만 재생성했으며 원기록/정본/지정 스킬은 수정하지 않았다.

최종 실제 명령·종료코드 원문은 outputs/commands.json에 있으며 다음 결과를 얻었다.

| 명령/출력 | 실제 결과 |
|---|---|
| `validation.json` / 종료 0 | valid=true (연결/해시/범위 한정) |
| `index-build.json` / 종료 0 | records=1 |
| `query-TIME-DELAY.json` / 종료 0 | A-M3, B-M3 |
| `query-PROPERTY-VALUE.json` / 종료 0 | A-M3, B-M1, B-M3 |
| `query-TIME-OVERLAP.json` / 종료 0 | A-M1, A-M3, B-M1, B-M2, B-M3 |
| `query-MR-04.json` / 종료 0 | A-M1, A-M2, A-M3, B-M1, B-M2, B-M3 |
| `query-IP-05.json` / 종료 0 | A-M1, A-M2, A-M3, B-M1, B-M2, B-M3 |
| `query-Q-MOTION-01.json` / 종료 0 | A-M1, A-M2, A-M3, B-M1, B-M2, B-M3 |
| `query-excluded-proposal.json` / 종료 0 | 0건 |
| `query-definition-A-M3.json` / 종료 0 | A-M3 |

핵심 조회 재실행 예(현재 디렉터리를 outputs로 두고 실행):

```powershell
$py = 'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$tool = 'C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/candidate/company-video-grammar-analyzer/scripts/knowledge_links.py'
& $py -B -X utf8 $tool query --catalog catalog.json --index index.json --id TIME-DELAY --motion-only
& $py -B -X utf8 $tool query --catalog catalog.json --index index.json --id Q-MOTION-01 --motion-only
```

- 실제 조회 결과에서 사례→정의/판본→TIME-DELAY→다른 사용처→각 근거/원기록 해시·시간 사건을 outputs/verify_roundtrip.py로 왕복했다. 종료0, passed=true, A-M3/B-M3, 제안 혼입0건. outputs/roundtrip-result.json에는 실제 claims/events/event_links/original_records/current_evidence/reviews를 확장 보존했다.
- 지식의 source pin/관측 파일 pin과 이번 정의/사용처 판본 일치, 각 시차 단위의 continues_after 관계, IP-05 not_reviewed/Q-MOTION-01 hold 반환을 확인했다. 이는 시각 의미/효과/전편 발견을 자동 판정한 시험이 아니다.

## 결과와 결정 이유

- 총10단위(전체사례2+독립모션6+부분전체흐름2), 사용처8, 관측사건21, 사건관계17, 실제 검토행27, 지식연결92를 작성했다. 숫자/태그 수는 완성도 점수가 아니다.
- A-M3: 실제 매출12.9억원의 숫자는(110,110.5]초에 끝값 최초 관측.111초 도상 상태와112초 완성 상승 화살표 차이를 함께 보존.112초는 기존 문맥 PNG이며6창 안에 새 연속 관측했다고 쓰지 않았다.
- B-M3: 지원 BIM설계19.4억원/3건·약82%의 비중은(148.5,149]초에 끝값 최초 관측.149.5초 도넛 보조 분할색·카드가 뒤늦게 보강. 배경 재구성·카드 겉보기 크기·막대 후속 진행을 보존하고 정확 길이/종료/Scale은 유보.
- 같은 완료시차 개념으로 조회하되 동일 동작/자산/회사 공통규칙으로 합치지 않았다. 원래 A-M1~3/B-M1~3 ID·의미와 전체 상세 원문은 유지했다.
- 관측 기반 태그는 classified_as(분석자의 해석), 원칙의 관련성은 review_relevant, 실제 범위별 검토는 reviews/evaluated_against로 분리했다. AP-05는 관련질문만 연결하고 관성/효과 판정은 하지 않았다.
- MR-04 pass는 기존 기록의 순서/중첩을 현재 기록에 보존한 자기 검토만 의미한다. AP-06 hold, IP-05 not_reviewed, Q-MOTION-01 hold를 조회 결과에도 반환시켰다.

## 미상·미실시·남은 범위

- 창 사이100–103/106–108/111–112(끝PNG만)/140–143/146–147초의 연속 변화,6창 밖의 모션 상세, 개별46프레임 전부/추출로그/MP4 PTS 매핑 재검증은 미실시.
- 오디오/시나리오·발화 싱크, 완성 뒤 유지/퇴장과 실제 읽기 충분성, 원본 폰트/효과·곡선/opacity/mask/Scale·제작의도, 막대 데이터 분모/스케일, 실제 집계 사실·같은 자산·외부 적용 효과는 미상/미검수.
- 100초 비용 숫자는 시트에서 중간0.7억원처럼 보이나 원본 크기 전사는 하지 않았다. 종료값8.7억원과 구별한다. 이 제한이 전체 구성/순서 기록을 지우는 이유는 아니다.
- 새 화면·영상·PDF, 정본 DB/스킬 수정·등록/교체, 글로벌 활성화, 다른 실행과 비교/채점은 수행하지 않았다. 이 결과는 정밀 전편 검수 완료나 회사 승인/일반 성능 평가 결과가 아니다.
- 다음 선택지는 outputs/00_수집기록.md 끝에 큰 범주4개로 남겼다. 선택에 의존하는 새 묶음은 시작하지 않았다.

## 산출 경로

- outputs/00_수집기록.md: 사례 요약→전체 상세→근거/판정/후속 선택
- outputs/01_근거대조.md: 실제 시각 대조·해시·원래근거 범위
- outputs/02_조회안내.md: 작동 명령·실제 결과·시차2사례 왕복
- outputs/motion.links.json / catalog.json / index.json: 편집 부속·정본 지식 pin·생성 조회 색인
- outputs/validation.json / query-*.json / knowledge_queries.json / commands.json / roundtrip-result.json: 실제 실행 결과
- outputs/read_manifest.json / output_manifest.json: 실제 열람자료와 산출해시
- with_skill/execution.md: 이 실행 기록.
