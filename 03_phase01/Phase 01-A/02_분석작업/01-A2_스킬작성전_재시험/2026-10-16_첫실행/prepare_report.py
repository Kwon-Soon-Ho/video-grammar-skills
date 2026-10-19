from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,importlib.util
HERE=Path(__file__).resolve().parent
ROOT=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
AN=Path('Phase 01-A/02_분석작업/01-A2_스킬작성전_재시험/2026-10-16_첫실행')
PRE=Path('Phase 01-A/06_도구와계약/01-A2_모션검수절차/스킬작성전_재발시험')
REPORT=Path('Phase 01-A/05_결과보고/12_01-A2_스킬작성전_재시험_결과.md')
NOTICE=Path('Phase 01-A/00_진행안내/19_01-A2_스킬작성전_재시험_현재안내.json')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
now=datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds')
audit=read(HERE/'실행감사.json')
spec=importlib.util.spec_from_file_location('review',r'C:\Users\User\.codex\skills\anthropic-skill-creator\eval-viewer\generate_review.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
runs=m.find_runs(HERE/'evaluation/iteration-1')
assert len(runs)==6 and {r['eval_id'] for r in runs}==set(range(1,7))
for r in runs:
    assert r['grading']['case_status']=='충족';assert len(r['outputs'])==3
    assert all(x.get('type')!='error' for x in r['outputs'])
html=(HERE/'재시험_검토화면.html').read_text(encoding='utf-8');assert '\ufffd' not in html
result={'version':'1.0','completed_at':now,'state':'A2_known_case_regression_passed_A3_user_decision_pending','run_type':'known-case baseline procedure regression; no new skill','new_procedure_behavior_replay':'performed','content_grading':'performed_after_first_output_hash_seals','case_results':audit['case_results'],'known_required_cases_all_satisfied':True,'no_aggregate_accuracy_or_generalization_score':True,'content_analysis_retries_after_feedback':0,'method_changed_after_grading':False,'rerun_affected_cases_after_method_changes':'not_applicable_no_method_change_after_grading','fresh_selected_pngs':audit['total_selected_PNGs'],'fresh_base_pngs':174,'adaptive_native_pngs':54,'within_run_unique_source_times':188,'add_to_prior_unique_times':False,'analysis_contexts':3,'new_human_confirmation_requests':0,'new_human_approval':False,'prior_human_confirmations_preserved':True,'unseen_source_evaluation':False,'independent_human_grading':False,'coverage_gaps':[{'window':'EG-BIM 8.2~10.4s','event':'UI table selection row / thumbnail selection changes','status':'not_in_this_six_case_run','reference_status':'prior_AI_candidate_not_human_gold','action':'add a separate case when designing A3 tests; do not claim this run validated it'},{'event':'장헌0~5.9초 도입의 정지 대조 시험 및 전체 영상','status':'not_separately_retested_in_this_run; T05 only5.9~6.6s','action':'preserve current scope; whole-video/audio and expansion tests remain deferred'}],'acceptable_unknowns':['exact AE keyframe/handle/preset recovery','exact thin-light full route and mathematical easing','exact earliest/peak frames between supplied temporal samples'],'A3_authoring_ready':True,'A3_authoring_ready_scope':'only the six frozen A2 known-case requirements; recommendation to author a limited draft, not approval to start or overall motion accuracy','A3_started':False,'skill_created':False,'user_stage_decision':'pending per latest user instruction','recommended_next_step':'A3 limited skill draft plus these six regression cases and separate internal-UI-selection case, only after user stage decision','evidence_root':str(AN).replace('\\','/'),'report':str(REPORT).replace('\\','/'),'viewer':str(AN/'재시험_검토화면.html').replace('\\','/'),'audit':str(AN/'실행감사.json').replace('\\','/'),'workflow_skill':'anthropic-skill-creator baseline-only evaluation workflow; no with_skill condition or benchmark advantage claimed','limits':['same two already-exposed originals, one procedure run per case, separate contexts not unseen-source independence','local source PNGs/temporal crops, not full real-time native video playback','self-reported analyst access lists, no OS secrecy boundary or complete tool telemetry claim','root graded content using frozen references and selected source evidence; not independent human adjudication']}
write(HERE/'재시험_결과.json',result)
write(HERE/'경로_보존안내.json',{'original_execution_root':str(HERE),'canonical_snapshot_root':str(ROOT/AN),'rule':'Raw outputs/logs/seals retain original C paths and hashes. Resolve a missing C path by replacing the original_execution_root prefix with canonical_snapshot_root. Do not rewrite raw records.','snapshot_is_not_standalone_runtime':True,'runtime_and_source_dependencies':'Original videos remain at pinned D source paths; extractor depends on existing C phase01a-a2/prepare.py and isolated PyAV runtime; not a packaged standalone skill.'})
md='''# 01-A2 스킬 작성 전 재시험 결과

**사전에 고정한 여섯 재발 유형은 모두 필수 기준을 충족했습니다. A3의 제한된 초안 작성을 권고하지만, A3 착수와 스킬 생성은 하지 않았습니다. 다음 단계는 사용자가 결과를 보고 결정합니다.**

| 시험 | 확인한 내용 | 판정 |
|---|---|---|
| T01 · EG 3.5~5.5초 | E 조각별 좌→우 진입, 시간차, 후반 감속 | 충족 |
| T02 · EG 0~1.4초 | 본체와 얇은 빛 통과를 분리, 격자/보조 요소 관측 | 충족 |
| T03 · EG 1~3.8초 | 십자·점선 영역 확대와 영문 공개, 영역 축소 후 연한 문구 잔존 | 충족 |
| T04 · 장헌 6~18초 | 수주→매출→이익, 막대 상향·원형 시계 채움·숫자 증가와 감속 | 충족 |
| T05 · 장헌 5.9~6.6초 | 겹침 전환, 혼합 진행의 초반 빠름·후반 느림 | 충족 |
| T06 · EG 10.6~15.5초 | 기존 창 재배치·새 창 우향 진입·모델 우하향 확대·후속 광량 분리 | 충족 |

여기서 충족은 각 사건을 실제로 발견하고 방향·순서·관측량을 맞게 구분했다는 뜻입니다. T02의 빛 전체 경로·정확한 이징, T06 빛의 수학적 곡선, AE 키프레임/프리셋은 미확정으로 남겼습니다. 전반적인 누락률이나 새로운 영상에 대한 정확도 수치는 만들지 않았습니다.

## 이번에는 달라진 점

이전 대화·사용자 정정·사례별 답안을 전달하지 않은 세 분석 문맥에 중립 과제와 보완 절차를 제공했습니다. 주요 대상뿐 아니라 작은 선·테두리·빛·화면 내부를 조사하고, 정착 화면 역추적과 원본 크롭을 사용했습니다. 분석자의 최초 JSON과 한국어 서술을 먼저 해시로 고정한 후 원본/고정 기준으로 내용 채점했습니다. 채점 피드백을 받아 답을 고친 재실행은 없었습니다.

앞서 사용자 지적이 필요했던 E 조각·얇은 빛·십자·점선의 수축을 이번에는 추가 지적 없이 기록했습니다. T06의 반투명 회색 연결면 후보도 별도로 발견했습니다. 이 후보와 새 미세 관측을 기존 사람 승인에 자동 포함하지 않았습니다.

가감속은 이름만 붙이지 않고 관측량에 연결했습니다. E의 상단 오른쪽 끝은 약x1084@3.7초→1772@4.0초→2153@4.8초로 정착하며 등시간 이동량이 줄었습니다. 장헌 전환의 화면 혼합 proxy는6.1초 .524→6.2초 .825→6.3초 .959로 후반 변화가 줄었습니다. 이 값들은 렌더 표본의 근사치이며 실제 AE 속성값이 아닙니다. 장헌16초31억·48%는 카운트 중간 상태,18초55억·92%/39억·61%/5억·71%는 그 시점의 정착 상태로 구분했습니다.

## 남은 검증 공백

**EG-BIM8.2~10.4초의 표 선택행·썸네일 선택 변경은 이번 여섯 창에 포함되지 않았습니다.** T06의 “내부 유지”는10.6초 이후에만 적용됩니다. 이 구간까지 재시험했다고 쓰지 않습니다. A3 시험을 설계할 때 별도 내부 UI 변화 사례를 추가해야 합니다. 기존 관측은 AI 후보이며 사람 기준답안으로 승격하지 않았습니다.

이번은 이미 노출된 같은 두 원본에 대한 알려진 실패의 재시험입니다. 사례당 한 번의 분석, 같은 계열 모델, 작성자의 내용 채점이며 독립 사람 검수나 미노출 영상 시험은 아닙니다. 장헌 도입 전체의 정지 대조 시험, 전체 영상·오디오, A4/A5의 확대 검증도 이번 결과에 포함하지 않습니다. 작은 정지 대조는 T05의5.9~6.0초와 전환 후 표본으로만 다뤘습니다.

## 실행과 보존

- 새 추출228장: 기본174장 + 분석자가 요구한 원본 폭 추가54장. 이 실행 안의 원본 시점188개이며 이전 실행의 고유 시점 수에 단순 합산하지 않습니다.
- EG 원본 크기127장, 장헌 원본 크기42장, 장헌 절반 크기59장입니다. 확대/개요 시트·원본 크롭은 파생 자료로 따로 보존했습니다.
- 입력/기준/기존 사람 회신 해시, 원본 MP4 전후 해시, 추출 PNG 해시와 컨테이너 표본 시각 대응, 최초 분석본의 채점 후 무변경을 확인했습니다.
- T03의 첫 폴더 생성 오류는 디코딩 전 실패였고 재추출은 성공했습니다. 분석 중 SciPy 사용 불가는 NumPy 대체로 처리했으며 탐색 이력도 남겼습니다.
- 오디오는 청취·전사하지 않았고 SAR/정밀 색 범위와 원본 배율 전 프레임 재생은 검증하지 않았습니다. 토큰/실행 시간 telemetry는 도구가 제공하지 않아 추정하지 않았습니다.
- 같은 항목의 사람 확인을 다시 요청하지 않았습니다. 새 스킬·A3·외부 AI 분석 API·AE 조작은 실행하지 않았습니다.

세 분석 문맥은 대화 이력을 물려받지 않았지만 파일 접근은 절차로 분리한 것이며 OS 차단을 주장하지 않습니다. 분석자의 자료 열람 목록은 자체 기록입니다. 보존 사본의 원출력/로그는 원래 C 경로와 해시를 그대로 유지하며, 경로 대응 안내로 D 사본을 찾을 수 있습니다.

## 다음 단계 판단

고정한 A2 필수 사건에는 남은 중대 실패가 없어 **A3 초안 작성으로 넘어갈 근거는 마련됐습니다.** A3에서는 검증한 절차만 짧은 본문과 참조/보조 도구로 옮기고, 여섯 시험과 내부 UI 변경 시험으로 스킬 적용 전후를 비교하는 것이 적절합니다. 모든 영상의 누락 방지가 입증됐다는 뜻으로 읽으면 안 됩니다. 사용자 지시대로 이번에는 결과 보고까지만 수행했습니다.

'''
base=ROOT/AN
def link(label,path):return '['+label+'](<'+str(path).replace('\\','/')+'>)'
md+='근거: '+', '.join([link('결과 JSON',base/'재시험_결과.json'),link('6개 원출력·채점 검토 화면',base/'재시험_검토화면.html'),link('실행 감사',base/'실행감사.json'),link('착수 기준',ROOT/PRE/'01_착수판정기준.json')])+'.\n'
(HERE/'결과보고.md').write_text(md,encoding='utf-8')
write(HERE/'검토화면_파일확인.json',{'generated_by':str(spec.origin),'loaded_runs':6,'case_ids':[r['eval_id'] for r in runs],'embedded_outputs_per_run':3,'replacement_characters':0,'check':'data loading, JSON/text/image embedding and Korean encoding checked; no rendered-browser visual QA claimed','benchmark':'not produced; baseline condition only'})
print('report and six-case result prepared; A3 false')
