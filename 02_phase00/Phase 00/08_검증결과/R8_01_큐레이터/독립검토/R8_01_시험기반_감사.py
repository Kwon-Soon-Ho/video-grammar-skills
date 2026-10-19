import json,hashlib,re,subprocess,sys
from pathlib import Path
O=Path(__file__).parent;W=O.parent/'R8_시험/video-knowledge-curator-workspace';B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=read(B/'08_검증결과/R8_00_입력보존.json')['source_hashes'];D_before={r:sha(B/r) for r in source};failure=read(W/'시험준비_실패와보완.json');equal=read(W/'동등조건_확인.json');rows=[];meta_paths=[W/'시험준비_실패와보완.json',W/'동등조건_확인.json']
probe_code='''import sys,json,importlib.util\nfrom pathlib import Path\nb=Path(sys.argv[1]);sys.path.insert(0,str(b/'07_실행도구'))\nimport R7_연결확인 as r7\nimport R6_사람검수 as human\nimport 資料검증\n'''.replace('資料','자료')+'''a=r7.inspect(b);h=human.inspect(b,source_artifacts=False);cat=자료검증.validate_catalogs()\nprint(json.dumps({'R7':a,'R6_declaration_only':h,'catalog_errors':cat,'full_original_artifact_check_invoked':False},ensure_ascii=True))'''
for case in sorted((W/'iteration-2').glob('eval-*')):
 pair=[]
 for arm in ['new_skill','old_skill']:
  run=case/arm/'run-1';db=run/'inputs/Phase00';meta=read(run/'fixture_before.json');pre=read(run/'fixture_preflight.json');dispatch=read(run/'dispatch.json');task=(run/'task.txt').read_text(encoding='utf-8');skillroot=db/'실행스킬/video-knowledge-curator';Dskill=B/('06_맞춤스킬/재구성후보/video-knowledge-curator' if arm=='new_skill' else '06_맞춤스킬/video-knowledge-curator')
  m={k:v for k,v in meta['files'].items() if not k.startswith('실행스킬/')}
  required=[{'path':p,'present':(db/p).is_file(),'matches_prepared_hash':sha(db/p)==meta['files'][p]} for p in pre['required_files']]
  copies=[{'relative':p.relative_to(skillroot).as_posix(),'copy_sha256':sha(p),'source_same':sha(p)==sha(Dskill/p.relative_to(skillroot))} for p in skillroot.rglob('*') if p.is_file()]
  result=subprocess.run([sys.executable,'-B','-c',probe_code,str(db)],capture_output=True,text=True,encoding='utf-8',errors='replace');parsed=read(run/'fixture_preflight_failure.json') if (run/'fixture_preflight_failure.json').exists() else None
  try:q=json.loads(result.stdout);err=None
  except Exception: q=None;err=result.stderr[:2000]
  norm=task.replace(str(run),'<RUN>')
  pair.append({'arm':arm,'run':str(run),'db':str(db),'non_skill_manifest':m,'normalized_task':norm,'preflight':pre,'required_files':required,'skill_copy':copies,'old_parent_depth_correct':skillroot.parents[1]==db,'task_hash_matches_dispatch':sha(run/'task.txt')==dispatch['task_sha256'],'fixture_manifest_hash_matches_dispatch':sha(run/'fixture_before.json')==dispatch['fixture_manifest_sha256'],'skill_entry_matches_dispatch':sha(skillroot/'SKILL.md')==dispatch['skill_entry_sha256'],'task_json_scope_matches_text':read(run/'eval_metadata.json')['prompt']==task,'tools_probe':q,'probe_exit_code':result.returncode,'probe_exception_or_error':err,'first_full_artifact_failure_preserved':parsed is not None and parsed.get('valid') is False,'preflight_is_prepared_snapshot_not_actual_run_state':dispatch['state']=='prepared_not_executed'})
  meta_paths += [run/x for x in ['fixture_before.json','fixture_preflight.json','dispatch.json','task.txt','eval_metadata.json']]
 row={'case':case.name,'same_prepared_non_skill_bytes':pair[0]['non_skill_manifest']==pair[1]['non_skill_manifest'],'same_normalized_task':pair[0]['normalized_task']==pair[1]['normalized_task'],'non_skill_input_count':len(pair[0]['non_skill_manifest']),'arms':pair}
 rows.append(row)
checks={
 'three_case_pairs_and_six_prepared_runs':len(rows)==3 and all(len(r['arms'])==2 for r in rows),
 'all_non_skill_prepared_bytes_equal':all(r['same_prepared_non_skill_bytes'] for r in rows),
 'task_same_except_run_specific_absolute_paths':all(r['same_normalized_task'] for r in rows),
 'reported_common_counts_300_301_300_match':sorted(r['non_skill_input_count'] for r in rows)==[300,300,301] and [r['non_skill_input_count'] for r in rows]==[x['non_skill_input_file_count'] for x in equal],
 'all_required_eight_files_present_and_initial_hash_match':all(len(a['required_files'])==8 and all(x['present'] and x['matches_prepared_hash'] for x in a['required_files']) for r in rows for a in r['arms']),
 'all_loaded_skills_equal_actual_D_version':all(all(x['source_same'] for x in a['skill_copy']) for r in rows for a in r['arms']),
 'same_skill_relative_layout_and_old_depth_assumption_satisfied':all(a['old_parent_depth_correct'] for r in rows for a in r['arms']),
 'prepared_task_manifest_and_skill_hashes_match_dispatch':all(all(a[k] for k in ['task_hash_matches_dispatch','fixture_manifest_hash_matches_dispatch','skill_entry_matches_dispatch','task_json_scope_matches_text']) for r in rows for a in r['arms']),
 'all_probe_subprocesses_no_uncaught_exception':all(a['probe_exit_code']==0 and a['probe_exception_or_error'] is None for r in rows for a in r['arms']),
 'catalogs_API_independently_available_and_valid':all(a['tools_probe'] is not None and a['tools_probe']['catalog_errors']==[] for r in rows for a in r['arms']),
 'R7_normal_cases_valid_case3_intentional_conflict_detected':all(a['tools_probe'] is not None and a['tools_probe']['R7']['valid'] is (not r['case'].startswith('eval-03')) for r in rows for a in r['arms']),
 'all_R6_declaration_only_structural_valid':all(a['tools_probe'] is not None and a['tools_probe']['R6_declaration_only']['structural_valid'] is True for r in rows for a in r['arms']),
 'no_full_original_artifact_validation_run_by_reviewer':all(a['tools_probe'] is not None and a['tools_probe']['full_original_artifact_check_invoked'] is False for r in rows for a in r['arms']),
 'full_artifact_limit_disclosed_same_task':all('미포함 자산을 읽으려고 시험 루트 밖으로 나가지 않는다' in a['normalized_task'] and '전체 원문/자산 검사를 이 사본에서 통과했다고 주장하지 말고' in a['normalized_task'] for r in rows for a in r['arms']),
 'prepared_preflight_scope_before_case3_is_explicit':all(a['preflight']['R6_full_original_artifact_check_performed'] is False and a['preflight']['deliberate_case3_conflict_applied_after_baseline_check'] is r['case'].startswith('eval-03') for r in rows for a in r['arms']),
 'iteration1_exclusion_is_pair_level_for_incomplete_fixture':failure['iteration-1']['state']=='excluded_from_main_comparison_incomplete_fixture' and len(failure['iteration-1']['completed_executor_runs'])==2,
 'iteration1_other_four_runs_not_executed':set(failure['iteration-1']['not_executed'])=={'eval-02/*','eval-03/*'},
 'candidate_not_modified_for_infrastructure_retry':failure['iteration-1']['skill_candidate_changed_for_retry'] is False,
 'initial_builder_not_reconstructed_or_falsely_archived':failure['iteration-2']['initial_builder_byte_snapshot_available'] is False and failure['iteration-2']['initial_fixture_inputs_and_results_preserved'] is True,
 'iteration2_preflight_fullartifact_failure_raw_preserved':rows[0]['arms'][0]['first_full_artifact_failure_preserved'],
 'six_new_paired_runs_plan_not_actual_video_trials':failure['iteration-2']['expected_paired_runs']==6 and failure['iteration-2']['actual_video_trials']==0,
}
# Preserve infrastructure-only omission evidence from iteration1; no content-quality grades.
old_omissions=[]
for arm in ['new_skill','old_skill']:
 run=W/'iteration-1/eval-01-회의메모_지식정리'/arm/'run-1';db=run/'inputs/Phase00';text=(run/'outputs/설명.md').read_text(encoding='utf-8');p=read(run/'fixture_before.json');old_omissions.append({'arm':arm,'has_preserved_output_and_transcript':(run/'outputs/설명.md').is_file() and (run/'transcript.md').is_file(),'three_files_missing_from_initial_manifest':all(x not in p['files'] for x in ['01_공통용어/공통용어사전.json','07_실행도구/자료검증.py','07_실행도구/지식조회.py']),'missing_scope_reported':'없어' in text and '미수행' in text,'md_sha256':sha(run/'outputs/설명.md'),'transcript_sha256':sha(run/'transcript.md')})
checks['initial_pair_missing_files_and_omission_reports_preserved']=all(all(x[k] for k in ['has_preserved_output_and_transcript','three_files_missing_from_initial_manifest','missing_scope_reported']) for x in old_omissions)
D_after={r:sha(B/r) for r in source};checks['original152_D_inputs_unchanged']=D_before==D_after and all(D_after[r]==h for r,h in source.items())
result={'scope':'R8-1 infra preparation audit only. Not output-quality grading or skill trial execution. Reviewer read-only probes of existing checker APIs used six C fixtures; no full artifact inspect.','static_or_infrastructure_conditions':len(checks),'passed':sum(checks.values()),'all_passed':all(checks.values()),'checks':checks,'case_pairs':rows,'initial_omission_evidence':old_omissions,'metadata_hashes':{str(p):sha(p) for p in meta_paths},'D_before_hashes':D_before,'D_after_hashes':D_after,'actual_behavior_outputs_scored':False,'reviewer_contacted_executor_agents':False,'reviewer_created_new_agents':False}
(O/'R8_01_시험기반_최종대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'total':len(checks),'passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v]},ensure_ascii=True))
