"""Check A3 intermediate references; never grades recognition accuracy."""
import argparse, json, re
from fractions import Fraction as F
from pathlib import Path

def check(d):
    errors=[]
    for k in ['schema_version','case_id','source','window_seconds','method','document_mode','audio_reviewed','evidence','objects','coverage','hypotheses','limitations','files_read']:
        if k not in d: errors.append('missing '+k)
    if errors:return errors
    if d['schema_version']!='a3-observation-0.1':errors.append('schema version')
    if not re.fullmatch('[0-9a-f]{64}',d['source'].get('sha256','')):errors.append('source hash')
    lo,hi=map(lambda x:F(str(x)),d['window_seconds'])
    if not 0<=lo<hi:errors.append('window')
    evidence={}
    for e in d['evidence']:
        if e['id'] in evidence:errors.append('duplicate evidence id')
        evidence[e['id']]=e
        t=F(str(e['actual_seconds']))
        role=e.get('role')
        if role not in ['within','context_before','context_after']:errors.append('evidence role')
        if role=='within' and not lo<=t<hi:errors.append('frame outside half-open window')
        if role=='context_before' and t>=lo:errors.append('context_before boundary')
        if role=='context_after' and t<hi:errors.append('context_after boundary')
        if not Path(e['path']).is_file():errors.append('missing frame '+e['id'])
    objects=d['objects']; ids=[o['id'] for o in objects]
    if len(set(ids))!=len(ids):errors.append('duplicate object id')
    for o in objects:
        if o.get('parent') and o['parent'] not in ids:errors.append('unknown parent')
        for ev in o['events']:
            refs=ev['evidence_ids']
            if any(r not in evidence for r in refs):errors.append('dangling evidence');continue
            if ev['status']=='observed' and not refs:errors.append('observed without evidence')
            easing=ev['easing'];kind=easing['classification']
            if kind not in ['accelerate','decelerate','in_out','linear','unknown','not_applicable']:errors.append('easing label')
            times={F(str(evidence[r]['actual_seconds'])) for r in refs}
            if kind in ['accelerate','decelerate','in_out'] and len(times)<3:errors.append('curve needs three distinct times')
            if not easing.get('basis'):errors.append('missing easing basis')
            a,b=map(lambda x:F(str(x)),ev['time_seconds'])
            if not lo<=a<=b<=hi:errors.append('event outside window')
    for k in ['overview','secondary_details','internal_content','unresolved']:
        if k not in d['coverage']:errors.append('coverage missing '+k)
    return errors

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');a=p.parse_args()
    try: errors=check(json.loads(Path(a.input).read_text(encoding='utf-8')))
    except (KeyError,ValueError,TypeError,ZeroDivisionError) as e:errors=['malformed input: '+str(e)]
    print(json.dumps({'structure_passed':not errors,'content_verified':False,'errors':errors},ensure_ascii=False))
    raise SystemExit(bool(errors))
