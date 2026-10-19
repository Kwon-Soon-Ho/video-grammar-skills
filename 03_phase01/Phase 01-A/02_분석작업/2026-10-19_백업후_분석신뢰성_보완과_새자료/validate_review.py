from pathlib import Path
from copy import deepcopy
import json,sys
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(HERE/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import load,digest,check
from review_ledger import validate
OUT=HERE/'validation-review';OUT.mkdir(exist_ok=True);results=[]
def test(name,condition,detail=''):
    results.append({'name':name,'passed':bool(condition),'detail':detail});assert condition,(name,detail)
for case in ('H03','H04'):
    ledger=load(HERE/'cases-r3'/case/'review-ledger.json');cat=load(HERE/'cases-r3'/case/'catalog.json');result=validate(ledger,cat)
    test(case+'_pinned_corrections_and_provenance',result['structure_passed'])
    test(case+'_same_context_not_independent',result['reviewer_kind']=='same_agent_context' and result['independence_verified_by_tool'] is False and result['content_truth_verified_by_tool'] is False)
ledger=load(HERE/'cases-r3/H04/review-ledger.json');cat=load(HERE/'cases-r3/H04/catalog.json')
before=digest(ledger['before']['path']);after=digest(ledger['after']['path'])
def reject(name,mutation,expected,mutate_record=None):
    value=deepcopy(ledger);mutation(value)
    if mutate_record:
        record=load(value['after']['path']);mutate_record(record);p=OUT/(name+'.json');p.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');value['after']={'path':str(p),'sha256':digest(p)}
    error=''
    try:validate(value,cat)
    except (ValueError,KeyError,TypeError,OSError) as exc:error=str(exc)
    test(name,expected in error,error)
reject('changed_before_pin',lambda x:x['before'].update(sha256='0'*64),'before observation changed')
reject('changed_after_pin',lambda x:x['after'].update(sha256='0'*64),'after observation changed')
reject('open_is_not_closed',lambda x:x['findings'][0].update(state='open',resolution_claim_ids=['c017'],next_probe='추가 표본'),'unfinished or excluded')
reject('addressed_needs_claim',lambda x:x['findings'][0].update(resolution_claim_ids=[]),'addressed without correction')
reject('unrelated_target_cannot_close',lambda x:x['findings'][0].update(resolution_claim_ids=['c021']),'unrelated correction claim')
reject('all_required_dimensions_must_be_covered',lambda x:x['findings'][0]['requirements'].append({'object_id':'mini-halo','property':'size','dimension':'halo-area'}),'missing required correction')
reject('unchanged_fact_cannot_close',lambda x:x['findings'][0].update(requirements=[{'object_id':'caption','property':'text','dimension':'caption-before'}],resolution_claim_ids=['c019']),'unchanged prior claim')
reject('inference_cannot_satisfy_observed_request',lambda x:None,'supported matching basis',lambda x:next(c for c in x['claims'] if c['id']=='c017').update(basis_kind='inferred'))
reject('uncertain_fact_cannot_close',lambda x:None,'supported matching basis',lambda x:next(c for c in x['claims'] if c['id']=='c017').update(content_review='uncertain'))
reject('other_case_is_not_revision',lambda x:None,'review scope changed',lambda x:x.update(case_id='OTHER-CASE'))
reject('revision_bool_is_invalid',lambda x:x.update(revision=True),'review revision')
old=load(ledger['before']['path']);test('draft6_source_not_current_pass',bool(check(old)));test('draft6_source_remains_readable',not check(old,allow_historical=True))
test('original_before_after_preserved',digest(ledger['before']['path'])==before and digest(ledger['after']['path'])==after)
out={'scope':'feedback correction pins, required target/field/basis, unfinished status and historical version boundaries. No visual truth or independent assessment.','passed':sum(r['passed'] for r in results),'total':len(results),'tests':results}
(OUT/'checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='tests'},ensure_ascii=False))
