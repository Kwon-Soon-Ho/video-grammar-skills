"""Number draft patterns without replacing entries; pin immutable library snapshots."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,tempfile,re

CATEGORIES={'TEXT','CARD','TRANSITION','FLOW','DETAIL','LAYOUT'}

def content_hash(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')).hexdigest()

def validate_library(library):
    from check_record import need
    need(library['schema_version'] in ('video-pattern-library-0.1','video-pattern-library-0.2'),'pattern library schema')
    seen=set()
    for p in library['patterns']:
        need(p['id'] not in seen,'duplicate pattern id');seen.add(p['id'])
        need(p['category'] in CATEGORIES and re.fullmatch('PAT-'+p['category']+'-[0-9]{4,}',p['id']) is not None,'pattern category/id')
        need(content_hash({k:v for k,v in p.items() if k!='sha256'})==p['sha256'],'pattern content hash mismatch')
        need(p['status']=='draft','registration cannot grant company approval')
        if 'definition' in p:
            validate_definition(p)
            need(all(x in seen and x!=p['id'] for x in p['derived_from']),'derivation must point to an earlier preserved entry')

def validate_definition(pattern):
    from check_record import need,nonempty
    definition=pattern['definition'];category=pattern['category']
    need(pattern['definition_version']=='video-pattern-definition-0.2','definition version')
    need(nonempty(definition['summary']),'missing pattern summary')
    if category=='LAYOUT':
        need(set(definition)=={'summary','canvas','groups','design_dimensions'},'layout needs its own composition definition')
        need(nonempty(definition['canvas']) and bool(definition['groups']),'layout canvas/groups')
        need(set(definition['design_dimensions'])=={'hierarchy','alignment','spacing','typography','color','background','shapes'},'layout design dimensions')
    elif category=='FLOW':
        need(set(definition)=={'summary','stages','overlap_notes','stable_context'},'flow definition')
        need(bool(definition['stages']) and nonempty(definition['stable_context']) and isinstance(definition['overlap_notes'],list),'flow stages and context')
        for stage in definition['stages']:need(nonempty(stage['name']) and bool(stage['claim_ids']) and nonempty(stage['timing']),'flow stage')
    else:
        need(set(definition)=={'summary','target_role','phases','parameters','preserve_constraints'},'independent detail definition')
        need(nonempty(definition['target_role']) and bool(definition['phases']) and bool(definition['parameters']) and bool(definition['preserve_constraints']),'detail role/phases/parameters/constraints')
        for phase in definition['phases']:
            need(nonempty(phase['name']) and nonempty(phase['property']) and nonempty(phase['observed_change']) and bool(phase['claim_ids']),'detail phase')
        for parameter in definition['parameters']:
            need(nonempty(parameter['name']) and parameter['status'] in ('observed','estimated','unknown'),'parameter status')
            need('value' in parameter and nonempty(parameter['unit_or_type']),'parameter value/unit')
            if parameter['status']=='unknown':need(parameter['value'] is None,'unknown parameter value must stay null')
    need(isinstance(pattern['derived_from'],list) and len(pattern['derived_from'])==len(set(pattern['derived_from'])),'derived_from list')

def write_atomic(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent,delete=False) as f:temporary=Path(f.name);f.write(data)
    os.replace(temporary,path)

def add(library_path,pattern_path):
    from check_record import load,need,digest,check,nonempty
    library_path=Path(library_path).resolve();pattern_path=Path(pattern_path).resolve()
    need(library_path!=pattern_path,'input pattern and library must differ')
    pattern=load(pattern_path)
    modern='definition' in pattern
    required={'category','name','source','applicability','counterexamples','status','supersedes'} | ({'definition','definition_version','derived_from'} if modern else {'design_spec','motion_spec'})
    need(set(pattern)==required,'pattern requires a complete draft definition, without assigned id/hash')
    need(pattern['category'] in CATEGORIES and nonempty(pattern['name']) and pattern['status']=='draft','category/name/draft status')
    if modern:validate_definition(pattern)
    else:
        need(set(pattern['design_spec'])=={'layout','typography','color','information_relation'},'full pattern design specification')
        need(set(pattern['motion_spec'])=={'flow','detail','timing','properties','unknowns'},'flow/detail pattern specification')
        need(all(pattern['design_spec'].values()) and all(pattern['motion_spec'][k] for k in ('flow','detail','timing','properties')),'empty first pattern detail')
    need(nonempty(pattern['applicability']) and isinstance(pattern['counterexamples'],list),'pattern applicability/counterexamples')
    source=pattern['source'];observation=Path(source['observation_path'])
    need(digest(observation)==source['observation_sha256'],'pattern source observation changed')
    record=load(observation);need(not check(record,allow_historical=True),'source record fails structure checks')
    need(record['case_id']==source['case_id'] and record['source']['sha256']==source['source_sha256'],'pattern source identity mismatch')
    claims={x['id']:x for x in record['claims']}
    need(bool(source['claim_ids']) and len(source['claim_ids'])==len(set(source['claim_ids'])) and all(c in claims and claims[c]['basis_kind']!='inferred' and claims[c]['content_review']=='supported' for c in source['claim_ids']),'pattern needs reviewed source facts')
    if modern:
        unknowns={u['id'] for u in record['unknowns']}
        need(isinstance(source['unknown_ids'],list) and len(source['unknown_ids'])==len(set(source['unknown_ids'])) and set(source['unknown_ids'])<=unknowns,'pattern unresolved source links')
        def nested_claims(value):
            if isinstance(value,dict):
                for key,item in value.items():
                    if key=='claim_ids':
                        need(isinstance(item,list) and bool(item) and set(item)<=set(source['claim_ids']),'definition claims outside pinned source scope')
                    else:nested_claims(item)
            elif isinstance(value,list):
                for item in value:nested_claims(item)
        nested_claims(pattern['definition'])
    library=load(library_path) if library_path.exists() else {'schema_version':'video-pattern-library-0.2','patterns':[]}
    validate_library(library)
    need(pattern['supersedes'] is None or any(p['id']==pattern['supersedes'] for p in library['patterns']),'supersedes unknown pattern')
    if modern:need(all(any(p['id']==identifier for p in library['patterns']) for identifier in pattern['derived_from']),'unknown derivation source')
    existing=[int(p['id'].rsplit('-',1)[1]) for p in library['patterns'] if p['category']==pattern['category']]
    identifier=f'PAT-{pattern["category"]}-{max(existing,default=0)+1:04d}'
    entry={'id':identifier,**pattern,'created_utc':datetime.now(timezone.utc).isoformat()}
    entry['sha256']=content_hash(entry);library['patterns'].append(entry);library['schema_version']='video-pattern-library-0.2'
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

def select(library_path,identifier):
    from check_record import load,need,digest
    path=Path(library_path);library=load(path);validate_library(library)
    matches=[p for p in library['patterns'] if p['id']==identifier];need(len(matches)==1,'pattern not found')
    pattern=matches[0];source=pattern['source'];need(digest(source['observation_path'])==source['observation_sha256'],'source observation changed')
    record=load(source['observation_path']);known={c['id']:c for c in record['claims']}
    need(all(c in known for c in source['claim_ids']),'pinned source claims missing')
    selected=[known[c] for c in source['claim_ids']]
    evidence_ids={e for c in selected for e in c['evidence_ids']}
    return {'pattern':pattern,'library_sha256':digest(path),'source_claims':selected,'source_evidence':[e for e in record['evidence'] if e['id'] in evidence_ids],'source_unknowns':[u for u in record['unknowns'] if u['id'] in source.get('unknown_ids',[])],'scope_note':'Selected definition only; derivation source and whole-scene patterns are not automatically applied.'}

def search(library_path,query='',category=None,limit=20):
    from check_record import load,need
    need(category is None or category in CATEGORIES,'unknown search category')
    need(isinstance(query,str) and (query.strip() or category),'provide query or category')
    need(type(limit) is int and 1<=limit<=100,'search limit must be 1..100')
    library=load(library_path);validate_library(library);tokens=query.casefold().split();results=[]
    for pattern in library['patterns']:
        if category is not None and pattern['category']!=category:continue
        searchable=' '.join([pattern['id'],pattern['name'],str(pattern.get('definition',{})),pattern['applicability']]).casefold()
        if all(token in searchable for token in tokens):results.append({'id':pattern['id'],'name':pattern['name'],'category':pattern['category'],'source_case_id':pattern['source']['case_id'],'status':pattern['status'],'pattern_sha256':pattern['sha256']})
    return {'match_method':'literal keywords and optional category; discovery only, not visual similarity or suitability judgment','total_matches':len(results),'returned':results[:limit]}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('add');p.add_argument('--library',required=True);p.add_argument('--pattern',required=True)
    p=sub.add_parser('select');p.add_argument('--library',required=True);p.add_argument('--id',required=True);p.add_argument('--out',required=True)
    p=sub.add_parser('search');p.add_argument('--library',required=True);p.add_argument('--query',default='');p.add_argument('--category',choices=sorted(CATEGORIES));p.add_argument('--limit',type=int,default=20)
    a=parser.parse_args()
    try:
        if a.command=='add':print(json.dumps(add(a.library,a.pattern),ensure_ascii=False))
        elif a.command=='search':print(json.dumps(search(a.library,a.query,a.category,a.limit),ensure_ascii=False))
        else:
            value=select(a.library,a.id);out=Path(a.out).resolve()
            need_safe=out not in (Path(a.library).resolve(),Path(value['pattern']['source']['observation_path']).resolve())
            if not need_safe:raise ValueError('selection output must not replace a library or source observation')
            data=json.dumps(value,ensure_ascii=False,indent=2).encode('utf-8');out.parent.mkdir(parents=True,exist_ok=True)
            if out.exists() and out.read_bytes()!=data:raise FileExistsError('selection output already contains different content')
            if not out.exists():
                with out.open('xb') as f:f.write(data)
            print(json.dumps({'pattern_id':a.id,'output':str(out),'source_claim_count':len(value['source_claims'])},ensure_ascii=False))
    except (KeyError,ValueError,TypeError,OSError) as e:parser.exit(1,str(e)+'\n')
