# 전체 디자인과 반복 패턴

## 기록 밀도

레이아웃은 전체 디자인을 기록한다. 화면비, 전체 구도·영역·그룹·위계·정렬·여백, 문구·서체 특징·크기 관계, 색·배경·형태·아이콘·강조·겹침을 포함한다. 작은 요소라는 이유로 삭제하지 않는다. 값의 정밀도는 무엇을 전달하고 재사용할지에 따라 선택한다. 전체 요소 기록과 모든 픽셀의 정밀 측정은 다르다. 기준을 정하기 어려우면 관계와 비율을 먼저 적고 수치·서체·색 값의 추정/측정/미상·단위·좌표계를 명시한다.

원래 제작 의도가 문서·제작자 확인에 없으면 관측에서 해석한 목적을 inferred로 둔다. 목적 해석을 이유로 눈에 보이는 구성·동작을 생략하지 않는다.

layout:{canvas,states,unresolved_ids}. canvas={aspect_ratio,coordinate_system}. states:[{id,time_seconds,evidence_ids,composition,element_object_ids,claim_ids,design_spec,unresolved_ids}]. design_spec에는 hierarchy/alignment/spacing/typography/color/background/shapes를 각각 기록한다. 각 값은 {description,basis_kind,precision,claim_ids}다. precision=measured/estimated/qualitative/unknown. 측정한 경우 value/unit/coordinate_system/method/error를 추가한다. unknown은 관련 미해결 ID를 states.unresolved_ids에 연결한다. 요소의 존재·위치·색·텍스트는 해당 객체 주장과 연결한다. 한 상태의 전체 대상 목록과 원본을 대조한다.

motion_groups:[{id,level,name,time_seconds,object_ids,claim_ids,pattern_occurrence_ids}]. level=flow/detail. flow는 장면 전체에서 무엇이 먼저·함께·나중에 움직이며 어떻게 상태가 바뀌는지 기록한다. detail은 텍스트/카드의 등장·작은 선·내부 상태·빛·가감속 등 개별 동작을 기록한다. 동작이 없을 때도 확인한 정지 상태를 적고 detail 생략 이유를 limitations에 남긴다. 흐름만 설명하고 세부를 지우거나 세부 목록만 나열해 순서를 잃지 않는다.

## 첫 기록과 반복 기록

처음 발견한 패턴은 전체 구도와 흐름·세부까지 상세 기록한다. 사용자가 원하는 카테고리와 번호는 TEXT(텍스트 등장), CARD(카드 등장), TRANSITION(장면 전환), FLOW(전체 흐름), DETAIL(세부 효과), LAYOUT(레이아웃)로 시작한다. 예: PAT-TEXT-0001. 실제 사례 없이 빈 패턴을 채우지 않는다. 새 범주는 필요가 생길 때 추가한다.

패턴 라이브러리는 JSON 정본, 본문과 해시를 가진 개별 항목으로 관리한다. scripts/pattern_library.py add --library <파일> --pattern <상세항목.json>은 다음 번호를 배정하고 기존 항목을 덮어쓰지 않는다. 수정·반례로 본문이 달라지면 새 항목 번호로 등록하고 supersedes에 이전 ID를 연결한다. 번호는 해당 라이브러리 안에서 유일하며 다른 라이브러리의 같은 번호를 혼용하지 않는다.

상세항목 필수: category,name,source:{case_id,source_sha256,observation_path,observation_sha256,claim_ids},design_spec,motion_spec,applicability,counterexamples,status,supersedes. status는 draft만 등록한다. design_spec에는 레이아웃/타이포/색/관계를, motion_spec에는 흐름/세부/타이밍/속성별 변화와 미확정을 기록한다. applicability에는 무엇을 보존하며 언제 쓸지, counterexamples에는 반례 또는 아직 시험하지 않았다는 사실을 적는다. 각 세부는 원본 관측·근거로 돌아갈 수 있어야 한다. 등록 도구는 의미 정확성이나 상세함을 자동 보증하지 않는다.

반복 기록 pattern_refs:[{id,pattern_id,pattern_sha256,library_path,library_sha256,object_ids,current_claim_ids,match_status,differences,unverified_dimensions}]. match_status=confirmed/candidate/mismatch. confirmed는 이번 장면 근거를 대조하고 미검증 차원이 없을 때만 사용한다. 문구·크기·요소 수·화면비·시간·순서·가감속·내부 동작·겹침을 비교한다. 차이는 differences에 적고 실제로 본 주장만 current_claim_ids에 연결한다. 반복이므로 안 본 것을 봤다고 쓰지 않는다. confirmed는 회사 문법 승인이나 효과 검증을 뜻하지 않는다.

번호·카테고리·이름으로 먼저 찾고 필요한 상세 원본만 읽는다. 패턴 파일이나 원본 관측 해시가 달라지면 비교를 다시 한다. 이전 라이브러리 해시를 쓴 반복 기록은 해당 스냅샷을 보존하며 새 파일 해시에 몰래 치환하지 않는다. 라이브러리는 채택된 회사 규칙 DB와 구분한다.
