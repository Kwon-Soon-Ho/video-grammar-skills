import json,hashlib,re,sys
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
f='13_품질검수/연결과인계/';rels=[f+'00_R7-4_진행안내.md',f+'01_현재기반과_연결범위.md',f+'02_연결방식_검토안.md','08_검증결과/R7_04_01_입력보존.json','08_검증결과/R7_04_01_착수확인.json',f+'연결방식_사용자결정.json','08_검증결과/R7_04_01_최초작성_스냅샷.json'];a,b,c=[(B/r).read_text(encoding='utf-8') for r in rels[:3]];pres=read(B/rels[3]);w=read(B/rels[4]);policy=read(B/rels[5]);initial_writer=read(B/rels[6]);before={r:sha(B/r) for r in set(rels)|set(pres['source_hashes'])}
back=B/'backup/2026-10-15_R7_04_1_현행대조/입력정본';protected=[{'path':r,'sha256':h,'current_matches':sha(B/r)==h,'backup_matches':sha(back/r)==h} for r,h in pres['source_hashes'].items()]
snapshot=O/'R7_04_01_A선택후원문';snapshot.mkdir(exist_ok=True)
for rel in rels:
 dest=snapshot/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((B/rel).read_bytes())
refrows=[]
def walk(x,owner):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str):
   p=B/x['path'];refrows.append({'owner':owner,'path':x['path'],'exists':p.is_file(),'hash_matches':p.is_file() and sha(p)==x['sha256']})
  for v in x.values():walk(v,owner)
 elif isinstance(x,list):
  for v in x:walk(v,owner)
for r in ['13_품질검수/품질항목_정본.json','13_품질검수/평가계획/평가설계_정본.json','05_출처와검토/R7_03_평가계획_조사기록.json']:walk(read(B/r),r)
links=[]
for r,t in zip(rels[:3],[a,b,c]):
 for u in re.findall(r'\]\(([^)]+)\)',t):
  if not u.startswith(('http://','https://','#')):links.append({'file':r,'link':u,'exists':((B/r).parent/u).resolve().is_file()})
checks={
 'seven_review_files_preserved_in_C':all(sha(snapshot/r)==before[r] for r in rels),
 '130_existing_sources_and_backups_match':len(protected)==130 and all(x['current_matches'] and x['backup_matches'] for x in protected),
 'writer_four_outputs_current':len(w['outputs'])==4 and all(sha(B/r)==h for r,h in w['outputs'].items()),
 'writer_not_actual_video_or_01A_or_skill_execution':w['actual_new_reviews']==0 and w['actual_video_analysis'] is False and w['phase01a_started'] is False and w['existing_R8_skills_rebuilt'] is False,
 'current_quality_plan_nested_references_match':all(x['exists'] and x['hash_matches'] for x in refrows),
 'three_custom_skills_and_common_14_files_preserved':len([x for x in protected if x['path'].startswith('06_맞춤스킬/')])==14 and len([x for x in protected if x['path'].startswith('06_맞춤스킬/') and x['path'].endswith('/SKILL.md')])==3,
 'stage1_not_R7_or_Phase00_completion':'R7 전체/Phase00은 아직 미완료' in a,
 'no_actual_quality_or_video_or_human_content_review':'실제 영상/기준답안/평가/사람 내용 검수는 아직 없다' in a,
 'no_existing_contract_decision_changes':'자동 변경하지 않는다' in a,
 'four_R2_units_not_frame_or_cut_substitution':'프레임=화면상태/컷=설명구간으로 자동 대체' in b,
 'R4_refs_not_guess_or_spatial_supported_release':'누락 필드를 추정·spatial supported 보류 해제' in b,
 'R5_selection_not_official_CI_or_UI_mandate':'관측색/초안의 회사 공식화·CI 자동 재색칠' in b,
 'R6_reply_scope_and_old_context_not_transferred':'오래된/다른 문맥 답변 이식' in b,
 'past_query_saved_JSON_not_current':'저장된 과거 조회 JSON은 그때의 스냅샷' in b and '도구를 다시 실행해야 한다' in b,
 'structure_hash_not_truth_identity_company':'원본 내용·사람 신원·회사 승인 인증이 아니다' in b,
 'CI_latest8_and_Sanha_noAI_actual_reply_distinct':'8회사 제공CI 최신성·산하 AI원본 부재는 이미 사용자 답변' in b,
 'conditional_unknowns_not_global_block':'쓰지 않는 회사/스타일 때문에 전체 작업을 일괄 차단하지 않는다' in b,
 'actual_CI_reply_not_new_R7_content_review':'기존 R6의 실제 CI 회신과 R7의 새 내용검수0건을 혼동하지 않는다' in b,
 'historical_static_scores_not_new_video_performance':'정적 문서 검사 수는 새 영상 평가 성적이 아니다' in b,
 '26_conditional_criteria_not_universal':'전26항목 일괄 의무화' in b,
 'version_history_and_old_hash_retained':'과거 항목/판본을 덮어 지우지 않고' in b and '과거 hash를 보존' in b,
 'four_options_A_B_separate_C_D_existing_extension':all('| '+x in c for x in ['A 추천','B','C','D']) and 'R7 별도 JSON' in c and 'R6 검수 문맥/규격' in c and 'R4 통합 기록 안' in c,
 'user_A_choice_preserved_with_locator_not_content_approval':policy['selected']=='A' and policy['kind']=='workflow_policy' and policy['question_item_id'] and policy['company_approved'] is False and policy['actual_content_review'] is False and policy['actual_video_analyzed'] is False and w['selected_mode']=='A' and '사용자가 A를 선택했다' in c,
 'initial_writer_preserved_as_history':initial_writer['outputs'][f+'02_연결방식_검토안.md']=='a688e24ebfcf0dfb9d003f6b8957a188be6df4c081ff99c07db9f2ff67919636',
 'A_tool_scope_readonly_refs_not_quality_or_approval':'영상 디코딩/OCR·자동 의미 판정/품질 점수·스킬 실행·DB 자동 수정·검수 승인 기능이 없다' in c,
 'R7_tool_not_substitute_R6_record_inspection':'R7 도구 하나로 R6/실제 기록 검사까지 통과시켰다고 하지 않는다' in c,
 'future_reviews_have_target_version_evidence_applicability_wait_history':'대상·버전·근거·적용 이유·상태·사람 대기·수정/재검토 이력' in c,
 'local_links_exist':all(x['exists'] for x in links),
}
sys.path.insert(0,str(B/'07_실행도구'));import R6_통합조회 as q
current=q.inspect(B);checks['current_R6_query_valid']=current['valid'];checks['actual_R6_reply1_CI_latest8_guide8_unresolved']=current['recorded_answer_count']==1 and current['active_declared_answer_count']==1 and len(current['companies'])==8 and all(x['latest_materials']=='user_statement_recorded' and x['additional_ci_guide']=='unresolved' for x in current['companies']);checks['R6_no_actual_record_content_or_authority_promotion']=all(current[k] is False for k in ['actual_r4_r5_records_validated','actual_video_analyzed','spatial_supported_unlocked','identity_authenticated','content_verified','company_approved','permission_granted','operational_release']);checks['existing_hanmac_UI_optional_preserved']=current['hanmac_design']['source_selection']['ui_mandatory'] is False;after={r:sha(B/r) for r in before};checks['source_unchanged_during_review']=after==before
result={'scope':'R7-4-1착수/현행연결범위 문서설계 정적 감사. 신규도구구현/외부원문추가조사/실제내용검수 아님.','total':len(checks),'passed':sum(checks.values()),'all_static_checks_passed':all(checks.values()),'checks':checks,'protected_files':protected,'R7_reference_checks':refrows,'links':links,'current_R6_query':current,'before_hashes':before,'after_hashes':after,'actual_new_quality_reviews':0,'actual_human_content_review_performed':False}
(O/'R7_04_01_최종_원문대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'total':len(checks),'passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v],'refs':len(refrows),'hashcount':len(after)},ensure_ascii=True))


