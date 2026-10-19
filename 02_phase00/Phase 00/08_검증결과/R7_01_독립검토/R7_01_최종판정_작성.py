import json,hashlib,re
from pathlib import Path
BASE=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');OUT=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
a=read(OUT/'R7_01_최종_원문대조.json');f='13_품질검수/';texts={n:(BASE/f/n).read_text(encoding='utf-8') for n in ['00_R7_단계별진행안내.md','01_기존자료와_보완목록.md','02_품질판정방식_검토안.md']};p=read(BASE/f/'판정방식_사용자결정.json');alltext='\n'.join(texts.values());choice=texts['02_품질판정방식_검토안.md'];old=read(OUT.parent/'R6_독립검토/R6_04_최종판정.json');oldcheck={r:sha(BASE/r)==h for r,h in old['after_hashes'].items()}
checks={
 'selected89_current_backup_hashes_match':a['existing_selected_files']==89 and a['existing_current_and_backup_all_same'],
 'R6_current_read_only_query_valid':a['current_R6_query']['valid'] is True,
 'previous_R6_264_frozen_files_preserved':len(oldcheck)==264 and all(oldcheck.values()),
 'audit_read_only_source_unchanged':a['source_unchanged_during_audit'],
 'new_guide_links_exist':all(r['exists'] for r in a['links']),
 'historical_R7_file13_and_report26plus13_separated':a['legacy_test_source_facts']['R7_file']['total']==13 and a['legacy_test_source_facts']['R4_R5_file']['total']==26 and '자체는13조건' in alltext and '26+추가13' in alltext,
 'analysis_accuracy_and_video_quality_separated':'잘못 만든 원본 영상을 정확히 분석한 기록' in alltext,
 'four_options_and_recommendation_recorded':all('| '+k in choice for k in ['A (추천)','B','C','D']),
 'actual_A_choice_with_locator_preserved':p['selected']=='A' and p['kind']=='workflow_policy' and bool(p['question_item_id']) and p['state']=='user_directed',
 'A_choice_does_not_grant_content_company_permission':all(p[k] is False for k in ['individual_content_review_performed','company_rule_approval','permission_granted','actual_video_test']),
 'four_item_outcomes_no_total_score':'통과/수정필요/판단보류/비적용' in p['rule'] and '단일총점없음' in p['rule'],
 'required_items_in_current_scope_only':'적용 필수항목' in alltext and '관련없는 미정/미사용 지식' in alltext,
 'D_axis_difference_and_nonselection_disclosed':'축이 달랐다' in choice and '실제로는 A가 선택' in choice,
 'unknown_not_silently_nonapplicable':'아직 모른다는 이유로 비적용을 선택하지 않는다' in alltext,
 'duplicate_errors_not_double_scored':'임의 감점 합산하지 않는다' in alltext,
 'human_content_review_remains_material_specific_pending':'구체 자료/사람 질문' in alltext and '어떤 대상·근거·조건으로 누구에게 무엇을 물을지' in alltext,
 'R3_principles_conditional_no_blanket_card_bans':'개수만큼 의무 검사하지 않는다' in alltext and '무조건 불합격시키지 않음' in alltext,
 'video_brand_caption_parameters_not_invented':'미정 자막/보호공간/영상글자 수치를 임의로 채우지 않는다' in alltext,
 'R7_2_3_4_future_not_implemented':'R7-2' in alltext and 'R7-3' in alltext and 'R7-4' in alltext,
 '01A_media_API_skill_reconstruction_excluded':'영상 추출/OCR/모션분석/모델API/새화면 제작·렌더·스킬 재구성은 하지 않는다' in alltext,
 'phase00_R7_not_marked_complete':'R7 전체/Phase00 미완료' in alltext,
}
assert all(checks.values()),[k for k,v in checks.items() if not v]
planned_cases=[{'case':'잘못된 단위의 원본 차트를 정확히 기록','desired':'분석기록 정확도와 원본 영상 품질을 각각 판단. 원본 오기 자동수정 금지.'},{'case':'보기 좋은 화면을 근거 없이 제작의도/이징수치로 단정','desired':'미관과 별개로 분석 근거/의도는 보류 또는 수정 필요.'},{'case':'로고를 사용하지 않는 작업에 최소크기 가이드가 없음','desired':'해당항목 비적용 이유를 기록, 관련없는 미정이 전체차단으로 확장되지 않음.'},{'case':'자막판정에 필요한 음성/원문 자체가 아직 없음','desired':'자료부족 판단보류. 자막이 불필요하다는 비적용으로 변환하지 않음.'},{'case':'의도적으로 무음이며 화면문구가 전부 전달하는 설명','desired':'청취조건/목적 근거를 확인한 뒤 관련 음성항목의 적용여부 판단. 무조건 자막추가/삭제 금지.'},{'case':'소수점/부정어 누락이 있으나 화면/모션이 아름다움','desired':'적용필수 정보오류는 다른장점으로 상쇄하지 않음. 원문/비교대상 확보 필요.'},{'case':'원칙 여러개가 같은 라벨-도형 대응 오류를 지적','desired':'같은 원인/대상을 연결하되 서로다른 오류 발생범위는 보존, 중복감점 금지.'},{'case':'구조합성 시험13/13 및 과거26+13보고를 재사용','desired':'해당조건의 역사자료만, 실영상 성능·회사합격·새 R7quality완료로 승격하지 않음.'}]
fixes=[{'id':'R7-1-F1','finding':'R7_최종반례검사.json 자체의13조건을 역사 합계39로 혼동','resolution':'해당 파일13/13과 R4_R5의26 + 추가13 역사보고를 문서·착수감사에서 분리','status':'fixed'},{'id':'R7-1-F2','finding':'D는 적용범위/진행순서, A~C는 종합방식으로 비교축 혼합','resolution':'원질문/응답은 보존하고 미선택 D의 추가운영결정 필요성을 이력에 공개. 실제A선택으로 현재 운영안은 명확함','status':'fixed_for_selected_A_scope'},{'id':'R7-1-F3','finding':'필요한 사람검수/핵심오류를 전역보류로 읽을 위험','resolution':'현재목적/범위의 적용 필수항목에 한정, 미사용·관련없는 미정의 전체차단 금지 명시','status':'fixed'}]
expected={**old['after_hashes'],**a['after_hashes']};after={r:sha(BASE/r) for r in expected};assert expected==after
boundary={'completed':['기존 선택89파일/89backup 현황 및 자료동선 감사','분석 정확도/원본·기획 품질/구조·내용/역사·현재 경계 검토','사용자 A 운영방식 실제 선택 기록 확인과 4안 비교 이력 보완','R7-2 품질항목·예반례/R7-3 평가/R7-4 인계로 나누는 단계설계'], 'not_completed':['R7-2 품질항목 정본·검수표와 적용예/반례 체계 구현','R7-3 정답/표본·잠금/지표·분모·기권/누락/불일치·재시험의 평가계획 확정','R7-4 R8·01-A 연계 구현과 최종 인계 검수','실제 영상/시나리오·사람 내용검수·시청 가독성/효과 평가','회사 규정/자막 px·cps·점수 가중치 확정, 스킬 재구성·01-A 구현, R7 전체·Phase00 종료'], 'next_stage_requirements':['항목마다 대상유형/목적·적용조건/필요입력·근거/필수여부와 심각도 영향/관찰과추정/사람질문/비적용 이유를 분리','R4/R5/R6 원계약과 수치·미상·범위/버전·선언의 한계를 유지','기준을 실행한 결과가 없는 현재는 설명용 반례를 시험통과/실영상효과라고 기록하지 않음','R7-3에서는 실영상이 없으면 표본계획과 실제잠금표본 확보를 구분하고 개발/holdout 유출·기권/오류분모·사람불일치를 정의']}
verdict={'stage':'R7-1 현황감사와 운영방식 확인','limited_completion_supported':True,'unresolved_blocking_findings':[],'new_user_question_required':False,'user_policy_choice':'A','actual_human_content_review_performed':False,'actual_video_analyzed':False,'actual_video_available_for_this_review':False,'company_approved':False,'permission_granted':False,'R7_complete':False,'Phase00_complete':False,'phase01a_started':False,'verification_scope':'정적 문서/원문·현재/backup hash와 기존 읽기전용 R6 조회 확인. 아래 조건수는 문서 감사조건이며 품질평가 성능·합성 영상 시험수가 아님.','verification':{'static_review_conditions':len(checks),'static_review_passed':sum(checks.values()),'checks':checks,'selected_current_and_backup_bytes':89,'previous_frozen_files_preserved':264,'read_only_source_unchanged':True,'historical_tests_not_rerun':True},'findings_fixed':fixes,'boundary':boundary,'planned_design_counterexamples_not_executed':planned_cases,'read_depth':a['read_depth'],'evidence':[{'path':str(OUT/'R7_01_독립감사.py'),'sha256':sha(OUT/'R7_01_독립감사.py')},{'path':str(OUT/'R7_01_최종_원문대조.json'),'sha256':sha(OUT/'R7_01_최종_원문대조.json')},{'path':str(OUT/'R7_01_초기_원문대조.json'),'sha256':sha(OUT/'R7_01_초기_원문대조.json')}],'after_hashes':after}
(OUT/'R7_01_최종판정.json').write_text(json.dumps(verdict,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# R7-1 독립 검토 판정

**현황감사·단계설계·사용자 A 운영방식 확인 범위로 완료를 지지합니다. 미해결 차단사항은 없고 추가 사용자 질문은 필요하지 않습니다.**

지정89파일과89backup이 모두 byte 일치했고 기존 R6-4 확인대상264파일도 유지됐습니다. 현재 R6 읽기 전용 조회는 정상이며 감사중 원문이 바뀌지 않았습니다. 정적 감사조건21/21은 문서/정합성 확인 수이며 영상 품질이나 분석 정확도의 평가 성적이 아닙니다.

보완한 세 항목은 과거 시험 수(이 파일13/13, 당시 보고26+13)의 구분, 미선택 D와 A~C의 비교축 차이 공개, 필수항목의 핵심오류/사람보류를 현재 목적·범위에만 반영하는 규칙입니다. 원래 질문과 실제 A답변/locator는 보존했고 정책 선택을 내용·회사·권한 승인으로 확대하지 않았습니다.

사용자 A에 따라 항목별 통과/수정필요/판단보류/비적용 및 준비상태 제안을 사용하고 단일 총점은 두지 않습니다. 필요한 사람 판단/근거는 남기되 관련없는 미정이 전체작업을 막지 않게 합니다.

R7-2의 품질항목 정본·조건별 설명용 예/반례, R7-3의 정답·표본·지표·기권/누락·평가계획, R7-4의 인계는 후속입니다. 원본의 오류를 정확히 기록한 경우와 영상 자체의 품질을 구별하고, 자료부족을 비적용으로 바꾸지 않는 등 8개 설계 반례를 JSON에 제안했습니다. 이 반례를 실행·통과한 것은 아닙니다.

실제 영상/시나리오·사람 내용검수·가독성/모션 효과 검증, 회사 기준/자막 수치·점수 가중치 확정, 스킬 재구성·01-A 구현 및 R7/Phase00 전체 완료는 이 판정에 포함하지 않습니다. 89파일 전체를 새로 의미 정독한 것으로 주장하지 않으며 실제 전문을 읽은 파일과 hash-only 확인을 근거 JSON에 분리했습니다.
'''
(OUT/'R7_01_최종판정.md').write_text(md,encoding='utf-8')
print(json.dumps({'limited_completion_supported':True,'conditions':len(checks),'after_hash_count':len(after),'hashes':{r:sha(OUT/r) for r in ['R7_01_최종판정.json','R7_01_최종판정.md','R7_01_최종_원문대조.json','R7_01_독립감사.py']}},ensure_ascii=True))
