# 전체 디자인과 반복 패턴

## 기록 밀도

레이아웃은 전체 디자인을 기록한다. 화면비, 전체 구도·영역·그룹·위계·정렬·여백, 문구·서체 특징·크기 관계, 색·배경·형태·아이콘·강조·겹침을 포함한다. 작은 요소라는 이유로 삭제하지 않는다. 값의 정밀도는 무엇을 전달하고 재사용할지에 따라 선택한다. 전체 요소 기록과 모든 픽셀의 정밀 측정은 다르다. 기준을 정하기 어려우면 관계와 비율을 먼저 적고 수치·서체·색 값의 추정/측정/미상·단위·좌표계를 명시한다.

원래 제작 의도가 문서·제작자 확인에 없으면 관측에서 해석한 목적을 inferred로 둔다. 목적 해석을 이유로 눈에 보이는 구성·동작을 생략하지 않는다.

layout:{canvas,states,unresolved_ids}. canvas={aspect_ratio,coordinate_system}. states:[{id,time_seconds,evidence_ids,composition,element_object_ids,claim_ids,design_spec,unresolved_ids}]. design_spec에는 hierarchy/alignment/spacing/typography/color/background/shapes를 각각 기록한다. 각 값은 {description,basis_kind,precision,claim_ids}다. precision=measured/estimated/qualitative/unknown. 측정한 경우 value/unit/coordinate_system/method/error를 추가한다. unknown은 관련 미해결 ID를 states.unresolved_ids에 연결한다. 요소의 존재·위치·색·텍스트는 해당 객체 주장과 연결한다. 한 상태의 전체 대상 목록과 원본을 대조한다.

motion_groups:[{id,level,name,time_seconds,object_ids,claim_ids,pattern_occurrence_ids}]. level=flow/detail. flow는 장면 전체에서 무엇이 먼저·함께·나중에 움직이며 어떻게 상태가 바뀌는지 기록한다. detail은 텍스트/카드의 등장·작은 선·내부 상태·빛·가감속 등 개별 동작을 기록한다. 동작이 없을 때도 확인한 정지 상태를 적고 detail 생략 이유를 limitations에 남긴다. 흐름만 설명하고 세부를 지우거나 세부 목록만 나열해 순서를 잃지 않는다.

## 첫 기록과 반복 기록

전체 디자인과 흐름·세부는 사례 관측에 보존한다. 전체 사례를 한 CARD 패턴에 몰아넣지 않고 [패턴 조합](pattern-composition.md)의 독립 정의와 사례 연결을 사용한다. 처음 발견한 각 단위는 대상·상태·속성·순서·시간 근거·조건·미해결을 상세 기록한다. 번호를 나누는 기준은 독립 재사용 가능성이다. 문구·색·간격이 조금 다르다는 이유만으로 새 단위로 쪼개지 않는다.

카테고리: LAYOUT(전체 디자인), FLOW(전체 모션), TEXT(텍스트 등장·교체·퇴장), CARD(카드/UI 동작), TRANSITION(장면 전환), DETAIL(독립 세부 효과). 첫 번호는 해당 라이브러리의 다음 빈 번호로 배정한다. 기존 번호를 다른 뜻으로 바꾸지 않는다.

반복 기록 pattern_refs:[{id,pattern_id,pattern_sha256,library_path,library_sha256,object_ids,current_claim_ids,match_status,differences,unverified_dimensions}]. match_status=confirmed/candidate/mismatch. confirmed는 현재 자료에서 해당 범위를 대조했고 미검증 차원이 없을 때만 사용한다. 문구·크기·요소 수·화면비·시간·순서·가감속·내부 동작·겹침을 비교하고 차이와 미검증 부분을 남긴다. confirmed는 회사 승인이나 사용 효과 검증이 아니다.

`library_path`는 고정 스냅샷을 가리킨다. 스냅샷과 원본 관측이 달라지면 다시 확인한다. 과거 통합 CARD 항목은 이력으로 보존하고 새 분리 정의의 derived_from으로 연결한다. 과거 라이브러리를 자동 갱신하거나 과거 분석의 형식을 덮어쓰지 않는다.
