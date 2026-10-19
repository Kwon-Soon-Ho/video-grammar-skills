from pathlib import Path
from fractions import Fraction
import json,sys,hashlib
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
SCRIPTS=HERE/'candidate/company-video-grammar-analyzer/scripts';sys.path.insert(0,str(SCRIPTS))
from evidence_catalog import catalog
from check_record import check
from render_observations import render
from review_ledger import validate
from source_coverage import summarize
def load(p):return json.loads(Path(p).read_text('utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
old=WORK/'analysis-reliability-20261019/fresh'
logs=list((old/'cases').rglob('실행기록.json'))+list((HERE/'source-overview/cases').rglob('실행기록.json'))
logs=[p for p in logs if load(p).get('complete_target_selection')]
crops=load(HERE/'probes/crop-inputs.json')+load(HERE/'probes/line-crop-inputs.json')
# Preserve the old detailed evidence, including the exact native crops used in prior claims.
for p in (old/'detail-results').rglob('catalog.json'):
    for e in load(p)['frames']:
        if 'crop_xyxy_native_pixels' in e:
            crop={k:e[k] for k in ('path','parent_path','crop_xyxy_native_pixels')}
            if not any(x['path']==crop['path'] for x in crops):crops.append(crop)
cat=catalog(logs,crops);write(HERE/'evidence-catalog.json',cat)
def augment(d,object_id,prop):
    o=next(o for o in d['objects'] if o['id']==object_id)
    if prop not in o['required_properties']:o['required_properties'].append(prop);o['excluded_properties'].pop(prop)
def ev(d,path):
    entry=next(e for e in cat['frames'] if Path(e['path']).resolve()==Path(path).resolve())
    eid='p'+str(len(d['evidence'])).zfill(3);t=Fraction(entry['actual_playback_seconds']);a,b=map(Fraction,d['window_seconds'])
    d['evidence'].append({'id':eid,'path':str(Path(path).resolve()),'actual_seconds':str(t),'role':'within' if a<=t<b else 'context_after' if t>=b else 'context_before'})
    return eid
def claim(d,cid,obj,prop,dim,text,eids,kind='observed'):
    c={'id':cid,'object_id':obj,'property':prop,'facet':'value','dimension':dim,'time_seconds':d['window_seconds'],'statement':text,'basis_kind':kind,'evidence_ids':eids,'content_review':'supported'}
    d['claims'].append(c)
    rows=[r for r in d['observation_rows'] if r['object_id']==obj and r['property']==prop]
    if not rows:
        rows=[{'id':obj+'-'+prop,'object_id':obj,'property':prop,'time_seconds':d['window_seconds'],'review_state':'reviewed','change':'unknown','evidence_ids':[],'claim_ids':[],'unknown_ids':[],'reason':'추가 확인한 속성. 확인한 표본 범위만 판정.'}];d['observation_rows']+=rows
    r=rows[0];r['claim_ids'].append(cid);r['evidence_ids']=list(dict.fromkeys(r['evidence_ids']+eids))
    d['review']['content_reviewed_claim_ids'].append(cid)
    for state in d['layout']['states']:state['claim_ids'].append(cid)
    return c
for code in ['NEW-N','NEW-P']:
    before=old/'detail-results'/code/'observations-property-reviewed.json';d=load(before);d['skill_version']='0.1.0-draft.8'
    findings=[]
    if code=='NEW-N':
        bg=[ev(d,HERE/'probes'/f'N-background-{side}-{t}.0.png') for side in ['left','right'] for t in [166,168,170,172,174]]
        rear=[ev(d,HERE/'probes'/f'N-rear-{t:.1f}.png') for t in [168.5,169,169.5,170,170.5,171,171.5,172,172.5,173,173.5,174]]
        claim(d,'c033','background','color','local-brightness-evolution','확인한 좌측 점·망사 ROI와 오른쪽 푸른 배경 ROI에서는 166→168→170초에 더 밝아지고 170/172/174초 표본은 유사한 밝기다. 같은 무늬의 위치는 대체로 유지된다. 전체 배경의 미세 이동·밝기 곡선·실제 opacity 구현은 이 표본으로 확정하지 않는다.',bg)
        claim(d,'c034','rear-arcs','visibility','sampled-onset-and-exit','먼 끝 ROI는 168.5초에 곡선이 뚜렷하지 않고 169초에 희미한 일부, 169.5초에 더 분명한 곡선, 170~173초 표본에 청록 쌍 곡선이 보인다. 173.5초에는 약해지고 174초 문맥 표본에는 보이지 않는다. 정확 출현·소실 시각은 인접 표본 사이이며 전체 주기와 가감속은 미확정이다.',rear)
        row=next(r for r in d['observation_rows'] if r['id']=='background-color');row.update(change='changed',reason='주 색상 계열 유지와 시간별 밝기 변화는 별도. 새 ROI 비교에서 밝기 변화 확인.')
        row=next(r for r in d['observation_rows'] if r['id']=='rear-arcs-visibility');row.update(review_state='reviewed',change='changed',unknown_ids=[],reason='원본 크기 ROI의 .5초 표본에서 출현·강약·소실 확인. 표본 사이 정확 곡선은 별도 미해결.')
        u=d['unknowns'][0];u.update(reason='양측 ROI 166/168/170/172/174초에서 밝기 변화와 위치 유사를 확인함. 연속 미세 변화와 전체 배경 영역의 독립성·정확 곡선은 남음.',next_probe='같은 배경 ROI의 진행 중 연속 프레임과 하단 곡선 영역을 비교해 밝기/위치 변화 및 다른 요소의 겹침을 분리')
        u=d['unknowns'][3];u.update(state='resolved',reason='0.5초 표본의 출현 범위·강약·소실을 추가 관측. 정확 프레임 경계·반복 파형은 u02에 남음.',resolution_claim_ids=['c034'],next_probe='')
        requirements=[('background','color','local-brightness-evolution','c033'),('rear-arcs','visibility','sampled-onset-and-exit','c034')]
    else:
        # Keep the first wrong hypothesis visible as rejected; do not silently rewrite history.
        next(c for c in d['claims'] if c['id']=='c002')['content_review']='rejected'
        eids=[e['id'] for e in d['evidence'] if e['id'].startswith('f')]
        claim(d,'c041','map','size','stable-map-anchors','40~48초의 0.5초 표본에서 지도 남서·남동의 서로 떨어진 지형 ROI와 기존 경찰청 카드의 같은 특징이 같은 원본 좌표에 유지된다. 40/48초 정합에서도 두 지도 ROI와 카드가 같은 위치에서 일치한다. 이 구간의 지도 줌·기존 묶음 축소 추정 c002는 기각한다. 새 기관 카드·패널의 개별 등장은 별도 동작이며 AE 카메라·부모 리그를 복원한 것이 아니다.',eids)
        claim(d,'c042','map','size','native-roi-difference','같은 native 좌표 ROI를 40초와 나머지 16개 표본에서 비교한 최대 평균 RGB 절대차는 지도 남서 0.10819/남동 0.05304(0~255 단위), 경찰청 카드 0.35044다. 40/48초의 1/4회색조 NCC는 두 지도 ROI 약1, 카드 0.99999이며 일치 위치는 동일하다. 4px 정합 해상도와 압축 차이를 포함한다. 가려진 북쪽 ROI(NCC .315)와 강조가 바뀐 정책 패널(.374)은 채택하지 않는다. 세 점 affine 잔차가 0에 가깝다는 사실은 독립 검증 근거로 사용하지 않는다.',eids,'calculated')
        augment(d,'regional-link','position')
        line=[ev(d,HERE/'probes'/f'line-frame-{i}.png') for i in range(10)]
        more=[ev(d,x['path']) for x in crops if Path(x['path']).name.startswith('P-connector-')]
        claim(d,'c043','regional-link','position','stationary-upward-glyph','연결선 ROI의 43.8~45.3초 선택 표본과 44.000~44.300초의 연속 10프레임에서 위를 향하는 화살 무늬의 위치는 같아 보이고 주로 밝기 차이가 보인다. 위를 향하는 모양을 위로 이동하는 애니메이션으로 쓰지 않는다. 검사하지 않은 시간의 흐름·초기 성장·주기는 이 결론에 포함하지 않는다.',line+more)
        row=next(r for r in d['observation_rows'] if r['id']=='map-size');row.update(change='unchanged',reason='c002는 기각된 이전 추정. 현재 결론은 c041/c042의 분리된 고정 기준점 비교에 근거.')
        row=next(r for r in d['observation_rows'] if r['id']=='regional-link-position');row.update(change='unchanged',reason='연속 10프레임과 선택 ROI에서 같은 무늬 위치 확인. 전체 창의 모든 시각·초기 등장 과정은 미확정.')
        # The checked settled span must not mark the entire new property as reviewed.
        next(c for c in d['claims'] if c['id']=='c043')['time_seconds']=[43.8,45.3]
        row['time_seconds']=[43.8,45.3]
        for rid,span in [('regional-link-position-before',[40,43.8]),('regional-link-position-after',[45.3,48])]:
            d['observation_rows'].append({'id':rid,'object_id':'regional-link','property':'position','time_seconds':span,'review_state':'not_reviewed','change':'unknown','evidence_ids':[],'claim_ids':[],'unknown_ids':['u02'],'reason':'정착 구간의 위치 비교를 앞뒤 시간대로 확대하지 않음. 생성/퇴장과 다른 시각은 추가 검수 대상.'})
        u=d['unknowns'][0];u.update(state='resolved',reason='기존 지도/카드의 서로 떨어진 고정 특징을 확인해 전체 줌 추정을 기각. 새 카드·패널 등장과 분리. 실제 리그·렌더 사이 숨은 움직임은 검증하지 않음.',resolution_claim_ids=['c041'],next_probe='')
        u=d['unknowns'][1];u.update(reason='선택 ROI와 연속 10프레임의 정착 구간에서는 위쪽 화살 모양이 같은 위치에 보임. 초기 생성/다른 시간대의 이동 여부는 아직 남음.',next_probe='연결선 처음 생성~정착과 이후 퇴장까지 같은 무늬 특징을 연속 비교. 방향 형태와 실제 이동을 분리')
        for g in d['motion_groups']:g['claim_ids']=['c041' if c=='c002' else c for c in g['claim_ids']]
        requirements=[('map','size','stable-map-anchors','c041'),('regional-link','position','stationary-upward-glyph','c043')]
    open_ids=[u['id'] for u in d['unknowns'] if u['state']=='open']
    d['discovery']['unresolved_ids']=open_ids;d['layout']['unresolved_ids']=open_ids
    for s in d['layout']['states']:s['unresolved_ids']=open_ids
    for g in d['motion_groups']:
        g['claim_ids']+=['c033','c034'] if code=='NEW-N' else ['c043']
    d['method']+=' 추가로 전체 개요 5초 표본과 지정 ROI, PG 연결선의 30fps 연속 10프레임을 검토했다. 지도 정합은 실제 native ROI와 별도 수치 진단을 대조했다. 동일 AI 후속 검수이며 정밀 검수 완료 아님.'
    d['review']['remaining_scope']=['동일 AI의 후속 검수. 원본 전체 정밀 분석·독립 정답·모든 미발견 요소의 분모는 미확인.', '열린 쟁점 '+', '.join(open_ids)]
    after=HERE/'records'/code/'observations.json';write(after,d)
    errors=check(d,cat);assert not errors,(code,errors)
    (after.with_suffix('.md')).write_text(render(d),encoding='utf-8')
    for i,(obj,prop,dim,cid) in enumerate(requirements):
        findings.append({'id':'F'+str(i+1),'question':d['claims'][next(j for j,c in enumerate(d['claims']) if c['id']==cid)]['statement'],'requirements':[{'object_id':obj,'property':prop,'dimension':dim}],'required_basis_kind':'observed','before_claim_ids':['c002'] if code=='NEW-P' and obj=='map' else [],'state':'addressed','resolution_claim_ids':[cid],'reason':'지정 ROI를 실제 비교하여 확인한 새 사실. 전체 발견 완전성/구현 확정과 구분.','next_probe':''})
    ledger={'schema_version':'video-review-ledger-0.1','revision':1,'before':{'path':str(before.resolve()),'sha256':sha(before)},'after':{'path':str(after),'sha256':sha(after)},'reviewer':{'kind':'same_agent_context','name':'Codex','method':'원본 픽셀 ROI·시각 순서 대조, 수치 정합의 가림/강조 예외 검토. 사람/독립 AI 아님.'},'findings':findings}
    write(after.parent/'review-ledger.json',ledger);write(after.parent/'validation.json',{'observation_errors':errors,'review_ledger':validate(ledger,cat)})

# Work partitions chosen from the 129 visually inspected overview samples, never exact cut claims.
N=[(0,25,'기술 도면·3D 부재와 브랜드 도입'),(25,60,'교량·현장·공장·운송 소개'),(60,75,'적용 사례와 디지털 작업 개요'),(75,100,'거더 정의와 제작·운송·조립'),(100,125,'구조 장점과 곡선 적용'),(125,140,'부품 변형과 운송·조립 설명 카드'),(140,165,'핵심 기술 분해도와 부품 강조'),(165,185,'전체 거더·단면·보강 화살표와 설명'),(185,210,'균열·단면·캔틸레버 성능 설명'),(210,240,'디지털 설계·BIM과 작업자 인셋'),(240,250,'BIM 시공과 일정 프로그램 병렬'),(250,270,'공장 제작 CG와 실사 병렬'),(270,285,'부품 갤러리와 공장·현장 연결'),(285,300,'현장 조립 도입과 임시 지지 구조'),(300,330,'철근·연결부·타설·긴장 조립 순서'),(330,365,'가설 장비·거더 배치·상판 시공'),(365,400,'야간 CG 전환과 결론 사례'),(400,None,'도시 교량·결론 문구·브랜드 마감')]
P=[(0,25,'착공식 제목·미래차·탑승 장면'),(25,55,'지도 위 경찰청·강원 기관과 정책 설명'),(55,80,'도로교통공단·KCL 등 협력 기관 확장'),(80,100,'평가 검증단지 평면과 조감도'),(100,115,'버스·교차로·어린이보호 등 시험 구역'),(115,120,'관제실 실사'),(120,155,'차량·보행자 인지와 회전교차로·버스 시험 CG'),(155,175,'관제·전국 지도와 지역 연결망'),(175,195,'디지털 전환과 미래 비전 표제'),(195,205,'단지 건물 조감도와 제목'),(205,None,'기관 로고 띠와 단지 전경 마감')]
sources=load(HERE/'source-overview/manifest.json');groups=[];records=[]
for s,plan in zip(sources,[N,P]):
    fs=[]
    for p in (HERE/'source-overview/cases'/s['id']).glob('overview*/실행기록.json'):
        log=load(p)
        if log.get('complete_target_selection'):fs+=log['frames']
    for i,(a,b,summary) in enumerate(plan,1):
        b=s['duration_seconds'] if b is None else b
        es=[{'path':f['path'],'actual_seconds':f['actual_playback_seconds']} for f in fs if Fraction(a)<=Fraction(f['actual_playback_seconds'])<Fraction(str(b))]
        groups.append({'id':s['id']+'-G'+str(i).zfill(2),'source_id':s['id'],'planning_seconds':[a,b],'boundary_kind':'provisional_work_partition','summary':summary,'overview_evidence':es,'next_probe':'실제 전환 경계·전체 디자인·전체 흐름·대상 내부/주변의 세부 동작을 분해. 5초 표본 사이 짧은 장면도 확인.'})
    obs=HERE/'records'/s['id']/'observations.json';d=load(obs);a,b=d['window_seconds']
    records.append({'id':s['id']+'-current','source_id':s['id'],'path':str(obs),'sha256':sha(obs),'group_ids':[g['id'] for g in groups if g['source_id']==s['id'] and Fraction(str(g['planning_seconds'][0]))<b and a<Fraction(str(g['planning_seconds'][1]))]})
coverage={'schema_version':'source-coverage-0.1','sources':sources,'groups':groups,'records':records}
write(HERE/'source-coverage.json',coverage);result=summarize(coverage,cat);write(HERE/'coverage-result.json',result)
md=['# 두 사내 원본의 개요와 남은 상세 분석','', '5초 간격 129장 개요를 실제 검토한 작업 묶음이다. 아래 경계는 정확 컷이 아닌 잠정 작업 분할이다. 표본 사이 숨은 장면은 남아 있다.','', '두 기록 창 16초도 모든 속성의 정밀 검수 완료를 뜻하지 않는다. 전체 정밀 검수 완료: 아직 판단하지 않음.','']
for s in result['sources']:
    md+=['## '+s['id'],f"원본 {float(Fraction(s['duration_seconds'])):.3f}초 / 작업 묶음 {s['planning_groups']} / 일부 기록 있는 묶음 {s['groups_with_some_record']} / 기록 창 밖 {float(Fraction(s['outside_recorded_windows_seconds'])):.3f}초 / 열린 쟁점 {s['open_unknown_entries']}개",'']
    for g in groups:
        if g['source_id']==s['id']:md+=[f"- {g['id']} [{g['planning_seconds'][0]}~{g['planning_seconds'][1]}초]: {g['summary']} / 개요 근거 {', '.join(e['actual_seconds'] for e in g['overview_evidence'])}"]
md+=['','바로 다음: 노듈러의 현재 창 끝에서 등장 중인 왼쪽 설명을 완료 시점까지 이어 확인하고, 화살표 반복·배경 변화와 PG 연결선 생성/퇴장·강조 동기화를 보완한다. 그 뒤 미기록 작업 묶음으로 범위를 넓힌다. 재사용 확대보다 사내 영상 검수가 우선이다.','', '스킬 전체: ① 분석 신뢰성 보완 중 ② 패턴 검색·재사용 일부 구현 ③ 전문가 대안·선택·비평은 연결 형식 중심 ④ 편집 가능한 재제작·렌더 비교·내용 변경 검증은 미구현. 조사한 모든 스킬 반영 완료가 아니다.']
(HERE/'00_현재위치와_다음작업.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
registration=load(HERE/'probes/map-registration.json');registration['visual_review']={'reviewer':'same_agent_context','state':'reviewed','accepted':['map-west-south','map-east-south','police-card'],'excluded':{'map-north':'새 붉은 패널에 가림. 낮은 NCC 후보 기각.','policy-panel':'행 강조가 바뀜. 낮은 NCC 후보 기각.'},'conclusion':'선택 고정 특징에서 위치 일치. 지도 줌 추정 기각. affine 잔차 자체를 증거로 사용하지 않음.'};write(HERE/'probes/map-registration.json',registration)
change=load(HERE/'source-overview/chunk-read-change.json');retry=HERE/'source-overview/cases/NEW-P/overview1_retry1/실행기록.json';log=load(retry);assert log['complete_target_selection'] and log['input_sha256']==log['input_sha256_after'];change['validation']={'actual_retry':'passed','log':str(retry),'frames':len(log['frames']),'scope':'새 개요 추출 보조 어댑터만 변경. 범용 디코더/정본 런타임 수리 주장 아님.'};write(HERE/'source-overview/chunk-read-change.json',change)
print(json.dumps({'catalog_frames':len(cat['frames']),'coverage':result},ensure_ascii=False))
