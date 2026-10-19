from pathlib import Path
from copy import deepcopy
import json,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def save(p,d):p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def main():
 inputs=load(OUT/'inputs.json');glyphs=load(OUT/'glyph-measurements.json')
 dims=['hierarchy','alignment','spacing','typography','color','background','shapes']
 for code,prefix in [('NEW-N','N'),('NEW-P','P')]:
  base=ROOT/'case-benchmarks-20261019/records'/code/'observations-linked.json';d=load(base)
  frames=[x for x in inputs['evidence'] if x['id'].startswith(prefix) and x['id']!='N175']
  a={'schema_version':'design-details-0.1','case_id':d['case_id'],'source':d['source'],
    'base_record':{'path':str(base),'sha256':sha(base)},'pattern_ids':sorted(set(x['pattern_id'] for x in d['pattern_refs'])),
    'scope':{'record_window_seconds':d['window_seconds'],'snapshot_seconds':[x['seconds'] for x in frames],
      'new_continuous_video_coverage':False,'content_status':'AI observed development candidate; user selected density/classification policy, not content approval',
      'limits':'기존 분석 창 안의 선택 정착/변화 화면을 보강. 전 프레임 디자인 검수·회사 표준 확정·음성 검수·재제작 성공을 뜻하지 않음.'},
    'frames':frames,'regions':[],'typography':[g for g in glyphs if g['frame'].startswith(prefix)],'relations':[],
    'dimensions':{},'layers':[],'unknowns':[],'implementation_hypotheses':[]}
  def region(ident,frame,box,desc,purpose,error=6):
   f=next(x for x in frames if x['id']==frame);w,h=f['canvas'];l,t,r,b=box
   a['regions'].append({'id':ident,'frame':frame,'bbox_ltrb':box,'precision':'estimated','basis_kind':'observed',
    'coordinate_system':'native decoded frame pixels, origin upper-left, half-open LTRB',
    'method':'manual boundary reading on native full frame and 1:1 crops; glow/soft edges excluded where practical','error_px':error,
    'description':desc,'reuse_reason':purpose,'normalized_xywh':[round(l/w,5),round(t/h,5),round((r-l)/w,5),round((b-t)/h,5)],
    'bbox_canvas_area_percent':round((r-l)*(b-t)/(w*h)*100,2)})
  def dim(k,desc):a['dimensions'][k]={'description':desc,'basis_kind':'observed','precision':'qualitative'}
  def relation(ident,refs,value,unit,method,error,meaning):
   a['relations'].append({'id':ident,'region_ids':refs,'value':value,'unit':unit,'basis_kind':'calculated','precision':'estimated',
    'method':method,'error':error,'meaning':meaning})
  if prefix=='N':
   region('header','N177',[0,60,1190,240],'좌상단 흰 HANMAC 로고 오각형/사선 접합과 남색→청색 리본. 아래 가는 밝은 선, 오른쪽 사선 끝.','장 제목 배치와 좌측 브랜딩 여백을 복원할 기준')
   region('long-model','N177',[940,185,3560,2030],'왼쪽 긴 거더의 투영 외접 범위. 앞 단면에서 오른쪽 위로 수렴하며 철근·바닥판·청록 강조가 겹침.','오른쪽 단면과의 시각 비중·사이 여백; 불규칙 3D의 실면적 아님',20)
   region('section-model','N177',[5030,720,6870,1540],'오른쪽 단면의 콘크리트 형상 범위. 주변 곡선 화살표는 포함하지 않음.','모델과 별도 화살표의 범위를 분리',15)
   region('section-arrows','N177',[5160,540,6740,1750],'오른쪽 단면 양옆의 녹색 곡선 화살표 묶음 범위.','형상 면에 붙는 청록 강조와 독립 외곽 동작을 혼동하지 않음',15)
   region('left-label','N177',[1334,253,2808,370],'어두운 청록 띠, 양끝 청록 세로선, 단일 행 흰 글자.','독립 TEXT 패턴의 현 장면 폭/패딩 변형',3)
   region('right-label','N177',[5226,253,6699,370],'왼쪽과 같은 틀의 설명 띠. 짧은 문구가 가운데에 놓임.','글자 길이가 달라도 같은 틀을 사용하는지 확인',4)
   region('caption','N177',[2455,1956,5228,2074],'하단 중앙 별도 진청 사각 자막판, 흰 본문과 어두운 그림자.','모델 영역/하단 안전 여백/가독성 관계',5)
   relation('model-balance',['long-model','section-model'],[34.1,24.0],'percent of canvas width','각 투영 외접 폭 / 7680 × 100','약 ±0.5 percentage points','왼쪽 긴 모델과 오른쪽 단면의 폭 비중. 외접 상자 면적을 실제 물체 면적으로 부르지 않는다.')
   relation('inter-model-gap',['long-model','section-model'],1470,'native px','오른쪽 단면 left5030 - 왼쪽 모델 right3560','약 ±35 px','177초 모델 외접 범위 사이 여백; 19.1%W. 광선/배경선이 없는 빈 픽셀 수가 아님.')
   relation('left-label-padding',['left-label'],[126,135],'native px','글자 bbox1460..2673와 띠1334..2808의 좌/우 차','약 ±5 px','문구와 양끝선 바깥 경계 사이 가시적 여백. 실제 AE text box padding 아님.')
   relation('right-label-padding',['right-label'],[240,244],'native px','글자 bbox5466..6455와 띠5226..6699의 좌/우 차','약 ±6 px','짧은 문구의 여백이 더 넓음. 두 라벨은 이 정착 화면에서 사실상 같은 폭.')
   relation('type-height-ratio',[],[1,1.29,1.31,1.59],'ratio to header visible glyph height','58/75/76/92px를58로 나눔','임계값 약 ±2 px/항목; 비율은 근사','제목/왼쪽 라벨/오른쪽 라벨/자막. 글자의 가시 높이이며 폰트 크기 원값 아님.')
   relation('caption-bottom',['caption'],86,'native px','2160 - 자막판 bottom2074','약 ±5 px','하단 여백 약4.0%H; 자막폭 약36.1%W.')
   dim('hierarchy','32:9. 좌상단 장 제목, 왼쪽 큰 사시도와 오른쪽 작은 정면 단면의 비교 구도. 두 설명 띠는 같은 y의 상단, 공통 자막은 하단 중앙. 제목이 가장 큰 글자라는 전제를 두지 않는다.')
   dim('alignment','177초 양 라벨은 y253..370으로 상단선이 맞는다. 오른쪽 단면과 설명 띠는 대략 중심을 공유한다. 왼쪽 모델은 원근 방향 때문에 라벨 중심과 기하 중심이 일치하지 않으며 이를 오류 정렬로 바꾸지 않는다.')
   dim('spacing','왼쪽 모델 외접 폭34.1%W, 오른쪽24.0%W, 두 모델 사이 약19.1%W의 투영 여백. 라벨은 각각 약19.2%W. 왼쪽 글자 좌우 여백126/135px, 오른쪽240/244px. 자막판 하단 여백86px. 배경 장식은 이 사이에도 존재한다.')
   dim('typography','흰 산세리프 한글. 가시 글자 높이는 제목58px, 왼쪽75px, 오른쪽76px, 자막92px(177초). 왼쪽 라벨의 “켄틸레버 바닥판”과 “동바리 역할 수행”이 굵게 보이고 “시공시”는 상대적으로 가늘다. 자막 앞 “켄틸레버 바닥판”도 뒤 문장보다 굵게 보인다. 서체명/포인트 크기/weight 수치는 미확정. 표기 켄틸레버·시공시/시공 시를 유지한다.')
   dim('color','남청/청색 기술 배경, 흰·회색 콘크리트/검은 내부 구멍, 흰 글자. 라벨과 모델 면·모서리는 청록, 오른쪽 외곽 화살표는 녹색 계열로 분리한다. 화면 색을 원본 색 토큰으로 확정하지 않는다.')
   dim('background','기저의 어두운 남청 그라데이션 위에 좌상단 점열, 좌하단 노드와 망, 하단~우측 곡선 다발과 청색 발광 교차점이 보인다. 라벨 아래로 배경/모델이 비치는 외관이 있으나 opacity 값은 미상. 앞 단계의 밝아짐과177초 배경 상태를 구분한다.')
   dim('shapes','로고 사선 흰 면+외곽선+청색 리본을 한 사각형으로 단순화하지 않는다. 라벨은 직각 띠+양끝 가는 수직선이며 둥근 카드가 아니다. CG는 날개/원형 정착부/중공/철근/판의 겹침을 보존한다. 녹색 화살표는 양쪽 곡선·화살촉, 청록 강조는 형상에 밀착한 모서리/면이다. 자막은 설명 띠와 다른 별도 사각판이다.')
   a['layers']=['배경 남청 기저','점·망·곡선·작은 발광점(상호 제작 레이어 순서는 미확정)','철근/슬래브/거더 모델의 가림 관계','모델 면·모서리 청록 강조와 바깥 녹색 화살표','설명 띠와 흰 문구, 상단 로고/리본','하단 자막판·흰 글자·어두운 그림자']
   a['unknowns']=['서체명·폰트 크기·행간·자간의 원본 값','양 라벨의 생성 중 폭 변화 함수는 같다고 확정하지 않음','정확 RGB/그라데이션 stop·투명도·광선 효과·원본 레이어 구조','앞/뒤 곡선 화살표의 정확 강도 곡선과 원본 동기화 설정(기존 열린 쟁점 유지)']
   a['implementation_hypotheses']=[{'basis_kind':'inferred','proposal':'두 라벨은 같은 정착 틀에 문구 길이와 굵기 구간을 바꿔 담는 템플릿 후보.','reason':'177초 가시 폭은1474/1473px로 차이가 오차 범위 안. 기존 TEXT-0002 번호 유지.','verification_needed':'다른 장면의 라벨 정착 폭과 긴 문구 대응·실제 재제작 확인'}]
  else:
   region('police-panel-outer','P47',[242,222,1120,616],'가는 밝은 외곽 사각선과 노랑 모서리 L자.','바깥 프레임/안쪽 판/행 폭의 독립 비율',3)
   region('police-panel-inner','P47',[266,245,1098,593],'지도가 비쳐 보이는 연두/노랑 판, 네 모서리 짧은 흰 표시.','외곽과 안쪽 판의 이격',3)
   region('police-card-outer','P47',[354,787,1006,1021],'가는 흰 사각선과 노랑 L자 모서리.','로고 카드와 설명 패널은 동일 폭이 아님',3)
   region('police-card-face','P47',[374,809,985,1001],'미색 밝은 면 위 독수리 문장·경찰청 한글·영문 로고.','로고는 개별 자막 폰트로 추정하지 않음',3)
   region('regional-panel-outer','P47',[1520,114,2324,616],'분홍 L자 모서리+가는 밝은 사각 외곽선.','기관별 패널 차이와 상태별 크기 구분',3)
   region('regional-panel-inner','P47',[1550,144,2294,586],'양옆 붉은 기운, 중앙 지도 투과 외관의 판.','실제 opacity와 외관 구분',3)
   region('regional-card-outer','P47',[1594,787,2246,1021],'가느다란 사각선+분홍 모서리.','카드 배치/여백/후속 이동 기준',3)
   region('regional-card-face','P47',[1614,809,2225,1001],'옅은 분홍 밝은 면과 강원특별자치도 로고.','설명 행의 한글 서체와 로고 아트워크 분리',3)
   region('regional-connector','P47',[1908,605,1934,790],'가는 밝은 테두리 안 붉은 위쪽 꺾쇠 무늬, 패널 아래 흰 원형 접점.','카드 위와 패널 아래의 연결 구조',3)
   region('regional-panel-outer-53','P53',[2822,190,3503,616],'오른쪽 재배치 후 패널 외접 범위.47초보다 폭·높이가 작다.','위치 이동에 포함된 하위 패널 크기 변화 보강',4)
   region('regional-card-outer-53','P53',[2834,787,3487,1021],'오른쪽 재배치 후 카드.47초와 크기가 유사하고 x위치가 달라짐.','전체 묶음의 일괄 축소라는 오해 방지',4)
   relation('panel-card-width-police',['police-panel-outer','police-card-outer'],1.35,'ratio','878 / 652','약 ±0.02','경찰 설명 외곽은 카드 외곽의 약1.35배. 밴드는 패널보다도 양옆으로 돌출.')
   relation('panel-card-width-regional',['regional-panel-outer','regional-card-outer'],1.23,'ratio','804 / 652','약 ±0.02','47초 강원 설명 외곽/카드 외곽.53초에는681/653≈1.04로 변함.')
   relation('panel-card-gap',['police-panel-outer','regional-panel-outer','regional-card-outer'],171,'native px','카드 외곽 top787 - 패널 외곽 bottom616','약 ±6 px','47초 두 묶음의 패널 바닥과 카드 윗선 간 간격이 유사. 연결선이 이 틈을 잇는다.')
   relation('panel-inner-inset',['regional-panel-outer','regional-panel-inner'],[30,30,30,30],'native px, left/top/right/bottom','안쪽 판 bbox - 바깥 프레임 bbox 차','약 ±6 px','강원 외곽과 안쪽 판이 약30px 이격. 경찰은24/23/22/23px로 다름.')
   relation('panel-state-resize',['regional-panel-outer','regional-panel-outer-53'],[0.847,0.849],'width ratio / height ratio','681/804,426/502','약 ±0.02','47→53초 패널은 약85% 폭·높이. 카드 외곽 폭652→653px,높이234→234px로 유사. 전체 묶음을 단일 scale로 설명하면 누락.')
   relation('regional-x-shift',['regional-card-outer','regional-card-outer-53'],1240.5,'native px','카드 외곽 중심3160.5 - 1920','약 ±7 px','화면폭 약32.3%의 오른쪽 이동. 두 시점의 차이이며 정확 이동곡선 아님.')
   relation('regional-type-police-comparison',[],[34,42,46,36,36],'visible glyph height px','경찰 두 행34/34;강원47초42/46;강원53초36/36;선택 글자 ROI 임계값','약 ±2 px/항목','색 강조뿐 아니라 문구의 가시 크기·굵은 외관도 상태별로 다름. font-size/weight 키프레임 확정 아님.')
   dim('hierarchy','16:9 위성 지도와 횡성 청록 강조가 위치 맥락을 만들고 기관 카드→세로 연결선→두 정책 행의 묶음이 상단에 놓인다. 하단 검은 자막판은 별도층. 경찰청 왼쪽, 강원 중앙 등장 후 오른쪽으로 이동하여 중앙 자리를 비운다.')
   dim('alignment','패널 바닥 원형 접점·세로 연결선·카드 중심이 각 기관 묶음의 축이다.47초 경찰은x약681,강원은x약1921.두 기관 패널의 바닥y616과 카드 외곽y787..1021은 맞고,패널 상단은경찰222/강원114로 다르다. 억지로 같은 높이 패널로 통일하지 않는다.')
   dim('spacing','47초 경찰 패널폭878px(22.9%W),강원804px(20.9%W),기관 카드 외곽폭652px(17.0%W).패널-카드 간격171px(7.9%H).강원 안쪽 판은 외곽보다 각방향 약30px 안쪽.53초 강원 패널681×426px로 작아지나 카드653×234px는 유사.한 정착 수치로 전 구간을 대표하지 않는다.')
   dim('typography','정책 문구는 흰 산세리프.경찰 두 행의 선택 글자 가시 높이34px.47초 강원 첫행42px,둘째46px이며 둘째가 굵게 보임.53초 두 행은36px로 유사하고 가는 외관.이는 프레임/행 크기 변화와 강조 상태를 함께 보아야 하며 font-size/weight 원값은 미확정.기관 로고와 지도 지명은 정책 글자와 별도 아트워크/정보 역할.')
   dim('color','경찰 노랑/연두,강원 붉은색/분홍,카드 밝은 미색/분홍,지도 어두운 녹갈색·남청 바다,횡성은청록.상태별 강조가 띠/글자 외관에 영향을 준다.밝은 카드 면만 단색 흰 사각형으로 기록하지 않는다.')
   dim('background','지형 질감·해안·행정 경계·회색 지명과 검은 외곽 효과가 보이고 횡성만 청록 채움과 밝은 경계/흰 지명으로 강조.정책 패널의 중앙은 지명이 비쳐 보이며 양옆으로 기관색이 짙어진다.밝은 카드면은 지도 대비가 강하고,하단 자막판은 별도의 어두운 바탕이다.실제 투명도 값/블렌드/그라데이션 stop은 미상.')
   dim('shapes','정책 묶음은 바깥 가는 밝은 사각선+색 L자 모서리,안쪽 비치는 판+짧은 흰 모서리 표시,그 위 양끝 뾰족한 가로 띠 두 행+바깥 분리 꺾쇠/빛나는 윤곽으로 구성된다.기관 카드는 밝은 사각 면·가는 외곽선·색 모서리·로고로 분리.연결선은 밝은 가는 양옆선+색 꺾쇠 무늬+패널 바닥의 겹친 흰 원형 접점.보이는 선 두께는 대략 가는 외곽1~3px/색 모서리4~6px이나 발광 포함 범위에 따라 달라 원본 stroke로 확정하지 않음.')
   a['layers']=['위성 지도·바다 질감','행정 경계·회색 지명과 횡성 청록 영역/흰 지명','반투명 외관의 기관색 패널·안/밖 선틀','양끝 돌출 정책 띠·바깥 꺾쇠·흰 문구와 강조','세로 연결선·화살 무늬·원형 접점,밝은 기관 카드·외곽 모서리·로고','하단 어두운 자막판과 시간에 따라 드러나는 글자']
   a['unknowns']=['원본 폰트명·크기·굵기·자간과 로고 소스','원본 opacity/stroke/glow/gradient 설정과 레이어 순서','51.5~53초 패널 크기 변화의 정확 시작·속도곡선·앵커(두 시점 차이는 관측됨);카드와 다른 변환임을 후속 정밀 표본으로 분리할 것']
   a['implementation_hypotheses']=[{'basis_kind':'inferred','proposal':'기관 카드/정책 패널/연결선을 독립 조절하되 묶음 위치를 함께 이동시키는 편집 구조 후보.','reason':'53초 카드 크기는47초와 유사하지만 정책 패널은약85%크기.기존LAYOUT-0003/FLOW-0003/DETAIL-0006과 차이 항목으로 연결하며 새번호를 만들지 않음.','verification_needed':'크기 변화 타이밍·중간상태와 편집 가능한 재제작 결과 대조'}]
  assert set(a['dimensions'])==set(dims)
  dest=OUT/'records'/code/'design-details.json';save(dest,a)
  d['skill_version']='0.1.0-draft.9'
  d['method']+=' 이번 판은 기존 근거·번호를 보존한 디자인 기록 보강본. 별도 design_details에 원본 크기 측정/추정,상태별 차이와 미확정을 연결.'
  d['design_details']={'path':str(dest),'sha256':sha(dest)}
  d['record_lineage']={'base_path':str(base),'base_sha256':sha(base),'change':'design enrichment; prior immutable pattern definitions remain pinned'}
  d['limitations'].extend(a['unknowns'])
  for s in d['layout']['states']:
   for k in dims:
    s['design_spec'][k]['description']=s['design_spec'][k]['description'].replace('다른 길이/폭이다','문구 길이는 다르며177초 정착 띠 폭은 측정상 유사하다')
    s['design_spec'][k]['description']+=' 보강: '+a['dimensions'][k]['description']+' 수치의 기준 시점은 design_details의 frame별 항목에 한정.'
  # Add precise new claims without rewriting historical assertions or immutable pattern sources.
  def claim(obj,prop,facet,dimension,span,statement,basis,eids):
   ident='c'+str(max(int(x['id'][1:]) for x in d['claims'])+1).zfill(3)
   d['claims'].append({'id':ident,'object_id':obj,'property':prop,'facet':facet,'dimension':dimension,'time_seconds':span,'statement':statement,'basis_kind':basis,'evidence_ids':eids,'content_review':'supported'})
   d['review']['content_reviewed_claim_ids'].append(ident)
   row=next(r for r in d['observation_rows'] if r['object_id']==obj and r['property']==prop)
   row['claim_ids'].append(ident)
   row['evidence_ids']=list(dict.fromkeys(row['evidence_ids']+eids))
   for p in d['pattern_refs']:
    if obj in p['object_ids']:
     p['current_claim_ids'].append(ident)
     p['differences'].append('디자인 보강 '+ident+': '+statement)
   for s in d['layout']['states']:
    if obj in s['element_object_ids']:
     s['claim_ids'].append(ident)
     for spec in s['design_spec'].values():
      if ident not in spec['claim_ids']:spec['claim_ids'].append(ident)
   return ident
  if prefix=='P':
   new=claim('regional-frame','size','value','panel-versus-card-state-size',[47,53],
    '47초와53초 원본 크기 외곽을 비교하면 정책 패널은 약804×502px→681×426px(약85%), 기관 카드는 약652×234px→653×234px로 유사하다. 오른쪽 이동에 하위 패널 크기 변화가 함께 있다. 경계 수동 추정 오차 약3~4px. 정확한 시작·속도곡선·AE설정은 미확인.','calculated',['f14','b124'])
   d['review']['remaining_scope'].append('새 발견: 정책 패널은 카드와 달리47→53초 약85%크기로 변함.크기 변화의 정확 시간·가감속은 아직 미확인.')
   d['unknowns'].append({'id':'u04','object_id':'regional-frame','question':'패널 크기 변화의 정확 시작·중간 속도·정착은 언제인가?','state':'open','reason':'47/53초 외접 크기 차이를 새로 확인했으나 정확한 변화 궤적을 정밀 검수하지 않음.','required_basis_kind':'observed','next_probe':'51~53초 기존0.1초 표본에서 패널 외곽과 카드 크기를 따로 추적하고 필요시 연속 프레임 보강.','resolution_claim_ids':[]})
   d['layout']['unresolved_ids'].append('u04')
   d['layout']['states'][-1]['unresolved_ids'].append('u04')
   if d['handoff'] is not None:d['handoff']['open_unknown_ids'].append('u04')
   d['reuse_map'].setdefault('design_enrichment_note','패턴 ID·항목 해시 유지. DETAIL-0006/FLOW-0003의 위치 관측은 유효하나 강체 이동만이라는 설명은 부족하며 하위 패널 크기 차이를 새 주장으로 보강.')
  else:
   ids=[e['id'] for e in d['evidence'] if e.get('actual_seconds')=='177' and 'crop_xyxy' not in e]
   claim('left-label','size','value','settled-label-width-comparison',[177,177.001],'177초 양 설명 띠의 가시 폭은 약1474/1473px로 수동 경계 오차3~4px 안에서 유사하다.문구 길이·글자 좌우 여백은 다르다. 이전의 길이/폭 차이라는 요약은 생성중/문구 길이와 정착 띠 폭을 구분해 읽어야 한다.','calculated',ids[:1])
  save(OUT/'records'/code/'observations.json',d)
 print('two addenda and new observation revisions written; IDs retained')
if __name__=='__main__':main()
