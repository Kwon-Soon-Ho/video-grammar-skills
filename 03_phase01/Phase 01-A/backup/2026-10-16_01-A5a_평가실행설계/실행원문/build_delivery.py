from pathlib import Path
import json,hashlib,datetime
ROOT=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
B=Path(__file__).resolve().parent
S=B/'staged'
def write(relative,text):
 p=S/relative;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(text,encoding='utf-8')
def js(relative,d):write(relative,json.dumps(d,ensure_ascii=False,indent=2))
C=json.loads((B/'contract-v1.json').read_text(encoding='utf-8'))
report='Phase 01-A/05_결과보고/16_01-A5a_평가기준과_별도확인_설계보고.md'
notice='Phase 01-A/00_진행안내/24_01-A5a_평가조건_현재안내.json'
protocol='Phase 01-A/00_진행안내/25_01-A5a_평가실행계약.md'
design='Phase 01-A/04_검증자료/01-A5a_실행설계/2026-10-16'
write(protocol,(B/'25_01-A5a_평가실행계약.md').read_text(encoding='utf-8'))
write(report,'''# A5a 평가 기준과 별도 확인 설계 보고

2026-10-16 · 추천 A안 구체화 완료 · A5b 진행 판단용

참조 채팅에서 정한 분석→회사 문법→기획 판단의 방향을 반영해 A5a 설계를 구체화했습니다. **별도 확인은2프로젝트·4구간·2반복·2비교군으로16실행**입니다. 새 자료에 들어가기 전 기존3구간을 최종 통합 draft.3으로1회씩 확인하므로 기본 분석은 총19실행입니다. 기존 A1~A4 결과·실패·재시험·사람 확인 기록과 스킬은 유지했습니다.

## 평가 기준

| 항목 | 적용할 기준 |
|---|---|
| 중대 오류·구조/근거 연결 오류 | 0건 |
| 핵심 사실·동작 | 각 실행100% |
| 세부 관측 | 각 실행90% 이상 |
| 확정 주장 정확도 | 각 실행95% 이상, 기준표 밖 추가 주장도 확인 |
| 회피 가능한 기권 | 판독 가능 항목의10% 이하. 핵심100% 기준은 별도 유지 |
| 반복성 | 같은 구간의 두 반복에서 모두 맞은 세부 항목90% 이상 |
| 동작 경계 | 기준 범위와 거리0.2초 이내·보고 범위 폭0.4초 이내 |

각 스킬 적용 실행8개를 따로 판정하며 평균으로 실패를 숨기지 않습니다. 숫자·단위·부정어·대상/문구 순서를 바꿔 의미가 달라지거나, 근거 없이 이동·이징을 확정하면 중대 오류입니다. 진짜 판독 불가인 곡선은 미확정으로 남길 수 있지만 확인 가능한 방향·순서를 생략한 것은 누락입니다. 기준 경계 자체가0.2초 안으로 좁혀지지 않으면 그 수치 판정은 보류합니다.

이 수치는 다음 시험을 위한 작업 기준이며 과거 A4의 성능 추정값이 아닙니다. 기존 결과에 소급 적용하지 않았습니다. 구간별 실제 기준답안은 A5b 준비 시 원본만 보고 만들고, 분석 출력 전에 봉인합니다. AI 기준은 사람 정답으로 표시하지 않습니다.

## 별도 확인 자료

| 자료 | 지정 구간 | 사용 조건 |
|---|---|---|
| TOVA `01_(T).mp4` | 0–8초 | 무문서 경로 |
| TOVA `04_(A).mp4` | 12–20초 | 같은 TOVA 프로젝트의 별도 클립 |
| K-GEO `K-GEO FESTA_250919_3.mp4` | 25–35초,66–76초 | 영상은 기존 시험에 미사용, 연결 시나리오 DOC064 본문은 사전 노출 |

영상3파일·프로젝트2묶음·총36초입니다. 화면을 먼저 보고 유리한 구간을 고르지 않고 등록 경로·재생시간으로 정했습니다. 파일 해시와 구간을 고정했으며 영상 픽셀·음성은 열지 않았습니다. 모션 유형이 부족하면 그 한계를 보고하고 실패 때문에 표본을 바꾸지 않습니다. TOVA는 EG-BIM과 같은 홈페이지 장르이며, K-GEO는 문서까지 완전 미노출인 자료가 아닙니다. 이 두 프로젝트의 소량 확인을 회사 전체 일반화로 확대하지 않습니다.

## 반복과 실행 순서

**기존 G퇴장·싱글 자막·듀얼 자막/정착 구별3구간의 회귀 → 별도4구간 기준표 봉인 → 새 문맥16실행 → 이름을 가린 결과 대조** 순서입니다. 두 비교군은 같은 과제·기본 표본·도구와 추가 관찰 한도를 받습니다. 추가 표본은 독자적으로 고를 수 있으며 실제 사용량도 남깁니다.

사전 회귀가 실패하면 새 자료를 열기 전에 멈춥니다. 새 자료를 본 뒤 수정한 스킬의 재시험은 개발/회귀 결과로 분리합니다. 과거 정정 내용을 분석자에게 알려 주고 재작성한 결과를 최초 확인 결과로 세지 않습니다.

## 검수 공수와 자원 상한

| 작업 | 한도 |
|---|---|
| 별도16실행 | 회당15분, 합계240분 |
| 기존3구간 회귀 | 회당10분, 합계30분 |
| 기술 준비 | 30분 |
| 기준표 작성·대조 | 40분 |
|16실행 결과 검수 | 32분 |
| 불일치 정리 | 18분 |
| **검수 합계** | **90분** |
| 사용자에게 새로 요청할 확인 | 위90분 안에서 **20분·6항목 이하** |
| 전체 합계 | **390 작업분**. 병렬 경과시간과 구분 |

분석당 기본 프레임 최대32장, 보강2회·총48장, 무배율 크롭40개를 사용합니다. 새 원본 PNG는 전체1,000장, 파생 포함 저장8GiB로 제한합니다. 기술 재시도는 같은 입력으로 총2회까지, 위 시간 한도에 포함합니다. 내용 피드백 후 재작성은 별도 최초 시험으로 인정하지 않습니다.

검수 주체가 사람인지 AI인지, 사람 활성 공수와 AI 경과시간·사용자 대기를 구분합니다. A4의 미기록 공수를 새로 추정하지 않습니다. 같은 품질의 검수 공수가 미사용군의1.2배를 넘으면 비용 보완 대상으로 표시하고, 비교 가능한 공수가 없으면 절감 효과를 미입증으로 남깁니다. 품질과 공수 중 하나가 좋아졌다고 다른 쪽의 실패를 통과시키지 않습니다.

## A5b 진행 판단

이 설계로 A5b를 진행하는 것을 추천합니다. 중대 오류, 사전 회귀 실패, 판본 변화 또는 자원 한도 도달 시 멈추고 완료·실패·미실행 수를 보고하도록 준비했습니다. A5b 결과에서는 관측 품질 통과, 미확정, 스킬 효과 미입증, 보완 필요를 구분하겠습니다.

**이번에 완료한 것은 A5a 실행 설계입니다.** 영상 분석·기준답안 작성·사전 회귀·A5b16실행은 모두0건이고 실제 점수도 없습니다. A5b는 사용자가 이 보고를 본 뒤 결정합니다. 회사 문법의 적용 조건·반례는01-B, 새 기획의 표현 선택과 제작·유지 경제성은02에서 검증합니다.

## 상세 기록

- [평가 실행 계약](../00_진행안내/25_01-A5a_평가실행계약.md)
- [현재 상태](../00_진행안내/24_01-A5a_평가조건_현재안내.json)
- [파일 해시와 실행 설계](../04_검증자료/01-A5a_실행설계/2026-10-16/contract-v1.json)
- [유지하는 A4 결과](14_01-A4_다른영상_확대시험_결과.md)
- [방향성 단계별 반영](../../00기획/08_수정방향_단계별반영.md)

변경 전 문서와 실행 원문은 `Phase 01-A/backup/2026-10-16_01-A5a_평가실행설계`에, 중요 자체 검토와 보존 확인은 `작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A5a_평가실행설계`에 저장합니다.
''')
state=json.loads((ROOT/'Phase 01-A/00_진행안내/01-A_계획상태.json').read_text(encoding='utf-8'))
state.update(version='1.4',date='2026-10-16',state='A5a_design_pinned_pending_A5b_decision',current_stage='01-A5a',approved_execution_scope='A5a recommended design: evaluation criteria, repetitions, selected file/window identities and resource caps; A5b requires later user decision',A5_started=True,A5a_started=True,A5a_status='design_completed_no_analysis_runs',A5b_started=False,A5b_authorized=False,A5_experiment_started=False,stage_A5a_report=report,stage_A5a_current_notice=notice,stage_A5a_contract=protocol,stage_A5a_design=design,stage_A5_plan_status='A5a_concrete_design_v1_pending_A5b',stage_A5_planning_version='1.1',numeric_thresholds=C['quality_gates'],numeric_thresholds_status='prospective_only_no_historical_regrading',final_evaluation_sample_count=4,final_evaluation_sample_count_unit='windows across two project groups; not four independent projects',locked_sample_sets=2,locked_sample_sets_status='file/window design pinned for review; reference answers not yet authored',company_media_opened_this_stage=0,company_media_metadata_inspected_this_stage=3,company_documents_new_body_read_this_stage=0,actual_scores=None,human_content_reviews_pending=0,next_decision='User reviews A5a report and decides whether to execute A5b: three known-case preflight regressions, then 16 fixed comparisons',current_execution_stage_note='A5a design complete; last content analysis remains A4; no A5b experiments')
js('Phase 01-A/00_진행안내/01-A_계획상태.json',state)
js(notice,{'id':'phase01a-A5a-design','date':'2026-10-16','status':state['state'],'user_authorized_A5a':True,'user_authorized_A5b':False,'report':report,'contract':protocol,'design':design,'skill_version':'0.1.0-draft.3','recommended_option_selected':'A','primary_runs_planned':16,'legacy_regressions_planned':3,'actual_runs':0,'actual_scores':None,'video_pixels_opened_this_stage':False,'file_metadata_and_hashes_inspected':True,'project_groups':2,'windows':4,'unique_visual_seconds':36,'K_GEO_document_preexposed':True,'reference_answers_status':'A5b preparation before primary outputs','review_minutes_max':90,'user_minutes_max':20,'user_questions_max':6,'next_action':'report to user; no automatic A5b execution','old_results_and_skill_preserved':True})
write('Phase 01-A/00_진행안내/22_01-A5_진행계획.md','''# Phase 01-A5 진행계획

2026-10-16 · v1.1 · A5a 추천안 구체화 완료 · A5b 사용자 판단 대기

현재 스킬은0.1.0-draft.3이다. A1~A4 결과와 최초 실패·재시험·보정·사람 확인 범위를 유지한다. A5a에서 평가 기준·반복·자료와 구간·자원 한도를 구체화했다. 실제 영상 분석·기준답안 제작·A5b 시험은 시작하지 않았다.

## 현재 적용할 실행 설계

- [A5a 결과 보고](../05_결과보고/16_01-A5a_평가기준과_별도확인_설계보고.md)
- [평가 실행 계약](25_01-A5a_평가실행계약.md)
- [현재 상태](24_01-A5a_평가조건_현재안내.json)

선택한 추천 A안은2프로젝트×2구간×2반복×2비교군16실행이다. 이에 앞서 최종 통합 스킬의 기존3구간 회귀를1회씩 확인하므로 기본 분석은19실행이다. 회귀 실패 시 새 자료를 열기 전에 중단한다. 기존 구간을 별도 확인 표본 수에 넣지 않는다.

## 핵심 조건

스킬 적용군8개 실행 각각에서 중대 오류·근거 연결 오류0, 핵심100%, 세부90%, 확정 주장 정확도95%를 기준으로 한다. 같은 구간의 두 반복 모두에서 맞는 세부 항목은90% 이상이어야 한다. 정당한 기권과 누락을 구분한다. 구체적인 분모·반올림·경계0.2초/보고범위0.4초와 중단 기준은 실행 계약을 따른다. 과거 결과에 소급 채점하지 않는다.

자료는 TOVA T0–8초·A12–20초, K-GEO25–35초·66–76초다. 파일과 구간은 픽셀을 보기 전에 고정했다. K-GEO는 영상 신규·DOC064 본문 사전 노출로 기록한다. 한 프로젝트의 여러 클립이나 반복을 독립 프로젝트로 세지 않는다. 문서 없는 입력도 정상 경로이며 제작 의도·정확 AE 구현·음성은 추정하지 않는다.

검수 상한은 기준표40분+결과 대조32분+불일치18분=90분이며 사용자 추가 확인은 그 안에서20분·6항목 이하로 둔다. 별도 분석240분, 회귀30분, 기술 준비30분을 합한 전체 상한은390작업분이다. 실제 수행 주체와 대기·중첩 시간을 구분하며 A4의 미기록 공수를 추정하지 않는다.

## A5b 이후 판단

사용자가 A5a 보고를 본 뒤 A5b 진행 여부를 결정한다. 승인 후 기준답안을 분석 출력과 분리해 작성·봉인하고 같은 과제와 자원 한도로 실행한다. 후보·도구·프롬프트가 바뀌면 판본을 다시 고정한다. 새 자료를 보고 수정한 결과는 개발·회귀로 구분한다.

A5b에서 성공·실패·기권·반복 차이와 실제 공수를 보고한 후 A6 인계 또는 보완·축소를 정한다. A5 성공은 회사 문법 승인이나 제작 경제성 입증이 아니다. 적용 조건·반례는01-B, 새 브리프의 표현 선택·구현·수정·지원까지의 효과는02에서 확인한다.

## 규모 선택 이력

A안은 이번 사용자 지시로 A5a 구체화에 선택됐다. 이전 B축소안은8실행, C확대안은36실행, D는설계만 정리하는 대안이었다. 새로운 추가 결정을 요구하지 않고 선택한 A안을 기준으로 준비했다. 이전 v1.0의 미정 수치·미잠금 상태는 변경 전 백업에 보존한다.
''')
write('Phase 01-A/00_진행안내/10_01-A_계획_읽는순서.md','''# 01-A 현재 읽는 순서

2026-10-16 · A5a 설계 완료 · draft.3 유지 · A5b 판단 대기

1. [A5a 결과 보고](../05_결과보고/16_01-A5a_평가기준과_별도확인_설계보고.md)
2. [현재 상태](24_01-A5a_평가조건_현재안내.json)
3. [평가 실행 계약](25_01-A5a_평가실행계약.md)
4. [A5 진행계획](22_01-A5_진행계획.md)
5. [유지하는 A4 결과](../05_결과보고/14_01-A4_다른영상_확대시험_결과.md)
6. [01-B와02의 범위](../../00기획/08_수정방향_단계별반영.md)

A1~A4의 결과·실패·재시험과 사람 확인 범위를 유지한다. A5a는16개 별도 비교와3개 사전 회귀를 위한 기준·자료·공수 설계만 완료했다. 실제 분석 실행은0이며 A5b는 사용자 결정 전이다. 이전 수치 미정·A5 미착수 문구는 작성 당시 이력이다.
''')
write('00기획/00_최신기획_읽는순서.md','''# 현재 기획의 읽는 순서

2026-10-16 · A5a 설계 완료 · A5b 판단 대기

현재 분석 스킬은0.1.0-draft.3이다. A1~A4 검증과 실패·재시험 기록을 유지하고, A5a에서 평가 기준·반복·별도 자료·검수 공수 한도를 구체화했다. A5b 영상 분석은0회다.

1. [A5a 설계 보고](<../Phase 01-A/05_결과보고/16_01-A5a_평가기준과_별도확인_설계보고.md>)
2. [평가 실행 계약](<../Phase 01-A/00_진행안내/25_01-A5a_평가실행계약.md>)
3. [수정 방향의 단계별 반영](08_수정방향_단계별반영.md)
4. [전체 로드맵](00_최종_파이프라인_계획.md)
5. [01-A 진행계획](07_Phase01-A_진행계획.md)
6. [유지하는 A4 결과](<../Phase 01-A/05_결과보고/14_01-A4_다른영상_확대시험_결과.md>)

분석의 정확성·반복성과 검수 부담은A5, 적용 조건·반례는01-B, 새 기획 선택과 제작 경제성은02에서 검증한다. 입력 자료 등록과 문서 연결은 완료했으며 같은 연결을 다시 묻지 않는다. Phase00의 관리 스킬 전환·봉인 범위는 유지한다.
''')
for relative,heading in [('00기획/07_Phase01-A_진행계획.md','01-A 최신'),('00기획/00_최종_파이프라인_계획.md','전체 로드맵 최신'),('Phase 01-A/00_진행안내/새채팅인계/00_새채팅_이어하기.md','현재 이어하기')]:
 prefix=f'> {heading} 2026-10-16: A5a 추천 A안의 평가·반복·자료/구간·공수 설계를 완료했습니다. [A5a 결과 보고](<{str(ROOT/report).replace(chr(92),"/")}>)와 [실행 계약](<{str(ROOT/protocol).replace(chr(92),"/")}>)을 우선 적용합니다. A5b는 사용자 판단 대기이며 실제 분석0회입니다. 기존 A1~A4 결과와 아래의 이전 상태는 이력으로 보존합니다.\n\n'
 write(relative,prefix+(ROOT/relative).read_text(encoding='utf-8'))
js('delivery-map.json',{'report':report,'notice':notice,'protocol':protocol,'design':design,'backup':'Phase 01-A/backup/2026-10-16_01-A5a_평가실행설계','review':'작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A5a_평가실행설계'})
print('A5a report, protocol and current pointers staged; no A5b execution')
