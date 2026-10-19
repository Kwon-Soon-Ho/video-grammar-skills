# 전체 사례와 독립 패턴

## 무엇을 따로 번호화하는가

전체 사례의 원본·관측·전체 디자인·모션은 계속 보존한다. LAYOUT은 화면 구조, FLOW는 장면 전체의 전개, TEXT/CARD/TRANSITION/DETAIL은 독립적으로 다시 쓸 동작을 담는다. 사례의 `reuse_map`이 이들을 조합한다. 문구·색·시간 차이는 먼저 변형값으로 기록한다. 대상 관계나 동작 원리가 달라 별도 조건 검수가 필요한 경우 새 번호를 만든다.

## 개별 정의

새 정의 입력 필드: definition_version=video-pattern-definition-0.2, category, name, source, definition, applicability, counterexamples, status=draft, supersedes, derived_from.

- source:{case_id,source_sha256,observation_path,observation_sha256,claim_ids,unknown_ids}. 최초 상세 관측의 고정 파일과 해당 단위의 주장·미해결만 연결한다. 라이브러리 등록 전에 관측 파일을 저장하고 이후 수정은 새 파일로 보존한다.
- LAYOUT definition:{summary,canvas,groups,design_dimensions}. groups는 구성 영역과 관계를, design_dimensions는 hierarchy/alignment/spacing/typography/color/background/shapes의 상세 기록을 담는다. 모션 함수를 의무적으로 넣지 않는다.
- FLOW definition:{summary,stages,overlap_notes,stable_context}. stages:[{name,timing,claim_ids}]. 장면 전체의 순서·유지·겹침과 무엇이 계속 남는지를 기록한다. 실제 겹치는 과정을 완전 직렬로 만들지 않는다.
- TEXT/CARD/TRANSITION/DETAIL definition:{summary,target_role,phases,parameters,preserve_constraints}. phases:[{name,property,observed_change,claim_ids}]. parameters:[{name,status,value,unit_or_type}], status=observed/estimated/unknown. 미상의 값은 null. 원본 AE 값과 새 구현 파라미터를 혼동하지 않는다. 해당 동작과 무관한 열차 배경·주제 문구·전체 화면 배치를 의무적으로 넣지 않는다.
- applicability는 사용 조건, counterexamples는 반례 또는 미시험 사실이다. supersedes는 같은 정의의 교정 이전 번호, derived_from은 분리의 근원이 된 보존 항목 번호다. 분류 선택은 관측 사실이나 회사 공통 규칙 승인이 아니다.

`pattern_library.py add --library <library.json> --pattern <definition.json>`은 다음 번호를 배정한다. 기존 0.1 항목을 보존하며 0.2 라이브러리에 새 정의를 추가한다. 항목마다 콘텐츠 해시, 라이브러리마다 고정 스냅샷을 만든다. 다중 등록자는 한 라이브러리에 순차 접수한다.

`pattern_library.py select --library <snapshot.json> --id <PAT-...> --out <selection.json>`은 그 정의와 관련 원본 주장·근거·미해결만 꺼낸다. derived_from에 적힌 옛 전체 CARD를 함께 적용하지 않는다. 검색·추출은 구현 성공이나 새 장면의 적합성 검증이 아니다.

## 사례의 조합 기록

reuse_map:{case_id,layout_occurrence_ids,flow_occurrence_ids,detail_occurrence_ids,links,unresolved_ids}.

세 ID 목록은 `pattern_refs.id`를 가리킨다. 전체 사례 조합에는 LAYOUT과 FLOW를 연결하고, 필요한 독립 세부를 묶는다. 모든 인용은 정확히 한 역할에 속한다. 각 occurrence의 object_ids/current_claim_ids는 현재 사례의 범위다. 기존 패턴 원본의 대상 ID를 현재 장면에서 본 대상으로 간주하지 않는다.

links:[{from_id,to_id,relation,basis_kind,claim_ids}]. relation=contains/anchors_to/precedes/overlaps/accompanies. from/to는 occurrence ID다. basis_kind=observed/inferred. 예: 전체 흐름 contains UI 이동, 레이아웃 anchors_to UI 위치, UI 진입 overlaps 테두리 전개. 관측된 시간 관계와 설계상 조합 해석을 분리한다.

기계 검사는 역할·참조·해시·선후 모순을 검사한다. 실제 순서와 가독성, 무엇을 독립 패턴으로 나눌지는 원본과 사용 목적을 대조해야 한다. 분리한 각 정의에 남은 미해결을 전파하고 새 장면 비교가 없으면 재사용 적합성을 확정하지 않는다.


## 후보 검색

`pattern_library.py search --library <snapshot.json> --category DETAIL --query "경로 드론"`으로 번호·이름·정의·조건의 단어를 찾는다. 검색은 단순 키워드 교집합이며 의미 유사도·현재 장면 적합성 판정이 아니다. 필요한 결과를 select한 뒤 현재 대상·속성·좌표계·차이·미해결과 대조한다.
