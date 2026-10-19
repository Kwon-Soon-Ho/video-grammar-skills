"""검토 완료된 증거의 현재 SHA를 고정한다. D나 수행 결과에는 쓰지 않는다."""
from pathlib import Path
import json,hashlib
O=Path(__file__).resolve().parent;C=O.parents[1];W=O.parent/'R8_시험/video-record-steward-workspace'
D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=read(O/'R8_02_최종파일근거.json');view=read(O/'R8_02_집계뷰어근거.json')
assert files['run_count']==10 and not files['completion_hash_errors'] and not files['output_json_errors'] and not files['positive_approval_flags'] and not files['candidate_hash_errors'] and not files['R7_pin_errors']
assert all(not r['unexpected_existing_changes'] and not r['deleted_existing_inputs'] and r['grade_present'] and r['grade_texts_match_fixed_criteria'] for r in files['rows'])
assert all(r['exact_checkpoint']['restored_byte_exact'] and r['legacy_unchanged'] for r in files['rows'] if r['case']==3)
assert view['embedded_data_equal_official_raw'] and not view['viewer_errors'] and not view['comparison_errors'] and not view['external_resource_tags'] and not view['final_actual_output_files_missing_from_display']
DH=files['D_source_hashes'];CH={**files['C_result_hashes'],**view['C_result_hashes']}
staleD=[p for p,h in DH.items() if sha(D/p)!=h]
staleC=[p for p,h in CH.items() if sha(C/p)!=h]
assert not staleD,staleD
assert set(staleC)<= {'phase00-build/R8_02_결과정리.py'},staleC
for p in staleC:CH[p]=sha(C/p)
for rel in ['00_운영계약/01_보존과버전_계약.md','14_스킬재구성/R8-2_기록관리자_구성안내.md']:
    DH[rel]=sha(D/rel)
extra=[W/'판본대조_단위검사.json',W/'검사도구_실패와보완.json',W/'시험준비이력/사실검사_줄바꿈_보완전/R8_02_실행결과_사실검사.py',O.parent/'R8_02_실행결과_사실검사.py']
failure=read(W/'검사도구_실패와보완.json')
assert sha(extra[2])==failure['before_checker_sha256']
for p in extra:CH[p.relative_to(C).as_posix()]=sha(p)
for p in O.rglob('*'):
    if p.is_file() and p.name!='R8_02_최종판정.json':CH[p.relative_to(C).as_posix()]=sha(p)
result={
 'date':'2026-10-15','candidate_version':'0.2.0-draft.3',
 'limited_completion_supported':True,
 'limited_completion_scope':'R8-2 후보 재구성·소량 합성 개발 비교·보완·출력/뷰어·레드팀 정리. 사람 출력 피드백은 대기.',
 'unresolved_blocking_findings':[],
 'actual_model_trials':10,'initial_trials':4,'final_trials':6,'model_trials_excluded_as_infrastructure_invalid':0,
 'final_case_conditions':{'new_skill':['8/8','8/8','6/6'],'old_skill':['7/8','8/8','6/6']},
 'initial_case_conditions':{'new_skill':['7/8','8/8'],'old_skill':['7/8','8/8']},
 'final_condition_totals':view['final_condition_totals'],
 'independent_file_observations':{'existing_input_changes_outside_request':0,'deleted_existing_inputs':0,'invalid_output_json':0,'positive_known_approval_flags':0,'completion_register_hash_mismatches':0,'candidate5_hash_mismatches':0,'old_canonical14_hash_mismatches':0,'R7_static130_hash_mismatches':0,'checkpoint_restore_byte_exact_both':True,'legacy_bytes_unchanged_both':True},
 'viewer_structural_observations':{'final_runs':6,'final_output_files':106,'previous_runs':4,'previous_output_files':63,'data_or_grading_mismatches':0,'external_resource_tags':0,'browser_render_or_click_test_performed':False},
 'scope_flags':{'candidate_adopted':False,'default_switched':False,'R8_2_human_output_feedback_received':False,'R8_complete':False,'Phase00_complete':False,'actual_video_performance_verified':False,'company_approved':False,'independent_skill_effect_proven':False,'R8_4_unseen_independent_check_complete':False,'postwrite_failure_or_concurrent_change_recovery_verified':False,'R6_R7_full_fixture_validation_performed':False,'phase01a_started':False},
 'retained_nonblocking_limits':['같은 알려진 사례를 보고 보완한 재시험이며 맹검·미사용 잠금 평가가 아님.','실제 저장 후 자동 rollback/복수 파일 부분 실패/외부 변경/복구 실패는 R8-4 잔여.','backup byte 동일성은 직접 확인했고 실제 생성 순서·작업 주체는 로그/자기보고와 구분.','R4/R5 실제 검사 재실행은 채점자의 별도 근거를 읽었고 이 최종 레드팀이 시험 수를 중복 합산하지 않음.','실행 중 임시 변경 전체와 외부 행위 부재를 최종 파일만으로 인증하지 않음.','초기 요청문구 해석 한계·추가 R1 근거 전달의 비맹검 이력 유지.','main CRLF 검사 코드 오류, 실행자 동일 시행 내 KeyError 수정, 독립 감사 도구 키 가정 오류를 각각 보존하고 모델 시행 제외로 세지 않음.'],
 'publication_review':{'script':'phase00-build/R8_02_결과정리.py','latest_own_run_KeyError_disclosure_reviewed':True,'planned_navigation_and_status_documents':5,'requires_separate_post_publication_preservation_receipt':True,'R8_3_before_user_output_feedback_not_started':True},
 'D_source_hashes':DH,'C_result_hashes':CH,
 'reviewer_D_write':False,'reviewer_executor_or_grader_rerun':False
}
(O/'R8_02_최종판정.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'limited_completion_supported':True,'unresolved_blocking_findings':[],'D_source_hash_count':len(DH),'C_result_hash_count':len(CH),'updated_publication_script_hash':CH['phase00-build/R8_02_결과정리.py']},ensure_ascii=True))
