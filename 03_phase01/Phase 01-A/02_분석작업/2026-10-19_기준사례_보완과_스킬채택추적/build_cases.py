from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
SCRIPTS=WORK/'internal-video-audit-20261019/candidate/company-video-grammar-analyzer/scripts';sys.path.insert(0,str(SCRIPTS))
from check_record import check,PROPERTIES
from evidence_catalog import catalog
from render_observations import render
def load(p):return json.loads(Path(p).read_text('utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
logs=[]
for root in [WORK/'analysis-reliability-20261019/fresh/cases',WORK/'internal-video-audit-20261019/source-overview/cases',HERE/'extraction/cases']:
 for p in root.rglob('실행기록.json'):
  if load(p).get('complete_target_selection'):logs.append(p)
oldcat=load(WORK/'internal-video-audit-20261019/evidence-catalog.json');crops=[]
for e in oldcat['frames']:
 if 'crop_xyxy_native_pixels' in e:
  item={k:e[k] for k in ['path','parent_path','crop_xyxy_native_pixels']}
  if item not in crops:crops.append(item)
for p in (HERE/'inspection').glob('*crop-inputs.json'):crops+=load(p)
cat=catalog(logs,crops);write(HERE/'evidence-catalog.json',cat)
all_frames={}
for e in cat['frames']:
 if 'crop_xyxy_native_pixels' not in e:
  all_frames.setdefault(e['source_sha256'],{}).setdefault(F(e['actual_playback_seconds']),e)
for code,window in [('NEW-N',[166,181]),('NEW-P',[40,53])]:
 old=WORK/'internal-video-audit-20261019/records'/code/'observations.json';d=load(old);d['case_id']='DEV-'+code+'-REFERENCE-20261019';d['window_seconds']=window
 # Past observations remain immutable at their original path. This is a larger, new case.
 for r in d['observation_rows']:r['time_seconds']=window[:]
 for s in d['layout']['states']:s['time_seconds']=window[:]
 for g in d['motion_groups']:g['time_seconds']=window[:]
 for e in d['evidence']:
  t=F(e['actual_seconds']);e['role']='within' if window[0]<=t<window[1] else 'context_before' if t<window[0] else 'context_after'
 ef={F(e['actual_playback_seconds']):e for e in all_frames[d['source']['sha256']].values()}
 def ev(t):
  t=F(str(t));f=ef[t]
  found=next((e for e in d['evidence'] if Path(e['path']).resolve()==Path(f['path']).resolve()),None)
  if found:return found['id']
  eid='b'+str(len(d['evidence'])).zfill(3);d['evidence'].append({'id':eid,'path':f['path'],'actual_seconds':str(t),'role':'within' if window[0]<=t<window[1] else 'context_before' if t<window[0] else 'context_after'});return eid
 def addprop(obj,prop):
  o=next(x for x in d['objects'] if x['id']==obj)
  if prop not in o['required_properties']:o['required_properties'].append(prop);o['excluded_properties'].pop(prop)
 def claim(cid,obj,prop,dim,text,ts,span=None,kind='observed',facet='value',easing=None):
  addprop(obj,prop);es=[ev(t) for t in ts];c={'id':cid,'object_id':obj,'property':prop,'facet':facet,'dimension':dim,'time_seconds':span or window[:],'statement':text,'basis_kind':kind,'evidence_ids':es,'content_review':'supported'}
  if easing:c['easing']={'classification':easing,'basis_evidence_ids':es,'method':text,'limitation':'영상에서 보이는 속성의 변화율. 원본 AE 보간 함수·키프레임·Influence·물리량 복원 아님.'}
  d['claims'].append(c);return cid
 def obj(oid,name,shape,props,identity_cid):
  d['objects'].append({'id':oid,'name':name,'parent':None,'shape_description':shape,'required_properties':props,'excluded_properties':{p:'이 객체의 현재 관측 목적에서는 독립 요구 속성이 아님. 재사용 시 해당 목적에서 다시 검토.' for p in PROPERTIES-set(props)},'identity':{'status':'reviewed','label':name,'candidates':[],'claim_ids':[identity_cid]}})
 if code=='NEW-N':
  claim('c035','background','internal_state','sampled-background-geometry','좌측 점·망, 오른쪽 여백, 오른쪽 하단 곡선/빛 교차점의 원본 ROI를 대조했다. 166~180초의 선택 표본에서 무늬 위치와 교차점은 유지되어 보이고, 도입의 밝아짐 이후 독립적인 빛 이동·흐름은 확인되지 않는다. 전체 픽셀의 연속 무변화나 원본 레이어 독립성을 뜻하지 않는다.',[166,167,168,169,170,172,174,176,178,180])
  claim('c036','background','color','rgb-signal','좌측 고정 ROI(0,300~500,1400)의 평균 RGB는 166초 약(9.2,16.4,27.3), 168초(14.3,23.2,37.1), 169.5초(15.5,25.0,39.6). 이후 180초까지 큰 반복 밝기 파형은 보이지 않는다. 8bit 디코딩 RGB의 영역 평균이며 레이어 opacity 값이 아니다.',[166,168,169.5,180],kind='calculated')
  claim('c037','front-arcs','visibility','one-envelope-not-cycle','전면 화살표는 168.5초에 뚜렷하지 않고 169초 옅은 상태, 169.5~170초 선명한 상태로 들어가 173초까지 유지된 뒤 173.5초 약화, 174초에는 보이지 않는다. 이 범위에서 확인한 것은 한 번의 등장·유지·소실이며 주기적 점멸을 확인한 것이 아니다. 먼 끝도 비슷한 시간 범위에 생겼다 사라지지만 오른쪽 단면의 곡선은 이후에도 남는다.',[168.5,169,169.5,170,173,173.5,174],span=[168.5,174])
  claim('c038','girder','position','projected-aperture-angle','앞 단면 검은 구멍 상단의 화면 투영 경사를 1/5 크기 ROI에서 추적했다. 약170.6초 +17.8도, 171.5초 -6.3도, 172.4초 +17.9도로 방향이 왕복하고 173.2초 약+6.1도로 돌아온다. 두 양의 극값 간 약1.8초(0.1초 표본 기반 대략±0.2초). 실제 3D 회전각·반복 루프 주기가 아니며 패치의 선형 적합 오차 약0.25px은 전체 측정 오차를 뜻하지 않는다.',[170.6,171.5,172.4,173.2],span=[169.5,173.5],kind='calculated')
  claim('c039','girder','position','projected-sway-easing','투영 경사 170.6→170.7→170.8→170.9→171.0→171.1초는 +17.82→+16.87→+14.00→+10.40→+6.17→+1.71도, 이후171.3→171.4→171.5초는 -5.04→-6.20→-6.34도로 극점 부근 변화량이 작아진다. 같은 투영 방향의 반주기에서 시작은 느리고 중간은 빠르며 끝이 느려지는 성격이다. 각도 자체는 화면상 관측량이고 AE 커브 복원 아님.',[170.6,170.7,170.8,170.9,171,171.1,171.3,171.4,171.5],span=[170.6,171.5],kind='calculated',facet='easing',easing='in_out')
  next(c for c in d['claims'] if c['id']=='c028')['content_review']='rejected'
  claim('c040','left-label','text','verified-copy','완성 문구의 화면 표기는 “켄틸레버 바닥판 시공시 동바리 역할 수행”이다. 기술 용어의 통상 표기로 고치지 않고 원본 표기를 기록한다. 이전 c028의 “캔틸레버” 판독은 기각한다.',[174,174.6,175],span=[173,181])
  claim('c041','left-label','visibility','complete-reveal','173초 중앙 세로선, 173.2초 가까운 두 선, 173.4초 넓어진 빈 띠, 173.6~173.8초 부분 문구, 174초 전체 문구가 읽히는 상태, 174.8~175초 선 간격 정착으로 이어진다. 글자가 읽히는 시점과 외곽 폭이 정착하는 시점은 다르다. 180초에도 문구는 남는다.',[173,173.2,173.4,173.6,173.8,174,174.8,175,180],span=[173,181])
  claim('c042','left-label','size','bar-separation-easing','청록 세로선 간격은 173.0/173.2/173.4/173.6/173.8/174.0/174.2/174.4/174.6/174.8초에 약21/53/242/733/1087/1272/1377/1435/1465/1473px이다. 같은 0.2초에서 증가량은32→189→491→354→185→105→58→30→8px이므로 초반 가속·후반 감속 성격을 확인한다. 174.8~175초에는 간격이 약1473px로 유지된다. 색 임계값 기반 외곽 추정 오차 약±3px, AE 폭/마스크 원값 아님.',[173,173.2,173.4,173.6,173.8,174,174.2,174.4,174.6,174.8,175],span=[173,175],kind='calculated',facet='easing',easing='in_out')
  claim('c043','left-label','size','settled-bar-geometry','175초 청록선의 좌우 바깥 추정 x는1334/2807px, 간격 약1473px이다. native ROI(1000,230~3300,380)의 청록 세로열>35픽셀 검출. 이는 선 간격이며 텍스트 레이어 폭과 다르다.',[175],span=[173,181],kind='calculated')
  claim('c044','deck','position','second-assembly','174.5~175.5초에는 추가 흰 판들이 위쪽에 떨어져 보이다가 아래로 내려오며 연결되고 176초에는 더 넓은 연속 상부 판으로 정리된다. 앞서167초 부근의 조립과 같은 시각 사건으로 합치지 않는다.',[174.5,175,175.5,176],span=[174,176.5])
  obj('edge-highlight','거더 외곽·날개를 따르는 청록 강조','좌측 거더 상부 길이와 옆 날개에 밀착한 청록 윤곽·빛 면',['identity','visibility','color'],'c045')
  claim('c045','edge-highlight','identity','visible-form','거더 가장자리와 돌출 날개를 따라 별도로 생기는 청록 테두리·빛 면. 전면의 원호 화살표와 구분한다.',[177],span=[176,179])
  next(c for c in d['claims'] if c['id']=='c045')['facet']='identity'
  claim('c046','edge-highlight','visibility','envelope','176초에는 강한 청록 외곽이 뚜렷하지 않고176.5~178초에 보이며178.5초 약해진 뒤179초에는 강한 강조가 보이지 않는다. 직전 구조 조립의 완료와 겹쳐 등장한다.',[176,176.5,177,178,178.5,179],span=[176,179])
  claim('c047','edge-highlight','color','appearance','흰/회색 원래 구조 위에 청록·밝은 푸른 외곽과 넓은 반투명 밝은 면이 더해진다. 발광/색 혼합 효과의 외관이며 특정 Glow 효과나 알파 값은 미확정이다.',[177,178],span=[176,179])
  obj('top-slab','마감되는 넓은 상부 판','상부 철근 판 위를 넓게 덮는 밝은 회백색 연속 면',['identity','position','visibility'],'c048')
  claim('c048','top-slab','identity','visible-form','179.5초 이후 상부에 새로 들어오는 넓고 연속적인 밝은 판. 기존 분할 철근 판과 구분한다.',[179.5,180,180.5],span=[179,181])
  next(c for c in d['claims'] if c['id']=='c048')['facet']='identity'
  claim('c049','top-slab','position','assembly','179.5초 위쪽의 넓은 판이 보이고180초 겹치며 내려온 상태,180.5초 상부를 연속 면으로 덮은 상태다. 실제 시공 순서의 기술적 정확성은 검증하지 않았다.',[179.5,180,180.5],span=[179,181])
  claim('c050','top-slab','visibility','occlusion','180~180.5초 마감 판이 상부의 철근·분할선을 가린다. 181초 문맥 표본에도 넓은 상부 면이 보인다. 기존 판이 없어졌다는 사실로 바꾸지 않는다.',[180,180.5,181],span=[179,181])
  claim('c051','section-arcs','visibility','longer-hold','오른쪽 단면의 곡선은173~174초 약해진 뒤174~180초에도 녹색 원호로 남아 있다. 좌측 전면·먼 끝 곡선의174초 소실과 같은 퇴장으로 묶지 않는다.',[173,174,175,178,180],span=[173,181])
  claim('c052','section','position','settled-after-tilt','단면은 앞 구간의 기울기 변화 이후174/176/178/180초에 유사한 정면 구도로 유지된다. 원본 회전각/중심축은 복원하지 않았다.',[174,176,178,180],span=[174,181])
  claim('c053','caption','text','third-caption','174~180초의 다음 자막은 “켄틸레버 바닥판 시공 시 동바리 역할도 수행하는 다목적 부재입니다.”로 읽힌다. 위쪽 설명 띠의 문구·띄어쓰기와 별도로 보존한다.',[174.5,175,180],span=[174,181])
  claim('c054','caption','visibility','late-caption-hold','새 자막은174.5/175/180초에 유지된다. 181.2초 이후의 다른 장면 겹침과182초의 다음 자막은 분석 창 밖 문맥이다.',[174.5,175,180],span=[174,181])
  claim('c055','right-label','visibility','late-hold','오른쪽 설명과 양끝 세로선은175/178/180초에도 유지된다. 새 왼쪽 설명이 생겨도 기존 오른쪽 설명을 대체하지 않는다.',[175,178,180],span=[174,181])
  for u in d['unknowns']:
   if u['id']=='u01':u.update(state='resolved',reason='세 배경 ROI에서 밝기 변화와 무늬 위치 유사를 추가 확인. 원본 레이어 독립성/정확 속성은 범위 한계로 보존.',resolution_claim_ids=['c035'],next_probe='')
   if u['id']=='u03':u.update(state='resolved',reason='창 뒤 구간에서 완성 문구·폭 정착·가감속을 별도 확인. c028 문자 판독도 정정.',resolution_claim_ids=['c040','c041'],next_probe='')
   if u['id']=='u02':u.update(reason='한 번의 화살표 포락선과 별도의 거더 왕복 기울임, 좌측/오른쪽 강조 유지 차이를 확인했다. 정확한 화살표 강도 곡선·원본 동기화 설정까지는 미확정.',next_probe='필요한 재사용 정밀도에 따라 움직이는 화살표의 자세 변화와 밝기를 분리 추적하거나 원본 프로젝트에서 강도/동기화 설정 확인')
  row_changes={'deck-internal_state':'changed','background-internal_state':'unchanged','left-label-visibility':'changed','left-label-size':'changed'}
  composition='32:9 전체 배경 위에 왼쪽 길이 방향 CG, 오른쪽 단면 CG, 좌상단 로고 리본, 각 도해 위 설명, 중앙 하단 공통 자막을 배치한다. 후반 상부 판 조립·청록 외곽 강조·마감 판을 순차 추가하며 오른쪽 단면과 설명은 유지한다.'
  flow=[('초기 구도와 판 조립','166~168.5',['c006','c007','c009']),('단면·오른쪽 설명과 회전 강조','167.3~174',['c017','c024','c025','c037','c038','c051']),('왼쪽 설명과 두 번째 조립','173~176',['c040','c041','c042','c044']),('외곽 강조와 상부 마감','176~181',['c046','c049','c050','c053','c055'])]
 else:
  for ob in ['gangwon','gangwon-face','regional-frame','regional-row1','regional-row2']:addprop(ob,'position')
  claim('c044','map','size','late-fixed-anchors','48초와49/50/51/52/53초의 지도 남서·남동, 경찰청 카드의 같은 native ROI를 비교했을 때 픽셀 RGB 절대차 평균이 모두0이었다. 이 고정 기준점 범위에서 지도와 기존 카드의 이동/축소는 보이지 않고, 오른쪽 기관 묶음만 옆으로 이동한다. 실제 카메라 리그는 미확정.',[48,49,50,51,52,53],span=[48,53],kind='calculated')
  claim('c045','policy-panel','color','no-observed-repeated-pulse','40초 전후의 잔여 밝기 변화 뒤40.5~51초 선택 표본의 기존 노란 두 행은 유사한 상태다. 새 분홍 행의 강조와 동시 점멸한다고 볼 근거가 없고, 이 구간에서 반복 강조 주기를 확인하지 못했다.',[40,40.5,41,43,45,47,49,51],span=[40,51])
  claim('c046','regional-row1','color','single-emphasis-window','첫 분홍 행은43.5초 이후 더 밝아져44~46초 선명하고46.5~47.5초 어두운 붉은 상태로 돌아간다. 검사 구간에서 확인한 것은 한 번의 강조이며 반복 주기나 노란 행과의 동기화를 주장하지 않는다.',[43.5,44,45,46,46.5,47,47.5,49,51],span=[43.5,51])
  claim('c047','regional-row2','color','second-emphasis-window','두 번째 행은46.5초 이후 글자가 드러나47.5~50초 밝은 강조 상태,50.5~51초 어두워지는 상태다. 첫 행의 약화와 두 번째 행의 진입이46.5~47.5초에 겹친다. 단순 교대 점멸 루프로 확정하지 않는다.',[46.5,47,47.5,48,49,50,50.5,51],span=[46.5,51])
  claim('c048','regional-link','internal_state','fill-versus-flow','42.4~42.6초 ROI에서 유색 세로 무늬가 뚜렷하지 않고42.7초 카드 위에 작은 부분이 보인다. 42.8~43.5초 유색 무늬가 차오르는 위쪽 경계가 올라가고, 위 원형 접점은 같은 부근에서 더 크게/선명하게 나타난다. 43.8~45.3초에는 무늬 위치가 유지된다. 생성 중의 노출 영역 성장과 정착 뒤 반복 무늬 이동을 구분한다.',[42.4,42.6,42.7,42.8,43,43.2,43.4,43.5,43.8,44,45.3],span=[42.4,45.3])
  claim('c049','regional-link','internal_state','filled-edge-acceleration','고정 native ROI(1908,605~1933,790)에서 분홍 픽셀의 위 경계 y는42.8/43.0/43.2/43.4초에772/748/704/642px로 검출된다. 같은0.2초 동안 위쪽 진행량24→44→62px로 생성 전반의 가속 성격이 보인다. 43.5초 무렵 경계는약618px에 이른다. 무늬 임계값 때문에 수 px 오차가 가능하며 실제 글리프 이동속도나 정확 감속 함수가 아니다.',[42.8,43,43.2,43.4,43.5],span=[42.8,43.5],kind='calculated',facet='easing',easing='accelerate')
  for cid,ob in [('c050','regional-link'),('c051','gangwon'),('c052','gangwon-face'),('c053','regional-frame'),('c054','regional-row1'),('c055','regional-row2')]:
   claim(cid,ob,'position','group-reposition','51.5초에는 기존 중앙 배치,52초에는 오른쪽으로 옮겨가는 중,52.5~53초에는 오른쪽 배치로 보인다. 연결선·카드 면/로고·두 문구·설명 프레임이 함께 이동하며 기존 경찰청과 지도 기준점은 유지된다. 이 대상의 개별 재등장이나 무늬 흐름으로 바꾸지 않는다.',[51.5,52,52.5,53],span=[51.5,53])
  claim('c056','caption','text','late-copy-hold','48.5~53초에도 “전기차, 자율주행차 등 첨단산업의 활성화를 추진하고 있습니다”가 유지된다.54~55초의 새 기관·새 자막은 다음 문맥으로 분리한다.',[48.5,50,52,53],span=[48,53])
  claim('c057','police','visibility','left-anchor-hold','기존 경찰청 카드와 노란 설명 묶음은49/51/52/53초에 왼쪽 자리를 유지한다. 이동하는 분홍 기관 묶음과 구분된다.',[49,51,52,53],span=[48,53])
  claim('c058','regional-link','visibility','continues-past-window','연결선은52~53초 기관 묶음의 일부로 옮겨가며 유지된다. 이번 창에서는 최종 퇴장을 관측하지 않았다.79초 문맥에서는 카드/설명 프레임 없이 기관 로고 배치가 보이지만 그 사이의 전환 과정을 조사한 것은 아니다.',[52,53],span=[51.5,53])
  for u in d['unknowns']:
   if u['id']=='u02':u.update(state='resolved',reason='생성 시 위쪽 노출 영역 성장과 정착 뒤 무늬 위치, 이후 묶음 이동을 분리 확인. 최종 퇴장과 원본 구현은 범위 밖 미확인.',resolution_claim_ids=['c048','c050','c058'],next_probe='')
   if u['id']=='u03':u.update(state='resolved',reason='한 번의 행별 강조 순서와 기존 노란 행의 유사 상태를 대조. 반복 주기라는 전제를 채택하지 않음.',resolution_claim_ids=['c045'],next_probe='')
  d['observation_rows']=[r for r in d['observation_rows'] if r['id'] not in ['regional-link-position-before','regional-link-position-after']]
  row_changes={'regional-link-internal_state':'changed','regional-link-position':'changed'}
  composition='16:9 어두운 위성 지도와 지명·지역 경계 위에 횡성 청록 강조를 두고, 기관 카드→세로 연결선→두 행 설명 프레임을 묶는다. 노란 기존 경찰청은 왼쪽에 유지하고 분홍 강원 묶음을 중앙에 추가한 뒤51.5~53초 오른쪽으로 재배치해 중앙 여백을 만든다. 아래 검은 자막은 별도 정보층이다.'
  flow=[('기존 기관과 지역 맥락 유지','40~41.3',['c008','c014','c041','c045']),('로고→밝은 면→설명/연결선','41.4~44.5',['c017','c039','c040','c019','c048','c049']),('행별 등장과 강조 이관','43.5~51',['c023','c027','c046','c047']),('기관 묶음 재배치','51.5~53',['c044','c050','c051','c052','c053','c054','c055'])]
 # Explicitly reconcile every property row with the current claim set, preserving rejected claims as history.
 oldrows={(r['object_id'],r['property']):r for r in d['observation_rows']}
 d['observation_rows']=[]
 for o in d['objects']:
  for prop in o['required_properties']:
   cs=[c for c in d['claims'] if c['object_id']==o['id'] and c['property']==prop]
   oldrow=oldrows.get((o['id'],prop),{});uid=[u['id'] for u in d['unknowns'] if u['state']=='open' and u['object_id']==o['id']]
   state='unresolved' if uid and prop=='visibility' else 'reviewed'
   change=row_changes.get(o['id']+'-'+prop,oldrow.get('change','changed' if prop in ['position','visibility','size','color'] else 'unchanged'))
   if o['id'] in ['gangwon','gangwon-face','regional-frame','regional-row1','regional-row2'] and prop=='position':change='changed'
   d['observation_rows'].append({'id':o['id']+'-'+prop,'object_id':o['id'],'property':prop,'time_seconds':window[:],'review_state':state,'change':change,'evidence_ids':list(dict.fromkeys(e for c in cs for e in c['evidence_ids'])),'claim_ids':[c['id'] for c in cs],'unknown_ids':uid,'reason':'이 사례의 전후 표본과 속성별 주장에 근거. identity는 대상 식별이며 매 순간의 가시성·연속 정지를 뜻하지 않음. 기각 주장은 이력이며 현재 결론으로 쓰지 않음.'})
  assert all(c['evidence_ids'] for c in cs)
 openids=[u['id'] for u in d['unknowns'] if u['state']=='open']
 supported=[c['id'] for c in d['claims'] if c['content_review']=='supported']
 s=d['layout']['states'][0];s.update(composition=composition,element_object_ids=[o['id'] for o in d['objects']],claim_ids=supported,unresolved_ids=openids,evidence_ids=[ev(175 if code=='NEW-N' else 47)])
 s['design_spec']['alignment']['description']+='  후속 배치/기준점·모션 변화는 새 주장에 별도 연결.'
 s['design_spec']['spacing']['description']+='  노듈러 설명선의 정착 간격 또는 PG 기관 재배치의 여백 변화를 관측 기록과 구분.'
 for spec in s['design_spec'].values():spec['claim_ids']=supported
 d['layout']['unresolved_ids']=openids
 d['discovery']['unresolved_ids']=openids
 d['motion_groups']=[{'id':'flow','level':'flow','name':composition,'time_seconds':window,'object_ids':[o['id'] for o in d['objects']],'claim_ids':list(dict.fromkeys(c for _,_,cs in flow for c in cs)),'pattern_occurrence_ids':[]},{'id':'detail','level':'detail','name':'대상별 가시성·내부 변화·가감속·기울임·유지와 재배치','time_seconds':window,'object_ids':[o['id'] for o in d['objects']],'claim_ids':[c['id'] for c in d['claims'] if c['content_review']=='supported' and c['property'] not in ['identity','text']],'pattern_occurrence_ids':[]}]
 d['review'].update(content_reviewed_claim_ids=[c['id'] for c in d['claims']],claim_denominator_complete=False,remaining_scope=['동일 AI 후속 검수이며 독립 정답·회사 승인·원본 전체 미발견 항목의 분모 검토 아님.','선택 표본/특정 경계 연속프레임/ROI/수치 보조. 모든 프레임의 native 전체 화면 검수 아님.','열린 관측 쟁점: '+str(openids)])
 d['method']='원본·기존 draft.8 관측을 보존하고 새 범위로 작성한 기준 사례 후보. 기존0.1초 표본 재사용, 새 전후 구간과 PG 연결선 생성의 연속36프레임 보강. 원본 크기 ROI, 경사/선 간격/유색 경계의 변화율과 전체 구도 대조. 같은 AI 문맥의 개발 관측이며 독립 평가·최종 정답 아님.'
 d['limitations']=['영상 표기 그대로 읽으며 기술적 용어/홍보 내용의 사실성은 검증하지 않음.','원본 글꼴명·AE 레이어 구조·효과 종류·키프레임·Influence·3D 축/각도는 미확정. 화면 투영/색 임계값의 관측량과 구분.','원본 전체 정밀 분석 아님. 정지/주기 없음은 확인한 구간·표본의 범위에 한정.','범위 밖 전후 문맥은 분석 창 시간으로 집계하지 않음.','초기 사례 초안이며 새 문구/화면비로 편집·재제작·렌더 검증한 패턴은 아님.']
 d['files_read'] += [str(HERE/'decision.json'),str(HERE/'inspection/phase-measurements.json'),str(HERE/'inspection/pose-geometry.json')]
 d['handoff']=None;d['pattern_refs']=[];d['reuse_map']=None
 errors=check(d,cat);assert not errors,(code,errors)
 dest=HERE/'records'/code/'observations.json';write(dest,d);dest.with_suffix('.md').write_text(render(d),encoding='utf-8')
 write(dest.parent/'flow-stages.json',[{'name':n,'timing':t,'claim_ids':cs} for n,t,cs in flow])
 print(json.dumps({'case':code,'objects':len(d['objects']),'claims':len(d['claims']),'open_ids':openids,'window':window},ensure_ascii=False),flush=True)
