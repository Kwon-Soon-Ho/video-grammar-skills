"""AI-authored observations from actually viewed K-GEO frames; development, not blind grading."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(HERE/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import check
from evidence_catalog import catalog
PROPS={'identity','text','relation','position','size','shape','visibility','color','internal_state'}
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
source=D/'한맥 영상/K-GEO FESTA 1핵심 홍보동영상/K-GEO FESTA_250919_3.mp4'
class Case:
    def __init__(self,name,start,end):
        self.name=name;self.start=start;self.end=end;self.folder=HERE/'runs'/name;self.folder.mkdir(parents=True,exist_ok=True)
        self.log=WORK/f'phase01a-a5b/cases/A5-K/{name}/실행기록.json'
        self.catalog=catalog([self.log]);(self.folder/'catalog.json').write_text(json.dumps(self.catalog,ensure_ascii=False,indent=2),encoding='utf-8')
        self.ev=[];self.lookup={}
        for i,f in enumerate(self.catalog['frames']):
            e={'id':f'f{i:02d}','path':f['path'],'actual_seconds':f['actual_playback_seconds'],'role':'context_after' if F(f['actual_playback_seconds'])>=end else 'within'};self.ev.append(e);self.lookup[F(f['actual_playback_seconds'])]=e['id']
        self.d={'schema_version':'video-observation-0.3','skill_version':'0.1.0-draft.5','case_id':'DEV-KGEO-'+name+'-20261019','source':{'path':str(source),'sha256':self.catalog['frames'][0]['source_sha256']},'window_seconds':[start,end],'method':'기존 base native 프레임의 전체 개요 시트를 시간순·역순으로 보고 26.2/31.4초 또는 66/72.8초 native를 세부 재대조한 실제 개발 분석. 과거 기준답안 준비 노출 이력 있음. 독립 비교·전 프레임 관찰 아님.','document_mode':'none','audio_reviewed':False,'files_read':[str(self.log)],'evidence':self.ev,'objects':[],'observation_rows':[],'claims':[],'unknowns':[],'discovery':{'forward_evidence_ids':[e['id'] for e in self.ev],'reverse_evidence_ids':[e['id'] for e in reversed(self.ev)],'unresolved_ids':[]},'layout':{},'motion_groups':[],'pattern_refs':[],'reuse_map':None,'review':{},'handoff':None,'limitations':['기존 추출 표본을 실제 열람한 AI 개발 실행. 새 홀드아웃·독립 채점 아님.','오디오·시나리오 대응·원본 AE 값은 미검수.','전체 디자인 기술을 원자 주장 분모에 모두 편입하는 전수 검수는 미완료.','세계 좌표 비행과 화면상 움직임은 다르며 카메라·가림·영상 전환 영향을 분리한다.']};self.active={}
    def refs(self,*times):return [self.lookup[F(str(t))] for t in times]
    def target(self,oid,name,shape,props,active,anchor,parent=None):
        self.active[oid]=active
        obj={'id':oid,'name':name,'parent':parent,'shape_description':shape,'required_properties':['identity',*props],'excluded_properties':{p:'독립 변화 분석 대상 아님; 정성 디자인은 전체 레이아웃에 기록하며 미상 수치를 의미하지 않음' for p in PROPS-{'identity',*props}},'identity':{'status':'reviewed','label':name,'candidates':[],'claim_ids':[]}}
        self.d['objects'].append(obj);cid=self.claim(oid,'identity','identity','visible-form',name+'의 보이는 형태를 식별한다.',[anchor]);obj['identity']['claim_ids']=[cid]
    def claim(self,oid,prop,facet,dimension,text,times,span=None):
        cid=f'c{len(self.d["claims"])+1:03d}'
        self.d['claims'].append({'id':cid,'object_id':oid,'property':prop,'facet':facet,'dimension':dimension,'time_seconds':span or self.active[oid],'statement':text,'basis_kind':'observed','evidence_ids':self.refs(*times),'content_review':'supported'});return cid
    def unknown(self,oid,question):
        uid=f'u{len(self.d["unknowns"])+1:02d}';self.d['unknowns'].append({'id':uid,'object_id':oid,'question':question,'state':'open','reason':'현재 표본 또는 개발 검수 범위만으로 확정하지 않음','required_basis_kind':'observed','next_probe':'해당 원본 ROI·구간 표본을 먼저 보강하고 같은 대상의 전후를 비교','resolution_claim_ids':[]});return uid
    def layout(self,states,spec):
        self.d['layout']={'canvas':{'aspect_ratio':'16:9','coordinate_system':'3840x2160 native raster; 정성 관계, 정확 픽셀 미측정'},'states':[],'unresolved_ids':[u['id'] for u in self.d['unknowns']]}
        for sid,span,oids,anchor,description in states:
            cids=[c['id'] for c in self.d['claims'] if c['object_id'] in oids]
            self.d['layout']['states'].append({'id':sid,'time_seconds':span,'element_object_ids':oids,'evidence_ids':self.refs(anchor),'composition':description,'claim_ids':cids,'unresolved_ids':[u['id'] for u in self.d['unknowns']],'design_spec':{k:{'description':v,'basis_kind':'observed','precision':'qualitative','claim_ids':cids} for k,v in spec.items()}})
    def finish(self,flow,details):
        for o in self.d['objects']:
            a,b=self.active[o['id']]
            for prop in o['required_properties']:
                cids=[c['id'] for c in self.d['claims'] if c['object_id']==o['id'] and c['property']==prop];assert cids,(o['id'],prop)
                for suffix,span in [('before',[self.start,a]),('after',[b,self.end])]:
                    if span[0]<span[1]:self.d['observation_rows'].append({'id':o['id']+'-'+prop+'-'+suffix,'object_id':o['id'],'property':prop,'time_seconds':span,'review_state':'not_applicable','change':'not_applicable','evidence_ids':[],'claim_ids':[],'unknown_ids':[],'reason':'대상이 이 상태에서는 아직 나타나지 않았거나 화면에서 사라진 범위. 경계는 표본으로 정한 개발 구간.'})
                refs=sorted({e for c in self.d['claims'] if c['id'] in cids for e in c['evidence_ids']})
                self.d['observation_rows'].append({'id':o['id']+'-'+prop,'object_id':o['id'],'property':prop,'time_seconds':[a,b],'review_state':'reviewed','change':'unchanged' if prop=='identity' else 'changed' if prop in ('visibility','position','size','internal_state') else 'unchanged','evidence_ids':refs,'claim_ids':cids,'unknown_ids':[],'reason':''})
        self.d['motion_groups']=[{'id':'flow','level':'flow','name':flow,'time_seconds':[self.start,self.end],'object_ids':[o['id'] for o in self.d['objects']],'claim_ids':[c['id'] for c in self.d['claims'] if c['property'] in ('visibility','position','size')],'pattern_occurrence_ids':[]},{'id':'detail','level':'detail','name':details,'time_seconds':[self.start,self.end],'object_ids':[o['id'] for o in self.d['objects']],'claim_ids':[c['id'] for c in self.d['claims'] if c['property'] not in ('identity',)],'pattern_occurrence_ids':[]}]
        self.d['review']={'content_reviewed_claim_ids':[c['id'] for c in self.d['claims']],'claim_denominator_complete':False,'remaining_scope':['지원 판정은 이 실행의 AI 재대조 상태이며 사람 정답 아님. 미세 모션·정확 수치·고유 주장 전수 분모는 미완료.']}
        path=self.folder/'first-observations.json';path.write_text(json.dumps(self.d,ensure_ascii=False,indent=2),encoding='utf-8')
        errors=check(self.d,self.catalog);(self.folder/'first-validation.json').write_text(json.dumps({'candidate':'draft.5','structure_errors':errors,'content_truth_verified_by_code':False},ensure_ascii=False,indent=2),encoding='utf-8')
        return path,errors

h=Case('H03',25,35)
h.target('header','좌상단 파란 섹션 표제','흰 외곽의 청색 사선 리본과 흰 글씨',['text','visibility'],[25,35],26.2)
h.claim('header','text','value','section-before','데이터 분석 방법 표제.',[26.2],[25,29.8]);h.claim('header','text','value','section-after','데이터 취득 방법 소개 표제로 바뀐다.',[31.4],[29.8,35]);h.claim('header','visibility','order','section-transition','29.4~30.2초 사이 표제 내용이 전환되며 중첩 표본이 있다.',[29.4,29.8,30.2])
h.target('receivers','수신기 이미지 세 개','위쪽에 세 장비 사진/렌더와 각각의 이름표',['text','visibility'],[25,30.2],26.2)
for i,label in enumerate(['수신기 1','수신기 2','수신기 3(저가형)'],1):h.claim('receivers','text','value',f'label-{i}',label+' 이름표.',[26.2])
h.claim('receivers','visibility','direction','exit','비교 화면이 29.8초 표본에서 흐려지고 지도 화면과 겹친 뒤 교체된다.',[29.4,29.8,30.2])
h.target('table','하단 GNSS 장비 비교표','회색/청록/파랑 머리글과 표 셀',['text','color','visibility'],[25,30.2],26.2)
for dim,text in [('drone-model','드론 모델명은 Matrice 300 RTK.'),('drone-accuracy','드론 RTK 포지셔닝 정확도는 1cm + 1ppm.'),('receiver1-accuracy','수신기 1 정확도는 0.6cm+0.5ppm.'),('receiver2-accuracy','수신기 2 정확도는 1cm+1ppm.'),('receiver3-accuracy','수신기 3(저가형) 정확도는 1cm+1ppm.')]:h.claim('table','text','value',dim,text,[26.2])
h.claim('table','color','value','column-style','드론 열은 청록 계열이고 수신기 열은 연한 파랑 계열이며 일부 수치·수신기3 문구는 주황으로 강조된다.',[26.2]);h.claim('table','visibility','direction','crossfade','비교표가 29.8초의 새 지도와 중첩되며 약해진 뒤 보이지 않게 된다.',[29.4,29.8,30.2])
h.target('highlight','수신기 3의 주황 외곽 강조','오른쪽 검정 장비 둘레의 주황 선',['visibility'],[25,30.2],26.2,'receivers');h.claim('highlight','visibility','direction','emphasis','25초에는 약하거나 보이지 않던 강조가 25.4초 이후 표본에서 나타나 수신기 3을 두른다.',[25,25.4,26.2])
h.target('left-panel','왼쪽 세로 운동장 패널','흰 둥근 테두리의 긴 운동장 사진',['visibility','size'],[29.8,35],31.4)
h.claim('left-panel','visibility','direction','enter','29.8초 작은 지도 패널이 비교 화면 위에 겹쳐 나타나 30.2초 이후 두 패널 화면이 된다.',[29.8,30.2,31.4]);h.claim('left-panel','size','direction','growth','전환 중 작게 보이는 왼쪽 패널이 커져 세로 패널로 정착한다. 정확 곡선 미상.',[29.8,30.2,30.6])
h.target('right-panel','오른쪽 넓은 운동장 지도 패널','흰 둥근 테두리의 비스듬한 넓은 사진',['visibility','size','text'],[29.8,35],31.4)
h.claim('right-panel','visibility','direction','enter','29.8초의 작은 오른쪽 지도 패널이 나타나 넓은 오른쪽 화면으로 전환된다.',[29.8,30.2,31.4]);h.claim('right-panel','size','direction','growth','전환 중 오른쪽 패널의 보이는 크기가 커져 정착한다. 정확 보간은 미확정.',[29.8,30.2,30.6]);h.claim('right-panel','text','value','waypoints','WP 1~WP 5 문구가 보라색 핀 근처에 표시된다.',[31.4])
h.target('left-route','왼쪽 패널의 노란 경로와 보라색 핀','운동장 위 고정 경로선과 다섯 핀',['shape'],[29.8,35],31.4,'left-panel');h.claim('left-route','shape','value','route-shape','아래와 좌우를 잇는 노란 선 및 상단의 꺾인 선과 보라색 핀 다섯 개가 보인다.',[31.4])
h.target('left-marker','왼쪽 패널의 드론 표시','흰/보라색 작은 드론 그림',['position'],[29.8,35],31.4,'left-panel');h.claim('left-marker','position','direction','panel-relative','왼쪽 패널 내부 드론 표시가 상단 오른쪽 쪽에서 오른쪽 경로를 따라 화면 아래쪽으로 옮겨 간다.',[30.6,31.4,32.6,34.6])
h.target('right-route','오른쪽 패널의 경로와 핀','사진 위 노란 경로와 보라색 핀',['shape'],[29.8,35],31.4,'right-panel');h.claim('right-route','shape','value','route-shape','비스듬한 사진 위에 노란 선과 보라색 핀들이 고정 기준으로 배치된다.',[31.4])
h.target('right-marker','오른쪽 패널의 드론 표시','경로 위 작은 드론 그림',['position'],[29.8,35],31.4,'right-panel');h.claim('right-marker','position','direction','panel-relative','오른쪽 패널에서도 경로에 대한 드론 그림 위치가 표본마다 변한다. 정확 방문 순서는 미확정.',[30.6,31.4,33,34.6])
h.target('caption','아래쪽 비행 조건 문구','흰 반투명 바탕의 짧은 문구 묶음',['text','visibility'],[31.4,35],32.6)
for dim,text in [('caption-title','드론 비행 경로.'),('height','비행고도: 50m.'),('speed','비행속도: 2m/s.')]:h.claim('caption','text','value',dim,text,[32.6])
h.claim('caption','visibility','direction','enter','31.4초에는 옅은 문구/바가 시작되고 뒤 표본에서 비행 조건이 읽히게 된다.',[31.4,31.8,32.6])
h.unknown('right-marker','두 지도 드론 표시의 정확 방문 순서·속도·회전은 무엇인가?');h.unknown('left-panel','패널 성장·전환의 정확 시작/끝·가감속은 무엇인가?');h.unknown('table','정확한 글꼴·색·좌표 수치와 원고 대응은 무엇인가?')
h.layout([('comparison',[25,30.2],['header','receivers','table','highlight'],26.2,'상단 수신기 세 개와 하단 비교표가 같은 열 관계를 이룬다.'),('maps',[29.8,35],['header','left-panel','right-panel','left-route','left-marker','right-route','right-marker','caption'],31.4,'왼쪽 좁은 세로 패널과 오른쪽 넓은 패널을 병렬로 배치한다.')],{'hierarchy':'좌상단 섹션 표제, 주 콘텐츠, 하단 표/조건 문구를 구분.','alignment':'수신기 이미지/이름표/표 열을 대응시키고 지도 패널은 위·아래 변을 대체로 맞춘다.','spacing':'상하 여백을 둔 비교 화면에서 작은 패널 간격을 둔 두 지도 화면으로 바뀐다.','typography':'한글 산세리프, 비교표와 이름표는 짙은 글자, 섹션 제목은 흰 글자. 정확 서체·크기 미상.','color':'밝은 회청 배경, 청색/청록 머리글, 주황 강조, 지도 위 노랑 경로·보라 핀.','background':'연한 회청 단색 계열 배경 위 사진·표·지도 패널.','shapes':'사선 리본 표제, 둥근 표, 사각 장비 이름표, 둥근 모서리 지도 패널과 핀.'})
p,e=h.finish('수신기 비교·강조 → 겹치는 화면 교체 → 두 지도와 드론 표시 이동·조건 문구','주황 외곽 강조, 두 패널 크기 변화, 패널 내부 드론 위치, 하단 문구 출현')
print(json.dumps({'case':'H03','claims':len(h.d['claims']),'first_errors':e},ensure_ascii=False))

h=Case('H04',66,76)
h.target('header','좌상단 비행 단계 표제','파란 사선 리본과 흰 문구',['text','visibility'],[66,76],66)
h.claim('header','text','value','section-before','드론 비행 시험 진행 표제.',[66],[66,67.6]);h.claim('header','text','value','section-after','드론 비행 시험 종료 표제로 바뀐다.',[72.8],[67.6,76]);h.claim('header','visibility','order','replacement','67.2~68초 사이 표제가 약해지고 새 문구로 교체되는 표본이 보인다.',[67.2,67.6,68])
h.target('footage','하늘·운동장 실사 화면','하늘과 구름, 후반 운동장·수목·건물 배경',['internal_state'],[66,76],72.8);h.claim('footage','internal_state','value','shot-change','하늘 위주 화면에서 운동장과 지면이 더 보이고 71.2~71.6초 사이 드론이 훨씬 크게 보이는 다른 구도로 바뀐다.',[66,70.8,71.2,71.6,72.8])
h.target('real-drone','실사 드론','하늘의 검은 멀티로터 드론',['position','size','visibility'],[66,76],72.8)
h.claim('real-drone','position','direction','screen-relative','구간 후반 화면에서 드론이 지면 쪽으로 낮아져 보인다. 화면 이동만으로 세계 좌표의 정확 궤적을 복원하지 않는다.',[72.8,74,75.6]);h.claim('real-drone','size','value','shot-boundary','71.2초와 71.6초 사이 보이는 드론 크기가 크게 바뀌며 연속 스케일 애니메이션으로 단정하지 않는다.',[71.2,71.6,72.8]);h.claim('real-drone','visibility','presence','visible','선택 표본에서 드론은 계속 보이며 76초 경계에서도 보인다. 바닥 접촉 완료는 확인하지 않는다.',[66,72.8,75.6,76])
h.target('mini-panel','우상단 경로 인셋','흰 둥근 테두리의 작은 세로 운동장 지도',['position','size'],[66,76],66)
h.claim('mini-panel','position','value','anchor','작은 경로 패널이 우상단에 고정된 배치로 유지된다.',[66,72.8,75.6]);h.claim('mini-panel','size','value','container-size','인셋의 외곽 크기는 선택 전후 표본에서 대체로 유지된다. 정확 측정은 안 했다.',[66,72.8,75.6])
h.target('mini-route','인셋의 노란 경로와 핀','지도 안 노란 선과 보라 핀',['shape'],[66,76],66,'mini-panel');h.claim('mini-route','shape','value','route-shape','다섯 보라 핀과 노란 경로가 내부 이동의 고정 기준으로 보인다.',[66,72.8])
h.target('mini-marker','인셋의 드론 표시','노란 경로 위 흰/보라색 작은 드론 그림',['position'],[66,76],66,'mini-panel');h.claim('mini-marker','position','direction','panel-relative','인셋 외곽은 고정돼도 내부 드론 표시 위치는 표본에 따라 경로 위에서 달라진다. 전체 정확 방문 순서·속도는 미확정.',[66,68,70.8,72.8,75.6])
h.target('caption','하단 비행 단계 문구','흰 반투명 가로 바탕과 짙은 글씨',['text','visibility'],[66,76],66)
h.claim('caption','text','value','caption-before','하단 문구는 경로 비행이다.',[66],[66,67.6]);h.claim('caption','text','value','caption-after','후반 하단 문구는 착륙이다.',[72.8],[67.6,76]);h.claim('caption','visibility','order','replacement','67초대 표본에서 경로 비행이 약해지고 착륙 문구로 바뀐다.',[66.8,67.2,67.6,68])
h.target('person','후반 왼쪽 아래의 사람','검은 옷을 입고 장비를 든 사람',['visibility'],[73.2,76],75.6);h.claim('person','visibility','presence','entry','후반 지면 구도에서 왼쪽 아래에 사람이 보인다. 정확 첫 등장 시점은 표본 간 범위다.',[73.2,74,75.6])
h.unknown('mini-marker','인셋 드론의 전체 방문 순서·속도·회전은 무엇인가?');h.unknown('real-drone','실제 착지 완료 시점·고도·세계 좌표 궤적은 무엇인가?');h.unknown('header','문구 교체의 정확 경계·리빌 방식과 오디오 대응은 무엇인가?')
h.layout([('flight',[66,73.2],['header','footage','real-drone','mini-panel','mini-route','mini-marker','caption'],66,'실사 배경 전체 위에 좌상단 제목, 우상단 경로 인셋, 하단 단계 문구를 겹친다.'),('landing',[73.2,76],['header','footage','real-drone','mini-panel','mini-route','mini-marker','caption','person'],75.6,'운동장과 사람이 보이는 실사 위에서 제목·경로 인셋·착륙 문구 배치를 유지한다.')],{'hierarchy':'실사 드론이 주 대상이며 섹션 제목·경로 인셋·하단 단계 문구가 보조한다.','alignment':'표제는 좌상단, 경로는 우상단, 단계 문구는 아래 중앙에 배치한다.','spacing':'실사 중앙을 가리지 않도록 보조 요소를 모서리와 아래에 둔다.','typography':'흰 한글 섹션 표제와 밝은 바탕 위의 짙은 단계 문구. 정확 서체·크기 미상.','color':'청색 리본·흰 경계·노란 경로·보라 핀을 실사의 청회색 하늘·녹색 지면에 겹친다.','background':'하늘·드론·운동장 실사, 중간에 구도 전환.','shapes':'사선 리본, 둥근 세로 인셋, 반투명 하단 바, 경로선·핀과 드론 표시.'})
p,e=h.finish('경로 비행 → 표제/문구 교체 → 실사 구도 전환 → 지면 쪽 드론과 착륙 문구','우상단 인셋 내부 이동과 외곽 고정 분리, 문구 교체, 구도 전환에 의한 크기 변화')
print(json.dumps({'case':'H04','claims':len(h.d['claims']),'first_errors':e},ensure_ascii=False))
