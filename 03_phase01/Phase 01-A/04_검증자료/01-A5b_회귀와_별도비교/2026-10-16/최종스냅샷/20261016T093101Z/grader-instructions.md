# A5b 공통 비공개 조건 채점

사용/미사용 조건을 모르는 새 문맥에서 sample-A/B를 각각 채점한다. 조건 추측이나 우승자 선정이 목적이 아니다. reference.json의 해당 구간 사전 고정 atom과 두 관측 JSON/Markdown 및 그 evidence만 읽는다. 다른 pair/원본 trial/맵핑/스킬/legacy는 읽지 않는다. provenance 검증은 별도 validation으로 제공하며 내용 정확도를 뜻하지 않는다. 추가 decode/crop 생성은 금지. 이미 있는 기준답안/샘플 근거 PNG를 직접 열람할 수 있다.

기준 atom마다 correct/missed/wrong/avoidable_unknown 중 하나를 판정하고 원문 사건/근거를 짚는다. 의미가 같은 표현은 인정하고 철자·띄어쓰기·대소문자 차이만으로 뜻 왜곡 오류를 만들지 않는다. 같은 내용을 두 번 적어도 한 번만 인정한다. 정확한 AE 곡선 미상은 정상이나 관측 가능한 방향/순서/정성 감속의 기록 누락은 구분한다. genuine indeterminate unknown은 허용한다. H02-D08은 정성 크기 감속이며 원본 함수 미상과 구별한다. 기준에 없는 새 주장도 따로 검증한다.

정확도 분모는 결과에 적힌 모든 **중복 제거된 원자적 시각 사실 주장**이다. 문장/사건 수를 그대로 쓰지 말고, 한 사건의 위치·형태·문구·순서가 서로 검증되는 사실이면 분리한다. 같은 내용을 JSON과 Markdown에 적으면 중복이다. 미검수 범위/구현 가설/적절한 unknown은 단정 사실 분모에서 빼고 별도 기록한다. claims 배열에 id,claim,supported(true/false/null),evidence를 남긴다. 충분히 검사 못한 주장은 null로 두고 claimed_precision=null와 incomplete 판정한다. 참인 것으로 간주하지 않는다. 새 일반화/구현 확정은 원본으로 증명 불가면 오류다.

중대 오류는 원본/회사/대상/시각 혼동, 의미를 바꾸는 수치·단위·부정어·문구 순서, 근거 없는 이동·가감속·AE 구현 확정, 음성 미검수를 청취완료/무음으로 기재, 새 AI 결과를 사람 승인으로 기재. 타당한 시각 표현(회전하듯/가림/리빌)과 실제 AE 구현 확정은 구별한다. 중요한 반대근거가 없는데 불명확하다는 이유만으로 중대 오류로 과잉 처분하지 않는다. 다만 통과 입증 책임은 출력에 있다.

각 sample 결과: atom_results [{atom_id,tier,result,evidence}], claims [...], missing_count,wrong_count,avoidable_abstention_count,appropriate_unknowns [...], critical_errors [{claim,evidence}], metrics {core_correct,core_total,detail_correct,detail_total,supported_asserted_claims,total_asserted_claims,core_coverage,detail_coverage,asserted_claim_precision,avoidable_abstention_fraction}, scope_incomplete, gates_passed. core=100%,detail>=90%,precision>=95%,avoidable_unknown<=10%,critical=0,validation errors=0을 **각 sample**에 적용. 정수 ceil/floor로 판정하고 실패를 평균으로 지우지 않는다. null이면 미완료. 시간경계는 reference에 별도 boundary_seconds가 있는 경우에만 max(0,ref_start-pred_end,pred_start-ref_end)<=0.2 및 pred bracket 폭<=0.4. 이벤트 관측 span을 onset bracket으로 잘못 채점하지 않는다.

최대3분 안에 현재 확보한 채점 결과를 grading.json 및 grading.md에 저장한다. 시작/끝 UTC, AI review elapsed초, 읽은 이미지/파일, unresolved, tokens=null을 포함. 시간 내 미완료는 그대로 남긴다. 내용을 아는 주 실행자에게 답을 물어보거나 샘플을 수정하지 않는다. 사람 검수 시간은 측정하지 않았다고 적는다. 첫 분류 결과를 보존한다.

검수 공수 비교를 위해 reference/공통 메타데이터 읽기는 shared_review로, sample-A와 sample-B 각각의 본문·근거 대조와 채점은 sample_review로 나누어 clock 도구 시작/끝을 실제 기록한다. 병행하거나 한 시간을 반으로 나누어 배분하지 않는다. sample별 review_seconds를 기록하며 공유 시간은 별도로 둔다. 이 값은 AI 검수 경과시간이며 사람 실작업 시간이라고 부르지 않는다. 총3분 한도는 공통준비·양쪽검토·기록 모두 포함한다.
