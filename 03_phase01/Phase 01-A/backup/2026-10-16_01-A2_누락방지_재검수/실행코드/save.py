from pathlib import Path
from fractions import Fraction as F
import sys,json,shutil,re
from datetime import datetime
from zoneinfo import ZoneInfo
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'phase01a-a2'))
from prepare import ROOT,sha,write
P='Phase 01-A';AN=f'{P}/02_분석작업/01-A2_누락방지_재검수';VE=f'{P}/04_검증자료/01-A2_누락방지_재검수';OP=f'{P}/06_도구와계약/01-A2_모션검수절차'
BK=f'{P}/backup/2026-10-16_01-A2_누락방지_재검수';IMP='작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A2'
REPORT=f'{P}/05_결과보고/10_01-A2_검수절차보완과_재대조_보고.md';GUIDE=f'{AN}/00_절차보완과_추가발견.md';NOTICE=f'{P}/00_진행안내/17_01-A2_누락방지검수_현재안내.json'
STAGE=HERE/'게시안_확정';STAGE.mkdir(exist_ok=True);before={};now=datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds')
def read(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8-sig'))
def put(rel,obj):
    dst=ROOT/rel
    if dst.exists():
        before[rel]=sha(dst);back=STAGE/BK/'변경전'/rel;back.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dst,back)
    out=STAGE/rel;out.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(obj,str):out.write_text(obj,encoding='utf-8')
    else:write(out,obj)
def cp(src,rel):
    out=STAGE/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,out)
def build():
    mapping={}
    for p in (HERE/'cases').rglob('*'):
        if p.is_file():
            rel=f'{AN}/재추출/{p.relative_to(HERE/"cases").as_posix()}';cp(p,rel);mapping[str(p)]=(ROOT/rel).as_posix()
    # Local source files are preserved under Korean names below; do not depend on C: scratch paths.
    for p in (HERE/'검수판').iterdir():
        if p.is_file():
            rel=f'{AN}/검수판/{p.name}';cp(p,rel);mapping[str(p)]=(ROOT/rel).as_posix()
    matrix=json.loads((HERE/'02_속성검수표.json').read_text(encoding='utf-8'))
    for row in matrix['rows']:
        for pin in row['evidence']:
            src=Path(pin['path'])
            if str(src) not in mapping:
                rel=f'{VE}/기존참조근거/{src.name}';cp(src,rel);mapping[str(src)]=(ROOT/rel).as_posix()
            pin['source_workspace_path']=pin['path'];pin['path']=mapping[str(src)]
    put(f'{OP}/02_속성검수표.json',matrix)
    for name in ['00_실행검수절차.md','01_대상목록.json','04_회귀확인_과거누락.json','validate.py']:
        cp(HERE/name,f'{OP}/{name}')
    for name in ['03_변화구역_대조.json','06_절차검사.json']:
        cp(HERE/name,f'{VE}/{name}')
    for p in HERE.glob('*.py'):cp(p,f'{BK}/실행코드/{p.name}')
    for p in HERE.glob('run_*.json'):cp(p,f'{VE}/추출실행/{p.name}')
    cp(HERE/'groups.json',f'{VE}/추출실행/groups.json')
    write(STAGE/VE/'게시경로_연결.json',mapping)
    new=[{'id':'A3audit-new-UI-state','type':'new_omission','asset':'자료013','window':'약8.2~10.4초','description':'첫 UI의 상단 표 선택행이 아래로, 하단 주황 선택 표시가 윗줄 도면 첫째→둘째→셋째→넷째로 순차 교체. 중간에는 전후 화면이 겹침. 실제 클릭/커서 주행으로 단정하지 않음.','subject_ids':['E-ui1-row','E-ui1-thumb'],'curve':'선택은 상태 교체. 위치 이징 비적용, 화면 혼합 곡선 미분류.','human_status':'not_asked_not_approved_AI_observation'},
      {'id':'A3audit-new-connector','type':'new_omission','asset':'자료013','window':'약13~15.5초','description':'도면 창의 작은 지점 부근과 전경 모델 사이에 회색 반투명 연결면이 펼쳐지고 모델 뒤에 남음. 모델 확대와 14초대 후반 광점은 별도 요소.','subject_ids':['E-connector'],'curve':'확대와 연동해 변화량 감소 성향. 연결면 자체 곡선 미분류.','human_status':'not_asked_not_approved_AI_observation'},
      {'id':'A3audit-refine-body','type':'previous_description_refined','asset':'자료013','window':'약2.8~4초','description':'EG-BIM 문자 수렴→영문 부제→한글 본문 위쪽→아래쪽 순으로 중첩하며 선명해짐. 기존 N4의 본문 선명화를 순서별로 세분화.','subject_ids':['E-subtitle','E-body-upper','E-body-lower'],'human_status':'new_detail_not_covered_by_previous_N4_approval'},
      {'id':'A3audit-refine-dim','type':'previous_description_refined','asset':'자료013','window':'약5~8초','description':'금빛 E가 정착한 뒤 광량이 줄어 어두운 배경 역할로 약화됨. 내부 선무늬의 독립 흐름으로 확정하지 않음.','subject_ids':['E-hero-dim','E-texture'],'human_status':'AI_refinement'},
      {'id':'A3audit-refine-intro','type':'previous_description_refined','asset':'자료013','window':'약0.2~1.2초','description':'도입의 어두운 E 조각 조립을 3.5초 이후 전경 E 조립과 분리. 커서/큰 영문보다 앞선 단계로 기록.','subject_ids':['E-early-upper','E-early-middle','E-early-lower'],'human_status':'AI_refinement'}]
    viewed=[f'{g}_{i}.jpg' for g,n in [('eg_intro',3),('eg_late',3),('eg_model',3),('jh_all',4),('모델_원근형태',3),('문구_역순',3),('E내부_역순',3)] for i in range(1,n+1)]
    viewed+=['배경_수평단면.png','E_세로단면.png','본문_등장순서_1.jpg','연결면_원본크롭_1.jpg','추가발견_모델_연결면.jpg','장헌_역순_전체.jpg','EG도입_역순_전체.jpg','도입_작은요소_역순_1.jpg','추가발견_UI내부_선택변화.jpg']
    viewed += [f'{aid}_구역변화_대조_{i}.jpg' for aid,n in [('자료005',3),('자료013',2)] for i in range(1,n+1)]
    for name in viewed:assert (HERE/'검수판'/name).is_file(),name
    execution={'date':now,'scope':{'자료005':[0,24],'자료013':[0,15.5]},'reviewer':'current Codex, self-review not independent','new_PNGs':174,'native3840_PNGs':38,'1920_PNGs':136,'proxy_frames_reused_for_search':1652,'manually_viewed_boards':[{'path':f'{AN}/검수판/{name}','sha256':sha(HERE/'검수판'/name)} for name in viewed],'not_every_native_frame_viewed':True,'not_actual_realtime_playback':'temporal image sequences/crops, not continuous player review','scope_limits':['audio/AV sync not assessed','unobserved outside current windows not assessed','SAR unknown; raw-raster proportions only','exact AE implementation/curve parameters not recovered'],'analysis_corrections_this_run':['initial schema check rejected improper reuse of old human approval on new N4 details; corrected','draft UI internal-static observation rejected after temporal tile review; native/cropped evidence confirmed selected row/thumbnail changes','tentative model rotation not confirmed; not promoted to a finding'],'source_and_Phase00_unchanged':True}
    put(f'{VE}/05_실행근거와_자체보완.json',execution)
    known=json.loads((ROOT/P/'02_분석작업/01-A2_전체모션재검수/모션재검수_확정과_추가정정.json').read_text(encoding='utf-8'))
    for pin in known['knowledge']:assert sha(ROOT/pin['path'])==pin['sha256']
    put(f'{VE}/기존지식_재확인.json',known['knowledge'])
    current={'id':'A2-motion-audit-current','version':'0.3','state':'A2_subject_property_audit_performed_with_declared_unclassified_properties','scope':execution['scope'],'operational_procedure':f'{OP}/00_실행검수절차.md','subject_registry':f'{OP}/01_대상목록.json','axis_matrix':f'{OP}/02_속성검수표.json','structure_check':f'{VE}/06_절차검사.json','previous_current_observation':f'{P}/02_분석작업/01-A2_전체모션재검수/모션재검수_확정과_추가정정.json','previous_confirmed_receipt':f'{P}/04_검증자료/01-A2_전체모션재검수/사람확인_N1-N8과_빛커서정정_회신.json','prior_six_N1_N8_and_user_C1_C2_preserved':True,'new_observations':new,'JH_new_omissions_found':0,'subjects':49,'axis_cells':441,'not_recognition_accuracy_or_no_omission_guarantee':True,'remaining_unclassified':['thin-light full path and speed curve','background grid boundary identity/curve','individual body-line visibility curve','connector own boundary curve','original AE compositing/keyframe implementation'],'human_questions_pending':[],'new_findings_human_approved':False,'A3_started':False}
    put(f'{AN}/현재관측_통합안내.json',current)
    guide='''# 누락 방지 절차 보완과 현재 구간 재대조

장헌0~24초, EG-BIM0~15.5초를 다시 대조했습니다. 기존①~⑥·N1~N8 확인과 C1/C2 사용자 정정은 보존했습니다. 새 AI 관측에 기존 사람 승인을 붙이지 않았습니다. A3는 시작하지 않았고 추가 회신을 요청하지 않습니다.

## 실제로 추가 발견한 누락

| 구간 | 새로 기록한 동작 | 기존 기록의 문제 |
|---|---|---|
| EG 약8.2~10.4초 | UI 상단 표의 선택행이 내려가고, 하단 주황 선택 표시가 도면 첫째→둘째→셋째→넷째로 바뀝니다. 교체 중 전후 화면이 겹칩니다. | 창 전체 이동만 기록하고 창 안의 상태 교체를 놓쳤습니다. 이번 실행 초안에서도 정지로 쓰려다 구역 변화 대조에 남은 차이를 따라가 발견하고 정정했습니다. |
| EG 약13~15.5초 | 도면 창과 전경 모델 사이에 반투명 연결면이 펼쳐지고 모델 뒤에 남습니다. | 모델 확대와 나중 광점에 묶어 별도 연결면을 누락했습니다. |

![UI 내부 선택행·도면 선택의 순차 교체](검수판/추가발견_UI내부_선택변화.jpg)

![도면과 모델 사이의 반투명 연결면](검수판/추가발견_모델_연결면.jpg)

## 기존 설명을 더 구체화한 부분

- 작은 EG-BIM 문자 수렴 뒤 영문 부제, 한글 본문 위쪽, 아래쪽 순으로 중첩하며 선명해집니다. 기존 “부제/본문이 선명해짐”을 순서별로 나눴습니다.
- 금빛 E는 약5초 전후 밝게 정착한 뒤 약7~8초에 걸쳐 어두운 배경 역할로 약해집니다. E 내부 무늬가 독립적으로 계속 흐른다는 가설은 확정하지 않았습니다.
- 도입의 어두운 E 조각 조립과 3.5초 이후 전경 E 조립을 별도 단계로 나눴습니다.

장헌에서는 이번 대조로 기존 차트·수치·장면 전환 이외의 추가 독립 동작을 발견하지 못했습니다. 모델이 따로 회전한다는 후보도 검토했으나 확대·블러·연결면과 분리한 명확한 근거가 없어 확정하지 않았습니다.

## 바꾼 절차와 적용 결과

1. 화면 구역마다 본체뿐 아니라 작은 글자·커서·테두리·빛·내부 질감·화면 안 화면을 목록화했습니다. 창 전체와 내부 상태는 따로 확인합니다.
2. 장헌22개·EG27개 대상의9개 속성(이동·크기·형태/회전·가시성/공개·색/광량·내부변화·중첩·등퇴장/순서·가감속)을 각각 기록했습니다. 미분류에는 이유를 적었습니다.49개/441칸은 기록 개수이며 정확도 점수가 아닙니다.
3. 순방향 시점 대조 뒤 정착 상태를 역순으로 추적하고, 얇은 선·작은 요소는 원본 해상도와 crop으로 확인했습니다.1652개 저해상도 프레임의40개 시간 구간·공간 구역 변화 지도를 탐색 보조로 재사용했습니다. 이 과정에서 UI 내부 변화를 추가 발견했습니다.
4. 대상/속성/근거가 빠지거나 새 AI 관측에 예전 사람 승인을 붙이면 기록 검사가 실패하도록 했습니다. 커서·연결면·UI 내부 선택 삭제, 가감속 빈칸, 근거 제거, 잘못된 승인 재사용의6개 오류 주입이 모두 검출됐습니다. 이 검사는 영상 인식 정확도 시험이 아닙니다.

원본 해상도38장과1920px136장, 총174개 선택 PNG를 추가 추출했습니다. 같은 시점의 기존 원본 해상도5장은 해시가 일치했습니다. 전체 해상도의 모든 프레임을 눈으로 확인하거나 실제 속도로 연속 재생 검수했다는 뜻은 아닙니다. 현재 Codex의 시간별 화면 대조이며 독립 검토도 아닙니다.

얇은 빛의 전체 경로/가감속, 배경 격자 경계의 동일 대상 추적, 본문 각 줄과 연결면의 정확한 곡선, 실제 AE 합성 구성은 미분류로 남겼습니다. 미분류를 “동작 없음”으로 바꾸거나 전체 무누락을 보증하지 않습니다. 오디오와 현재 구간 밖은 이번 검수 대상이 아닙니다.

[적용한 실행 절차](../../06_도구와계약/01-A2_모션검수절차/00_실행검수절차.md) · [대상 목록](../../06_도구와계약/01-A2_모션검수절차/01_대상목록.json) · [속성별 검수표](../../06_도구와계약/01-A2_모션검수절차/02_속성검수표.json) · [현재 관측 통합안내](현재관측_통합안내.json)
'''
    put(GUIDE,guide)
    report='# 01-A2 검수 절차 보완과 재대조 보고\n\n'+guide.split('\n',1)[1]
    report=report.replace('(검수판/','(../02_분석작업/01-A2_누락방지_재검수/검수판/').replace('(../../06_도구와계약/','(../06_도구와계약/').replace('(현재관측_통합안내.json)','(../02_분석작업/01-A2_누락방지_재검수/현재관측_통합안내.json)')
    put(REPORT,report)
    notice={'date':now,'state':current['state'],'report':REPORT,'guide':GUIDE,'procedure':f'{OP}/00_실행검수절차.md','current_observation':f'{AN}/현재관측_통합안내.json','subject_count':49,'axis_count':9,'new_omission_groups':2,'new_description_refinements':3,'prior_human_confirmations_preserved':True,'pending_human_questions':0,'A3_started':False,'Phase00_changed':False,'readiness_scope':'A2 procedure and bounded current-window audit performed; no exhaustive no-omission or A3 authorization claim'}
    put(NOTICE,notice)
    planrel=f'{P}/00_진행안내/01-A_계획상태.json';plan=read(planrel)
    plan.update(version='0.8',state=current['state'],stage_A2_status='대상별9속성 검수 절차를 적용해 재대조. UI 내부 선택 변화·반투명 연결면 누락 추가 기록. 기존 사람 확인 유지, 새 관측은 AI만. 미분류 속성 명시.',stage_A2_report=REPORT.removeprefix(P+'/'),stage_A2_current_notice=NOTICE.removeprefix(P+'/'),stage_A2_current_observation=f'{AN}/현재관측_통합안내.json',current_thread_media_work_stopped=False,A3_started=False,human_content_reviews_pending=0,next_decision='현재 절차/검수표와 새 누락 보완 적용. A3 미착수; 미분류를 무동작으로 처리하지 않음',active_A2_motion_review_procedure=f'{OP}/00_실행검수절차.md',motion_review_record_validator=f'{OP}/validate.py',motion_review_gate_scope='record completeness and pins only, not automatic motion-recognition accuracy',stage_A2_new_AI_observation_groups=2)
    unique=set();selected=0
    for folder in ['phase01a-a2','phase01a-a2-fullmotion','phase01a-a2-correction2','phase01a-a2-audit3']:
        for log in (HERE.parent/folder/'cases').rglob('실행기록.json'):
            if 'retest' in log.parent.name:continue
            rr=json.loads(log.read_text(encoding='utf-8'));selected+=len(rr.get('frames',[]))
            for f in rr.get('frames',[]):unique.add((rr['id'],F(f['actual_playback_seconds'])))
    plan.update(stage_A2_images=selected,stage_A2_unique_times=len(unique),stage_A2_primary_extraction_jobs=17,stage_A2_images_counting_basis='successful primary selected PNGs including same-time repeats/native supplements; visual boards and retests excluded')
    put(planrel,plan)
    oldnotice=f'{P}/00_진행안내/16_01-A2_현재구간_모션재검수_현재안내.json';old=read(oldnotice);old['superseded_by']=NOTICE;put(oldnotice,old)
    for rel in [f'{P}/04_검증자료/01-A2_작은예비/사람검수_대기.json',f'{IMP}/내용검수/사람검수_대기.json']:
        q=read(rel);q['current_observation']=f'{AN}/현재관측_통합안내.json';q['AI_new_unapproved_findings']=[n['id'] for n in new];q['pending_new_human_questions']=[];q['no_auto_approval']=True;put(rel,q)
    put(f'{IMP}/보완과_재시험/누락방지_재검수_요약.md',f'# 검수 절차 보완과 재대조\n\n[현재 결과·비교 화면](<{(ROOT/GUIDE).as_posix()}>)\n\n기존①~⑥·N1~N8 확인과 C1/C2 정정 유지. 새 누락2묶음과 기존 설명 세분화3묶음은 AI 관측이며 사람 승인이 아닙니다. 추가 사람 질문 없음. A3 미착수.\n')
    put(f'{IMP}/보완과_재시험/누락방지_기록검사.json',json.loads((HERE/'06_절차검사.json').read_text(encoding='utf-8')))
    # Save before/after integrity and a precise scope list for publication.
    write(HERE/'게시명세.json',{'created_at':now,'expected_before':before,'files':[{'path':p.relative_to(STAGE).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in STAGE.rglob('*') if p.is_file()]})
    print(json.dumps({'files':len(list(STAGE.rglob('*'))),'selected_PNGs_total':selected,'unique_selected_times':len(unique),'objects':49,'human_questions':0},ensure_ascii=False))
def publish():
    m=json.loads((HERE/'게시명세.json').read_text(encoding='utf-8'));before=m['expected_before'];links=0
    allowed=[AN+'/',VE+'/',OP+'/',BK+'/',IMP+'/']
    named={REPORT,NOTICE,f'{P}/00_진행안내/01-A_계획상태.json',f'{P}/00_진행안내/16_01-A2_현재구간_모션재검수_현재안내.json',f'{P}/04_검증자료/01-A2_작은예비/사람검수_대기.json'}
    for item in m['files']:
        rel=item['path'];src=STAGE/rel;dst=(ROOT/rel).resolve();assert dst.is_relative_to(ROOT.resolve()) and (rel in named or any(rel.startswith(p) for p in allowed)),rel
        assert sha(src)==item['sha256'];assert not dst.exists() or sha(dst)==item['sha256'] or sha(dst)==before.get(rel),rel
        if src.suffix=='.json':json.loads(src.read_text(encoding='utf-8-sig'))
        if src.suffix=='.md' and not rel.startswith(BK+'/'):
            for ref in re.findall(r'\]\(([^)]+)\)',src.read_text(encoding='utf-8')):
                ref=ref.strip('<>')
                if ref.startswith(('http:','https:')):continue
                if re.match('^[A-Za-z]:',ref):target=Path(ref).resolve().relative_to(ROOT.resolve())
                else:target=(ROOT/Path(rel).parent/ref).resolve().relative_to(ROOT.resolve())
                assert (STAGE/target).is_file() or (ROOT/target).is_file(),('broken_link',rel,ref)
                links+=1
    if '--publish' not in sys.argv:print(json.dumps({'prepublication_passed':True,'files':len(m['files']),'links':links}));return
    for item in m['files']:
        dst=ROOT/item['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(STAGE/item['path'],dst);assert sha(dst)==item['sha256']
    receipt={'files':len(m['files']),'all_hashes_match':True,'human_approvals_extended':False,'human_questions_pending':0,'A3_started':False,'Phase00_changed':False}
    write(HERE/'게시후_검증.json',receipt);write(ROOT/VE/'게시후_검증.json',receipt);print(json.dumps(receipt,ensure_ascii=False))
if __name__=='__main__':
    if '--check' in sys.argv or '--publish' in sys.argv:publish()
    else:build()
