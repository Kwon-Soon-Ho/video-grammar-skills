"""Validate provenance, expanded issue scope and selection boundaries, not video truth."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
import json,sys,collections
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(WORK/'internal-video-audit-20261019/candidate/company-video-grammar-analyzer/scripts'))
from check_record import load,digest,check,need
from pattern_library import validate_library,select
from source_coverage import summarize
cat=load(HERE/'evidence-catalog.json');rows=[]
def test(name,ok):rows.append({'name':name,'passed':bool(ok)});assert ok,name
def validate_expanded(ledger):
 counts=collections.Counter()
 for item in ledger['issues']:
  records=[]
  for key in ['before','after']:
   p=item[key];need(digest(p['path'])==p['sha256'],'expanded record changed');d=load(p['path']);need(not check(d,cat),'invalid expanded record');records.append(d)
  before,after=records;need(before['source']==after['source'],'expanded source mismatch')
  need(after['window_seconds'][0]<=before['window_seconds'][0]<before['window_seconds'][1]<=after['window_seconds'][1],'expanded window must contain before')
  b=next(u for u in before['unknowns'] if u['id']==item['before']['unknown_id']);a=next(u for u in after['unknowns'] if u['id']==item['after']['unknown_id'])
  claims={c['id']:c for c in after['claims']};need(all(c in claims and claims[c]['content_review']=='supported' for c in item['answer_claim_ids']),'unsupported answer claims')
  if item['state']=='addressed_with_limits':
   need(a['state']=='resolved','cannot close an open unknown')
   need(all(claims[c]['object_id']==b['object_id'] and claims[c]['basis_kind']==b['required_basis_kind'] for c in item['answer_claim_ids']),'wrong answer target or basis')
  elif item['state']=='partial':need(a['state']=='open' and bool(a['next_probe']),'partial must stay open with next probe')
  else:raise ValueError('invalid issue state')
  counts[item['state']]+=1
 need(dict(counts)==ledger['counts'],'issue counts differ')
 return dict(counts)
ledger=load(HERE/'expanded-review-ledger.json');test('expanded_scope_and_4_answers_1_partial',validate_expanded(ledger)=={'addressed_with_limits':4,'partial':1})
v=deepcopy(ledger);v['issues'][1]['state']='addressed_with_limits';error=''
try:validate_expanded(v)
except ValueError as e:error=str(e)
test('cannot_close_partial_with_related_but_incomplete_evidence','cannot close' in error)
v=deepcopy(ledger);v['issues'][2]['answer_claim_ids']=['c035'];error=''
try:validate_expanded(v)
except ValueError as e:error=str(e)
test('cannot_close_label_question_with_background_claim','wrong answer target' in error)
lib=load(HERE/'knowledge/pattern-library.json');validate_library(lib)
old=load(WORK/'skill-pattern-linking-20261019/knowledge/pattern-library.json')
test('preserve_six_prior_definitions_exactly',lib['patterns'][:6]==old['patterns'])
for code in ['NEW-N','NEW-P']:
 base=load(HERE/'records'/code/'observations.json');linked=load(HERE/'records'/code/'observations-linked.json')
 test(code+'_source_and_composition_pass',not check(base,cat) and not check(linked,cat))
 test(code+'_draft_not_whole_content_accepted',linked['review']['claim_denominator_complete'] is False and all(p['match_status']=='candidate' for p in linked['pattern_refs']))
 if code=='NEW-N':
  a,b=[p for p in linked['pattern_refs'] if p['id'] in ['left-label','right-label']];test('shared_label_definition_with_current_differences',a['pattern_id']==b['pattern_id'] and a['current_claim_ids']!=b['current_claim_ids'])
 else:
  a,b=[p for p in linked['pattern_refs'] if p['id'] in ['row1','row2']];test('shared_row_definition_with_distinct_evidence',a['pattern_id']==b['pattern_id'] and a['current_claim_ids']!=b['current_claim_ids'])
selected=[]
for pattern in lib['patterns'][6:]:
 value=select(HERE/'knowledge/pattern-library.json',pattern['id']);test(pattern['id']+'_selection_scope_and_source_pin',set(c['id'] for c in value['source_claims'])==set(pattern['source']['claim_ids']))
 selected.append({'pattern_id':pattern['id'],'claim_count':len(value['source_claims']),'evidence_count':len(value['source_evidence']),'unknown_count':len(value['source_unknowns'])})
cov=summarize(load(HERE/'source-coverage.json'),cat)
test('only_28_recorded_seconds_not_scout_context',cov['recorded_union_seconds']=='28' and cov['outside_recorded_windows_seconds']=='75284/125')
trace=load(HERE/'adoption-trace-draft8.json')
test('all_41_source_pins_still_match',len(trace['records'])==41 and all(digest(r['upstream']['local_path'])==r['upstream']['sha256'] for r in trace['records']))
prior=load(WORK/'internal-video-audit-20261019/publication-receipt.json')
test('prior_335_local_published_files_unchanged',all(digest(f['source'])==f['sha256'] for f in prior['published_files']))
test('active_draft8_skill_unchanged',all(digest(Path(prior['working_skill'])/f['relative'])==f['sha256'] for f in prior['new_working_files']))
result={'all_passed':True,'check_count':len(rows),'checks':rows,'selection_scopes':selected,'source_coverage':cov,'scope':'Provenance, declared coverage, expanded issue status and selective references. Not semantic video accuracy, independent evaluation, company acceptance, or whole research adoption.','manual_visual_review':'same_agent_context','third_party_tests_executed':False,'runtime_skill_changed':False}
(HERE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'all_passed':True,'checks':len(rows),'runtime_skill_changed':False,'video_quality_score':None},ensure_ascii=False))
