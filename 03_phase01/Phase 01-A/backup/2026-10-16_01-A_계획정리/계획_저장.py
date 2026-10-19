"""Publish planning documents only; no video access, skill creation or evaluation."""
import pathlib,json,hashlib,os,re,shutil
from urllib.parse import quote,unquote
W=pathlib.Path(__file__).resolve().parent;ST=W/'게시안';ST.mkdir(exist_ok=True)
P=pathlib.Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증');D=P/'Phase 01-A';F=P/'Phase 00';targets=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def target_link(p,base):
    try:r=os.path.relpath(p,base.parent).replace('\\','/')
    except ValueError:r=p.as_posix()
    return quote(r,safe='/:._-')
def link(p,base,label=None):return '['+(label or p.name)+']('+target_link(p,base)+')'
def stage(rel,text):
    p=P/rel;s=ST/rel;s.parent.mkdir(parents=True,exist_ok=True);s.write_text(text if isinstance(text,str) else json.dumps(text,ensure_ascii=False,indent=2)+'\n','utf-8');targets.append({'relative':rel,'before':sha(p) if p.exists() else None,'after':sha(s)})
source_rels=[
'00_시작안내.md','01_진행현황.md',
'01_공통용어/공통용어사전.json','01_공통용어/분류운영규칙.json','01_공통용어/02_기록단위와분류축.md',
'02_원칙과레이아웃/모션과정보전달원칙.json','02_원칙과레이아웃/레이아웃지식.json','02_원칙과레이아웃/레이아웃_심화지식.json','02_원칙과레이아웃/화면설계원칙.json',
'03_한맥디자인/한맥디자인정본.json','04_기록규격/통합최소기록_스키마_v0.2.json',
'04_기록규격/02_시간과프레임_기록규격.md','04_기록규격/03_근거와주장_기록규격.md','04_기록규격/04_좌표와변환_기록규격.md',
'05_출처와검토/스킬심층검토/08_기능별_연결표.md','05_출처와검토/스킬심층검토/스킬심층검토정본.json',
'09_다음단계인계/R7_01-A_구현전_인계.md','09_다음단계인계/R6_검수연결_인계.md','13_품질검수/03_판정운영기준.md',
'13_품질검수/평가계획/평가설계_정본.json','13_품질검수/평가계획/지표정의_정본.json',
'14_스킬재구성/R8_현재사용안내.md','14_스킬재구성/현재상태_정정표.json','14_스킬재구성/시범운영/00_최신_시범운영_안내.md','14_스킬재구성/02_도구와_이식범위.md','14_스킬재구성/제한소스_보관과활용_미정.json']
for n in ['video-knowledge-curator','video-record-steward','video-guidance-reviewer']:source_rels.append('06_맞춤스킬/재구성후보/'+n+'/SKILL.md')
sources=[]
for rel in source_rels:
    p=F/rel;assert p.exists(),p;sources.append({'path':p.relative_to(P).as_posix(),'sha256':sha(p),'use':'기존 기준·역할·계획 참조. 실행·개정·성능 검증 아님.'})
for rel in ['00_진행안내/09_제공자료_묶음목록.json','00_진행안내/07_재구성원고_사용자확인.json','00_진행안내/08_가족사7곳_작업기준후보_선택기록.json','00_진행안내/기획서검토_현황.json']:
    p=D/rel;sources.append({'path':p.relative_to(P).as_posix(),'sha256':sha(p),'use':'현재 자료 등록·사용자 답변 참조'})
creator=pathlib.Path(r'C:\Users\User\.codex\skills\anthropic-skill-creator\SKILL.md')
guide_dir='Phase 01-A/00_진행안내/'
details=[('테스트영상_선정안.md',guide_dir+'11_테스트영상_선정안.md'),('검수와레드팀_계획.md',guide_dir+'12_단계별검수와_레드팀계획.md'),('Phase00와_기존스킬_활용표.md',guide_dir+'13_Phase00와_기존스킬_활용표.md')]
mainrel='00기획/07_Phase01-A_진행계획.md';mainp=P/mainrel;main=(W/'진행계획.md').read_text('utf-8')
main+='\n바로가기: '+' · '.join(link(P/r,mainp,l) for l,r in [('시험 영상 선정안',details[0][1]),('검수·레드팀 계획',details[1][1]),('Phase 00·스킬 활용표',details[2][1]),('현재 입력자료 목록',guide_dir+'09_제공자료_묶음목록.md')])+'\n';stage(mainrel,main)
for src,rel in details:
    text=(W/src).read_text('utf-8')+'\n[전체 진행 계획]('+quote(os.path.relpath(mainp,(P/rel).parent).replace('\\','/'),safe='/._-')+')\n'
    if src=='Phase00와_기존스킬_활용표.md':
        text+='\n## 확인한 기준 파일 바로가기\n\n'
        for s in sources:
            if s['path'].startswith('Phase 00/'):text+='- '+link(P/s['path'],P/rel,s['path'])+'\n'
        text+='- '+link(creator,P/rel,'설치된 Anthropic Skill Creator 지침')+'\n'
    stage(rel,text)
stage(guide_dir+'10_01-A_계획_읽는순서.md','# 01-A 계획 — 여기부터 보세요\n\n2026-10-16 / 사용자 계획 검토 대기. 실제 분석·스킬 개발 미시작.\n\n1. '+link(mainp,D/'00_진행안내/10_01-A_계획_읽는순서.md','전체 진행 계획과 A~D 선택안')+'\n2. [첫 시험과 후속 표본](11_테스트영상_선정안.md)\n3. [단계별 검수·레드팀](12_단계별검수와_레드팀계획.md)\n4. [Phase 00·기존 스킬 활용](13_Phase00와_기존스킬_활용표.md)\n\n계획 확인 후에도 먼저 01-A1만 진행해 도구·출력 계약·기능 범위를 보고합니다. 영상·시나리오 묶음은 이미 등록됐으므로 같은 확인을 반복하지 않습니다.\n')
stage('00기획/00_최신기획_읽는순서.md','# 현재 기획의 읽는 순서\n\n2026-10-16\n\n- 현재 01-A 계획: [07_Phase01-A_진행계획.md](07_Phase01-A_진행계획.md)\n- 전체 단계의 초기 배경: [00_최종_파이프라인_계획.md](00_최종_파이프라인_계획.md)\n- 초기 준비/보고 안내는 작성 당시의 자료입니다. 실제 입력 폴더는 이미 생성·등록됐습니다.\n\nPhase 00의 봉인보고·고정 참조는 수정하지 않았고, 최신 관리 스킬의 소량 사본 사용·기본 전환 보류는 유지합니다. 이번 01-A 계획은 검토 대기이며 실제 분석·개발은 시작하지 않았습니다.\n')
samples=[{'role':'첫 예비','id':'자료005','video':'장헌_최종.mp4','input_mode':'재구성 원고 있음','locked':False}, {'role':'초기 무문서 시범','id':'자료013','video':'01_(E).mp4','input_mode':'별도 시나리오 없음','locked':False},{'role':'확대 예비','id':'자료010','video':'1.크레인 작업 반경, 물류·인양 안정성 검토.mp4','locked':False},{'role':'확대 예비','id':'자료017','video':'[EG-Bim]소개영상.mp4','locked':False},{'role':'변형판 스트레스','id':'자료022','video':'싱글·듀얼','locked':False},{'role':'별도 확인 후보','id':'자료014','video':'TOVA 홈페이지 묶음','locked':False},{'role':'별도 확인 후보','id':'자료011','video':'K-GEO FESTA_250919_3.mp4','locked':False}]
plan={'id':'phase01a-development-plan','version':'0.1','date':'2026-10-16','state':'planning_only_pending_user_review','canonical_document':mainrel,'input_bundling_complete':True,'reask_input_pairing':False,'proposed_skill_name':'company-video-grammar-analyzer','skill_created':False,'actual_media_analysis_runs':0,'media_analysis_api_calls':0,'implementation_started':False,'default_skill_promotion':False,'phase00_modified':False,'approved':False,'first_step_after_approval':'01-A1 only','stages':['01-A1','01-A2','01-A3','01-A4','01-A5a','01-A5b','01-A6'],'sample_proposals':samples,'numeric_thresholds':None,'final_evaluation_sample_count':None,'locked_sample_sets':0,'ground_truth_items':0,'actual_scores':None,'redteam_execution_performed':False,'plan_review_type':'작성자의 반대 관점 계획 검토. 독립 실행/레드팀 완료 아님.','choices':{'recommended':'A','A':'장헌→무문서SW→복합→별도확인','B':'무문서SW우선→장헌→확대','C':'장헌·SW의작은기능으로범위축소','D':'수정후검토·착수보류'},'unchanged_management_skill_versions':{'video-knowledge-curator':'0.2.0-draft.3','video-record-steward':'0.2.0-draft.5','video-guidance-reviewer':'0.2.0-draft.4'}}
stage(guide_dir+'01-A_계획상태.json',plan)
stage(guide_dir+'01-A_계획_참조기준.json',{'date':'2026-10-16','kind':'planning_reference_manifest_not_runtime_pin_or_verification','sources':sources,'anthropic_skill_creator':{'path':str(creator),'sha256':sha(creator),'use':'초안·동일조건비교·사람피드백·정적뷰어의 후속 계획만. 실제 도구 호출 없음.'},'existing_fixed_references_changed':False})
s=json.loads((D/'00_진행안내/기획서검토_현황.json').read_text('utf-8'));s.update({'phase01a_plan_created':True,'phase01a_plan_approved':False,'phase01a_plan_ref':'01-A_계획상태.json'});stage(guide_dir+'기획서검토_현황.json',s)
g=(D/'00_먼저읽기.md').read_text('utf-8');g=g.replace('# Phase 01-A 자료 준비 - 여기부터 보세요','# Phase 01-A 자료 준비·진행 계획 - 여기부터 보세요')
g=g.replace('**자료 준비와 기획서 사전 검토까지 진행했습니다. 실제 영상 분석과 스킬 개발은 시작하지 않았습니다.**','**입력자료 연결은 완료했고 01-A 진행 계획은 검토 대기입니다. 실제 영상 분석과 스킬 개발은 시작하지 않았습니다.**\n\n[01-A 전체 계획과 시험 순서](00_진행안내/10_01-A_계획_읽는순서.md)를 먼저 보세요. 계획 확인 후 01-A1부터 단계별로 보고합니다.')
stage('Phase 01-A/00_먼저읽기.md',g)
stage('Phase 01-A/05_결과보고/05_01-A_계획정리_보고.md','# 01-A 진행 계획 정리 보고\n\n2026-10-16 / 계획 검토 대기\n\nPhase 00의 현재 안내·R4 통합 v0.2·R7 평가 계약·R8 후보 세 스킬과 소량 사본 사용 범위, 실제 입력자료 등록 및 사용자 답변을 읽고 진행 계획을 작성했습니다.\n\n장헌 경영보고와 시나리오 없는 EG-BIM 홈페이지를 초기 예비로, 복합 모션·홍보·변형판을 확대 예비로 제안했습니다. TOVA 홈페이지·K-GEO는 별도 확인 후보이며 아직 잠금하지 않았습니다. 문서 사전 노출·같은 시리즈/변형판·재구성 원고의 독립성 한계를 공개했습니다.\n\n기존 관리용 스킬과 새 영상 분석 스킬을 구분하고 단계별 자체검수·레드팀·보완/재시험·사람 검수·보고 계획을 만들었습니다. 수치 기준과 최종 표본 수는 예비 후 검토하도록 미정으로 뒀습니다.\n\n현재 계획 자체를 반대 관점으로 검토해 무문서 입력 누락, 사후 원고를 정답으로 쓰는 문제, 원본 그룹 유출, 형식 통과와 실제 정확성 혼동을 보완했습니다. 독립 검토자/영상 실험을 실행한 것은 아닙니다.\n\n영상 파일은 열지 않았고 프레임 추출·OCR·전사·API 시험·스킬 생성·기본 전환은 하지 않았습니다. 02_분석작업·03_분석스킬·04_검증자료 예약 폴더를 유지했습니다. Phase 00 정본/고정 참조는 변경하지 않았습니다.\n')
# Plan-only checks. None of these is an analysis/evaluation run.
for x in targets:
    dest=P/x['relative'];assert sha(dest)==x['before'] if x['before'] else not dest.exists()
    text=(ST/x['relative']).read_text('utf-8');assert '\ufffd' not in text and not re.search(r'[\u3040-\u30ff]',text)
    if x['relative'].endswith('.md'):
        for u in re.findall(r'\]\(([^)\n]+)\)',text):
            if '://' in u:continue
            to=(dest.parent/unquote(u)).resolve()
            try:staged=ST/to.relative_to(P.resolve())
            except ValueError:staged=None
            assert to.exists() or (staged and staged.exists()),(dest,u)
for name in ['02_분석작업','03_분석스킬','04_검증자료']:assert sorted(x.name for x in (D/name).rglob('*') if x.is_file())==['00_예약폴더_안내.md']
protected={x['path']:x['sha256'] for x in sources if x['path'].startswith('Phase 00/')}
(W/'게시명세.json').write_text(json.dumps({'targets':targets,'plan':plan,'sources':sources},ensure_ascii=False,indent=2),'utf-8')
if os.environ.get('PLAN_PUBLISH')=='1':
    B=D/'backup/2026-10-16_01-A_계획정리';assert not B.exists();B.mkdir(parents=True)
    for x in targets:
        dest=P/x['relative'];assert sha(dest)==x['before'] if x['before'] else not dest.exists()
        if x['before']:
            b=B/'변경전'/x['relative'];b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,b);assert sha(b)==x['before']
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((ST/x['relative']).read_bytes());assert sha(dest)==x['after']
    for rel,h in protected.items():assert sha(P/rel)==h
    for name in ['02_분석작업','03_분석스킬','04_검증자료']:assert sorted(x.name for x in (D/name).rglob('*') if x.is_file())==['00_예약폴더_안내.md']
    result={'date':'2026-10-16','files_published':len(targets),'previous_files_backed_up':sum(bool(x['before']) for x in targets),'phase00_reference_files_unchanged':len(protected),'plan_pending_user_review':True,'actual_media_analysis_runs':0,'skills_created':0,'media_api_calls':0,'evaluation_sets_locked':0,'analysis_skill_eval_executed':False,'planning_document_checks_only':True}
    (W/'저장검증_결과.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
    for f in W.iterdir():
        if f.is_file():shutil.copy2(f,B/f.name)
    R=P/'작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A_진행계획';R.mkdir(exist_ok=False)
    shutil.copy2(D/'05_결과보고/05_01-A_계획정리_보고.md',R/'00_계획정리_보고.md')
    for rel,name in [(mainrel,'01_전체진행계획.md'),(details[0][1],'02_테스트영상_선정안.md'),(details[1][1],'03_단계별검수와_레드팀계획.md'),(details[2][1],'04_Phase00와_스킬활용표.md')]:
        text=(P/rel).read_text('utf-8')
        def fix(mt):
            u=mt.group(1)
            if '://' in u:return mt.group(0)
            to=((P/rel).parent/unquote(u)).resolve()
            return ']('+target_link(to,R/name)+')'
        (R/name).write_text(re.sub(r'\]\(([^)\n]+)\)',fix,text),'utf-8')
    shutil.copy2(W/'저장검증_결과.json',R/'05_계획저장_검증결과.json')
    print(json.dumps(result,ensure_ascii=False))
else:print(json.dumps({'mode':'preflight','planning_files':len(targets),'phase00_references':len(protected),'analysis_started':False},ensure_ascii=False))
