"""Check A3 intermediate references; never grades recognition accuracy."""
import argparse, json, re, hashlib
from fractions import Fraction as F
from pathlib import Path

def check(d, catalog=None):
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
    parents={o['id']:o.get('parent') for o in objects}
    for oid in ids:
        visited=set();current=oid
        while current in parents and current is not None:
            if current in visited:
                errors.append('parent cycle');break
            visited.add(current);current=parents[current]
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
            if ev['status']=='observed' and times and not any(a<=t<=b for t in times):errors.append('no evidence in event range')
    for k in ['overview','secondary_details','internal_content','unresolved']:
        if k not in d['coverage']:errors.append('coverage missing '+k)
    if catalog is not None:
        entries={}
        for frame in catalog['frames']:
            key=str(Path(frame['path']).resolve()).casefold()
            identity=(frame['source_sha256'],F(str(frame['actual_playback_seconds'])),frame['sha256'])
            if key in entries and entries[key]!=identity:errors.append('conflicting catalog frame')
            entries[key]=identity
        for e in d['evidence']:
            identity=entries.get(str(Path(e['path']).resolve()).casefold())
            if identity is None:
                errors.append('frame not in verified catalog '+e['id']);continue
            source_hash,t,frame_hash=identity
            if source_hash!=d['source']['sha256']:errors.append('cross-source evidence '+e['id'])
            if t!=F(str(e['actual_seconds'])):errors.append('evidence time differs from extraction '+e['id'])
            p=Path(e['path'])
            if p.is_file():
                h=hashlib.sha256()
                with p.open('rb') as f:
                    for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
                if h.hexdigest()!=frame_hash:errors.append('evidence file changed '+e['id'])
    return errors

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--catalog');a=p.parse_args()
    try:
        catalog=json.loads(Path(a.catalog).read_text(encoding='utf-8')) if a.catalog else None
        errors=check(json.loads(Path(a.input).read_text(encoding='utf-8')),catalog)
    except (KeyError,ValueError,TypeError,ZeroDivisionError) as e:errors=['malformed input: '+str(e)]
    print(json.dumps({'structure_passed':not errors,'evidence_provenance_checked':bool(a.catalog),'content_verified':False,'errors':errors},ensure_ascii=False))
    raise SystemExit(bool(errors))
