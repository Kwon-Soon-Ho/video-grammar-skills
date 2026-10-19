from pathlib import Path
from fractions import Fraction as F
import json,hashlib,shutil,sys,importlib.util
HERE=Path(__file__).resolve().parent;BASE=HERE.parent/'phase01a-a2'
sys.path.insert(0,str(BASE));from prepare import ROOT,sha,write
STAGE=HERE/'게시안';P='Phase 01-A';AN=f'{P}/02_분석작업/01-A2_전체모션재검수';VE=f'{P}/04_검증자료/01-A2_전체모션재검수';BK=f'{P}/backup/2026-10-16_01-A2_전체모션재검수';IMP='작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A2'
REPORT=f'{P}/05_결과보고/08_01-A2_현재구간_모션재검수_보고.md'
def read(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8-sig'))
def local(rel):return json.loads((HERE/rel).read_text(encoding='utf-8'))
def put(rel,x):write(STAGE/rel,x)
def textfile(rel,s):
    p=STAGE/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def copy(src,rel):
    p=STAGE/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,p)
def q(x):
    x=F(x);return {'num':x.numerator,'den':x.denominator}
def run(aid,phase):return local(f'cases/{aid}/{phase}/실행기록.json')
def main():
    clip_records=local('추가검수_화면/검수영상_파생기록.json');clips={r['id']:r for r in clip_records}
    groups=[
      {'id':'N1','asset':'자료005','window':'약6.0~6.4초·21.0~21.4초','description':'이전 화면과 다음 화면이 겹쳐 교체되는 전환. 슬라이드가 아니라 크로스페이드이며 초반 전환량이 크고 끝에서 완만해짐.','plain_check':'두 장면이 겹쳐 바뀌며, 처음 빠르게 전환된 뒤 끝에서 부드럽게 마무리되는지.','property':'혼합 영상 진행량(왼쪽 제목 ROI)','direction':'가시성 교체; 이동 방향 비적용','curve':'ease-out 감속형','taxonomy':['CURVE-DECEL'],'evidence_files':['장헌_정지와_전환곡선.json'],'clips':['N1','N3'],'confidence':'관측 곡선군에 대한 강한 후보'},
      {'id':'N2','asset':'자료005','window':'약8~9.3초 / 15.5~16.7초 / 16.8~17.8초','description':'수주→매출→영업이익 순으로 실적 막대가 아래에서 위로 자라고, 원형 진행표시는12시 방향에서 시계방향으로 채워짐. 수치도 증가하고 증가량은 끝에서 작아짐.','plain_check':'숫자 값 자체가 아니라, 막대가 위로 자라고 원이 시계방향으로 채워지며 끝에서 느려지는지.','property':'동일 원형 ROI의 파란 채움 픽셀량과 막대/숫자의 시점 대조','direction':'막대 위쪽 / 원형 시계방향','curve':'세 지표 모두 ease-out 감속형','taxonomy':['CURVE-DECEL'],'evidence_files':['장헌_차트_시간곡선진단.json'],'clips':['N2','N2S','N2P'],'confidence':'원형 진행량에 대한 강한 후보; 개별 숫자 타이밍은 반올림 영향'},
      {'id':'N3','asset':'자료005','window':'약21.3~22.6초','description':'매출처 도넛의 색 영역이 시계방향으로 늘고 가족사 비중 숫자가 함께 올라간 뒤 완만하게 정착. 오른쪽 사업분야 원은24초까지 회색 상태.','plain_check':'왼쪽 도넛과 가족사 비중이 빠르게 채워지다가 천천히 마무리되는지.','property':'고정 도넛 ROI의 빨강/분홍 채움 면적','direction':'도넛 시계방향','curve':'ease-out 감속형','taxonomy':['CURVE-DECEL'],'evidence_files':['장헌_차트_시간곡선진단.json'],'clips':['N3'],'confidence':'채움 진행량에 대한 강한 후보'},
      {'id':'N4','asset':'자료013','window':'약1.9~3.8초','description':'Value of는 글자 전체가 옆으로 날아오는 것보다 공개 영역이 오른쪽/아래로 확장되며 보임. 밝은 글자는 이후 왼쪽부터 오른쪽으로 지워져 옅은 배경 문구가 남고, 작은 EG-BIM 글자들이 간격을 좁히며 맞춰지고 부제/본문이 선명해짐.','plain_check':'큰 문구가 좌→우로 드러났다 같은 방향으로 지워지고, EG-BIM 글자들이 모여 정착하는지.','property':'공개된 흰 영역의 오른쪽 경계 / 밝은 영역 소실량 / 작은 제목 좌우 끝','direction':'공개/소실 경계 좌→우; 글자 간격 수렴','curve':'공개 ease-in-out / 소실 ease-in / 자간 수렴 ease-out 성향','taxonomy':['CURVE-INOUT','CURVE-ACCEL','CURVE-DECEL'],'evidence_files':['EG_이동과_공개_곡선진단.json','EG_작은제목_문자간격진단.json','곡선분류_자체진단과_민감도.json'],'clips':['N4'],'confidence':'공개·소실은 곡선 후보, 자간 수렴은 짧은 범위/가시성 중첩 한계'},
      {'id':'N5','asset':'자료013','window':'약6.9~8.0초','description':'첫 UI 이미지가 오른쪽으로 이동하면서 선명해지고 정착함. 초기 희미한 테두리 일부를 놓치면 폭 증가나 반대 방향 이동으로 오인할 수 있어 오른쪽 경계를 따로 추적함.','plain_check':'첫 UI 이미지가 오른쪽으로 움직이며 나타나고, 끝에서 느려지는지.','property':'동일 UI 오른쪽 노란 세로 테두리의 x 위치','direction':'오른쪽','curve':'ease-out 감속형','taxonomy':['CURVE-DECEL'],'evidence_files':['EG_이동과_공개_곡선진단.json','EG_사진테두리_1920진단.json'],'clips':['N5'],'confidence':'추적 경계의 감속 강한 후보; 가시성은 별도 관찰'},
      {'id':'N6','asset':'자료013','window':'약10.7~12.2초','description':'먼저 있던 UI 창이 오른쪽 아래로 이동하며 작아져 뒤쪽 자리를 만들고, 다음 도면 창이 그 앞에 오른쪽으로 이동하면서 선명해져 겹침. 두 사건은 일부 중첩되지만 같은 동작이나 같은 속도곡선이 아님.','plain_check':'앞 창이 우하단으로 작아져 물러나고, 새 도면 창이 그 앞에 오른쪽으로 들어와 정착하는지.','property':'기존 창 왼쪽/위쪽 경계와 크기 / 새 앞 창 오른쪽 경계','direction':'기존창 우하단+축소 / 새창 오른쪽','curve':'기존창 재배치 ease-in-out / 새창 진입 ease-out','taxonomy':['CURVE-INOUT','CURVE-DECEL'],'evidence_files':['EG_이동과_공개_곡선진단.json','EG_전면창_재배치진단.json','곡선분류_자체진단과_민감도.json'],'clips':['N6'],'confidence':'곽선군 후보; 처음 가시성이 낮은 새 창의 시작 시각은 근사'},
      {'id':'N7','asset':'자료013','window':'약13.0~14.6초','description':'작은 모델 이미지가 오른쪽 아래로 이동하고 커지며 화면 앞쪽으로 펼쳐져 보임. 확대 변화량은 끝에서 작아짐. 그 뒤 배경의 두 창도 오른쪽 아래로 다시 재배치되어 겹침 간격이 달라짐. 원본 카메라/3D 키프레임 구현은 판정하지 않음.','plain_check':'모델이 우하단으로 커져 나오다가 느려지고, 뒤의 창들도 다시 우하단으로 재배치되는지.','property':'연결된 밝은 모델 면의 면적 제곱근/중심 / 앞 창 왼쪽 경계','direction':'모델 우하단+확대 / 뒤창 우하단 재배치','curve':'모델 확대 ease-out / 창 재배치 ease-in-out 성향','taxonomy':['CURVE-DECEL','CURVE-INOUT'],'evidence_files':['EG_모델면_연결성보완진단.json','EG_전면창_재배치진단.json','곡선분류_자체진단과_민감도.json'],'clips':['N7'],'confidence':'모델 면과 창 경계에 대한 후보; 면적은 전체 모델의 원본 Scale 아님'},
      {'id':'N8','asset':'자료013','window':'약14.3~15.0초','description':'모델 왼쪽 위 부근의 광점과 오른쪽으로 퍼지는 빛띠가 강해짐. 위치 이동 속도가 아니라 고정 영역의 밝기 진행량이 처음/끝에서 완만하고 중간에서 빠른 S형임.','plain_check':'광점과 빛띠가 서서히 시작해 중간에 빠르게 밝아진 뒤 완만해지는지.','property':'모델 상부 고정 ROI의 평균 밝기','direction':'빛띠가 오른쪽으로 퍼져 보임; 밝기 곡선과 이동속도 구분','curve':'밝기 진행량 ease-in-out 성향','taxonomy':['CURVE-INOUT'],'evidence_files':['EG_이동과_공개_곡선진단.json'],'clips':['N8'],'confidence':'참고 후보: 모델 이동·배경 밝기 중첩으로 실제 opacity 곡선은 확정하지 않음'}]
    knowledge_paths=['Phase 00/01_공통용어/공통용어사전.json','Phase 00/01_공통용어/03_용어별적용예와반례.md','Phase 00/01_공통용어/04_복합화면과미분류처리.md','Phase 00/02_원칙과레이아웃/03_모션원칙_적용예와반례.md']
    knowledge=[{'path':p,'sha256':sha(ROOT/p)} for p in knowledge_paths]
    put(f'{VE}/기존지식_연결과_누락원인.json',{'knowledge_pins':knowledge,'existing_ids':['AP-06','MP-02','CURVE-LINEAR','CURVE-ACCEL','CURVE-DECEL','CURVE-INOUT'],'already_prepared':True,'failure_reason':['did not turn knowledge into a per-object per-property inspection checklist','used sparse appearance/state samples to close the analysis too early','did not track same objects or compare equal-time changes','after the first E correction, rechecked only that object instead of auditing other motions'],'not_the_reason':['absence of AE keyframe values','missing Phase00 easing vocabulary'],'corrective_workflow':['inventory each target/property','separate direction from order and speed magnitude','measure same quantity across source-timed samples','compare candidate curves and identity/visibility confounds','leave explicit unsupported/unknown fields instead of silently skipping them'],'new_A3_skill_created':False})
    # Compare each successful primary/retest using exact time and image/proxy pins.
    comparisons=[];runs=[]
    for aid,phase in [('자료005','scan'),('자료013','scan'),('자료005','jh_detail'),('자료013','eg_title'),('자료013','eg_screens'),('자료013','eg_model')]:
        a,b=run(aid,phase),run(aid,phase+'_retest');runs.append((aid,phase,a))
        c={'asset':aid,'phase':phase,'images':len(a['frames']),'count_equal':len(a['frames'])==len(b['frames']),'image_hashes_equal':all(x['sha256']==y['sha256'] for x,y in zip(a['frames'],b['frames'])),'times_ordinals_equal':all(all(x[k]==y[k] for k in ['actual_playback_seconds','reported_pts','container_cts_ticks','display_ordinal_zero_based']) for x,y in zip(a['frames'],b['frames'])),'input_hash_equal':a['input_sha256_after']==b['input_sha256_after']}
        if 'tracking_proxy' in a:c['all_frame_proxy_RGB_hash_equal']=a['tracking_proxy']['decoded_RGB_sha256']==b['tracking_proxy']['decoded_RGB_sha256']
        assert all(v for k,v in c.items() if k.endswith('equal'))
        comparisons.append(c)
    put(f'{VE}/동일조건_재시험.json',comparisons)
    # Native extraction metadata remains immutable, with C execution paths mapped to D archives.
    archived=[]
    for aid,phase,r in runs:
        for variant in [phase,phase+'_retest']:
            for src in (HERE/'cases'/aid/variant).iterdir():
                rel=f'{AN}/{aid}/{variant}/{src.name}' if not variant.endswith('_retest') else f'{BK}/재시험/{aid}/{variant}/{src.name}'
                copy(src,rel);archived.append({'execution_path':str(src),'archive_path':str(ROOT/rel),'sha256':sha(src)})
    put(f'{VE}/실행과_보존위치_색인.json',archived)
    for src in (HERE/'추가검수_화면').iterdir():copy(src,f'{AN}/추가검수_화면/{src.name}')
    for src in HERE.glob('*.json'):
        if src.name not in {'게시명세.json','게시후_검증.json'}:copy(src,f'{VE}/진단원문/{src.name}')
    for src in HERE.glob('*.jpg'):copy(src,f'{VE}/검토용_연락시트/{src.name}')
    copy(HERE/'장헌_0초6초_차이.png',f'{VE}/검토용_연락시트/장헌_0초6초_차이.png')
    for src in HERE.glob('*.py'):copy(src,f'{BK}/실행코드/{src.name}')
    for src in (HERE/'backup').rglob('*'):
        if src.is_file():copy(src,f'{BK}/중간본과_실패/{src.relative_to(HERE/"backup").as_posix()}')
    for src in HERE.glob('*stdout.txt'):copy(src,f'{BK}/실행로그/{src.name}')
    # Existing R4-1 schema/validator only. New snapshots, not a falsely integrated spatial record.
    time_checks=[]
    tool=ROOT/'Phase 00/07_실행도구/시간프레임_규격검사.py';spec=importlib.util.spec_from_file_location('r4_fullmotion',tool);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    for aid in ['자료005','자료013']:
        record=read(f'{P}/02_분석작업/01-A2_작은예비/{aid}/R4-1_시간연결_초안.json');record['frames']=[]
        for asset,phase,r in runs:
            if asset!=aid:continue
            for f in r['frames']:
                record['frames'].append({'id':f['frame_id'],'timeline_ref':aid+'-T','period_ref':aid+'-SAMPLED','role':'within_period','source_pts':f['container_cts_ticks'],'pts_kind':'original_pts','time_base':q(F(f['time_base'])),'source_frame_ordinal':f['display_ordinal_zero_based'],'requested':q(F(f['requested_playback_seconds'])),'actual':q(F(f['actual_playback_seconds'])),'mapping_state':'mapped','selection_policy':'at_or_after','limitations':'snapshot in full-motion recheck. CTS is reconstructed from original MP4 sample tables with verified single edit offset; source-native identity/time index also checked on every decoded proxy frame. Content interpretation is separate.'})
        record['notes']='A2 full-motion snapshot subrecord. Not merged with previous records as duplicate timelines. Uncertainty unknown. 480px all-frame proxy is separately indexed; this record contains PNG snapshots only.'
        put(f'{AN}/{aid}/R4-1_재검수_시간연결.json',record);result=m.validate(record);assert result['valid'];time_checks.append({'asset':aid,'frames':len(record['frames']),'result':result,'validator_sha256':sha(tool)})
    put(f'{VE}/R4-1_추가시간_검사.json',time_checks)
    inventory=groups+[
      {'id':'S-JH-intro','window':'0~6초','status':'정지 대조','observation':'181개 저해상도 프레임에서 기준 대비 최대 평균 절대차0.00844/255, 단일 채널 최대4. 의도된 pan/zoom 근거 없음. 중간 commentary의 배경 이동 추정을 철회.','curve':'비적용','evidence_files':['장헌_정지와_전환곡선.json']},
      {'id':'S-JH-fixed-layout','window':'6.4~21초','status':'배치 유지/값 변화 분리','observation':'카드와 제목의 자리는 유지되고 실적 막대·원형·숫자만 변화. 카드가 차례로 들어온 것으로 기록하지 않음.','curve':'카드 위치에는 비적용; 데이터 동작 N2 참조'},
      {'id':'S-JH-right-donut','window':'21.4~24초','status':'범위 한정 미진행','observation':'오른쪽 사업분야 도넛의 회색 상태가 유지됨. 이 범위 밖에서 채워지는지 단정하지 않음.','curve':'관찰 범위에서 채움 곡선 미발생'},
      {'id':'S-EG-E-pieces','window':'약3.5~5.5초','status':'기존 사용자 정정·보완 유지','observation':'조각별 좌→우 슬라이드와 감속은 이전 회신/31장 보완 근거를 유지. 이번 추가 사람 검수에서 재질문하지 않음.','curve':'기존 ease-out 관측 유지'},
      {'id':'S-EG-ambient','window':'0~1.8초 및 배경 유지 구간','status':'보조 변화 관찰, 속도곡선 미분류','observation':'저대비 사각 패널·격자·수평 광선의 가시성이 달라짐. 도입부의 일부 가장자리가 이동하지만 안정적으로 동일 대상을 분리하지 못해 방향/가감속을 확정하지 않음. 정지로 처리하지도 않음.','curve':'미분류; 대상 정체성/낮은 대비/중첩 한계'},
      {'id':'S-EG-camera','window':'전체 검토 구간','status':'구현 가설 분리','observation':'창·모델의 화면상 위치와 크기 변화를 기록. 실제 카메라 이동/그룹 transform/3D 회전으로 확정하지 않음.','curve':'원본 구현 미확인'}]
    for g in groups:
        g['human_review']='pending_new_motion_scope_only';g['evidence_pins']=[{'path':f'{VE}/진단원문/{n}','sha256':sha(HERE/n)} for n in g['evidence_files']];g['clip_pins']=[{'id':key,'path':f'{AN}/추가검수_화면/{Path(clips[key]["path"]).name}','sha256':clips[key]['sha256']} for key in g['clips']]
    put(f'{AN}/모션재검수_관측초안.json',{'id':'A2-fullmotion-review','version':'0.1','status':'AI_motion_recheck_complete_pending_new_human_items','scope':{'자료005':'0~24초','자료013':'0~15.5초'},'source_reading':'every decoded displayed frame in scope processed as480px RGB proxy,1652 total; selected native1920PNG frames visually inspected; not every full-resolution frame read','knowledge':knowledge,'inventory':inventory,'human_new_groups':[g['id'] for g in groups],'earlier_human_confirmations':'preserved under01-A2_작은예비; not broadened to these new motion details','exact_original_AE_values_needed_for_curve_family':False,'exact_original_AE_values_recovered':False,'independent_review':False,'separate_API_calls':0,'A3_started':False,'spatial_record_status':'diagnostic proxy coordinates only, no validated integrated R4 spatial record'})
    def cliplink(key):return f'[{key} 재생](추가검수_화면/{Path(clips[key]["path"]).name})'
    guide='''# 추가로 확인할 모션 8묶음

이전①~⑥의 확인과 E조각 정정은 유지합니다. 아래는 새로 보완한 동작만 확인하는 목록입니다. 숫자 판독은 다시 묻지 않습니다. 검수용 영상은 원래 프레임 간격과 재생 속도를 유지했고, 위에 원본 시각을 표시했습니다. 저해상도 미리보기이며 음성은 넣지 않았습니다.

| 번호 | 재생 | 추가로 확인할 것 | 영상에서 판단한 이징 |
|---|---|---|---|
'''
    for g in groups:guide+=f"| {g['id']} | {' · '.join(cliplink(k) for k in g['clips'])} | {g['plain_check']} | {g['curve']} |\n"
    guide+='''
ease-in은 변화가 점점 빨라지는 가속형, ease-out은 점점 느려지는 감속형, ease-in-out은 가속한 뒤 감속하는 형태입니다. 위치뿐 아니라 공개 경계·채움·밝기 중 무엇이 변하는지 구분했습니다. 이름은 관측 곡선의 분류이며 실제 AE 프리셋이나 핸들 값을 뜻하지 않습니다.

답변 예: `N1 맞음 / N2 맞음 / N3 수정: … / N4 일부만 확인: … / N5 보류`. 직접 확인한 항목만 답하면 됩니다. 이번 항목은 아직 사람 확인 전입니다.

## 시간별 표본

'''
    for g in groups:
        guide+=f"\n**{g['id']} · {g['window']}**\n\n{g['description']}\n\n"
        for key in g['clips']:guide+=f'![{key} 첫·중간·끝 표본](추가검수_화면/{Path(clips[key]["path"]).stem}_표본.jpg)\n\n'
    textfile(f'{AN}/00_추가로_확인할_모션.md',guide)
    # Current pending list contains only new motion review, with prior approvals retained.
    oldq=f'{P}/04_검증자료/01-A2_작은예비/사람검수_대기.json';oldimp=f'{IMP}/내용검수/사람검수_대기.json'
    changed=[f'{P}/00_진행안내/01-A_계획상태.json',oldq,oldimp]
    before={rel:sha(ROOT/rel) for rel in changed}
    for rel in changed:copy(ROOT/rel,f'{BK}/변경전/{rel}')
    queue=read(oldq);queue.update(status='previous_six_confirmed_new_eight_motion_groups_pending',pending_claims=[g['id'] for g in groups],pending_scope='new per-property direction/order/curve detail only',current_motion_request=f'{VE}/추가모션_8항목_검수요청.json',prior_current_receipt=queue.get('current_receipt'),no_auto_approval=True)
    put(oldq,queue);put(oldimp,queue)
    request={'id':'A2-HUMAN-NEW-MOTION-8','version':'0.1','status':'pending','groups':groups,'original_reply_requested':'그럼 A3로 넘어가기 전에 장헌과 EG-BIM의 현재 분석 구간에서 다른 동작도 이동 방향·등장 순서·가감속까지 다시 검수해줘. 이번처럼 놓친 부분을 정리하고, 내가 추가로 확인할 항목만 보여줘. 그리고 ae 키프레임 값은 내가 제공 못해. 니가 동영상 검수 스킬을 사용해서 이지 인인지 아웃인지 등을 파악해. 그리고 이전 00단계에서 준비하던 지식 중에 이런 모션 들을 정리하지않았어? 왜 파악 못한거야','guide_path':f'{AN}/00_추가로_확인할_모션.md','guide_sha256':sha(STAGE/AN/'00_추가로_확인할_모션.md'),'observation_sha256':sha(STAGE/AN/'모션재검수_관측초안.json'),'scope':'new movement/order/curve descriptions only; no request for AE source values; excludes exact reconstruction/business facts/audio/generalization','does_not_reask':['previous numeric transcription','previous E correction'],'receipt':None}
    request['context_sha256']=hashlib.sha256(json.dumps(request,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest();put(f'{VE}/추가모션_8항목_검수요청.json',request);put(f'{IMP}/내용검수/추가모션_8항목_검수요청.json',request)
    review='''# 모션 재검수 — 자체검수·레드팀·보완

동일 작성자의 자체 검토이며 독립 검토가 아닙니다. 기준은 Phase00 AP-06/MP-02와 CURVE 계열 및 사건/가시성/위치 구분입니다. 스킬은 animation-principles와 pixel의 관측/측정 구분을 사용했습니다. pixel의 정적 웹/UI 기본값·고정 격자·강제 이징은 영상 정답으로 사용하지 않았습니다.

## 실제로 드러난 누락과 오판

- 지식은 있었지만 대상/관측량/방향/사건순서/변화율 표로 옮기지 않아 분석 단계에서 적용을 빠뜨렸습니다. AE값이 없어서 이징을 분류하지 못한 것이 아닙니다.
- 최초엔 화면 상태와 숫자 중간값만 기록했고, E보완 뒤에도 다른 동작에 대한 감사를 하지 않았습니다. 이번에는 전 구간을 대상으로 관측량을 나누고 실패/미분류도 명시했습니다.
- 재검수 중 장헌 도입부 배경을 이동으로 해석한 commentary는 잘못된 중간 추정이었습니다.181개 프레임의 차이가 압축 오차 수준임을 확인하고 정지로 정정했습니다. 이 오탐을 최종 검수 항목으로 만들지 않았습니다.
- 처음 노란색 분할은 금색 E까지 섞였고 여러 창을 한 bbox로 합쳤습니다. 해당 파일은 진단 이력으로 보존하되 개별 객체 속도 근거에서 제외했습니다. 같은 창의 세로 경계/앞뒤 창의 분리 가능한 부분으로 다시 추적했습니다.
- 모델 중성색 면적의 첫 진단은 고정 제목 픽셀이 섞였습니다. 제목과 기존 도면 영역을 제외하고 연결된 밝은 면으로 보완했습니다. 전체 모델의 정확한 Scale로 발표하지 않습니다.
- 같은 외곽이 커져 보인다는 이유로 확대를 단정하지 않았습니다. 첫 UI 진입은 오른쪽 경계 이동과 가시성 증가로 기록했습니다. 기존 UI의10.7~11.3초 축소는 분리 가능한 왼쪽/위쪽 경계로 확인했습니다.

## 실행 실패와 보완

첫 전체 스캔은 EG에서45초 제한으로 중지됐습니다. 다음 버전은 모든 RGB 프레임을 두 번 보관해 배열 합치기에서1.5GiB 메모리 제한에 걸렸습니다. 제한을 늘리지 않고 swscale에서 직접480px로 줄인 뒤 한 번만 할당하는 방식으로 바꿨습니다. 실패/성공 중간본과 로그를 보존했습니다. 최종 장헌721·EG931프레임 proxy와175개 PNG 선택이 끝났고, 같은 조건 재시험에서 proxy RGB와 PNG/시각/순번이 일치합니다.

곡선 비교기는 등속/가속/감속/가속후감속의 알려진 수식과 상수 신호로 기술 진단했습니다. 제목 공개·첫 UI·모델의 시각 범위를1프레임씩 바꿔 분류군 민감도를 봤습니다. 이는 실영상 성능 점수나 원본 이징 프리셋 복원 검증이 아닙니다. 모델 면적의 첫 전역 진단 대신 연결성 보완 결과를 현재 근거로 사용합니다.

## 남긴 한계

이징은 특정 관측량의 곡선군입니다. 밝기 곡선과 위치 속도, 사건 순서와 가감속을 혼용하지 않습니다. 폰트/색/원본 키프레임/핸들/정확한 곡선 식을 알아냈다고 쓰지 않습니다. proxy 좌표의 실제 오차는 미확인입니다. 저대비 배경 패널/광선 중 같은 대상을 분리하지 못한 속도곡선은 미분류로 남겼습니다. 모델·빛·가시성이 겹친 구간의 수치도 참고 후보입니다.

기존 사람 확인①~⑥은 그 범위에서 유지합니다. 새N1~N8은 확인 전이며 기존 승인으로 통과시키지 않았습니다. 음성·전체 영상·사업 사실·회사 문법·R4 통합 공간 레코드는 이번 검사 대상이 아닙니다. 원본·Phase00·기존 관리 스킬·AE/CU 연결과 A3는 변경하지 않았습니다.
'''
    textfile(f'{VE}/자체검수_레드팀_보완.md',review);textfile(f'{IMP}/보완과_재시험/전체모션_자체검수_레드팀_보완.md',review)
    allkeys=set();snapshot_total=0
    for aid,phase,r in runs:
        snapshot_total+=len(r['frames']);allkeys.update((aid,F(f['actual_playback_seconds'])) for f in r['frames'])
    for aid in ['자료005','자료013']:
        for phase in ['initial','detail']+(['motion_review'] if aid=='자료013' else []):
            r=json.loads((BASE/'cases'/aid/phase/'실행기록.json').read_text(encoding='utf-8'));snapshot_total+=len(r['frames']);allkeys.update((aid,F(f['actual_playback_seconds'])) for f in r['frames'])
    assert snapshot_total==272
    status=read(f'{P}/00_진행안내/01-A_계획상태.json');status.update(version='0.6',state='A2_full_current_scope_motion_recheck_pending_new_human_groups',human_content_reviews_pending=8,human_content_reviews_pending_unit='new motion groups N1–N8 only; previous six approvals retained',stage_A2_status='현재 분석 구간 전 프레임 proxy/세부 PNG로 모션 재검수와 보완 재시험 완료. 새N1~N8 사람 확인 대기',stage_A2_report=REPORT.removeprefix(P+'/'),stage_A2_current_notice='00_진행안내/16_01-A2_현재구간_모션재검수_현재안내.json',human_content_review_record=f'{VE}/추가모션_8항목_검수요청.json',stage_A2_images=snapshot_total,stage_A2_unique_times=len(allkeys),stage_A2_motion_proxy_frames=1652,stage_A2_primary_extraction_jobs=11,stage_A2_retest_extraction_jobs=11,A3_started=False,next_decision='새모션N1~N8의 사람 확인. A3 착수 승인으로 확대하지 않음')
    put(f'{P}/00_진행안내/01-A_계획상태.json',status)
    put(f'{P}/00_진행안내/16_01-A2_현재구간_모션재검수_현재안내.json',{'date':'2026-10-16','state':status['state'],'report':REPORT,'guide':f'{AN}/00_추가로_확인할_모션.md','earlier_six_groups':'confirmed unchanged','new_human_groups_pending':8,'coverage':{'JH':'0~24초','EG':'0~15.5초','processed_lowres_frames':1652,'selected_PNGs_this_recheck':175,'new_review_clips':10},'original_AE_values_requested':False,'curve_family_from_video':True,'exact_AE_values_recovered':False,'A3_started':False,'Phase00_changed':False,'separate_API_calls':0})
    report=f'''# 01-A2 현재 구간 모션 재검수 결과

2026-10-16 · AI 재검수·자체 레드팀·보완·영향 범위 재시험 완료. **새N1~N8은 사람 확인 대기이며 기존①~⑥은 유지합니다. A3는 시작하지 않았습니다.**

장헌0~24초, EG-BIM0~15.5초의 모든 디코드 프레임을480px 관측 배열로 처리했습니다(장헌721, EG931). 전체 해상도 프레임을 전부 눈으로 읽었다는 뜻은 아닙니다.175개1920px PNG를 선택해 연락시트와 핵심 개별 PNG로 방향·공개·등장 순서·가감속을 대조했습니다. 기존 누적까지 PNG는{snapshot_total}장, 고유 선택 시점은{len(allkeys)}개입니다. 같은 원본의 반복 추출을 독립 표본으로 세지 않았습니다.

## 왜 이전에 파악하지 못했는가

Phase00에는 AP-06 가속/감속, MP-02 이징과 CURVE-ACCEL/DECEL/INOUT/LINEAR가 이미 있었습니다. 제가 이를 대상별 실행 체크리스트로 적용하지 않고, 성긴 정지 표본을 상태 설명으로만 정리했습니다. E의 첫 정정 뒤에도 같은 구간의 다른 동작을 다시 감사하지 않은 것이 추가 누락입니다. **지식이나 AE 키프레임 입력이 없어서 생긴 실패가 아니라 분석 절차와 적용의 실패입니다.**

이번에는 대상·관측량·방향·순차/중첩·곡선·근거·불확실성을 분리했습니다. 원본 AE값 없이 영상의 위치/공개 경계/채움/밝기 시계열로 곡선군을 판단했습니다. 실제 AE 프리셋·베지어 핸들·정확한 지수는 복원했다고 쓰지 않습니다.

## 새로 보완한 내용

| 그룹 | 추가 관측 | 곡선군 판단 |
|---|---|---|
|N1|장헌 두 화면 교체는 슬라이드가 아닌 크로스페이드|영상 혼합 진행량 감속형|
|N2|실적 막대 위쪽 성장, 원형 시계방향 채움과 숫자 변화|세 원형 진행량 모두 감속형|
|N3|매출처 도넛의 시계방향 채움과 가족사 비중 증가|채움 감속형|
|N4|큰 제목 공개/소실과 작은 EG-BIM 자간 수렴·가시성 증가|공개 가속후감속, 소실 가속, 자간 수렴 감속 성향|
|N5|첫 UI 이미지의 오른쪽 이동과 가시성 증가|경계 이동 감속형|
|N6|기존 UI 우하단 이동·축소와 다음 도면 창 진입|기존창 가속후감속, 새창 감속|
|N7|모델 우하단 이동·확대와 뒤 창 재배치|모델 확대 감속, 창 재배치 가속후감속 성향|
|N8|광점/빛띠 강화|고정 ROI 밝기 가속후감속 성향; 위치 속도와 구분|

장헌 도입부를 움직임으로 설명했던 중간 추정은 픽셀 대조 뒤 철회했습니다. 관측 해상도에서는 정지입니다. EG 저대비 배경의 일부 변화는 같은 대상을 분리하기 어려워 곡선 미분류로 남겼습니다. 원형 채움과 창 경계의 곡선은 비교 근거가 강하지만, 빛·복합 가시성의 곡선은 참고 후보입니다. 애매한 대상을 전부 ease-out으로 채우지 않았습니다.

## 실행과 검수

원본 등록경로/해시, MP4 자체 참조, bounded decode와 sample-table 시간 대조를 유지했습니다. 첫 시간 제한 중지와 다음 메모리 제한 중지는 보존하고, 제한을 늘리지 않은 직접 축소/단일 할당으로 보완했습니다. 같은 조건의6개 실행 재시험에서175개 PNG와 두 관측 배열 RGB, 시각/순번이 일치했습니다. 기존 R4-1로 추가 시간 기록 구조도 검사했고, 오차 미상은 그대로 남겼습니다. 영상 분석 정확도나 일반화 성능 수치는 만들지 않았습니다.

검수용 짧은 영상10개는 원래 프레임 간격/속도를 유지하고 원본 시각을 헤더에 표시했습니다. 저해상도·무음 미리보기이며 실영상 무음 판정이 아닙니다. 인코딩 후 프레임 수/PTS/크기를 다시 확인했습니다. 별도 API·전사·AE/CU 조작은 없습니다. 동일 작성자의 자체 레드팀이며 독립 검토가 아닙니다.

## 사용자가 추가로 확인할 것

[추가 모션8묶음 — 재생 영상과 확인 항목](../02_분석작업/01-A2_전체모션재검수/00_추가로_확인할_모션.md)만 제시합니다. 기존 숫자 판독과 E 정정은 다시 묻지 않습니다. 새 항목의 회신 전에는 사람 검수를 완료 처리하지 않습니다.

전체 영상/음성/정밀 좌표·공간 이관/실제 사업·제품 사실은 여전히 이번 범위 밖입니다. 현재 구간의 AI 재검수 완료를 미분류 대상의 속도 확정이나 영상 전체 승인으로 확대하지 않습니다.

상세 근거: [관측 초안](../02_분석작업/01-A2_전체모션재검수/모션재검수_관측초안.json), [레드팀과 보완](../04_검증자료/01-A2_전체모션재검수/자체검수_레드팀_보완.md), [기존 지식과 누락 원인](../04_검증자료/01-A2_전체모션재검수/기존지식_연결과_누락원인.json), [재시험](../04_검증자료/01-A2_전체모션재검수/동일조건_재시험.json).
'''
    textfile(REPORT,report)
    put(f'{VE}/미실행과_범위경계.json',{'no_AE_source_values_requested':True,'no_new_A3_skill':True,'existing_management_skills_changed':False,'Phase00_modified':False,'AE_CU_changed':False,'audio_decoded':False,'separate_API_calls':0,'outside_windows_display_frames_selected':False,'decoder_packet_lookahead':'B-frame reference/lookahead packets may be read; no claim about hidden native processing outside selected presentation range','full_resolution_all_frames_visually_reviewed':False,'proxy_all_frames_in_scope_processed':1652,'static_preview_notes':'contact sheets may be host-resized; full1920 selected PNGs checked for motion identity','original_SAR_unknown':True,'diagnostic_geometry_uncertainty':'unknown','integrated_R4_spatial_validation':False})
    # Assert all source pins still match; original companies' sources are read-only.
    original=json.loads((BASE/'입력고정과_컨테이너사전점검.json').read_text(encoding='utf-8'))
    sourcecheck=[{'path':i['path'],'unchanged':sha(Path(i['path']))==i['sha256']} for i in original]+[{'path':i['path'],'unchanged':sha(ROOT/i['path'])==i['sha256']} for i in knowledge];assert all(x['unchanged'] for x in sourcecheck);put(f'{VE}/원본과_Phase00_재확인.json',sourcecheck)
    for name in ['기존지식_연결과_누락원인.json','R4-1_추가시간_검사.json','동일조건_재시험.json','원본과_Phase00_재확인.json']:
        category='보완과_재시험' if '재시험' in name else '기술검수';copy(STAGE/VE/name,f'{IMP}/{category}/전체모션_{name}')
    textfile(f'{IMP}/내용검수/추가모션_검수안내.md',f'새 사람 검수는N1~N8이며 대기 중입니다. 기존①~⑥은 유지합니다.\n\n[재생 영상과 확인 항목](<{(ROOT/AN/"00_추가로_확인할_모션.md").as_posix()}>)\n')
    manifest=[]
    for src in sorted(STAGE.rglob('*')):
        if src.is_file():manifest.append({'relative_path':src.relative_to(STAGE).as_posix(),'sha256':sha(src),'bytes':src.stat().st_size})
    write(HERE/'게시명세.json',{'expected_before':before,'files':manifest})
    print(json.dumps({'files':len(manifest),'bytes':sum(x['bytes'] for x in manifest),'new_pending_groups':8,'snapshots_new':175,'snapshot_total':snapshot_total,'unique_times':len(allkeys),'R4_time_valid':[x['result']['valid'] for x in time_checks],'A3_started':False},ensure_ascii=False))
if __name__=='__main__':main()
