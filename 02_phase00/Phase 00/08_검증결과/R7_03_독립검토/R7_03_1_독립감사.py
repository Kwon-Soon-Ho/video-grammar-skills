import json,hashlib,sys,re
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
f='13_품질검수/평가계획/';rels=[f+'00_진행방식_검토안.md',f+'01_정답과_판정단위.md',f+'02_표본과_유출방지.md','13_품질검수/06_평가계획_읽는순서.md',f+'진행방식_사용자결정.json','08_검증결과/R7_03_입력보존.json','08_검증결과/R7_03_1_작성확인.json'];pres=read(B/rels[-2]);w=read(B/rels[-1]);p=read(B/rels[4]);texts={r:(B/r).read_text(encoding='utf-8-sig') for r in rels};before={r:sha(B/r) for r in set(rels)|set(pres['protected_inputs'])};policy=texts[rels[0]];gold=texts[rels[1]];sample=texts[rels[2]];guide=texts[rels[3]]
backup=B/'backup/2026-10-15_R7_03_1_정답과표본/입력정본';rows=[{'path':r,'expected':h,'current':sha(B/r),'backup':sha(backup/r),'same':h==sha(B/r)==sha(backup/r)} for r,h in pres['protected_inputs'].items()]
checks={
 '110_current_backup_preserved':len(rows)==110 and all(r['same'] for r in rows),
 'four_distinct_options_recommendation':all('| '+x in policy for x in ['A 추천','B','C','D']),
 'actual_A_policy_recorded_with_locator':p['selected']=='A' and p['kind']=='workflow_policy' and bool(p['question_item_id']) and '사용자가 A를 선택했다' in policy,
 'A_does_not_approve_thresholds_company_or_01A':all(p[k] is False for k in ['thresholds_approved','company_approval','phase01a_execution_authorized_by_this_choice']),
 'no_real_samples_gold_or_trials':all(p[k]==0 for k in ['actual_sample_count','actual_gold_count','actual_trial_count']) and all(w[k]==0 for k in ['actual_media','actual_gold_items','actual_locked_groups','actual_trials']),
 'four_evaluation_axes_separate':all('| '+x+' |' in gold for x in ['구조/기록 계약','영상 분석 정확성','지식 적용/검토','실제 전달/업무 효과']),
 'past_static_and_skill_results_not_new_video_performance':'새 실영상 성적으로 합산하지 않는다' in gold,
 'R2_units_and_no_frame_pseudoreplication':'영상 전체→설명 구간→화면 상태→동작' in gold and '독립 영상 수로 세지 않는다' in gold,
 'render_transcription_preserves_original_error':'분석 전사는25' in gold and '원본을 몰래 정정하지 않음' in gold,
 'multiple_valid_alternatives_and_Unknown_reasons':all(x in gold for x in ['복수 허용 답안','단정 불가+이유/필요 확인','근거 충돌','자료 부족','적용 안 됨']),
 'gold_state_vs_output_outcome_separate':'다른 축이다' in gold and '모델 결과 통과/수정필요/보류/비적용' in gold,
 'matching_identity_and_duplicates':'대상 동일성·종류·구간·시간 기준' in gold and '여러 번 맞혔다고 세지 않음' in gold,
 'gold_and_allowed_input_isolated':'분석에 제공할 입력과 평가자만 보는 정답/근거를 분리' in gold and '영상만 볼 과제' in gold,
 'no_posthoc_gold_fitting_and_comparison_versions':'사후 고치는 것은 금지' in gold and '양쪽 비교 대상 모두 같은 새 버전' in gold,
 'raw_normalization_meaning_preserved':'원문 문자열은 보존' in gold and '소수점/부정어/법인명/단위·첨자' in gold,
 'observational_uncertainty_not_evaluation_tolerance':'관측 불확실성과 평가 허용오차는 다른 값' in gold and '사건 시작 정의' in gold,
 'arbitrary_numeric_thresholds_not_adopted':'null이다' in gold and '임의1프레임/IoU0.5' in gold,
 'independent_human_initial_gold_before_comparison':'동일 원본을 독립 검수하고 초기 답을 잠근 뒤 비교' in gold and '사람 검수가 완료되지 않았다' in gold,
 'operational_vs_challenge_frequency_separate':'실제 업무 빈도 표본과 분리 보고' in sample,
 'family_units_no_filename_hash_independence':'회사명·파일명·해시가 다르다는 이유만으로 독립 표본' in sample and 'source_family' in sample,
 'family_not_all_company_assets_merged':'모든 영상을 한 그룹으로 묶지는 않는다' in sample,
 'split_before_search_examples_and_prompt_tuning':'검색 DB·스킬 예시·프롬프트 조정 전에' in sample,
 'new_context_no_prior_answers_or_feedback':'별도 새 실행 문맥' in sample and '같은 대화에 공개한 정답을 숨겼다고 가정하지 않는다' in sample,
 'actual_lock_requires_control_logs_not_folder_hash':'접근/열람 로그·허용 검색 목록' in sample and '폴더명·해시만으로' in sample,
 'role_vs_exposure_and_challenge_derivative_leak':'사용/노출 단계' in sample and '과제 역할' in sample and 'A′' in sample and 'A도 미노출 검증 자료로 사용할 수 없다' in sample,
 'unexposed_scope_no_base_model_training_claim':'기반 모델의 사전학습' in sample and '전부 확인했다는 뜻이 아니다' in sample,
 'missing_conditions_no_generalization_and_sample_plan_review':'없는 조건은 미평가' in sample and '사람에게 표본 수/수치 계획을 검토받는다' in sample,
 'API_upload_not_authorized':'업로드/API 제공을 승인하지 않는다' in sample,
 'metrics_disagreement_retest_are_later':'다음 소단계는 평가 지표' in guide and '사람 의견 차이·중재·재시험' in guide,
 'implementation_and_actual_work_still_not_done':'01-A 실행 승인' in policy and '실제 분할·접근 통제·잠금은 수행하지 않았다' in sample,
 'current_output_hash_report_matches':all(sha(B/r)==h for r,h in w['outputs'].items()),
 'writer_status_not_false_pending_choice':('policy' not in w['state'] or 'policy_selected' in w or 'policy_choice' in w or 'selected' in w),
}
links=[]
for r,t in texts.items():
 if not r.endswith('.md'):continue
 for u in re.findall(r'\]\(([^)]+)\)',t):
  if not u.startswith(('http://','https://','#')):links.append({'file':r,'link':u,'exists':(B/r).parent.joinpath(u.split('#')[0]).resolve().is_file()})
checks['local_links_exist']=all(x['exists'] for x in links)
sys.path.insert(0,str(B/'07_실행도구'));import R6_통합조회 as q
current=q.inspect(B);checks['R6_current_query_valid']=current['valid'] is True
after={r:sha(B/r) for r in before};checks['source_unchanged_during_readonly_audit']=before==after
result={'scope':'R7-3-1 static gold/sample/operating-plan audit, not evaluation execution.','total':len(checks),'passed':sum(checks.values()),'all_static_checks_passed':all(checks.values()),'checks':checks,'protected_files':rows,'current_R6_query':current,'policy':p,'links':links,'read_depth':{r:'full_text_static_review' for r in rels},'before_hashes':before,'after_hashes':after,'actual_media_analyzed':False,'actual_human_gold_review_performed':False,'actual_locked_data':0,'actual_trials':0}
(O/'R7_03_1_최종_원문대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'total':len(checks),'passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v],'after_hash_count':len(after)},ensure_ascii=True))
