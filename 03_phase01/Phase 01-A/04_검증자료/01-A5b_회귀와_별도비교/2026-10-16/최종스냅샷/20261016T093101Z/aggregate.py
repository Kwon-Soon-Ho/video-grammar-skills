from pathlib import Path
import json,datetime,math,hashlib
B=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
ref=read(B/'reference/reference.json');results=[];flags=[]
for p in sorted((B/'blind').glob('*/grading.json')):
 pair=p.parent.name;grading=read(p);mapping=read(B/'blind-mappings'/f'{pair}.json');cid=pair.split('-')[0]
 supplement=read(p.parent/'review-supplement.json') if (p.parent/'review-supplement.json').exists() else None
 truth=next(x for x in ref['criteria'] if x['case_id']==cid)['atoms'];truthids={a['id'] for a in truth}
 for label,rid in mapping.items():
  g=grading['samples'][label];ars=g.get('atom_results',[]);claims=g.get('claims',[])
  if supplement:
   sg=supplement['samples'][label];updates={x['claim_id']:x for x in sg['claim_updates']}
   for c in claims:
    if c['id'] in updates:c.update(supported=updates[c['id']]['supported'],evidence=updates[c['id']]['evidence'])
   g['scope_incomplete']=sg.get('scope_incomplete',g.get('scope_incomplete'))
  if {x['atom_id'] for x in ars}!=truthids or len(ars)!=len(truth):flags.append({'pair':pair,'sample':label,'issue':'atom count/IDs mismatch'})
  allowed={'correct','missed','wrong','avoidable_unknown'}
  if any(x['result'] not in allowed for x in ars):flags.append({'pair':pair,'sample':label,'issue':'unknown classification enum'})
  denom={t:sum(a['tier']==t for a in truth) for t in ['core','detail']}
  good={t:sum(a['tier']==t and a['result']=='correct' for a in ars) for t in ['core','detail']}
  unknown=sum(a['result']=='avoidable_unknown' for a in ars);nulls=sum(c.get('supported') is None for c in claims)
  supported=sum(c.get('supported') is True for c in claims);false=sum(c.get('supported') is False for c in claims)
  if any(c.get('supported') not in [True,False,None] for c in claims):flags.append({'pair':pair,'sample':label,'issue':'claim supported must be bool/null'})
  precision=supported/len(claims) if claims and not nulls and not g.get('scope_incomplete') else None
  cr=g.get('critical_errors',[]);v=read(B/'trials'/rid/'validation.json');incomplete=bool(g.get('scope_incomplete')) or bool(nulls) or not claims or {x['atom_id'] for x in ars}!=truthids
  metrics={'core_correct':good['core'],'core_total':denom['core'],'detail_correct':good['detail'],'detail_total':denom['detail'],'core_coverage':good['core']/denom['core'] if denom['core'] else None,'detail_coverage':good['detail']/denom['detail'] if denom['detail'] else None,'supported_enumerated_claims':supported,'total_asserted_claims':None if incomplete else len(claims),'enumerated_asserted_claims':len(claims),'unresolved_enumerated_claims':nulls,'unsupported_enumerated_claims':false,'asserted_claim_precision':precision,'avoidable_abstention_count':unknown,'avoidable_abstention_fraction':unknown/sum(denom.values())}
  passed=not incomplete and not cr and v['structure_passed'] and v['evidence_provenance_checked'] and good['core']==denom['core'] and good['detail']>=math.ceil(.9*denom['detail']) and precision is not None and supported>=math.ceil(.95*len(claims)) and unknown<=math.floor(.1*sum(denom.values()))
  r={'run_id':rid,'case_id':cid,'configuration':'without_skill' if 'without_skill' in rid else 'with_skill','repeat':int(rid.split('-r')[1][0]),'blind_label':label,'metrics':metrics,'gates_passed':bool(passed),'scope_incomplete':incomplete,'critical_errors':cr,'missing_reference_atoms':[a['atom_id'] for a in ars if a['result']=='missed'],'wrong_reference_atoms':[a['atom_id'] for a in ars if a['result']=='wrong'],'avoidable_unknown_reference_atoms':[a['atom_id'] for a in ars if a['result']=='avoidable_unknown'],'appropriate_unknowns':g.get('appropriate_unknowns',[]),'grading_path':str(p),'review_seconds':grading.get('timing',{}).get('sample_review_seconds',{}).get(label),'assertion_count_unit':'deduplicated factual atoms supplied by blinded AI reviewer; not event count','structure_provenance_passed':v['structure_passed'] and v['evidence_provenance_checked']}
  results.append(r)
  # Viewer-compatible score wrapper, retaining original independent grading unchanged.
  expectations=[]
  for a in ars:
   expectations.append({'text':a['atom_id']+': '+next(t['state_or_direction_or_order'] for t in truth if t['id']==a['atom_id']),'passed':a['result']=='correct','evidence':a.get('evidence','')})
  save(B/'trials'/rid/'grading.json',{'expectations':expectations,'summary':{'passed':sum(x['passed'] for x in expectations),'failed':sum(not x['passed'] for x in expectations),'total':len(expectations),'pass_rate':sum(x['passed'] for x in expectations)/len(expectations)},'A5b_gate':r,'content_grader':'fresh blinded AI; not human gold','claim_details':g.get('claims',[])})
  if r['configuration']=='with_skill' and (cr or not r['structure_provenance_passed']):
   if not (B/'STOP.json').exists():save(B/'STOP.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'with_skill critical error or structure/provenance failure','run_id':rid,'critical_errors':cr,'source_grading':str(p),'remaining_analyses_must_not_start':True})
joint=[]
for cid in ['H01','H02','H03','H04']:
 for cfg in ['with_skill','without_skill']:
  rr=[r for r in results if r['case_id']==cid and r['configuration']==cfg]
  if len(rr)==2:
   sets=[]
   for r in rr:
    g=read(Path(r['grading_path']))['samples'][r['blind_label']]
    sets.append({a['atom_id'] for a in g['atom_results'] if a['tier']=='detail' and a['result']=='correct'})
   n=rr[0]['metrics']['detail_total'];common=len(sets[0]&sets[1]);joint.append({'case_id':cid,'configuration':cfg,'joint_correct':common,'detail_total':n,'joint_coverage':common/n if n else None,'passed':bool(n and common>=math.ceil(.9*n))})
completed=[r['run_id'] for r in read(B/'run-matrix.json') if (B/'trials'/r['run_id']/'seal.json').is_file()]
value=[]
for cid in ['H01','H02','H03','H04']:
 for rep in [1,2]:
  rr=[r for r in results if r['case_id']==cid and r['repeat']==rep]
  if len(rr)==2:
   s=next(x for x in rr if x['configuration']=='with_skill');n=next(x for x in rr if x['configuration']=='without_skill');same=s['gates_passed'] and n['gates_passed'];st=s['review_seconds'];nt=n['review_seconds']
   value.append({'pair':f'{cid}-r{rep}','both_quality_passed':same,'skill_AI_review_seconds':st,'baseline_AI_review_seconds':nt,'like_quality_AI_review_ratio':st/nt if same and isinstance(st,(int,float)) and isinstance(nt,(int,float)) and nt>0 else None,'actual_human_review_ratio':None,'note':'not a human labor or model-cost ROI; null if quality/cost incomparable'})
data={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'legacy':read(B/'legacy-decision.json'),'primary_planned':16,'primary_completed':len(completed),'primary_completed_ids':completed,'primary_graded':len(results),'primary_results':results,'repeat_joint_detail':joint,'review_value_comparison':value,'grading_integrity_flags':flags,'stopped':(B/'STOP.json').exists(),'stop':read(B/'STOP.json') if (B/'STOP.json').exists() else None,'full_comparison_complete':len(results)==16 and not flags,'default_promotion':False,'model':'parent inherited; exact host ID not exposed; no model-specific comparative claim'}
save(B/'result.json',data)
print(json.dumps({'completed':len(completed),'graded':len(results),'flags':flags,'stopped':data['stopped'],'runs':[{k:r[k] for k in ['run_id','gates_passed','scope_incomplete','metrics','critical_errors']} for r in results]},ensure_ascii=False))
