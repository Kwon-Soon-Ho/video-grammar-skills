"""합성 계약 fixture만 사용한다. '실제draft' 분기 시험도 메모리 가짜자료이며 운영DB 등록 금지."""
from pathlib import Path
import copy,json,importlib.util
BASE=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
def load_checker(path):
    spec=importlib.util.spec_from_file_location('ev_checker',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def ref(x):return {k:x[k] for k in ['id','version']}
def pin(x):return {k:x[k] for k in ['id','version','sha256']}
def frac(n,d=1):return {'num':n,'den':d}
def fixture():
    tr=json.loads((BASE/'04_기록규격/시간프레임_설명용기록.json').read_text(encoding='utf-8'))
    tr['periods']+=[{'id':'EX-WHOLE','timeline_ref':'EX-TIME','parent_ref':None,'kind':'range','start':frac(0),'end':frac(10),'uncertainty':frac(0),'unknown_reason':None},{'id':'EX-INSTANT','timeline_ref':'EX-TIME','parent_ref':'EX-SEGMENT','kind':'instant','start':frac(1),'end':None,'uncertainty':frac(0),'unknown_reason':None}]
    def material(id,kind,hash='1'*64,parent=None,text=None,frame=None,period=None):return {'id':id,'version':'0.1.0','sha256':hash,'kind':kind,'locator':'fixture-only://'+id,'availability':'present','source_type':'synthetic_example','parent_ref':parent,'frame_ref':frame,'period_ref':period,'method_note':'인위적 형식 검사 자료. 파일/내용/원본 정확성 검증 아님.','text':text,'authority':None}
    video=material('EX-ASSET','video','0'*64)
    meta=material('EX-META','project_document',text='길이10초와 원점90000을 설명하는 가상 자료다.')
    image=material('EX-IMAGE','frame',parent=pin(video),frame='EX-FRAME')
    targets=[]
    for id,unit,parent,period in [('TG-ASSET','asset',None,'EX-WHOLE'),('TG-SEGMENT','segment','TG-ASSET','EX-SEGMENT'),('TG-STATE','screen_state','TG-SEGMENT','EX-SEGMENT'),('TG-OBJECT','object','TG-STATE','EX-SEGMENT')]:
        targets.append({'id':id,'version':'0.1.0','unit':unit,'asset_ref':pin(video),'parent_ref':None if parent is None else {'id':parent,'version':'0.1.0'},'period_ref':period,'label':'가상 영상의 '+unit+' 대상'})
    def selector(kind,frame=None,period=None,exact=None,start=None,end=None):return {'kind':kind,'frame_ref':frame,'period_ref':period,'exact':exact,'start':start,'end':end}
    evidence=[]
    for id in ['EX-DURATION','EX-ORIGIN']:
        evidence.append({'id':id,'version':'0.1.0','material_ref':pin(meta),'target_ref':ref(targets[0]),'selector':selector('text',exact=meta['text'],start=0,end=len(meta['text'])),'limitations':'시간 메타의 가상 확인 근거. 실제 원본 정확성 아님.'})
    evidence.append({'id':'EV-FRAME','version':'0.1.0','material_ref':pin(image),'target_ref':ref(targets[-1]),'selector':selector('frame',frame='EX-FRAME'),'limitations':'프레임이 대상에 해당한다는 내용은 사람 검수 필요.'})
    claim={'id':'CL-ONE','version':'0.1.0','statement':'화살표가 있다는 주장에 근거를 연결하는 미관측 설명 예시다.','support_mode':'not_observed_example','aspect':'visual_presence','scope':{'target_ref':ref(targets[-1]),'period_ref':'EX-INSTANT','extent':'instant'},'evidence_links':[{'ref':ref(evidence[-1]),'role':'support'}],'measurement':None,'review_ref':None,'limitations':'실영상·회사 문법·사람 승인으로 사용하지 않는 합성 구조 예.'}
    return {'contract_version':'0.1.0','record_purpose':'spec_test','time_contract':tr,'materials':[video,meta,image],'targets':targets,'evidence':evidence,'claims':[claim],'review_records':[],'notes':'모든 값은 인위적 fixture. 테스트 전용·운영DB 등록 금지.'}
def observed(x):x['claims'][0].update(support_mode='rendered_observation',statement='1초 표본에서 화살표가 보인다는 구조 시험 주장.');return x
def real_branch(x):
    x['record_purpose']='draft_record';x['time_contract']['source_type']='internal'
    for m in x['materials']:m['source_type']='internal'
def add_frame(x,id='EX-FRAME-2',n=2,ordinal=26):
    f=copy.deepcopy(x['time_contract']['frames'][0]);f.update(id=id,source_pts=str(90000+n*90000),actual=frac(n),requested=frac(n),source_frame_ordinal=ordinal);x['time_contract']['frames'].append(f)
    m=copy.deepcopy(x['materials'][-1]);m.update(id='MAT-'+id,sha256='2'*64,frame_ref=id);x['materials'].append(m)
    e=copy.deepcopy(x['evidence'][-1]);e.update(id='EV-'+id,material_ref=pin(m));e['selector']['frame_ref']=id;x['evidence'].append(e)
    return e,f
def change_claim(x):
    c=x['claims'][0];c.update(support_mode='rendered_observation',aspect='temporal_change');c['scope'].update(period_ref='EX-SEGMENT',extent='sampled');return c
def clip(x):
    e=copy.deepcopy(x['evidence'][-1]);e.update(id='EV-CLIP',material_ref=pin(x['materials'][0]));e['target_ref']=ref(x['targets'][1]);e['selector'].update(kind='clip',frame_ref=None,period_ref='EX-SEGMENT');x['evidence'].append(e);return e
def text_evidence(x,kind='scenario',text='화살표가 등장하도록 계획한다.'):
    m=copy.deepcopy(x['materials'][1]);m.update(id='MAT-TEXT',kind=kind,text=text);x['materials'].append(m)
    e=copy.deepcopy(x['evidence'][0]);e.update(id='EV-TEXT',material_ref=pin(m),target_ref=ref(x['targets'][-1]));e['selector'].update(exact=text,start=0,end=len(text));x['evidence'].append(e);return e,m
def measure(x,quantity='average_speed',count=2,aspect='numeric_value'):
    c=x['claims'][0];c.update(support_mode='numerical_estimate',aspect=aspect);c['scope'].update(period_ref='EX-SEGMENT',extent='sampled')
    evs=[x['evidence'][-1]]
    for i in range(1,count):evs.append(add_frame(x,id='EX-FRAME-'+str(i+1),n=i+1,ordinal=25+i)[0])
    # 3초는 [0,3) 밖이므로 세 번째 표본은 2.5초로 만든다.
    if count>=3:
        f=x['time_contract']['frames'][-1];f.update(source_pts='315000',actual=frac(5,2),requested=frac(5,2))
    c['evidence_links']=[{'ref':ref(e),'role':'support'} for e in evs]
    c['measurement']={'method':'가상 위치표본의 구간 평균 추정. 실제 측정/계산 검증은 사람 대상.','quantity':quantity,'unit':'px/s' if quantity=='average_speed' else 'px/s^2' if quantity=='average_acceleration' else 'ratio' if quantity=='opacity_estimate' else 'px','sample_unit':'ratio' if quantity=='opacity_estimate' else 'px','value':0.5 if quantity=='opacity_estimate' else 100,'uncertainty':1,'uncertainty_kind':'absolute_bound','samples':[{'frame_ref':e['selector']['frame_ref'],'evidence_ref':ref(e),'target_ref':c['scope']['target_ref'],'value':i*100,'coordinate_space_ref':None} for i,e in enumerate(evs)],'assumptions':['가상 동일대상을 추적했다는 전제.'],'limitations':'좌표 규격과 실측은 미확인.'}
def cases(checker):
    out=[]
    def add(name,kind,change,needle=None,content_state=None):
        x=fixture();change(x);out.append({'name':name,'kind':kind,'record':x,'expected_error_fragment':needle,'expected_content_state':content_state})
    def C(x):return x['claims'][0]
    def E(x):return x['evidence'][-1]
    def review(x,outcome='supported',real=False):
        if real:real_branch(x)
        c=C(x);r={'id':'REVIEW-1','kind':'human' if real else 'specimen','reviewer_id':'FIXTURE-REVIEWER','reviewed_at':'2026-10-15T00:00:00Z','claim_ref':ref(c),'context_sha256':checker.context_hash(x,c),'outcome':outcome,'rationale':'가상 receipt의 연결 검사. 실제 검수자가 아님.','conflict_resolution':None}
        x['review_records'].append(r);c['review_ref']=r['id'];return r
    add('미관측 예시 구조와 사람대기','queue',lambda x:None)
    add('원본정지표본 visual 존재는 내용검수대기','queue',observed)
    add('빈근거 hypothesis 보존','queue',lambda x:C(x).update(support_mode='hypothesis',evidence_links=[]))
    add('없던근거ID','invalid',lambda x:C(x)['evidence_links'][0]['ref'].update(id='NONE'),'없는 참조')
    add('근거버전다름','invalid',lambda x:C(x)['evidence_links'][0]['ref'].update(version='0.2.0'),'버전/hash')
    add('재구성이미지 원본frame세탁','invalid',lambda x:x['materials'][-1].update(kind='reconstruction'),'frame 근거')
    add('자료frame/selector대응다름','invalid',lambda x:E(x)['selector'].update(frame_ref='NONE'),'frame_ref')
    add('자료hashpin 불일치','invalid',lambda x:E(x)['material_ref'].update(sha256='f'*64),'버전/hash')
    add('파일변경후 검수receipt 무효','stale',lambda x:(observed(x),review(x),x['materials'][-1].update(locator='changed.png')))
    add('자료파생부모없음','invalid',lambda x:x['materials'][-1].update(parent_ref=None),'원본 참조')
    add('자료파생순환','invalid',lambda x:x['materials'][-1].update(parent_ref=pin(x['materials'][-1])),'파생 순환')
    add('대상참조없음','invalid',lambda x:C(x)['scope']['target_ref'].update(id='NONE'),'없는 참조')
    add('다른object지지근거','invalid',lambda x:(x['targets'].append({**copy.deepcopy(x['targets'][-1]),'id':'TG-OTHER'}),C(x)['scope'].update(target_ref={'id':'TG-OTHER','version':'0.1.0'})),'대상 불일치')
    add('상위화면을통한object지지 내용대기','queue',lambda x:E(x).update(target_ref=ref(x['targets'][2])))
    add('대상부모순환','invalid',lambda x:x['targets'][-1].update(parent_ref=ref(x['targets'][-1])),'부모 순환')
    add('단일still로 변화확인금지','invalid',change_claim,'서로 다른 시각2개')
    add('서로다른2시각변화 표본검수대기','queue',lambda x:(change_claim(x),C(x)['evidence_links'].append({'ref':ref(add_frame(x)[0]),'role':'support'})))
    add('같은시각2이미지 변화증명금지','invalid',lambda x:(change_claim(x),C(x)['evidence_links'].append({'ref':ref(add_frame(x,n=1)[0]),'role':'support'})),'서로 다른 시각2개')
    add('범위clip 변화검수대기','queue',lambda x:(change_claim(x),C(x).update(evidence_links=[{'ref':ref(clip(x)),'role':'support'}])))
    add('support프레임 주장시간밖','invalid',lambda x:(observed(x),x['time_contract']['periods'].append({**copy.deepcopy(x['time_contract']['periods'][2]),'id':'EX-INSTANT-2','start':frac(2)}),C(x)['scope'].update(period_ref='EX-INSTANT-2')),'주장 시간 밖')
    add('전시간 주장 단일frame금지','invalid',lambda x:(observed(x),C(x)['scope'].update(target_ref=ref(x['targets'][0]),period_ref='EX-WHOLE',extent='whole_asset'),E(x).update(target_ref=ref(x['targets'][0]))),'전체 범위 clip')
    add('구간부재 단일frame금지','invalid',lambda x:(observed(x),C(x).update(aspect='negative_absence'),C(x)['scope'].update(period_ref='EX-SEGMENT',extent='sampled')),'단일 프레임')
    add('순간부재는 가림범위 사람검수','queue',lambda x:(observed(x),C(x).update(aspect='negative_absence')))
    add('시나리오 계획 내용검수대기','queue',lambda x:(C(x).update(support_mode='scenario_supported',aspect='scenario_content',evidence_links=[{'ref':ref(text_evidence(x)[0]),'role':'support'}]),C(x)['scope'].update(period_ref=None,extent='unspecified')))
    add('계획을visual실재mode로 승격금지','invalid',lambda x:(observed(x),C(x).update(evidence_links=[{'ref':ref(text_evidence(x)[0]),'role':'support'}])),'원본 frame/clip')
    add('자연어실재문장 typedscenario라면 사람검수필수','queue',lambda x:C(x).update(support_mode='scenario_supported',aspect='scenario_content',statement='영상에서 실제로 화살표가 등장했다.',evidence_links=[{'ref':ref(text_evidence(x)[0]),'role':'support'}]))
    add('OCR을원문시나리오로오용','invalid',lambda x:C(x).update(support_mode='scenario_supported',aspect='scenario_content',evidence_links=[{'ref':ref(text_evidence(x,'ocr')[0]),'role':'support'}]),'원문/전사')
    add('인용위치불일치','invalid',lambda x:(C(x).update(support_mode='scenario_supported',aspect='scenario_content',evidence_links=[{'ref':ref(text_evidence(x)[0]),'role':'support'}]),E(x)['selector'].update(start=1)),'인용 불일치')
    add('emoji Unicode codepoint선택','queue',lambda x:(C(x).update(support_mode='scenario_supported',aspect='scenario_content',evidence_links=[{'ref':ref(text_evidence(x,text='가🙂나')[0]),'role':'support'}]),E(x)['selector'].update(start=1,end=2,exact='🙂')))
    add('UTF16 codeunit를문자index로오용','invalid',lambda x:(C(x).update(support_mode='scenario_supported',aspect='scenario_content',evidence_links=[{'ref':ref(text_evidence(x,text='가🙂나')[0]),'role':'support'}]),E(x)['selector'].update(start=1,end=3,exact='🙂')),'인용 불일치')
    add('일반문서로제작의도확인금지','invalid',lambda x:C(x).update(support_mode='intent_confirmed',aspect='intent',evidence_links=[{'ref':ref(text_evidence(x,'project_document')[0]),'role':'support'}]),'제작자/기획')
    def intent(x):
        e,m=text_evidence(x,'creator_confirmation','이 화살표로 순서를 강조하려고 했다.');m['authority']={'actor_id':'CREATOR','role':'creator','target_refs':[ref(x['targets'][-1])],'confirmation_scope':'해당 화살표의 의도 진술'};C(x).update(support_mode='intent_confirmed',aspect='intent',evidence_links=[{'ref':ref(e),'role':'support'}])
    add('명시확인진술도 실제주체 내용검수','queue',intent)
    add('의도확인범위다른대상','invalid',lambda x:(intent(x),x['materials'][-1]['authority'].update(target_refs=[ref(x['targets'][0])])),'의도 확인 대상')
    add('수치추정measurement없음','invalid',lambda x:C(x).update(support_mode='numerical_estimate',aspect='numeric_value'),'measurement 필요')
    add('속도1표본금지','invalid',lambda x:measure(x,count=1),'서로 다른 원본 시각 2개')
    add('속도2표본 내용좌표검수대기','queue',measure)
    add('가속도2표본금지','invalid',lambda x:measure(x,'average_acceleration',2,'acceleration'),'시각 3개')
    add('가속도3표본도 순간곡선단정금지','queue',lambda x:measure(x,'average_acceleration',3,'acceleration'))
    add('정적위치1표본허용','queue',lambda x:measure(x,'position_x',1))
    add('표본근거 frameref다름','invalid',lambda x:(measure(x),C(x)['measurement']['samples'][0].update(frame_ref='NONE')),'프레임 없음')
    add('측정표본대상다름','invalid',lambda x:(measure(x),C(x)['measurement']['samples'][0].update(target_ref=ref(x['targets'][0]))),'표본 대상')
    add('opacity가정없음','invalid',lambda x:(measure(x,'opacity_estimate',1),C(x)['measurement'].update(assumptions=[])),'합성 조건')
    add('NaN수치금지','invalid',lambda x:(measure(x),C(x)['measurement'].update(value=float('nan'))),'NaN')
    add('Infinity수치금지','invalid',lambda x:(measure(x),C(x)['measurement'].update(value=float('inf'))),'Infinity')
    add('음수불확실성금지','invalid',lambda x:(measure(x),C(x)['measurement'].update(uncertainty=-1)),'schema')
    add('문맥을지지로세탁금지','invalid',lambda x:(observed(x),C(x)['evidence_links'][0].update(role='context')),'support 근거 필요')
    add('같은근거지원반대중복금지','invalid',lambda x:C(x)['evidence_links'].append({'ref':ref(E(x)),'role':'oppose'}),'중복 role')
    add('반대근거검수목록유지','queue',lambda x:(observed(x),C(x)['evidence_links'].append({'ref':ref(add_frame(x,n=1)[0]),'role':'oppose'})))
    add('specimen검수는사실승인아님','queue',lambda x:(observed(x),review(x)),content_state='example_only')
    add('합성에humanreceipt금지','invalid',lambda x:(observed(x),review(x).update(kind='human')),'합성 시험')
    add('검수주장버전다름','invalid',lambda x:(observed(x),review(x)['claim_ref'].update(version='0.2.0')),'검수 주장 버전')
    add('검수후주장내용수정','stale',lambda x:(observed(x),review(x),C(x).update(statement='바뀐 문장')))
    add('검수후대상label수정같은version','stale',lambda x:(observed(x),review(x),x['targets'][-1].update(label='다른 대상')))
    add('검수후근거selector수정','stale',lambda x:(observed(x),review(x),E(x).update(limitations='근거 제한 변경')))
    add('실제draft분기humanreceipt 자기일관성','valid',lambda x:(observed(x),review(x,real=True)),content_state='declared_supported')
    add('실제draft 미검토 내용사람에게대기','queue',lambda x:(observed(x),real_branch(x)))
    add('실제draft 접근불명확supported금지','invalid',lambda x:(observed(x),x['materials'][-1].update(availability='unknown'),review(x,real=True)),'미해결 근거')
    add('실제draft 좌표미해결 수치supported금지','invalid',lambda x:(measure(x),review(x,real=True)),'미해결 근거')
    add('실제draft 가설supported승격금지','invalid',lambda x:(C(x).update(support_mode='hypothesis'),review(x,real=True)),'가설/미관측')
    add('검수ref만있고receipt없음','invalid',lambda x:C(x).update(review_ref='NONE'),'없는 사람 검수')
    add('검수datetime무효','invalid',lambda x:(observed(x),review(x).update(reviewed_at='yesterday')),'schema')
    add('미관측예시actualdraft혼합금지','invalid',real_branch,'미관측 설명 예시')
    add('metadataevidenceID실재','invalid',lambda x:x['time_contract']['timelines'][0]['origin'].update(evidence_refs=['NONE']),'메타 근거 ID 없음')
    add('시간원점대응불일치','invalid',lambda x:x['time_contract']['frames'][0].update(actual=frac(2)),'PTS 변환')
    add('속도단위kg오용','invalid',lambda x:(measure(x),C(x)['measurement'].update(unit='kg')),'단위 차원')
    add('속도표본에시간단위오용','invalid',lambda x:(measure(x),C(x)['measurement'].update(sample_unit='s')),'위치 단위')
    add('standard불확실성은절대상한과구분','queue',lambda x:(measure(x),C(x)['measurement'].update(uncertainty_kind='standard_uncertainty')))
    add('불확실성미상보존','queue',lambda x:(measure(x),C(x)['measurement'].update(uncertainty_kind='unknown',uncertainty=None)))
    add('미상불확실성을0으로채움','invalid',lambda x:(measure(x),C(x)['measurement'].update(uncertainty_kind='unknown',uncertainty=0)),'미상 불확실성')
    add('알려진불확실성인데값없음','invalid',lambda x:(measure(x),C(x)['measurement'].update(uncertainty=None)),'값 필요')
    add('clipselector instant로runtime예외금지','invalid',lambda x:(observed(x),C(x).update(evidence_links=[{'ref':ref(clip(x)),'role':'support'}]),E(x)['selector'].update(period_ref='EX-INSTANT')),'range 필요')
    add('변화주장을순간으로기록금지','invalid',lambda x:(observed(x),C(x).update(aspect='temporal_change',evidence_links=[{'ref':ref(clip(x)),'role':'support'}])),'range 범위')
    add('다른시간반대근거는문맥','invalid',lambda x:(observed(x),C(x)['evidence_links'].append({'ref':ref(add_frame(x)[0]),'role':'oppose'})),'반대 프레임')
    add('원본영상접근불명확supported우회금지','invalid',lambda x:(observed(x),x['materials'][0].update(availability='missing'),review(x,real=True)),'미해결 근거')
    add('메타근거를화살표frame으로대체금지','invalid',lambda x:x['time_contract']['timelines'][0]['origin'].update(evidence_refs=['EV-FRAME']),'시간 메타 근거는')
    add('음수폭금지','invalid',lambda x:(measure(x,'width',1),C(x)['measurement'].update(value=-1)),'음수 결과')
    add('가속도는signed음수허용','queue',lambda x:(measure(x,'average_acceleration',3,'acceleration'),C(x)['measurement'].update(value=-100)))
    add('시간메타원문없음supported금지','invalid',lambda x:(observed(x),x['materials'][1].update(text=None),review(x,real=True)),'미해결 근거')
    add('시나리오원문없음supported금지','invalid',lambda x:(C(x).update(support_mode='scenario_supported',aspect='scenario_content',evidence_links=[{'ref':ref(text_evidence(x)[0]),'role':'support'}]),x['materials'][-1].update(text=None),review(x,real=True)),'미해결 근거')
    add('other량으로좌표미검증우회금지','invalid',lambda x:(measure(x,'position_x',1),C(x)['measurement'].update(quantity='other'),review(x,real=True)),'미해결 근거')
    add('other량초안은사람에게대기','queue',lambda x:(measure(x,'position_x',1),C(x)['measurement'].update(quantity='other')))
    def add_period(x,id,start,end):x['time_contract']['periods'].append({'id':id,'timeline_ref':'EX-TIME','parent_ref':None,'kind':'range','start':frac(start),'end':frac(end),'uncertainty':frac(0),'unknown_reason':None})
    def clip_mat(x,id,p,parent=None):
        m=copy.deepcopy(x['materials'][2]);m.update(id=id,kind='clip',frame_ref=None,period_ref=p,parent_ref=parent or pin(x['materials'][0]));x['materials'].append(m);return m
    def short_parent(x):
        add_period(x,'P-SHORT',0,1);m=clip_mat(x,'MAT-PARENT','P-SHORT');x['materials'][2]['parent_ref']=pin(m)
    add('frame은부모clip끝점소속이아님','invalid',short_parent,'부모 clip 시간 밖')
    def nested_clip(x):
        add_period(x,'P-SHORT',0,1);add_period(x,'P-LATER',2,3)
        parent=clip_mat(x,'MAT-PARENT','P-SHORT');clip_mat(x,'MAT-CHILD','P-LATER',pin(parent))
    add('자식clip범위는부모clip안','invalid',nested_clip,'부모 clip 범위 밖')
    def copied_frame(x,same=False):
        if same:
            m=copy.deepcopy(x['materials'][2]);m.update(id='MAT-COPY',parent_ref=pin(x['materials'][2]));x['materials'].append(m)
        else:
            e,f=add_frame(x);x['materials'][-1]['parent_ref']=pin(x['materials'][2])
    add('부모frame사본은같은sourceidentity필수','invalid',copied_frame,'같은 원본 frame identity')
    add('같은frameref사본은보존','queue',lambda x:copied_frame(x,True))
    def later_clip(x,role='oppose'):
        add_period(x,'P-LATER',4,5);e=clip(x);e['target_ref']=ref(x['targets'][0]);e['selector']['period_ref']='P-LATER';C(x)['evidence_links'].append({'ref':ref(e),'role':role})
    add('다른시간opposeclip을해결문구로우회금지','invalid',lambda x:(observed(x),later_clip(x),review(x,real=True).update(conflict_resolution='가짜 해결 문구')),'겹치지 않음')
    add('다른시간clip문맥은대기보존','queue',lambda x:(observed(x),later_clip(x,'context')))
    def later_text(x):
        e,m=text_evidence(x,'transcript');m.update(parent_ref=pin(x['materials'][0]));add_period(x,'P-LATER',4,5);m['period_ref']='P-LATER';e['selector']['period_ref']='P-LATER';e['target_ref']=ref(x['targets'][0]);C(x).update(support_mode='scenario_supported',aspect='scenario_content',evidence_links=[{'ref':ref(e),'role':'support'}])
    add('명시시간transcript다른시점으로세탁금지','invalid',lambda x:(later_text(x),review(x,real=True)),'겹치지 않음')
    add('stale라도draft의specimenreceipt금지','invalid',lambda x:(observed(x),review(x,real=True).update(kind='specimen',context_sha256='f'*64)),'specimen 검수')
    def aliased_copy(x,unknown=False):
        e,f=add_frame(x,n=1,ordinal=25)
        if unknown:f['source_frame_ordinal']=None
        x['materials'][-1]['parent_ref']=pin(x['materials'][2]);C(x)['evidence_links']=[{'ref':ref(e),'role':'support'}]
    add('같은원본identity의다른frameID별칭보존','queue',lambda x:(observed(x),aliased_copy(x)))
    add('별칭ordinal미상은검수대기','queue',lambda x:(observed(x),aliased_copy(x,True)))
    add('별칭identity미확인supported우회금지','invalid',lambda x:(observed(x),aliased_copy(x,True),review(x,real=True)),'미해결 근거')
    add('unpaired highsurrogate 구조오류','invalid',lambda x:(observed(x),review(x,real=True).update(context_sha256='f'*64),C(x).update(statement='broken:'+chr(0xD800))),'surrogate')
    add('unpaired lowsurrogate 원문거부','invalid',lambda x:x['materials'][1].update(text=chr(0xDC00)),'surrogate')
    add('surrogate JSONkey 안전한오류표시','invalid',lambda x:x.update({chr(0xD800):'bad key'}),'surrogate key')
    add('정상emoji문장은유지','queue',lambda x:C(x).update(statement='화살표🙂가 있다는 가상 예시'))
    add('NFC한글인용보존','queue',lambda x:C(x).update(support_mode='scenario_supported',aspect='scenario_content',evidence_links=[{'ref':ref(text_evidence(x,text='가각')[0]),'role':'support'}]))
    add('NFD한글인용정규화없이보존','queue',lambda x:C(x).update(support_mode='scenario_supported',aspect='scenario_content',evidence_links=[{'ref':ref(text_evidence(x,text='가각')[0]),'role':'support'}]))
    return out
def run(checker,schema):
    results=[]
    for c in cases(checker):
        r=checker.validate(c['record'],schema);kind=c['kind']
        passed=r['valid'] if kind!='invalid' else not r['valid']
        if kind=='queue':passed=passed and bool(r['human_review_queue'])
        if kind=='stale':passed=passed and any(s['content_review_state']=='stale' for s in r['claim_states']) and bool(r['human_review_queue'])
        if c['expected_error_fragment']:
            needle=c['expected_error_fragment'];passed=passed and (bool(r['errors']) if needle=='schema' else any(needle in e for e in r['errors']))
        if c['expected_content_state']:passed=passed and any(s['content_review_state']==c['expected_content_state'] for s in r['claim_states'])
        passed=passed and not r['fact_verified'] and not r['operational_release'] and not r['company_approved']
        results.append({k:v for k,v in c.items() if k!='record'}|{'passed':passed,'result':r})
    return {'scope':'合成 contract fixture만 검사. actualdraft 분기도 메모리 가짜자료. 사실/실측/사람정체성/회사승인 검증 아님.'.replace('合成','합성'),'count':len(results),'passed':sum(x['passed'] for x in results),'all_passed':all(x['passed'] for x in results),'cases':results}
if __name__=='__main__':
    b=Path(__file__).resolve().parents[1];checker=load_checker(b/'07_실행도구/근거주장_규격검사.py');schema=json.loads((b/'04_기록규격/근거주장_스키마.json').read_text(encoding='utf-8'));r=run(checker,schema)
    print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(0 if r['all_passed'] else 1)
