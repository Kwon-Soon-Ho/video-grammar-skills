import json,hashlib,sys,re
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent;O.mkdir(exist_ok=True);read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f='14_스킬재구성/';rels=[f+n for n in ['00_R8_진행안내.md','01_현황과_차이.md','02_도구와_이식범위.md','도구와이식_근거목록.json','진행상태.json']]+['08_검증결과/R8_00_입력보존.json','08_검증결과/R8_00_착수확인.json','08_검증결과/R8_00_최초작성_스냅샷.json'];a,b,c=[(B/r).read_text(encoding='utf-8') for r in rels[:3]];basis=read(B/rels[3]);status=read(B/rels[4]);pres=read(B/rels[5]);w=read(B/rels[6]);src=pres['source_hashes'];back=B/'backup/2026-10-15_R8_00_현행대조/입력정본';before={r:sha(B/r) for r in set(rels)|set(src)}
originals=[{'path':r,'expected_sha256':h,'current_same':sha(B/r)==h,'backup_same':sha(back/r)==h} for r,h in src.items()]
creator=[]
for name,item in basis['files'].items():
 p=Path(item['original_path']);saved=B/item['saved_path'];creator.append({'name':name,'original_path':str(p),'saved_path':item['saved_path'],'sha256':item['sha256'],'original_same':sha(p)==item['sha256'],'backup_same':sha(saved)==item['sha256']})
links=[]
for r,t in zip(rels[:3],[a,b,c]):
 for link in re.findall(r'\]\(([^)]+)\)',t):
  if not link.startswith(('http:','https:','#')):links.append({'source':r,'link':link,'exists':((B/r).parent/link).resolve().is_file()})
checks={
 '152_previous_inputs_and_backups_preserved':len(originals)==152 and all(x['current_same'] and x['backup_same'] for x in originals),
 'old_three_skills_common14files_unchanged':len([x for x in originals if x['path'].startswith('06_맞춤스킬/')])==14 and all(x['current_same'] for x in originals if x['path'].startswith('06_맞춤스킬/')),
 'creator_nine_original_and_backup_file_hashes':len(creator)==9 and all(x['original_same'] and x['backup_same'] for x in creator),
 'installed_commit_source_not_latest_or_license_null_fabrication':basis['creator_source']['commit']=='683bc88e56f3e09ba94f7055977f3d3aa499f202' and basis['creator_source']['license_spdx'] is None and 'upstream 최신본을 확인했다고 하지 않는다' in c,
 'license_explicit_text_not_legal_company_certification':'Apache' in basis['license_text_observed'] and '서비스 조건의 승인은 별개' in c,
 'staged_sequential_skills_then_transition':all(x in a for x in ['R8-0','R8-1','R8-2','R8-3','R8-4']) and '사람 피드백을 먼저 다룬 뒤 다음 스킬' in a,
 'candidate_separate_same_name_old_fixed130_maintained':'재구성후보/<동일 스킬명>/' in a and '기존 고정 목록을 자동 재생성' in a,
 'actual_dbroot_not_parent_depth_in_candidate':'작업에서 명시한 DB 루트를 우선' in b and '실제 규격/색인 확인' in b,
 'single_absolute_skill_path_no_global_or_default_switch':'하나만 절대 경로로 읽고 전역/자동 발견 설정을 바꾸지 않는다' in a,
 'fresh_context_same_conditions_and_independence_limits':'부모 대화 없이 같은 모델/설정' in a and '상대 스킬·예상 답안/채점표·레드팀 결론은 열람하지 않는다' in a and '지시상 격리' in a,
 'baseline_topology_equal_and_pair_run_slots_honest':'같은 상대 위치에 스킬' in a and '슬롯 제한 때문에 사례별 old/new 쌍' in a and '앞선 시행 대화가 다음 사례에 전달되지 않도록' in a,
 'authorized_actual_small_draft_writes_not_just_documentation':'실제 draft 파일 변경도 포함' in a and '허용 변경/backup/diff' in a,
 'normal_work_failure_abstention_and_recovery_planned':'실제 수정·검증은 생략하지 않는가' in b and '실패와 복구' in a,
 'role_specific_tests_not_all_conditions_claimed':'세 스킬 전체의 누락 점검표' in b and '모든 조건을 검증했다고 하지 않는다' in b,
 'development_regression_and_unused_test_separate':'미사용 확인 자료를 구분' in a and '공개한 예를 잠금 자료라 부르지 않는다' in a,
 'draft_authority_A_not_repeated_and_newjudgments_fourchoices':'같은 목적/draft 권한/기존 소량 시범 A는 다시 승인받지 않는다' in a and '최소4지선다와 추천안' in a,
 'R3_conditional_transfer_and_blocked_sources_not_copied':'직접/파생 이식하지 않는다' in c and '외부 SKILL 전체/코드·폰트·이미지 묶음을 복사하지 않는다' in c,
 'UI_Taste_not_company_video_mandate':'영상 공통 규칙으로 만들지 않는다' in c and '정지/등속/반복·텍스트 단독·대칭·한국어/SI·CI를 일괄 금지' in b,
 'aggregate_null_charcount_defaults3_and_direction_limit_explicit':'문자 수를 대신' in a and '반복 수3고정' in c and '탐색순서delta' in c and '실패/보류·명시 비교 방향' in a,
 'no_missing_time_tokens_invented_or_viewer_metrics':'제공되지 않으면 null/미수집' in a and '시간/token이 없으면 뷰어에도 해당 통계를 넣지 않는다' in a,
 'no_Claude_CLI_SDK_API_or_trigger_accuracy_claim':'Claude CLI 기반 자동 트리거 최적화는 실행하지 않' in a and '단순 설명문 정적 대조를 실제 자동 호출률로 제시하지 않는다' in a,
 'Codex_model_not_Claude_performance':'실행 모델은 이 Codex 환경' in a and 'Claude 모델의 성능을 시험했다고 하지 않는다' in a,
 'viewer_unsafe_script_boundary_and_external_refs_gate':'script 종료 경계 문자를 이스케이프' in c and '외부 font/script 참조를 제거' in c and 'JSON을 해독한 원문 내용은 같아야' in c,
 'static_UTF8_original_display_and_human_not_fabricated':'PYTHONUTF8=1' in c and '원문대로 들어 있는지 대조' in c and '사람이 검수했다는 기록을 만들지 않는다' in c,
 'new_status_no_adoption_feedback_completion_or_video':status['R8_complete'] is False and status['Phase00_complete'] is False and status['phase01a_started'] is False and status['new_candidate_adopted'] is False and status['human_feedback_received'] is False and status['actual_video_analysis_trials']==0,
 'R81_plan_R82_R83_R84_not_started':status['stages']['R8-1']=='planned' and all(status['stages'][k]=='not_started' for k in ['R8-2','R8-3','R8-4']),
 'current_all_five_R8_files_hashes_match':len(w['outputs'])==5 and set(w['outputs'])=={f+x.name for x in (B/f).iterdir() if x.is_file()} and all(sha(B/r)==h for r,h in w['outputs'].items()),
 'local_links_exist':all(x['exists'] for x in links),
}
sys.path.insert(0,str(B/'07_실행도구'));import R7_연결확인 as r7;import R6_통합조회 as r6
q7=r7.inspect(B);q6=r6.inspect(B);checks['R7_current_readonly_valid']=q7['valid'];checks['R6_separate_current_readonly_valid']=q6['valid'];after={r:sha(B/r) for r in before};checks['D_review_inputs_unchanged']=before==after
snap=O/'R8_00_검토시점원문'
for r in rels:
 p=snap/r;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((B/r).read_bytes())
result={'scope':'R8-0 현행대조/계획정합성 정적감사.새후보/행동평가/Creator도구실행/사용자피드백검증아님','static_conditions':len(checks),'static_passed':sum(checks.values()),'all_static_checks_passed':all(checks.values()),'checks':checks,'preserved_originals':originals,'creator_file_byte_comparisons':creator,'links':links,'R7_current_readonly':q7,'R6_separate_current_readonly':q6,'before_hashes':before,'after_hashes':after}
(O/'R8_00_최종_원문대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'total':len(checks),'passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v],'hashcount':len(after)}))


