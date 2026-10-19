"""Exercise actual table records and search boundaries; no visual-accuracy claim."""
from pathlib import Path
from copy import deepcopy
from hashlib import sha256
import sys,json
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(HERE/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import check,load
from pattern_library import search
results=[]
def record(name,passed,detail=''):
    results.append({'name':name,'passed':bool(passed),'detail':detail})
    assert passed,(name,detail)
for name in ('H03','H04'):
    d=load(HERE/'runs'/name/'observations.json');catalog=load(HERE/'runs'/name/'catalog.json')
    record(name+'_current_structure_and_provenance',not check(d,catalog),str(check(d,catalog)))
    record(name+'_preserved_first_pass_readable',bool(load(HERE/'runs'/name/'first-observations.json')))
d=load(HERE/'runs/H03/observations.json');catalog=load(HERE/'runs/H03/catalog.json')
keys={}
for c in d['claims']:
    key=(c['object_id'],c['property'],c['facet'],tuple(c['time_seconds']))
    keys.setdefault(key,[]).append(c)
siblings=next(v for v in keys.values() if len({c['dimension'] for c in v})>1)
record('real_table_distinct_fields_retained',len(siblings)>1 and not check(d,catalog))
value=deepcopy(d);value['claims'].append({**value['claims'][0],'id':'c-duplicate'})
record('same_dimension_duplicate_rejected',any('duplicate semantic claim' in x for x in check(value,catalog)))
value=deepcopy(d);value['claims'][0].pop('dimension')
record('missing_dimension_rejected',any('dimension' in x for x in check(value,catalog)))
value=deepcopy(d);value['claims'][0]['dimension']=' '
record('blank_dimension_rejected',any('dimension' in x for x in check(value,catalog)))
library=WORK/'skill-pattern-linking-20261019/knowledge/pattern-library.json'
before=sha256(library.read_bytes()).hexdigest();p=load(library)['patterns']
record('category_search_returns_only_detail',[r['id'] for r in search(library,category='DETAIL')['returned']]==[x['id'] for x in p if x['category']=='DETAIL'])
record('exact_id_discovery',search(library,'PAT-DETAIL-0001')['returned'][0]['id']=='PAT-DETAIL-0001')
record('all_keywords_required',not search(library,'PAT-DETAIL-0001 impossible-token-974')['returned'])
record('wrong_category_has_no_match',not search(library,'PAT-DETAIL-0001',category='TEXT')['returned'])
record('limit_retains_total',len(search(library,category='CARD',limit=1)['returned'])==1 and search(library,category='CARD',limit=1)['total_matches']==2)
for name,args in [('empty_query',{}),('unknown_category',{'category':'UNKNOWN'}),('zero_limit',{'category':'TEXT','limit':0})]:
    failed=False
    try:search(library,**args)
    except ValueError:failed=True
    record(name+'_rejected',failed)
record('search_does_not_mutate_library',sha256(library.read_bytes()).hexdigest()==before)
for item in load(HERE/'protected-before.json'):
    assert sha256(Path(item['path']).read_bytes()).hexdigest().lower()==item['sha256'].lower(),item['path']
record('all_223_protected_files_unchanged',True)
out={'scope':'record semantics and literal keyword search; not image recognition, independent content review, matching quality or reconstruction','tests':results,'passed':sum(x['passed'] for x in results),'total':len(results),'visual_accuracy_proven':False,'default_installed':False}
(HERE/'validation-changes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='tests'},ensure_ascii=False))
