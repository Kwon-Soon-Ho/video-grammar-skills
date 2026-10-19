from pathlib import Path
from fractions import Fraction as F
import json,hashlib,shutil,sys,importlib.util
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'phase01a-a2'
sys.path.insert(0,str(BASE))
from prepare import ROOT,sha,write
STAGE=HERE/'게시안'
P='Phase 01-A';AN=f'{P}/02_분석작업/01-A2_작은예비';VE=f'{P}/04_검증자료/01-A2_작은예비'
BK=f'{P}/backup/2026-10-16_01-A2_검수회신과_모션보완'
IMP='작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A2'
guide=ROOT/IMP/'내용검수/사람검수_화면안내/00_확인할_화면과_항목.md'
def read(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8-sig'))
def put(rel,obj):write(STAGE/rel,obj)
def txt(rel,s):
    p=STAGE/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def copy(src,rel):
    p=STAGE/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,p)
def q(x):
    x=F(x);return {'num':x.numerator,'den':x.denominator}
def main():
    changes=[f'{AN}/관측초안.json',f'{AN}/00_분석초안_읽기.md',f'{VE}/사람검수_대기.json',f'{VE}/자체검수와_레드팀_보완.md',f'{P}/05_결과보고/07_01-A2_작은예비분석_보고.md',f'{P}/00_진행안내/01-A_계획상태.json',f'{P}/00_진행안내/15_01-A2_실행결과_현재안내.json',f'{IMP}/내용검수/사람검수_대기.json']
    expected_before={rel:sha(ROOT/rel) for rel in changes}
    for rel in changes:
        backup_rel=Path(rel).relative_to(P).as_posix() if rel.startswith(P+'/') else rel
        copy(ROOT/rel,f'{BK}/변경전/{backup_rel}')
    run=json.loads((BASE/'cases/자료013/motion_review/실행기록.json').read_text(encoding='utf-8'))
    repeat=json.loads((BASE/'cases/자료013/motion_review_retest/실행기록.json').read_text(encoding='utf-8'))
    assert len(run['frames'])==len(repeat['frames'])==31
    retest={'images':31,'all_hashes_match':all(a['sha256']==b['sha256'] for a,b in zip(run['frames'],repeat['frames'])),'all_times_match':all(a['actual_playback_seconds']==b['actual_playback_seconds'] and a['container_cts_ticks']==b['container_cts_ticks'] and a['display_ordinal_zero_based']==b['display_ordinal_zero_based'] for a,b in zip(run['frames'],repeat['frames'])),'input_unchanged':run['input_sha256_after']==repeat['input_sha256_after'],'decoded_frames_each':run['decoded_frames'],'timing_check':run['timing_status'],'scope':'same decoder/path deterministic re-extraction, not independent motion performance test'}
    assert retest['all_hashes_match'] and retest['all_times_match'] and retest['input_unchanged']
    put(f'{VE}/모션보완_재시험.json',retest)
    # Pin precisely the six review groups and the original presented evidence.
    draft=read(f'{AN}/관측초안.json')
    review_map={'①':['JH-01'],'②':['JH-02 remainder','JH-03 goals'],'③':['JH-05'],'④':['EG-01','EG-02'],'⑤':['JH-04'],'⑥':['EG-03']}
    context={'guide_path':str(guide),'guide_sha256':sha(guide),'observation_version':draft['version'],'observation_sha256':sha(ROOT/AN/'관측초안.json'),'groups':review_map,'preview_pins':[{ 'path':str(p),'sha256':sha(p)} for p in [guide.parent/'01_확인할_정지화면.jpg',guide.parent/'02_확인할_변화순서.jpg']],'source_assets':run['input_sha256'],'scope':'only presented text/numbers/layout/sampled sequence; excludes actual business/product truth, audio, full-video quality and exact keyframe/easing parameters'}
    context_hash=hashlib.sha256(json.dumps(context,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
    reply='①~⑥ 모두 맞아. 이 답변을 검수 기록에 반영하고, 01-A2에서 더 확인할 게 남았는지 알려줘. 추가로 말하면 단순히 "큰 E가 녹색에서 금색·갈색 계열로 변함"가 아니라 큰 E가 조각되어서 좌측에서 우측으로 슬라이드 되며 들어오는거야. 그리고 키프레임도 슬라이드 되듯이 초반에 빠르게 진입하다가 천천히 진입(이걸 전문영어로 뭐라고 부르지? 이지 아웃 뭐 이런 식이던데) 이 부분까지 니가 검수 했는데, 나한텐 화면 구성만 확인한다고 안 물어본거야? 아니면 놓친거야?'
    receipt={'id':'A2-HUMAN-SIX-GROUPS-20261016','version':'0.1','recorded_at':'2026-10-16T13:17:18+09:00 or later; exact user submission time not exposed','source':'actual direct user reply in this chat','verbatim':reply,'context':context,'context_sha256':context_hash,'decision':'confirmed_presented_six_groups_with_E_motion_correction','confirmed_groups':list(review_map),'correction':{'previous':'large E green-to-gold/brown change only','user_description':'large E is divided into pieces that slide in left-to-right; starts fast and decelerates into place','accepted_scope':'user-provided qualitative motion description','AI_had_previously_verified_this':False,'AI_verified_after_reply':'31 images over4.0–5.5s and repeated extraction, separate report','exact_curve_or_AE_keyframes_confirmed':False},'identity_verified':False,'company_approved':False,'does_not_approve':['whole video','audio','actual business figures','actual product performance','exact start/end/easing formula/control handles','A3/01-B/02 execution']}
    put(f'{VE}/사람확인_6묶음과_E모션보완_회신.json',receipt)
    put(f'{VE}/사람검수_대기.json',{'status':'presented_six_groups_confirmed_with_E_motion_correction','confirmed':['H-JH16','H-JH18']+list(review_map),'confirmed_claim_groups':review_map,'pending_claims':[],'pending_scope':'none within the six presented groups only','current_receipt':'사람확인_6묶음과_E모션보완_회신.json','new_motion_measurements':'AI diagnostic evidence, not new human-approved numeric ground truth','remaining_unreviewed_scope':['audio and AV sync','unobserved portions and changes between sparse samples','precise original coordinates/SAR','exact easing curve, start/end times and original AE keyframe parameters','business/product truth','R4 integrated evidence/spatial ingestion'],'no_auto_approval':True})
    draft['version']='0.3'
    for claim in draft['claims']:
        claim['human_status']='user_confirmed_presented_scope_20261016; no business/product/whole-video approval'
        if claim['id']=='JH-03':
            claim['text']=claim['text'].replace('사람 확인 범위는 세 지표 실적/달성률이며 목표값은 AI 초안.','최초에는 실적/달성률만 확인했으며, 후속 ② 회신으로 제시한 목표값도 확인됨. v4와의 문서 대응은 작성자의 비교 기록임.')
        if claim['id']=='EG-03':
            claim['text']='3~7초 표본에서 Value of 문구가 흐려지고 우측 EG-BIM 제목이 보인다. 큰 E는 단순 색 변화뿐 아니라 나뉜 조각들이 좌측에서 우측으로 슬라이드하며 맞춰지고 감속하는 진입 동작이다. 색·질감도 녹색에서 금색/갈색 계열로 달라진다. 사용자 설명 후4.0~5.5초 0.05초 표본으로 이동과 감속을 보완 확인했다. 8초 UI 이미지→12초 도면 이미지→14~15.5초 전면 철근/콘크리트 형태 모델 이미지의 순서가 보인다. 정밀 경계·원본 AE 키프레임·곡선 식은 미확인.'
            claim['human_status']='six-group sample sequence confirmed; piecewise left-to-right decelerating slide supplied by user; rechecked by AI afterwards'
    draft['review_receipt']=receipt['id']
    draft['remaining']=['audio and full-video scopes not reviewed','sparse sampling can miss other motion','exact easing/keyframes/coordinate uncertainty unresolved','R4 integrated ingestion not implemented']
    draft['motion_correction']={'missed_in_initial_analysis':True,'why':'sample description stopped at appearance/state sequence; did not track moving pieces or inspect deceleration','user_feedback_applied':True,'new_evidence':'자료013/motion_review/실행기록.json','measurement_status':'diagnostic edge candidates only, unknown positional uncertainty; not validated R4 spatial measurements'}
    put(f'{AN}/관측초안.json',draft)
    # Independent R4-1 subrecord for added frame evidence; original record is untouched.
    time=read(f'{AN}/자료013/R4-1_시간연결_초안.json');time['periods']=[{'id':'자료013-MOTION','timeline_ref':'자료013-T','parent_ref':None,'kind':'range','start':q(4),'end':q(F(111,20)),'uncertainty':None,'unknown_reason':None}]
    time['frames']=[{'id':f['frame_id'],'timeline_ref':'자료013-T','period_ref':'자료013-MOTION','role':'within_period','source_pts':f['container_cts_ticks'],'pts_kind':'original_pts','time_base':q(F(f['time_base'])),'source_frame_ordinal':f['display_ordinal_zero_based'],'requested':q(f['requested_playback_seconds']),'actual':q(f['actual_playback_seconds']),'mapping_state':'mapped','selection_policy':'at_or_after','limitations':'container CTS reconstructed with sample tables and single edit offset; scope is added4.0–5.5s sparse frames; metadata/source identity same as initial record'} for f in run['frames']]
    time['notes']='Separate A2 motion evidence subrecord; not an additional time axis in an integrated record. Full evidence/spatial integration not built. Boundary error unknown. Does not validate motion interpretation.'
    put(f'{AN}/자료013/R4-1_모션보완_시간연결.json',time)
    tool=ROOT/'Phase 00/07_실행도구/시간프레임_규격검사.py';spec=importlib.util.spec_from_file_location('r4_motion',tool);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);valid=mod.validate(time)
    assert valid['valid'];put(f'{VE}/모션보완_R4-1_검사.json',{'validator':str(tool),'validator_sha256':sha(tool),'result':valid})
    diag=json.loads((HERE/'E_가운데조각_경계진단.json').read_text(encoding='utf-8'))
    # Values remain candidates; manual image checks establish correspondence for reviewed examples only.
    pts={F(s['seconds']):s['derived_right_edge_x_candidate'] for s in diag['samples']}
    samples=[{'interval_seconds':[str(a),str(a+F(1,10))],'approx_derived_raster_displacement_px':pts[a+F(1,10)]-pts[a]} for a in [F(4),F(22,5),F(24,5)]]
    diag.update(visual_correspondence_review={'method':'4.0–5.5 contact sheet plus individual4.1/4.4/4.8 images; middle horizontal piece right boundary','reviewer':'current Codex model','independent':False},illustrative_equal_time_displacements=samples,interpretation='rightward displacement decreases in these equal-time windows, supporting qualitative deceleration; not an exact easing curve fit',late_edge_caution='5.45s detector moves5px after near-plateau; changing texture/glow may bias the detector; no claim of perfectly stationary object or certified positional error')
    put(f'{VE}/E_가운데조각_경계진단.json',diag)
    sources={'checked_on':'2026-10-16','purpose':'terminology only; no company files uploaded to web search','sources':[{'url':'https://web.dev/articles/the-basics-of-easing','claim':'ease-out is faster start with deceleration at end'},{'url':'https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/speed-between-keyframes/speed.html','claim':'AE Easy Ease In acts on incoming speed, Easy Ease Out on outgoing speed; generic easing name does not identify actual AE preset'}],'skill':{'path':'C:/Users/User/.codex/skills/animation-principles/SKILL.md','scope':'easing vocabulary and motion review; no prescribed curve/grid adopted as observed truth'}}
    put(f'{VE}/이징_용어출처.json',sources)
    note='''# 01-A2 후속 검수 — 여섯 묶음 확인과 E 모션 누락 보완

2026-10-16 · 사용자 ①~⑥ 확인 접수 · 제시한 내용의 사람 검수 대기 0건. 전체 영상 승인은 아니다.

사용자는 ① 제목/배치, ② 목표 숫자/빈칸, ③ 매출 구성, ④ EG-BIM 제목/설명문, ⑤ 장헌 표본 변화 순서, ⑥ EG-BIM 표본 순서를 모두 맞다고 확인했다. 실제 답변과 당시 안내·초안·이미지 해시는 별도 회신 파일에 고정했다. 최초 숫자 회신은 당시 범위 그대로 보존했다.

## 놓친 부분과 수정

이전 분석은 E의 색·외관 변화와 다른 요소의 등장 순서까지만 적었다. **E가 나뉜 조각으로 좌측에서 우측으로 슬라이드하며 진입하고 감속하는 동작을 충분히 분석하지 않았다.** 알고도 사용자에게 묻지 않은 것이 아니라 최초 분석과 검수 안내의 누락이다. 원래 보고의 ‘정확한 이징 미측정’ 한계가 이 동작을 놓쳐도 된다는 뜻은 아니다.

사용자가 알려 준 설명을 사용자 출처로 기록한 뒤, EG-BIM 4.0~5.5초를 0.05초 간격으로 요청해31장을 추가 추출했다. 331프레임의 시간은 기존처럼 MP4 시간표와 편집 오프셋을 대조했고, 같은 조건의 재추출31장은 해시·시각·순번이 같다. 원본 해시도 같다. 음성·별도 API·AE/CU 조작은 없다.

여러 조각의 경계가 서로 다른 위치에서 우측으로 이동해 E를 구성하는 모습을 표본에서 확인했다. 가운데 가로 조각의 오른쪽 경계를 파생1920×1080 raster에서 진단하면, 같은0.1초 동안 이동한 후보량이4.0~4.1초 약170px,4.4~4.5초 약42px,4.8~4.9초 약12px로 줄어든다. 이는 감속 동작을 지지하는 보조 근거다. 원본 좌표나 공식 속도값, 오차 검증이 끝난 R4 공간 측정값은 아니다. 표면 질감·광선에 따라 경계 검출이 흔들릴 수 있으며5.45초 이후 작은 후보 이동도 보존했다.

‘처음 빠르게 이동하고 도착하며 느려지는’ 동작은 일반적으로 **ease-out / decelerating slide-in**이라고 부른다. AE 메뉴는 키프레임의 들어오는 쪽/나가는 쪽을 기준으로 이름을 붙인다. 도착 키프레임으로 들어오는 속도를 누그러뜨리는 항목은 Easy Ease In이며, 일반 동작 설명의 ease-out과 메뉴명 Easy Ease Out을 그대로 동일시하면 안 된다. 실제 영상이 어떤 프리셋·베지어 핸들·키프레임 값으로 만들어졌는지는 MP4만으로 확인하지 않았다.

## 아직 확인하지 않은 범위

제시한 ①~⑥의 사람 내용 검수는 이번 회신으로 종료한다. 새 이징 곡선 수치나 원본 AE 키프레임까지 사용자가 승인한 것으로 기록하지 않는다. 나레이션/무음 여부·음성 동기, 장헌24초 이후·EG 마지막 약0.68초, 표본 사이 변화, 정확한 이징 곡선과 정밀 좌표/SAR, 실제 사업·제품 사실, R4 통합 근거·공간 이관은 여전히 미확인/미실행이다. 이번 작은 예비의 범위를 넘어가는 항목을 사용자에게 추가 화면 검수로 다시 요구하지 않는다.

## 자체 검수·레드팀·재시험

- 사람의 정정을 처음부터 AI가 관측한 것처럼 소급하지 않았다. 최초 누락과 이후 보완을 구분했다.
- E의 색/질감 변화도 보존하되, 이를 이동·분절 동작의 대체 설명으로 쓰지 않았다.
- 한 경계의 움직임으로 모든 조각의 동일 속도·동일 이징·정확한 시작/종료를 확정하지 않았다.
- 재추출31장, 원본 해시, R4-1 추가 시간기록의 형식/연결을 확인했다. 경계 오차 미상 등 unresolved는 남겼다. 구조 검사 통과를 내용 검증으로 확대하지 않았다.
- 작성자 자체 레드팀이며 독립 검토가 아니다. 변경 전 파일과 새 실행/진단 코드는 별도 backup에 보존했다. A3는 착수하지 않았다.

용어 출처: [Google web.dev](https://web.dev/articles/the-basics-of-easing), [Adobe AE 속도 제어](https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/speed-between-keyframes/speed.html).
'''
    txt(f'{VE}/후속검수_6묶음확인과_E모션보완.md',note)
    old_read=(ROOT/AN/'00_분석초안_읽기.md').read_text(encoding='utf-8')
    txt(f'{AN}/00_분석초안_읽기.md','''# 현재 검수 상태 — 2026-10-16 후속 회신 반영

①~⑥의 제시 내용은 사용자 확인 완료다. E 모션은 사용자 정정 뒤 조각별 좌→우 슬라이드와 감속을 추가 확인했다. `관측초안.json` v0.3과 [후속 검수 기록](../../04_검증자료/01-A2_작은예비/후속검수_6묶음확인과_E모션보완.md)을 현재 기준으로 읽는다.

아래는 최초 v0.2 분석 당시의 설명이다. 당시 사람 미검수·모션 미확인 문구는 이력이며 현재 상태는 위 안내/새 회신이 우선한다. 변경 전 파일은 backup에 보존했다.

'''+old_read)
    old_review=(ROOT/VE/'자체검수와_레드팀_보완.md').read_text(encoding='utf-8')
    txt(f'{VE}/자체검수와_레드팀_보완.md',old_review+'\n\n## 후속: 사용자 확인과 실제 모션 누락\n\n①~⑥ 확인 뒤 E 조각 슬라이드·감속 누락을 보완했다. 최초 분석에서 이 동작을 검수하지 못한 사실과0.05초 표본/경계 진단/31장 재시험을 [별도 후속 기록](후속검수_6묶음확인과_E모션보완.md)에 남겼다. 최초 사람 확인 범위만으로 현재 미검수 상태를 판단하지 않는다.\n')
    report='''# 01-A2 결과 — 후속 사람 검수와 모션 보완 반영

2026-10-16 · v0.2 · **제시한 ①~⑥의 사람 내용 검수 완료. E의 슬라이드·감속 누락을 수정하고 재시험했다.**

사용자가 제목·배치, 남은 목표 숫자/빈칸, 매출 구성, EG-BIM 제목·설명문, 두 영상의 표본 변화 순서를 모두 맞다고 확인했다. 최초 장헌 두 화면 숫자 확인도 보존했다. 확인 범위는 제시한 화면과 항목이며 회사 실적·제품 성능·영상 전체 승인이 아니다.

## 이번에 수정한 분석 누락

E의 색·외관 변화만 적었던 설명은 불충분했다. E는 **나뉜 조각들이 좌측에서 우측으로 슬라이드하며 들어와 맞춰지고, 처음 빠르게 움직이다 도착하며 감속한다.** 이 동작은 최초 검수에서 놓쳤고 사용자 정정 뒤 보완했다. 예전부터 검수한 것처럼 소급하지 않았다.

EG-BIM4.0~5.5초를0.05초 간격으로31장 추가 추출했다. 가운데 가로 조각의 이동 경계를 비교해 같은 시간 동안의 이동량이 줄어드는 양상을 확인했다. 이는 일반적으로 ease-out(감속 이징) 또는 decelerating slide-in으로 설명할 수 있다. 정확한 곡선·시작/종료·원본 AE 키프레임·베지어 핸들은 확인하지 않았다.

## 확인한 범위와 검수 결과

| 항목 | 현재 상태 |
|---|---|
| 사람 검수 | 제시한①~⑥ 확인 완료, 해당 여섯 묶음의 사람 대기0건. 사용자 정정은 별도 출처로 보존 |
| 장헌 | 0~24초 표본, 숫자 모션의 중간값/이후 안정값 구분. 24초에56%가 아직 안 보인다는 확인을 전체 영상 누락 판정으로 확대하지 않음 |
| EG-BIM | 0~15.5초 표본과3~7초 세부 표본, 이번4.0~5.5초 이동·감속 보완. 시나리오 없는 정상 경로 유지 |
| 추출물 | 최초66장/59고유시점 + 추가31장. 총97장/83고유시점. 재시험 복사본은 별도이며 독립 표본으로 세지 않음 |
| 기술 재시험 | 최초66장과 추가31장 각각 같은 조건 재추출에서 이미지 해시·시각·ordinal 동일. 원본 해시 동일. 정확도/일반화 성능 수치 아님 |
| 시간 | MP4 stts/ctts와 단일rate1 edit를 직접 읽어 디코드창 PTS와 대조. 추가331프레임 시간도 일치. 기존 R4-1 및 추가 모션 시간기록은 구조 검사 통과, 오차/내용 미확인 unresolved 유지 |
| 원본/환경 | 원본 영상·Word/PPT·Phase00 정본 수정 없음. SAR0/1은 미확인. 별도API/전사0건, AE·CU 연결 조작 없음 |

## 남은 미확인 범위

이번에 제시한 화면과 항목에 대해 사용자께 다시 확인받을 내용은 없다. 다만 음성/무음·AV동기, 장헌24초 이후·EG마지막약0.68초, 표본 사이의 변화, 정밀 좌표/SAR, 정확한 이징 곡선/원본 키프레임, 실제 사업·제품 사실, R4 통합 근거·공간 이관은 확인하지 않았다. 작은 예비 분석의 완료를 이 범위의 완료로 확대하지 않는다. 다른 동작도 같은 방식으로 모두 검수한 것은 아니다.

## 근거와 변경 이력

- [실제 사용자 회신과 확인 범위](../04_검증자료/01-A2_작은예비/사람확인_6묶음과_E모션보완_회신.json)
- [누락 원인·보완·남은 한계](../04_검증자료/01-A2_작은예비/후속검수_6묶음확인과_E모션보완.md)
- [추가31장 재시험](../04_검증자료/01-A2_작은예비/모션보완_재시험.json)
- [관측 초안 v0.3](../02_분석작업/01-A2_작은예비/관측초안.json)

중요 검수 기록은 루트 작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A2 아래에 보존했다. 변경 전 파일·실패·중간본은 backup에 있다. 최초 보고의 게시후 해시검증은 당시 복사본의 검증 이력이며, 이번 수정본은 별도의 게시 검증으로 구분한다. 새 PDF는 만들지 않았다. A3·기존 스킬 기본 전환·01-B·Phase02는 착수하지 않았다.
'''
    txt(f'{P}/05_결과보고/07_01-A2_작은예비분석_보고.md',report)
    status=read(f'{P}/00_진행안내/01-A_계획상태.json')
    status.update(version='0.5',state='A2_presented_content_confirmed_motion_omission_corrected',human_content_reviews_pending=0,human_content_reviews_pending_unit='only six presented screen-review groups; other scopes remain unreviewed',stage_A2_status='①~⑥ 한정 사람 내용 검수 완료. E조각 슬라이드·감속 누락 보완/재시험. 전체 영상·음성·정밀 곡선은 미확인',next_decision='한정 예비 검수 결과 보고. 후속 범위 별도 검토; A3 자동 착수 없음',human_content_review_record='04_검증자료/01-A2_작은예비/사람확인_6묶음과_E모션보완_회신.json',stage_A2_images=97,stage_A2_unique_times=83,stage_A2_primary_extraction_jobs=5,stage_A2_retest_extraction_jobs=5,stage_A2_motion_correction=True,human_confirmed_review_groups=6,full_runtime_validation_completed=False,redteam_execution_scope='A1 고정 합성 검토와 A2 자체 반대 관점 검토. 후속 사용자 정정으로 E 모션 누락 보완',A3_started=False)
    put(f'{P}/00_진행안내/01-A_계획상태.json',status)
    notice=read(f'{P}/00_진행안내/15_01-A2_실행결과_현재안내.json');notice.update(status=status['state'],primary_images=97,unique_sample_times=83,human_review_received='six presented review groups confirmed; user supplied E piecewise slide/deceleration correction',remaining_human_review=False,remaining_human_review_scope='none for presented six groups; other scopes explicitly unreviewed',motion_omission_corrected=True,latest_receipt=status['human_content_review_record'],latest_supplement=f'{VE}/후속검수_6묶음확인과_E모션보완.md',A3_started=False)
    put(f'{P}/00_진행안내/15_01-A2_실행결과_현재안내.json',notice)
    archived=[]
    for phase in ['motion_review','motion_review_retest']:
        for src in (BASE/'cases/자료013'/phase).iterdir():
            rel=f'{AN}/자료013/{phase}/{src.name}' if phase=='motion_review' else f'{BK}/재시험/자료013/{phase}/{src.name}'
            copy(src,rel);archived.append({'execution_path':str(src),'archive_path':str(ROOT/rel),'sha256':sha(src)})
    put(f'{VE}/모션보완_보존위치.json',archived)
    for name in ['E_진입_상세표본.jpg','변경범위.json']:copy(HERE/name,f'{VE}/모션보완/{name}')
    for src in HERE.glob('*.py'):copy(src,f'{BK}/실행코드/{src.name}')
    for name in ['run_motion_review_자료013.json','run_motion_review_retest_자료013.json']:copy(BASE/name,f'{BK}/실행로그/{name}')
    # Preserve the first diagnostic filename as an intermediate, not a delivered current record.
    for src in HERE.glob('E_*診断.json'):copy(src,f'{BK}/중간진단/{src.name}')
    for name,category in [('사람확인_6묶음과_E모션보완_회신.json','내용검수'),('사람검수_대기.json','내용검수'),('후속검수_6묶음확인과_E모션보완.md','보완과_재시험'),('모션보완_재시험.json','보완과_재시험'),('모션보완_R4-1_검사.json','기술검수'),('이징_용어출처.json','기술검수'),('E_가운데조각_경계진단.json','기술검수')]:copy(STAGE/VE/name,f'{IMP}/{category}/{name}')
    copy(HERE/'E_진입_상세표본.jpg',f'{IMP}/보완과_재시험/E_진입_상세표본.jpg')
    txt(f'{IMP}/내용검수/사람검수_화면안내/03_검수완료와_E모션정정.md','①~⑥은 사용자 직접 회신으로 확인 완료다. E는 색 변화뿐 아니라 조각별 좌→우 슬라이드와 감속 진입이다. 이 모션은 최초 분석에서 놓쳤고 사용자 설명 뒤 추가 추출/진단으로 보완했다. 기존 안내는 당시 질문 문맥으로 보존하며, 현재 상태는 ../사람확인_6묶음과_E모션보완_회신.json 및 ../../보완과_재시험/후속검수_6묶음확인과_E모션보완.md를 확인한다.\n')
    put(f'{VE}/모션보완_현재AI입력.json',{'separate_API_calls':0,'audio':False,'current_model_id':'host_not_exposed','contact_sheet':{'path':str(HERE/'E_진입_상세표본.jpg'),'sha256':sha(HERE/'E_진입_상세표본.jpg'),'source_size':[1920,1560],'tool_display_size':[1760,1430]},'individual_frames':[{'path':f['path'],'sha256':f['sha256']} for f in run['frames'] if F(f['actual_playback_seconds']) in {F('4.1'),F('4.4'),F('4.8')}],'meaning':'new AI verification after user correction, not prior detection; selected contact frames plus three full derived PNGs, not all31 individual images visually checked'})
    # Test summary and scope checks, not a single quality score.
    all_frame_keys=set()
    for aid in ['자료005','자료013']:
        for phase in ['initial','detail']+(['motion_review'] if aid=='자료013' else []):
            r=json.loads((BASE/'cases'/aid/phase/'실행기록.json').read_text(encoding='utf-8'))
            all_frame_keys.update((aid,F(f['actual_playback_seconds'])) for f in r['frames'])
    assert len(all_frame_keys)==83
    checks={'six_groups_recorded':receipt['confirmed_groups']==list(review_map),'verbatim_preserved':receipt['verbatim']==reply,'no_pending_presented_groups':read_staged(f'{VE}/사람검수_대기.json')['pending_claims']==[],'motion_omission_admitted':draft['motion_correction']['missed_in_initial_analysis'],'retest31':retest,'R4_time_valid':valid['valid'],'R4_time_unresolved_count':len(valid['unresolved']),'A3_not_started':not status['A3_started'],'no_exact_curve_claim':not receipt['correction']['exact_curve_or_AE_keyframes_confirmed'],'unique_frame_times':len(all_frame_keys),'original_video_hash_unchanged':sha(Path(json.loads((BASE/'입력고정과_컨테이너사전점검.json').read_text(encoding='utf-8'))[1]['path']))==run['input_sha256']}
    assert all(checks[k] for k in ['six_groups_recorded','verbatim_preserved','no_pending_presented_groups','motion_omission_admitted','R4_time_valid','A3_not_started','no_exact_curve_claim','original_video_hash_unchanged'])
    put(f'{VE}/후속회신_자체검수.json',checks)
    put(f'{BK}/게시전_보완기록.json',{'initial_dry_run_error':'unplanned_existing_change:重要검수기록 내용검수/사람검수_대기.json','actual_target':'내용검수/사람검수_대기.json','action':'added explicitly intended review queue copy to before-hash check and backup; no D write occurred on failed dry run','result':'re-audited exact before hash; no broad overwrite permission added'})
    manifest=[]
    for src in sorted(STAGE.rglob('*')):
        if src.is_file():manifest.append({'relative_path':src.relative_to(STAGE).as_posix(),'sha256':sha(src),'bytes':src.stat().st_size})
    write(HERE/'게시명세.json',{'expected_before':expected_before,'files':manifest})
    print(json.dumps({'files':len(manifest),'bytes':sum(x['bytes'] for x in manifest),'human_groups':6,'human_pending_presented':0,'R4_valid':valid['valid'],'R4_unresolved':len(valid['unresolved']),'retest':retest},ensure_ascii=False))
def read_staged(rel):return json.loads((STAGE/rel).read_text(encoding='utf-8'))
if __name__=='__main__':main()
