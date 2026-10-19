# 공통 실행 안내

이 문서는 양 조건에 동일하게 제공하는 입력/도구/한도 안내다. 평가 기준답안은 제공하지 않는다.

`common-task.md`와 `common-output-format.md`를 따른다. 해당 실행의 input.json에 원본, 구간, 기본 추출 로그와 문서 경로가 있다. 기본 PNG와 board*.jpg를 읽을 수 있다. 문서가 없으면 무문서 분석이다. 정확한 AE 키프레임은 없고 음성은 범위 밖이다.

본격 자료 열람 직전 UTC를 기록하고 15분 안에 저장·검증·종료한다. native RGB 무배율 크롭은 최대40개다. 크롭을 만들면 path/parent_path/crop_xyxy_native_pixels 정수 네 좌표를 JSON 배열로 기록한다. 보드는 탐색용, 출력의 근거는 로그 PNG 또는 그 픽셀 일치 크롭이다. 실제로 열람한 근거만 기록한다.

추가 추출은 각24개 이내로 최대2회, 합계48개다. 같은 실행의 요청 시각은 오름차순 중복없는 JSON 배열로 자신의 support 폴더에 저장한다. `trial_tools.py extra <run_id> <1 또는 2> <요청 JSON 절대경로>`로 실행한다. 도구가 출력한 LOG 경로의 actual_playback_seconds 및 PNG를 사용한다. 추출 실패는 보존하고 주 실행자에게 알린다. 다른 디코더/오디오 추출/외부 API를 쓰지 않는다. 소스/창은 교체하지 않는다.

Python: `C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -B -X utf8`. Pillow/numpy는 `phase01a-a1/후보런타임`을 sys.path에 추가하면 사용할 수 있다. trial_tools.py는 phase01a-a5b에 있다. 시스템/전역 설치하지 않는다.

출력은 자신의 trial/outputs/observations.json 및 observations.md. 추가 지원자료는 trial/support. 저장 후 `trial_tools.py finish <run_id> <크롭 JSON 절대경로>`로 구조/근거를 공통 검증하고 동결한다. 크롭이 없으면 마지막 인수 생략. 이 검증은 내용 정답 검사가 아니다. 형식 오류는 15분 한도 안에서 고칠 수 있으나 내용 피드백은 없다. 검증 통과 뒤 본문을 바꾸지 않는다.

run-effort.json은 자신의 trial 루트에 저장: UTC 시작/종료, AI elapsed초(검증 포함), 실제 읽은 파일, 보드/직접PNG/크롭 생성·열람 수, 추가추출 수, 미완료 항목, 사용자 참여 없음, tokens=null(도구가 미제공하면) 및 모델은 parent inherited exact host ID unavailable. 실제 사람 읽기 시간을 추정하지 않는다.

허용자료는 자신의 input, 공통 안내·출력형식·도구, 자신의 원본 기본 PNG/log/보드·문서, 자신의 추가 추출/크롭뿐이다. 이전 관측·과거 사용자 정정·legacy·reference·채점/다른 반복 결과·다른 trial 지원자료를 읽지 않는다. 스킬 사용군만 따로 지정받은 동결 스킬을 읽는다. 다른 사용 가능한 스킬은 읽지 않는다.
