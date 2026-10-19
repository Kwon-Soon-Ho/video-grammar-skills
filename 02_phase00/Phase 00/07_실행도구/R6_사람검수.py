"""R6-3 사람 답변 접수의 구조/대상 동일성 검사. 사람 신원/내용/권한 인증 아님."""
from pathlib import Path
import copy,json,hashlib,re
from datetime import date
from jsonschema import Draft202012Validator,FormatChecker
from jsonschema.exceptions import SchemaError
import R6_출처사용검사 as source

FOLDER=source.FOLDER
LEDGER=FOLDER+'사람검수_접수대장.json'
SCHEMA=FOLDER+'사람검수_접수규격.json'
CATALOG=FOLDER+'사람검수_요청목록.json'
FIXED_INPUTS={
 'intake_policy':FOLDER+'사람검수_접수정책.json',
 'r6_sources':source.INDEX,
 'company_design':'03_한맥디자인/회사별_디자인연결_현황.json',
 'companies':'10_공용자산/회사목록.json',
 'assets':'10_공용자산/자산목록.json',
 'ci_colors':'10_공용자산/CI색상목록.json',
 'r5_policy':'05_출처와검토/R5_적용정책_결정.json',
 'r5_parameters':'03_한맥디자인/영상전용_미정항목.json',
 'skill_cards':'05_출처와검토/스킬심층검토/스킬심층검토정본.json',
 'workflow_policy_links':FOLDER+'작업정책_연결목록.json',
 'hanmac_profile':'03_한맥디자인/한맥디자인정본.json',
 'hanmac_thread':FOLDER+'한맥디자인_대화근거.json',
}
def pins(base):return {k:source.pin(base,v) for k,v in FIXED_INPUTS.items()}
def content_hash(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
def strict_pointer(data,ptr):
 if ptr=='':return data
 if not isinstance(ptr,str) or not ptr.startswith('/'):raise ValueError('JSON pointer must start with /')
 for bit in ptr[1:].split('/'):
  if re.search(r'~(?![01])',bit):raise ValueError('invalid JSON pointer escape')
  bit=bit.replace('~1','/').replace('~0','~')
  if isinstance(data,list):
   if re.fullmatch(r'0|[1-9][0-9]*',bit) is None:raise ValueError('invalid JSON array pointer index')
   data=data[int(bit)]
  elif isinstance(data,dict):data=data[bit]
  else:raise ValueError('JSON pointer traverses scalar')
 return data
def inspect(base,data=None,source_artifacts=True):
 base=Path(base).resolve();errors=[];queue=[]
 out={'structural_valid':False,'errors':errors,'queue':queue,'recorded_answer_count':0,'identity_authenticated':False,'content_verified':False,'company_approved':False,'permission_granted':False,'operational_release':False}
 try:
  d=source.read(source.local(base,LEDGER)) if data is None else copy.deepcopy(data);source.validate_json_values(d)
  if data is None and d.get('data_scope')!='actual_review_queue':raise ValueError('canonical ledger cannot be spec_test')
  schema=source.read(source.local(base,SCHEMA));Draft202012Validator.check_schema(schema)
  errors.extend('schema: '+e.message for e in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(d))
  if errors:return out
  if d['source_pins']!=pins(base):errors.append('stale_review_inputs');return out
  policies=source.read(source.local(base,FIXED_INPUTS['workflow_policy_links']))
  ids=set()
  transitive_pins={}
  for policy in policies['entries']:
   if policy['policy_id'] in ids:errors.append('duplicate_policy_id')
   ids.add(policy['policy_id']);ref=policy['source'];p=source.local(base,ref['path'])
   if source.digest(p)!=ref['sha256']:errors.append('stale_policy_source');continue
   transitive_pins[ref['path']]=ref['sha256']
   original=strict_pointer(source.read(p),ref['pointer']) if ref['kind']=='json' else p.read_text(encoding='utf-8')
   if original!=policy['original_value'] or policy['classification']!='workflow_policy' or policy['individual_content_review_performed'] is not False or policy['company_approval_created'] is not False:errors.append('invalid_workflow_policy_link')
  if d['request_catalog_pin']!=source.pin(base,CATALOG):errors.append('stale_request_catalog');return out
  catalog=source.read(source.local(base,CATALOG))
  if catalog['source_pins']!=d['source_pins'] or catalog['requests']!=d['requests']:errors.append('request_catalog_differs');return out
  request_ids=[r['request_id'] for r in d['requests']]
  if len(set(request_ids))!=len(request_ids) or set(catalog['coverage_units'])!=set(request_ids):raise ValueError('coverage request set differs')
  for rid,units in catalog['coverage_units'].items():
   if not isinstance(units,list) or not units:raise ValueError('coverage units must be nonempty list')
   ids=[]
   for unit in units:
    if not isinstance(unit,dict) or set(unit)!=set(['unit_id','meaning']) or not all(isinstance(unit[k],str) and unit[k].strip() for k in ['unit_id','meaning']):raise ValueError('invalid coverage unit')
    ids.append(unit['unit_id'])
   if len(set(ids))!=len(ids):raise ValueError('duplicate coverage unit')
  companies=source.read(source.local(base,FIXED_INPUTS['companies']))['companies']
  expected_ci={c['company_id']+':'+kind for c in companies for kind in ['latest_material','usage_guide']}
  if {x['unit_id'] for x in catalog['coverage_units']['R6-REQ-CI-STATUS']}!=expected_ci:raise ValueError('CI coverage must include latest and guide for every company')
  sr=source.inspect(base,verify_artifacts=source_artifacts)
  if not sr['structural_valid']:errors.extend('source_index: '+s for s in sr['errors']);return out
  out['source_artifact_identity_checked']=sr['artifact_identity_checked']
  requests={};events={};latest={}
  for r in d['requests']:
   if r['request_id'] in requests:errors.append('duplicate_request_id');continue
   requests[r['request_id']]=r
   if {o['key'] for o in r['options']}!=set('ABCD') or sum(o['recommended'] for o in r['options'])!=1:errors.append('four_distinct_choices_and_one_recommendation_required')
   if r['readiness']=='awaiting_response' and not r['targets']:errors.append('missing_concrete_target')
   if r['readiness']!='awaiting_response' and not r['dependency']:errors.append('missing_dependency_reason')
   for ref in r['targets']+r['evidence']:
    k=ref['source_key']
    if k not in FIXED_INPUTS:errors.append('unregistered_review_source');continue
    doc=source.read(source.local(base,FIXED_INPUTS[k]))
    strict_pointer(doc,ref['pointer'])
   if r['applicability']=='not_applicable' and not r['applicability_reason']:errors.append('missing_non_applicability_reason')
  for e in d['events']:
   eid=e['event_id'];rid=e['request_id']
   if eid in events:errors.append('duplicate_event_id');continue
   r=requests.get(rid)
   if r is None:errors.append('unknown_review_request');continue
   if e['request_version']!=r['version']:errors.append('stale_request_version')
   if e['request_sha256']!=content_hash(r):errors.append('stale_request_content')
   if e['context_sha256']!=content_hash(d['source_pins']):errors.append('stale_review_context')
   if e['origin_data_scope']!=d['data_scope']:errors.append('specimen_actual_origin_mismatch')
   if (e['provenance']['kind']=='specimen')!=(d['data_scope']=='spec_test'):errors.append('provenance_actual_scope_mismatch')
   receipt=e['reply_evidence_pin']
   if d['data_scope']=='actual_review_queue':
    if receipt is None:errors.append('actual_reply_evidence_required')
    else:
     ep=source.local(base,receipt['path'])
     if source.pin(base,receipt['path'])!=receipt:errors.append('stale_reply_evidence')
     evidence=source.read(ep);transitive_pins[receipt['path']]=receipt['sha256']
     if evidence.get('source_kind')!='actual_conversation_transcription' or evidence.get('reply')!=e['raw_reply'] or evidence.get('presented_request_sha256')!=e['request_sha256']:errors.append('reply_evidence_differs')
     if evidence.get('received_on')!=e['provenance']['received_on']:errors.append('reply_received_date_differs')
     snapshot=evidence['presented_request_snapshot'];sp=source.local(base,snapshot['path'])
     snapshot_pin={k:snapshot[k] for k in ['path','version','sha256']}
     if source.pin(base,snapshot['path'])!=snapshot_pin:errors.append('stale_presented_request_snapshot')
     presented=strict_pointer(source.read(sp),snapshot['pointer'])
     if content_hash(presented)!=evidence['presented_request_sha256']:errors.append('presented_snapshot_request_differs')
     transitive_pins[snapshot['path']]=snapshot['sha256']
   elif receipt is not None:errors.append('specimen_cannot_claim_actual_reply_evidence')
   units=catalog['coverage_units'][rid]
   expected_units={x['unit_id'] for x in units}
   covered=e['covered_scope_ids'];unresolved=e['unresolved_scope_ids'];nonapp=e['not_applicable_scope_ids']
   if len(expected_units)!=len(units) or len(set(covered+unresolved+nonapp))!=len(covered+unresolved+nonapp) or set(covered+unresolved+nonapp)!=expected_units:errors.append('scope_partition_must_cover_registered_units_once')
   if e['scope_coverage']!=('partial' if unresolved else 'full'):errors.append('scope_coverage_conflicts_with_unresolved_units')
   if nonapp and not e['applicability_reason']:errors.append('unit_non_applicability_requires_reason')
   if e['outcome']=='not_applicable' and set(nonapp)!=expected_units:errors.append('not_applicable_outcome_requires_all_units_with_reason')
   if r['readiness']!='awaiting_response':errors.append('answer_before_materials_or_adoption')
   if e['kind']=='response':
    if e['supersedes'] is not None or rid in latest:errors.append('response_requires_correction_event')
   else:
    prev=events.get(e['supersedes'])
    if prev is None or prev['request_id']!=rid or latest.get(rid)!=e['supersedes']:errors.append('invalid_event_chain')
    elif date.fromisoformat(e['provenance']['received_on'])<date.fromisoformat(prev['provenance']['received_on']):errors.append('event_date_before_parent')
   if e['kind']=='withdrawal' and e['outcome']!='withdrawn':errors.append('withdrawal_outcome_required')
   if e['kind']!='withdrawal' and e['outcome']=='withdrawn':errors.append('withdrawal_event_required')
   if e['outcome']=='not_applicable' and not e['applicability_reason']:errors.append('non_applicability_reason_required')
   if e['outcome']=='limited_statement' and not e['assessed_scope']:errors.append('limited_statement_needs_scope')
   if not e['excluded_scope']:errors.append('excluded_scope_required')
   events[eid]=e;latest[rid]=eid
  for r in requests.values():
   e=events.get(latest.get(r['request_id']))
   state=r['readiness'] if e is None else 'withdrawn' if e['kind']=='withdrawal' else 'declared_answer_recorded'
   active=e is not None and e['kind']!='withdrawal'
   queue.append({'request_id':r['request_id'],'title':r['title'],'state':state,'question':r['question'],'latest_event_id':e['event_id'] if e else None,'outcome':e['outcome'] if e else None,'covered_scope_ids':e['covered_scope_ids'] if active else [],'unresolved_scope_ids':e['unresolved_scope_ids'] if active else [x['unit_id'] for x in catalog['coverage_units'][r['request_id']]],'human_followup_required':e is None or e['outcome'] in ['needs_material','unable_to_determine','withdrawn'] or bool(e['unresolved_scope_ids']),'identity_authenticated':False,'company_approved':False})
  out['recorded_answer_count']=len([x for x in d['events'] if x['kind']!='withdrawal']) if d['data_scope']=='actual_review_queue' else 0
  out['active_declared_answer_count']=len([e for e in latest.values() if events[e]['kind']!='withdrawal']) if d['data_scope']=='actual_review_queue' else 0
  out['specimen_only']=d['data_scope']=='spec_test'
  if d['source_pins']!=pins(base):errors.append('review_inputs_changed_during_check')
  if d['request_catalog_pin']!=source.pin(base,CATALOG):errors.append('request_catalog_changed_during_check')
  for rel,h in transitive_pins.items():
   if source.digest(source.local(base,rel))!=h:errors.append('transitive_policy_changed_during_check')
  out['structural_valid']=not errors
  if errors:out['queue']=[];out['recorded_answer_count']=0
 except (OSError,ValueError,TypeError,KeyError,IndexError,AttributeError,RecursionError,SchemaError) as e:errors.append(type(e).__name__+': '+str(e))
 if errors:out['queue']=[];out['recorded_answer_count']=0;out['active_declared_answer_count']=0;out['structural_valid']=False
 return out

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,default=Path(__file__).resolve().parents[1]);args=p.parse_args();r=inspect(args.base)
 print(json.dumps(r,ensure_ascii=True,indent=2));raise SystemExit(0 if r['structural_valid'] else 1)
