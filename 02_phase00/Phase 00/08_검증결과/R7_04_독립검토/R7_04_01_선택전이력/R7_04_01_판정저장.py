import json,hashlib
from pathlib import Path
O=Path(__file__).parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();e=json.loads((O/'R7_04_01_최종_원문대조.json').read_text(encoding='utf-8'))
j={'stage':'R7-4-1 현행대조/연결범위 설계','limited_completion_supported':e['all_static_checks_passed'],'unresolved_blocking_findings':[],'findings_fixed':[],
 'scope':{'included':['새3안내 전문과 착수확인/입력보존 목록·실제R2/R4/R5/R6 연결점의 기존계약 대조','R7-2/3 현재 참조/판본/해시·R6 현재 읽기전용조회','기존130파일과backup 바이트대조·3스킬/공통자료14파일 보존','4안의 위치/영향/권한범위 비교·실제CI회신과R7내용검수0 구분'],
 'excluded':['연결안 선택 승인·단계2 연결표/양식/도구 구현검수·단계3 정본등록/인계','새 외부이론 조사·기존스킬 재구성/실행·R8 평가·01-A 분석기 구현','실제 R4/R5 레코드내용/영상검수·사람 신원/회사/사용권한 인증']},
 'selection_snapshot':{'state':'awaiting_user_choice','recommendation':'A','selected_option':None,'scope':'A/B 별도목록, C/D 기존계약확장. A 권고를 승인으로 다루지 않음. 이후 실제회신/정책반영은 별도시점 증거 필요.'},
 'verification':{'static_conditions':e['total'],'static_passed':e['passed'],'protected_current_and_backup_count':130,'R7_reference_entries_checked':len(e['R7_reference_checks']),'source_hashes_unchanged_during_review':len(e['after_hashes']),'R6_current_valid':e['current_R6_query']['valid'],'performance_test':False},
 'existing_skill_preservation':{'custom_skill_count':3,'files_including_common_materials':14,'unchanged_at_this_snapshot':True},
 'current_actual_reply_scope':{'R6_recorded_answers':1,'CI_latest_material_units_covered':8,'CI_usage_guides_unresolved':8,'Sanha_Illustrator_original_absent':'既存ユーザー申述'.replace('既存ユーザー申述','기존 사용자 진술'),'new_R7_content_reviews':0,'company_approval':False,'identity_authenticated':False,'content_verified':False,'permission_granted':False},
 'nonblocking_followup_gates_for_stage2':['실제선택답변의 locator/원문/범위를 별도정책으로 고정하고 해당범위만 구현','별도품질결과에는 대상record/단위ID·판본·원문hash·검수범위·항목적용/필수선정이유·상태/미검수·근거와사람응답문맥을 명시','비적용/미상/자료없음·부분범위를 분리하고 기존R6회신·R4spatial보류를 우회하지 않음','향후도구는 입력pin/자기규격·반환직전현재성·실패시큐/표시정리·오프라인참조·타입/파서경계를 독립반례로 검수; 아직 구현통과 주장은 금지'],
 'primary_document_reading':'이번은 기존계약·신규3안내의 직접 로컬대조다. 새 외부원문조사/전체기존파일 의미재독/법적판정이 아님.130보존은 byte/hash 검사이며130전문정독 수가 아님.',
 'actual_human_content_review_performed':False,'actual_media_analysis_performed':False,'R7_4_complete':False,'R7_complete':False,'Phase00_complete':False,
 'snapshot_boundary':'현행대조5파일/130기존입력의 검토시점 판정. 사용자선택·문서/목록/상태의 후속변경을 현재 승인/미래불변으로 보증하지 않음.',
 'evidence':[{'path':str(O/n),'sha256':sha(O/n)} for n in ['R7_04_01_독립감사.py','R7_04_01_최종_원문대조.json']],
 'after_hashes':e['after_hashes']}
(O/'R7_04_01_최종판정.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# R7-4-1 독립 현행대조 판정

**현행대조·범위 설계에 한정해 완료를 지지한다. 미해결 차단 결함은 없다.**

3개 안내를 직접 읽고 R2의4단위, R4 통합v0.2의 대상/근거/시간·공간 및 spatial supported 보류, R5 별도 프로젝트초안, R6 실제 회신문맥과 대조했다. 130개 기존입력은 현파일과backup이 일치했고 검토 중135개 해시가 바뀌지 않았다. R7-2/3 참조24개와 작성확인의3개 출력hash가 현재파일과 일치한다. 정적 조건32/32는 이 문서·참조 정합성 결과이며 영상/모델 성능 성적이 아니다.

R6 현재조회는 valid다. 실제회신은1건으로 CI최신자료8단위만 확인하고 사용가이드8단위는 미확인이다. 산하 Illustrator원본 부재의 기존진술·한맥의 선택UI 참고정책도 유지된다. 실제기록내용/신원/권한/회사승인과 공간 supported는 false로 유지된다. 새 R7의 사람내용검수는0건이다. 이 두 사실은 문서에 올바르게 구분돼 있다.

A/B는 별도 R7 연결목록, C/D는 기존 R6/R4 계약확장이라는 비교가 명확하다. 현재 A는 추천이며 실제선택은 아직 없다. 도구구현/입력확인 방식 승인으로 처리하지 않았다. 이후 실제선택답변과 locator를 별도로 고정한 뒤 그 범위만 구현해야 한다.

다음 단계에서는 대상ID/판본·부분검수범위·근거/응답문맥·필수선정이유·미검수/비적용/보류·변경 후 stale/재검토를 구체화하고, 도구가 생기면 파서/현재성/권한승격 반례를 별도로 검수해야 한다. 이것은 후속 작업조건이며 이번 문서설계의 미해결 차단 결함으로 세지 않았다.

기존3개 스킬과 공통자료14파일은 보존됐다. 130개 보존검사는130개를 이번에 전문정독했다는 주장이 아니다. 새 외부이론조사·실제R4/R5레코드내용검사·스킬실행·R8 재평가·01-A 구현·전체Phase00완료는 하지 않았다. 최종판정과 after_hashes는 사용자선택/후속 문서변경 전의 스냅샷이다.
'''
(O/'R7_04_01_최종판정.md').write_text(md,encoding='utf-8')
for n in ['R7_04_01_최종판정.json','R7_04_01_최종판정.md','R7_04_01_최종_원문대조.json','R7_04_01_독립감사.py']:print(n.encode('unicode_escape').decode(),sha(O/n))
