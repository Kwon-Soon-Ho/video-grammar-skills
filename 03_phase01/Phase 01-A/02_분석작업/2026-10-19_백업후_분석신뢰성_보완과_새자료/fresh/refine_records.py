from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
import sys,json
HERE=Path(__file__).resolve().parent;TASK=HERE.parent
sys.path.insert(0,str(TASK/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import load,digest,check,PROPERTIES
from evidence_catalog import catalog
from render_observations import render
from review_ledger import validate
def save(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists(),p
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
for aid in ('NEW-N','NEW-P'):
    before=HERE/'results'/aid/'first-observations.json';d=deepcopy(load(before));out=HERE/'detail-results'/aid
    logs=[HERE/'cases'/aid/phase/'실행기록.json' for phase in ('window','detail1','detail2','detail3')]
    cat=catalog(logs);save(out/'catalog.json',cat);fine={}
    for frame in cat['frames']:
        if '/window/' in frame['path'].replace('\\','/'):continue
        t=F(frame['actual_playback_seconds']);eid='x'+str(len(d['evidence'])).zfill(3)
        d['evidence'].append({'id':eid,'path':frame['path'],'actual_seconds':str(t),'role':'context_after' if t>=d['window_seconds'][1] else 'within'});fine[t]=eid
    def refs(*times):return [fine[F(str(t))] for t in times]
    def current(oid,dim):return next(c for c in d['claims'] if c['object_id']==oid and c['dimension']==dim)
    findings=[]
    def finding(fid,question,cids,oldids):
        cs=[c for c in d['claims'] if c['id'] in cids]
        findings.append({'id':fid,'question':question,'requirements':[{'object_id':c['object_id'],'property':c['property'],'dimension':c['dimension']} for c in cs],'required_basis_kind':'observed','before_claim_ids':oldids,'state':'addressed','resolution_claim_ids':cids,'reason':'0.1초 간격 근거를 만든 뒤 지정 ROI의 시간순 개요를 재관찰해 보완. 동일 AI 문맥, 독립 검수 아님.','next_probe':None})
    def prop(oid,p):
        obj=next(o for o in d['objects'] if o['id']==oid)
        if p not in obj['required_properties']:obj['required_properties'].append(p);obj['excluded_properties'].pop(p,None)
    def add(oid,p,facet,dim,text,times):
        cid='c'+str(len(d['claims'])+1).zfill(3);d['claims'].append({'id':cid,'object_id':oid,'property':p,'facet':facet,'dimension':dim,'time_seconds':d['window_seconds'],'statement':text,'basis_kind':'observed','evidence_ids':refs(*times),'content_review':'supported'});return cid
    open_fields=[]
    if aid=='NEW-N':
        c=current('right-label','reveal');old=c['id'];c.update(statement='167.2초 표본에서는 설명 세로선이 뚜렷하지 않고 167.3초 옅은 단일 세로선이 보인다. 167.9초 가까운 두 선, 168.2초 부분 글자, 168.6~168.7초 문구가 전체로 읽히는 상태가 된다. 두 선 사이 가로 범위 전개와 글자의 가시성은 서로 구분한다.',evidence_ids=refs(167.2,167.3,167.9,168.2,168.6,168.7))
        finding('D01','설명 띠 중간 상태와 판독 구간을 0.1초 표본으로 구체화',[old],[old])
        prop('background','internal_state');open_fields=[('background','internal_state','u01','배경 미세 모션은 아직 대상별 연속 검수하지 않음')]
    else:
        c=current('gangwon','logo-assembly');old=c['id'];c.update(statement='41.3초 선택 ROI에서 로고가 뚜렷하지 않고 41.4초 얇게 드러난 부분, 41.5초 일부 글자, 41.6초 강원 로고 형태가 보인다. 밝은 카드 면은 그 뒤 42.3초 가느다란 세로 범위로 생겨 42.4~42.8초 가로로 넓어진다. 로고 글자와 카드 면을 하나의 동시 등장으로 처리하지 않는다.',evidence_ids=refs(41.3,41.4,41.5,41.6,42.3,42.4,42.8))
        d['objects'].append({'id':'gangwon-face','name':'강원 카드의 밝은 배경 면','parent':'gangwon','shape_description':'로고 뒤에 나중에 펼쳐지는 흰색·연분홍 직사각 면과 가는 모서리 선','required_properties':['identity','visibility','size'],'excluded_properties':{p:'이번 독립 관측은 면의 형태·출현·가로 전개. 다른 외관은 기존 전체 디자인에 연결.' for p in PROPERTIES-{'identity','visibility','size'}},'identity':{'status':'reviewed','label':'강원 카드의 밝은 배경 면','candidates':[],'claim_ids':[]}})
        ident=add('gangwon-face','identity','identity','visible-form','42.5초 로고 뒤의 밝은 직사각 면과 모서리 선을 구분한다.',[42.5]);d['objects'][-1]['identity']['claim_ids']=[ident]
        face=add('gangwon-face','visibility','order','face-after-logo','41.6초 로고는 보이지만 밝은 직사각 면은 없고, 42.3초 뒤에 좁은 세로 면이 생겨 42.5초 이후 카드 바탕으로 보인다.',[41.6,42.2,42.3,42.5])
        width=add('gangwon-face','size','direction','face-width','42.3초 좁은 세로 면에서 42.4~42.8초 넓은 가로 카드 면으로 변한다. 실제 스케일·마스크·회전 구현은 미확정.',[42.3,42.4,42.5,42.6,42.8])
        finding('D02','로고 먼저, 밝은 카드 면 나중의 순서와 면 전개 구분',[old,face,width],[old])
        c=current('regional-row2','second-row-enter');old=c['id'];c.update(statement='46.0초에는 둘째 줄 띠가 뚜렷하지 않고 46.1초 작은 어두운 띠가 생겨 46.2~46.4초 가로로 넓어진다. 46.5초 옅은 글자가 나타나 46.6~47.0초 더 읽히고, 47.2초 이후 밝은 분홍 강조가 강해진다. 띠·글자·강조의 시작을 분리한다.',evidence_ids=refs(46,46.1,46.3,46.5,46.8,47,47.2))
        finding('D03','둘째 줄 띠·글자·강조의 순서를 0.1초 표본으로 분리',[old],[old])
        prop('regional-link','internal_state');open_fields=[('regional-link','internal_state','u02','연결선 내부 무늬의 이동 방향은 아직 미확정')]
    for oid,p,uid,reason in open_fields:
        d['observation_rows'].append({'id':oid+'-'+p,'object_id':oid,'property':p,'time_seconds':d['window_seconds'],'review_state':'unresolved','change':'unknown','evidence_ids':[],'claim_ids':[],'unknown_ids':[uid],'reason':reason})
        findings.append({'id':'OPEN-'+oid,'question':reason,'requirements':[{'object_id':oid,'property':p,'dimension':'unreviewed-change'}],'required_basis_kind':'observed','before_claim_ids':[],'state':'open','resolution_claim_ids':[],'reason':'미확인 속성을 범위 밖으로 숨기지 않고 열린 검수로 유지','next_probe':'해당 영역을 기준점으로 시간순 원본 비교 후 관측 주장 또는 판독 한계를 보완'})
    for obj in d['objects']:
        for p in obj['required_properties']:
            cs=[c for c in d['claims'] if c['object_id']==obj['id'] and c['property']==p]
            rows=[r for r in d['observation_rows'] if r['object_id']==obj['id'] and r['property']==p]
            if not rows:
                rows=[{'id':obj['id']+'-'+p,'object_id':obj['id'],'property':p,'time_seconds':d['window_seconds'],'review_state':'reviewed','change':'changed' if p!='identity' else 'unchanged','evidence_ids':[],'claim_ids':[],'unknown_ids':[],'reason':'보강 표본의 관측'}];d['observation_rows']+=rows
            for row in rows:
                if row['review_state']!='reviewed':continue
                row.update(claim_ids=[c['id'] for c in cs],evidence_ids=sorted({e for c in cs for e in c['evidence_ids']}))
    for state in d['layout']['states']:
        state['element_object_ids']=[o['id'] for o in d['objects']];state['claim_ids']=[c['id'] for c in d['claims']]
    d['motion_groups'][1]['object_ids']=[o['id'] for o in d['objects']];d['motion_groups'][1]['claim_ids']=[c['id'] for c in d['claims'] if c['property']!='identity']
    d['discovery']['unresolved_ids']=[u['id'] for u in d['unknowns']]
    d['method']+=' 동일 문맥의 후속 정밀 검토에서 0.1초 간격 81개 추가 표본을 만들고, N의 오른쪽 설명 영역 또는 P의 지역 카드·프레임 영역을 전 시간순 ROI 시트로 대조했다. 추가 표본 81장을 모두 전체 화면 native로 읽은 것은 아니다.'
    d['review']['content_reviewed_claim_ids']=[c['id'] for c in d['claims']]
    d['limitations']+=['전체 원본 영상에서 확인한 구간은 8초. 원본 전체 분석 완료 아님.','0.1초 보강은 지정 ROI의 상세 확인. 다른 대상·전체 프레임의 완전성을 보장하지 않음.']
    errors=check(d,cat);assert not errors,(aid,errors)
    after=out/'observations-detailed.json';save(after,d);(out/'observations-detailed.md').write_text(render(d),encoding='utf-8')
    ledger={'schema_version':'video-review-ledger-0.1','revision':1,'before':{'path':str(before),'sha256':digest(before)},'after':{'path':str(after),'sha256':digest(after)},'reviewer':{'kind':'same_agent_context','name':'Codex detail review','method':'지정 ROI의 0.1초 표본 시각 재대조. 독립 검수 아님.'},'findings':findings}
    save(out/'review-ledger.json',ledger);result=validate(ledger,cat);save(out/'validation.json',result);print(json.dumps({'case':aid,'claims':len(d['claims']),**result},ensure_ascii=False))
