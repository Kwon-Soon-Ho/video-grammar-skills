"""인위적 시간 계약의 양성/오류/미해결 시험. 실제 사내 영상의 검증이 아니다."""
import json, copy, importlib.util
from pathlib import Path
def load_checker(path):
    spec=importlib.util.spec_from_file_location('r4_time',path); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def frac(n,d=1): return {'num':n,'den':d}
def fixture():
    return {'contract_version':'0.1.0','source_type':'synthetic_example','asset':{'id':'EX-ASSET','version':'0.1.0','sha256':'0'*64},'timelines':[{'id':'EX-TIME','asset_ref':'EX-ASSET','stream_index':0,'duration':frac(10),'duration_evidence_refs':['EX-DURATION'],'origin':{'method':'verified_offset','pts':'90000','time_base':frac(1,90000),'evidence_refs':['EX-ORIGIN'],'limitations':'가상 값. 파일 존재·원점·회사 사실을 증명하지 않음.'},'frame_rate_mode':'vfr','nominal_fps':None,'frame_count':None,'limitations':'전체프레임인덱스 미제공·가상시험용'}],'periods':[{'id':'EX-SEGMENT','timeline_ref':'EX-TIME','parent_ref':None,'kind':'range','start':frac(0),'end':frac(3),'uncertainty':frac(0),'unknown_reason':None}],'frames':[{'id':'EX-FRAME','timeline_ref':'EX-TIME','period_ref':'EX-SEGMENT','role':'within_period','source_pts':'180000','pts_kind':'original_pts','time_base':frac(1,90000),'source_frame_ordinal':25,'requested':frac(1),'actual':frac(1),'mapping_state':'mapped','selection_policy':'manual','limitations':'가상 프레임. 25는 인위적 값이며 FPS 환산이 아님.'}],'notes':'합성 규격 fixture만 사용. 실제 분석/승인/파일 내용 검증 없음.'}
def cases():
    out=[]
    def add(name,kind,change,needle=None):
        x=fixture();change(x);out.append({'name':name,'kind':kind,'record':x,'expected_error_fragment':needle})
    def F(x): return x['frames'][0]
    def T(x): return x['timelines'][0]
    def P(x): return x['periods'][0]
    def at(x,n,d=1): F(x).update(actual=frac(n,d),source_pts=str(90000+n*90000//d))
    add('정상 비영점 원본PTS→재생1초','valid',lambda x:None)
    add('영상 10초 밖 프레임100초','invalid',lambda x:at(x,100),'프레임 영상 범위 밖')
    add('부모3초 밖 프레임4초','invalid',lambda x:at(x,4),'프레임 구간 범위 밖')
    add('근거 구간으로 연결할 역전9→1초','invalid',lambda x:P(x).update(start=frac(9),end=frac(1)),'시작<끝')
    add('근거 구간으로 연결할 영상밖 끝100초','invalid',lambda x:P(x).update(end=frac(100)),'영상 길이 이하')
    add('구간끝3초 내부프레임으로 오인','invalid',lambda x:at(x,3),'프레임 구간 범위 밖')
    add('구간끝3초 문맥프레임','unresolved',lambda x:(at(x,3),F(x).update(role='context_after')))
    add('끝3초는 다음구간 내부프레임','valid',lambda x:(P(x).update(start=frac(3),end=frac(5)),at(x,3)))
    add('영상끝10초 프레임','invalid',lambda x:at(x,10),'프레임 영상 범위 밖')
    add('영상끝10초 instant','invalid',lambda x:(x.update(frames=[]),P(x).update(kind='instant',start=frac(10),end=None)),'끝 미만')
    add('0길이 range','invalid',lambda x:P(x).update(end=frac(0)),'시작<끝')
    add('유효1초 instant','valid',lambda x:P(x).update(kind='instant',start=frac(1),end=None))
    add('instant끝값 추가','invalid',lambda x:P(x).update(kind='instant'),'start만')
    add('unknown 시간과 이유 보존','unresolved',lambda x:P(x).update(kind='unknown',start=None,end=None,uncertainty=None,unknown_reason='미확인'))
    add('unknown을0초로 채움','invalid',lambda x:P(x).update(kind='unknown',end=None,uncertainty=None,unknown_reason='미확인'),'시간/오차 null')
    add('unknown 이유 없음','invalid',lambda x:P(x).update(kind='unknown',start=None,end=None,uncertainty=None),'이유 필요')
    add('원점 미확인값 보존','unresolved',lambda x:(T(x)['origin'].update(method='unknown',pts=None,time_base=None,evidence_refs=[]),F(x).update(mapping_state='unmapped',actual=None)))
    add('원점미확인인데mapped','invalid',lambda x:T(x)['origin'].update(method='unknown',pts=None,time_base=None,evidence_refs=[]),'확인 원점')
    add('원점근거 비어있음','invalid',lambda x:T(x)['origin'].update(evidence_refs=[]),'매핑근거')
    add('음수 원본PTS 재생0.5초','valid',lambda x:(T(x)['origin'].update(pts='-90000'),F(x).update(source_pts='-45000',actual=frac(1,2),requested=frac(1,2))))
    add('원점보다 앞의PTS를0초라 주장','invalid',lambda x:F(x).update(source_pts='0',actual=frac(0)),'PTS 변환')
    add('다른 time_base 섞기','invalid',lambda x:F(x).update(time_base=frac(1,1000)),'time_base 불일치')
    add('29.97fps 정확분수 CFR','valid',lambda x:T(x).update(frame_rate_mode='cfr',nominal_fps=frac(30000,1001)))
    add('VFR에 고정FPS 환산','invalid',lambda x:T(x).update(nominal_fps=frac(30)),'VFR/unknown')
    add('CFR fps 없음','invalid',lambda x:T(x).update(frame_rate_mode='cfr'),'CFR 양수')
    add('프레임 수 초과 ordinal','invalid',lambda x:T(x).update(frame_count=25),'전체 수 이상')
    add('추정PTS 확정과 구분','unresolved',lambda x:F(x).update(pts_kind='best_effort_estimate'))
    add('미매핑인데actual선언','invalid',lambda x:F(x).update(mapping_state='unmapped'),'actual=null')
    add('at_or_after 앞프레임','invalid',lambda x:F(x).update(selection_policy='at_or_after',requested=frac(2)),'방향 위반')
    add('at_or_before 뒤프레임','invalid',lambda x:F(x).update(selection_policy='at_or_before',requested=frac(0)),'방향 위반')
    add('nearest 실제최근접 미증명','unresolved',lambda x:F(x).update(selection_policy='nearest'))
    add('오차로 영상밖100초 합법화 금지','invalid',lambda x:(at(x,100),P(x).update(uncertainty=frac(100))),'프레임 영상 범위 밖')
    add('오차가 프레임소속 경계 겹침','unresolved',lambda x:P(x).update(uncertainty=frac(2)))
    add('구간끝만 duration까지 허용','valid',lambda x:P(x).update(end=frac(10)))
    add('없는 시간축참조','invalid',lambda x:F(x).update(timeline_ref='NONE'),'없는 시간축')
    add('없는 부모구간참조','invalid',lambda x:P(x).update(parent_ref='NONE'),'없는 부모')
    add('자기부모 순환','invalid',lambda x:P(x).update(parent_ref='EX-SEGMENT'),'순환')
    add('다른 시간축 부모','invalid',lambda x:(x['timelines'].append({**copy.deepcopy(T(x)),'id':'OTHER','stream_index':1}),x['periods'].append({**copy.deepcopy(P(x)),'id':'CHILD','timeline_ref':'OTHER','parent_ref':'EX-SEGMENT'})),'다른 시간축')
    add('자식이 부모밖으로 나감','invalid',lambda x:x['periods'].append({**copy.deepcopy(P(x)),'id':'CHILD','start':frac(2),'end':frac(4),'parent_ref':'EX-SEGMENT'}),'부모 구간 범위 밖')
    add('unknown 부모 포함검사 미해결','unresolved',lambda x:(x['periods'].append({**copy.deepcopy(P(x)),'id':'PARENT','kind':'unknown','start':None,'end':None,'uncertainty':None,'unknown_reason':'미확인'}),P(x).update(parent_ref='PARENT')))
    add('instant 부모에 자식','invalid',lambda x:(x['periods'].append({**copy.deepcopy(P(x)),'id':'PARENT','kind':'instant','start':frac(1),'end':None}),P(x).update(parent_ref='PARENT')),'부모는 range')
    add('동일ID 중복','invalid',lambda x:F(x).update(id='EX-SEGMENT'),'ID 중복')
    add('부모없는 unassigned 프레임','unresolved',lambda x:F(x).update(period_ref=None,role='unassigned'))
    add('context_before 방향 오류','invalid',lambda x:F(x).update(role='context_before'),'위치 오류')
    add('context_after 방향 오류','invalid',lambda x:F(x).update(role='context_after'),'위치 오류')
    add('미상duration','unresolved',lambda x:T(x).update(duration=None,duration_evidence_refs=[]))
    add('0denominator 형식 오류','invalid',lambda x:F(x)['actual'].update(den=0),'[minimum]')
    add('bool 정수 위장 금지','invalid',lambda x:F(x)['actual'].update(num=True),'integer')
    add('float정수 타입 위장 금지','invalid',lambda x:F(x)['actual'].update(num=1.0),'원본 정수')
    add('NaN 기록 금지','invalid',lambda x:F(x)['actual'].update(num=float('nan')),'integer')
    add('JS safe integer 초과','invalid',lambda x:F(x)['actual'].update(num=2**53),'[maximum]')
    add('PTS int64 초과','invalid',lambda x:F(x).update(source_pts=str(2**63)),'int64 범위')
    add('PTS 문자열 초장문 금지','invalid',lambda x:F(x).update(source_pts='1'*5000),'too long')
    add('원점 AV_NOPTS_VALUE 거부','invalid',lambda x:T(x)['origin'].update(pts='-9223372036854775808'),'AV_NOPTS_VALUE')
    add('프레임 AV_NOPTS_VALUE 거부','invalid',lambda x:F(x).update(source_pts='-9223372036854775808'),'AV_NOPTS_VALUE')
    add('유효 분수 PTS→1001/30000초','valid',lambda x:(T(x)['origin'].update(pts='0',time_base=frac(1001,30000)),F(x).update(source_pts='1',time_base=frac(1001,30000),actual=frac(1001,30000),requested=frac(1001,30000))))
    add('비약분 분수도 동일시간 인정','valid',lambda x:F(x).update(actual=frac(2,2)))
    add('unknown선택 정책 확정아님','unresolved',lambda x:F(x).update(selection_policy='unknown'))
    add('nullordinal 확인누락 보존','unresolved',lambda x:F(x).update(source_frame_ordinal=None))
    add('instant 오차가 부모 제외끝점과 일치','unresolved',lambda x:(x.update(frames=[]),x['periods'].append({'id':'CHILD','timeline_ref':'EX-TIME','parent_ref':'EX-SEGMENT','kind':'instant','start':frac(2),'end':None,'uncertainty':frac(1),'unknown_reason':None})))
    add('instant 오차가 영상 제외끝점과 일치','unresolved',lambda x:(x.update(frames=[]),P(x).update(kind='instant',start=frac(9),end=None,uncertainty=frac(1))))
    add('0초영상 미매핑프레임 거부','invalid',lambda x:(T(x).update(duration=frac(0)),x.update(periods=[]),F(x).update(actual=None,mapping_state='unmapped',period_ref=None,role='unassigned',requested=None)),'0초 영상')
    add('0framecount nullordinal 거부','invalid',lambda x:(T(x).update(frame_count=0),F(x).update(source_frame_ordinal=None)),'0 프레임')
    add('동일스트림 상충시간축 거부','invalid',lambda x:x['timelines'].append({**copy.deepcopy(T(x)),'id':'ALIAS','duration':frac(20),'origin':{**T(x)['origin'],'pts':'0'}}),'중복 시간축')
    add('동일스트림 동일값alias 거부','invalid',lambda x:x['timelines'].append({**copy.deepcopy(T(x)),'id':'ALIAS'}),'중복 시간축')
    add('프레임PTS끝개행 거부','invalid',lambda x:F(x).update(source_pts='180000\n'),'[pattern]')
    add('원점PTS끝개행 거부','invalid',lambda x:T(x)['origin'].update(pts='90000\n'),'[pattern]')
    add('sha256끝개행 거부','invalid',lambda x:x['asset'].update(sha256='0'*64+'\n'),'[maxLength]')
    add('unknown자식 instant부모 거부','invalid',lambda x:(x.update(frames=[]),x['periods'].append({**copy.deepcopy(P(x)),'id':'PARENT','kind':'instant','start':frac(1),'end':None}),P(x).update(kind='unknown',start=None,end=None,uncertainty=None,unknown_reason='미확인',parent_ref='PARENT')),'부모는 range')
    add('실제 서로 다른스트림 시간축 등록','valid',lambda x:x['timelines'].append({**copy.deepcopy(T(x)),'id':'OTHER','stream_index':1,'duration':frac(20)}))
    add('동일ordinal 다른시간 충돌','invalid',lambda x:x['frames'].append({**copy.deepcopy(F(x)),'id':'SECOND','source_pts':'270000','actual':frac(2)}),'ordinal의 시각 충돌')
    add('ordinal 증가하지만시간역전','invalid',lambda x:x['frames'].append({**copy.deepcopy(F(x)),'id':'SECOND','source_frame_ordinal':26,'source_pts':'135000','actual':frac(1,2)}),'시각 역전')
    add('다른ordinal 같은PTS 임의금지 안함','valid',lambda x:x['frames'].append({**copy.deepcopy(F(x)),'id':'SECOND','source_frame_ordinal':26}))
    add('동일ordinal 동일PTS 참조공유 허용','valid',lambda x:x['frames'].append({**copy.deepcopy(F(x)),'id':'SECOND'}))
    add('두프레임 정상표시순서','valid',lambda x:x['frames'].append({**copy.deepcopy(F(x)),'id':'SECOND','source_frame_ordinal':26,'source_pts':'270000','actual':frac(2)}))
    return out
def run(checker,schema):
    results=[]
    for c in cases():
        r=checker.validate(c['record'],schema)
        passed=(r['valid'] if c['kind']!='invalid' else not r['valid'])
        if c['kind']=='valid': passed=passed and not r['unresolved']
        if c['kind']=='unresolved': passed=passed and bool(r['unresolved'])
        if c['expected_error_fragment']: passed=passed and any(c['expected_error_fragment'] in e for e in r['errors'])
        results.append({k:v for k,v in c.items() if k!='record'}|{'passed':passed,'result':r})
    return {'scope':'합성 입력의 구조·시간 계약 검사. 파일/영상/원점/추정 정확성 미검증.','count':len(results),'passed':sum(x['passed'] for x in results),'all_passed':all(x['passed'] for x in results),'cases':results}
if __name__=='__main__':
    b=Path(__file__).resolve().parents[1]
    m=load_checker(b/'07_실행도구/시간프레임_규격검사.py')
    schema=json.loads((b/'04_기록규격/시간프레임_스키마.json').read_text(encoding='utf-8'))
    result=run(m,schema); print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0 if result['all_passed'] else 1)
