from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE/'candidate/company-video-grammar-analyzer'
files={
'references/output-contract.md':'''# 분석 기록 0.2

JSON이 정본이며 MD는 생성 표시다. schema_version=video-observation-0.2, skill_version=0.1.0-draft.4. R4 DB나 과거 A3 형식과 구분한다. 과거 실패·고정 시험 기록을 변환해 덮어쓰지 않는다.

## 공통

필수: case_id, source:{path,sha256}, window_seconds:[시작,끝], method, document_mode, audio_reviewed, files_read, evidence, objects, observation_rows, claims, unknowns, discovery, layout, motion_groups, pattern_refs, review, handoff, limitations.

evidence:[{id,path,actual_seconds,role}]는 실제 읽은 원본 PNG 또는 검증된 RGB 무배율 크롭. role=within/context_before/context_after. 끝 제외 창을 지키고 실제 표시시각·현재 PNG 해시·원본 해시를 검증 카탈로그와 대조한다. ID는 각 목록 안에서 유일하다. 없는 ID나 다른 대상·속성의 근거를 빌리지 않는다.

## 대상·속성·주장

objects:[{id,name,parent,shape_description,required_properties,excluded_properties,identity}]

아홉 속성 identity/text/relation/position/size/shape/visibility/color/internal_state를 검토한다. required_properties에는 관찰할 속성을, excluded_properties:{속성:이유}에는 해당 없는 속성을 적는다. identity는 항상 요구한다. 확인 안 한 것을 제외하지 않는다. name은 중립적 이름이고 shape_description은 실제 보인 특징이다. identity:{status,label,candidates,claim_ids}의 status는 reviewed/unresolved. reviewed에는 이름과 observed 식별 주장이 필요하다. unresolved의 label은 null이고 후보는 문자열 목록이다.

observation_rows:[{id,object_id,property,time_seconds,review_state,change,evidence_ids,claim_ids,unknown_ids,reason}]

요구한 대상×속성의 행이 분석 구간 전체를 덮게 한다. 상태는 reviewed/unresolved/not_reviewed/not_applicable, change는 changed/unchanged/unknown/not_applicable. reviewed에는 같은 대상·속성의 주장과 근거가 필요하다. unresolved/not_reviewed에는 열린 unknown을 연결한다. not_applicable에는 이유를 적는다. 확실한 일부 사실과 아직 모르는 세부는 분리한다. 이 행 검사는 처음 발견 목록에서 빠진 대상을 알아내지 못한다.

claims:[{id,object_id,property,facet,time_seconds,statement,basis_kind,evidence_ids,content_review,easing?}]

한 주장은 한 대상·속성·판정. facet=identity/value/direction/order/easing/relation/presence. 같은 대상·속성·facet·구간은 하나로 정리한다. 겹친 구간의 의미 중복과 모순은 실제 내용 검수에서 다시 확인한다. basis_kind=observed/calculated/inferred, content_review=not_reviewed/supported/rejected/uncertain. observed/calculated에는 실제 근거를 연결한다. inferred는 원본 사실로 내보내지 않는다.

facet=easing일 때 easing:{classification,basis_evidence_ids,method,limitation}을 넣는다. classification=accelerate/decelerate/in_out/linear/unknown/not_applicable. 가감속 분류에는 서로 다른 실제 시각 3개 이상이 필요하다. 진행 중 변화율이 보이는지, 같은 대상·속성인지, 정지 도착만 본 것은 아닌지는 내용 검수 사항이다.

## 미해결·검수

unknowns:[{id,object_id,question,state,reason,required_basis_kind,next_probe,resolution_claim_ids}]. state=open/resolved/withdrawn/out_of_scope. open에는 이유와 다음 확인. resolved에는 요구 유형(observed/calculated/inferred)에 맞는 supported 해소 주장. withdrawn/out_of_scope에는 이유가 필요하고 해소 입증으로 세지 않는다.

discovery:{forward_evidence_ids,reverse_evidence_ids,unresolved_ids}: 시간순 관찰과 정착 화면 역추적의 실제 근거, 목록 간 미해결 차이. 비어 있으면 발견 검수 완료가 아니다.

review:{content_reviewed_claim_ids,claim_denominator_complete,remaining_scope}. 분모 완료는 모든 고유 주장에 supported/rejected/uncertain이 있고 검수 ID가 빠짐없을 때만 true다. 전부 검토와 무오류는 다르다. 코드 검사는 픽셀의 글자·개수·의미·방향을 판독하지 않는다. 사람 확인·회사 승인도 부여하지 않는다.

## 전체 디자인·모션·반복 패턴

[디자인과 패턴 기록](design-and-patterns.md)을 함께 읽는다. layout에는 전체 디자인을, motion_groups에는 전체 흐름과 세부 동작을 연결한다. 반복 장면은 pattern_refs로 첫 상세 기록을 인용하되 이번 장면의 차이와 근거를 남긴다. handoff는 null 또는 [판단 인계](judgment-handoff.md) 객체다.
''',
'references/design-and-patterns.md':'''# 전체 디자인과 반복 패턴

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
''',
'references/judgment-handoff.md':'''# 판단·재제작 인계

handoff:{purpose,information_relation,observed_claim_ids,preserve_claim_ids,open_unknown_ids,condition_candidates,implementation_options}.

purpose와 information_relation은 null 또는 {text,basis_kind,claim_ids}. 시나리오·제작자 확인 없이 의도를 확정하지 않는다. observed_claim_ids에는 observed/calculated 주장만, preserve_claim_ids에는 새 설계에서 보존할 특성의 주장 ID를 넣는다. 원본 관측의 검수 상태도 함께 전달한다.

condition_candidates:[{condition,reason,claim_ids,counterexample,validation_state}]. 조건은 문구 길이·요소 수·화면비·읽기 시간 등 실제 적용 쟁점에 연결한다. 반례 미시험이면 counterexample=null, validation_state=untested. 그 원본 한 사례에서 확인한 범위만 observed_case로 쓸 수 있다. 회사 공통 규칙의 승인은 여기서 만들지 않는다.

implementation_options:[{proposal,basis_kind:"inferred",claim_ids,verification_needed}]. 같은 렌더를 만드는 구현은 여럿이다. 원본 AE 키프레임·효과를 복원했다는 주장과 새 구현 제안을 분리한다. 실제 편집 결과·렌더에서 확인해야 할 내용, 새 문구·화면비로 바꿔 확인해야 할 내용을 적는다.

선택 순서는 필수 문구·정보 관계·가독성·동작 목적을 충족하는 내부 사례, 작은 변형, 기존 제작 기능, 필요한 새 표현이다. 맞지 않으면 다음 대안으로 넘어간 이유를 적는다. 요소 수나 후보 수의 최소화 자체를 목표로 삼지 않는다.

원본·시간 매핑·추출 설정·관측 판본이 같은 근거는 재활용한다. 새 목적과 조건의 적합성 검수는 다시 한다. 원본 재현 성공과 새 내용 재사용 성공은 따로 입증한다. 같은 품질이 확인된 비교에서만 공수 절감을 계산한다.
'''}
for relative,content in files.items():(ROOT/relative).write_text(content,encoding='utf-8')
decisions=json.loads((HERE/'decisions.json').read_text(encoding='utf-8-sig'))
decisions['decisions'].append({'id':'D2','kind':'user_record_density_choice','selected':1,'user_additions':['레이아웃의 전체 디자인 기록; 목적에 따라 기록 정밀도 판단','모션은 전체 흐름과 세부 모션 구분','첫 패턴 상세 분석 후 카테고리·번호 등록','반복 시 번호와 현행 근거·차이 연결로 재사용'],'interpretation_boundary':'원제작 의도 미확인 시 추론으로 표시; 패턴 등록은 회사 공통 문법 승인 아님'})
(HERE/'decisions.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2),encoding='utf-8')
print('references and user decisions written')
