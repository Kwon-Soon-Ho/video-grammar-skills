import json,hashlib
from pathlib import Path
O=Path(__file__).parent;read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();e=read(O/'R8_01_시험기반_최종대조.json')
j={'stage':'R8-1 행동시험 기반/인프라 보완 독립점검','limited_completion_supported':e['all_passed'],'unresolved_blocking_findings':[],
 'scope':{'included':['iteration1불완전fixture의쌍단위무효/누락보고·입력/출력/로그보존·준비코드이력한계','iteration2준비6사본의초기입력SHA/정규화task/실행SKILL사본·배치/필수8파일','기존C체커의읽기전용독립재검사:R7fixed참조·R6선언구조source_artifacts=False·지원catalogs검사','의도case3충돌과외부원본544/CI바이너리미확보의범위/실패분리'],
 'excluded':['수행중모델의작업품질·후보/구버전우위·전체6결과채점','시행agent의system/modelconfig/파일접근격리의기술인증','R6원문/CI전체artifact검사·루트외원본조회','실제미디어/모델성능·사용자실출력피드백·최종후보채택·D쓰기/새agent/수행자메시지']},
 'verification':{'infrastructure_conditions':e['static_or_infrastructure_conditions'],'passed':e['passed'],'paired_cases':3,'prepared_execution_runs':6,'prepared_non_skill_input_counts_by_case':[x['non_skill_input_count'] for x in e['case_pairs']],'normalized_tasks_equal':True,'required_files_per_fixture':8,'skill_path_relative_to_DB':'실행스킬/video-knowledge-curator','actual_old_two_parent_root_assumption_satisfied':True,'all_SKILL_source_copy_SHA_matched':True,'read_only_checker_probe_subprocesses':6,'no_uncaught_probe_exceptions':True,'catalogs_supported_checks_valid_in_all_six':True,'D_original152_unchanged':True,'not_skill_behavior_or_performance_counts':True},
 'infrastructure_failure_accounting':{'iteration1_confirmed_completed_model_attempts':2,'iteration1_other_four_not_executed':True,'iteration1_initial_arms_excluded_together_from_main_eligible_comparison':True,'exclusion_reason':'要求参照が不足'.replace('要求参照が不足','요청에필요한공통용어사전/자료검증/지식조회가누락된준비오류'),'exclusion_is_posthoc_recorded_infrastructure_remediation_not_pre_registered_rule':True,'initial_builder_byte_snapshot_available':False,'initial_inputs_outputs_omission_reports_and_transcripts_preserved':True,'candidate_unchanged_for_retry':True,'iteration2_initial_full_R6_probe_failed_and_raw_saved':True,'full_R6_preflight_probe_is_model_trial':False,'iteration2_new_model_attempts_planned':6,'actual_iteration2_completion_count_verified_by_this_review':None,'future_total_if_all_six_complete':'전체모델실행시도8/비교적격6/인프라무효2. preflight실행실패는별도이며9번째모델시행으로세지않음.','actual_video_trials':0},
 'scope_of_R6_validity':{'source_artifacts_false_explicit':True,'declaration_structure_valid_in_all_six':True,'full_original_artifact_identity_verified':False,'human_identity_or_company_authority_verified':False,'task_discloses_same_limit_and_no_out_of_root_asset_search':True,'not_claimed_full_reference_complete':'참조/기본도구를포함한이번큐레이터목적의text/선언구조시험사본.외부원문/자산전수완비아님.'},
 'case3_expected_negative':{'intentional_conflict_added_after_baseline_preflight':True,'both_arms_same_injected_bytes':True,'current_R7_check_valid':False,'classification':'입력의동일판본/hash충돌을다루는본래시험조건.인프라누락이나후보실패성적과동일시하지않음.','independent_before_injection_execution_recreated':False,'basis':'작성코드순서/fixture_preflight·현재case3의고정hash실패·쌍별초기SHA동일성을대조.동작중사본을복구/재고정하지않음.'},
 'metadata_limits':['dispatch.json의prepared_not_executed는준비시점snapshot이며현재실행상태의증거가아님. 실제agent완료/시도ID·입력/출력hash·실패이력은후속행동보고에서연결해야함.','same model/tools_requested는요청조건임.관측되지않은seed/내부모델설정/token은null로유지.','현재실행중인case의허용작업초안변경을준비입력동등성검사와섞지않음.이점검은before초기기록을기준으로함.'],
 'reviewer_actions':{'D_writes':False,'test_fixture_changes':False,'full_original_artifact_query':False,'executor_agents_contacted':False,'new_agents_spawned':False,'actual_behavior_outputs_scored':False,'iteration1_reports_read_scope':'누락/미수행고지와보존존재만확인.지식정리내용의정답률을채점하지않음.'},
 'remaining_gates':['전체수행결과가모이면입력/실제출력/허용delta·backup/판본/실제검사로그·충돌보류를행동으로채점','최종집계에는실제시도/적격/인프라무효/미실행분모를구분하고성공만남기지않음','R6문맥/원문미검증과실제사람검수·뷰어표시/피드백·최종채택을따로확인'],
 'R8_1_complete':False,'candidate_adopted':False,'actual_human_feedback_received':False,'actual_video_trials':0,'Phase00_complete':False,
 'evidence':[{'path':str(O/n),'sha256':sha(O/n)} for n in ['R8_01_시험기반_감사.py','R8_01_시험기반_최종대조.json']],
 'D_after_hashes':e['D_after_hashes'],'prepared_metadata_hashes':e['metadata_hashes']}
(O/'R8_01_시험기반_판정.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# R8-1 試験基盤の独立判定

'''.replace('試験基盤の独立判定','시험기반 독립 판정')+'''**이번 큐레이터의 제한된 시험기반 보완을 지지한다. 차단할 준비 오류는 발견하지 않았다.**

인프라조건23/23을확인했다. 3사례의old/new각사본은실행스킬을제외한준비입력bytes가같고공통파일수는각300/301/300개다. task도실행별절대경로를치환하면같다. 필수8파일·스킬사본SHA와동일상대배치를대조했고구버전의두폴더위루트가정도성립한다. 기존152개D입력은그대로다.

각C사본을별도Python과정으로읽기검사해지원catalogs검사는전부정상이며R6선언구조도source_artifacts=False로정상이다. R6원문544/CI전체바이너리확인은수행하지않았고양측task에같은한계/루트외자산조회금지가명시됐다. ‘제한된text/선언구조사본’이지전수자료가완비된운영DB복제본은아니다.

R7현재검사는사례1/2에서정상이고사례3에서는의도한동일판본레이아웃변조로실패한다. 사례3의사전preflight뒤주입순서와두arm의동일초기SHA를확인했다. 이충돌은본래시험조건이며인프라실패로제외하거나고정목록을새로만들어없애면안된다. 검토자가수행중fixture를수정/복구하지않았다.

iteration1은공통사전·조회/검사코드가빠진준비오류였다. 양측완료시도2건의누락보고/입력/출력/로그를남기고쌍전체를주비교에서제외하는것은타당하다. 다만이는사후에기록한인프라보완이며미리정해둔제외정책이라고쓰지않는다. 초기builder원문사본이없는점도공개돼있다. iteration2최초R6full검사실패는모델시행과별개의도구preflight이력으로보존됐다.

재시험6건이모두완료되면전체모델시도8·비교적격6·인프라무효2를구분해야한다. 현재이검토는실제재시험완료수를검증하지않았다. 준비dispatch의prepared_not_executed를현재실행상태로읽거나새preflight실패를추가모델시행으로세지않는다.

후속검토에서실제파일수정·허용delta/backup/판본·검사로그·충돌보류와누락/실패를채점해야한다. 동일모델/도구는요청조건이며미관측내부설정/token은null이다. 이번23조건은스킬성능이아니며수행agent에연락/새agent생성·D변경·원문자산조회·사람피드백/채택은하지않았다.
'''
(O/'R8_01_시험기반_판정.md').write_text(md,encoding='utf-8')
for n in ['R8_01_시험기반_판정.json','R8_01_시험기반_판정.md','R8_01_시험기반_최종대조.json','R8_01_시험기반_감사.py']:print(n.encode('unicode_escape').decode(),sha(O/n))
