import json,hashlib
from pathlib import Path
O=Path(__file__).parent;read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();e=read(O/'R8_00_최종_원문대조.json');initial=read(O/'R8_00_초기위험과_원문대조.json')
reading=list(initial['read_ledger'])
for row in reading:
 if row['path'].endswith('eval-viewer\\generate_review.py') or row['path'].endswith('eval-viewer/generate_review.py'):row['reading_depth']='selected initial~284lines(find/build/embed/previous/generate_html),main~380-end;_kill_portselected. HTTPrequesthandlerremainingnotfullyreviewed; noexecution'
reading.append({'path':r'C:\Users\User\.codex\skills\anthropic-skill-creator\eval-viewer\viewer.html','sha256':sha(Path(r'C:\Users\User\.codex\skills\anthropic-skill-creator\eval-viewer\viewer.html')),'reading_depth':'header1-20 and renderBenchmark~1115-1194 + locatorsearch of selectedfunctions; fulltemplate/JS/runtime not audited','code_executed':False})
findings=[{'id':'R8-ROOT','planning_correction_confirmed':True,'issue':'추가후보폴더·snapshot이동으로두폴더위DBroot오인','documented_response':'명시DBroot/실제규격·색인확인·old/new동일상대배치','runtime_fix_validated':False}, {'id':'R8-CONTEXT-NAME','planning_correction_confirmed':True,'issue':'fullhistory/공유outputs/동일skillname동시로드비교오염','documented_response':'부모대화없이동일모델/조건·지시상격리한계·매사례새agent·한절대경로·전역/기본전환R8-4','runtime_isolation_validated':False}, {'id':'R8-METRICS','planning_correction_confirmed':True,'issue':'공식aggregate의null→문자수/0,3회고정/발견순서delta/run누락으로잘못된성적','documented_response':'프로젝트관측수/null-safe정본·실패/보류/명시방향·공식기본출력효능정본배제','actual_aggregation_validated':False}, {'id':'R8-VIEWER','planning_correction_confirmed':True,'issue':'기본encoding/replace·script종료데이터삽입·외부Fonts/CDN·null통계fmtStat','documented_response':'공식static원본보존후별도표시사본UTF8/embeddedJSON경계escape·불필요외부참조제거·decode동일·원문대조·없는통계객체생략·실제피드백별도','actual_static_generation_or_HTML_runtime_validated':False}, {'id':'R8-META','planning_correction_confirmed':True,'issue':'뷰어게이트추가뒤착수확인의00/02SHA가구형','documented_response':'최초작성snapshot보존·현재14자료5개전체SHA갱신·최종동결160입력불변','current_hashes_validated':True}]
j={'stage':'R8-0 현행대조/진행계획','limited_completion_supported':e['all_static_checks_passed'],'unresolved_blocking_findings':[],'findings_fixed_or_planned_gates':findings,
 'scope':{'included':['R8순차진행/역할·후보/기존보존·기본전환계획·draft권한/사람피드백 경계','기존3SKILL/3참조·R3-3설계/이식범위와R7인계의현행차이','AnthropicCreator설치본SKILL/SOURCE/LICENSE와aggregate전문·선택viewer/템플릿/채점/스키마의정적위험','152기존입력/current/backup·Creator9파일/보존본SHA·현재R7/R6조회·새문서정합성'],
 'excluded':['R8-1신규후보생성·개별스킬메타검사/행동시험·old/new실제모델시행','공식aggregate/viewer코드실행·표시가공/HTML런타임/외부요청차단의실증','실제피드백접수·사용자최종채택·전역설치/기본전환','ClaudeCLI/SDK/API·영상/OCR/렌더·01-A·회사문법승인/전체Phase00완료']},
 'verification':{'static_conditions':e['static_conditions'],'static_passed':e['static_passed'],'preserved_inputs_current_and_backup':152,'old_custom_skills':3,'files_with_common_materials':14,'Creator_original_and_backup_hash_pairs':9,'current_R8_folder_output_files':5,'note':'14폴더현재5파일과착수확인1파일은별개. 6개14출력이있다고기록하지않음.','R7_current_readonly_valid':e['R7_current_readonly']['valid'],'R6_separate_current_valid':e['R6_separate_current_readonly']['valid'],'D_after_hash_count':len(e['after_hashes']),'D_sources_unchanged_final_frozen_review':e['before_hashes']==e['after_hashes'],'performance_trials':0},
 'independent_reading_ledger':reading,
 'source_license_observation':{'creator_source_commit':'683bc88e56f3e09ba94f7055977f3d3aa499f202','installed_SOURCE_license_spdx':None,'LICENSE_text_observed':'Apache License Version2.0 with2026Anthropicnotice','upstream_latest_or_original_bytes_certified':False,'new_legal_authority_judgment':False,'creator_code_executed_by_reviewer':False},
 'human_and_authority':{'existing_userA_draft_and_limited_pilot_reapproval_required':False,'new_purpose_or_final_operational_judgment_requires_concrete_four_options_and_recommendation':True,'actual_human_content_answer_not_inferred_from_static_feedback_or_blank_file':True,'actual_human_output_feedback_received':False,'company_approved':False,'permission_granted':False},
 'remaining_execution_gates':['첫스킬candidate에서DBroot/입출력/역할/권한·필수ref의실제구현과변경대상허용범위검토','fork없는old/new동일조건의분리fixture에서정상업무/실제draft변경/예외·기권/실패복구를시험하고모든실패·단위·미수집자원을보존','실제viewer생성전정적코드사용경로/사본가공을검증하고최종표시의문자열/외부참조·자원통계가원문과계약에맞는지확인','구체출력과비교근거를사람에게보여피드백을접수한후다음스킬로진행;미응답을승인으로만들지않음','세후보가있어도기본전환/새R7입력문맥은R8-4별도보존·현재성/인계검토전금지'],
 'actual_new_candidate_adopted':False,'actual_skill_behavior_trials':0,'actual_tokens':None,'actual_times':None,'actual_human_content_review_performed':False,'actual_video_trials':0,'R8_complete':False,'Phase00_complete':False,'phase01a_started':False,
 'snapshot_boundary':'보완후최종동결R8-0계획의시점판정.기술위험을발견/계획에게이트로반영한것이며후속실행구현/성과가통과한것아님.중간작성중hash불일치와기록은R8_00_보완중이력/최초작성snapshot에보존.후속상태갱신은별도시점으로관리.',
 'evidence':[{'path':str(O/n),'sha256':sha(O/n)} for n in ['R8_00_독립감사.py','R8_00_최종_원문대조.json','R8_00_초기위험과_원문대조.json','R8_00_초기위험.md']],
 'creator_file_comparisons':e['creator_file_byte_comparisons'],'after_hashes':e['after_hashes']}
(O/'R8_00_최종판정.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# R8-0 독립 판정

**현행대조·순차진행계획 범위에 한정해 완료를 지지한다. 남은 차단사항은 없다.**

정적31/31조건을 확인했다. 기존152입력과backup, 기존3스킬/공통자료14파일은 그대로다. Creator설치본/보존본9파일hash가 맞고 현재R7/R6읽기조회도 정상이다. 보완후동결160입력은 검토중변경되지 않았다. 14폴더의현재출력은5파일이며 착수확인파일은별도다. 이 숫자는 실행성능/실험수가 아니다.

기존스킬의두폴더위DBroot와추가후보폴더의충돌, baseline이동/fullhistory/동일이름오염, aggregate의null→문자수/0·3회고정/발견순서delta 등은 계획에서 바로잡았다. 정상업무/실제draft수정과기권/실패복구를 분리fixture에서동일조건으로시험하고작은시범을전체효과로확대하지않게했다. 기존A의목적/draft시범을다시승인받을필요는없다.

뷰어의UTF8문제뿐아니라script종료문구직접삽입·외부Fonts/SheetJS도 후속사용전게이트로남겼다. 공식static원본과표시가공사본을보존하고embeddedJSON을안전한경계로이스케이프한뒤decode동일/실제표시·외부참조제거를검증한다. 미수집통계객체는뷰어에도넣지않는다. 지금그코드를실행하거나표시가공/브라우저안전성을실증한것은아니다.

Creator SKILL/SOURCE/LICENSE·aggregate는직접읽었으며 viewer/템플릿·채점자·스키마는지정부분만읽었다. 원문이력/고정commit과실제Apache문구를확인한범위일뿐최신upstream/법적유효성/자산권한을인증하지않았다. 읽기깊이와SHA를JSON에명시했다.

문서보완중착수확인의출력hash가구형이었던문제는 최초작성snapshot을보존하고현재5출력SHA로갱신해해결했다. 중간검사도이력으로남겼다. R8-0정적통과는새스킬의실제동작이나효과를증명하지않는다.

다음R8-1에서후보/root/ref/쓰기경계·old/new행동/출력과사람피드백을따로확인해야한다. 첫스킬피드백을받기전다음스킬로넘기거나미응답을승인으로만들지않는다. 기본전환/새R7문맥은R8-4의별도검토이며R8·Phase00전체·01-A·실제영상/사람내용검수는아직완료하지않았다.
'''
(O/'R8_00_최종판정.md').write_text(md,encoding='utf-8')
for n in ['R8_00_최종판정.json','R8_00_최종판정.md','R8_00_최종_원문대조.json','R8_00_독립감사.py']:print(n.encode('unicode_escape').decode(),sha(O/n))
