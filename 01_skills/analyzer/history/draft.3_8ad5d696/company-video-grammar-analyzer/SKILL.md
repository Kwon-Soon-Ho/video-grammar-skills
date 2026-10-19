---
name: company-video-grammar-analyzer
description: Analyze rendered company videos into evidence-linked screen states, text, information relations and motion observations. Use for reference-video analysis, motion omission audits, and draft company video grammar records, including software UI demonstrations. Produces observations rather than AE project reconstruction or final company approval.
metadata:
  short-description: 회사 영상의 화면·문구·모션을 근거와 함께 분석
---

# Company video grammar analyzer

영상에서 보이는 사실을 재사용 가능한 분석 초안으로 만든다. 화면 구성만 설명하고 시간 변화를 생략하지 않는다. 현재 판본은 **0.1.0-draft.3**, 로컬 원본/추출 근거 분석 경로다.

## 입력과 근거

원본 경로·해시·분석 구간과 문서 유형(제작 전 원고/재구성 원고/없음)을 고정한다. 사용자가 준 구간 안에서 먼저 작업한다. 오디오를 실제로 듣거나 전사하지 않았다면 음성/싱크는 미검수다.

[근거 계약](references/evidence-and-records.md)을 읽고 시간·좌표·주장 범위를 지킨다. 기존 추출 로그와 PNG가 있으면 `scripts/evidence_catalog.py --logs <log...> --out <catalog.json>`으로 파일 해시·표시시각을 확인한다. 로컬 실행 문맥에서 제공한 검증된 제한 추출기를 사용해 부족한 구간을 보충한다. 이 스킬은 범용 디코더를 번들하지 않는다. 추출기가 없으면 제공된 근거의 범위에서 분석하고 미확보 부분을 적는다. 한 장만 보고 이동/이징을 확정하지 않는다.

## 관찰

[모션 관찰](references/motion-review.md)을 읽고 다음 세 범위를 따로 살핀다.

- 화면 전체: 상태/전환, 주요 대상, 문구, 정보 관계.
- 대상 주변: 작은 선·테두리·커서·빛·가림·잔상 등 주요 대상과 별도로 변하는 요소.
- 대상 내부: 화면 속 UI, 데이터, 선택 상태, 내부 그림/질감. 외곽이 멈췄다고 내부도 정지라고 기록하지 않는다.

시간순으로 한 번 훑은 뒤 정착 화면의 각 요소가 어떻게 만들어졌는지 역으로 추적한다. 두 관찰에서 목록이 다르면 해당 경계를 촘촘히 확인한다. 개요 시트에서 작은 요소를 못 읽으면 원본 크기 ROI를 보고, 보이지 않은 이유를 확인하기 전 ‘없음’으로 닫지 않는다. 시작·변화 중·종료와 중첩 표본을 연결한다.

대상마다 실제로 해당하는 위치, 크기, 형태/회전, 가시성/리빌, 색/광량, 내부 상태와 순서를 기록한다. 속성이 변하면 그 속성의 가감속도 확인한다. 적용하지 않는 속성을 억지 수치로 채우지 않는다. 외곽 이동과 내부 변화, 텍스트 크기와 주변 프레임 크기, 빛 이동과 밝기 변화를 분리한다.

Phase 00 지식이 제공되면 관련 ID와 정의를 조회하되 관측의 증거로 사용하지 않는다. 가속/감속을 모르면 원인을 적고 확인된 방향·존재·순서는 보존한다. 기록 누락과 판독 불가를 같은 것으로 처리하지 않는다.

## 기록과 종료

[출력 계약](references/output-contract.md)에 따라 `observations.json`과 사람이 읽을 `observations.md`를 저장한다. 추출 로그가 있으면 카탈로그를 생성한 뒤 `scripts/check_observations.py <observations.json> --catalog <catalog.json>`으로 구조와 원본·프레임·시각 연결을 검사한다. 카탈로그 없는 검사는 구조만 확인한다. 어느 검사도 시각 내용의 정답 판정이 아니다. R4 정본 DB로 자동 등록하지 않는다.

완료 전 아직 조사하지 않은 대상·속성과 증거 부족을 확인한다. ‘모두 확인’ 대신 검사한 시각 범위/표본/남은 불확실성을 보고한다. 사용자 질문은 조사 후 남은 쟁점만, 해당 화면과 구체 주장으로 제시한다. 이전 사용자 확인은 정확히 같은 주장·자료 범위에만 연결한다. AI의 새 발견은 AI 관측으로 남기며 회사 공통 규칙/제작 의도/AE 구현으로 승격하지 않는다.

저장 전 대상별 주장과 근거를 역대조한다. 근거 ROI에서 해당 대상의 특징이 실제로 보이는지, 가림 해소를 이동으로 쓰지 않았는지, 다른 대상의 숫자를 가져와 설명하지 않았는지 확인한다. 이 내용 점검은 JSON 검사로 대체되지 않는다.
