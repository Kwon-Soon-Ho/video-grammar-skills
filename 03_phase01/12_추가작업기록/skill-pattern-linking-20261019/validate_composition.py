from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import sys,json
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(HERE/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import load,check,digest
from pattern_library import add,select,validate_library
from render_observations import render
OUT=HERE/'validation-composition';OUT.mkdir(exist_ok=True)
d=load(HERE/'development/H02/observations-linked.json')
catalog=load(WORK/'phase01a-a5b/trials/H02-r1-with_skill/support/evidence-catalog.json')
library_path=HERE/'knowledge/pattern-library.json';library=load(library_path);before=digest(library_path)
results=[]
def record(name,passed,detail=''):
    results.append({'name':name,'passed':bool(passed),'detail':detail});assert passed,(name,detail)
def reject(name,mutation):
    candidate=deepcopy(d);mutation(candidate);errors=check(candidate,catalog);record(name,bool(errors),str(errors))
record('valid_current_case_composition',not check(d,catalog),str(check(d,catalog)))
record('legacy_entry_preserved_exactly',library['patterns'][0]==load(WORK/'skill-revision-20261019/knowledge/pattern-library.json')['patterns'][0])
record('old_card_number_not_reassigned',next(p for p in library['patterns'] if p['id']=='PAT-CARD-0002')['definition']['target_role']=='주요 직사각형 기능 UI')
record('current_renderer_contains_all_five_patterns',all(p in render(d) for p in ('PAT-LAYOUT-0001','PAT-FLOW-0001','PAT-CARD-0002','PAT-DETAIL-0001','PAT-TEXT-0001')))
record('stored_historical_source_readable',not check(load(WORK/'skill-revision-20261019/development/H02/observations.json'),allow_historical=True))
record('historical_source_not_current_pass',bool(check(load(WORK/'skill-revision-20261019/development/H02/observations.json'))))
reject('wrong_case_composition',lambda x:x['reuse_map'].update(case_id='another'))
reject('missing_composition_with_occurrences',lambda x:x.update(reuse_map=None))
reject('unassigned_detail',lambda x:x['reuse_map']['detail_occurrence_ids'].pop())
reject('duplicate_role_assignment',lambda x:x['reuse_map']['layout_occurrence_ids'].append('ui-motion'))
reject('detail_in_layout_slot',lambda x:(x['reuse_map'].update(layout_occurrence_ids=['ui-motion']),x['reuse_map']['detail_occurrence_ids'].remove('ui-motion'),x['reuse_map']['detail_occurrence_ids'].append('layout-main')))
reject('missing_overall_flow',lambda x:x['reuse_map'].update(flow_occurrence_ids=[]))
reject('unknown_occurrence_link',lambda x:x['reuse_map']['links'][0].update(to_id='missing'))
reject('self_link',lambda x:x['reuse_map']['links'][0].update(to_id='flow-main'))
reject('bad_relation_type',lambda x:x['reuse_map']['links'][0].update(relation='maybe'))
reject('link_without_current_basis',lambda x:x['reuse_map']['links'][0].update(claim_ids=[]))
reject('cyclic_temporal_order',lambda x:x['reuse_map']['links'].extend([{'from_id':'ui-motion','to_id':'outline-motion','relation':'precedes','basis_kind':'inferred','claim_ids':['c014','c023']},{'from_id':'outline-motion','to_id':'ui-motion','relation':'precedes','basis_kind':'inferred','claim_ids':['c014','c023']}]))
reject('cyclic_containment',lambda x:x['reuse_map']['links'].append({'from_id':'ui-motion','to_id':'flow-main','relation':'contains','basis_kind':'inferred','claim_ids':['c014']}))
reject('wrong_current_object_scope',lambda x:x['pattern_refs'][3].update(object_ids=['bg']))
reject('unverified_match_not_confirmed',lambda x:x['pattern_refs'][3].update(match_status='confirmed'))
reject('missing_map_in_new_schema',lambda x:x.pop('reuse_map'))
reject('wrong_library_snapshot_pin',lambda x:x['pattern_refs'][3].update(library_sha256='0'*64))
selected=select(d['pattern_refs'][3]['library_path'],'PAT-DETAIL-0001')
record('detail_export_has_only_its_three_claims',set(c['id'] for c in selected['source_claims'])=={'c022','c023','c024'})
record('detail_export_omits_other_pattern_definitions','design_dimensions' not in selected['pattern']['definition'] and 'stages' not in selected['pattern']['definition'] and 'patterns' not in selected)
record('detail_export_evidence_is_exact_claim_union',{e['id'] for e in selected['source_evidence']}=={e for c in selected['source_claims'] for e in c['evidence_ids']})
record('detail_export_keeps_open_questions',bool(selected['source_unknowns']) and any(p['status']=='unknown' and p['value'] is None for p in selected['pattern']['definition']['parameters']))
base=load(HERE/'development/H02/input-detail.json')
def invalid_registration(name,mutation):
    value=deepcopy(base);mutation(value);path=OUT/(name+'.json');path.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8');failed=False
    try:add(library_path,path)
    except (ValueError,KeyError,TypeError):failed=True
    record(name,failed and digest(library_path)==before)
invalid_registration('definition_cannot_claim_another_source_atom',lambda x:x['definition']['phases'][0].update(claim_ids=['c001']))
invalid_registration('unknown_number_cannot_be_filled_with_zero',lambda x:x['definition']['parameters'][1].update(value=0))
invalid_registration('detail_cannot_occupy_layout_category',lambda x:x.update(category='LAYOUT'))
invalid_registration('derivation_target_must_exist',lambda x:x.update(derived_from=['PAT-DETAIL-9999']))
invalid_registration('source_unknown_must_exist',lambda x:x['source'].update(unknown_ids=['missing']))
invalid_registration('no_automatic_approval',lambda x:x.update(status='approved'))
invalid_registration('first_observation_pin_must_match',lambda x:x['source'].update(observation_sha256='0'*64))
record('registration_failures_did_not_mutate_library',digest(library_path)==before)
result={'utc':datetime.now(timezone.utc).isoformat(),'scope':'separation, composition graph, selective export, backward source references; no fresh video comparison','tests':results,'passed':sum(r['passed'] for r in results),'total':len(results),'all_passed':all(r['passed'] for r in results)}
(OUT/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='tests'},ensure_ascii=False))
