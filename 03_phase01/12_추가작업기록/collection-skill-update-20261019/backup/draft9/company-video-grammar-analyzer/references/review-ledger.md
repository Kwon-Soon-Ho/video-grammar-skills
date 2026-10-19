# 누락·오답 수정 검수

실제 피드백이나 기준 대조에서 지적이 생겼을 때만 수정 장부를 만든다. 이전 JSON을 덮어쓰지 않고 새 JSON에 보완한다. 수정 전·후 경로와 SHA-256, 지적과 필요한 대상·속성·세부 필드, 보완 주장, 검토 주체·확인 방법을 기록한다.

`scripts/review_ledger.py <review-ledger.json> --catalog <catalog.json>`으로 판본·범위·수정 주장·근거 연결을 검사한다. 카탈로그는 수정 후 기록의 프레임 출처를 검사하며 수정 전 판본은 별도로 고정 보존한다.

- `open`: 보완 미완료. 다음 확인 방법을 적고 보완 주장으로 닫지 않는다.
- `addressed`: 해당 지적에 답하는 관측 기록을 추가·변경했다. 원본 화면에서 그 내용이 맞는지는 검토 주체가 확인해야 한다.
- `withdrawn` / `out_of_scope`: 철회·검수 범위 밖의 이유를 적는다. 보완 완료로 집계하지 않는다.

장부의 각 `requirements`는 `object_id, property, dimension`으로 요구를 구분한다. addressed는 해당 요구마다 변경된 supported 주장과 요구한 근거 유형을 연결해야 한다. 관측 요구를 추론이나 관련 없는 대상의 주장으로 대신하지 않는다. 장부는 같은 영상·구간의 수정 전후만 비교하며, 다른 장면 검증이나 회사 승인을 나타내지 않는다.

검토자는 `same_agent_context`, `independent_ai`, `human` 중 실제 수행한 범위를 적고 이름·방법을 남긴다. 검사기는 검토자의 신원이나 독립성을 입증하지 않는다. 동일 문맥에서 이미 본 정답에 맞춘 보완은 개발 수정이며 성능 시험으로 보고하지 않는다. 원래 발견하지 못한 요소는 원본 재관찰로 계속 찾아야 한다.

장부 형식: `schema_version=video-review-ledger-0.1`, `revision` 양의 정수, `before/after={path,sha256}`, `reviewer={kind,name,method}`, `findings=[{id,question,requirements:[{object_id,property,dimension}],required_basis_kind,before_claim_ids,state,resolution_claim_ids,reason,next_probe}]`. 새 판본은 기존 장부도 별도 파일로 보존한다. 판본 번호는 원본 REA의 동시 수정·충돌 관리 기능을 구현했다는 뜻이 아니다.
