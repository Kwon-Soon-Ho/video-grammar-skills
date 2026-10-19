"""Check the declared composition of whole-case layout, flow and detail occurrences."""
from check_record import need,refs,ids,load

def check_reuse_map(d):
    need('reuse_map' in d,'missing reuse_map; use null before pattern assembly')
    mapping=d['reuse_map'];occurrences=ids(d['pattern_refs'])
    if mapping is None:
        need(not occurrences,'pattern occurrences need a whole-case composition map');return
    need(mapping['case_id']==d['case_id'],'reuse map belongs to another case')
    keys=('layout_occurrence_ids','flow_occurrence_ids','detail_occurrence_ids')
    all_ids=[]
    for key in keys:refs(mapping[key],occurrences,key);all_ids+=mapping[key]
    need(bool(mapping['layout_occurrence_ids']) and bool(mapping['flow_occurrence_ids']),'assembled case needs layout and overall flow')
    need(len(all_ids)==len(set(all_ids)) and set(all_ids)==set(occurrences),'occurrences must be assigned exactly once')
    claims=ids(d['claims']);unknowns=ids(d['unknowns']);refs(mapping['unresolved_ids'],unknowns,'composition unknowns')
    categories={}
    for oid,p in occurrences.items():
        library=load(p['library_path']);entry=next(x for x in library['patterns'] if x['id']==p['pattern_id'])
        need('definition' in entry,'whole-case composition requires separated definitions, not a legacy bundled card')
        categories[oid]=entry['category']
        need(all(claims[c]['object_id'] in p['object_ids'] for c in p['current_claim_ids']),'occurrence claims belong to another object scope')
    need(all(categories[x]=='LAYOUT' for x in mapping['layout_occurrence_ids']),'layout slot category mismatch')
    need(all(categories[x]=='FLOW' for x in mapping['flow_occurrence_ids']),'flow slot category mismatch')
    need(all(categories[x] not in ('LAYOUT','FLOW') for x in mapping['detail_occurrence_ids']),'detail slot category mismatch')
    for link in mapping['links']:
        need(link['from_id'] in occurrences and link['to_id'] in occurrences and link['from_id']!=link['to_id'],'invalid composition link')
        need(link['relation'] in ('contains','anchors_to','precedes','overlaps','accompanies'),'composition relation')
        need(link['basis_kind'] in ('observed','inferred'),'composition basis')
        refs(link['claim_ids'],claims,'composition relation claims');need(bool(link['claim_ids']),'relation needs current evidence or inference basis')
        if link['basis_kind']=='observed':need(all(claims[c]['basis_kind']!='inferred' for c in link['claim_ids']),'inference cannot prove observed relation')
    for relation in ('precedes','contains'):
        graph={x:[] for x in occurrences}
        for link in mapping['links']:
            if link['relation']==relation:graph[link['from_id']].append(link['to_id'])
        done=set();active=set()
        def visit(node):
            need(node not in active,'cyclic '+relation+' relations')
            if node in done:return
            active.add(node)
            for child in graph[node]:visit(child)
            active.remove(node);done.add(node)
        for node in graph:visit(node)
