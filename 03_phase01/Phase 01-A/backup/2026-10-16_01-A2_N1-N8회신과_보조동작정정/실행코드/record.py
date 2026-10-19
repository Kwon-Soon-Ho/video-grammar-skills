from pathlib import Path
import sys,json,shutil,hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
from fractions import Fraction
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'phase01a-a2'))
from prepare import ROOT,sha,write
P='Phase 01-A';AN=f'{P}/02_분석작업/01-A2_전체모션재검수';VE=f'{P}/04_검증자료/01-A2_전체모션재검수'
IMP='작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A2'
BK=f'{P}/backup/2026-10-16_01-A2_N1-N8회신과_보조동작정정'
STAGE=HERE/'게시안';STAGE.mkdir(exist_ok=True)
NOTE=f'{AN}/01_N1-N8_확인완료와_빛커서_정정.md'
OBS=f'{AN}/모션재검수_확정과_추가정정.json'
REC=f'{VE}/사람확인_N1-N8과_빛커서정정_회신.json'
REPORT=f'{P}/05_결과보고/09_01-A2_N1-N8_확인과_보조모션_정정보고.md'
NOW=datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds')
REPLY='N1~N8 모두 맞아. 검수 기록에 반영하고, 이번에 놓친 부분이 좀 더 있는데 "처음에 등장하는 큰E 주변으로 얇은 빛 테두리가 지나가고, 큰 영문은 케드 커서 같은 십자 커서로 점선 사각형테두리로 등장시키고 그 점선이 축소되면서 텍스트가 오퍼시티로 연해지는거야." 이 부분은 놓친거야? 아니면 기록을 그냥 안 한거야? 니가 파악할 수 있는 부분이야?'
before={}
def put(rel,obj):
    dst=ROOT/rel
    if dst.exists():
        before[rel]=sha(dst);back=STAGE/BK/'변경전'/rel;back.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dst,back)
    out=STAGE/rel;out.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(obj,str):out.write_text(obj,encoding='utf-8')
    else:write(out,obj)
def read(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8-sig'))
def copy(src,rel):
    out=STAGE/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,out)

def build():
    request_rel=f'{VE}/추가모션_8항목_검수요청.json';request=read(request_rel)
    assert request['status']=='pending','already processed or concurrent update'
    assert sha(ROOT/request['guide_path'])==request['guide_sha256']
    assert sha(ROOT/AN/'모션재검수_관측초안.json')==request['observation_sha256']
    for g in request['groups']:
        for pin in g['evidence_pins']+g['clip_pins']:assert sha(ROOT/pin['path'])==pin['sha256']
    native=json.loads((HERE/'cases/자료013/detail/실행기록.json').read_text(encoding='utf-8'))
    assert native['complete_target_selection'] and native['input_sha256']==native['input_sha256_after']
    # Fixed crop previews only; retain full source-derived native PNGs alongside them.
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
    fs={float(Fraction(f['actual_playback_seconds'])):f for f in native['frames']}
    for name,times,crop,size in [
        ('E주변_빛_시점대조',[.5,.75,1,1.25],(0,100,3500,2050),(800,446)),
        ('십자커서_점선영역_확대와축소',[1.9,2.1,2.4,3.2,3.3,3.4,3.5],(450,450,3650,1350),(1200,338))]:
        canvas=Image.new('RGB',(size[0],(size[1]+30)*len(times)),'#141a20');draw=ImageDraw.Draw(canvas)
        for i,t in enumerate(times):
            frame=Image.open(fs[t]['path']).crop(crop).resize(size,Image.Resampling.LANCZOS)
            y=i*(size[1]+30);canvas.paste(frame,(0,y+30));draw.text((8,y+2),f'{t:.3f}s | source-raster crop {crop}',font=font,fill='white')
        path=HERE/(name+'.jpg');canvas.save(path,quality=95)
        copy(path,f'{AN}/빛커서_보완근거/{path.name}')
    for f in native['frames']:
        path=Path(f['path']);assert sha(path)==f['sha256'];copy(path,f'{AN}/빛커서_보완근거/원본해상도/{path.name}')
    copy(HERE/'cases/자료013/detail/실행기록.json',f'{VE}/빛커서_보완추출_실행기록.json')
    for path in [HERE/'native.py',HERE/'prepare_native.py',Path(__file__)]:copy(path,f'{BK}/실행코드/{path.name}')
    additions=[
      {'id':'C1-E-outline-light','human_statement':'처음 큰 E 주변으로 얇은 빛 테두리가 지나감','prior_record':'S-EG-ambient에 저대비 광선을 일반적으로 적었지만, E 주변 빛의 통과를 별도 사건으로 식별하지 못함','classification':'분석 누락; 단순 기록 생략이 아님','video_observation':'약0.5~1.25초 비교에서 큰 E 주변의 얇은 녹색 발광선/수평 빛과 밝은 부분의 통과가 보임. E 본체 조각 슬라이드와 별개로 구분','curve':'미분류: 고정 테두리의 밝기 변화와 이동하는 발광 부분이 중첩. 경로 전체·속도곡선을 측정 완료했다고 하지 않음','human_status':'user_provided_correction_recorded','ai_status':'visible_supporting_motion_reidentified_after_user_cue'},
      {'id':'C2-CAD-cursor-box','human_statement':'CAD 같은 십자 커서로 점선 사각형 테두리를 나타내 큰 영문을 공개하고, 점선이 축소되면서 글자가 opacity로 연해짐','prior_record':'N4는 공개/소실 경계와 연한 문구 잔존만 적음. 커서·점선 선택 영역을 독립 대상으로 식별하지 않음','classification':'분석 누락 및 설명 과도 단순화','video_observation':'적색 가로선·녹색 세로선·중앙 작은 사각형의 십자 커서가 보이고, 그에 연결된 듯한 점선 사각 영역이 확대되며 Value of를 공개. 약3.2~3.5초 영역의 왼쪽 경계가 오른쪽으로, 위쪽 경계가 아래로 이동해 우하단 쪽으로 축소되며 연한 전체 문구가 남음. 글자 자체가 작아지는 현상과 구분','curve':'기존 N4의 공개 ease-in-out/밝은 영역 소실 ease-in은 경계 진행량의 관측 후보로 유지. 전체 텍스트 opacity 속도곡선으로 바꾸어 부르지 않음','human_status':'user_provided_correction_recorded','ai_status':'cursor_and_dashed_region_and_faint_text_visually_confirmed; actual_AE_opacity_or_matte_implementation_unverified'}]
    receipt={'id':'A2-HUMAN-N1-N8-CURSOR-LIGHT-REPLY','recorded_at':NOW,'reply_verbatim':REPLY,'approved_groups':[f'N{i}' for i in range(1,9)],'prior_six_approvals_preserved':True,'request_path':request_rel,'request_sha256_before_reply':sha(ROOT/request_rel),'context_sha256':request['context_sha256'],'guide_sha256_at_confirmation':request['guide_sha256'],'observation_sha256_at_confirmation':request['observation_sha256'],'new_user_corrections':additions,'scope':'N1–N8 visible direction/order/curve-family descriptions confirmed, with N4 additionally clarified by C2. Not exact AE values or complete-video approval. C1/C2 are direct user corrections, not answers to an invented new request.','pending_new_human_questions':[],'remaining_AI_uncertainties':['C1 full moving-light path and curve unclassified','C2 original AE opacity/matte implementation and exact curve unknown'],'A3_started':False}
    put(REC,receipt);put(f'{IMP}/내용검수/사람확인_N1-N8과_빛커서정정_회신.json',receipt)
    obs=read(f'{AN}/모션재검수_관측초안.json');obs['version']='0.2';obs['current_receipt']=REC
    for g in obs['observations'] if 'observations' in obs else obs.get('claims',[]):
        if g.get('id') in receipt['approved_groups']:g['human_review']='confirmed_N1-N8_reply'
    # The original schema uses groups; update every actual group, never rely on a guessed key.
    updated=0
    for value in obs.values():
        if isinstance(value,list):
            for g in value:
                if isinstance(g,dict) and g.get('id') in receipt['approved_groups']:
                    g['human_review']='confirmed_N1-N8_reply';updated+=1
    assert updated==8,('wrong_confirmed_group_count',updated)
    obs['additional_user_corrections']=additions;obs['current_status']='eight_groups_confirmed_with_two_additional_user_corrections';obs['pending_new_human_questions']=[]
    obs['earlier_human_confirmations']='original six approvals and E-piece correction preserved; N1–N8 now confirmed by current receipt'
    put(OBS,obs)
    request['status']='confirmed_with_additional_user_clarification';request['receipt']=REC;request['recorded_at']=NOW
    request['original_request_sha256']=receipt['request_sha256_before_reply'];request['clarifications']=['C1-E-outline-light','C2-CAD-cursor-box']
    for g in request['groups']:g['human_review']='confirmed_N1-N8_reply'
    put(request_rel,request);put(f'{IMP}/내용검수/추가모션_8항목_검수요청.json',request)
    for rel in [f'{P}/04_검증자료/01-A2_작은예비/사람검수_대기.json',f'{IMP}/내용검수/사람검수_대기.json']:
        queue=read(rel);queue['status']='previous_six_and_N1_N8_confirmed_additional_user_corrections_recorded'
        queue['confirmed']=list(dict.fromkeys(queue['confirmed']+receipt['approved_groups']));queue['pending_claims']=[];queue['pending_scope']=None
        queue['current_receipt']=REC;queue['current_observation']=OBS;queue['new_user_corrections']=['C1-E-outline-light','C2-CAD-cursor-box'];queue['pending_new_human_questions']=[]
        put(rel,queue)
    note='''# N1~N8 확인 완료와 빛·커서 동작 정정

2026-10-16 · 사용자가 N1~N8 모두 맞다고 확인했습니다. 기존①~⑥과 E 조각 슬라이드 정정도 유지합니다. 추가 질문 대기 항목은 없습니다. A3는 시작하지 않았습니다.

말씀하신 두 동작은 **분석에서 놓친 부분**입니다. 이미 파악하고 설명에서만 뺀 것이 아닙니다. 이전 기록의 S-EG-ambient에 광선 일반 묘사가 있었고 N4에 공개/소실 경계는 있었지만, E 주변 빛·십자 커서·점선 선택 영역을 각각 식별하고 연결하지 못했습니다.

| 보완 | 사용자 설명과 영상 재대조 결과 |
|---|---|
| C1 · E 주변 빛 | 큰 E 주변에 얇은 녹색 발광선이 지나갑니다. E 본체와 구분해 보조 동작으로 추가했습니다. 발광 부분의 전체 경로와 가감속은 아직 확정하지 않았습니다. |
| C2 · CAD 선택 연출 | 적색 가로선·녹색 세로선의 십자 커서와 점선 사각형이 나타나고, 선택 영역이 커지며 Value of를 공개합니다. 이후 점선 영역이 우하단 쪽으로 줄어들며 밝은 글자 영역이 걷히고 연한 전체 문구가 남습니다. 점선 영역 축소와 글자 자체의 크기 변화를 구분했습니다. |

사용자의 “opacity로 연해짐”을 연출 설명으로 기록했습니다. 영상에서도 연한 문구가 남는 것은 확인했습니다. 다만 실제 AE에서 하나의 Opacity를 낮췄는지, 매트와 연한 복제 텍스트를 겹쳤는지는 영상만으로 확정하지 않습니다. 기존 N4의 소실 가속형은 밝은 영역 경계의 진행량에 대한 판단이며, 전체 텍스트 Opacity 곡선 측정으로 확대하지 않습니다.

제가 파악할 수 있는 동작입니다. 이번에도 큰 대상과 밝은 영역 위주로 추적하면서, 동작을 만드는 작은 커서·점선과 얇은 빛을 빠뜨렸습니다. 저해상도 관측 배열과 전체 프레임 처리만으로 모든 요소의 동작을 검수했다고 볼 수 없는데, 완료 표현을 넓게 쓴 점도 정정합니다. 앞으로 같은 구간의 각 대상에 대해 본체·테두리/커서·빛·가시성 변화를 따로 식별한 다음 방향·순서·가감속을 기록해야 합니다. 이번 보완이 영상 전체의 완전성 보증은 아닙니다.

## 다시 대조한 화면

아래는 원본 해상도에서 추출한 프레임의 일부를 잘라 배열한 비교 화면입니다. 색/대비 증강은 하지 않았습니다. 원본 해상도 PNG와 PTS/해시 기록도 함께 보관했습니다.

![E 주변 빛 시점 대조](빛커서_보완근거/E주변_빛_시점대조.jpg)

![십자 커서와 점선 영역의 확대·축소](빛커서_보완근거/십자커서_점선영역_확대와축소.jpg)

N1~N8이나 이번에 직접 설명해 주신 두 동작을 다시 승인해 달라고 묻지 않습니다. 미확정 기술 사항은 AI 분석 한계로 남깁니다.
'''
    put(NOTE,note)
    guide=f'{AN}/00_추가로_확인할_모션.md'
    put(guide,'> 현재 상태: N1~N8 모두 사용자 확인 완료(2026-10-16). 아래 표는 당시 검수 요청 이력입니다. [빛·커서 추가 정정과 현재 결과](01_N1-N8_확인완료와_빛커서_정정.md)를 함께 적용합니다.\n\n'+(ROOT/guide).read_text(encoding='utf-8'))
    report='# 01-A2 N1~N8 확인과 보조 모션 정정\n\n'+note.split('\n',1)[1]+'\n\n[현재 관측 기록](../02_분석작업/01-A2_전체모션재검수/모션재검수_확정과_추가정정.json) · [사람 회신](../04_검증자료/01-A2_전체모션재검수/사람확인_N1-N8과_빛커서정정_회신.json)\n'
    # Report reuses prose, but images resolve from its own location.
    report=report.replace('(빛커서_보완근거/','(../02_분석작업/01-A2_전체모션재검수/빛커서_보완근거/')
    put(REPORT,report)
    oldreport=f'{P}/05_결과보고/08_01-A2_현재구간_모션재검수_보고.md'
    put(oldreport,'> 후속 회신 반영: N1~N8 확인 완료. [현재 정정 보고](09_01-A2_N1-N8_확인과_보조모션_정정보고.md)를 적용합니다. 아래는 회신 전 이력입니다.\n\n'+(ROOT/oldreport).read_text(encoding='utf-8'))
    planrel=f'{P}/00_진행안내/01-A_계획상태.json';plan=read(planrel)
    plan.update(version='0.7',state='A2_N1_N8_confirmed_secondary_motion_corrections_recorded',human_content_reviews_pending=0,human_content_reviews_pending_unit='no current human questions; AI uncertainties retained',next_decision='현재 확인 결과와 추가 누락 정정 적용. A3 미착수',stage_A2_status='기존6항목과 N1~N8 사용자 확인 완료. 빛·커서·점선 누락은 사용자 정정과 원본 재대조로 보완. 미확정 보조 빛 곡선은 유지',stage_A2_report=REPORT.removeprefix(P+'/'),human_content_review_record=REC,A3_started=False,stage_A2_current_observation=OBS,stage_A2_native_supplement_images=16)
    plan['human_confirmed_new_motion_groups']=8;plan['additional_user_corrections_recorded']=2
    put(planrel,plan)
    notice_rel=f'{P}/00_진행안내/16_01-A2_현재구간_모션재검수_현재안내.json';notice=read(notice_rel)
    notice.update(state=plan['state'],report=REPORT,guide=NOTE,new_human_groups_pending=0,new_human_groups_confirmed=8,current_receipt=REC,current_observation=OBS,additional_user_corrections=2,AI_uncertainties=receipt['remaining_AI_uncertainties'])
    put(notice_rel,notice)
    put(f'{IMP}/내용검수/추가모션_검수안내.md',f'# 현재 검수 상태\n\nN1~N8 모두 확인 완료. 기존①~⑥과 E 정정 유지. 추가 질문 없음.\n\n[빛·커서 정정과 현재 결과](<{(ROOT/NOTE).as_posix()}>)\n')
    request['guide_at_issue']={'path':guide,'sha256':receipt['guide_sha256_at_confirmation'],'archived_path':f'{BK}/변경전/{guide}'}
    request['current_guide_sha256']=sha(STAGE/guide)
    request['context_sha256_scope']='original issued request; approval receipt pins pre-reply bytes'
    put(request_rel,request);put(f'{IMP}/내용검수/추가모션_8항목_검수요청.json',request)
    files=[{'path':p.relative_to(STAGE).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in STAGE.rglob('*') if p.is_file()]
    write(HERE/'게시명세.json',{'created_at':NOW,'files':files,'expected_before':before})
    print(json.dumps({'staged':len(files),'human_confirmed':8,'new_user_corrections':2,'pending_questions':0},ensure_ascii=False))

def publish():
    m=json.loads((HERE/'게시명세.json').read_text(encoding='utf-8'));before=m['expected_before']
    for item in m['files']:
        rel=item['path'];src=STAGE/rel;dst=(ROOT/rel).resolve()
        assert dst.is_relative_to(ROOT.resolve()) and (rel.startswith((AN+'/',VE+'/',BK+'/',IMP+'/')) or rel in [f'{P}/00_진행안내/01-A_계획상태.json',f'{P}/00_진행안내/16_01-A2_현재구간_모션재검수_현재안내.json',f'{P}/04_검증자료/01-A2_작은예비/사람검수_대기.json',REPORT,f'{P}/05_결과보고/08_01-A2_현재구간_모션재검수_보고.md'])
        assert sha(src)==item['sha256']
        assert not dst.exists() or sha(dst)==item['sha256'] or sha(dst)==before.get(rel),rel
        if src.suffix=='.json':json.loads(src.read_text(encoding='utf-8-sig'))
    if '--publish' not in sys.argv:print('prepublication checks passed');return
    for item in m['files']:
        dst=ROOT/item['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(STAGE/item['path'],dst);assert sha(dst)==item['sha256']
    result={'published_files':len(m['files']),'all_hashes_match':True,'human_confirmed_N1_N8':True,'pending_questions':0,'AE_values_requested':False,'A3_started':False,'source_hash_unchanged':True,'not_a_claim_of_complete_video_accuracy':True}
    write(HERE/'게시후_검증.json',result);write(ROOT/VE/'N1-N8회신과_빛커서정정_게시후검증.json',result)
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':
    if '--check' in sys.argv or '--publish' in sys.argv:publish()
    else:build()
