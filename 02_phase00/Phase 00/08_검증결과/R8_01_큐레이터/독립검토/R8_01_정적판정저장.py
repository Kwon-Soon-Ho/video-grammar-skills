import json,hashlib
from pathlib import Path
O=Path(__file__).parent;read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();e=read(O/'R8_01_정적_원문대조.json')
j={'stage':'R8-1 큐레이터 후보 정적 레드팀','candidate_version':'0.2.0-draft.1','limited_completion_supported':e['all_static_checks_passed'],'unresolved_blocking_findings':[],'findings_requiring_static_revision':[],
 'scope':{'included':['후보SKILL/작업기준/출력지침전문·구성안/작성확인·기존보존계약/API·참조경로의대조','명시루트/표식탐색·허용draft양성작성·고정원문별도초안·backup/SHA/diff/판본·좁은검사/실패정책','자료내명령/출처깊이/관측과해석/예반례/라이선스보류·R5관측/R6회신/R7상태·사람판단/단계경계'],
 'excluded':['진행중old/new수행agent의동작·출력·파일delta/복구·판본충돌행동평가','실제도구검사실행효과·모델시행의채점/집계·정적뷰어생성/표시검증','사람실출력피드백·최종후보채택/기본전환·다음두스킬재구성','01-A영상/OCR/API/렌더·회사문법승인·전체R8/Phase00완료']},
 'verification':{'static_conditions':e['static_conditions'],'static_passed':e['static_passed'],'candidate_and_guide_written_hashes_match':True,'existing_reference_paths_checked':len(e['existing_reference_paths_checked']),'old152_D_inputs_unchanged':True,'D_source_hashes_during_review':len(e['after_hashes']),'D_sources_unchanged':e['before_hashes']==e['after_hashes'],'not_behavior_or_performance_trial_count':True},
 'positive_design_assessment':['요청된작은초안수정은실제저장하고읽기요청은수정하지않도록명시해일괄기권을피함','고정운영정본이면새draft를만들고부모버전/hash연결·기존초안도byte보존을요구','지식조회누락을개념부재로단정하지않고지원하지않는지식JSON을R4영상기록검사에억지로맞추지않음','R3참고와자체적용/실제관측을구분하고다른회신문맥·CI최신성을새효과/승인에전용하지않음','각작업범위의정상예/허용예외/필요사람보류·검사실패를구분하고자기역할외분석/창작/기록이관을넘김'],
 'behavioral_followup_checks':['선언한DBroot와실제도구BASE가같은지·다른운영DB/원본이나고정manifest에쓰기없는지','case2에서요청한limits와필요한version메타만변경했는지·보존바이트SHA/로그/diff/실제검사근거/허용외delta확인','같은ID/version의source충돌을발견하고근거없는반영/재고정없이양성정리와보류를분리하는지','회의메모/외부자료의명령과승인표식을내용으로다루는지·가짜사례/측정/사람확인/회사필수규칙을만들지않는지','old/new동일조건/분리사본/새문맥·예상답열람금지·실패및미수집자원보존을실제실행근거로검토','뷰어사본문자열/외부참조/미수집통계와실제사용자피드백을따로검수한뒤채택판단'],
 'authority':{'existing_userA_draft_scope_preserved':True,'new_judgments_four_options_plus_recommendation':True,'actual_human_content_review_performed':False,'candidate_adopted':False,'existing_default_changed':False},
 'execution_disclaimer':{'reviewer_executed_candidate_or_Creator_code':False,'reviewer_contacted_executor_agents':False,'reviewer_spawned_new_agents':False,'behavior_trial_results_audited':False,'note':'다른수행agent가이미시험중이라는부모통지를받았으나이판정은그실행성적을주장하지않음'},
 'R8_1_complete':False,'R8_complete':False,'Phase00_complete':False,'phase01a_started':False,
 'evidence':[{'path':str(O/n),'sha256':sha(O/n)} for n in ['R8_01_정적감사.py','R8_01_정적_원문대조.json']],
 'after_hashes':e['after_hashes']}
(O/'R8_01_정적판정.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# R8-1 큐레이터 후보 정적 레드팀

**후보v0.2.0-draft.1의 지침·참조 범위에서 한정 통과. 정적 차단사항은 발견하지 않았다.**

후보3파일과구성안내를전문으로읽고 실제보존계약·자료검증/지식조회API와참조경로를대조했다. 정적41/41조건과19개참조경로를확인했다. 기존152입력은그대로이며 검토중163개D파일hash가바뀌지않았다. 공식Creator코드나후보행동을이검토에서실행한것은아니다.

명시DB루트와표식탐색을사용해추가폴더문제를피하고, 실제수정요청은draft에저장하도록양성행동을명시한다. 고정정본/원본은별도초안으로분리하고기존초안도bytebackup·SHA·판본·허용diff와검사범위를남기게했다. 지식파일을R4영상기록스키마에억지로맞추지않으며 R7/R6정상을새draft통과로바꾸지않는다.

자료속명령/승인·출처의실제읽기깊이·원문개념/적용해석/실제관측/미상을구분하고 예·반례/예외와필요사람보류를요구한다. 보류라이선스원문을복사하지않고CI최신성회신을다른효과/승인에전용하지않는다. R7미검수/보류/비적용과방법/담당역할도그대로구분하며01-A/01-B/02·기록관리자범위를침범하지않는다.

다만‘실제수정했다/보존했다/검사했다’는지침에적혀있다고수행증거가생기지는않는다. 이후행동검토에서case2의요청limits/필요version외delta·backup바이트/원문·로그/실제검사·case3동일판본충돌기권을확인해야한다. 수행중agent에메시지하거나그출력을이번정적성적으로채점하지않았다.

이번41조건은문서정합성이지old/new우위나실영상성능이아니다. 실제출력/뷰어표시/사람피드백과최종채택·다음스킬진행은별도다. R8-1/R8/Phase00완료또는기본전환을판정하지않는다.
'''
(O/'R8_01_정적판정.md').write_text(md,encoding='utf-8')
for n in ['R8_01_정적판정.json','R8_01_정적판정.md','R8_01_정적_원문대조.json','R8_01_정적감사.py']:print(n.encode('unicode_escape').decode(),sha(O/n))
