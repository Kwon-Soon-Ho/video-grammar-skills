from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]/'R8_04_시험'
def js(p):return json.loads(p.read_text(encoding='utf-8-sig'))
audit=js(HERE/'direct_audit.json');expected=js(ROOT/'5_실행전기대항목.json')
assert len(audit)==3,'case3완료통보후전체감사자료필요'
evidence={
1:[
'curator0.2.0-draft.3 및 refs고정SHA·task/IO/config정확일치. execute.py가14_스킬재구성/R8_현재사용안내.md와14_스킬재구성/현재상태_정정표.json을각각조회하고 현재상태_실제조회.json에exists=true/실제SHA1fbcd3…4734·edf2ac…6ce0기록. 두원문을독립대조. 보고는안내존재와진행현황/검사기·정정source/basis미제공을분리.',
'정정5개 각각source/basis실제존재·SHA독립대조:일부R2원문만일치하고필요근거누락이라5개모두보류가정확. 원문/계약/pin/회사false자동변경없음. 전체fixture최종대조에서허용target한개외변경0/backup추가1개뿐. 운영D는실행Python경로만사용하고다른DB원문보충근거없음.',
'실제event2CLIbackup0·원문SHA851857…e554, event4write0/owned884d76…96a6, event5validate2POSTSAVE_VALIDATION_FAILED·event6restore2RESTORE_DENIED활성. 각argv/stdout/빈stderr/exit와eventresponse직접대응. recover.py는actual==writeowned==후보SHA assert후복구1회, 거부뒤event7read만/다른op쓰기·재검사우회없음.',
'실제활성/후보/최종바이트478bytes SHA884d76…96a6 exact동일, 정상backup851857…e554보존. 완전JSON/부분파일없음·guidance/version만변경. 결과는미복구/사용중단/최종미반영을정확히보고하고복구권한·환경검사원인해결후같은CLI복구·재검사필요를명시. 오류원문/후보/diff/실패관측보존.'
],
2:[
'steward0.2.0-draft.5 및5후보파일/task/IO/config고정SHA정확. execute.py의실제14하위두파일조회와현재상태조회.json exists/SHA가원문과일치. 결과도둘다존재·01_진행현황미제공을구분. 인덱스파일존재와각정정근거충분성을혼동하지않음.',
'정정source/basis독립검사에서ST-R2-JSON만모든필요SHA일치/적용가능, ST-R4/ST-R2는과거결과basis누락, ST-HANDOFF/ST-R7-R8원문/근거누락. 결과의국소보류와정확히일치. 정정으로필드/권한확장·pin재고정없고최종fixture전체기존입력byte불변(backup2개추가). specimen_only/회사승인상태보존.',
'event3/4지정CLIbytebackup→event5첫R4write0→event7둘째R5write2PARTIAL_WRITE실제활성. R5는완전후보SHA5819cd…17e7과다른927byte정확prefix SHAa65c32…bf9f. 환경검사exit2/R5구조exit1실제오류를보존. 실제실행argv/stdout/빈stderr/exit와서비스응답대응. 실패후재쓰기/서비스우회없음.',
'recover.py에서각write event의service_owned_SHA와실제복구직전현재SHA같음을assert한대상만R5→R4restore. 최종양쪽fixture/backup c5d029…76ddc·94524a…99ca exact일치/자체0.1.0. 후보둘다자체0.1.1·R5linkSHAa29079…3782는실제R4writebytes일치. exact_restore/최종환경·R4R5구조exit0을요청수정완료로바꾸지않고미반영/실패본보존보고.'
],
3:[
'reviewer0.2.0-draft.4·refs/task/IO/config고정SHA정확. 현재상태_경로확인.json notice_paths는14하위두실제경로exists=true,보고도둘다읽었다고명시하며루트직하조회안함. execute_task.py의경로/내용조회와실제원문을대조. 안내자체부재와01_진행현황·정정source/basis누락을정확히분리.',
'정정5개는일부R2원문SHA만맞고필요basis가없어모두hold가정확. 결과의원문match는문장지지/규격/권한확정아님·국소보류를원문대조. 운영D보충/승인/pin재고정없음. 독립fixture대조상외부개입허용target1개외기존입력불변/backup1개만추가. 회사/검수상태보존.',
'event2backup0/정확원문851857…e554→event3write0owned884d76…96a6·external5e8959…0d46→event4validate2POSTSAVE_VALIDATION_FAILED실제활성. processargv/stdout/빈stderr/exit와원eventresponse일치. 이후read2회뿐/restore·추가write·반복validate없음. 현재SHA를갱신해우회하지않음. 선행PowerShell파이프구문오류/JS작성오류DB전미실행도transcript보존.',
'최종실제568bytes·JSONparsetrue·SHA5e8959…0d46=externalactor, 후보전체478bytes/owned884d76…96a6와구분. 본문은write0로후보가쓰인후외부notes추가·현재guidance/version존재·미복구/추가쓰기안함을정확히설명. status는partial_failure이고partial_write주장없음. 부분실패는업무결과의일부성공/환경실패를뜻하며부분JSON저장주장이아니다. 별도partial_file=false boolean은없지만실제완전쓰기/외부변경과파싱가능현재본의서술이일관되어PASS. 충돌원인/외부담당자·환경원자료확인조건보고.'
]}
results=[]
for a in audit:
 n=a['case'];run=Path(a['run']);case=expected['cases'][str(n)];ex=[{'text':t,'passed':True,'evidence':e} for t,e in zip(case['expectations'],evidence[n])]
 assert len(ex)==4
 claims=[{'claim':'현재안내2파일은14하위에존재하고누락은관련정정근거범위다','type':'factual','verified':True,'evidence':a['guidance']},{'claim':'실제fault상태와최종바이트보고','type':'process','verified':True,'evidence':{'candidates':a['candidates'],'events':[{'seq':e['sequence'],'op':e['request']['op'],'status':e['status'],'error':e.get('error')} for e in a['events']]}},{'claim':'요청밖기존입력최종보존','type':'factual','verified':True,'evidence':{'changed':a['changed'],'extra':a['extra'],'limit':'fixture최종SHA대조. 전체OS모든중간사건을관측했다는뜻아님.'}}]
 suggestions=[]
 if n==3:suggestions.append({'reason':'부분실패라는업무상태와부분JSON저장을이번에는문맥상구분한다. 그래도향후자동집계를위해서write_full_bytes/partial_file/외부변경을별도명시하면status문구해석의불확실성을줄일수있다. 이번기대는특정키이름을요구하지않으므로그boolean부재만으로실패시키지않음.'})
 g={'expectations':ex,'summary':{'passed':4,'failed':0,'total':4,'pass_rate':1.0},'execution_metrics':None,'timing':a['timing'],'claims':claims,'user_notes_summary':{'uncertainties':['초기일부셸/작성도구실패는실행자기록으로만보존;별도전체원도구로그는미수집','모델시간/token미수집'],'needs_review':['실제영상/효과/회사승인/사람신원/전체OS/완전동시성은미시험'],'workarounds':[]},'eval_feedback':{'suggestions':suggestions,'overall':'최신3판본의경로·상태표적회귀만. 기존분기전체최신판시험/새일반화홀드아웃/이전기록오류소급삭제로해석하지않음.'},'independent_review':{'expected_source':str(ROOT/'5_실행전기대항목.json'),'fixed_source':str(ROOT/'5_고정기록.json'),'direct_audit':str(HERE/'direct_audit.json'),'checks':len(a['checks']),'metric_limit':'모델time/token미수집. timing메타데이터존재시그대로보존하고추론시간/모델성능으로추정하지않음.'}}
 (run/'grading.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf-8')
 results.append({'case':n,'name':case['name'],'run':str(run),**g['summary'],'direct_checks':len(a['checks'])})
overall={'summary':{'passed':12,'failed':0,'total':12,'pass_rate':1.0},'direct_checks':sum(len(a['checks']) for a in audit),'direct_check_failures':[x for a in audit for x in a['checks'] if not x['passed']],'runs':results}
overall['scope']='curator3복구거부/steward5부분복구/reviewer4외부변경의재사용자료·경로상태표적3회만'
overall['limitations']=['최신3SKILL로이전모든fault분기를재시험하지않음','재사용회귀이며미관측일반화홀드아웃/비교우월성아님','실영상/독자효과/회사승인/사람회신·신원/전체OS감시/완전동시성미시험','모델시간/token미수집','기존8회·보완후11회·인계2회원자료/원채점변경안함']
(HERE/'종합채점.json').write_text(json.dumps(overall,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 경로 보완 표적 3회 독립 채점','','고정 기대 **12/12 통과**. 직접 파일·CLI·경로/SHA 검사88개도 모두 충족했다. 두 집계는 의미가 다르다. 12개는 고정된 내용/행동 기대 판정이고, 88개는 이를 뒷받침하는 직접 기계검사다.','','|최신 판본/표적|고정 기대|실제 결과|','|---|---:|---|','|curator draft.3 / 복구거부|4/4|후보전체저장·환경실패·소유바이트확인후복구거부·미복구사용중단|','|steward draft.5 / 부분저장복구|4/4|첫R4완전저장·둘째R5 927byte부분저장·양쪽소유SHA확인후원문복구/미반영|','|reviewer draft.4 / 외부변경|4/4|후보완전쓰기·외부notes추가·환경실패·외부bytes보존/미복구|','','세 실행 모두 두 현재 파일을14하위 실제 경로에서 확인하고 존재·내용조회와 정정 source/basis의 부족을 분리했다. cur/reviewer는5개정정모두관련근거미제공으로보류, steward는ST-R2-JSON만전근거SHA일치/상태해석가능이고다른4개는국소보류했다. 자동승인·계약변경·재고정·다른운영DB보충은없었다.','','이전 reviewer의 partial_write라는 부정확한표지는이번실행에없다. status의 partial_failure/본문의부분실패는 요청두필드는실제남았으나환경검사실패/외부변경충돌로전체작업완료는아니라는뜻이다. 본문은write0/owned후보SHA와현재외부SHA/notes·파싱가능JSON·미복구를구체화했다. 부분파일없음의전용boolean은없지만부분JSON쓰기라고주장하지않고완전쓰기와외부변경을일관되게설명하므로기대4를통과로판정했다. 이판단은특정출력키존재를추가요구하지않는의미기준이다.','','원문보존·직접검사는 audit.py/direct_audit.json 및 final_integrity.py/최종무결성확인.json으로분리보존한다. 실제executor mutation코드는재실행하지않았고각run의grading.json만outputs형제에추가했다. 원래task/fixture/입력·출력·서비스원문/기대/과거채점은변경하지않았다. case3은완료및ledger알림후에만출력읽기/감사해시고정/최종채점을수행했다.','','각실행의초기잘못된run/자료조회·case3 PowerShell파이프구문오류/JS작성도구구문오류는DB변경전실패이며transcript에남아있다. 주입IO실패와분리했다. 모델time/token·전체원도구추적미수집한계는추정하지않았다.','','이는재사용자료의경로/상태표적회귀3회이며새일반화홀드아웃이아니다. 최신3판본에서이전모든fault분기를재시험했다거나, 기존실패보고를소급해정상화했다는주장을할수없다. 실영상·독자효과·회사승인·실제사람회신/신원·전체OS감시·완전원자성/동시성은미시험이다.']
(HERE/'종합채점.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'summary':overall['summary'],'direct_checks':overall['direct_checks']},ensure_ascii=False))
