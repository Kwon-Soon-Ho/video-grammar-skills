# 선택 경로: 지식 연결 부속 색인 0.1

기계 검색/DB 연결 요청에만 사용한다. 전체 디자인 수집 MD를 대체하거나 R4통합v0.2에 자동 등록하지 않는다. 관측 MD/이미지는 보존하고 이 JSON은 개념·단위·사용처·검토 연결의 편집 원본이다. 생성 표시/색인을 수정한 뒤 원본이 자동 갱신됐다고 주장하지 않는다.

필수 루트: `schema_version: video-knowledge-links-0.1`, `record_id`, `version`, `source:{sha256,duration_seconds}`, `source_records`, `evidence`, `claims`, `units`, `facets`, `knowledge_links`, `uses`, `composition_links`, `events`, `event_links`, `reviews`, `unknowns`, `limitations`, `company_approved:false`, `canonical_registered:false`.

모든 목록 ID는 해당 목록에서 유일하다. 근거 파일/기록 경로는 부속JSON 기준 상대경로 또는 절대경로다. source_records/evidence는 실제 파일의 sha256을 연결한다. source_records `{id,path,sha256,role}`. evidence `{id,path,sha256,time:{start,end},kind}`. 정지 한 점은 start=end; 표본 모음 창은 사용한 실제 범위이며 연속 재생 시간으로 계산하지 않는다.

claims `{id,text,basis_kind,evidence_ids,source_record_ids}`. basis_kind=observed/calculated/inferred. 원본 관측을 재사용하면 해당 기록과 표본을 연결하고 이번 새 관측과 구별한다. 계산이면 방법/단위/오차를 text 또는 별도 필드에 보충한다.

units `{id,kind,title,observation_status,definition_version,summary}`. kind=case/layout/component/visual_profile/flow/detail. observation_status=observed_static/observed_sampled/unobserved. definition_version은 기존 정의의 판본 또는 이번 지역 후보 판본이다. 이름이 유사해도 회사 정본 ID로 만들지 않는다.

facets `{id,unit_id,domain,name,description,basis_kind,claim_ids}`. domain=information/screen/visual/motion. 격자와 정보유형을 따로 기술하며 타입/색/재질/층의 역할을 묶는다. 수치가 필요하면 precision/unit/value/method/error를 보충한다. unknown 정밀값은 null로 두고 이유를 남긴다.

knowledge_links `{id,unit_id,concept_id,relation,basis_kind,claim_ids,rationale}`. relation=classified_as/review_relevant/evaluated_against. 분류/검토관련성은 inferred다. evaluated_against에는 같은 단위·항목의 review 행이 실제 있어야 한다. 용어 태그를 관측 사실/원칙 효과로 바꾸지 않는다.

uses `{id,definition_id,case_unit_id,time,evidence_ids,claim_ids,differences,unverified,conditions}`. conditions는 `{text,validation}`이고 validation=untested/observed_case_only/tested_elsewhere. 이번 한 사례만으로 다른 화면비/새 내용의 검증을 만들지 않는다. 정의의 전체 ID/판본과 현재 사용처가 왕복돼야 한다.

composition_links `{from,to,relation,basis_kind,claim_ids}`의 from/to는 unit 또는 use ID이며 relation=contains/anchors_to/precedes/overlaps/accompanies. 관측 동반과 설계 조합 해석을 구분한다. 시간적 인과는 선후와 다르다.

events `{id,unit_id,title,status,time,claim_ids,start_bounds?,end_bounds?}`. status=observed_sampled/unobserved. 경계는 마지막 미발생~첫 발생 구간이며 정확 시각이 아니다. event_links `{from,to,relation,basis_kind,claim_ids}`, relation=precedes/overlaps/continues_after/accompanies. 숫자 정착과 도상 완성의 시차를 보존한다. 미관측 단위/사건은 관측된 모션 검색에서 제외한다.

reviews `{id,unit_id,criterion_id,status,reason,evidence_ids,claim_ids,reviewer,scope,next_probe}`. status=pass/fix/hold/not_applicable/not_reviewed. 실제 원본 재검수인지 기존 기록과의 일관성 검토인지 scope에 명시한다. pass/fix에는 실제 근거/주장이, hold/not_reviewed에는 다음 확인이 필요하다. 회사 승인/일반 효과와 무관하다.

unknowns `{id,unit_id,question,impact,next_probe}`. 목록이 비었다는 것만으로 미상 없음/전편 완료를 판정하지 않는다. limitations에 관측 방식·미확보/미검수·음성·반복/동일자산/외부 적용 시험 범위를 적는다.

기계 검사는 위 연결과 범위를 확인한다. 파일 해시는 지식 내용/시각 진실성/권리를 증명하지 않는다. 상세 하위 필드 추가는 허용하며 스크립트가 해석하지 않는 데이터의 의미 검수는 별도다.
