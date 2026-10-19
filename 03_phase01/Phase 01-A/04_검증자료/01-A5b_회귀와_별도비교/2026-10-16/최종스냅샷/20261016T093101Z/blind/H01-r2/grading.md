# H01-r2 최초 조건가림 채점

두 sample을 독립 판정했다. 각각 core 8/8, detail 8/8 reference atom을 의미상 충족한다. 누락·wrong·avoidable unknown은 각 0개이다.

추가 단정의 검증은 미완료이다. A는 90개, B는 105개 목록 행을 남겼으나 모든 정밀 픽셀 좌표 및 부재 주장의 원자화/전수 대조가 끝나지 않아 전체 분모와 asserted_claim_precision은 null이다. 따라서 두 sample 모두 scope_incomplete=true, gates_passed=null이다. 발견한 중대 오류는 없지만 전체 부재를 입증한 것은 아니다. validation errors는 양쪽 모두 0이다.

reference atom 매칭과 추가 주장 검증을 분리했다. JSON/Markdown의 중복은 한 번만 기록했다. null을 참이나 통과로 보충하지 않았다. 미검수 묶음은 전체분모 산정용 원자 주장으로 간주하지 않는다. 정확한 AE 구현·회전축·곡선·지명 unknown은 적절하다. 큰 T의 좌향 점유 확대는 reference의 좌하 방향 점유와 양립한다. event span을 onset bracket으로 오채점하지 않았다.

시작 2026-10-16 09:12:44 UTC. 끝 2026-10-16 09:15:53 UTC. 총 AI 경과 189초. 공통준비 9초, A 검토 26초(09:12:53~09:13:19), B 검토 32초(09:13:19~09:13:51), 이후 기록 122초. 실제 clock 구간이며 시간을 반분하지 않았다. 사람 검수 시간은 측정하지 않았다. tokens=null.

읽은 파일과 이미지 및 각 claim의 근거·지원 상태는 grading.json에 기록했다. 원본 trial/스킬/맵핑/legacy/다른 pair/이전 채점은 열람하지 않았다. 새 crop/decode는 하지 않았다. 조건 추측 및 우승자 판정 없음.

