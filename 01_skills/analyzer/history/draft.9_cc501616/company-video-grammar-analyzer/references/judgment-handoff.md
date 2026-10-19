# 판단·재제작 인계

handoff:{purpose,information_relation,observed_claim_ids,preserve_claim_ids,open_unknown_ids,condition_candidates,implementation_options}.

purpose와 information_relation은 null 또는 {text,basis_kind,claim_ids}. 시나리오·제작자 확인 없이 의도를 확정하지 않는다. observed_claim_ids에는 observed/calculated 주장만, preserve_claim_ids에는 새 설계에서 보존할 특성의 주장 ID를 넣는다. 원본 관측의 검수 상태도 함께 전달한다.

condition_candidates:[{condition,reason,claim_ids,counterexample,validation_state}]. 조건은 문구 길이·요소 수·화면비·읽기 시간 등 실제 적용 쟁점에 연결한다. 반례 미시험이면 counterexample=null, validation_state=untested. 그 원본 한 사례에서 확인한 범위만 observed_case로 쓸 수 있다. 회사 공통 규칙의 승인은 여기서 만들지 않는다.

implementation_options:[{proposal,basis_kind:"inferred",claim_ids,verification_needed}]. 같은 렌더를 만드는 구현은 여럿이다. 원본 AE 키프레임·효과를 복원했다는 주장과 새 구현 제안을 분리한다. 실제 편집 결과·렌더에서 확인해야 할 내용, 새 문구·화면비로 바꿔 확인해야 할 내용을 적는다.

선택 순서는 필수 문구·정보 관계·가독성·동작 목적을 충족하는 내부 사례, 작은 변형, 기존 제작 기능, 필요한 새 표현이다. 맞지 않으면 다음 대안으로 넘어간 이유를 적는다. 요소 수나 후보 수의 최소화 자체를 목표로 삼지 않는다.

원본·시간 매핑·추출 설정·관측 판본이 같은 근거는 재활용한다. 새 목적과 조건의 적합성 검수는 다시 한다. 원본 재현 성공과 새 내용 재사용 성공은 따로 입증한다. 같은 품질이 확인된 비교에서만 공수 절감을 계산한다.
