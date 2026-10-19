"""Check declared corrections against pinned before/after records; not visual truth."""
from pathlib import Path
import argparse,json
from check_record import load,digest,check,need,nonempty,ids,refs,KINDS

def validate(ledger,catalog=None):
    need(isinstance(ledger,dict) and ledger.get('schema_version')=='video-review-ledger-0.1','unsupported review ledger')
    need(type(ledger['revision']) is int and ledger['revision']>=1,'review revision')
    records=[]
    for label in ('before','after'):
        pin=ledger[label];need(digest(pin['path'])==pin['sha256'],label+' observation changed')
        value=load(pin['path']);errors=check(value,catalog if label=='after' else None,allow_historical=label=='before')
        need(not errors,label+' observation invalid: '+str(errors));records.append(value)
    before,after=records
    need(Path(ledger['before']['path']).resolve()!=Path(ledger['after']['path']).resolve(),'preserve before record in a different file')
    need(before['case_id']==after['case_id'] and before['source']==after['source'] and before['window_seconds']==after['window_seconds'],'review scope changed')
    reviewer=ledger['reviewer'];need(reviewer['kind'] in ('same_agent_context','independent_ai','human') and nonempty(reviewer['name']) and nonempty(reviewer['method']),'reviewer and actual method required')
    old=ids(before['claims']);new=ids(after['claims']);objects=ids(after['objects']);findings=ids(ledger['findings']);need(bool(findings),'empty review findings')
    counts={state:0 for state in ('open','addressed','withdrawn','out_of_scope')}
    def fact(c):return {k:v for k,v in c.items() if k not in ('id','content_review')}
    for f in findings.values():
        need(nonempty(f['question']) and nonempty(f['reason']),'finding question/reason')
        refs(f['before_claim_ids'],old,'before claims');refs(f['resolution_claim_ids'],new,'resolution claims')
        need(f['required_basis_kind'] in KINDS and f['state'] in counts,'finding basis/state');counts[f['state']]+=1
        requirements=f['requirements'];need(isinstance(requirements,list) and bool(requirements),'finding requirements')
        keys=set()
        for r in requirements:
            need(r['object_id'] in objects and r['property'] in objects[r['object_id']]['required_properties'] and nonempty(r['dimension']),'requirement outside declared target/property')
            key=(r['object_id'],r['property'],r['dimension']);need(key not in keys,'duplicate finding requirement');keys.add(key)
        if f['state']=='addressed':
            need(bool(f['resolution_claim_ids']),'addressed without correction claims')
            selected=[new[c] for c in f['resolution_claim_ids']]
            need(all(c['basis_kind']==f['required_basis_kind'] and c['content_review']=='supported' for c in selected),'correction needs supported matching basis')
            need(all((c['object_id'],c['property'],c['dimension']) in keys for c in selected),'unrelated correction claim')
            need(keys<={(c['object_id'],c['property'],c['dimension']) for c in selected},'missing required correction')
            need(all(c['id'] not in old or fact(c)!=fact(old[c['id']]) for c in selected),'unchanged prior claim cannot close a correction')
        else:
            need(not f['resolution_claim_ids'],'unfinished or excluded finding cannot carry resolution claims')
            if f['state']=='open':need(nonempty(f['next_probe']),'open finding needs next probe')
    return {'structure_passed':True,'finding_counts':counts,'reviewer_kind':reviewer['kind'],'catalog_checked':catalog is not None,'content_truth_verified_by_tool':False,'independence_verified_by_tool':False,'scope_note':'Declared feedback tracking only; no discovery completeness or whole-skill acceptance.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('ledger');p.add_argument('--catalog');a=p.parse_args()
    try:print(json.dumps(validate(load(a.ledger),load(a.catalog) if a.catalog else None),ensure_ascii=False))
    except (ValueError,KeyError,TypeError,OSError) as e:p.exit(1,str(e)+'\n')
