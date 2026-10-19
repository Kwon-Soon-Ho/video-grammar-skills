# old_skill 실행 기록 — motion-knowledge-use-review

2026-10-19 / 실행자: AI 하위 실행 / 지정 스킬: 보존 draft.12.
사용한 과제는 eval_metadata.json의 prompt/files이며 기존6창을 Phase00 지식과 연결했다. 다른 평가 답안·후보 스킬·다른 실행 산출물은 열람/비교/채점하지 않았다.

## 실행 범위와 결과

- 제공 모음6개와 기존 수집문서4개를 대조하고 6동작/2전체흐름 연결을 작성했다.
- 12개 R2 개념, 8개 R3 관련원칙·심화카드, 5개 R7 품질기준을 정본 ID/파일버전/SHA와 연결했다. 관측속성/시간관계·기능추론·관련원칙·실제 판정을 분리했다.
- 제공6창의 원본 프레임 경로/시각/제공SHA46행을 보존했다. 원본 MP4나46개 프레임을 다시 열거나 해시 재계산하지 않았다.
- 숫자/도상 시차 조회는 A-M3/B-M3를 반환했다. VC-MOTION-03은 관측조회0건이며 요청 시 별도 제외제안으로만 반환했다.
- 원문 보존사본4개와 입력의 실제 SHA256 일치, 정의/흐름/개념/원칙 참조 연결을 확인했다. 이는 구조/참조 자기검수이며 독립 내용평가·사용자 승인·회사 승인이 아니다.

## 실제 읽은 입력·지침

기준 루트: C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기

1. 루트 AGENTS.md.
2. knowledge-linked-skill-20261019/backup/draft12/company-video-grammar-analyzer/SKILL.md.
3. 같은 스킬 references: collection-record.md, design-and-patterns.md, motion-review.md, pattern-composition.md, evidence-and-records.md, source-readback.md, source-coverage.md.
4. knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/eval_metadata.json.
5. knowledge-linked-skill-20261019/eval-inputs/input.md.
6. 같은 eval-inputs/motion: 01_계약_수집기록.md, 02_프로젝트지원_수집기록.md, 03_재사용단위_색인.md, 05_근거와_실행기록.md.
7. 같은 motion/evidence JPG6개: contract-reflow, contract-panel, contract-number, project-reflow, project-wipe, project-panel. view_image로 모두 실제 열람.

Phase00 루트: D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00

- 00_분석단계_지식연결_추가안내.md.
- 01_공통용어/공통용어사전.json:0.1.1. 처음 머리말·모션축 목록 조회 후 생성 시 전체JSON 로드.
- 02_원칙과레이아웃/모션과정보전달원칙.json:0.1.2. 원칙 목록·선택8개 전체행 확인.
- 02_원칙과레이아웃/모션원칙_심화카드.json:0.1.2. 선택8개 전체행 확인.
- 13_품질검수/품질항목_정본.json:0.1.1. 항목 목록·선택5개 전체행 확인.
- 13_품질검수/03_판정운영기준.md 전체.
- Phase00의 공통용어/원칙/품질 디렉터리는 rg --files로 목록 확인만 했다. 목록의 나머지 파일 내용을 읽었다고 주장하지 않는다.
- 사용자 지시의 Phase01-A/05_결과보고/2026-10-19_Phase00_지식연결_재감사/00_읽는순서와_현재상태.md 및05_R1-R8_연결과_수집계약.md만 읽었다. 안내에 연결된134/172/모션 예·uses/query/검증결과·기타 기존 답안은 읽지 않았다.

원본 관측이 아닌 공통 지식 파일의 원문 출처는 knowledge-pins.json 안의 source_refs/source_locator/source_read_depth에 유지했다. 이번에 웹/외부 원전을 읽거나 그 내용을 새로 검증하지 않았다.

## 실제 명령과 도구

PowerShell/exec_command로 위 문서를 Get-Content -LiteralPath ... -Raw로 읽었다. 처음 일괄출력은 잘렸으므로 주요 기존문서/계약참조를 별도 재조회했다. 프로젝트지원은 마지막38줄을 추가로 읽었다.

디렉터리 확인:

~~~powershell
Get-ChildItem -LiteralPath 'D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00' -Force
rg --files '<Phase00>/01_공통용어' '<Phase00>/02_원칙과레이아웃' '<Phase00>/13_품질검수'
~~~

지식 조회는 Get-Content ... | ConvertFrom-Json 후 terms/principles/cards의 Where-Object id 필터를 사용했다. 선택원칙 ID는 AP-05/AP-08/AP-09/MP-07/MR-04/MR-07/MR-08/IP-05, 품질ID는 Q-INFO-04/Q-MOTION-01/Q-MOTION-02/Q-TRUST-01/Q-TRUST-02다.

도구:
- tools.view_image: 제공 JPG6개 전체; native2160×705 / 표시2048×668. 재추출/ROI 생성/영상 연속재생 아님.
- mcp__codex_app__load_workspace_dependencies: 번들Python 경로 확인.
- tools.apply_patch: outputs/의 생성기·조회기·조회 실행기·검증기와 본 기록 작성.
- 최초 생성기 저장 시 functions.exec JavaScript의 문자열 내부 Markdown 백틱 때문에 SyntaxError가 발생했다. 실행/파일 쓰기 전 파싱 실패였으며 백틱을 제거해 같은 생성기를 저장하고 정상 실행했다.
- 셸은 공통 초기화 경고 Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.를 냈으나 문서 읽기와Python실행은 exit0으로 끝났다.

실제 실행한 생성 명령(프로젝트 루트 기준):

~~~powershell
& 'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/build_outputs.py'
~~~

exit0 결과: uses6, flows2, frame_refs46, terms12, principles8, quality5.

~~~powershell
& 'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/run_queries.py'
~~~

exit0. 내부에서 query.py 실제 subprocess를7회 실행했다. 전체 절대경로 명령·exit code·반환 본문은 outputs/query-results.json 및 사람이 읽을 outputs/query-results.md에 기록했다.

| 실제 query.py 인자 | 실제 관측 반환 |
|---|---|
| --relation numeric-before-graphic | A-M3, B-M3 |
| --concept TIME-DELAY | A-M3, B-M3 |
| --id A-M3 | A-M3 |
| --id LOCAL-FLOW-B-REVIEW-v1 | B-M1, B-M2, B-M3 |
| --principle MR-08 | A-M3, B-M3 |
| --id VC-MOTION-03 |0건|
| --id VC-MOTION-03 --include-excluded |관측0건; 별도 excluded_proposals에 VC-MOTION-03만|

~~~powershell
& 'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-2-motion-knowledge-use-review/old_skill/outputs/verify_outputs.py'
~~~

exit0: 보존사본 해시일치true,6사용처/2흐름/46프레임참조,개념/원칙/흐름 참조resolve=true,원본media해시 재검사false,음성검사false. 전체 결과는 outputs/verification.json.

## 주장별 확인과 한계

| 주장 | 실제 대조 | 현재 한계 |
|---|---|---|
| A-M1 판 재배치/도상→캡슐→숫자 |96~100 sheet와 계약§4|0.5초 상태표본이며 정확 시작/곡선 미상.100초 값은 최종8.7이 아님|
| A-M2 판 첫 가시경계·라벨 단계 |103~106 sheet/기존관측| (103.5,104]는 시작 범위. 기존판 모든 재정렬 강제 금지|
| A-M3 0.8→10.8→12.9억원 |109.5/110/110.5 및111 sheet|끝값(110,110.5],111은 도상후속 비교.112 화살표는 기존기록만; 이번 직접미검수|
| B-M1 퇴장/새값 겹침 |138 sheet|실제opacity/parent/곡선 미상|
| B-M2 대각분할과 내부영상 |144~146 sheet|첫가시경계(143.5,144],실제마스크/카메라 궤적 미상|
| B-M3 44→64→82%,후속카드/도넛/막대 |148/148.5/149/149.5/150 sheet|끝값(148.5,149],모든 도상 동시완료 아님; 실제 분모/Scale/연속완성시각 미상|

숫자의 의미/끝값 관계는 보존하되 동시 시작/종료 회사규칙으로 바꾸지 않았다. 원본 제작의도/실제실적 원자료·내용정확성은 AI 기능해석과 다르다. 6표본창 바깥·틈·퇴장·전편은 미관측이며 근거 없는 완료율/소요시간을 계산하지 않았다.

## 산출물·다음 범위

첫 열람: outputs/collection.md → preserved-input 상세 → evidence-manifest.json/원문 해시표.
조회: outputs/query.py + index.json + knowledge-pins.json.
실제 결과: outputs/query-results.md/json, verification.json, input-manifest.json.
로컬 생성기/조회 실행기/검증기도 outputs 아래 보존했다.

이번 요청의 기록/조회 시범은 완료했다. 남은 것은112초 직접 근거 확인, 표본 간 경계/곡선/전체 읽기 유지·음성/실측값 출처 검수다. 이는 본 입력에 없는 추가 근거가 필요한 별도 범위다. 새 화면/영상/PDF·정본 변경/등록·스킬 편집·R4 이관은 수행하지 않았다. 다음 묶음 선택은 상위 작업에서 사용자에게 보고할 범위이며 이번 실행이 임의 착수하지 않는다.

