from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json, hashlib, difflib, re
from urllib.parse import quote

WS = Path(__file__).resolve().parents[2]
PROJECT = Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
WORK = WS / 'tmp' / 'roadmap-update-20261016'
STAGE = WORK / 'staged'
BEFORE = WORK / 'before'
STAGE.mkdir(parents=True, exist_ok=True)
BEFORE.mkdir(parents=True, exist_ok=True)
NOW = datetime.now(ZoneInfo('Asia/Seoul')).isoformat()
BATCH = '2026-10-16_수정방향_로드맵과A5反映'.replace('反映', '반영')
NOTICE_REL = 'Phase 01-A/00_진행안내/23_수정방향과_A5계획_현재안내.json'
A5_REL = 'Phase 01-A/00_진행안내/22_01-A5_진행계획.md'
MATRIX_REL = '00기획/08_수정방향_단계별반영.md'
REVIEW_REL = f'작업 보고서(pdf)/02_중요검수기록/Phase 01-A/{BATCH}/계획변경_검토기록.md'
BACKUP_REL = f'Phase 01-A/backup/{BATCH}'
changes = []

def digest(b): return hashlib.sha256(b).hexdigest()
def read(rel): return (PROJECT/rel).read_text(encoding='utf-8-sig')
def swap(text, old, new):
    assert text.count(old) == 1, (old[:100], text.count(old))
    return text.replace(old, new, 1)
def section(text, start, end, replacement):
    a=text.index(start); b=text.index(end, a)
    return text[:a] + replacement.rstrip() + '\n\n' + text[b:]
def add(rel, content):
    target=PROJECT/rel
    old=target.read_bytes() if target.exists() else None
    if old is not None:
        saved=BEFORE/rel; saved.parent.mkdir(parents=True,exist_ok=True); saved.write_bytes(old)
    encoded=(content.rstrip()+'\n').encode('utf-8')
    dest=STAGE/rel; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(encoded)
    changes.append(dict(relative_path=rel,action='edit' if old is not None else 'create',
                        expected_before_sha256=digest(old) if old is not None else None,
                        after_sha256=digest(encoded),staged_path=str(dest),
                        original_path=str(target)))

matrix = '''# 修正方向的阶段反映'''.replace('修正方向的阶段反映','수정 방향의 단계별 반영') + '''

2026-10-16 · 계획 반영 v1.0

기존 분석 스킬과 검증 기록은 유지한다. 이번 보완은 A5에서 분석의 신뢰성과 검수 부담을 확인하고, 01-B에서 재사용 조건과 반례를 정리하며, 02에서 새 기획의 선택 품질과 제작 가치를 검증하는 데 적용한다.

## 유지하는 검증 결과

| 근거 | 유지할 결과 | 적용 범위 |
|---|---|---|
| A1 | 고정 합성 진단 최초 16/17, 보완 후 18/18 | 도구·시간·좌표 처리의 제한된 진단. 실영상 인식 점수로 환산하지 않음 |
| A2 | 사용자 확인·정정과 중립 재시험의 기존 기록 | 해당 자료·주장 범위에 연결. 이후 AI 발견을 사람 확인에 합치지 않음 |
| A3 | draft.2 초안과 선택 7구간의 결과, 두 구간 보완·재시험 | 나머지 5구간의 최초 결과와 UI의 AI 참고 기준 구분을 보존 |
| A4 | 5 MP4·4자료 묶음·6과제·7원본 구간, draft.3 보완 | 내용 문제 3종과 검사 허점 1종의 최초 실패·재시험·보정 이력 유지 |
| A4 보조 검사 | 코드 동작 검사 23개와 원본·시각·크롭 연결 검사 | 시각 인식 정확도나 사용자 이해도 평가와 분리 |

A4의 G·싱글·듀얼 3구간은 새 문맥에서 재시험했다. 추가로 발견한 정착·감속 문제는 근거 재대조와 보정으로 처리했다. 최종 통합 draft.3으로 7구간 모두를 새로 반복한 결과로 바꾸지 않는다. 기존 결과는 회귀·개발 근거이며, 이번 수정으로 취소하거나 새로운 별도 확인 표본으로 다시 세지 않는다.

## 지금 추가로 검증할 항목과 후속 단계

| 항목 | A5에서 확인 | 01-B에서 보완 | 02와 실제 제작에서 보완 |
|---|---|---|---|
| 고정 판본과 재현성 | 최종 스킬·참조·추출기·과제 판본을 고정하고 반복 결과 비교 | 승인 문법에 사용한 분석 판본 연결 | 기획 명세와 구현 결과의 판본 연결 |
| 누락과 과잉 단정 | 등장·유지·퇴장, 전후 문구, 대상별 변화, 정착과 가감속의 근거를 별도 자료에서 대조 | 어떤 관측이 문법 후보를 지지하는지 구분 | 선택 이유가 실제 화면·시간 구성에 드러나는지 확인 |
| 관측과 해석 | 기존 observations의 근거·hypotheses·미확정을 유지해 의도 단정 차단 | 전달 목적·정보 관계·선택 이유에 근거 수준과 확인 질문 연결 | 새 브리프에 대한 표현 제안과 원제작 의도 구분 |
| 적용 조건과 반례 | 기존 기록만으로 확인 가능한 제약·미상을 인계. 새로운 의미 판단 엔진은 만들지 않음 | 정보량·요소 수·문구 길이·시청 환경별 사용·제외 조건과 반례 구성 | 새 조건에 맞는 후보 선택과 부적합 후보 제외 검증 |
| 분석 깊이 | 문법 추출에 필요한 구조·시간 관측 유지, 조건부 정밀 측정과 중단 사유 기록 | 재사용 판단에 필요한 상세 수준 결정 | 장면 중요도에 따라 표현 탐색·검수 자원 배분 |
| 공수와 비용 | 이번 실행의 추출·추가 관찰·수정·검수 시간과 노출되는 사용량 기록 | 태깅·검토·검색·유지 부담 기록 | 기획부터 납품·수정·지원까지 총 공수와 실제 비용 비교 |
| 공통 명세 | 기존 분석 ID를 다음 기록에서 참조할 수 있는지 점검 | 사례·문법·제약 연결과 조회 확인 | 공통 제작 명세를 실제 실행 도구에 전달하고 변경 시험 |

## A5의 종료 범위

A5는 허용한 자료·구간·분석 목적에서 기록이 신뢰할 만한지 확인한다. 전체 영상·음성, 회사 주장의 진위, 원본 AE 키프레임 복원은 현재 기본 범위에 추가하지 않는다. 무문서 입력은 정상 경로로 유지하고 미검수 음성은 무음과 구분한다.

작업 등급은 사실 정확성의 등급이 아니다. 필수 문구·수치·관계·기본 가독성은 공통으로 지키며, 표현 탐색과 미세 조정의 자원 배분은 02에서 실제 제작 결과와 함께 검증한다. 원제작 공수는 MP4에서 역산하지 않는다.

## 01-B의 최소 산출물

대표 표현 3종 내외를 시작 후보로 삼되 새 완료 개수 기준으로 강제하지 않는다. 각 후보는 분석 ID, 전달 목적, 정보 관계, 레이아웃·모션 기능, 적용 조건, 제외 조건·반례, 근거 수준, 검수 범위·판본을 연결한다. 기존 분류와 ID를 재사용하고 관측 JSON과 문법 제안을 같은 사실로 합치지 않는다.

외형은 비슷해도 관계가 다른 입력을 조회에 넣어 부적합 사례가 제외되는지 확인한다. 결과가 없으면 없음으로 돌려준다. 회사 공통·프로젝트 한정·단일 예·외부 원칙을 구분하고 제작자 확인이 없는 의도는 해석 후보로 남긴다.

## 02의 최소 산출물

Scene Planner·Scene Composer·Motion Director의 역할을 유지한다. 새 브리프에 적합한 화면·시간 후보와 제외한 대안, 적용 문법, 선택 이유를 공통 제작 명세로 전달한다. 기본 재사용·선별 맞춤·대표 표현 탐색은 장르 고정 등급보다 장면별 자원 배분안으로 시험한다.

일반 AI, 회사 문법 적용, 필요 시 선별 Taste 적용을 같은 조건에서 비교한다. 문구·수치·요소 수·화면비 변경과 다른 프로젝트 전이를 포함하고, 최초 생성부터 수정·검수·지원·유지까지 측정한다. 한 실제 제작 경로에서 효과를 확인한 뒤 활용 환경을 넓힌다.

## 현재 읽을 근거

- [전체 로드맵](00_최종_파이프라인_계획.md)
- [A5 진행계획](<../Phase 01-A/00_진행안내/22_01-A5_진행계획.md>)
- [A3 결과](<../Phase 01-A/05_결과보고/13_01-A3_분석스킬_7구간시험_결과.md>)
- [A4 결과](<../Phase 01-A/05_결과보고/14_01-A4_다른영상_확대시험_결과.md>)
- [수정 기획안 v6](<C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기/output/기획수정_20261016/AI_영상_기획제작_스킬시스템_수정기획안_v6.pdf>)

이번 사용자 요청은 로드맵과 A5 계획에 수정 방향을 반영하는 범위다. A5 실험 실행·수치 기준 확정·잠금 자료 선정·01-B와 02 착수는 이 문서 저장으로 수행되지 않는다.
'''
add(MATRIX_REL,matrix)

a5 = '''# Phase 01-A5 진행계획

2026-10-16 · v1.0 · 계획 반영 완료 · 실제 확인 시험 미실행

A4의 완료 결과와 수정 기획안 v6를 바탕으로, 고정 판본의 분석 결과를 별도 자료에서 확인한다. 이미 검증한 구간의 결과는 유지하고 남은 반복성·일반화·기권 적절성·검수 부담을 확인한다. A5a에서 시험 조건을 정한 뒤 A5b에서 고정 조건으로 실행한다.

## 유지할 기준과 이번에 달라진 점

현재 스킬은 `0.1.0-draft.3`이다. A4의 선택 7구간 충족과 보조 검사 23개 통과, 최초 실패와 재시험·보정 기록을 그대로 보존한다. 이미 맞게 확인한 항목을 새로운 해석·비용 필드를 채우기 위해 처음부터 다시 분석하지 않는다.

이번 보완은 분석 목적과 필요한 깊이, 미확정 판단의 근거, 실제 검수·수정 부담을 시험 설계에 연결하는 것이다. 기존 SKILL·observations 형식과 과거 채점 기준은 변경하지 않는다. 새로운 의도 해석·품질 등급·제작비 필드를 관측 사실에 강제로 채우지 않는다.

## A5a에서 고정할 것

| 고정 대상 | 정할 내용 | 실행 전 남길 기록 |
|---|---|---|
| 후보 판본 | draft.3 SKILL·참조·보조 검사기, 제한 추출기·런타임과 과제 문구 | 파일 해시·실행 환경·노출되는 모델 정보. 미제공 버전은 미상 |
| 분석 목적 | 기본은 문법 추출용 구조·시간 관측. 정밀 수치 측정은 필요한 구간만 | 필수 대상·속성과 분석 범위, 정밀 측정 요청 이유 |
| 자료와 노출 | 프로젝트 단위 별도 자료, 기존 개요·문서 열람까지 포함한 노출 이력 | 개발·별도 확인 구분과 파일·구간·노출 목록 |
| 기준과 검수 | 필수 사건·주요 문구·경계 범위·근거 오류·기권 처리 | 모델 출력과 분리한 기준 초안, 기준의 작성자·근거·잠금 시점 |
| 비교 조건 | 스킬 없음과 고정 스킬 적용, 공통 기본 프레임과 같은 추가 관찰 정책 | 도구·프롬프트·자원 한도·실제 추가 표본과 예외 |
| 반복과 자원 | 표본·원본별 구간·반복 수, 보강 추출·검수의 중단 조건 | 선택한 시험안과 실제 한도. 이번 계획만으로 숫자를 확정하지 않음 |

### 시험 규모 제안

기존 별도 확인 후보는 자료014 TOVA 홈페이지와 자료011 K-GEO다. A4 결과상 이번 분석에 사용하지 않았으며, 실제 A5 선정 전 다른 채팅·문서·프레임의 노출도 다시 확인한다. 현재 후보 영상·시나리오·프레임은 열거나 잠금하지 않는다.

| 안 | 비교 실행 규모 | 장점과 한계 |
|---|---|---|
| A 추천 | 2프로젝트 × 프로젝트당 2구간 × 2반복 × 2비교군 = 16실행 | 무문서와 문서 연결 경로, 반복성의 균형. 소규모 확인 범위 |
| B 축소 | 2프로젝트 × 프로젝트당 1구간 × 2반복 × 2비교군 = 8실행 | 검수 부담 감소. 장면·모션 다양성의 확인 범위가 좁음 |
| C 확대 | 3프로젝트 × 프로젝트당 2구간 × 3반복 × 2비교군 = 36실행 | 다른 유형과 반복을 넓힘. 세 번째 프로젝트와 추가 자원 필요 |
| D 기준 정리만 | 별도 자료 실행 0건 | 후보 판본·평가·비용 기록 방식까지만 정하고 실험은 후속 진행 |

2비교군은 일반 분석과 동일 도구를 사용하는 스킬 적용 분석이다. 위 수는 실제 분석 실행 수이며 구간이나 독립 프로젝트 수와 구분한다. 알려진 사례의 표적 회귀와 보조 코드 검사는 위 별도 자료 실행 수에 넣지 않는다. A5 실행 범위를 정할 때 이미 합의된 값이 있으면 재사용하고 미정 값만 확인한다.

### 기존 자료의 제한된 회귀

A4는 최종 통합 draft.3으로 전 구간을 새 문맥에서 반복하지 않았다. 필요하면 기존 G 퇴장·싱글 자막·듀얼 자막과 정착 구별의 3구간만 최종 판본으로 확인하는 안을 사용한다. 이는 새 판본의 회귀 확인이며 과거 A4 결과의 취소나 미노출 성능 시험이 아니다.

회귀로 스킬을 수정하면 후보 판본과 해시를 다시 고정한 후 별도 확인 시험에 들어간다. 정밀 추적이나 다른 과거 구간의 전수 재시험은 새로운 오류·변경 영향이 있을 때만 추가한다.

## A5b에서 추가로 확인할 항목

| 항목 | 관측할 결과 | 오류와 미확정 처리 |
|---|---|---|
| 상태·동작의 누락 | 등장·중간 변화·유지·퇴장·잔존, 전체·주변·내부 상태 | 작은 요소가 표본에 없으면 추가 근거를 확인한 후 없음·미확정을 구분 |
| 문구와 대상 연결 | 바로 전후 문구·단위·대상별 수치와 각 시각의 근거 | 앞 장면 문구나 다른 대상 수치를 빌린 설명은 내용 오류 |
| 가감속의 근거 | 움직이는 동안 두 구간 이상의 변화율을 비교할 근거 | 정지 도착만 확인되면 정착은 기록하고 이징은 미확정 |
| 원본과 변형판 | 실제 원본·시각·PNG·크롭과 장면별 대응 | 같은 초·유사 화면·확대 비율만으로 원본이나 상태를 대체하지 않음 |
| 기권의 적절성 | 확인한 방향·순서와 모르는 속성을 분리 | 단순 누락과 근거 부족을 구분. 모든 필수 사건의 기권으로 통과하지 않음 |
| 판본의 반복성 | 고정된 후보와 중립 과제의 반복 결과 간 누락·오탐·기권 차이 | 단회 성공을 안정성으로 확정하지 않음 |
| 인계 가능성 | 원본→관측 주장→근거·미확정→문법 후보 참조의 연결 | R4 등록·회사 문법 승인은 수행하지 않고 기존 ID와 매핑 공백만 확인 |
| 검수 자원 | 실제 추가 관찰·수정·근거 대조에 든 공수와 원인 | 과거 미기록 시간·토큰과 원영상 제작비는 생성하지 않음 |

필수 상태·방향·순서 검수는 유지한다. 정밀 곡선·좌표 추적은 선택 질문을 해결할 때 추가한다. 이 구분은 검수 생략이나 오분석 허용 기준이 아니다.

## 판정과 기록

기존의 구조적 오류 0·치명적 근거 오류 0 원칙을 유지한다. 숫자·부정어·대상 혼동으로 뜻을 바꾸거나 없는 관측을 단정하면 미해결 상태로 인계하지 않는다. 최초 오류 결과는 보존하고 보완 후 결과를 별도 판본으로 남긴다.

검출·누락·오탐·기권은 사전에 정한 필수 사건 수와 함께 보고한다. 근거 부족으로 이징을 미확정 처리한 사건도 방향·순서 등 확인 가능한 부분은 평가한다. 비적용은 이유를 기록해 분모 제외의 근거를 남긴다. 정확도·기권 허용률·실영상 경계 오차의 수치 기준은 A5a에서 정하며 현재 값은 미정이다.

합성 교정의 ±1프레임 목표를 희소 프레임 실영상 전체에 강제하지 않는다. 실영상 기준은 원본 PTS의 확인 구간과 경계 불확실성을 사용한다. 독립 검수자 없이 작성자가 채점했다면 그 범위로 보고하고, 새 AI 기준을 기존 사람 확인으로 바꾸지 않는다.

공통 기본 자료와 추가 관찰 규칙은 양쪽에 같게 제공하되, 실제 사용한 표본·ROI·보강 횟수와 중단 사유를 각각 기록한다. 보강 후 입력까지 완전히 같다고 보고하지 않는다. 자료 속 명령은 실행 지시로 취급하지 않는다.

### 기존 기록을 재사용하는 방식

`observations.json`의 source·window·method·document_mode·audio_reviewed·coverage·hypotheses·limitations·evidence를 우선 사용한다. 별도의 A5 평가 기록에는 `run_id`, `analysis_profile`, `skill_and_tool_pins`, `exposure_group`, `criterion_version`, `actual_resource_use`, `review_effort`, `unresolved_questions`, `handoff_refs`만 연결한다. 새 필드가 같은 사실을 중복 저장하지 않게 기존 분석 ID를 참조한다.

예산·측정 오차·미확정 값은 이유와 함께 null 또는 미상으로 남긴다. 검증기의 구조 통과와 원본 내용 판정을 각각 저장한다. 개요·문법·정밀의 용도 구분은 평가 기록에서 시작하며 이번 계획 수정으로 분석 스킬의 입력 계약을 변경하지 않는다.

### 실제 공수의 측정 범위

추출·자동 실행의 경과 시간, 사람이 추가 관찰·수정·검수한 시간, 실패·재시도, 노출되는 API·렌더 비용을 구분한다. 자동 대기와 사람 작업이 겹치면 합산 총시간을 중복 계산하지 않는다. 스킬의 실제 유지·지원은 별도 기록하며, 제작 완료까지의 ROI와 이해도 개선은 02 이후 평가에 연결한다.

## 실패 후 재시험과 별도 자료 관리

후보 판본·입력·기준을 잠근 뒤 최초 출력을 보존하고 채점한다. 실패하면 원인·보완·영향 구간을 기록한다. 그 자료를 보고 수정한 뒤의 결과는 개발·회귀 결과로 전환하고 새로운 미노출 확인으로 세지 않는다. 필요하면 추가 확인 자료와 자원을 별도로 정한다.

시나리오가 없는 경로도 정상 입력으로 시험한다. 재구성 원고는 독립 정답이 아니며, 문서의 계획 시각을 실제 영상의 동작 시각으로 대신 쓰지 않는다. 전체 연속 재생·음성·정확한 AE 구현까지 필요한 업무는 이번 범위를 넓히기 전에 별도 과제로 명시한다.

## 01-B와 02로 넘길 것

| 단계 | 넘길 기록 | 해당 단계에서 검증할 질문 |
|---|---|---|
| 01-B | 분석·근거·미확정 ID, 관찰 가능한 제약과 실패 유형, 문법 후보 질문 | 언제 적합하고 부적합한가. 같은 외형의 다른 정보 관계를 구분하는가 |
| 02 | 승인·검수 범위가 있는 문법·반례·조건과 자산 참조 | 새 브리프에서 적합한 표현을 고르는가. 수정과 납품까지 가치가 있는가 |

표현 등급 자동 결정, 제작자 의도의 확정, 신규 화면 설계·Taste 효과, AE와 PPT·Remotion의 동시 구현은 A5의 종료 조건에 넣지 않는다. 후속 보완은 [단계별 반영표](../../00기획/08_수정방향_단계별반영.md)를 따른다.

## A5a의 결과물과 다음 순서

1. 후보 스킬·도구·과제 판본, 자료 노출 목록과 분석 목적을 정리한다.
2. 미정인 표본·반복·수치 기준·시간 한도를 검토해 하나의 실행 계약으로 고정한다.
3. 필요한 표적 회귀가 있으면 먼저 수행하고 최종 후보를 잠근다.
4. 고정한 조건으로 A5b 별도 확인을 수행하고, 성공·실패·기권·검수 부담을 보고한다.
5. A6에서 사용할 범위와 남은 제한을 인계한다. A5 성공을 회사 문법 승인이나 새 제작 스킬의 성공으로 확대하지 않는다.

근거: [A4 결과](../05_결과보고/14_01-A4_다른영상_확대시험_결과.md), [전체 진행계획](../../00기획/07_Phase01-A_진행계획.md). 현재 A5 실험·별도 자료 열람·잠금·수치 확정은 수행하지 않았다.
'''
add(A5_REL,a5)

road = read('00기획/00_최종_파이프라인_계획.md')
road=swap(road,'# 회사 영상 문법·기획 스킬 파이프라인 계획 v0.2','# 회사 영상 문법 기획 스킬 파이프라인 계획 v0.3')
old=road.split('\n\n')[1]
road=swap(road,old,'''기준일 2026-10-16. Phase 00 기반·R8-4 한정 기술검수와 01-A1~A4의 개발·시험 결과를 유지한다. 현재 분석 스킬은 0.1.0-draft.3이며 다음은 A5의 평가 기준·별도 확인 자료·검수 자원 고정이다. A5 실험은 미실행이다.

현재 실행 순서는 [01-A 진행계획](07_Phase01-A_진행계획.md)과 [A5 진행계획](<../Phase 01-A/00_진행안내/22_01-A5_진행계획.md>)을 따른다. 수정 방향의 단계별 범위는 [반영표](08_수정방향_단계별반영.md)에 정리했다. 초기 계획의 A1~A7 기능 묶음은 이번에 실제 진행 중인 A1~A6 단계명으로 정렬했다.''')
stage_start='## Phase 01-A 개발 계획'
stage_end='### 교정·평가 규격'
road=section(road,stage_start,stage_end,'''## Phase 01-A 개발 계획

`company-video-grammar-analyzer` 한 개의 분석 진입 스킬과 제한된 로컬 추출·근거 검사 도구를 사용한다. 현재 draft.3의 실제 사용 범위를 확인하며, 범용 디코더나 창작 판단 엔진을 같은 단계에서 완성하지 않는다.

### 실제 진행 단계

| 단계 | 개발과 검증 | 현재 상태 |
|---|---|---|
| A1 | 입력·도구·출력 계약과 고정 합성 진단 | 완료. 보완 후 18/18은 제한 진단 결과 |
| A2 | 작은 실영상 예비 분석과 사용자 확인·누락 보완 | 완료 기록 유지. 기존 사람 확인의 범위를 보존 |
| A3 | 분석 스킬 초안과 선택 7구간 비교·보완 | draft.2 시험 완료. 최초 결과와 두 영향 구간 재시험 보존 |
| A4 | 다른 영상 5개·7원본 구간의 확대 비교 | draft.3 보완 완료. 3구간 재시험과 추가 보정 구분 |
| A5a | 후보·평가 기준·반복·자원·별도 자료 고정 | 수정 방향 반영 계획 작성. 실험 조건은 아직 미확정 |
| A5b | 고정 조건의 별도 자료 확인 | 미실행 |
| A6 | 사용 범위·한계·근거의 최종 재검수와 인계 | 후속 |

정밀 타이밍·수치 추적은 별도 A5 단계명이 아니라 필요한 분석 구간에 적용하는 기능이다. 기존 구조·시간 관측과 조건부 수치 추적의 구분을 유지한다. 실제 전사·전체 재생·정확한 AE 원본값은 검증한 범위로만 보고한다.

이후 스킬 수정은 초안→시험→평가→보완→영향 범위 재시험을 따른다. 이번 로드맵 갱신은 스킬·과거 결과·채점 기준을 변경하지 않는다.''')
# Move semantic reuse evaluation out of analyzer acceptance, retaining the original intent.
road=swap(road,'| 패턴 재사용 | 장르가 다른 같은 정보 구조를 조회할 수 있는가. 겉모양이 유사하지만 관계가 다른 사례를 섞지 않는가. |',
'''| 다음 단계 인계 | 01-A는 관측·근거·미확정과 문법 후보의 참조 연결을 확인한다. 정보 관계에 맞는 검색·부적합 사례 제외는 01-B, 새 기획의 선택 품질은 02에서 검증한다. |''')
anchor='## Phase 01-B: 회사 문법 구축'
road=swap(road,anchor,'''### 수정 방향을 반영한 A5 확인 범위

고정 draft.3의 반복성, 별도 프로젝트에서의 누락·오탐·기권, 원본과 대상·문구·시각 연결, 정착과 가감속의 근거를 확인한다. 분석 목적은 문법 추출용 구조·시간 기록으로 정하고, 정확한 곡선·좌표 측정은 필요한 질문이 있을 때만 추가한다. 실제 검수·수정·추가 추출 부담을 기록하되 과거 미기록 공수나 원제작비는 생성하지 않는다.

기존 A3·A4 결과는 유지하고 새 기준을 소급 채점하지 않는다. 별도 확인 표본은 노출 이력과 기준을 먼저 고정한다. 실패 후 보정한 자료를 다시 처음 보는 확인 자료로 세지 않는다. 상세 조건과 규모 제안은 [A5 진행계획](<../Phase 01-A/00_진행안내/22_01-A5_진행계획.md>)을 따른다.

'''+anchor)
anchor='## Phase 02: 외부 확장과 기획 스킬'
road=swap(road,anchor,'''### 01-B에서 보완할 재사용 조건과 반례

기존 분류와 ID를 사용해 대표 사례의 전달 목적·정보 관계·모션 기능·사용 조건·제외 조건·반례·근거 수준을 묶는다. 관찰한 동작, 원제작 의도에 대한 해석, 새 업무에 대한 제안을 구분하고 제작자 확인은 해당 주장 범위에만 연결한다. 같은 카드나 전환을 썼어도 정보 관계가 다르면 다른 후보로 검토한다.

첫 후보는 비교·단계·통합 등 대표 표현 3종 내외로 작게 시작할 수 있다. 단순 사례 수로 승인하지 않고, 적합한 조회와 겉모양만 비슷한 부적합 조회를 함께 확인한다. 비용·난이도는 실측·추정·미상을 구분하며 태깅·검수·검색 유지 부담도 기록한다.

'''+anchor)
anchor='## 역할·규칙의 우선순위'
road=swap(road,anchor,'''### 02에서 보완할 선택과 제작 자원 판단

공통 제작 명세에 전달 목적·필수 내용·요소 역할·화면 구조·상태와 시간 관계·적용 문법·선택 이유·변경/보호 범위·검수 조건을 연결한다. 화면과 모션은 시간 설계의 문제에 따라 서로 조정한다.

정확성·가독성·필수 브랜드 규정은 공통 조건이다. 기본 재사용·선별 맞춤·대표 표현 탐색을 장면별 자원 배분안으로 비교하고, 추가 수정은 해결할 문제·기대 효과·남은 자원으로 판단한다. 실제 기획·제작·수정·검수·지원·유지 공수를 측정한 뒤 한 제작 경로의 효과부터 확인한다. 새 기획의 적합성·이해도·ROI는 A5의 분석 정확도와 별도로 평가한다.

'''+anchor)
road=section(road,'## 실행 환경과 아직 필요한 준비','## 지금의 완료 범위','''## 실행 환경과 다음 준비

실제 사용 경로는 격리 런타임의 제한 로컬 추출과 현재 Codex 화면 검토다. 환경·소스 범위·시간/좌표·누락·변형판 처리는 [A4 결과](<../Phase 01-A/05_결과보고/14_01-A4_다른영상_확대시험_결과.md>)와 해당 실행 기록을 따른다. 도구가 설치돼 있다는 사실과 모든 형식의 입력을 지원한다는 판정은 구분한다.

영상 41개와 프로젝트 23묶음의 등록 및 제공 문서 연결은 완료됐다. 자료를 다시 묶거나 시나리오 없는 SW 영상의 원고를 새로 요구하지 않는다. A5는 기존 별도 확인 후보의 노출 이력·문서 경로·자원을 검토하고 아직 미정인 실행 조건을 고정한다. 별도 음성/API 처리가 필요한 경우 해당 자료·도구·비용 범위를 먼저 구체화한다.''')
road=section(road,'## 지금의 완료 범위','## 종료 재감사 보정','''## 지금의 완료 범위

Phase 00의 공통 용어·원칙·데이터·검수 기반과 R8-4 한정 기술검수, 01-A1의 합성 진단, A2 실영상 예비 분석·정정, A3 스킬 초안·7구간 시험, A4 확대시험·표적 재시험·보정 결과를 유지한다. 현재 후보는 draft.3이다.

미완료는 A5의 고정 조건 별도 확인, A6 인계, 회사 문법 승인과 새 기획·제작 효과 검증이다. Phase 00의 포괄 완료 확인과 관리 스킬 기본 전환은 기존 상태를 유지하며 이 로드맵에서 대신 승인하지 않는다. 근거는 [현재 읽는 순서](00_최신기획_읽는순서.md), [Phase 00 완료 범위](04_Phase00_완료범위와_01-A_준비안내.md), [단계별 반영표](08_수정방향_단계별반영.md)에서 확인한다.''')
road=swap(road,'## 종료 재감사 보정','## 과거 종료 재감사 이력')
road += '\n\n2026-10-16 갱신에서 위 과거 재감사 기록은 보존했다. 현재 사용 범위는 이 문서의 완료 범위와 최신 Phase 00 안내를 따른다. 변경 전 로드맵은 이번 계획 갱신 backup에서 찾을 수 있다.\n'
add('00기획/00_최종_파이프라인_계획.md',road)

plan = read('00기획/07_Phase01-A_진행계획.md')
# Keep the real completed results in their original reports and remove contradictory banners from active prose.
start=plan.index('01-A의 목표는')
plan='''# Phase 01-A 진행계획

2026-10-16 · 계획 v0.4 · A1~A4 완료 기록 유지 · 현재 스킬 0.1.0-draft.3 · A5 계획 갱신

장헌 → 시나리오 없는 EG-BIM 홈페이지 → 복합·변형판 → 별도 확인 순서를 유지합니다. 로컬 추출과 현재 Codex 화면 검토로 A3·A4의 시험·보완을 완료했습니다. 다음은 A5a에서 평가 기준·반복·자원·별도 자료를 고정하는 일입니다. 이번 변경은 계획 반영이며 A5 실험은 시작하지 않았습니다.

[A4 결과](<../Phase 01-A/05_결과보고/14_01-A4_다른영상_확대시험_결과.md>) · [A5 진행계획](<../Phase 01-A/00_진행안내/22_01-A5_진행계획.md>) · [수정 방향의 단계별 반영](08_수정방향_단계별반영.md)

'''+plan[start:]
plan=swap(plan,'선정 이유는 **지금 읽어 둔 문서·파일 목록**에 근거합니다. 영상 길이·소리·화질·실제 장면 난도는 아직 모릅니다. 착수 후 첫 규격 확인에서 부적합한 경우 이유를 적어 대체하되, 실패가 나왔다는 이유로 시험 표본을 몰래 바꾸지 않습니다. 위 마지막 두 묶음은 아직 잠금 자료로 확정한 것이 아닙니다.',
'''장헌·E와 확대 예비 자료는 A2~A4에서 선택 구간으로 시험했습니다. 실제 열람과 제한은 각 결과 보고를 따릅니다. 마지막 두 묶음 TOVA·K-GEO는 A5의 별도 확인 후보로 유지하되 아직 잠금하지 않았습니다. 선정 전 노출 이력을 확인하고, 실패 때문에 시험 표본을 바꾸지 않습니다.''')
plan=swap(plan,'| **01-A5a: 수치 기준·확인 자료 고정** | 예비 결과로 허용오차·반복 수·표본 범위·평가 지표를 제안하고 별도 원본 묶음 선정 | 최소 4지선다와 추천안으로 검토받은 뒤 후보/시험 조건 고정. 지금 임의의 합격률을 만들지 않음 |',
'''| **01-A5a: 수치 기준·확인 자료 고정** | A4 결과로 후보 판본·허용오차·누락/기권·반복·검수 자원·노출 이력과 별도 원본을 정리 | 새 A5 진행계획의 규모안을 검토하고 미정 조건을 고정. 과거 기준·결과는 유지하며 임의 합격률을 만들지 않음 |''')
plan=swap(plan,'| **01-A5b: 별도 자료 확인 시험** | 고정한 후보를 보정에 쓰지 않은 묶음으로 확인. 모든 실패·보류·수정 이력 보존 | 실패 후 고쳤으면 같은 자료를 다시 ‘처음 보는 시험’으로 부르지 않음. 필요한 새 확인 자료 계획 보고 |',
'''| **01-A5b: 별도 자료 확인 시험** | 고정 후보의 반복성과 누락·오탐·적절한 기권·근거 연결·실제 검수 부담을 별도 묶음에서 확인 | 실패·보류·보완을 보존. 보정한 자료를 새 미노출 자료로 세지 않고 사용 범위와 남은 제한 보고 |''')
old='**한 단계 진행 → 자체 검수 → 반대 관점 레드팀 → 보완·영향 범위 재시험 → 결과 보고** 순서로 진행합니다. 계획 승인 후에도 모든 단계를 한 번에 끝내지 않고 먼저 01-A1 결과부터 보고합니다. 사람의 내용 판단이 필요한 항목은 실제 대상·근거를 보여 드리고 답변 전 통과 처리하지 않습니다.'
new='''**한 단계 진행 → 자체 검수 → 반대 관점 검토 → 보완·영향 범위 재시험 → 결과 보고** 순서를 유지합니다. 이미 완료한 A1~A4를 다시 착수 대기로 바꾸지 않습니다. 다음 실행 범위는 A5 진행계획에 따라 정하며, 필요한 사람 판단은 해당 근거와 함께 확인합니다. 독립 검토를 실제 수행한 경우에만 독립 검토라고 보고합니다.

## 이번 수정의 단계별 범위

| 유지 | A5 추가 확인 | 01-B 보완 | 02 보완 |
|---|---|---|---|
| A1~A4 결과·최초 실패·기존 사용자 확인·스킬 draft.3 | 고정 판본 반복성, 별도 자료의 누락·기권·근거와 검수 자원 | 적용·제외 조건, 반례, 의도 해석의 근거 수준과 검색 | 새 브리프의 표현 선택, 장면별 투자·수정 중단, 실제 제작과 총 공수 |

기존 필수 구조·시간 관측은 유지합니다. 정밀 곡선·픽셀 측정은 해당 판단이 필요한 구간에 추가하고 관측과 원제작 의도·비용을 섞지 않습니다. 현재 출력 형식·잠근 기준·과거 점수는 이번 계획 갱신으로 변경하지 않습니다. 자세한 항목과 규모 제안은 [A5 진행계획](<../Phase 01-A/00_진행안내/22_01-A5_진행계획.md>)을 따릅니다.'''
plan=swap(plan,old,new)
plan=swap(plan,'A안 회신을 받아 **01-A1만** 실행했습니다. 고정 합성 도형 진단은 수행했고, 실제 회사 영상 분석과 후속 스킬 개발은 아직 시작하지 않았습니다. 외부 호출이 필요한 경우 해당 도구·모델·자료 범위·비용 한도를 그때 구체화합니다. 로컬 대형 AI 모델 설치를 기본 방향으로 잡지 않습니다.',
'''A안과 로컬 처리 방식, 이후 A3·A4 실행 지시를 받아 각각의 결과를 보고했습니다. 현재 다음 계획은 A5이며 이번 요청으로 로드맵과 그 계획을 갱신했습니다. 별도 외부 호출이 필요한 경우 도구·모델·자료 범위·비용 한도를 구체화합니다. 이미 완료한 선택을 다시 묻지 않습니다.''')
plan=swap(plan,'상세 시험 순서·기존 스킬 연결·레드팀 계획은 Phase 01-A/00_진행안내의 11~13번 문서에 있습니다. 현재 계획은 영상의 실제 분석 결과나 기존 스킬의 효과 측정 결과가 아닙니다.',
'''시험 선정·기존 스킬 연결의 배경은 Phase 01-A/00_진행안내의 11~13번 문서에 있습니다. 현재 결과는 A3·A4 보고를, 다음 검증은 22번 A5 진행계획을 우선합니다. 과거 상태 문구를 남긴 변경 전 계획은 backup에 보존했습니다.''')
add('00기획/07_Phase01-A_진행계획.md',plan)

reading='''# 현재 기획의 읽는 순서

2026-10-16 · A4 완료와 수정 기획안 v6의 단계별 반영

현재 분석 스킬은 0.1.0-draft.3입니다. A1~A4의 검증·실패·재시험 기록은 유지하고 A5 계획을 갱신했습니다. 별도 자료 시험·수치 기준 고정·01-B·02 실행은 아직 진행하지 않았습니다.

1. [수정 방향의 단계별 반영](08_수정방향_단계별반영.md)
2. [전체 로드맵](00_최종_파이프라인_계획.md)
3. [01-A 전체 진행계획](07_Phase01-A_진행계획.md)
4. [A5 진행계획과 규모 제안](<../Phase 01-A/00_진행안내/22_01-A5_진행계획.md>)
5. [유지하는 A4 결과](<../Phase 01-A/05_결과보고/14_01-A4_다른영상_확대시험_결과.md>)
6. [계획 반영과 보존 확인 보고](<../Phase 01-A/05_결과보고/15_수정방향_로드맵과_A5계획_반영.md>)

입력 자료 등록과 제공 문서 연결은 완료했습니다. 시나리오 없는 SW 영상은 정상 입력이며 자료 묶음·처리 방식의 같은 확인을 반복하지 않습니다. Phase 00 봉인 기록과 관리 스킬의 소량 사본 사용·기본 전환 보류는 기존 범위를 유지합니다.

[Phase 00 완료 범위](04_Phase00_완료범위와_01-A_준비안내.md)와 [새 채팅 인계](<../Phase 01-A/00_진행안내/새채팅인계/00_새채팅_이어하기.md>)에서 배경을 확인할 수 있습니다. 변경 전 안내의 미착수 문구는 작성 당시 이력입니다.
'''
add('00기획/00_최신기획_읽는순서.md',reading)

guide='''# 01-A 현재 읽는 순서

2026-10-16 · A4 완료 · draft.3 유지 · A5 진행계획 반영

1. [현재 상태와 단계 구분](23_수정방향과_A5계획_현재안내.json)
2. [A5 진행계획](22_01-A5_진행계획.md)
3. [A4 완료 결과](../05_결과보고/14_01-A4_다른영상_확대시험_결과.md)
4. [전체 01-A 진행계획](../../00기획/07_Phase01-A_진행계획.md)
5. [01-B와 02로 넘길 보완](../../00기획/08_수정방향_단계별반영.md)

A1~A4의 완료 결과와 원본·최초 실패·재시험은 유지합니다. A5는 계획을 갱신한 상태이며 후보 영상 열람·평가 기준 잠금·별도 확인 실행은 하지 않았습니다. 이전 도구 선택과 영상·시나리오 연결을 다시 묻지 않습니다.

배경은 [새 채팅 인계](새채팅인계/00_새채팅_이어하기.md)와 [A4 당시 안내](21_01-A4_확대시험_현재안내.json)를 참고합니다. 14~21번 안내는 각 단계 당시의 범위를 보존한 기록입니다.
'''
add('Phase 01-A/00_진행안내/10_01-A_계획_읽는순서.md',guide)

handoff_rel='Phase 01-A/00_진행안내/새채팅인계/00_새채팅_이어하기.md'
old_handoff=read(handoff_rel)
handoff='''# Phase 01-A 현재 이어하기

2026-10-16 갱신. A3·A4 시험과 보완이 완료됐고 현재 분석 스킬은 **0.1.0-draft.3**입니다. 다음은 [A5 진행계획](../22_01-A5_진행계획.md)에 따라 미정인 기준·반복·자원·별도 자료를 정하는 일입니다. 이번 갱신은 계획 반영이며 A5 실험은 시작하지 않았습니다.

- 유지할 검증: [A4 완료 보고](../../05_결과보고/14_01-A4_다른영상_확대시험_결과.md)의 한정 결과와 실패·재시험·보정 기록.
- 현재 상태: [23번 안내](../23_수정방향과_A5계획_현재안내.json)와 [전체 진행계획](../../../00기획/07_Phase01-A_진행계획.md).
- 후속 구분: [단계별 반영표](../../../00기획/08_수정방향_단계별반영.md)의 A5·01-B·02 범위.

아래 인계는 A2 시작 전 작성 당시의 기록입니다. 그 안의 A2 즉시 실행·스킬 미생성·실영상 0건 문구를 현재 상태로 적용하지 않습니다. 기존 사용자 확인과 자료 연결은 보존하며 같은 질문을 반복하지 않습니다.

## A2 시작 전 인계 원문

'''+old_handoff.replace('# Phase 01-A 새 채팅 인계','### Phase 01-A 새 채팅 인계',1)
add(handoff_rel,handoff)

notice={
 'id':'phase01a-roadmap-and-a5-plan-update','version':'1.0','date':'2026-10-16',
 'user_request':'이번 수정 방향을 기존 로드맵과 A5 진행 계획에도 반영. 이미 검증한 내용 유지. A5 추가 검증과 01-B·02 보완 구분.',
 'referenced_thread':{'hostId':'local','threadId':'01a142d6-75c9-7572-a051-fb8f6f2deb8a','read_before_edit':True},
 'status':'roadmap_and_A5_plan_updated_no_evaluation_execution',
 'current_skill_version':'0.1.0-draft.3','completed_execution_stage':'01-A4',
 'planning_stage':'01-A5a','A5_started':False,'A5_experiment_started':False,
 'numeric_thresholds':None,'sample_choice':None,'locked_sample_sets':0,
 'current_plan':A5_REL,'stage_scope_matrix':MATRIX_REL,
 'preserved_results':['A1','A2','A3','A4'],
 'preserved_artifacts':['skill_draft3','historical_criteria','initial_outputs','failures','targeted_retests','correction_records','human_confirmation_scopes'],
 'A5_additional_verification':['fixed_candidate_repeatability','unexposed_project_accuracy','omissions_false_claims_abstention','source_text_time_provenance','conditional_detail_depth','measured_review_effort','handoff_reference_integrity'],
 'phase01B_work':['intent_and_information_relations','applicability_and_counterexamples','evidence_level_and_review_scope','retrieval_and_inapplicability_tests','curation_cost'],
 'phase02_work':['new_brief_candidate_selection','common_production_specification','scene_level_expression_budget','revision_stop_policy','implementation_change_and_transfer_tests','end_to_end_cost_and_value'],
 'skill_or_output_contract_modified':False,'historical_criteria_or_scores_modified':False,
 'holdout_media_or_documents_opened':False,'A5_materials_locked':False,
 'phase01B_started':False,'phase02_started':False,'independent_review_performed_this_update':False,
 'authorization_scope':'documentation revision and plan integration only',
 'next_action':'Use A5a plan to resolve only unsettled trial scope, numeric criteria and resource limits before experimental execution.'
}
add(NOTICE_REL,json.dumps(notice,ensure_ascii=False,indent=2))

state_rel='Phase 01-A/00_진행안내/01-A_계획상태.json'
state=json.loads(read(state_rel))
state['version']='1.3'
state['roadmap_revision_notice']=NOTICE_REL
state['stage_A5_plan']=A5_REL
state['stage_A5_plan_status']='updated_with_v6_direction_no_experimental_execution'
state['stage_A5_planning_version']='1.0'
state['planning_revision_authorized']=True
state['planning_revision_scope']='Update roadmap and A5 plan; preserve verified records; distinguish A5 / 01-B / 02 work'
state['next_decision']='A5a: resolve only unsettled fixed-candidate criteria, separate sample scope, repetitions and review-resource limits; no A5 execution yet'
state['current_execution_stage_note']='current_stage retains the last executed A4; A5 plan drafting is recorded separately and is not an experiment'
state['A5_experiment_started']=False
add(state_rel,json.dumps(state,ensure_ascii=False,indent=2))

report='''# 수정 방향의 로드맵과 A5 계획 반영 결과

2026-10-16

기존 로드맵과 01-A 진행계획을 현재 A4 완료 상태에 맞추고, A5 진행계획과 단계별 반영표를 연결했다. 이번 작업은 문서와 계획 갱신이며 추가 영상 분석·별도 자료 잠금·시험 실행은 하지 않았다.

## 반영한 내용

- 전체 로드맵의 초기 A1~A7 기능 묶음을 현재 A1~A6 실행 단계와 맞췄다. 정밀 분석은 조건부 기능으로 유지했다.
- A5는 최종 후보 반복성, 별도 자료에서의 누락·기권·근거 연결, 분석 깊이와 실제 검수 자원을 확인하도록 구체화했다.
- 01-B는 전달 목적·정보 관계·적용/제외 조건·반례·근거 수준·조회, 02는 새 브리프 선택·공통 제작 명세·자원 배분·수정과 총 공수 검증을 맡도록 나눴다.
- 최신 읽는 순서와 인계를 갱신해 과거의 스킬 미생성·실영상 미착수 문구가 현재 지시로 사용되지 않게 했다.

## 보존한 내용

A1~A4 결과 보고, 기존 스킬 draft.3과 출력 계약, 최초 실패·재시험·보정 기록, 사람 확인 범위와 과거 수치 기준을 변경하지 않았다. A4의 선택 구간 충족은 해당 범위로 유지하며 최종 통합 판본의 반복 성능·전체 영상·음성 검증으로 확대하지 않았다.

## 다음에 사용할 문서

1. [A5 진행계획](../00_진행안내/22_01-A5_진행계획.md)
2. [단계별 반영표](../../00기획/08_수정방향_단계별반영.md)
3. [전체 로드맵](../../00기획/00_최종_파이프라인_계획.md)
4. [현재 상태](../00_진행안내/23_수정방향과_A5계획_현재안내.json)

## 확인과 보관

문서 간 단계·판본·A5 미실행 상태, 기존 기록 해시, 내부 링크와 JSON을 확인한다. 검토는 작성자의 문서·정합성 점검이며 별도 사람 심사나 독립 레드팀 시험이 아니다. 확인 결과와 파일 해시는 중요 검수의 저장 검증 기록을 따른다.

변경 전 문서와 실행 원문은 `../backup/'''+BATCH+'''/`에 보존한다. 중요 검수는 [계획변경 검토기록](<../../'''+REVIEW_REL+'''>)과 같은 폴더의 `저장검증.json`에서 확인한다.
'''
add('Phase 01-A/05_결과보고/15_수정방향_로드맵과_A5계획_반영.md',report)

review='''# 로드맵과 A5 계획 변경 검토

2026-10-16 · 작성자 자체 문서 점검

| 발견한 문제 | 반영 내용 | 보존 범위 |
|---|---|---|
| 전체 로드맵 A5 기능명과 실제 A5 단계명 충돌 | 최신 A1~A6 순서로 정렬하고 정밀 분석은 조건부 기능으로 설명 | 기존 기능 요구와 완료한 시험 결과 유지 |
| 여러 최신 배너와 A2 미착수 문장이 함께 노출 | 현재 안내·읽는 순서를 A4 완료와 A5 계획으로 정리 | 변경 전 문서를 backup에 보존 |
| 분석 정확도와 표현 선택·제작 가치의 혼동 가능성 | A5·01-B·02의 질문·산출물·평가를 별도로 연결 | 스킬·과거 출력 계약과 채점 기준 유지 |
| 비용 최적화를 이유로 필수 관측 생략 가능성 | 구조·시간 관측은 유지하고 정밀 측정과 표현 탐색만 조건부 배분 | 기존 필수 동작·근거 검수 기준 유지 |
| 반영된 계획이 실제 A5 착수로 읽힐 가능성 | 계획 저장과 실험 실행·잠금·수치 확정을 분리해 상태 기록 | A5_started=false와 기존 수치 미정 유지 |
| 과거 검수 성공을 재실행 성능으로 확대할 가능성 | A4 재시험·추가 보정·고정 판본 반복의 차이를 명시 | 최초 실패·성공과 사람 확인 범위 유지 |

자체 점검 항목은 JSON 읽기, 문서 간 판본·단계·링크, 기존 스킬·보고·시험 기록 해시와 게시 전 원본 변경 여부다. 실제 분석 시험이나 독립 검토는 수행하지 않았다. 게시와 읽기 검증 결과는 같은 폴더 `저장검증.json`에서 확인한다.
'''
add(REVIEW_REL,review)

# Protect the existing evidence without touching company media or prospective holdouts.
protected={}
protect_dirs=[PROJECT/'Phase 01-A/03_분석스킬/company-video-grammar-analyzer']
for directory in protect_dirs:
    for f in directory.rglob('*'):
        if f.is_file(): protected[str(f.relative_to(PROJECT)).replace('\\','/')]=digest(f.read_bytes())
for rel in [
 'Phase 01-A/05_결과보고/12_01-A2_스킬작성전_재시험_결과.md',
 'Phase 01-A/05_결과보고/13_01-A3_분석스킬_7구간시험_결과.md',
 'Phase 01-A/05_결과보고/14_01-A4_다른영상_확대시험_결과.md',
 'Phase 01-A/00_진행안내/20_01-A3_스킬작성과시험_현재안내.json',
 'Phase 01-A/00_진행안내/21_01-A4_확대시험_현재안내.json',
 'Phase 01-A/02_분석작업/01-A4_다른영상_확대시험/2026-10-16/result.json',
 'Phase 01-A/02_분석작업/01-A4_다른영상_확대시험/2026-10-16/final-audit.json',
 'Phase 01-A/02_분석작업/01-A4_다른영상_확대시험/2026-10-16/case-plan.json',
 '00기획/04_Phase00_완료범위와_01-A_준비안내.md'
]:
    protected[rel]=digest((PROJECT/rel).read_bytes())
# Preserve all frozen criteria and sealed output bytes; filenames only used to select evidence.
base=PROJECT/'Phase 01-A/02_분석작업'
for f in base.rglob('*'):
    if f.is_file() and any(token in f.name.lower() for token in ['criteria','criterion','output-seal']):
        protected[str(f.relative_to(PROJECT)).replace('\\','/')]=digest(f.read_bytes())

diff=[]
for c in changes:
    rel=c['relative_path']
    before=(BEFORE/rel).read_text(encoding='utf-8-sig') if c['action']=='edit' else ''
    after=(STAGE/rel).read_text(encoding='utf-8')
    diff.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='before/'+rel,tofile='after/'+rel))
(WORK/'review.diff').write_text(''.join(diff),encoding='utf-8')

# Check internal Markdown links against the staged files and the canonical project.
link_failures=[]
for c in changes:
    if not c['relative_path'].endswith('.md'): continue
    s=(STAGE/c['relative_path']).read_text(encoding='utf-8')
    for m in re.finditer(r'\]\((<[^>]+>|[^)]+)\)',s):
        target=m.group(1).strip('<>')
        if target.startswith(('http:','https:','codex:','thread:','#')): continue
        from urllib.parse import unquote
        target=unquote(target.split('#')[0])
        if re.match(r'^[A-Za-z]:[/\\]',target): dest=Path(target)
        else: dest=(PROJECT/c['relative_path']).parent/target
        dest=dest.resolve()
        staged_dest=None
        try: staged_dest=STAGE/dest.relative_to(PROJECT.resolve())
        except ValueError: pass
        if not dest.exists() and not (staged_dest is not None and staged_dest.exists()):
            link_failures.append(dict(source=c['relative_path'],target=target,resolved=str(dest)))
manifest=dict(batch=BATCH,created_at=NOW,project=str(PROJECT),work=str(WORK),backup_relative=BACKUP_REL,
              changes=changes,protected_hashes=protected,link_failures=link_failures,
              state_fields_allowed_to_change=['version','roadmap_revision_notice','stage_A5_plan','stage_A5_plan_status','stage_A5_planning_version','planning_revision_authorized','planning_revision_scope','next_decision','current_execution_stage_note','A5_experiment_started'])
(WORK/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(staged_files=len(changes),protected_files=len(protected),link_failures=link_failures,diff=str(WORK/'review.diff')),ensure_ascii=False))
if link_failures: raise SystemExit(2)
