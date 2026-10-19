"""Validate declared coverage and evidence links. Does not recognize video content."""
import argparse,hashlib,json,re
from pathlib import Path
from fractions import Fraction

PROPERTIES={'identity','text','relation','position','size','shape','visibility','color','internal_state'}
KINDS={'observed','calculated','inferred'}

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()

def load(path):
    def unique(pairs):
        d={}
        for k,v in pairs:
            if k in d:raise ValueError('duplicate JSON key: '+k)
            d[k]=v
        return d
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=unique,parse_constant=lambda s:(_ for _ in ()).throw(ValueError('nonfinite JSON number')))

def need(ok,message):
    if not ok:raise ValueError(message)

def nonempty(value):return isinstance(value,str) and bool(value.strip())
def ids(rows):
    need(isinstance(rows,list),'expected record list')
    result={}
    for row in rows:
        need(isinstance(row,dict) and nonempty(row.get('id')),'missing record id')
        need(row['id'] not in result,'duplicate id '+row['id']);result[row['id']]=row
    return result

def refs(values,known,label):
    need(isinstance(values,list) and all(isinstance(v,str) for v in values),label+' must be ID list')
    need(len(values)==len(set(values)),label+' duplicate references')
    need(all(v in known for v in values),'dangling '+label)

def interval(values,window):
    need(isinstance(values,list) and len(values)==2,'invalid time interval')
    a,b=[Fraction(str(v)) for v in values]
    need(window[0]<=a<=b<=window[1],'interval outside analysis window')
    return a,b

def _check(d,catalog):
    need(isinstance(d,dict),'expected JSON object')
    required=['schema_version','skill_version','case_id','source','window_seconds','method','document_mode','audio_reviewed','files_read','evidence','objects','observation_rows','claims','unknowns','discovery','layout','motion_groups','pattern_refs','review','handoff','limitations']
    need(all(k in d for k in required),'missing top-level fields')
    versions={'video-observation-0.2':'0.1.0-draft.4','video-observation-0.3':'0.1.0-draft.5','video-observation-0.4':('0.1.0-draft.6','0.1.0-draft.7','0.1.0-draft.8')}
    need(d['schema_version'] in versions,'unsupported observation schema')
    supported=versions[d['schema_version']];supported=(supported,) if isinstance(supported,str) else supported
    need(d['skill_version'] in supported,'skill version mismatch')
    need(nonempty(d['case_id']) and nonempty(d['method']),'missing case or method')
    need(d['document_mode'] in ('none','preproduction','reconstructed'),'document mode')
    need(type(d['audio_reviewed']) is bool,'audio_reviewed must be explicit boolean')
    need(isinstance(d['files_read'],list) and isinstance(d['limitations'],list),'files/limitations must be lists')
    need(re.fullmatch('[0-9a-f]{64}',d['source']['sha256']) is not None,'source hash')
    need(nonempty(d['source']['path']),'source path')
    window=[Fraction(str(v)) for v in d['window_seconds']]
    need(len(window)==2 and 0<=window[0]<window[1],'analysis window')
    evidence=ids(d['evidence']);objects=ids(d['objects']);rows=ids(d['observation_rows']);claims=ids(d['claims']);unknowns=ids(d['unknowns'])
    need(bool(objects) and bool(evidence),'empty objects or evidence')
    for e in evidence.values():
        t=Fraction(str(e['actual_seconds']));role=e['role']
        need(role in ('within','context_before','context_after'),'evidence role')
        need((role=='within' and window[0]<=t<window[1]) or (role=='context_before' and t<window[0]) or (role=='context_after' and t>=window[1]),'evidence boundary')
        need(Path(e['path']).is_file(),'missing evidence '+e['id'])
    if catalog is not None:
        entries={}
        for e in catalog['frames']:
            key=str(Path(e['path']).resolve()).casefold()
            value=(e['source_sha256'],Fraction(str(e['actual_playback_seconds'])),e['sha256'])
            need(key not in entries or entries[key]==value,'conflicting catalog frame');entries[key]=value
        for e in evidence.values():
            entry=entries.get(str(Path(e['path']).resolve()).casefold())
            need(entry is not None,'frame not in catalog')
            need(entry[0]==d['source']['sha256'],'cross-source evidence')
            need(entry[1]==Fraction(str(e['actual_seconds'])),'evidence time mismatch')
            need(entry[2]==digest(e['path']),'evidence bytes changed')
    for o in objects.values():
        need(nonempty(o['name']) and nonempty(o['shape_description']),'missing neutral name or visible shape')
        props=o['required_properties'];excluded=o['excluded_properties']
        need(isinstance(props,list) and len(set(props))==len(props) and 'identity' in props,'required identity/property list')
        need(isinstance(excluded,dict) and set(props).isdisjoint(excluded) and set(props)|set(excluded)==PROPERTIES,'property screening incomplete')
        need(all(nonempty(x) for x in excluded.values()),'missing exclusion reason')
        need(o['parent'] is None or o['parent'] in objects,'unknown parent')
        seen=set();current=o['id']
        while current is not None:
            need(current not in seen,'parent cycle');seen.add(current);current=objects[current]['parent']
        identity=o['identity'];refs(identity['claim_ids'],claims,'identity claims')
        need(identity['status'] in ('reviewed','unresolved'),'identity status')
        need(isinstance(identity['candidates'],list) and all(nonempty(x) for x in identity['candidates']),'identity candidates')
        if identity['status']=='reviewed':
            need(nonempty(identity['label']) and bool(identity['claim_ids']),'reviewed identity requires label and claims')
            need(all(claims[c]['object_id']==o['id'] and claims[c]['property']=='identity' and claims[c]['facet']=='identity' and claims[c]['basis_kind']=='observed' and claims[c]['content_review']=='supported' for c in identity['claim_ids']),'identity needs supported observed identification')
        else:need(identity['label'] is None,'unresolved identity cannot carry a confirmed label')
    semantic_keys=set()
    for c in claims.values():
        need(c['object_id'] in objects and c['property'] in objects[c['object_id']]['required_properties'],'claim outside declared object/property')
        a,b=interval(c['time_seconds'],window)
        dimension=c.get('dimension','')
        if d['schema_version']=='video-observation-0.4':need(nonempty(dimension),'claim dimension is required; identify the cell, field or distinct facet')
        key=(c['object_id'],c['property'],c['facet'],dimension,a,b)
        need(key not in semantic_keys,'duplicate semantic claim key');semantic_keys.add(key)
        need(c['facet'] in ('identity','value','direction','order','easing','relation','presence'),'claim facet')
        need(c['basis_kind'] in KINDS and nonempty(c['statement']),'claim basis/statement')
        need(c['content_review'] in ('not_reviewed','supported','rejected','uncertain'),'claim content review')
        refs(c['evidence_ids'],evidence,'claim evidence')
        if c['basis_kind']!='inferred':need(bool(c['evidence_ids']),'fact without evidence')
        if c['evidence_ids']:need(any(a<=Fraction(str(evidence[e]['actual_seconds']))<=b for e in c['evidence_ids']),'claim evidence outside its interval')
        if c['facet']=='easing':
            easing=c['easing'];refs(easing['basis_evidence_ids'],evidence,'easing evidence')
            need(set(easing['basis_evidence_ids'])<=set(c['evidence_ids']),'easing evidence must belong to claim')
            need(easing['classification'] in ('accelerate','decelerate','in_out','linear','unknown','not_applicable') and nonempty(easing['method']),'easing classification/method')
            if easing['classification'] in ('accelerate','decelerate','in_out'):
                need(len({Fraction(str(evidence[e]['actual_seconds'])) for e in easing['basis_evidence_ids']})>=3,'curve needs three distinct actual times')
        else:need('easing' not in c,'easing data requires easing facet')
    referenced_claims=set()
    for r in rows.values():
        need(r['object_id'] in objects and r['property'] in objects[r['object_id']]['required_properties'],'row object/property')
        a,b=interval(r['time_seconds'],window)
        refs(r['evidence_ids'],evidence,'row evidence');refs(r['claim_ids'],claims,'row claims');refs(r['unknown_ids'],unknowns,'row unknowns')
        need(r['review_state'] in ('reviewed','unresolved','not_reviewed','not_applicable'),'row review state')
        need(r['change'] in ('changed','unchanged','unknown','not_applicable'),'row change')
        if r['review_state']=='reviewed':need(bool(r['claim_ids']) and bool(r['evidence_ids']),'reviewed row lacks claims/evidence')
        if r['review_state'] in ('unresolved','not_reviewed'):need(any(unknowns[u]['state']=='open' for u in r['unknown_ids']),'unfinished row requires open unknown')
        if r['review_state']=='not_applicable':need(nonempty(r['reason']) and r['change']=='not_applicable','inapplicable row needs reason')
        for cid in r['claim_ids']:
            c=claims[cid];x,y=interval(c['time_seconds'],window)
            need(c['object_id']==r['object_id'] and c['property']==r['property'] and a<=x<=y<=b,'cross-object/property/time claim in row')
            need(set(c['evidence_ids'])<=set(r['evidence_ids']),'row missing claim evidence');referenced_claims.add(cid)
    need(referenced_claims==set(claims),'orphan claim outside observation rows')
    for o in objects.values():
        for prop in o['required_properties']:
            spans=sorted(interval(r['time_seconds'],window) for r in rows.values() if r['object_id']==o['id'] and r['property']==prop)
            cursor=window[0]
            for a,b in spans:
                need(a<=cursor,'coverage gap in '+o['id']+'/'+prop);cursor=max(cursor,b)
            need(cursor==window[1],'missing coverage row for '+o['id']+'/'+prop)
    for u in unknowns.values():
        need(u['object_id'] in objects and nonempty(u['question']) and nonempty(u['reason']),'unknown target/question/reason')
        need(u['state'] in ('open','resolved','withdrawn','out_of_scope') and u['required_basis_kind'] in KINDS,'unknown state/basis')
        refs(u['resolution_claim_ids'],claims,'resolution claims')
        if u['state']=='open':need(nonempty(u['next_probe']) and not u['resolution_claim_ids'],'open unknown needs next probe, no resolution')
        if u['state']=='resolved':
            need(bool(u['resolution_claim_ids']),'resolved without evidence')
            need(all(claims[c]['basis_kind']==u['required_basis_kind'] and claims[c]['object_id']==u['object_id'] and claims[c]['content_review']=='supported' for c in u['resolution_claim_ids']),'resolution requires supported matching evidence type and object')
    disc=d['discovery'];refs(disc['forward_evidence_ids'],evidence,'forward discovery');refs(disc['reverse_evidence_ids'],evidence,'reverse discovery');refs(disc['unresolved_ids'],unknowns,'discovery unknowns')
    layout=d['layout'];need(nonempty(layout['canvas']['aspect_ratio']) and nonempty(layout['canvas']['coordinate_system']),'layout canvas')
    states=ids(layout['states']);need(bool(states),'missing full-layout states')
    represented=set()
    for s in states.values():
        interval(s['time_seconds'],window);refs(s['evidence_ids'],evidence,'layout evidence');need(bool(s['evidence_ids']),'layout lacks evidence')
        refs(s['element_object_ids'],objects,'layout objects');represented.update(s['element_object_ids'])
        refs(s['claim_ids'],claims,'layout claims');refs(s['unresolved_ids'],unknowns,'layout unknowns');need(nonempty(s['composition']),'layout composition')
        need(set(s['design_spec'])=={'hierarchy','alignment','spacing','typography','color','background','shapes'},'full design dimensions missing')
        for spec in s['design_spec'].values():
            need(nonempty(spec['description']) and spec['basis_kind'] in KINDS and spec['precision'] in ('measured','estimated','qualitative','unknown'),'design dimension')
            refs(spec['claim_ids'],claims,'design claims')
            if spec['precision']=='unknown':need(bool(s['unresolved_ids']),'unknown design dimension needs unresolved question')
            if spec['precision']=='measured':need(all(k in spec for k in ('value','unit','coordinate_system','method','error')),'measurement metadata missing')
    need(represented==set(objects),'discovered objects missing from full layout')
    refs(layout['unresolved_ids'],unknowns,'layout unresolved')
    patterns=ids(d['pattern_refs'])
    for p in patterns.values():
        refs(p['object_ids'],objects,'pattern objects');refs(p['current_claim_ids'],claims,'current pattern claims')
        need(p['match_status'] in ('confirmed','candidate','mismatch'),'pattern match state')
        need(isinstance(p['differences'],list) and isinstance(p['unverified_dimensions'],list),'pattern differences')
        library_path=Path(p['library_path']);need(library_path.is_file() and digest(library_path)==p['library_sha256'],'library snapshot mismatch')
        from pattern_library import validate_library
        library=load(library_path);validate_library(library)
        found=[x for x in library['patterns'] if x['id']==p['pattern_id'] and x['sha256']==p['pattern_sha256']]
        need(len(found)==1,'unknown or changed pattern')
        pinned_source=found[0]['source']
        need(digest(pinned_source['observation_path'])==pinned_source['observation_sha256'],'first detailed observation changed')
        if p['match_status']=='confirmed':
            need(bool(p['current_claim_ids']) and not p['unverified_dimensions'],'unverified occurrence cannot be confirmed')
            need(all(claims[c]['basis_kind']!='inferred' and claims[c]['content_review']=='supported' for c in p['current_claim_ids']),'confirmed occurrence needs reviewed current facts')
    groups=ids(d['motion_groups']);levels=set()
    for g in groups.values():
        need(g['level'] in ('flow','detail') and nonempty(g['name']),'motion group level/name');levels.add(g['level'])
        interval(g['time_seconds'],window);refs(g['object_ids'],objects,'motion objects');refs(g['claim_ids'],claims,'motion claims');refs(g['pattern_occurrence_ids'],patterns,'motion pattern occurrences')
    need('flow' in levels,'missing overall motion flow')
    if any(r['change']=='changed' for r in rows.values()):need('detail' in levels,'changing objects need detail motion record')
    review=d['review'];refs(review['content_reviewed_claim_ids'],claims,'reviewed claims')
    judged={c['id'] for c in claims.values() if c['content_review']!='not_reviewed'}
    need(set(review['content_reviewed_claim_ids'])==judged,'review index differs from claim review states')
    need(type(review['claim_denominator_complete']) is bool and isinstance(review['remaining_scope'],list),'review completion fields')
    if review['claim_denominator_complete']:need(bool(claims) and judged==set(claims),'false complete claim denominator')
    h=d['handoff']
    if h is not None:
        for k in ('observed_claim_ids','preserve_claim_ids'):refs(h[k],claims,k)
        need(all(claims[c]['basis_kind']!='inferred' for c in h['observed_claim_ids']),'inferred claim presented as observed handoff')
        refs(h['open_unknown_ids'],unknowns,'handoff unknowns')
        for k in ('purpose','information_relation'):
            if h[k] is not None:
                need(nonempty(h[k]['text']) and h[k]['basis_kind'] in KINDS,'handoff purpose/relation');refs(h[k]['claim_ids'],claims,'handoff basis')
        for condition in h['condition_candidates']:
            need(nonempty(condition['condition']) and nonempty(condition['reason']) and condition['validation_state'] in ('untested','observed_case'),'condition candidate');refs(condition['claim_ids'],claims,'condition claims')
        for option in h['implementation_options']:
            need(option['basis_kind']=='inferred' and nonempty(option['proposal']) and nonempty(option['verification_needed']),'implementation must remain a proposal');refs(option['claim_ids'],claims,'implementation claims')

def check(d,catalog=None,allow_historical=False):
    try:
        need(isinstance(d,dict),'expected JSON object')
        need(allow_historical or (d.get('schema_version')=='video-observation-0.4' and d.get('skill_version')=='0.1.0-draft.8'),'historical record: preserved source, not a current-format pass')
        _check(d,catalog)
        if d['schema_version'] in ('video-observation-0.3','video-observation-0.4'):
            from reuse_map import check_reuse_map
            check_reuse_map(d)
        return []
    except (KeyError,TypeError,ValueError,ZeroDivisionError,OSError,IndexError,AttributeError,ImportError) as e:return [str(e)]

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--catalog');a=p.parse_args()
    try:errors=check(load(a.input),load(a.catalog) if a.catalog else None)
    except (OSError,ValueError) as e:errors=[str(e)]
    print(json.dumps({'structure_passed':not errors,'evidence_provenance_checked':bool(a.catalog) and not errors,'content_verified':False,'whole_video_coverage_verified':False,'company_approval':None,'errors':errors},ensure_ascii=False))
    raise SystemExit(bool(errors))
