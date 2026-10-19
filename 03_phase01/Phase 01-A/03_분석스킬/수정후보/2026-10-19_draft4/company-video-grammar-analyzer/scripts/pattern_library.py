"""Number draft patterns without replacing entries; pin immutable library snapshots."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,tempfile,re

CATEGORIES={'TEXT','CARD','TRANSITION','FLOW','DETAIL','LAYOUT'}

def content_hash(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')).hexdigest()

def validate_library(library):
    from check_record import need
    need(library['schema_version']=='video-pattern-library-0.1','pattern library schema')
    seen=set()
    for p in library['patterns']:
        need(p['id'] not in seen,'duplicate pattern id');seen.add(p['id'])
        need(p['category'] in CATEGORIES and re.fullmatch('PAT-'+p['category']+'-[0-9]{4,}',p['id']) is not None,'pattern category/id')
        need(content_hash({k:v for k,v in p.items() if k!='sha256'})==p['sha256'],'pattern content hash mismatch')
        need(p['status']=='draft','registration cannot grant company approval')

def write_atomic(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent,delete=False) as f:temporary=Path(f.name);f.write(data)
    os.replace(temporary,path)

def add(library_path,pattern_path):
    from check_record import load,need,digest,check,nonempty
    library_path=Path(library_path).resolve();pattern_path=Path(pattern_path).resolve()
    need(library_path!=pattern_path,'input pattern and library must differ')
    pattern=load(pattern_path)
    required={'category','name','source','design_spec','motion_spec','applicability','counterexamples','status','supersedes'}
    need(set(pattern)==required,'pattern requires a complete draft definition, without assigned id/hash')
    need(pattern['category'] in CATEGORIES and nonempty(pattern['name']) and pattern['status']=='draft','category/name/draft status')
    need(set(pattern['design_spec'])=={'layout','typography','color','information_relation'},'full pattern design specification')
    need(set(pattern['motion_spec'])=={'flow','detail','timing','properties','unknowns'},'flow/detail pattern specification')
    need(all(pattern['design_spec'].values()) and all(pattern['motion_spec'][k] for k in ('flow','detail','timing','properties')),'empty first pattern detail')
    need(nonempty(pattern['applicability']) and isinstance(pattern['counterexamples'],list),'pattern applicability/counterexamples')
    source=pattern['source'];observation=Path(source['observation_path'])
    need(digest(observation)==source['observation_sha256'],'pattern source observation changed')
    record=load(observation);need(not check(record),'source record fails structure checks')
    need(record['case_id']==source['case_id'] and record['source']['sha256']==source['source_sha256'],'pattern source identity mismatch')
    claims={x['id']:x for x in record['claims']}
    need(bool(source['claim_ids']) and len(source['claim_ids'])==len(set(source['claim_ids'])) and all(c in claims and claims[c]['basis_kind']!='inferred' and claims[c]['content_review']=='supported' for c in source['claim_ids']),'pattern needs reviewed source facts')
    library=load(library_path) if library_path.exists() else {'schema_version':'video-pattern-library-0.1','patterns':[]}
    validate_library(library)
    need(pattern['supersedes'] is None or any(p['id']==pattern['supersedes'] for p in library['patterns']),'supersedes unknown pattern')
    existing=[int(p['id'].rsplit('-',1)[1]) for p in library['patterns'] if p['category']==pattern['category']]
    identifier=f'PAT-{pattern["category"]}-{max(existing,default=0)+1:04d}'
    entry={'id':identifier,**pattern,'created_utc':datetime.now(timezone.utc).isoformat()}
    entry['sha256']=content_hash(entry);library['patterns'].append(entry)
    validate_library(library)
    encoded=json.dumps(library,ensure_ascii=False,indent=2,allow_nan=False).encode('utf-8')
    library_hash=hashlib.sha256(encoded).hexdigest()
    snapshot=library_path.parent/(library_path.stem+'-snapshots')/(library_hash+'.json')
    snapshot.parent.mkdir(parents=True,exist_ok=True)
    if snapshot.exists():need(snapshot.read_bytes()==encoded,'snapshot collision')
    else:
        with snapshot.open('xb') as f:f.write(encoded)
    # Recheck the mutable index before publishing so an intervening edit is not overwritten.
    prior=load(library_path) if library_path.exists() else {'schema_version':'video-pattern-library-0.1','patterns':[]}
    need(prior['patterns']==library['patterns'][:-1],'library changed during registration; retry from current snapshot')
    write_atomic(library_path,encoded)
    return {'pattern_id':identifier,'pattern_sha256':entry['sha256'],'library_snapshot_path':str(snapshot),'library_sha256':library_hash,'status':'draft','content_verified_by_tool':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('add');p.add_argument('--library',required=True);p.add_argument('--pattern',required=True)
    a=parser.parse_args()
    try:print(json.dumps(add(a.library,a.pattern),ensure_ascii=False))
    except (KeyError,ValueError,TypeError,OSError) as e:parser.exit(1,str(e)+'\n')
