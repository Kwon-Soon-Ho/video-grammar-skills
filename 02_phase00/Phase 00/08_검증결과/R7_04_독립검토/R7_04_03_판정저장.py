import json,hashlib
from pathlib import Path
O=Path(__file__).parent;read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();e=read(O/'R7_04_03_최종_원문대조.json');f=O.parent/'R7_04_마무리.py';t=f.read_text(encoding='utf-8');procedure={'scope':'C마무리계획정적보조검토.이스크립트를D대상으로실행하지않음','source_path':str(f),'sha256':sha(f),'finding':'세판정의true만확인하던계획에는최신검토입력과현재파일동일성preflight누락','fix_observed':'최신3단계after_hashes전부현재대조/착수128불변+130backup/등록hash대조를첫D쓰기이전에실행.후속변경은허용8경로로제한하고별도old/new기록','preflight_present':"latest_review_hashes and all(sha(safe(BASE/p))==h" in t,'preflight_before_archive_and_first_save':t.index("latest_review_hashes and all")<t.index("archive=BASE/")<t.index("save('08_검증결과/R7_04_독립검토_보존목록.json'"),'post_review_allowlist_and_old_new':"<=allowed_after_review" in t and "R7_04_검토후_변경확인.json" in t,'actual_D_finalization_executed_by_reviewer':False}
(O/'R7_04_03_마무리계획_보조검토.json').write_text(json.dumps(procedure,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
j={'stage':'R7-4-3 인계·등록','limited_completion_supported':e['all_static_checks_passed'] and procedure['preflight_present'] and procedure['preflight_before_archive_and_first_save'] and procedure['post_review_allowlist_and_old_new'],'unresolved_blocking_findings':[],
 'findings_fixed':[{'id':'R7-4-3-PROCEDURE-1','scope':'미실행마무리계획의검토후변경통제','initial':'true판정만읽고D아카이브/현황변경시작;최신인계4문서현재hash미대조','fixed':'최신3단계after_hashes현재대조를첫쓰기전실행·허용상태/안내변경만old/new추적.기존1/2판정은당시이력','evidence':str(O/'R7_04_03_마무리계획_보조검토.json'),'execution_not_certified':True}],
 'scope':{'included':['현재인계/R8/01-A/사람준비4문서전문·읽기동선/링크·최소기록/사람범위','정본연결목록v0.3.15/버전목록v0.1.11의신규13종실물ID/version/path/SHA와기존행내용/순서·과거판본','착수130backup·의도변경등록2외현재128불변·3스킬14파일·2단계코드/문맥/양식불변','R7기반읽기확인과R6선언문맥의별도현재조회','후속마무리C코드의preflight/허용변경통제정적보조검토'],
 'excluded':['최종현황/완료상태갱신·아카이브/미실행마무리코드의D실행검증','실제R8스킬재구성/AnthropicCreator실행·01-A모델/분석/평가','실제영상내용/사람기준답안·중재·모델시행·회사/권한/신원인증·전체Phase00완료']},
 'verification':{'static_conditions':e['static_conditions'],'static_passed':e['static_passed'],'new_registered_artifacts_unique':13,'registration_rows_combined_two_lists':len(e['all_current_historical_registration_rows']),'note':'132는두등록목록의행합계이며132개신규정본/실험이아님.13종은두목록에각각연결됨.','prior_rows_order_and_content_preserved':True,'current_and_historical_registered_hashes_match':True,'original_backup_count':130,'original_current_unchanged_count':128,'intentional_changed_originals':['00_운영계약/정본과표시_연결목록.json','05_출처와검토/버전목록.json'],'R7_current_readonly_valid':e['R7_readonly_current']['valid'],'R6_separate_current_valid':e['R6_separate_current_query']['valid'],'source_unchanged_during_review':e['before_hashes']==e['after_hashes'],'after_hash_count':len(e['after_hashes']),'not_performance_or_video_trials':True},
 'authority_and_reading_limits':{'userA_draft_and_pilot_preserved':True,'R8_three_skill_purposes_preserved':True,'new_judgment_minimum_four_options_plus_recommendation':True,'actual_content_answer_not_forced_choice':True,'Anthropic_creator_current_instructions_and_separate_copy_are_future_requirement':True,'new_guide_is_not_generated_DB_view':True,'registration_does_not_mean_company_approval':True,'external_theory_new_research_performed':False,'all_130_existing_files_meaning_re_read_certified':False},
 'actual_state':{'actual_new_R7_content_reviews':0,'actual_media_samples':0,'actual_verified_gold':0,'actual_locked_groups':0,'actual_human_annotations':0,'actual_adjudications':0,'actual_model_trials':0,'actual_scores':None,'evaluation_numeric_decisions':None,'R6_actual_existing_reply':1,'CI_latest_material_units_covered':8,'CI_guide_units_unresolved':8,'actual_human_content_review_performed':False,'R8_skills_rebuilt':False,'phase01a_started':False,'company_approved':False,'permission_granted':False},
 'snapshot_boundary':'최종현황갱신/아카이브전145입력의시점판정.최신판정after_hashes를preflight로확인한후허용상태/안내만old/new로변경하고,최종R7/R6현재조회·등록hash·링크·130backup을별도마무리결과로확인해야함.과거1/2판정after_hashes는현재폴더불변보증이아님.',
 'remaining_gates':['검토후변경통제에따라R7한정완료현황/보고와증거아카이브를마무리하고새시점결과저장','R8세스킬은목적/입출력/실패조건별재구성·중간검토/새계약쓰기·기권/보존/복구·비교평가가남음','실제자료접수·내용담당/시청검수/권한범위·예비후수치결정은필요대상이생길때사람에게맡김','01-A는후속별도작업이며현재시작하지않음'],
 'R7_4_handoff_registration_review_limited_complete':True,'R7_final_status_update_performed':False,'R7_complete':False,'Phase00_complete':False,
 'evidence':[{'path':str(p),'sha256':sha(p)} for p in [O/'R7_04_03_독립감사.py',O/'R7_04_03_최종_원문대조.json',O/'R7_04_03_마무리계획_보조검토.json']],
 'after_hashes':e['after_hashes']}
(O/'R7_04_03_최종판정.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# R7-4 3단계 독립 판정

**인계·등록 범위의 한정 완료를 지지한다. 미해결 차단사항은 없다.**

4개 인계문서를 직접 읽고 기존계약/정책·실제자료상태와 대조했다. 정적43/43조건 통과, 신규13종의 ID·버전·경로·SHA 실물 일치와 두목록의 기존행 순서/내용·역사등록 보존을 확인했다. 두목록 전체132행의 현재/과거파일hash도 맞는다. 132는 목록행합계이며 신규자료132개나 실험수가 아니다.

착수130개 원문은backup에서 그대로이고 현재원문은 등록목록2개만 의도변경되어128개가 그대로다. 기존3스킬과공통자료14파일·2단계도구/문맥v0.1.3/양식v0.1.1도 유지됐다. R7기반조회와 별도R6현재조회는 정상이며, R6실제CI회신1건/최신성8단위·추가가이드8미확인을 새 R7내용통과로 바꾸지 않았다. 검토중145개 입력hash는 바뀌지 않았다.

R8의3스킬 재구성은 아직 계획이다. 현행Anthropic Skill Creator지침을 읽고 별도사본에서 목적/입출력/실패조건·참조/의존성/라이선스를 확인하며 소단계초안/중간목적검토/테스트/레드팀을 거치도록 인계했다. 기존A의draft·소량시범권한을 유지하고 과거11/12동률·8조건을 새규격호환/업무효과로 재사용하지 않는다.

01-A의 입력접수·분석구현/사람정답·예비후수치결정·다른원본잠금확인은 후속이다. 대표1편/추가1~2편은 입력교정출발제안이며 통계적으로충분한표본의주장이 아니다. 수치/운영판단에는4지선다와추천, 실제내용에는 구체대상/버전/근거와 자유답변을 받게 한다. 현재 실제표본/정답/잠금/사람초기답·중재/모델시행은0이고 성적·수치결정은null이다.

보조검토한 미실행마무리코드의 절차누락은 보완됐다. 세판정true만 읽고 진행하는 대신 최신3단계after_hashes를 첫D쓰기전에 대조하고, 등록/안내의 허용변경만old/new로 남긴다. 이 코드는 정적으로 읽었으며 D대상실행을 검증한 것은 아니다. 최종현황/보고/아카이브 뒤에는 새시점현재조회·등록hash·링크·backup을 별도로 확인해야 한다.

본판정은 최종갱신 전 스냅샷이다. 과거1/2판정과 새3단계판정을 한 시점의 폴더불변증명으로 합치지 않는다. R7최종현황갱신, R8실행·01-A·실제내용/권한/회사승인·전체Phase00완료는 이번에 수행하지 않았다.
'''
(O/'R7_04_03_최종판정.md').write_text(md,encoding='utf-8')
for n in ['R7_04_03_최종판정.json','R7_04_03_최종판정.md','R7_04_03_최종_원문대조.json','R7_04_03_독립감사.py','R7_04_03_마무리계획_보조검토.json']:print(n.encode('unicode_escape').decode(),sha(O/n))
