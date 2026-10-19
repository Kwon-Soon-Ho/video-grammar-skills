from pathlib import Path
import sys,json,shutil,re
from datetime import datetime
from zoneinfo import ZoneInfo
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'phase01a-a2'))
from prepare import ROOT,sha,write
P='Phase 01-A';OP=f'{P}/06_도구와계약/01-A2_모션검수절차';PRE=f'{OP}/스킬작성전_재발시험';VE=f'{P}/04_검증자료/01-A2_스킬작성전_통과조건';BK=f'{P}/backup/2026-10-16_01-A2_스킬작성전_통과조건';IMP='작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A2'
GUIDE=f'{PRE}/00_스킬작성전_통과조건.md';NOTICE=f'{P}/00_진행안내/18_01-A2_스킬작성전_통과조건_현재안내.json';REPORT=f'{P}/05_결과보고/11_01-A3_작성전_실패재발_통과조건.md'
STAGE=HERE/'게시안';STAGE.mkdir(exist_ok=True);before={};now=datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds')
def read(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8-sig'))
def put(rel,data):
    dst=ROOT/rel
    if dst.exists():
        before[rel]=sha(dst);back=STAGE/BK/'변경전'/rel;back.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dst,back)
    dest=STAGE/rel;dest.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(data,str):dest.write_text(data,encoding='utf-8')
    else:write(dest,data)
def build():
    old_receipt=f'{P}/04_검증자료/01-A2_전체모션재검수/사람확인_N1-N8과_빛커서정정_회신.json'
    old_e=f'{P}/04_검증자료/01-A2_작은예비/사람확인_6묶음과_E모션보완_회신.json'
    assert (ROOT/old_receipt).is_file() and (ROOT/old_e).is_file()
    inputs=read(f'{P}/00_진행안내/09_제공자료_묶음목록.json')
    raw=json.loads((HERE.parent/'phase01a-a2/입력고정과_컨테이너사전점검.json').read_text(encoding='utf-8'))
    asset={r['id']:r for r in raw}
    specs=[
      ('T01','자료013',[3.5,5.5],'조각 조립과 감속',['E를 한 덩어리 색 전환으로만 쓰지 않고 조각별 진입을 식별','좌→우 이동','초반 빠르고 끝에서 느려짐을 관측 곡선군으로 기록'],old_e,'human_confirmed'),
      ('T02','자료013',[0,1.4],'얇은 빛과 배경 보조 동작',['E 주변의 얇은 발광선/빛 통과를 본체와 별도 식별','가감속을 못 정해도 존재 관측을 지우지 않음','측정하지 않은 경로/정확한 이징을 확정하지 않음'],old_receipt,'user_provided_correction'),
      ('T03','자료013',[1,3.8],'커서·점선·가시성 연동',['십자 커서와 점선 사각형을 각각 식별','선택 영역 확대에 따른 큰 영문 공개','점선 영역 축소와 연한 문구 잔존의 순서','글자 자체 크기 축소나 실제 AE Opacity/마스크 구성으로 단정하지 않음'],old_receipt,'user_provided_correction'),
      ('T04','자료005',[6,18],'차트 본체·수치·채움과 순서',['수주→매출→이익의 데이터 변화 순서','막대 상향 성장·원형 시계방향 채움·숫자 증가를 각각 식별','정착부 감속 관측','카드 틀 등장을 데이터 동작 순서와 혼동하지 않음'],old_receipt,'human_confirmed'),
      ('T05','자료005',[5.9,6.6],'전환과 위치 이동 구분',['겹쳐 바뀌는 크로스페이드를 식별','슬라이드·카메라 이동으로 잘못 확정하지 않음','혼합 진행량의 감속형을 관측 속성에 연결'],old_receipt,'human_confirmed'),
      ('T06','자료013',[10.6,15.5],'복합 동작·가림·독립 광량',['기존 창 재배치와 새 창 진입의 순서/중첩을 분리','기존 창 우하단 축소와 새 창 오른쪽 진입을 구분','모델 우하단 확대와 광점/빛띠 밝기를 분리','가시성과 위치/크기의 가감속을 하나로 묶지 않음'],old_receipt,'human_confirmed')]
    public=[];answers=[]
    for id,aid,window,name,checks,ref,level in specs:
        item=asset[aid]
        public.append({'case_id':id,'media_path':item['path'],'media_sha256':item['sha256'],'allowed_window_seconds':window,'prompt':'이 구간에서 보이는 대상과 변화를 스킬 없이 분석하세요. 작은 보조 요소와 화면 내부도 살피고, 위치·크기·형태·가시성·광량·순서·가감속을 근거 시점과 함께 기록하세요. 정지/비적용/미분류에는 이유를 적고 관측과 구현 추정을 구분하세요. 추가로 사용자가 특정 동작을 지적해 주는 것을 기다리지 말고 결과를 먼저 저장하세요.'})
        answers.append({'case_id':id,'failure_family':name,'reference_level':level,'reference_receipt':ref,'reference_sha256':sha(ROOT/ref),'must_check':checks,'grading':'원본/허용 범위와 분석 출력을 의미 단위로 대조. 문구/ID 존재·문자 수·원본 링크만으로 채점하지 않음.','critical_failure':'필수 대상/사건 누락, 반대 방향/순서 확정, 관측량 혼동, 근거 없는 구현 단정','uncertainty_policy':'빛의 정확한 곡선처럼 기준답안에도 미정인 속성은 존재/방향 관측과 분리해 적절한 보류로 처리'})
    put(f'{PRE}/분석입력/중립과제.json',{'version':'0.1','purpose':'A2 pre-skill known-failure procedure replay','new_skill_available':False,'cases':public,'exposure':'all sources already exposed in this chat; this is not unseen-source generalization','do_not_provide_to_analyzer':['채점전용 기준답안','이전 분석/사용자 정정/관측표/실패 사례 제목'],'access_separation':'input/answer files separated by workflow; no OS-level secrecy or agent context isolation claimed'})
    put(f'{PRE}/채점전용/실패사례와_내용대조기준.json',{'version':'0.1','frozen_at':now,'required_known_failure_cases':answers,'reference_scope':'only prior human-confirmed or direct user-corrected content is mandatory. AI refinements are not silently promoted to human gold.','AI_candidate_additions':[{'name':'UI 선택행/미리보기 순차 교체','state':'AI-observed candidate, not independently human-confirmed','use':'supplementary diagnostic, no human-gold claim'},{'name':'도면과 모델 사이 반투명 연결면','state':'AI-observed candidate, not independently human-confirmed','use':'supplementary diagnostic, no human-gold claim'}],'negative_controls':[{'name':'장헌 도입 정지 후보','state':'technical/AI observation, not new human gold','failure_to_look_for':'압축 차이를 의도된 pan으로 확정'},{'name':'기록은 채웠지만 방향·정지·선택변화를 틀리게 설명','evidence':f'{VE}/기존검사_내용오류_반례.json','failure_to_look_for':'형식 통과를 내용 통과로 사용'}]})
    evidence=json.loads((HERE/'기존검사_내용오류_반례.json').read_text(encoding='utf-8'));put(f'{VE}/기존검사_내용오류_반례.json',evidence)
    criteria={'version':'0.1','scope':'A2 local regression before A3 authoring; not full A4/A5 performance evaluation','frozen_at':now,'must_complete':['freeze_neutral_input_and_reference_versions','save_new_procedure_execution_output_before_grading','compare_video_claims_with_reference_content_and_evidence','resolve_all_critical_failures_in_confirmed_known_cases','rerun_affected_cases_after_method_changes','record_limits_exposure_and_human_burden'],'not_sufficient':['49 object names present','441 cells filled','source hashes match','six structural fault injections caught','old corrected reports copied as a new run','all properties marked unknown'],'fail_closed_conditions':['no new behavior run','content grading not performed','required confirmed event omitted','wrong direction/order asserted','unexplained residual region closed as static','unsupported exact AE implementation','new detail inherits previous human approval'],'acceptable_deferred_scope':['exact thin-light path/curve when not established by the reference','exact AE keyframe/preset/handle recovery','whole-video/audio or A4/A5 generalization claims'],'no_aggregate_score_or_invented_pass_rate':True,'A4_A5_plan_preserved':True,'human_confirmation_for_same_details_not_reasked':True,'A3_authoring_is_separate_user_stage_decision':True}
    put(f'{PRE}/01_착수판정기준.json',criteria)
    state={'recorded_at':now,'record_structure_check':'performed','content_counterexample_diagnostic':'performed: three false motion statements still pass old structure checker','neutral_cases_and_reference':'prepared and version-pinned','new_procedure_behavior_replay':'not_run_after_criteria_freeze','content_grading':'not_run','independent_or_unseen_validation':'not_run','A3_authoring_ready':False,'skill_created':False,'A3_started':False,'reason':'새 절차의 실제 분석 출력과 내용 대조가 필요. 형식 검사/사후 정정만으로 작성 준비 완료 처리하지 않음.','next_action':'동일 원본·허용 구간·도구로 중립 과제를 실행해 원본 분석 출력을 먼저 고정하고 그 뒤 내용 대조. 노출 이력을 기록. A4/A5 확대/미노출 검증과 구분.'}
    put(f'{PRE}/02_현재판정.json',state)
    guide='''# 스킬 작성 전에 분석 방법부터 통과시키기

사용자 의도는 이번 사례를 더 잘 설명하는 데서 끝나지 않고, 같은 누락이 새 스킬 안에서 반복되지 않게 하는 것입니다. 01-A2에 **스킬 작성 전 재발 시험**을 추가합니다. 현재 새 스킬을 만들거나 A3를 시작한 것은 아닙니다.

## 지금까지 보완의 빈틈

대상49개·속성441칸과6개 기록 오류 검출은 대상/필드/근거 연결 검사입니다. 영상의 의미를 맞게 파악했다는 시험이 아닙니다. 격리한 사본에서 커서 정지 오판·E의 반대 방향·UI 선택 변화 부정을 넣어 봤더니 세 경우 모두 기존 형식 검사를 통과했습니다. 기존 파일은 수정하지 않았습니다.

## 스킬 작성 전 통과할 것

1. **실패 사례를 먼저 기준으로 고정합니다.** E 조각·빛·커서/점선·차트 순서·전환·복합 창/모델/빛의6과제를 기존 사람 회신과 연결했습니다. 뒤늦게 맞춰 고친 출력을 새 시험 성공으로 세지 않습니다.
2. **분석을 먼저, 채점은 나중에 합니다.** 분석자에게는 중립 과제와 허용 원본/구간/도구/절차를 줍니다. 사례별 정답·사용자 정정·이전 분석 결과는 채점 쪽에 둡니다. 입력/답안 파일의 분리는 운영상 분리이며 접근 통제나 문맥 격리가 이미 이뤄졌다는 뜻은 아닙니다.
3. **동작 내용으로 판정합니다.** 필수 대상과 보조 요소를 실제로 발견했는지, 방향·순서·가감속·중첩을 맞게 설명했는지 원본과 대조합니다. 이름이나 칸을 채운 것만으로 통과시키지 않습니다. 존재를 놓친 것과 정확한 곡선만 미정인 것을 다르게 다룹니다.
4. **같은 실패가 남으면 절차를 고칩니다.** 확인된 필수 사건의 누락·반대 방향/순서·관측량 혼동·근거 없는 AE 단정이 남으면 작성 준비 완료로 표시하지 않습니다. 다른 항목을 많이 맞혔다는 이유로 상쇄하지 않습니다. 수정 영향 구간을 다시 시험하고 실패 이력을 보존합니다.
5. **검증된 절차만 A3에 옮깁니다.** 짧은 스킬 본문은 대상 발견→시간 대조→잔여 변화 조사→근거/불확실성 기록을 호출하고, 상세 검수표·실패 처리·시험 자료는 참조/보조 도구로 분리할 예정입니다. 장헌/EG 특정 화면의 정답이나49개 대상 목록을 모든 영상의 규칙으로 넣지 않습니다.

## 준비된 작은 시험

| 과제 | 이번에 막아야 할 실패 |
|---|---|
| T01 | E 조각의 좌→우 진입과 감속을 한 덩어리 색 변화로 축약 |
| T02 | 얇은 빛을 배경 일반 묘사로만 적고 독립 동작을 누락 |
| T03 | 십자 커서·점선 영역·문구 가시성의 연동과 축소 순서 누락 |
| T04 | 차트 막대·채움·숫자·데이터 변화 순서를 한 동작으로 묶음 |
| T05 | 크로스페이드를 슬라이드/카메라 이동으로 오판 |
| T06 | 기존 창·새 창·모델·광량의 중첩과 서로 다른 가감속을 혼용 |

모든 과제는 이미 본 장헌0~24초/EG0~15.5초 안입니다. 미노출/독립 정확도 시험이라고 부르지 않습니다. UI 내부 선택 교체와 반투명 연결면은 AI 관측 후보로 따로 보관하며 사람 기준답안으로 자동 승격하지 않았습니다. 새로운 원본의 확장 비교와 고정 평가 수치/허용오차는 기존 A4/A5에서 다룹니다.

## 현재 상태

**실패 기준·중립 입력·채점 기준·착수 조건은 준비했습니다. 기준 고정 뒤 실제 행동 재시험과 내용 채점은 아직 실행하지 않았습니다. 따라서 스킬 작성 준비 완료는 아닙니다.** 이전 재검수·사후 정정은 개발 근거로 보존하며 새 실행을 대체하지 않습니다.

원본 AE 키프레임을 요구하지 않습니다. 영상에서 관측 가능한 가감속의 분류와 정확한 원본 핸들 복원은 다릅니다. 얇은 빛의 정확한 곡선처럼 기준에도 미정인 속성은 이유를 붙여 보류할 수 있지만, 그 때문에 동작의 존재까지 누락하면 안 됩니다.

추가로 같은 화면의 승인을 다시 요청하지 않습니다. A3 착수 여부는 [현재 판정](02_현재판정.json)에 연결합니다. [착수 기준](01_착수판정기준.json), [중립 분석 입력](분석입력/중립과제.json), [기존 형식 검사의 반례](../../../04_검증자료/01-A2_스킬작성전_통과조건/기존검사_내용오류_반례.json)를 함께 보관합니다.
'''
    put(GUIDE,guide)
    report='# 01-A3 작성 전 실패 재발 통과조건\n\n'+guide.split('\n',1)[1]
    report=report.replace('(02_현재판정.json)',f'(../06_도구와계약/01-A2_모션검수절차/스킬작성전_재발시험/02_현재판정.json)').replace('(01_착수판정기준.json)','(../06_도구와계약/01-A2_모션검수절차/스킬작성전_재발시험/01_착수판정기준.json)').replace('(분석입력/중립과제.json)','(../06_도구와계약/01-A2_모션검수절차/스킬작성전_재발시험/분석입력/중립과제.json)').replace('(../../../04_검증자료/','(../04_검증자료/')
    put(REPORT,report)
    oprel=f'{OP}/00_실행검수절차.md';op=(ROOT/oprel).read_text(encoding='utf-8').replace('v0.1','v0.2',1)
    op+='\n\n## 스킬 작성 전 필수 내용 시험\n\n기록 검사 통과를 영상 내용 통과나 A3 작성 준비 완료로 쓰지 않습니다. [스킬 작성 전 통과조건](스킬작성전_재발시험/00_스킬작성전_통과조건.md)에 따라 중립 입력의 실제 분석 출력을 먼저 저장하고, 원본과 기준답안을 내용으로 대조합니다. 확인된 필수 사건의 누락·오탐이 남으면 절차를 보완하고 영향 구간을 재시험합니다. 현재 실행/미실행은 [착수 판정](스킬작성전_재발시험/02_현재판정.json)에서 확인합니다.\n'
    put(oprel,op)
    planrel=f'{P}/00_진행안내/01-A_계획상태.json';plan=read(planrel)
    plan.update(version='0.9',state='A2_pre_skill_acceptance_prepared_behavior_replay_not_run',next_decision='A2 스킬작성전 실제 행동 재시험 및 내용 대조. A3 작성 준비 완료 아님.',stage_A2_report=REPORT.removeprefix(P+'/'),stage_A2_current_notice=NOTICE.removeprefix(P+'/'),A3_started=False,skill_created=False,pre_skill_acceptance_state=f'{PRE}/02_현재판정.json',A3_authoring_ready=False,stage_A2_status='현재 구간 재대조 근거 보존. 스킬 작성 전 필수 내용 시험 기준/입력/채점안 준비. 기준 고정 후 행동 재시험·내용 채점 미실행.')
    put(planrel,plan)
    notice={'date':now,'state':plan['state'],'guide':GUIDE,'report':REPORT,'decision':f'{PRE}/02_현재판정.json','A3_started':False,'skill_created':False,'A3_authoring_ready':False,'prior_human_confirmations_preserved':True,'questions_to_repeat_to_user':[],'new_behavior_replay_run':False,'meaningful_check_this_turn':'3 content-error counterexamples passed old structural validator; old checker not a semantic evaluator'}
    put(NOTICE,notice)
    previous=f'{P}/00_진행안내/17_01-A2_누락방지검수_현재안내.json';prev=read(previous);prev['pre_skill_acceptance_supplement']=NOTICE;put(previous,prev)
    canonical='00기획/07_Phase01-A_진행계획.md';text=(ROOT/canonical).read_text(encoding='utf-8')
    prefix=f'''> 2026-10-16 현재 상태 보완: 01-A2 실제 영상 재검수와 누락 정정까지 수행했습니다. 스킬 작성 전에 확인된 실패를 재시험하는 조건을 추가했습니다. **기준 고정 후 행동 재시험·내용 대조는 미실행이므로 A3 작성 준비 완료가 아닙니다.** [스킬 작성 전 조건](../{GUIDE})과 [현재 판정](../{PRE}/02_현재판정.json)을 우선 적용합니다. 아래의 “미실행/예정” 문장은 당시 계획 이력입니다. 기존 A4/A5 확장·평가 범위는 유지합니다.\n\n'''
    put(canonical,prefix+text)
    checkplan=f'{P}/00_진행안내/12_단계별검수와_레드팀계획.md';old=(ROOT/checkplan).read_text(encoding='utf-8')
    put(checkplan,f'> 후속 보완: A2→A3 사이에 [스킬 작성 전 내용 재발 시험](../06_도구와계약/01-A2_모션검수절차/스킬작성전_재발시험/00_스킬작성전_통과조건.md)을 적용합니다. 형식 검사·이전 정정 결과만으로 A3 작성 준비 완료로 판정하지 않습니다. 아래 단계표는 기존 계획을 보존한 이력입니다.\n\n'+old)
    put(f'{IMP}/보완과_재시험/스킬작성전_통과조건_현재안내.md',f'# 스킬 작성 전 통과조건\n\n[준비한 시험·현재 상태](<{(ROOT/GUIDE).as_posix()}>)\n\n원본을 보는 실제 분석 행동 재시험과 내용 채점은 미실행. 형식 검사 통과만으로 A3 작성 준비 완료 판정하지 않음. 기존 사람 회신 유지.\n')
    for p in HERE.glob('*.py'):
        dest=STAGE/BK/'실행코드'/p.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    write(HERE/'게시명세.json',{'before':before,'files':[{'path':p.relative_to(STAGE).as_posix(),'sha256':sha(p)} for p in STAGE.rglob('*') if p.is_file()]})
    print(json.dumps({'cases_prepared':len(specs),'behavior_replays_executed':0,'A3_ready':False,'content_gap_controls':3},ensure_ascii=False))
def publish():
    m=json.loads((HERE/'게시명세.json').read_text(encoding='utf-8'));allowed=[PRE+'/',VE+'/',BK+'/',IMP+'/'];names={GUIDE,REPORT,NOTICE,f'{OP}/00_실행검수절차.md',f'{P}/00_진행안내/01-A_계획상태.json',f'{P}/00_진행안내/17_01-A2_누락방지검수_현재안내.json','00기획/07_Phase01-A_진행계획.md',f'{P}/00_진행안내/12_단계별검수와_레드팀계획.md'};links=0
    from urllib.parse import unquote
    for item in m['files']:
        rel=item['path'];src=STAGE/rel;dst=(ROOT/rel).resolve();assert dst.is_relative_to(ROOT.resolve()) and (rel in names or any(rel.startswith(p) for p in allowed)),rel
        assert sha(src)==item['sha256'];assert not dst.exists() or sha(dst)==item['sha256'] or sha(dst)==m['before'].get(rel),rel
        if src.suffix=='.json':json.loads(src.read_text(encoding='utf-8-sig'))
        if src.suffix=='.md' and not rel.startswith(BK+'/'):
            for ref in re.findall(r'\]\(([^)]+)\)',src.read_text(encoding='utf-8')):
                ref=unquote(ref.strip('<>'))
                if ref.startswith(('http:','https:')):continue
                target=Path(ref).resolve().relative_to(ROOT.resolve()) if re.match('^[A-Za-z]:',ref) else (ROOT/Path(rel).parent/ref).resolve().relative_to(ROOT.resolve())
                assert (STAGE/target).is_file() or (ROOT/target).is_file(),(rel,ref)
                links+=1
    if '--publish' not in sys.argv:print(json.dumps({'staged_files':len(m['files']),'links_verified':links,'prepublication_passed':True}));return
    for item in m['files']:
        dst=ROOT/item['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(STAGE/item['path'],dst);assert sha(dst)==item['sha256']
    receipt={'saved_files':len(m['files']),'all_hashes_match':True,'actual_content_test_not_run':True,'new_skill_not_created':True,'A3_authoring_ready':False,'source_media_modified':False}
    write(ROOT/VE/'게시후_검증.json',receipt);write(HERE/'게시후_검증.json',receipt);print(json.dumps(receipt))
if __name__=='__main__':
    if '--check' in sys.argv or '--publish' in sys.argv:publish()
    else:build()
