import json,hashlib
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
a=read(O/'R7_03_3_최종_원문대조.json');assert a['all_static_checks_passed'] and all(sha(B/r)==h for r,h in a['after_hashes'].items())
v={'stage':'R7-3-3 사람불일치·중재·재시험 계획','limited_completion_supported':True,'unresolved_blocking_findings':[],'findings_fixed':[],'scope':{'included':['사람독립초기답/역할·결측/분모·중재·허용대안/미해결·재채점의운영계획','alpha후보의단위/척도·비교가능쌍·차이함수·0분모/미산출·한계','버전/원본/정답변경·실행조건·모든재시도·잠금노출후새원본·비교/업무효과계획'],'excluded':['실제검수자배정/동의·초기답/중재·신뢰도/alpha산출','실제실행/평가·실영상/이해도·시간/비용효과','통합5파일연결검토·최종메타갱신,R7-4/R8/01-A·전체Phase00완료']},'verification':{'static_conditions':a['total'],'static_passed':a['passed'],'not_performance_or_trial_counts':True,'protected_current_and_backup_files':110,'R6_current_query_valid':a['current_R6_query']['valid'],'source_unchanged':a['checks']['source_unchanged']},'independent_primary_reading':[{'url':'https://www.asc.upenn.edu/sites/default/files/2021-03/Computing%20Krippendorff%27s%20Alpha-Reliability.pdf','read_depth':'저자문서intro/하나의변수·여러검수자/척도·결측, C의비교가능쌍과D의차이함수에관한프로즈부분.표/수치예전체/참고논문전문미검토','comparison':'짝지을수없는단독값을일치로세지않고변수별척도/차이함수·분모조건을확인해야한다는설계와부합. 실제alpha를계산하지않았고고정합격선으로승격하지않음.','raw_fulltext_archived':False,'remote_content_hash':None},{'url':'https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents','read_depth':'동일R7-3검토의앞소단계에서직접읽은task/trial·ability/regression·isolatedharness·반복결과차이부분재사용.새전체조사아님','comparison':'반복출력과독립영상수구분·초기/재시도보존·스킬단독효과조건을지원하나논문성능을이전하지않음.'}],'remaining_human_gate':'두사람은권고계획이고아직미배정. 단독이면단독초안으로표시하고실제역할/응답·불일치·중재를접수하기전계수/회사승인/권한을만들지않음. 수치/반복/통계계획은예비자료뒤검토.','actual_human_annotations':0,'actual_adjudications':0,'actual_trials':0,'actual_alpha':None,'company_approved':False,'permission_granted':False,'R7_3_complete':False,'Phase00_complete':False,'evidence':[{'path':str(O/x),'sha256':sha(O/x)} for x in ['R7_03_3_독립감사.py','R7_03_3_최종_원문대조.json']],'after_hashes':a['after_hashes'],'snapshot_boundary':'현재110개원문/backup동일인검토시점의이력.추후13/00등허용된상태안내변경은그전backup·old/newSHA와나머지불변을별도확인해야하며이판정을현재불변보장으로확대하지않음.'}
(O/'R7_03_3_최종판정.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# R7-3-3 독립 검토 판정

**사람불일치·중재·재시험의운영계획범위로완료를지지합니다. 차단사항은없습니다.**

정적37/37,110원문/backup일치,R6조회정상·검토중원문불변을확인했습니다. 실제사람초기답/중재/평가시행은각0이며문서감사조건을실제시험성적으로세지않습니다.

두검수자는미배정권고이고단독초안/AI응답을사람간신뢰도로세지않습니다. 초기답과중재후답을분리하고결측·판정범주·매칭단위를구분하며,합의100%나높은계수를내용진실성으로확대하지않습니다. [Krippendorff저자문서](https://www.asc.upenn.edu/sites/default/files/2021-03/Computing%20Krippendorff%27s%20Alpha-Reliability.pdf)의intro·비교가능쌍/척도설명부분을직접대조했습니다. 실제alpha·고정합격선·원논문전체검토는없습니다.

모든재시도·실패이력,정답변경시양쪽재채점,새문맥·작업상태격리,잠금집계피드백으로튜닝한경우새원본묶음필요를명시했습니다. 반복/시청학습효과·전체재작업/대기시간없이업무효과를선언하지않습니다.

통합연결5파일과최종메타변경은별도검토합니다. R7-4/R8/01-A와전체Phase00완료는이판정밖입니다. 이번110불변확인은현재시점이력이며추후허용된상태안내변경의현재보증이아닙니다.
'''
(O/'R7_03_3_최종판정.md').write_text(md,encoding='utf-8');print(json.dumps({'after_hash_count':len(a['after_hashes']),'outputs':{x:sha(O/x) for x in ['R7_03_3_최종판정.json','R7_03_3_최종판정.md','R7_03_3_최종_원문대조.json','R7_03_3_독립감사.py']}},ensure_ascii=True))
