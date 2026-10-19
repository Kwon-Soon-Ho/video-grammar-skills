"""AI-authored corrections grounded in the explicitly inspected source samples."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import json,sys
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(HERE/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import load,check,digest,PROPERTIES
from evidence_catalog import catalog
from render_observations import render
from review_ledger import validate
def save(p,d):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists(),p
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')

class Revision:
    def __init__(self,name):
        self.name=name;self.out=HERE/'cases-r3'/name;self.out.mkdir(parents=True,exist_ok=True)
        self.before=WORK/'analyzer-realuse-20261019/runs'/name/'observations.json'
        self.d=deepcopy(load(self.before));self.d['skill_version']='0.1.0-draft.7'
        logs=[WORK/'phase01a-a5b/cases/A5-K'/name/'실행기록.json']
        if name=='H04':logs.append(WORK/'phase01a-a5b/cases/A5-K/REF-H04/실행기록.json')
        crops=[c for c in load(HERE/'crop-inputs.json') if '/'+name+'/' in c['parent_path'].replace('\\','/')]
        self.cat=catalog(logs,crops);save(self.out/'catalog.json',self.cat)
        existing={str(Path(e['path']).resolve()).casefold():e for e in self.d['evidence']}
        for f in self.cat['frames']:
            key=str(Path(f['path']).resolve()).casefold()
            if key in existing:continue
            t=F(f['actual_playback_seconds']);a,b=self.d['window_seconds']
            e={'id':f'x{len(self.d["evidence"]):03d}','path':f['path'],'actual_seconds':str(t),'role':'context_before' if t<a else 'context_after' if t>=b else 'within'}
            self.d['evidence'].append(e);existing[key]=e
        self.ev={F(e['actual_seconds']):e['id'] for e in self.d['evidence'] if Path(e['path']).parent.name in (name,'REF-H04')}
        self.claims={c['id']:c for c in self.d['claims']};self.newids=[];self.findings=[]
        self.d['method']+=' 이번 보완은 2026-10-19 동일 AI 문맥의 개발 재검토. 전체 개요와 명시한 native/픽셀 동일 ROI를 재관찰하고, 이미 노출된 지적의 보완을 추적했다. 독립 검수나 새 홀드아웃 아님.'
        self.d['files_read']+= [str(p) for p in logs if str(p) not in self.d['files_read']]
        self.d['limitations']+=['이번 지적 보완은 동일 문맥의 AI 재관찰이며, 미발견 대상·전체 프레임·의미 정확도 전수 검증을 입증하지 않는다.','원형 빛·강조의 정확 주기·파형·실제 구현은 미확정.','지원 주장과 같은 구간이라도 선택 표본 사이의 모든 프레임을 확인했다는 뜻은 아니다.']
    def refs(self,*times):return [self.ev[F(str(t))] for t in times]
    def change(self,cid,text,times,**extra):
        c=self.claims[cid];c.update(statement=text,evidence_ids=self.refs(*times),**extra);return cid
    def add(self,oid,prop,facet,dim,text,times,span=None):
        cid=f'c{max(int(c["id"][1:]) for c in self.d["claims"])+1:03d}'
        c={'id':cid,'object_id':oid,'property':prop,'facet':facet,'dimension':dim,'time_seconds':span or self.d['window_seconds'],'statement':text,'basis_kind':'observed','evidence_ids':self.refs(*times),'content_review':'supported'}
        self.d['claims'].append(c);self.claims[cid]=c;self.newids.append(cid);return cid
    def prop(self,oid,prop):
        obj=next(o for o in self.d['objects'] if o['id']==oid)
        if prop not in obj['required_properties']:obj['required_properties'].append(prop);obj['excluded_properties'].pop(prop,None)
    def unknown(self,oid,q,reason):
        uid='u'+str(max([int(u['id'][1:]) for u in self.d['unknowns']]+[0])+1).zfill(2)
        self.d['unknowns'].append({'id':uid,'object_id':oid,'question':q,'state':'open','reason':reason,'required_basis_kind':'observed','next_probe':'결과를 사용하는 목적에 맞춰 해당 ROI의 시간 표본 또는 원본 프로젝트를 확인','resolution_claim_ids':[]});return uid
    def target(self,oid,name,shape,props,parent,anchor,span):
        self.d['objects'].append({'id':oid,'name':name,'parent':parent,'shape_description':shape,'required_properties':['identity',*props],'excluded_properties':{p:'이번에 독립 변화가 확인된 속성 범위에 해당하지 않음. 미확인 변화를 없다고 판정한 것은 아님.' for p in PROPERTIES-{'identity',*props}},'identity':{'status':'reviewed','label':name,'candidates':[],'claim_ids':[]}})
        cid=self.add(oid,'identity','identity','visible-form',shape,[anchor],span)
        self.d['objects'][-1]['identity']['claim_ids']=[cid];return cid
    def finding(self,fid,q,before,resolved):
        selected=[self.claims[c] for c in resolved]
        req=list({(c['object_id'],c['property'],c['dimension']) for c in selected})
        self.findings.append({'id':fid,'question':q,'requirements':[dict(zip(('object_id','property','dimension'),r)) for r in sorted(req)],'required_basis_kind':'observed','before_claim_ids':before,'state':'addressed','resolution_claim_ids':resolved,'reason':'명시한 native 또는 픽셀 동일 ROI와 개요 시트를 재대조해 해당 관측을 추가·변경함. 자동 진실성 검증·독립 평가 아님.','next_probe':None})
    def rows(self):
        # Preserve the original scope rows. Rebuild each positive row's claim union.
        for obj in self.d['objects']:
            for prop in obj['required_properties']:
                cs=[c for c in self.d['claims'] if c['object_id']==obj['id'] and c['property']==prop]
                old=[r for r in self.d['observation_rows'] if r['object_id']==obj['id'] and r['property']==prop]
                if old:
                    for r in old:
                        if r['review_state']!='reviewed':continue
                        r['claim_ids']=[c['id'] for c in cs if r['time_seconds'][0]<=c['time_seconds'][0]<=c['time_seconds'][1]<=r['time_seconds'][1]]
                        r['evidence_ids']=sorted({e for c in cs if c['id'] in r['claim_ids'] for e in c['evidence_ids']})
                        if any(c['facet'] in ('direction','order') for c in cs):r['change']='changed'
                else:
                    a=min(c['time_seconds'][0] for c in cs);b=max(c['time_seconds'][1] for c in cs)
                    if a>self.d['window_seconds'][0]:
                        uid=self.unknown(obj['id'],'새 대상의 앞 구간 존재·상태는 무엇인가?','작게 보이거나 해당 요소가 아직 등장하지 않은 범위를 구분해 재검토해야 함')
                        self.d['observation_rows'].append({'id':obj['id']+'-'+prop+'-before','object_id':obj['id'],'property':prop,'time_seconds':[self.d['window_seconds'][0],a],'review_state':'unresolved','change':'unknown','evidence_ids':self.refs(self.d['window_seconds'][0]),'claim_ids':[],'unknown_ids':[uid],'reason':'이 앞 구간을 부재로 확정하지 않음'})
                    self.d['observation_rows'].append({'id':obj['id']+'-'+prop,'object_id':obj['id'],'property':prop,'time_seconds':[a,b],'review_state':'reviewed','change':'changed' if prop in ('size','color','visibility') else 'unchanged','evidence_ids':sorted({e for c in cs for e in c['evidence_ids']}),'claim_ids':[c['id'] for c in cs],'unknown_ids':[],'reason':'직접 대조한 표본의 관측. 표본 사이 전 프레임 확인을 뜻하지 않음'})
                    if b<self.d['window_seconds'][1]:
                        self.d['observation_rows'].append({'id':obj['id']+'-'+prop+'-after','object_id':obj['id'],'property':prop,'time_seconds':[b,self.d['window_seconds'][1]],'review_state':'not_applicable','change':'not_applicable','evidence_ids':[],'claim_ids':[],'unknown_ids':[],'reason':'원래 관찰 대상이 화면에서 교체된 이후 구간. 기존 대상의 출현 범위를 그대로 보존함.'})
        # Attach newly discovered objects to the complete case and detail motion, preserving scope.
        for state in self.d['layout']['states']:
            for obj in self.d['objects']:
                if obj['id'] not in ('mini-halo','red-light','left-halo'):continue
                if obj['parent'] in state['element_object_ids']:
                    state['element_object_ids'].append(obj['id'])
                    state['claim_ids']+= [c['id'] for c in self.d['claims'] if c['object_id']==obj['id']]
        detail=self.d['motion_groups'][1]
        detail['object_ids']=[o['id'] for o in self.d['objects']]
        detail['claim_ids']=[c['id'] for c in self.d['claims'] if c['property']!='identity']
        self.d['review']['content_reviewed_claim_ids']=[c['id'] for c in self.d['claims']]
        self.d['review']['claim_denominator_complete']=False
        self.d['review']['remaining_scope']+=['등록 지적의 보완 연결만 확인. 새 자료의 누락률·독립 정밀도·회사 승인 미확인.']
    def finish(self):
        self.rows();errors=check(self.d,self.cat);assert not errors,(self.name,errors)
        target=self.out/'observations-reviewed.json';save(target,self.d)
        (self.out/'observations-reviewed.md').write_text(render(self.d),encoding='utf-8')
        ledger={'schema_version':'video-review-ledger-0.1','revision':1,'before':{'path':str(self.before),'sha256':digest(self.before)},'after':{'path':str(target),'sha256':digest(target)},'reviewer':{'kind':'same_agent_context','name':'Codex development review','method':'기존 노출 자료·지적을 알고 native와 픽셀 동일 ROI 재관찰. 독립 평가 아님.'},'findings':self.findings}
        save(self.out/'review-ledger.json',ledger);result=validate(ledger,self.cat);save(self.out/'validation.json',result)
        print(json.dumps({'case':self.name,'claims':len(self.d['claims']),**result},ensure_ascii=False))

r=Revision('H03')
r.change('c019','수신기 3 주황 외곽은 나타난 뒤 단순 유지되지 않는다. 25.4초의 넓고 옅은 주변 띠, 26.2초의 상대적으로 얇은 강조, 27.0·27.4초의 다시 넓어진 밝은 띠, 28.2초의 약한 주변 띠로 강약·범위가 반복 변화한다. 정확 주기·파형은 미확정.',[25.4,26.2,27,27.4,28.2])
r.prop('receivers','color');c40=r.add('receivers','color','value','receiver3-label-emphasis','수신기 3 이름표 글자는 25.4초 갈색에 가까운 주황에서 26.2·27.4초 밝은 주황으로 차이가 보인다. 외곽 강조와 정확히 같은 곡선이라고 단정하지 않는다.',[25.4,26.2,27.4],[25,30.2])
r.change('c039','31.4초 아래 표제가 옅게 보이고 31.8초에는 드론 비행 경로가 먼저 뚜렷해진다. 같은 31.8초 오른쪽 흰 조건 상자의 문구는 아직 일부가 옅고, 32.2·32.6초 비행고도·속도가 더 읽히게 된다. 서로 완전히 분리된 직렬 등장이라고 단정하지 않는다.',[31.4,31.8,32.2,32.6])
c41=r.add('caption','visibility','order','title-versus-conditions','동일 시각 31.8초에서 왼쪽 드론 비행 경로는 읽히지만 오른쪽 조건 상자 문구는 일부가 약하다. 표제의 판독 가능 상태가 조건 문구 전체의 판독 가능 상태보다 먼저이며 두 과정은 일부 겹친다.',[31.8,32.2],[31.4,35])
r.target('left-halo','왼쪽 지도 드론 주변의 원형 빛','왼쪽 지도 드론을 둘러싼 반투명 흰 원형 영역',['visibility','size'],'left-panel',31.4,[29.8,35])
c43=r.add('left-halo','visibility','presence','halo-visible','31.4초 왼쪽 지도 드론 둘레에 반투명 원형 빛이 보인다. 드론 그림과 별도 효과 대상으로 기록한다.',[31.4],[29.8,35])
c44=r.add('left-halo','size','direction','halo-area','31.4초의 비교적 넓은 원형 빛과 31.8·32.2초의 더 약하거나 좁아 보이는 주변 영역이 다르다. 정확 반경·주기·밝기와 면적의 결합은 미확정.',[31.4,31.8,32.2],[29.8,35])
r.unknown('left-halo','원형 효과의 정확 반경·밝기 변화·반복 주기는 무엇인가?','선택한 표본으로 효과 존재와 차이는 보았으나 정확 곡선을 측정하지 않음')
r.finding('F01','단순 등장으로 축약한 강조의 반복과 이름표 변화',['c019'],['c019',c40])
r.finding('F02','하단 표제와 조건 상자의 선후·중첩',['c039'],['c039',c41])
r.finding('F08','재관찰에서 추가 발견한 왼쪽 지도 드론 주변 원형 빛',[],[c43,c44])
r.finish()

r=Revision('H04')
r.change('c017','66.0→66.4→66.8→67.2초 인셋 안 드론 표시는 왼쪽 세로 노란 경로를 따라 위쪽 핀 부근으로 올라간다. 67.2초 이후 선택 표본에서는 그 부근에 머문다. 화면 전체 카메라 이동이나 실사 드론 궤적과 별도이며 정확 속도·정착 경계는 미확정.',[66,66.4,66.8,67.2,67.6,72.8,75.6])
r.change('c004','67.2초 좌상단에 이전 문구 대신 가느다란 청록 세로 띠가 보인다. 67.6초 좁은 면과 일부 글자가 보이고 68초 새 사선 리본과 드론 비행 시험 종료가 전체 폭으로 보인다. 실제 3D 회전·마스크 방식은 확정하지 않는다.',[67.2,67.6,68])
r.prop('header','size');c24=r.add('header','size','direction','transition-width','67.2초의 가느다란 세로 띠에서 67.6초 좁은 면, 68초 전체 폭 리본으로 가로로 보이는 범위가 커진다. 실제 레이어 폭 변경인지 회전·가림인지 미확정.',[67.2,67.6,68],[66,76])
r.change('c021','67.2초 하단 착륙이 옅게 보이고 67.6초에는 읽히지만 같은 시각 상단 새 표제는 좁은 면·부분 글자 상태다. 68초 상단 표제가 전체 폭으로 보인다. 하단 착륙의 판독 가능 상태가 상단 새 표제 완성보다 먼저다.',[67.2,67.6,68])
r.change('c006','하늘 위주 화면에서 지면이 더 드러나며, 71.4초 원거리 드론·운동장 구도에서 71.5초 크게 보이는 드론·하늘 구도로 급히 바뀐다. 기존 71.2~71.6초 범위를 보강한 경계이며 실제 소스 컷 편집 방식은 프로젝트 없이 확정하지 않는다.',[66,70.8,71.4,71.5,72.8])
r.change('c009','71.4초와 71.5초 사이 드론의 보이는 크기와 배경 구도가 함께 크게 달라진다. 연속 스케일 애니메이션으로 단정하지 않는다.',[71.4,71.5,72.8])
r.target('mini-halo','인셋 드론 주변의 원형 빛','인셋 드론 그림을 둘러싼 반투명 흰 원과 밝은 주변 영역',['visibility','size','color'],'mini-panel',67.2,[66,76])
c26=r.add('mini-halo','visibility','presence','halo-visible','66.8·67.2·72.8초 인셋 드론 주변에 반투명 흰 원형 영역이 보인다. 드론 이동과 별도 주변 효과로 기록한다.',[66.8,67.2,72.8])
c27=r.add('mini-halo','size','direction','halo-area','66.0초와 66.8·67.2·67.6·72.8초를 비교하면 원형 효과의 보이는 면적이 달라진다. 드론이 상단 부근에 머문 뒤에도 넓은 원이 다시 보인다. 정확 반경·주기·파형은 미확정.',[66,66.8,67.2,67.6,72.8])
c28=r.add('mini-halo','color','value','halo-intensity','원형 영역과 드론 주변 밝은 부분의 강도가 표본마다 달라 보인다. 드론 자체의 흰/보라 명암과 효과의 밝기를 같은 속성으로 확정하지 않는다.',[66.8,67.2,67.6,72.8])
r.target('red-light','실사 드론 상단 붉은 광점','실사 드론 상단 중앙 부근의 작은 붉은 밝은 점',['visibility','color'],'real-drone',72.8,[71.5,76])
c30=r.add('red-light','visibility','presence','visible-sample','71.5·72.8초 실사 드론 상단에 작은 붉은 광점이 보인다. 앞 원거리 구간에서 안 읽힌다는 이유로 없다고 판정하지 않는다.',[71.5,72.8],[71.5,76])
c31=r.add('red-light','color','value','red-appearance','71.5·72.8초 광점은 주변의 검은 드론 몸체와 구별되는 붉은색으로 보인다. 발광 원인·깜빡임 주기는 확인하지 않았다.',[71.5,72.8],[71.5,76])
r.unknown('mini-halo','원형 빛의 정확 반경·밝기·주기와 드론 자세 변화의 관계는 무엇인가?','주변 효과의 존재와 표본 차이는 관측했으나 곡선·구현은 미측정')
r.finding('F03','인셋 내부 이동 방향과 상단 체류',['c017'],['c017'])
r.finding('F04','상단 표제의 중간 형태와 가로로 보이는 범위',['c004'],['c004',c24])
r.finding('F05','하단 착륙과 상단 새 표제 완성의 선후',['c021','c004'],['c021'])
r.finding('F06','인셋 드론 주변의 원형 빛 누락',[],[c26,c27,c28])
r.finding('F07','실사 드론 상단 붉은 광점 누락',[],[c30,c31])
r.finding('F09','보강 표본으로 실사 구도 전환 경계 좁히기',['c006','c009'],['c006','c009'])
r.finish()
