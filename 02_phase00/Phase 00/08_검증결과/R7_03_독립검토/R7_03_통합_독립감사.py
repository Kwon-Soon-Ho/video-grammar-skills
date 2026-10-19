import json,hashlib,re,sys
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
f='13_품질검수/평가계획/'
rels=['05_출처와검토/R7_03_평가계획_조사기록.json',f+'항목별_평가준비표.json',f+'평가설계_정본.json',f+'08_정리된_판정예.md','08_검증결과/R7_03_연결작성확인.json']
r,c,p=map(lambda r:read(B/r),rels[:3]);t=(B/rels[3]).read_text(encoding='utf-8');w=read(B/rels[4]);pres=read(B/'08_검증결과/R7_03_입력보존.json');back=B/'backup/2026-10-15_R7_03_1_정답과표본/입력정본'
ref_objects=p['document_refs']+[p[k] for k in ['policy_ref','outcome_policy_ref','metrics_ref','coverage_ref','research_ref']]+r['local_contexts']+[c['criteria_ref']]
paths=set(rels)|set(pres['protected_inputs'])|{x['path'] for x in ref_objects};before={r:sha(B/r) for r in paths}
snapshot=O/'R7_03_통합_독립검토시점원문';snapshot.mkdir(exist_ok=True)
for rel in rels:
 dest=snapshot/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((B/rel).read_bytes())
protected=[{'path':r,'expected_sha256':h,'current_same':sha(B/r)==h,'backup_same':sha(back/r)==h} for r,h in pres['protected_inputs'].items()]
refs=[{'path':x['path'],'expected_sha256':x['sha256'],'actual_sha256':sha(B/x['path']),'same':sha(B/x['path'])==x['sha256']} for x in ref_objects]
criteria=read(B/c['criteria_ref']['path']);cards={x['id']:x for x in criteria['cards']};rows=c['rows'];ids=[x['criterion_ref'] for x in rows]
row_evidence=[]
for x in rows:
 q=cards.get(x['criterion_ref'],{})
 row_evidence.append({'id':x['criterion_ref'],'group_matches':x['group']==q.get('group'),'question_matches':x['question']==q.get('question'),'evidence_matches':x['planned_evidence']==q.get('required_evidence'),'human_role_matches':x['human_role']==q.get('human_review',{}).get('role'),'empty_actual_fields':x['applicable_to_future_suite'] is None and x['actual_case_ids']==[] and x['actual_reference_answer'] is None and x['actual_reference_state'] is None,'plan_not_test':x['coverage_state']=='not_collected_not_a_test_case','conditional_not_universal':'전26항목 일괄 의무 아님' in x['track_note'],'edge_conditions_count':len(x['planned_edge_conditions'])})
checks={
 'five_integration_files_read_and_snapshot_preserved':all(sha(snapshot/x)==before[x] for x in rels),
 '110_originals_and_backups_match_at_review_time':len(protected)==110 and all(x['current_same'] and x['backup_same'] for x in protected),
 'all_plan_research_criteria_hash_references_match':all(x['same'] for x in refs),
 'criteria_version_matches':c['criteria_ref']['version']==criteria['version'],
 'exact_26_unique_criterion_ids':len(ids)==len(set(ids))==26 and set(ids)==set(cards),
 'all_26_copied_fields_exact_not_new_rule':all(all(x[k] for k in ['group_matches','question_matches','evidence_matches','human_role_matches']) for x in row_evidence),
 'all_26_actual_fields_empty':all(x['empty_actual_fields'] for x in row_evidence),
 'all_26_plan_not_test_and_conditionally_selected':all(x['plan_not_test'] and x['conditional_not_universal'] for x in row_evidence),
 'all_26_edge_classes_are_planning_not_130_tests':all(x['edge_conditions_count']==5 for x in row_evidence) and c['kind']=='coverage_plan_not_dataset_or_gold',
 'coverage_actual_cases_zero':c['actual_test_case_count']==0 and w['actual_test_cases']==0 and w['actual_gold_items']==0,
 'planning_contract_not_executable_harness':p['kind']=='planning_contract_not_executable_harness',
 'all_actual_counts_zero':all(v==0 for v in p['actual_counts'].values()),
 'all_numeric_decisions_unset':all(v is None for v in p['numeric_decisions'].values()),
 'actual_scores_unset_company_and_01A_false':p['actual_scores'] is None and p['company_approved'] is False and p['phase01a_started'] is False,
 'nine_documents_00_through_08_pinned':len(p['document_refs'])==9 and all(any(Path(x['path']).name.startswith(f'{i:02}_') for x in p['document_refs']) for i in range(9)),
 'two_different_user_policies_not_conflated':p['policy_ref']['path']!=p['outcome_policy_ref']['path'],
 'workflow_A_confirmed_but_numeric_pending':'사용자A:' in p['workflow'] and '예비후구체검토' in p['workflow'],
 'critical_and_human_holds_not_offset':any('상쇄금지' in x for x in p['invariants']) and '수치 조건도 이 원칙을 우회하는 허용선이 아니다' in t,
 'twelve_examples_explicitly_hypothetical':len([x for x in t.splitlines() if x.startswith('| ')])-1==12 and '실제 시험을 하지 않은 설명용 예' in t and '시험 통과 건수로 세지 않는다' in t,
 'example_transcription_not_silent_correction':'원본을 몰래 보정해 전사를 오답으로 만들지 않음' in t,
 'example_source_family_and_derivative_exposure':'A그룹 미노출 성적 불가' in t and '잠금 미노출 성적으로 쓰지 않음' in t,
 'example_unresolved_gold_vs_correct_hold':'보류 정답R_H로 바꾸지 않음' in t,
 'example_abstention_null_and_mixed_response_unit_denominator':'조건부 오류율null' in t and '300%비율 금지' in t,
 'example_duplicate_occurrences_one_to_one':'일대일 매칭TP1·중복FP2' in t,
 'example_conflicting_conclusion_invalid_once':'무효출력F1회' in t,
 'example_no_postadjudication_fake_initial_agreement':'초기 독립 답 불일치를 보존' in t,
 'example_all_trials_and_both_candidates_regrade':'최초/모든 시행·실패/재시도' in t and '비교 양측을 같은 버전으로 재채점' in t,
 'example_CI_reply_not_usage_or_video_approval':'실제 시안/사용권한 검수는 별도' in t,
 'seven_external_sources_unique':len(r['external_sources'])==len({x['id'] for x in r['external_sources']})==7,
 'seven_existing_contexts_not_new_studies':len(r['local_contexts'])==7 and '기존 참조7개' in r['scope'],
 'source_depth_limits_and_no_remote_full_hash_claim':all(x.get('locator') and x.get('read_depth') and x.get('limit') and x['full_document_archived'] is False and x['remote_sha256'] is None for x in r['external_sources']),
 'weak_sources_explicitly_not_substantive':len(r['not_used_as_substantive_evidence'])==2 and '신규 연구로 중복 계수하지 않음' in r['scope'],
 'no_actual_media_evaluation':w['actual_media_evaluation'] is False,
}
sys.path.insert(0,str(B/'07_실행도구'));import R6_통합조회 as q
current=q.inspect(B);checks['R6_current_query_valid']=current['valid'];after={r:sha(B/r) for r in before};checks['sources_unchanged_during_review']=after==before
result={'scope':'R7-3통합5파일의 문서/참조/빈준비행/가상판정예 정적 감사. 실제평가/자료분석/사람검수 아님.','total':len(checks),'passed':sum(checks.values()),'all_static_checks_passed':all(checks.values()),'checks':checks,'row_comparisons':row_evidence,'reference_comparisons':refs,'protected_files':protected,'current_R6_query':current,'before_hashes':before,'after_hashes':after,'actual_media_evaluation_performed':False,'actual_human_content_review_performed':False,'model_trials_performed':0}
(O/'R7_03_통합_최종_원문대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'total':len(checks),'passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v],'refs':len(refs),'after_hash_count':len(after)},ensure_ascii=True))

