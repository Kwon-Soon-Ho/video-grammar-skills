"""Count recorded source intervals, not visual completeness or skill adoption."""
import argparse,json
from fractions import Fraction
from pathlib import Path
from check_record import load,need,ids,refs,interval,digest,check

def union_length(spans):
    total=Fraction(0);end=None
    for a,b in sorted(spans):
        if end is None or a>end:total+=b-a;end=b
        elif b>end:total+=b-end;end=b
    return total

def summarize(d,catalog):
    need(d['schema_version']=='source-coverage-0.1','coverage schema')
    sources=ids(d['sources']);groups=ids(d['groups']);records=ids(d['records'])
    need(bool(sources) and bool(groups),'empty coverage scope')
    frames={}
    for f in catalog['frames']:
        key=str(Path(f['path']).resolve()).casefold()
        val=(f['source_sha256'],Fraction(str(f['actual_playback_seconds'])),f['sha256'])
        need(key not in frames or frames[key]==val,'conflicting catalog frame')
        frames[key]=val
    def evidence(items,source,window):
        need(isinstance(items,list) and bool(items),'missing overview evidence')
        paths=set()
        for e in items:
            key=str(Path(e['path']).resolve()).casefold();need(key not in paths,'duplicate overview evidence');paths.add(key)
            val=frames.get(key);t=Fraction(str(e['actual_seconds']))
            need(val is not None and val==(source['sha256'],t,digest(e['path'])),'overview source/time/bytes mismatch')
            need(window[0]<=t<window[1],'overview outside group')
    result=[];total_recorded=Fraction(0);total_duration=Fraction(0)
    for s in sources.values():
        duration=Fraction(str(s['duration_seconds']));need(duration>0,'source duration')
        need(len(s['sha256'])==64 and Path(s['path']).is_file(),'source pin')
        sg=sorted((g for g in groups.values() if g['source_id']==s['id']),key=lambda g:Fraction(str(g['planning_seconds'][0])))
        need(bool(sg),'source has no planning groups');cursor=Fraction(0)
        for g in sg:
            a,b=interval(g['planning_seconds'],[Fraction(0),duration])
            need(a==cursor and b>a,'planning groups must partition source without gaps or overlaps');cursor=b
            need(g['boundary_kind']=='provisional_work_partition' and bool(g['summary']) and bool(g['next_probe']),'group boundary/summary/next probe')
            evidence(g['overview_evidence'],s,[a,b])
        need(cursor==duration,'source tail unplanned')
        spans=[];open_unknowns=0;with_records=set();partial=0
        for r in records.values():
            if r['source_id']!=s['id']:continue
            need(digest(r['path'])==r['sha256'],'record bytes changed')
            obs=load(r['path']);errors=check(obs,catalog)
            need(not errors,'invalid current observation: '+str(errors))
            need(obs['source']['sha256']==s['sha256'] and Path(obs['source']['path']).resolve()==Path(s['path']).resolve(),'cross-source record')
            a,b=interval(obs['window_seconds'],[Fraction(0),duration]);spans.append((a,b))
            refs(r['group_ids'],groups,'record groups');need(bool(r['group_ids']),'record needs planning groups')
            intersect={g['id'] for g in sg if Fraction(str(g['planning_seconds'][0]))<b and a<Fraction(str(g['planning_seconds'][1]))}
            need(set(r['group_ids'])==intersect,'record group links differ from actual time intersection')
            with_records.update(intersect);open_unknowns+=sum(u['state']=='open' for u in obs['unknowns'])
            partial+=not obs['review']['claim_denominator_complete']
        recorded=union_length(spans);total_recorded+=recorded;total_duration+=duration
        result.append({'id':s['id'],'duration_seconds':str(duration),'planning_groups':len(sg),'groups_with_some_record':len(with_records),'groups_without_record':len(sg)-len(with_records),'record_count':len(spans),'recorded_union_seconds':str(recorded),'outside_recorded_windows_seconds':str(duration-recorded),'open_unknown_entries':open_unknowns,'records_with_incomplete_claim_denominator':partial})
    need(all(g['source_id'] in sources for g in groups.values()) and all(r['source_id'] in sources for r in records.values()),'unknown source')
    return {'structure_passed':True,'sources':result,'planning_groups':len(groups),'recorded_union_seconds':str(total_recorded),'outside_recorded_windows_seconds':str(total_duration-total_recorded),'total_duration_seconds':str(total_duration),'fine_review_completion':'not_assessed','source_duration_verified_by_tool':False,'discovery_completeness_verified':False,'note':'Overview samples and declared record intervals only. No completion percentage, no continuous-view claim, no quality acceptance. Unknown counts are entries, not deduplicated issues.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('coverage');p.add_argument('--catalog',required=True);p.add_argument('--out');a=p.parse_args()
    try:
        result=summarize(load(a.coverage),load(a.catalog));text=json.dumps(result,ensure_ascii=False,indent=2)
        if a.out:
            need(Path(a.out).resolve()!=Path(a.coverage).resolve(),'cannot overwrite coverage input')
            with Path(a.out).open('x',encoding='utf-8') as f:f.write(text+'\n')
        print(text)
    except (ValueError,KeyError,TypeError,OSError,ZeroDivisionError,IndexError) as e:p.exit(1,str(e)+'\n')
