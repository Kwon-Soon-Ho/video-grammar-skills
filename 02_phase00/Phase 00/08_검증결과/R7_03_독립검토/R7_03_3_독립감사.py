import json,hashlib,re,sys
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
f='13_품질검수/평가계획/';rels=[f+'05_사람의견차이와_중재.md',f+'06_재시험과_비교.md',f+'07_실행전_검토목록.md','08_검증결과/R7_03_3_작성확인.json'];a,b,c=[(B/r).read_text(encoding='utf-8') for r in rels[:3]];w=read(B/rels[3]);pres=read(B/'08_검증결과/R7_03_입력보존.json');before={r:sha(B/r) for r in set(rels)|set(pres['protected_inputs'])};back=B/'backup/2026-10-15_R7_03_1_정답과표본/입력정본';rows=[{'path':r,'expected':h,'current_same':sha(B/r)==h,'backup_same':sha(back/r)==h} for r,h in pres['protected_inputs'].items()]
checks={
 '110_originals_and_backups_preserved':len(rows)==110 and all(x['current_same'] and x['backup_same'] for x in rows),
 'two_human_plan_not_assigned':'현재 두 사람이 배정/동의했다는 뜻이 아니다' in a,
 'solo_review_not_interrater_reliability':'단독 검토 초안' in a and '사람 간 신뢰도를 산출했다고 하지 않는다' in a,
 'two_AIs_not_two_people':'두 명의 실제 사람으로 세지 않는다' in a,
 'same_inputs_roles_blindness_limits':'같은 상태로 전달' in a and '블라인드가 불가능하면 제한' in a,
 'initial_answers_independent_and_fixed':'독립 기록 후 시각·버전을 고정' in a,
 'disagreement_types_fact_vs_fitness':'전사 사실과 전달 적합성의 차이를 섞지 않는다' in a,
 'adjudicator_not_automatic_truth_or_authority':'중재자가 있다는 사실만으로 원본 근거가 생기지 않는다' in a and '단순 다수결로 기술 사실이나 회사 권한을 승인하지 않는다' in a,
 'unresolved_RU_vs_confirmed_hold_RH':'자료 부족/미해결이면 R_U' in a and 'R_H로 별도 기록' in a,
 'missing_vs_explicit_hold_denominators':'미응답/누락은 일치도 불일치도 아니며' in a and '명시 보류는 판정 범주' in a,
 'matched_event_labels_not_whole_segmentation':'전체 구간 분할 신뢰도로 부르지 않는다' in a,
 'one_measurement_type_not_all_labels':'시간 경계는 경계 차이 분포' in a,
 'alpha_requires_scale_units_missing_and_software':'선택한 차이 함수와 소프트웨어/버전' in a,
 'no_fixed_alpha_0_8_threshold':'0.8 같은 고정 회사 합격선을 도입하지 않는다' in a,
 'alpha_no_pairs_or_zero_expected_difference_null':'기대 차이 분모가0이면 산출 불가/null' in a,
 'no_postadjudication_fake_initial_agreement':'초기 일치율100%' in a and '만들지 않는다' in a,
 'agreement_not_factual_truth':'같은 오답에 동의할 수도' in a,
 'model_judge_human_calibration_no_authority':'검수된 사람 판단으로 보정' in a and '모델 판정만으로 기술 사실' in a,
 'actual_reply_provenance_not_name_only':'실제 응답·초기 답안/해시/시각' in a and '사람의 이름만 적힌 파일' in a,
 'execution_configuration_complete':'시행/재시도/시간 제한·예산/성공 조건' in b,
 'unknown_model_configuration_preserved':'제공되지 않으면 미상' in b,
 'no_keys_private_chainofthought_collection':'API키/비밀·모델의 비공개 내부 추론은 수집하지 않는다' in b,
 'gold_changes_both_candidates_regraded':'비교 후보 모두 재채점' in b,
 'new_model_not_skill_only_effect':'스킬 하나의 효과' in b and '해석하지 않는다' in b,
 'fresh_context_and_state':'새 문맥/분리된 작업 상태' in b,
 'all_retries_preserved_not_best_only':'최고 결과만 고르는 것을 금지' in b and '새로운 독립 영상 표본이 아니다' in b,
 'locked_aggregate_feedback_also_leakage':'집계 숫자만 보고 튜닝해도 누출 위험' in b,
 'seen_lock_becomes_dev_need_new_family':'다른 적합 원본 묶음' in b and '노출된 개발/회귀 이력' in b,
 'no_sequential_testing_superiority':'통계적 보정은 설계하지 않았으므로' in b,
 'actual_work_effect_requires_counterlearning_and_total_cost':'순서/학습 효과' in b and '재작업·실패·대기 시간' in b,
 'future_review_4choices_no_arbitrary_thresholds':'4지선다·추천안' in c and '임의90%/1프레임/IoU0.5 안 씀' in c,
 'all_actual_counts_zero':all(w[k]==0 for k in ['actual_human_annotations','actual_adjudications','actual_trials']) and '모두0건' in c,
 'API_scope_separate_no_current_upload_request':'지금 자료 업로드를 새로 요구하지 않음' in c and '외부 API 업로드·사용권한은 별도' in c,
 'current_writer_hashes_match':all(sha(B/r)==h for r,h in w['outputs'].items()),
}
links=[]
for r,t in zip(rels[:3],[a,b,c]):
 for u in re.findall(r'\]\(([^)]+)\)',t):
  if not u.startswith(('http://','https://','#')):links.append({'file':r,'link':u,'exists':(B/r).parent.joinpath(u).resolve().is_file()})
checks['local_links_exist']=all(x['exists'] for x in links)
sys.path.insert(0,str(B/'07_실행도구'));import R6_통합조회 as q
current=q.inspect(B);checks['R6_current_query_valid']=current['valid'];after={r:sha(B/r) for r in before};checks['source_unchanged']=after==before
result={'scope':'R7-3-3정의문서정적검토. 실제사람/alpha/중재/평가시행없음','total':len(checks),'passed':sum(checks.values()),'all_static_checks_passed':all(checks.values()),'checks':checks,'protected_files':rows,'current_R6_query':current,'links':links,'actual_human_annotations':0,'actual_adjudications':0,'actual_trials':0,'before_hashes':before,'after_hashes':after}
(O/'R7_03_3_최종_원문대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'total':len(checks),'passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v],'after_hash_count':len(after)},ensure_ascii=True))

