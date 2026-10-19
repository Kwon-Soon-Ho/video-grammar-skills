# 기존 draft.12 실제 실행 기록

2026-10-19. 지정된 같은 기존 자료에서의 독립 문맥 실행이며 일반화/새 영상 시험이 아니다. 비교·채점은 하지 않았다. 적용 스킬은 [backup draft.12 SKILL.md](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/backup/draft12/company-video-grammar-analyzer/SKILL.md>) 하나이며 Phase00 스킬 안내는 지식의 역할 경계를 읽기 위한 자료다. 다른 스킬을 실행하거나 편집하지 않았다.

## 수행 범위·산출

제공 134·172초 PNG와 기존 수집 5문서를 대조하고 로컬 DB 수집 초안/조회 색인을 작성했다. 원본 MP4·오디오·시나리오는 미제공이다. 출력은 본 old_skill/outputs, 이 실행 기록만 old_skill/execution.md에 저장했다. 새 화면/영상/PDF·정본 쓰기·글로벌 스킬 활성화 없음.

- [시작/사례 요약](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/00_읽는순서.md>)
- [전체 상세·기존 번호·현재 사용처](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/01_수집기록.md>)
- [지식 연결·실제 자기 재대조](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/02_지식연결과검수.md>)
- [조회 명령과 색인](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/03_조회색인.md>)
- [로컬 조회 DB](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/index.json>) / [조회 도구](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/query.py>)
- [명령별 실제 종료코드/출력](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/query_execution.json>) / [실제 결과 확인](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/query_verification.json>)

## 실제 읽은 입력/근거/참조

- [task_input](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/input.md>) — SHA256 `65e070acd852cd5bf911d30d62c4c635a5ccaa2c945b9e1d9f8a51b55a01817e`
- [provided_prior_record](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/static/00_사례요약.md>) — SHA256 `680cd5f9db361d4ee7b7b5f166405bf7cacff28ac55f02245725703e777036c9`
- [provided_prior_record](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/static/01_부품과조합.md>) — SHA256 `5c4ae7ad8b8254b52432ba9883c6139d8c2bd6ce4446dec4624e5581b713942e`
- [provided_prior_record](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/static/02_전체상세.md>) — SHA256 `c1bc9c1d49e460a276c394ef5e8a260021c24f5abd8c864fca542fba9ffa6d85`
- [provided_prior_record](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/static/03_근거와검수.md>) — SHA256 `a677b68f81e085aaffebd9a684b36f9bc6396791965765570c0fd5d21670f671`
- [provided_prior_record](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/static/04_모션조사.md>) — SHA256 `2e4915cfd3e6ce3e6b0384ef3e61b6a487f5237c3093c433cdbb26aa2f7e3036`
- [phase00_knowledge_read_selected_objects](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/01_공통용어/공통용어사전.json>) — SHA256 `c71ec597b924bd6da69fdfeb4635e290de75823186fbf7236b9615d613c6c7b2`
- [phase00_knowledge_read_selected_objects](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/02_원칙과레이아웃/레이아웃지식.json>) — SHA256 `0225b8ff97c7ab9441cbe6d1fd7539da8d97ce90bf2e9003d63f4f4ae6175306`
- [phase00_knowledge_read_selected_objects](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/02_원칙과레이아웃/모션과정보전달원칙.json>) — SHA256 `249ef6b9e7b14ff62f41352922be2f00e748c8b10debb4d4992b580364e0daa5`
- [phase00_knowledge_read_selected_objects](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/02_원칙과레이아웃/화면설계원칙.json>) — SHA256 `281fe61151dfc96649a070b6fd3ae653c0353b7513f3209534140ce1f54e6b96`
- [phase00_knowledge_read_selected_objects](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/13_품질검수/품질항목_정본.json>) — SHA256 `c5b9e91e902747a1d657fbbaee19c4b2b97e96dcf58f0ae2bb032384f29ce60f`
- [instruction_or_reference_retrieved](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/AGENTS.md>) — SHA256 `9c4fc79f89c67f4337872ddabe3a5ddee9572dfba3a74115155db71c4871093a`
- [instruction_or_reference_retrieved](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/backup/draft12/company-video-grammar-analyzer/SKILL.md>) — SHA256 `1b41563eb1690ff894f98ffe9f7f3aacc5e6dbcc44b1eb990ae830c1a9eb1f4e`
- [instruction_or_reference_retrieved](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/eval_metadata.json>) — SHA256 `65510b82be9809115e32dd3bd71898272a47453565275cb948ee379d3d227ff7`
- [instruction_or_reference_retrieved](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/backup/draft12/company-video-grammar-analyzer/references/evidence-and-records.md>) — SHA256 `8c93e253300030ae303f13e292017d566dab74466c4f2872cd5f60d4bb351771`
- [instruction_or_reference_retrieved](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/backup/draft12/company-video-grammar-analyzer/references/collection-record.md>) — SHA256 `89f8b08d64f6ad69898ae6c7bcb027eb1e219d905ae7ddab8cd2329506257e3c`
- [instruction_or_reference_retrieved](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/backup/draft12/company-video-grammar-analyzer/references/design-and-patterns.md>) — SHA256 `da014fee6aba36a2256733693d2fac2a358161b0eacf15e125149398b97aa61a`
- [instruction_or_reference_retrieved](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/backup/draft12/company-video-grammar-analyzer/references/pattern-composition.md>) — SHA256 `9ee0683e725589e28a46536392b57be0b4985bd2f3bcc1289935919cd40a0489`
- [instruction_or_reference_retrieved](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/backup/draft12/company-video-grammar-analyzer/references/source-readback.md>) — SHA256 `514d6065271ea10695c94cc7867186517dd8f04af28e6df8c7ab21bc29140be2`
- [instruction_or_reference_retrieved](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/backup/draft12/company-video-grammar-analyzer/references/motion-review.md>) — SHA256 `b386dc2a59eca610217db2de39b58e095eda0edf1f9e7a6916f422b257e1bdd3`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/00_분석단계_지식연결_추가안내.md>) — SHA256 `f79cedc4aee147c6349242c7d520dd701537b1703d3085f6210eb0a858f8fbdd`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/00_시작안내.md>) — SHA256 `efbc89c42637577c8a1d540c0231d77e7071e03a421cb146ef9bcc669ed38a8c`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/01_공통용어/02_기록단위와분류축.md>) — SHA256 `8889d8d482add29ab4a61ea504bc9a2b12fd3168fad9c73c5b7fc2569975c87a`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/01_공통용어/용어목록.md>) — SHA256 `5162ffa42eb40131890f2c2bbcb4c44e54d662dede2d83712d56f52e0c341d8c`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/02_원칙과레이아웃/00_지식안내.md>) — SHA256 `f5fbbd632bd0cf604c73b6859ddc37d8e64cd5a3ab55ab383e4de69f29d737af`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/02_원칙과레이아웃/06_레이아웃지식_읽는순서.md>) — SHA256 `2fdfb5a725ae2c7d54a425c189dbdc9aec8092b6bc9157886bbefa9f8a42fc49`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/02_원칙과레이아웃/07_레이아웃별_선택조건과반례.md>) — SHA256 `945fa1ec974bd73899d71de9b4019edf0d465d3c32443a9fe8ee610d56c471dd`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/02_원칙과레이아웃/08_화면설계_적용기준과반례.md>) — SHA256 `1c6216125725542785ac8773d4cc6d41adbc178044aa2016f2c0af5630431c0e`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/02_원칙과레이아웃/지식목록.md>) — SHA256 `df848ec46422e54dd6f25d067676f3acb6bc15957554f8547273ec39a99b3b3b`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/06_맞춤스킬/00_스킬안내.md>) — SHA256 `6f259a80ad6a29a67fa0a24fafa7d1bb010629c604f51953c8a7f42de61238af`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/03_한맥디자인/07_회사CI와_화면역할_연결규칙.md>) — SHA256 `be1baa8a5535d9f43f189bd7bab3f46320c81c5e7697a972f2a6a93320def83b`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/13_품질검수/04_품질항목_읽는순서.md>) — SHA256 `0d03a7a5b0216937ad6f0b8aab24aabe263240e7b6649853dec721545620fc04`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/13_품질검수/03_판정운영기준.md>) — SHA256 `2a8e21f028e18398ab2a6544cc429e585ab6a0a59abd370dbacd7991e141b7c1`
- [instruction_or_reference_retrieved](<D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/13_품질검수/항목별기준/07_분석신뢰도.md>) — SHA256 `913573ab7251705ade6d24b540be00fc6c77a0ea3098f1355fd7133e65c62901`
- [E1](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/static/evidence/134.png>) — SHA256 `e1fe065b8d9f9ad8ce819266389a8326d58ecb886fe85b53eb6e18a701f3f2f8`
- [E2](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/eval-inputs/static/evidence/172.png>) — SHA256 `44a26a91328863dd335f9b950780afb96929888f8475b45b2298035250a1771a`
- [e1_logos](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/evidence/e1_logos.png>) — SHA256 `28e5f0d5a8519701c2165d86d93f1b2484f9eb2055bdf8e8567099a9b0137de3`
- [e1_roles](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/evidence/e1_roles.png>) — SHA256 `867c8a0da1fd764274349a013e6ee9895e53ab0acea3cccba5f02767284b0400`
- [e1_arrows](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/evidence/e1_arrows.png>) — SHA256 `4b8a06cb9b54972b85246d345313191ff43bc1fc520ea8d4724727d13b9cd1c3`
- [e1_work](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/evidence/e1_work.png>) — SHA256 `3434f46fc04c72b547d5d9c0b128093806ae9d13fa28cb4cac2eff280aab7b0e`
- [e2_logos](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/evidence/e2_logos.png>) — SHA256 `be46708f5dc7d67266003952f8d28bcd1f4bdc0c45138a05f55c7e5ac6eeff64`
- [e2_value](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/evidence/e2_value.png>) — SHA256 `ec05cfe020b527c3d372a6981fec1287c178c235f0b0cff2e4684f1c35fe89f7`
- [e2_building](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/evidence/e2_building.png>) — SHA256 `c54ba9bc56e3a65bbc8d0b433eb23f40e7f502d69da1b55cdc538f80918cf2f7`
- [e2_number](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/evidence/e2_number.png>) — SHA256 `d698290c30b12d96ebdb4ae735873dc3c999a7f70ff35bef5bf4dece708f1932`

`eval_metadata.json`에서는 prompt/files를 사용했다. assertions는 판단 근거로 사용하지 않았다. 원기록 안의 미제공 original/collection.md와 예전 절대경로는 열지 않았으며 현재 두 PNG로 연결한다. 다른 실행 결과/답안 파일 내용은 읽지 않았다. Phase00 최신 추가안내의 링크 목록을 확인했지만 같은 입력의 기존 사용처 답안이 포함될 수 있는 Phase01-A 권장 구조/문법색인 결과는 열지 않았다.

## 실제 실행 명령과 방법

1. PowerShell `Get-Content -LiteralPath ... -Raw`로 루트 AGENTS, 지정 SKILL/참조, eval_metadata, 공통 입력/기존 5문서, 위 Phase00 안내/조건 문서를 읽었다. 결합 출력 일부가 잘려 핵심 적용 조건은 정본 JSON에서 선택 객체/필드를 다시 조회했다.
2. 처음 `rg --files <Phase00 root>`를 실행했으나 backup을 포함한 매우 큰 경로 목록이 잘렸다. 파일명 목록만 반환됐고 그 경로의 다른 실행 내용은 읽지 않았다. 이후 `Get-ChildItem -LiteralPath <주제 폴더> -Name`와 정본 파일 직접 읽기로 범위를 좁혔다.
3. `load_workspace_dependencies`로 번들 Python을 확인했다. Python은 `C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`다.
4. 위 Python으로 `outputs/prepare.py`를 실행했다. 기존 문서 6개(공통 입력 포함) 바이트 복사/해시 확인, 원본 PNG 치수·해시 확인, PIL crop-only 8개 생성, 선택 지식 41개를 정본 해시·버전·JSON pointer와 보존했다. crop은 증거 보조이며 새 디자인이 아니다.
5. `view_image`로 원본 PNG 두 장과 crop 8개를 실제 보았다. 표시 크기/좌표/변환은 근거 문서에 기록했다.
6. 같은 Python으로 `outputs/build.py`를 실행해 사례2·기존 정의10·사용처12·지식연결12·검수15·미상6과 문서/색인을 만들었다. `outputs/query.py --validate --out query_results/validation.json`을 실행했다.
7. `outputs/run_queries.py`를 실행해 실제 조회 명령 9개를 subprocess로 실행하고 종료코드/명령/결과를 저장했다. 최초에는 사례002 기대 개수를7로 적은 확인 코드 오기가 발견되어6으로 정정했다. [실패/정정 이력](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/query_verification_initial_failure.md>)에 보존했다. 조회 데이터와 스킬은 바꾸지 않았다.
8. `outputs/finish.py`로 읽은 파일 목록/해시와 본 실행 이력을 추가한 뒤 `run_queries.py`를 다시 실행해 확장 출처 목록까지 검사했다. 최종 검사 수는 [실제 validation 결과](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/knowledge-linked-skill-20261019/company-video-grammar-analyzer-workspace/iteration-4/eval-1-static-knowledge-use-review/old_skill/outputs/query_results/validation.json>)를 따른다.

실제 조회 명령은 `query_execution.json`에 Python 절대 경로·전체 인자·cwd·종료코드·stdout/stderr로 보존했다. 문서의 예시는 실행된 인자와 같다.

## 확인 결과와 한계

- 기존 5기록과 공통 입력의 복사 SHA 일치. 기존 번호/판본/정의·상세/미관측 조사 번호 보존.
- 전체 PNG2·ROI8에서 정적 문구·방향·회사 순서·소품/층/명찰 관계를 자기 재대조했다. 표본2를38초 연속 검사로 부르지 않는다.
- 실제 조회9개 종료코드0. 업무묶음1·건물1·역할판2·명찰1·회사타일1·IP-04 연결2·REV-04 대상2·사례002 정의6이 반환된다. 해시/ID/포인터 검사는 내용 정확성·R4 호환·회사 승인 판정이 아니다.
- 정본 지식과 원본 관측/기능 추론/실제 검토를 별도 필드로 분리했다. 분할 비교·실제 UI·차트·실제 공간 관계·카운트업을 모양만으로 확정하지 않았다.
- 원본 PNG의 해시는 검증했지만 MP4 해시·원본 PTS·음성은 입력 메타데이터 이상으로 검증하지 않았다. 전편·모션·정확 폰트/색/효과·원자산·회사CI 사용형·실제 시청 효과는 미확인이다.

바로 다음 확인이 필요하다면 원본 구간/편집 자산/표시 환경 중 목적에 맞는 입력을 확보해 기존 Q 조사 범위나 해당 보류 항목만 보강한다. 이번 과제에서 추가 제작이나 정본 등록을 착수하지 않았다.
