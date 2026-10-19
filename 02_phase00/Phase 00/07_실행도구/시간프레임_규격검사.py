"""R4-1 시간 규격의 형식/의미 검사. 미디어·파일·근거 진실을 검사하지 않는다."""
import json
from pathlib import Path
from fractions import Fraction
from jsonschema import Draft202012Validator
BASE=Path(__file__).resolve().parents[1]
def q(value):
    return None if value is None else Fraction(value['num'],value['den'])
def validate(data, schema=None):
    if schema is None: schema=json.loads((BASE/'04_기록규격/시간프레임_스키마.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    def leaf_errors(e):
        if e.context:
            for child in e.context: yield from leaf_errors(child)
        else:
            msg=e.message if len(e.message)<=320 else e.message[:160]+' … '+e.message[-160:]
            yield f"{list(e.absolute_path)} [{e.validator}]: {msg}"
    errors=[msg for e in Draft202012Validator(schema).iter_errors(data) for msg in leaf_errors(e)]
    unresolved=[]
    def err(label,msg): errors.append(label+': '+msg)
    def pending(label,msg): unresolved.append(label+': '+msg)
    # JSONSchema integer는 정수 값 float도 허용한다. 원본 정수 필드는 타입까지 제한한다.
    def integers(value,path='record'):
        if isinstance(value,dict):
            for k,v in value.items():
                if k in ('num','den','stream_index','frame_count','source_frame_ordinal') and v is not None and type(v) is not int:
                    err(path+'.'+k,'원본 정수 타입 필요')
                integers(v,path+'.'+k)
        elif isinstance(value,list):
            for i,v in enumerate(value): integers(v,path+f'[{i}]')
    integers(data)
    if errors: return {'valid':False,'errors':errors,'unresolved':[], 'fact_verified':False}
    allids=[data['asset']['id']]+[x['id'] for k in ('timelines','periods','frames') for x in data[k]]
    if len(allids)!=len(set(allids)): err('record','ID 중복')
    ts={x['id']:x for x in data['timelines']}; ps={x['id']:x for x in data['periods']}
    streams=[(t['asset_ref'],t['stream_index']) for t in data['timelines']]
    if len(streams)!=len(set(streams)): err('record','동일 자산/스트림 중복 시간축 금지')
    for t in data['timelines']:
        id=t['id']; origin=t['origin']; dur=q(t['duration']); fps=q(t['nominal_fps'])
        if t['asset_ref']!=data['asset']['id']: err(id,'asset_ref 불일치')
        if dur is None:
            if t['duration_evidence_refs']: err(id,'미상 duration에 확인 근거 선언 금지')
            pending(id,'영상 길이 미확인')
        elif not t['duration_evidence_refs']: err(id,'duration 근거 참조 필요')
        if t['frame_rate_mode']=='cfr':
            if fps is None or fps<=0: err(id,'CFR 양수 nominal_fps 필요')
        elif fps is not None: err(id,'VFR/unknown에서 명목 FPS를 번호 환산에 사용 금지')
        if origin['method']=='verified_offset':
            if origin['pts'] is None or origin['time_base'] is None or q(origin['time_base'])<=0 or not origin['evidence_refs']:
                err(id,'원점 PTS/양수 time_base/매핑근거 필요')
        else:
            if any(origin[x] is not None for x in ('pts','time_base')) or origin['evidence_refs']: err(id,'미상 원점에 확정 매핑 선언 금지')
            pending(id,'원점 변환 미확인')
        if origin['pts'] is not None and not -(2**63)<=int(origin['pts'])<2**63: err(id,'PTS int64 범위 밖')
        if origin['pts']=='-9223372036854775808': err(id,'AV_NOPTS_VALUE는 null/unknown으로 기록')
    # ID 연결은 형식 검사 다음, 수치 계산 전 확인한다.
    for p in data['periods']:
        id=p['id']; t=ts.get(p['timeline_ref']); a=q(p['start']); b=q(p['end'])
        if t is None: err(id,'없는 시간축'); continue
        dur=q(t['duration'])
        if p['kind']=='range':
            if a is None or b is None or a>=b: err(id,'range 시작<끝 필요')
            if p['unknown_reason'] is not None: err(id,'known 구간의 unknown_reason은 null')
        elif p['kind']=='instant':
            if a is None or b is not None: err(id,'instant는 start만 기록')
            if p['unknown_reason'] is not None: err(id,'known 순간의 unknown_reason은 null')
        else:
            if a is not None or b is not None or p['unknown_reason'] is None or p['uncertainty'] is not None:
                err(id,'unknown은 시간/오차 null + 이유 필요')
            pending(id,'구간 시간 미확인')
        if dur is not None:
            if a is not None and a>=dur: err(id,'시작/순간은 영상 끝 미만')
            if b is not None and b>dur: err(id,'구간 끝은 영상 길이 이하')
        if p['kind']!='unknown' and p['uncertainty'] is None: pending(id,'경계 오차 미확인')
        elif a is not None and q(p['uncertainty']) is not None and dur is not None:
            u=q(p['uncertainty'])
            upper=(b if b is not None else a)+u
            if a-u<0 or upper>dur or (p['kind']=='instant' and upper==dur): pending(id,'오차 범위가 영상 경계를 가로지름')
        parent=ps.get(p['parent_ref'])
        if p['parent_ref'] is not None:
            if parent is None: err(id,'없는 부모 구간'); continue
            if parent['timeline_ref']!=p['timeline_ref']: err(id,'부모와 다른 시간축'); continue
            if parent['kind']=='instant': err(id,'부모는 range 또는 unknown만 가능')
            if parent['kind']=='unknown' or p['kind']=='unknown': pending(id,'부모/자식 포함 관계 미확인')
            elif parent['kind']!='range': err(id,'부모는 range 또는 unknown만 가능')
            else:
                pa=q(parent['start']); pb=q(parent['end'])
                if pa is not None and pb is not None and a is not None:
                    if a<pa or a>=pb or (b is not None and b>pb): err(id,'부모 구간 범위 밖')
                    u=q(p['uncertainty']); pu=q(parent['uncertainty'])
                    if u is None or pu is None: pending(id,'포함 관계 경계 오차 미확인')
                    else:
                        upper=(b if b is not None else a)+u
                        if a-u<pa+pu or upper>pb-pu or (p['kind']=='instant' and upper==pb-pu):
                            pending(id,'오차를 고려한 부모 소속 미해결')
            seen={id}; node=parent
            while node is not None:
                if node['id'] in seen: err(id,'부모 구간 순환'); break
                seen.add(node['id']); node=ps.get(node['parent_ref'])
    for f in data['frames']:
        id=f['id']; t=ts.get(f['timeline_ref']); a=q(f['actual']); requested=q(f['requested'])
        if t is None: err(id,'없는 시간축'); continue
        dur=q(t['duration']); origin=t['origin']; tb=q(f['time_base'])
        if dur==0: err(id,'0초 영상에는 프레임을 등록할 수 없음')
        if t['frame_count']==0: err(id,'0 프레임 시간축에 프레임 등록 금지')
        if f['source_pts'] is not None and not -(2**63)<=int(f['source_pts'])<2**63: err(id,'PTS int64 범위 밖')
        if f['source_pts']=='-9223372036854775808': err(id,'AV_NOPTS_VALUE는 null/unknown으로 기록')
        if f['pts_kind']=='unknown':
            if f['source_pts'] is not None or f['time_base'] is not None: err(id,'미상 PTS 종류에 값 선언 금지')
        elif f['source_pts'] is None or tb is None or tb<=0: err(id,'PTS 종류에 원본값/양수 time_base 필요')
        if f['mapping_state']=='mapped':
            if a is None or f['source_pts'] is None or tb is None or origin['method']!='verified_offset' or origin['pts'] is None or origin['time_base'] is None:
                err(id,'mapped에 원본 시간/확인 원점/actual 필요')
            else:
                if tb!=q(origin['time_base']): err(id,'프레임과 원점 time_base 불일치')
                expected=(int(f['source_pts'])-int(origin['pts']))*tb
                if a!=expected: err(id,'PTS 변환과 actual 불일치')
        else:
            if a is not None: err(id,'unmapped는 actual=null')
            pending(id,'프레임 재생 시각 미확인')
        if f['pts_kind']=='best_effort_estimate': pending(id,'추정 PTS — 확정 시간 근거로 승격 금지')
        if dur is not None:
            if a is not None and a>=dur: err(id,'프레임 영상 범위 밖')
            if requested is not None and requested>=dur: err(id,'요청 시점 영상 범위 밖')
        if f['source_frame_ordinal'] is not None and t['frame_count'] is not None and f['source_frame_ordinal']>=t['frame_count']: err(id,'프레임 번호가 전체 수 이상')
        if f['source_frame_ordinal'] is None: pending(id,'표시 순서 프레임 번호 미확인')
        if f['selection_policy']=='unknown': pending(id,'프레임 선택 방법 미확인')
        if f['selection_policy'] in ('at_or_after','at_or_before'):
            if a is None or requested is None: pending(id,'선택 방향 검사에 실제/요청 시각 필요')
            elif f['selection_policy']=='at_or_after' and a<requested: err(id,'at_or_after 방향 위반')
            elif f['selection_policy']=='at_or_before' and a>requested: err(id,'at_or_before 방향 위반')
        if f['selection_policy']=='nearest': pending(id,'최단 거리 여부는 전체 프레임 인덱스로 확인 필요')
        p=ps.get(f['period_ref'])
        if f['period_ref'] is None:
            if f['role']!='unassigned': err(id,'미지정 프레임 role은 unassigned')
            pending(id,'프레임 구간 소속 미지정')
        elif p is None: err(id,'없는 프레임 구간')
        else:
            if f['role']=='unassigned': err(id,'지정 구간에 unassigned 금지')
            if p['timeline_ref']!=f['timeline_ref']: err(id,'구간과 다른 시간축'); continue
            start=q(p['start']); end=q(p['end'])
            if p['kind']=='unknown' or a is None: pending(id,'프레임 소속 검사 미해결'); continue
            if start is None: continue
            if f['role']=='within_period':
                if p['kind']=='instant':
                    if a!=start: err(id,'순간과 프레임 시각 불일치')
                elif end is not None and not start<=a<end: err(id,'프레임 구간 범위 밖')
                u=q(p['uncertainty'])
                if u is None: pending(id,'프레임 소속 경계 오차 미확인')
                elif p['kind']=='range' and end is not None and (a<start+u or a>=end-u): pending(id,'프레임 경계 소속 미해결')
                elif p['kind']=='instant' and u>0: pending(id,'순간 소속 오차 미해결')
            elif f['role']=='context_before':
                if not a<start: err(id,'context_before 위치 오류')
                pending(id,'문맥 프레임은 구간 내부 근거 아님')
            else:
                if p['kind']=='range' and end is not None:
                    if a<end: err(id,'context_after 위치 오류')
                elif p['kind']=='instant' and a<=start: err(id,'context_after 위치 오류')
                pending(id,'문맥 프레임은 구간 내부 근거 아님')
    # 입력에 선언된 순서의 자기 모순만 검사한다. 실제 전체 인덱스를 재구성하지 않는다.
    for timeline_id in ts:
        ordinal_times={}
        for f in data['frames']:
            if f['timeline_ref']!=timeline_id or f['pts_kind']!='original_pts' or f['mapping_state']!='mapped' or f['source_frame_ordinal'] is None or f['actual'] is None: continue
            ordinal=f['source_frame_ordinal']; actual=q(f['actual'])
            if ordinal in ordinal_times and ordinal_times[ordinal]!=actual:
                err(f['id'],'동일 프레임 ordinal의 시각 충돌')
            else: ordinal_times[ordinal]=actual
        ordered=sorted(ordinal_times.items())
        if any(b[1]<a[1] for a,b in zip(ordered,ordered[1:])):
            err(timeline_id,'표시 순서 ordinal과 시각 역전')
    return {'valid':not errors,'errors':errors,'unresolved':list(dict.fromkeys(unresolved)), 'fact_verified':False}
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('record',type=Path)
    args=parser.parse_args(); result=validate(json.loads(args.record.read_text(encoding='utf-8')))
    print(json.dumps(result,ensure_ascii=False,indent=2)); raise SystemExit(0 if result['valid'] else 1)
