from pathlib import Path
import sys,json,copy
B=Path(__file__).resolve().parent
sys.path.insert(0,str(B/'skill-draft3/scripts'))
from evidence_catalog import catalog
from check_observations import check
from prepare import write
fixtures=json.loads((B/'root-audit/provenance-fixtures.json').read_text(encoding='utf-8'))
cat=catalog([B/'cases/A4-D/V01/실행기록.json',B/'cases/A4-G/V05/실행기록.json'])
write(B/'root-audit/test-catalog.json',cat)
results=[]
for k,d in fixtures.items():
 errors=check(d,cat);expected=k=='valid'
 results.append({'test':k,'expected_accept':expected,'errors':errors,'correct':(not errors)==expected})
conflict=copy.deepcopy(cat);f=copy.deepcopy(conflict['frames'][0]);f['source_sha256']='0'*64;conflict['frames'].append(f)
errors=check(fixtures['valid'],conflict);results.append({'test':'conflicting_catalog','expected_accept':False,'errors':errors,'correct':bool(errors)})
changed=copy.deepcopy(cat);changed['frames'][0]['sha256']='0'*64
errors=check(fixtures['valid'],changed);results.append({'test':'PNG_hash_mismatch','expected_accept':False,'errors':errors,'correct':bool(errors)})
empty={'frames':[]};errors=check(fixtures['valid'],empty);results.append({'test':'unregistered_frame','expected_accept':False,'errors':errors,'correct':bool(errors)})
write(B/'root-audit/draft3-provenance-tests.json',results)
assert all(r['correct'] for r in results),results
print('6/6 provenance behavior tests correct; no visual recognition score')
