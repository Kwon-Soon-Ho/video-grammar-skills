import json,hashlib
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=read(O/'R7_03_1_최종_원문대조.json');assert a['all_static_checks_passed'] and all(sha(B/r)==h for r,h in a['after_hashes'].items())
primary=read(O/'R7_03_1_공개원문_독립대조.json');f='13_품질검수/평가계획/';sample=(B/f/'02_표본과_유출방지.md').read_text(encoding='utf-8');initial=(O/'R7_03_1_초기후보'/f/'02_표본과_유출방지.md').read_text(encoding='utf-8');meta='08_검증결과/R7_03_1_초기작성_스냅샷.json'
checks=a['after_hashes'];checks[meta]=sha(B/meta)
evidence_names=['R7_03_1_독립감사.py','R7_03_1_최종_원문대조.json','R7_03_1_공개원문_독립대조.json','R7_03_1_메타갱신전_원문대조.json','R7_03_1_초기보존.py']
fixes=[{'id':'R7-3-1-F1','finding':'도전/회귀 역할을 잠금 노출 분리의 예외처럼 읽을 위험','before':'원본 묶음으로 예비/개발과 잠금을 분리하나 과제역할/노출단계의별도축과A파생도전사례의영향은명시되지않음','after':sample.split('## 레드팀 보완',1)[1],'status':'fixed'},{'id':'R7-3-1-F2','finding':'독립/미노출을 기반모델사전학습까지인증한것으로확대할위험','before':'개발/대화노출통제는설명하나주장가능범위의사전학습한계가명시되지않음','after':'통제·기록 가능한 프로젝트 개발·대화·검색범위에한정, 기반모델사전학습/공개벤치마크중복 전수확인아님을명시','status':'fixed'},{'id':'R7-3-1-F3','finding':'A선택과문서보완후작성확인의outputSHA/미선택state가이전초안값','before_evidence':str(O/'R7_03_1_메타갱신전_원문대조.json'),'after':'최초상태는별도초기작성스냅샷에보존,현재5개outputSHA와A선택상태갱신','status':'fixed'}]
verdict={'stage':'R7-3-1 정답·표본·운영방식 계획 검토','limited_completion_supported':True,'unresolved_blocking_findings':[],'scope':{'included':['네평가축/정답상태·허용대안·Unknown/주장별근거·정규화·허용오차의설계','원본묶음/도전역할·노출/개발/잠금·대화검색유출/실제통제계획경계','실제사용자A선택원문/locator와수치·회사·실행권한비승격','110원문/110backup·R6현재조회·초안/현재메타의시점분리'],'excluded':['정답셋·실제표본·접근통제/잠금·모델/도구시행·채점실행','R7-3-2지표/분모·보류/미채점·R7-3-3사람불일치·중재/재시험의완료','실영상/사람기준답안확정·시청효과/업무성과·회사/외부사용권한','R7-4/R8·스킬재구성·01-A구현·전체R7/Phase00완료']},'user_policy_choice':'A','policy_confirmed':True,'thresholds_approved':False,'new_user_question_required_now':False,'verification':{'static_conditions':a['total'],'static_passed':a['passed'],'condition_count_is_not_model_trials_or_quality_performance':True,'originals_and_backups_preserved':110,'R6_current_query_valid':a['current_R6_query']['valid'],'source_unchanged':a['checks']['source_unchanged_during_readonly_audit']},'findings_fixed':fixes,'independent_external_reading':primary,'depth_note':'4개MD·사용자정책/보존·작성확인JSON을정적검토.110파일은byte/hash보존을확인했으며모든원문을새로의미정독한것아님. 공개3자료는지정부분직접대조이며전체열람/저자의열람행위인증아님.','remaining_materials':{'actual_media':0,'actual_gold':0,'actual_locked_groups':0,'actual_trials':0,'next_human_gate':'예비자료확보/독립사람초기답안뒤 표본수·반복수·허용오차·필수합격조건수치별도검토. 아직자료요청/실행권한으로사용하지않음.'},'actual_human_gold_review_performed':False,'actual_evaluation_run':False,'actual_video_analyzed':False,'company_approved':False,'permission_granted':False,'phase01a_started':False,'R7_3_complete':False,'Phase00_complete':False,'evidence':[{'path':str(O/r),'sha256':sha(O/r)} for r in evidence_names],'after_hashes':checks,'after_hashes_note':'R7-3-1 최종검토시점스냅샷.후속03-2/3와최종안내/현황갱신은별도시점검토이며자동현재보증아님.'}
(O/'R7_03_1_최종판정.json').write_text(json.dumps(verdict,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# R7-3-1 독립 검토 판정

**정답·표본·A 운영방식의 계획 범위로 완료를 지지합니다. 미해결 차단사항은 없습니다.**

정적35/35,110원문·110backup동일,R6현재조회정상,최종읽기감사중원문불변입니다. 이수치는문서감사조건이며모델시행/성능성적이아닙니다. 원본25의전사와기술원문0.25의사실충돌,복수허용답·Unknown,정답상태/모델출력판정,관측불확실성/평가허용오차를구분합니다.

도전/회귀의과제역할과개발/잠금노출단계를별도축으로보완했습니다. 잠금A파생A′를미리튜닝하면A도미노출로볼수없습니다. 독립성주장은프로젝트에서통제·기록한범위이며기반모델사전학습까지인증하지않습니다. 수정전작성확인은초기스냅샷에보존하고현재문서/실제A선택과SHA를맞췄습니다.

[Anthropic 평가해설](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)의task/trial·유효대안/Unknown·시행격리와 [scikit-learn 누출](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage), [그룹평가](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data)의해당부분만직접대조했습니다. 원문수치나라이브러리실행/프로젝트실증으로확대하지않았습니다.

사용자A는미래의예비보정→다른원본묶음잠금확인순서를선택한것입니다. 실제영상/정답/잠금/시행은각0이며합격수치·표본수·01-A실행·회사승인은승인되지않았습니다. 지표/분모/보류와사람불일치/재시험은다음소단계이며전체R7-3·Phase00완료는포함하지않습니다.
'''
(O/'R7_03_1_최종판정.md').write_text(md,encoding='utf-8')
print(json.dumps({'after_hash_count':len(checks),'hashes':{r:sha(O/r) for r in ['R7_03_1_최종판정.json','R7_03_1_최종판정.md','R7_03_1_최종_원문대조.json','R7_03_1_독립감사.py']}},ensure_ascii=True))
