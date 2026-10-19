import json,hashlib,re
from pathlib import Path
BASE=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');OUT=Path(__file__).parent
rels=['13_품질검수/03_판정운영기준.md','05_출처와검토/R7_조사착수메모.md'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={r:sha(BASE/r) for r in rels};texts={r:(BASE/r).read_text(encoding='utf-8') for r in rels};op=texts[rels[0]];memo=texts[rels[1]]
old=OUT/'R7_01_최종판정.json';oldsha=sha(old);prev=json.loads(old.read_text(encoding='utf-8'))
checks={
 'only_two_new_documents_reviewed':len(texts)==2,
 'scope_quality_items_and_evaluation_remain_future':'개별 품질 항목·원문 근거·적용 예와 반례는 R7-2' in op and '평가 표본·지표·합격 조건의 검증 계획은 R7-3' in op,
 'four_target_types_separate_accuracy_quality_structure':all('| '+s+' |' in op for s in ['분석 기록','기획·시안','실제 영상','규격·검수 기록']),
 'unreviewed_progress_not_false_outcome':'진행 상태를 ‘미검수’로 표시한다' in op and '네 가지의 완료 판정으로 만들지 않고' in op,
 'missing_required_scope_cannot_bypass_readiness':'필수인 항목을 요청 범위에서 빼도 전체 준비 완료로 제안할 수 없다' in op,
 'required_scope_unknown_requires_clarification':'필수 범위를 정할 근거가 부족하면 범위 자체의 확인이 필요' in op,
 'version_and_partial_range_recorded':'대상 ID·버전/해시' in op and '일부 결과로 표시' in op,
 'missing_evidence_is_hold_not_NA':'확인하지 못했다는 이유로 선택하지 않음' in op,
 'no_evidence_no_confirmed_error':'의심만으로 확정하지 않음' in op,
 'human_reply_absent_not_completed':'실제 답변이 있기 전에는 검수 완료로 적지 않는다' in op,
 'required_unreviewed_or_human_pending_not_ready':'필수항목이 미검수이거나' in op and '아직 준비 완료로 제안하지 않는다' in op,
 'multiple_findings_not_hidden_by_one_summary':'수정필요와 판단보류가 함께 있으면 둘 다 표시' in op,
 'scoped_next_review_proposal_not_approval':'다음 검토로 진행 가능' in op and '납품·배포·권한 승인' in op,
 'irrelevant_unknown_not_global_block':'관련없는 회사의 미정 가이드까지 전체 작업의 차단 조건' in op,
 'severity_separate_from_confidence':'판단의 확실성과 오류의 영향은 별개' in op,
 'human_roles_not_actual_identity_or_existing_CI_scope_upgrade':'역할만 정했다고 실제 사람이 검수한 것으로 기록하지 않는다' in op and '자료 최신성 확인을 다른 내용·시안·배포 승인에 재사용하지 않는다' in op,
 'operational_choices_fourplus_and_recommendation':'최소 4개 선택지·추천안' in op,
 'content_review_free_answer_not_leading_fourchoice':'정답을 유도하는 네 가지 답에 억지로 맞추지 않고' in op and '자유 답변과 근거' in op,
 'hypothetical_cases_not_actual_validation':'판정 차이를 설명하기 위한 가정' in op and '실제 영상을 검수한 결과가 아니다' in op,
 'no_DB_or_fixed_R6_input_edit':'R4 DB 필드나 R6 고정 입력을 이번 단계에서 변경하는 것은 아니다' in op,
 'research_is_partial_not_deep_review_complete':'원문을 부분 열람' in memo and '심층 조사 완료나 새 회사 기준 확정이 아니다' in memo,
 'unread_and_failed_sources_not_asserted_read':'단위 표기 세부 조항을 새로 모두 검토했다는 주장' in memo and '열람 시도 실패' in memo and '이번 근거로 사용하지 않음' in memo,
 'web_reference_numbers_not_company_video_rules':'웹 pt/px를 그대로 영상 글자 크기로 적용' in memo and '회사 영상 납품 규정으로 승격하지 않는다' in memo,
 'implementation_and_real_effects_unverified':'실제 판정은 수행하지 않았다' in memo and '라이브러리 설치/실행' in memo,
}
assert all(checks.values()),[k for k,v in checks.items() if not v]
links=[]
for r,text in texts.items():
 for link in re.findall(r'\]\(([^)]+)\)',text):
  if link.startswith(('https://','http://')):links.append({'file':r,'url':link,'independently_opened_in_this_additional_review':False})
  else:links.append({'file':r,'relative_path':link,'exists':(BASE/r).parent.joinpath(link).resolve().is_file()})
assert all(x.get('exists',True) for x in links)
after={r:sha(BASE/r) for r in rels};assert before==after and sha(old)==oldsha
line_evidence={r:[{'line':i,'text':s} for i,s in enumerate(t.splitlines(),1) if any(k in s for k in ['미검수','필수','사람','자유','열람','주장','승격','실패','별개','부분','변경'])] for r,t in texts.items()}
verdict={'stage':'R7-1 정적 운영문서 두 건 추가검토','limited_completion_supported':True,'unresolved_blocking_findings':[],'additional_user_question_required':False,'boundary':{'included':['판정운영/미검수/적용필수 범위/사람질문/준비제안/판정기록 경계의 정적 검토','조사착수 메모가 선언한 부분열람·미검토·실패/규범 한계의 명시성 확인'],'excluded':['웹10자료를 이번 검토에서 독립 열람하거나 저자의 실제 열람행위를 인증하는 일','개별 R7-2 품질기준·R7-3 평가조건 확정/시험 구현','실제 내용/영상·신원·회사/법적권한 검수','코드/DB/스킬/R6 입력변경·01-A·전체R7/Phase00완료']},'verification':{'static_conditions':len(checks),'static_passed':sum(checks.values()),'checks':checks,'scope_note':'문서감사 조건수이며 품질/영상 성능시험수가 아님.','source_unchanged':before==after,'prior_verdict_unchanged':sha(old)==oldsha},'findings':[],'nonblocking_followup_notes':['R7-2/3에서 링크별 필요한 조항·실제 열람 위치/판본·원문 수치의 적용 조건과 반례를 개별 지식/품질항목에 연결할 것. 메모 자체로 열람깊이나 허가를 승격하지 않음.','현재운영문서의 제약은 아직 DB/실행검사에 구현된 것으로 주장하지 않으며 후속 schema/평가에서 all-NA·필수누락·부분검수·판정변경을 재현할 것.'],'prior_verdict':{'path':str(old),'sha256':oldsha,'scope':'그 판정의 after_hashes는 당시 snapshot이며 이후 진행안내/현황 갱신의 현재보증으로 취급하지 않음.'},'read_depth':{r:'full_text_static_review' for r in rels},'line_evidence':line_evidence,'links':links,'actual_human_content_review_performed':False,'actual_video_analyzed':False,'company_approved':False,'permission_granted':False,'before_hashes':before,'after_hashes':after}
(OUT/'R7_01_추가판정.json').write_text(json.dumps(verdict,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# R7-1 운영 문서 추가 독립 검토

**추가 두 문서의 정적 운영설계 범위로 완료를 지지합니다. 차단사항과 추가 사용자 질문은 없습니다.**

정적 감사조건24/24를 확인했습니다. 미검수는 진행 상태이며 네 가지 완료 판정과 구분합니다. 적용 필수항목을 범위에서 빼거나 일부 프레임만 확인해 전체 준비를 제안할 수 없습니다. 필수범위 자체가 불명확하면 그 범위를 확인하도록 했습니다. 오류·보류를 함께 표시하고 근거/버전/사람 확인범위를 유지하며 준비상태는 다음 검토를 위한 제안에 한정합니다.

운영방식 판단에는 최소4선택지·추천안을 사용하고, 실제 내용검수는 유도형 선택지로 제한하지 않고 자유답변·근거를 받도록 구분했습니다. 역할 지정이나 기존 자료최신성 답변은 실제 내용/회사/권한 승인으로 확대하지 않습니다.

조사 메모는 부분 열람, BIPM 세부조항 미검토, BBC 열람실패·근거미사용과 웹 규칙의 영상 전이 한계를 명시했습니다. 이번 추가 검토는 이 명시성을 확인한 것이며 웹 원문10건을 독립 열람하거나 저자의 열람행위를 인증한 것은 아닙니다. R7-2/3에서 필요한 조항·판본·위치와 조건별 예/반례를 연결해야 합니다.

기존 최종판정은 해시 그대로 보존했고 두 D문서도 검토중 불변입니다. 기존 판정의 after_hashes는 당시 snapshot입니다. 품질항목/평가 구현·실제 영상/내용검수·코드/DB/스킬 변경·01-A와 R7/Phase00 전체 완료는 포함하지 않습니다.
'''
(OUT/'R7_01_추가판정.md').write_text(md,encoding='utf-8')
print(json.dumps({'limited_completion_supported':True,'static_conditions':len(checks),'after_hashes':after,'outputs':{r:sha(OUT/r) for r in ['R7_01_추가판정.json','R7_01_추가판정.md']}},ensure_ascii=True))
