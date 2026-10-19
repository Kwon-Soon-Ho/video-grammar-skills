from pathlib import Path
import hashlib
import json
import sys

OUT=Path(__file__).resolve().parent
CASE=OUT.parent
DB=CASE/'inputs'/'Phase00'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

audit=load(OUT/'local_audit.json')
selection=load(OUT/'검수항목_사전선정.json')
readonly=load(OUT/'readonly_verification.json')
errata=load(OUT/'errata_hash_checks.json')
cards=load(DB/'작업초안/쉬운말_지식카드.json')
index=load(DB/'작업초안/연결목록.json')

source_specs=[
 ('01_공통용어/공통용어사전.json','0.1.1',['/terms/27','/terms/37','/terms/47','/terms/48']),
 ('01_공통용어/용어판정기준.json','0.1.2',['/guides/27','/guides/37','/guides/47','/guides/48']),
 ('01_공통용어/분류운영규칙.json','0.1.1',['/axis_units','/claim_status_policy','/evidence_rules']),
 ('02_원칙과레이아웃/레이아웃지식.json','0.1.1',['/layouts/3']),
 ('02_원칙과레이아웃/레이아웃_심화지식.json','0.1.2',['/layout_cards/3']),
 ('02_원칙과레이아웃/07_레이아웃별_선택조건과반례.md',None,['머리말 1~5행','선형 프로세스 73~94행']),
 ('13_품질검수/품질항목_정본.json','0.1.1',[x['id'] for x in selection['items']]),
 ('13_품질검수/03_판정운영기준.md','R7-1 2026-10-15',['전체']),
 ('03_한맥디자인/한맥디자인정본.json','0.1.0',['/profile_id','/version','/description','/provenance_limit','/sources']),
 ('14_스킬재구성/R8_현재사용안내.md','2026-10-15',['전체']),
 ('14_스킬재구성/현재상태_정정표.json','0.1.1',['/records 5건']),
]
sources=[{'path':str(DB/p),'relative_path':p,'version':v,'sha256':sha(DB/p),'semantic_scope':s} for p,v,s in source_specs]

card_reviews=[
 {'card_id':'시범카드001','version':'0.1.1','term_id':'LAYOUT-PROCESS-LINE','term_version':'0.1.0','axis':'layout','progress':'문서 대조 완료','verdict':'통과','scope':'제공 원문에 대한 의미·조건·반례·기권 경계의 문서 검토','target_locations':['/records/0/plain_explanation','/records/0/use_when','/records/0/example','/records/0/counterexample','/records/0/caution'],'source_locations':['공통용어사전.json /terms/27','용어판정기준.json /guides/27','레이아웃지식.json /layouts/3','레이아웃_심화지식.json /layout_cards/3','07_레이아웃별_선택조건과반례.md 73~94행'],'evidence':'단계를 선·방향으로 연결한다는 정의와 순서 있는 단계 조건을 보존. 세로 예에서도 단계 순서·연결 방향을 유지하고 가로/세로는 방향 속성으로 분리. 동등 나열·연도축·중요 분기/회귀 은폐를 반례로 두고 선 길이와 실제 소요시간을 분리한다. 선후·분기 근거가 없으면 순서를 확정하지 않는다.','valid_exceptions':'가로·세로 재배열 모두 가능. 순서선이 반드시 기간 길이를 뜻하지 않음. 분기/기간이 핵심이면 다른 구조를 검토하는 원문 조건을 보존.','counterevidence_or_limits':'실제 단계 명칭·선후 사실, 실제 화면의 가독성·밀도·지속시간은 제공되지 않았으므로 검수하지 않음. 원문이 요구하는 모든 시안 조정 지침을 이 간단한 용어 설명에 전부 복제할 필요는 없음.','action':'현재 문장 유지','required_edit':None,'recheck_when':'카드 문장/원문 판본·SHA가 바뀌거나 실제 절차/시안에 적용할 때'},
 {'card_id':'시범카드002','version':'0.1.1','term_id':'FUNCTION-FOCUS','term_version':'0.1.0','axis':'motion_function','progress':'문서 대조 완료','verdict':'통과','scope':'모션 기능 설명과 효과 입증 범위의 문서 검토','target_locations':['/records/1/plain_explanation','/records/1/use_when','/records/1/counterexample','/records/1/caution'],'source_locations':['공통용어사전.json /terms/37','용어판정기준.json /guides/37','분류운영규칙.json /evidence_rules/temporal_change_plus_message_context'],'evidence':'지금 설명하는 대상에 안내하는 움직임의 역할이라고 쓰고, 시간에 따른 강조 변화와 설명 맥락을 함께 요구한다. 장식용 점의 모든 이동을 기능으로 보지 않으며 대상 근거가 부족하면 후보로 남긴다. 실제 시청자의 시선을 옮겼는지는 별도 검토가 필요하다고 명시한다.','valid_exceptions':'기능의 문서 정의/계획된 예를 설명할 수 있으나 실제 렌더 관측·시청효과로 승격하지 않음.','counterevidence_or_limits':'눈길을 안내한다는 목적 표현만 떼어 효과 확정으로 읽으면 오해할 수 있으나 같은 카드의 caution이 실제 효과를 명시 분리해 확인된 의미 오류는 없음. 실제 시선효과·학습효과·제작자 의도는 미확인.','action':'효과 분리 caution을 포함해 현재 문장 유지','required_edit':None,'recheck_when':'해당 caution 삭제·축약, 실제 영상/효과 주장 추가 시'},
 {'card_id':'시범카드003','version':'0.1.1','term_id':'PROPERTY-VISIBILITY','term_version':'0.1.0','axis':'motion_property','progress':'문서 대조 완료','verdict':'통과','scope':'가시성 관측과 구현/원인 추정의 문서 검토','target_locations':['/records/2/plain_explanation','/records/2/use_when','/records/2/counterexample','/records/2/caution'],'source_locations':['공통용어사전.json /terms/47','공통용어사전.json /terms/48','용어판정기준.json /guides/47','용어판정기준.json /guides/48','분류운영규칙.json /claim_status_policy'],'evidence':'보이는 범위·정도의 시간 변화와 같은 대상/시간 범위 조건을 보존. 불투명도·마스크·합성·배경 중 원인을 원본 없이 확정하지 않고, 관측이 충분하면 가시성 기록을 유지하며 원인만 미확정으로 둔다.','valid_exceptions':'구현 원인이 미확정이어도 충분한 화면 관측까지 삭제하지 않음. 정확한 opacity 수치/알고리즘은 별도 정의 필수근거 없으면 확정 불가.','counterevidence_or_limits':'가상 예를 실제 제목/글자의 등장 관측으로 등록하지 않음. 실제 opacity/마스크/합성 원인은 조사하지 않음.','action':'현재 문장 유지','required_edit':None,'recheck_when':'관측/원인 분리 문장 변경 또는 실제 구현 주장 추가 시'},
]

details={
 'Q-INFO-01':('판단보류','문서 검토 완료; 사람 적합성 판단 대기','쉬운말 설명카드라는 목적과 가상 예는 확인했다. 대상 독자의 실제 사전지식·실무 출력 피드백이 없어 설명 난이도/이해 용이성은 아직 확정하지 않는다. 각 카드의 용어 의미 검토는 별도 통과.',['task.txt','쉬운말_지식카드.json /scope,/records[*]/plain_explanation,/human_review'],'독자의 사전지식 근거·이번 판본에 대한 자유 답변 내용 검토. 실제 영상 효과 자료를 지금 요청하지 않음.','H-01'),
 'Q-INFO-02':('통과','문서 대조 완료','3 source_snapshot은 용어 원문과 필드 전체가 같고, 쉬운말 본문은 부정·한계·조건·가상 예 표기를 보존한다. 원문의 짧은 정의를 회사 사실/실영상으로 확대하지 않았다.',['공통용어사전.json /terms/27,/terms/37,/terms/47','쉬운말_지식카드.json /records[*]'],'원문·카드 판본/SHA 또는 검토할 의미가 바뀌면 해당 문장을 다시 대조. 실제 자막/음성 일치성은 미실시.',None),
 'Q-SCREEN-02':('통과','조건부 지식 문서 대조 완료','선형 프로세스의 순서·방향·분기/회귀·시간축 구분과 가로/세로 변형을 보존한다. 원문 반례와 충돌하는 단정은 발견하지 않았다.',['레이아웃_심화지식.json /layout_cards/3','07_레이아웃별_선택조건과반례.md 73~94행','쉬운말_지식카드.json /records/0'],'실제 절차/문구/화면비·시안에 적용할 때 화면 적합성 별도 검토.',None),
 'Q-BRAND-02':('통과','출처·역할 경계 문서 검토 완료','design_reference는 hanmac-video@0.1.0 실제 profile_id/판본/SHA와 일치하고 usage=reference_only_no_new_color_selected다. 새 색·역할·공식 CI나 회사 승인으로 쓰지 않았다.',['연결목록.json /design_reference','한맥디자인정본.json /profile_id,/version,/description,/provenance_limit','07_한맥디자인과_CI_확인현황.md 3~14행'],'새 색/화면 역할을 실제 선택하면 별도 적용 조건을 검토. 이번에 사용하지 않은 CI 세부 미정은 전체 차단 조건이 아님.',None),
 'Q-TRUST-01':('통과','로컬 판본/연결/내용 대조 완료','3카드 ID·term_ref·원문 snapshot/원문 SHA·draft_ref 문서/카드 판본·실제 파일 SHA가 일치했다. 상류 인계 destination별 SHA도 모두 일치한다. source 경로 존재/SHA만으로 의미 통과라 하지 않고 위 카드별 본문 대조를 별도로 수행했다.',['local_audit.json','상류결과/01/결과.md','상류결과/02/결과.md','상류_인계증거.json'],'full R6/R7와 품질 출처 조사 전체는 제공되지 않아 full 검증 통과로 확대하지 않음. 문서 주장이므로 PTS/OCR/좌표는 요구하지 않음.',None),
 'Q-TRUST-02':('통과','추론/승인 범위 문서 검토 완료','주목 이동 기능/효과와 가시성 관측/구현 원인을 분리한다. draft·human_review=pending·company_approved=false를 유지했다. 옛 R8-3 구성/분량 유지 회신과 CI 최신성 회신을 이번 3카드 내용 승인에 재사용하지 않는다.',['쉬운말_지식카드.json /records/1/caution,/records/2/caution,/human_review,/company_approved','연결목록.json /human_review,/company_approved','R8-3_적용성검토자_검토답변.json /scope'],'실제 제작 의도/원인·시선/학습 효과·회사 규칙·회사 승인·후보 기본 전환을 확정하지 않음.',None),
}
criteria=[]
for x in selection['items']:
    verdict,progress,why,evidence,recheck,human=details[x['id']]
    criteria.append({**x,'criteria_version':'0.1.1','criteria_sha256':selection['criteria_sha256'],'progress':progress,'verdict':verdict,'evidence_and_reason':why,'evidence_locations':evidence,'required_edit':None,'recheck_or_resolution':recheck,'human_question_ref':human})

questions=[{'id':'H-01','status':'pending_not_sent','role':'이번 설명카드를 사용할 내용 담당자·필요시 실제 독자','target_file':str(DB/'작업초안/쉬운말_지식카드.json'),'document_version':'0.1.1','sha256':audit['target_document']['sha256'],'target_ids':['시범카드001','시범카드002','시범카드003'],'locations':['/records/0/plain_explanation,/use_when,/counterexample,/caution','/records/1/plain_explanation,/use_when,/counterexample,/caution','/records/2/plain_explanation,/use_when,/counterexample,/caution'],'confirmed':'제공 원문과 축·조건·반례·추론범위는 문서 대조에서 유지됨.','missing':'이번 카드 판본을 읽은 실제 사람의 실무 용이성/사전지식/내용 확인 회신','question':'이 세 설명을 사용할 독자는 관련 용어를 어느 정도 알고 있나요? 각 카드에서 이해하기 어렵거나 실제 업무 의미와 다르게 읽히는 문장·위치를 자유롭게 알려 주시고, 수정이 필요하면 근거 또는 원하는 의미를 함께 적어 주세요.','answer':None,'resolution':'해당 v0.1.1/이 SHA·카드 위치/범위의 실제 답변을 확인한 부분만 기록. 다른 판본/옛 R8 회신으로 완료하지 않음.'}]
options=[{'option':'A','label':'세 카드 전체 내용 검토','recommend':True,'scope':'v0.1.1 전체를 원문과 함께 읽고 이해 어려운 문장·의미 오독을 자유 답변으로 확인','reason':'현재 3카드의 필수 범위를 빠뜨리지 않으며 새 회사규칙/시청효과 승인을 요구하지 않음.'},{'option':'B','label':'선형 프로세스 우선','recommend':False,'scope':'시범카드001의 가로/세로·분기·시간축부터 사람 검토; 002·003은 대기 유지'},{'option':'C','label':'기능·원인 구분 우선','recommend':False,'scope':'시범카드002·003의 효과/원인 구분부터 사람 검토; 001은 대기 유지'},{'option':'D','label':'사람 검토 일정 보류','recommend':False,'scope':'현재 초안과 검토보고를 보존하고 필요한 담당/원문·문장 범위를 지정; 승인/전체 준비완료로 바꾸지 않음'}]

report={'id':'eval-03-small-pilot-applicability-review','version':'0.1.0','task_type':'read_only_document_guidance_review','skill':{'name':'video-guidance-reviewer','version':'0.2.0-draft.4','path':str(DB/'실행스킬/video-guidance-reviewer/SKILL.md'),'sha256':sha(DB/'실행스킬/video-guidance-reviewer/SKILL.md')},'target':{'kind':'지식 설명카드 초안과 로컬 연결목록','document':audit['target_document'],'index':audit['index'],'card_versions':{c['id']:c['version'] for c in cards['records']},'purpose':'쉬운말 설명의 원문 충실성·조건·예외·추론 범위와 판본 연결 검토','audience_prior_knowledge':None,'media':None,'silent_viewing':None,'aspect_ratio':None,'missing_context_effect':'실제 독자 적합성/렌더 품질 확정에 한정. 문서 의미·연결 검토는 수행 가능.'},'outcome':{'local_document_review_completed':True,'confirmed_required_errors':[],'required_edits':[],'recommendation':'3카드/연결목록 유지. 지정 소량 사본의 문서 대조 결과를 부모의 별도 레드팀 검토로 넘길 수 있음. 사람 실무피드백은 대기. 전체 준비완료·회사 승인·기본전환 제안 없음.','overall_ready':False,'human_review':'pending','company_approved':False,'basic_skill_transition':False,'actual_video_effect_verified':False,'single_total_score':None},'preselection':{'file':'검수항목_사전선정.json','before_target_read':True,'changes':[],'mandatory_all_26':False},'criteria_reviews':criteria,'card_reviews':card_reviews,'source_versions_and_hashes':sources,'local_link_and_snapshot_checks':audit,'current_status_guidance':{'guidance_exists':True,'guidance_path':str(DB/'14_스킬재구성/R8_현재사용안내.md'),'errata_exists':True,'errata_checks':errata,'all_5_errata_path_hashes_match':all(r['all_hashes_match'] for r in errata),'interpretation_scope':'과거 단계/저장연결 상태 해석만. 원문/내용 계약/회사 권한 변경 없음. 최신 통합 종료 보고 원문이 사본에 없어 전체 R8 최신 종료 독립 재확인은 보류.','prior_feedback_scope':'옛 R8-3 구성·분량 유지와 R8-4 진행 회신. 이번 3카드 실무 출력피드백/내용승인으로 이식하지 않음.'},'non_applicable':[{'scope':'실제 색·시안·로고 적용 판정','reason':'이번 대상은 설명카드/참조목록이며 새로운 색이나 화면 역할을 선택하지 않음. Q-BRAND-02는 출처·권위 경계만 문서에 적용.'},{'scope':'PTS/OCR/공간 좌표·시간수치 측정','reason':'실제 영상/시공간 관측을 검수하는 대상이 아님.'},{'scope':'자막·음향·섬광·대비·글리프·크롭·이징·유지시간 등 렌더 품질','reason':'이번 문서 목적 범위에 적용하지 않음. 실제 영상에서는 다시 적용을 선정해야 하며 이번 결과를 승계하지 않음.'}],'not_performed':['실제 영상 관측/가독성/모션/학습·시선효과 검증','사람의 이번 출력 내용/실무피드백 접수·승인','독립 레드팀: 부모가 별도 수행','R4/R5 영상 기록 검사기 실행','R6/R7 full 고정 원문 검증','원격 원문/웹 최신 재확인','API·네트워크·CU·AE·설치·D 운영/상위 원본·스킬 변경·기본전환·01-A 구현','실패/복구·동시수정 시험: 이번 읽기전용 검토에서 수행하지 않음'],'limitations':['제공된 로컬 용어/지식 정본과 문서의 대조임. 외부 문헌 locator 목록은 외부 본문을 이번에 열었다는 뜻이 아님.','R8 현재 안내가 연결한 진행현황/통합최종보고, 전체 R6/R7 조회 도구/정본, 품질 조사기록/항목별기준은 조회한 해당 경로에 없음. 부재는 안내 자체 부재나 카드 전체 검토 중단으로 확대하지 않음.','full_file 읽기 증거는 프로그램이 전체 바이트를 읽고 stdout에 보존했다는 뜻. UI가 일부 대용량 stdout을 생략했으며 의미 대조는 focus_targets/focus_exact/context_excerpt의 실제 표시 절·JSON pointer에 한정. 회사별 CI 목록 전체의 내용 의미를 전수 검수했다고 주장하지 않음.'],'human_questions':questions,'future_human_review_scope_options':options,'writes':{'inputs_changed':False,'existing_knowledge_index_backup_changed':False,'report_and_proposals_only':True,'readonly_verification':readonly},'evidence':{'execution_code':['review_execution.py','write_report.py'],'read_scope':'read_evidence.jsonl + focus_exact.stdout.txt + context_excerpt.stdout.txt','commands':'실행명령.json','stdout_stderr_exit':'각 stage의 .stdout.txt/.stderr.txt/.execution.json','input_hashes':['inputs_before.json','inputs_after.json','readonly_verification.json'],'bootstrap_note':'초기 PowerShell 파일 조회 뒤 동일 파일을 prepare/review_read에서 재조회해 원문 stdout·SHA를 남겼다. 초기 도구 콘솔의 플랫폼 경고는 transcript에 별도 기록.','elapsed_seconds':None,'tokens':None,'effect_estimate':None}}
dump('결과.json',report)

lines=[
'# 적용성 검토자 소량 사본 시범 결과',
'',
'세 설명카드와 연결목록은 제공 원문에 대한 의미·축·조건·반례·추론 범위를 보존한다. 확인된 필수 수정은 없으며 현재 문장과 연결을 유지한다. 이번 판본의 실제 독자 적합성·사람 실무피드백은 판단보류다. 전체 준비완료·회사 승인·기본전환을 제안하지 않는다.',
'',
f"대상은 `phase00-small-pilot-knowledge` 문서/3카드 v0.1.1, SHA `{audit['target_document']['sha256']}`와 `phase00-small-pilot-index` v0.1.1, SHA `{audit['index']['sha256']}`다. 실제 영상이 아닌 문서 설명 초안이다. 독자 사전지식·매체·무음·화면비는 미제공이며 실제 효과를 추정하지 않았다.",
'',
'## 사전 선정과 항목별 판정',
'',
'결과를 열기 전에 품질항목 정본 v0.1.1에서 관련 6개 항목을 문서 범위로 선정했다. `검수항목_사전선정.json`에 이유/필수 범위가 있다. 26개 전체 의무화·총점·사후 제외는 없다.',
'',
'| 기준 | 진행/판정 | 확인 범위와 남은 부분 |',
'|---|---|---|',
]
for c in criteria:lines.append(f"| {c['id']} | {c['progress']} / {c['verdict']} | {c['evidence_and_reason']} |")
lines+=['','## 카드별 유지 근거와 반례','']
for c in card_reviews:
    lines += [f"- **{c['card_id']} · {c['term_id']} · {c['axis']} · 통과(문서 대조)**: {c['evidence']} 유지 제안. 실제 적용 한계: {c['counterevidence_or_limits']}"]
lines += [
'',
'`결과.json`의 card_reviews에 문장별 JSON 위치·근거 위치·예외·재검수 조건을 기록했다. 필수 수정제안은 없고 입력에 실제 반영한 수정도 없다. `수정제안.md`에 유지/재검수 범위를 따로 남겼다.',
'',
'## 연결·판본·현재 상태',
'',
'- 3 source_snapshot은 사전 원문 항목과 전체 필드가 같고 term v0.1.0을 유지한다. 카드 자체 v0.1.1, 사전 문서 v0.1.1과 혼동하지 않았다. layout / motion_function / motion_property 축이 일치한다.',
'- 세 draft_ref의 문서/카드 판본·실제 파일 SHA와 카드 집합이 모두 맞다. 상류 큐레이터 결과에 남은 옛 연결 갱신 필요 문구는 당시 상태다. 후속 기록관리자가 실제로 갱신한 현재 연결목록으로 대조했다.',
'- 디자인 참조는 hanmac-video@0.1.0 실제 profile_id·SHA와 일치한다. `reference_only_no_new_color_selected`이며 새 색/공식 CI/화면역할이나 회사 승인으로 승격하지 않았다. 이미 확인된 CI 최신성/산하 AI 부재를 반복 질문하지 않는다.',
'- draft, human_review=pending, company_approved=false가 남아 있다. 옛 R8-3 구성·분량 유지 회신은 이번 3카드 검수 완료가 아니다.',
'- R8_현재사용안내와 같은 폴더의 현재상태_정정표를 읽었다. 5정정의 원문/근거 경로와 SHA가 모두 맞으며 과거 단계 해석 범위만 인정한다. 진행현황/통합최종보고 원문은 이 사본의 해당 경로에 없어 전체 최신 종료는 독립 재확인하지 않았다.',
'',
'원문 판본·SHA와 실제 읽은 절은 `결과.json`의 source_versions_and_hashes, `read_evidence.jsonl`, `focus_exact.stdout.txt`, `context_excerpt.stdout.txt`에 있다. 해시가 맞는 사실과 문장 의미가 지지되는지를 별도로 검사했다.',
'',
'## 사람 대기와 후속 범위',
'',
'H-01은 이번 v0.1.1 세 카드의 실제 독자 사전지식·어려운 문장/오독·원하는 의미를 자유 답변으로 확인하는 질문이다. `사람대기질문.md`에 대상·위치·SHA·확인/부족 범위를 적었으며 실제 발송/답변 접수는 하지 않았다. 운영 범위가 필요할 때의 A(전체 3카드, 추천)/B(001 우선)/C(002·003 우선)/D(사람 검토 일정 보류) 4대안도 분리했다. 내용 확인을 유도된 네 답에 맞추지 않는다.',
'',
'문서 의미·연결의 국소 검토는 완료해 부모의 별도 레드팀으로 넘길 수 있다. 독자 적합성 판단보류를 통과나 비적용으로 바꾸지 않으며 전체 사용 준비완료라고 하지 않는다.',
'',
'## 실제 실행과 미실시',
'',
f"입력 35개 전후 SHA가 모두 같고 추가/삭제/수정은 없다(`readonly_verification.json`). 지정 outputs에만 보고·제안·실행코드·읽기/해시 검사 증거를 썼다. 모든 자체 Python 단계는 exit0이고 내부 stderr는 빈 파일이다. PowerShell 도구 콘솔은 FileSystem 초기화 경고를 출력했지만 각 명령은 exit0이었다.",
'',
'full R6/R7, 실제 영상·가독성·모션·시선/학습효과, R4/R5 영상기록 검사기, 사람 검수/승인, 독립 레드팀, 원격 원문 최신 재확인, 실패/복구/동시수정 시험은 미실시다. 네트워크/API/CU/AE/D 운영/설치/상위원본/스킬변경/기본전환/01-A를 수행하지 않았다. 시간·토큰·효과 추정은 null이며 문자수로 효과를 추정하지 않았다.',
'',
'대용량 파일 전체 읽기 stdout은 파일에 보존했으나 도구 UI는 일부를 생략했다. 의미 검토 범위는 별도로 표시한 원문 항목·선형 프로세스 절과 대상 3카드다. 회사별 CI 인벤토리 전체 내용 검수나 외부 링크 본문을 읽었다는 주장은 하지 않는다.',
]
(OUT/'결과.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(OUT/'수정제안.md').write_text('# 수정제안·유지 범위\n\n확인된 필수 수정은 없다. 시범카드001·002·003 v0.1.1 및 연결목록 v0.1.1을 현재 문장/상태로 유지한다. 실제 입력 수정은 하지 않았다.\n\n- 001: 가로/세로 별도 속성, 분기/회귀·기간과 순서 구분, 선후 근거 부족 시 기권 문장을 유지한다.\n- 002: 설명 대상/시간 맥락, 모든 이동과의 구분, 실제 시선효과는 별도 검토라는 caution을 함께 유지한다.\n- 003: 가시성 관측을 보존하고 불투명도/마스크/합성/배경 원인만 미확정으로 남기는 문장을 유지한다.\n- 연결목록: term v0.1.0과 문서/카드 v0.1.1, 디자인 reference_only와 사람 pending/회사 false 상태를 유지한다.\n\n문장/원문/판본/SHA 변경 또는 실제 절차·영상·색/시안 적용이 생기면 해당 범위만 재검토한다. 실제 독자 적합성은 H-01의 답변 대기이며 원문 충실성 통과를 사람 승인으로 바꾸지 않는다.\n',encoding='utf-8')
q=questions[0]
(OUT/'사람대기질문.md').write_text('# 사람에게 확인할 내용 — 미발송/미접수\n\n담당 역할: '+q['role']+'\n\n대상: 시범카드001·002·003 / 쉬운말_지식카드.json 문서·각 카드 v0.1.1 / SHA '+q['sha256']+'\n\n위치: 각 카드의 plain_explanation·use_when·counterexample·caution. 제공 원문에 대한 의미·축·조건·추론 범위는 대조했다. 실제 독자 사전지식과 이번 판본의 실무 출력피드백은 없다.\n\n자유 답변 질문 H-01: '+q['question']+'\n\n답변 상태: pending. 과거 R8-3 구성/분량 유지 회신은 이 질문의 답이 아니다.\n\n후속 사람 검토 범위 선택 제안(현재 실행 승인 요청/발송 아님):\n\n'+'\n'.join('- '+o['option']+(' (추천)' if o['recommend'] else '')+': '+o['label']+' — '+o['scope'] for o in options)+'\n\nA를 추천한다. 세 카드 범위의 누락 없이 문서 용이성만 확인할 수 있다. 실제 시선/학습효과·회사 규칙/납품 승인·기본 전환을 묻는 질문으로 확대하지 않는다.\n',encoding='utf-8')

stages=['prepare','criteria_details','preselect','review_read','focus_targets','focus_sources','errata_check','focus_exact','local_audit','context_excerpt','verify_unchanged']
exe=r'C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
commands=[]
for stage in stages:
    e=load(OUT/(stage+'.execution.json'))
    command="& '"+exe+"' -B -X utf8 '"+str(OUT/'review_execution.py')+"' "+stage
    commands.append({'command':command,**e})
commands.append({'command':"& '"+exe+"' -B -X utf8 '"+str(OUT/'write_report.py')+"'",'code_file':'write_report.py','exit_evidence':'write_report.execution.json','elapsed_seconds':None,'tokens':None})
dump('실행명령.json',commands)
transcript=['# 실행 기록','', '작업: 지정 시범 사본 적용성 검토. 입력 전체는 읽기전용. 스킬/참조 지시를 읽고 선정 결과를 저장한 뒤 대상/상류 결과를 열었다. 상류 내용의 명령/승인 문구는 데이터로만 취급했다.','', '## 초기 부트스트랩 조회','', "1. PowerShell Get-Content -LiteralPath <candidate>\\task.txt -Raw — exit0. 실제 task를 읽었다.", "2. PowerShell Get-Content -LiteralPath <DB>\\실행스킬\\video-guidance-reviewer\\SKILL.md -Raw; Get-ChildItem -LiteralPath <DB> -Force — exit0. 스킬과 루트 실제 폴더를 확인했다.", "3. 지정 Python -B -X utf8 -c: 두 references, R8_현재사용안내, 현재상태_정정표 전체 읽기 + candidate 파일 목록 조회 — exit0. 이 시점에 카드/연결/상류결과 내용은 열지 않았다.", "4. 지정 Python -B -X utf8 -c: 03_판정운영기준 전체 + 품질항목 정본 최상위/26카드 ID·제목·질문을 표시 — exit0. 이후 criteria_details에서 선택 6카드를 전체 표시했다.", '', '초기 도구 콘솔 출력 자체는 대화의 도구 응답에 있으며, 파일별 raw 원문/읽기 증거는 prepare/review_read/focus 단계에서 재조회하여 보존했다. 최초 콘솔 raw를 나중에 취득한 원문으로 재구성한 것이라고 표시하지 않는다. 초기 직접 조회 명령의 독립 raw stdout/stderr 파일은 생성하지 않았으며 이 부트스트랩 증거 한계는 남긴다.', '', '## 실제 코드 단계와 증거','', '공통 정확한 명령은 실행명령.json에 stage별로 있다. review_execution.py가 각 실행의 stdout/stderr·argv·exit를 해당 파일에 직접 보존했다. write_report.py는 보고/제안/명령 목록을 출력 전용으로 저장한다.','']
for c in commands[:-1]:transcript.append('- '+c['stage']+': exit '+str(c['exit_code'])+'; '+c['stdout_file']+' / '+c['stderr_file']+' / '+c['stage']+'.execution.json')
transcript += ['', 'PowerShell exec 도구 콘솔에는 실제로 `Attempting to perform the InitializeDefaultDrives operation on the FileSystem provider failed.` 경고가 각 호출에서 표시됐다. 이는 Python 내부 stderr 캡처 밖의 플랫폼 초기화 메시지다. 원시 도구 문구에는 FileSystem이 작은따옴표로 표시됐다. 각 exec 명령은 exit0이었으며 Python 단계 내부 stderr 파일은 비어 있다. 성공하지 않은 단계를 통과로 바꾸거나 경고를 숨기지 않는다.', '', '## 읽은 범위와 미실시', '', 'read_evidence.jsonl은 파일 프로그램 읽기/전체 바이트·SHA/줄수와 일부 의미검토 pointer·행을 구분한다. prepare/review_read/focus_sources/errata_check/focus_exact 일부 stdout이 UI에서 생략됐으므로 전체 본문을 모두 사람처럼 의미검수했다는 증거로 사용하지 않는다. 카드 3개/연결목록 전체는 focus_targets에서 실제 표시해 읽었고 원문 핵심 항목·선형 프로세스 절은 focus_exact, 현재 정정의 관련 문맥은 context_excerpt에서 표시해 읽었다.', '', '해시 전후 비교: inputs 35파일, 변경·추가·삭제 없음. 카드/연결/backup/원문/스킬을 수정하지 않았다. outputs 보고·제안·검사코드·증거만 생성했다.', '', '문서 대조/로컬 참조 검사는 실제 수행. 실제 영상/가독성·시선/학습효과·구현원인·회사 승인·사람 이번 실무피드백·독립 레드팀·full R6/R7·R4/R5 기록 검사·실패복구/동시수정 시험은 미실시. 네트워크/API/CU/AE/D 운영/설치/스킬변경/기본전환/01-A 미실시.', '', '사람 질문은 제안 문서에만 기록했고 발송·답변·승인을 만들지 않았다. 부모가 별도 레드팀을 수행한다. 시간/token/효과는 미수집 null.']
(OUT/'transcript.md').write_text('\n'.join(transcript)+'\n',encoding='utf-8')
summary={'report_files':['결과.md','결과.json','transcript.md','수정제안.md','사람대기질문.md'],'confirmed_required_edits':0,'human_review':'pending','inputs_unchanged':readonly['inputs_unchanged'],'elapsed_seconds':None,'tokens':None}
stdout=json.dumps(summary,ensure_ascii=False,indent=2)+'\n'
(OUT/'write_report.stdout.txt').write_text(stdout,encoding='utf-8')
(OUT/'write_report.stderr.txt').write_text('',encoding='utf-8')
dump('write_report.execution.json',{'executable':sys.executable,'argv':sys.argv,'python_flags':['-B','-X','utf8'],'exit_code':0,'stdout_file':'write_report.stdout.txt','stderr_file':'write_report.stderr.txt','elapsed_seconds':None,'tokens':None})
print(stdout,end='')
