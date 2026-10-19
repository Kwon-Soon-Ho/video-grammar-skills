# 전체 디자인의 관측 밀도

첫 레이아웃 상세 기록이나 디자인 누락 보완 때 읽는다. 기존 7개 design_spec 차원을 유지하되, '넓다/굵다/프레임'만으로 재사용 결정을 할 수 없다면 아래 관계를 보강한다. 반복 사례는 기존 상세 기록과 현재 근거·차이를 연결한다. 모든 요소를 숫자로 재는 작업으로 확대하지 않는다.

## 기록할 관계와 선택적 측정

- **위계·영역:** 화면비, 주요 그룹의 범위와 비중, 초점과 정보 관계. 불규칙 물체의 외접 상자 비중을 실제 물체 점유 면적으로 부르지 않는다.
- **정렬·여백:** 무엇을 기준으로 정렬했는지, 그룹 사이/요소 안쪽의 여백, 화면 가장자리와의 관계. 투영된 3D의 중심과 설명 띠 중심을 무조건 같게 만들지 않는다.
- **글자:** 제목·설명·자막·지도 지명·로고의 역할, 가시 크기 관계, 굵기 구간, 줄/단락, 그림자·윤곽·배경과의 관계. 글자 ROI의 픽셀 높이는 폰트 크기 원값이 아니다. 로고를 일반 자막 폰트로 추정하지 않는다.
- **형태·선:** 바깥 선틀, 안쪽 판, 색 모서리, 분리 꺾쇠/화살촉, 연결선과 접점, 글자/빛의 범위를 나눈다. 가는 선과 발광까지 포함한 외관 두께를 원본 stroke 값으로 바꾸지 않는다.
- **색·배경·겹침:** 기저·질감·장식·공간/지역 강조·모델/카드·문구·자막의 보이는 겹침을 적는다. 비쳐 보인다는 사실에서 opacity %, blend mode, 원본 레이어 수를 역산하지 않는다.

재사용에 영향이 큰 관계부터 수치화한다. 예를 들어 전체 영역 비율, 문구와 띠의 좌우 여백, 설명판/카드 폭 비율, 글자의 가시 높이 관계다. 각 숫자에 **시점, 원본 좌표계/단위, 측정/추정, 방법, 오차, 왜 필요한지**를 연결한다. 가시 경계를 손으로 읽었다면 estimated다. 정밀하지 않아도 전체 구성 설명은 남기고, 정확한 원제작 설정은 unknown으로 둔다. 의도·구현 제안은 inferred다.

## 상태 차이를 고정 디자인으로 오인하지 않기

등장/강조/재배치/정착 중 어느 시점의 값인지 적는다. 같은 그룹의 카드·문구·프레임이 함께 이동해도 크기까지 같이 변한다고 가정하지 않는다. 비교 시 고정 배경/다른 그룹을 기준으로 부모 이동과 하위 대상의 크기·내부 변화를 따로 살핀다. 두 시점의 크기 차이를 확인한 것은 변화의 정확 시작·가감속을 확인한 것과 다르다. 추가 관측이 필요한 속성은 열린 쟁점으로 인계한다.

## 혼합 정밀도의 보강 파일

한 design_spec 설명 안에 정성 관측과 여러 수치가 섞이면 `design-details.json`을 만들고 observations.json의 `design_details:{path,sha256}`로 연결할 수 있다. 필수 필드:

- schema_version=design-details-0.1, case_id, source:{path,sha256}, base_record:{path,sha256}, pattern_ids
- scope:{record_window_seconds,snapshot_seconds,new_continuous_video_coverage:false,content_status,limits}
- frames:[{id,path,sha256,canvas:[W,H],seconds,crops:[{path,sha256,box_ltrb}]}]
- regions:[{id,frame,bbox_ltrb,precision:estimated|measured,basis_kind,coordinate_system,method,error_px,description,reuse_reason,normalized_xywh,bbox_canvas_area_percent}]
- typography:[{id,frame,roi_ltrb,bbox_ltrb,visible_glyph_height_px,text_scope,precision,method,error,crop_path,crop_sha256}]
- relations:[{id,region_ids,value,unit,basis_kind,precision,method,error,meaning}]
- dimensions:{hierarchy,alignment,spacing,typography,color,background,shapes}의 각 값은 {description,basis_kind,precision}
- layers:[보이는 겹침 설명], unknowns:[미확정], implementation_hypotheses:[{basis_kind:inferred,proposal,reason,verification_needed}]

`scripts/check_design_details.py <design-details.json>`은 연결·해시·좌표·비율의 일관성을 검사한다. 연결된 경우 check_record도 이를 검사한다. 영상 내용의 정확성이나 전체 디자인 발견 완료를 판정하지 않는다. 같은 패턴의 세부 설명이 늘어났다는 이유로 새 번호를 만들거나 과거 패턴 정의를 덮어쓰지 않는다. 보강 기록은 기존 정의와 판본·차이를 연결한다.
