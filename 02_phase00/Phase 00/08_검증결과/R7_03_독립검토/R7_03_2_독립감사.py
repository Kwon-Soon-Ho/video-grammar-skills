import json,hashlib,re,sys
from fractions import Fraction as Q
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
f='13_품질검수/평가계획/';rels=[f+'03_지표와_분모.md',f+'04_판단보류와_미채점.md',f+'지표정의_정본.json','08_검증결과/R7_03_2_작성확인.json'];m=(B/rels[0]).read_text(encoding='utf-8');h=(B/rels[1]).read_text(encoding='utf-8');d=read(B/rels[2]);w=read(B/rels[3]);pres=read(B/'08_검증결과/R7_03_입력보존.json');before={r:sha(B/r) for r in set(rels)|set(pres['protected_inputs'])};backup=B/'backup/2026-10-15_R7_03_1_정답과표본/입력정본';rows=[{'path':r,'sha256':x,'current_same':sha(B/r)==x,'backup_same':sha(backup/r)==x} for r,x in pres['protected_inputs'].items()]
checks={
 '110_inputs_and_backups_same':len(rows)==110 and all(x['current_same'] and x['backup_same'] for x in rows),
 'all4_reference_states':set(d['reference_sets'])=={'R_A','R_H','R_U','R_N'},
 'reference_units_partition_explicit':'N_planned = N_A+N_H+N_U+N_N' in m and '배타·완전분할' in d['reference_partition'],
 'unresolved_gold_not_correct_abstention':'R_U를 ‘모델은 보류해야 한다’는 R_H로 바꾸지 않는다' in m,
 'allowed_input_justification_not_hidden_oracle':'허용되는 입력으로 정당화할 수 있는지' in m,
 'RU_disclosed_not_silent_exclusion':'R_U를 빼서 높은 숫자만 보고하지 않는다' in m and '미해결 필수 기준답안' in m,
 'all8_closed_outcomes':set(d['closed_slot_outcomes'])=={'TP','FP','FN','TN','A','X','M','F'},
 'one_closed_outcome_per_unit':'각 항목/시행은 하나' in d['partition'],
 'abstention_state_vs_quality_separate':'이유가 없는 보류도 이 상태에는 포함' in m and '적절한 보류 성공으로 세지 않는다' in m,
 'whole_failure_not_double_missing':'같은 항목을 M에도 중복 계수하지 않는다' in m,
 'contradictory_conclusion_invalid_once':'invalid_conflicting_conclusion' in m and 'TP/FN 양쪽에 중복 계수하지 않는다' in m,
 'all_error_denominator_keeps_unanswered_positives':'부당 비적용·누락·실패에 있는 실제 오류도 분모에 유지' in m,
 'zero_denominator_null_and_reason':d['zero_denominator']=={'value':None,'reason_required':True} and '양성이 없는 표본' in m,
 'conditional_risk_not_whole_accuracy':'보류/누락/실패를 숨긴 전체 정확도로 부르지 않음' in m,
 'RH_units_not_claim_count':'단위당0/1' in h and '하나라도 있는 단위 수' in h,
 'RH_mixed_response_no_correct_hold':'적절 보류 성공은0이고 단정 위반은1' in h,
 'RH_assertion_counts_separate':'단정 개수/유형은 별도 건수' in h,
 'EM7_8_match_corrected_units':d['rates'][6]['formula']=='units_on_R_H_with_appropriate_hold_and_no_unsupported_assertion/N_H' and d['rates'][7]['formula']=='units_on_R_H_with_any_unsupported_definitive_assertion/N_H',
 'extraction_instances_not_string_set':'목록/다중집합 P' in m and 'P를 수학적 집합으로 중복 제거하지 않는다' in m,
 'distinct_occurrences_and_gold_alternatives':'다른 시간/대상의 발생은 별개' in m and '각 필요한 발생에 대한 허용 대안 동치군' in m,
 'one_to_one_maximum_and_tie_rules':'일대일 최대 대응 수' in m and '동률 해소 순서' in m,
 'duplicate_predictions_count_false_positives':'TP1/FP2/FN0' in m and '정밀도1/3' in m,
 'parse_failure_precision_scope_not_asserted_total':'전체 정밀도가 확인됐다고 하지 않는다' in m,
 'known_gold_remains_recall_on_failure':'해당 실행의 누락 수/재현율 진단에 반영' in m,
 'classification_and_extraction_FP_not_combined':'FP는 단위가 다르므로 합산하지 않는다' in m,
 'matched_time_error_alone_not_full_tracking':'쉬운 매칭 항목만의 평균오차' in m and 'VFR에 고정fps' in m,
 'cluster_dependence_no_pseudo_N':'반복 시행을 독립 영상 N으로 늘리지 않는다' in m,
 'statistical_intervals_not_inherited_for_dependent_frames':'종속 프레임·군집 반복에 바로 적용하지 않는다' in m,
 'no_scores_thresholds_CI_method_yet':d['actual_runs']==0 and d['actual_scores'] is None and d['numeric_thresholds'] is None and d['confidence_interval_method'] is None,
 'human_decisions_not_auth_approval':'각 보류의 정당성은 실제 근거로 사람에게 맡긴다' in h and '회사 규칙/권한 승인으로 확대하지 않는다' in h,
 'writer_output_hashes_match':all(sha(B/r)==x for r,x in w['outputs'].items()),
 'synthetic_examples_not_trials':w['actual_runs']==0 and w['arithmetic_example_is_synthetic_not_run'] is True and '실행·채점한 적은 없다' in m,
}
links=[]
for r,t in [(rels[0],m),(rels[1],h)]:
 for u in re.findall(r'\]\(([^)]+)\)',t):
  if not u.startswith(('http://','https://','#')):links.append({'file':r,'link':u,'exists':(B/r).parent.joinpath(u).resolve().is_file()})
checks['local_links_exist']=all(x['exists'] for x in links)
sys.path.insert(0,str(B/'07_실행도구'));import R6_통합조회 as core
current=core.inspect(B);checks['R6_query_valid']=current['valid'];after={r:sha(B/r) for r in before};checks['source_unchanged']=after==before
# Arithmetic sanity only: no parser, model, matching algorithm, or evaluator implementation.
r=lambda n,z:None if z==0 else Q(n,z)
math=[('synthetic10_partition',2+1+4+1+2==10),('synthetic10_coverage',r(8,10)==Q(4,5)),('synthetic10_conditional_error',r(2,8)==Q(1,4)),('synthetic10_error_recall',r(2,4)==Q(1,2)),('synthetic10_wrong_pass',r(1,4)==Q(1,4)),('all_hold_condition_risk_null',r(0,0) is None),('all_hold_full_answer_rate_zero',r(0,10)==0),('zero_positive_recall_null',r(0,0) is None),('all_failure_full_recall_zero',r(0,4)==0),('duplicate1_of3_precision',r(1,3)==Q(1,3)),('RH_one_unit_three_assertions_binary_violation',r(int(3>0),1)==1)]
result={'scope':'정적지표설계/산술검산이며실제채점기나모델시험아님','total':len(checks),'passed':sum(checks.values()),'all_static_checks_passed':all(checks.values()),'checks':checks,'synthetic_arithmetic_sanity':{'conditions':len(math),'passed':sum(x for _,x in math),'cases':[{'name':n,'passed':x} for n,x in math],'not_actual_model_or_evaluator_run':True},'protected_files':rows,'current_R6_query':current,'links':links,'actual_runs':0,'before_hashes':before,'after_hashes':after}
(O/'R7_03_2_최종_원문대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'static_total':len(checks),'static_passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v],'arithmetic_total':len(math),'arithmetic_passed':sum(x for _,x in math),'after_hash_count':len(after)},ensure_ascii=True))
