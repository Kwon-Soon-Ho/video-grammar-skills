# 분석 기록 0.2

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
