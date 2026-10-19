from pathlib import Path
import importlib.util,json,hashlib,shutil
O=Path(__file__).resolve().parent;L=O.parents[2];P=L/'R8_후보연결확인.py';source=L/'R8_04_독립검토/후보문맥_자체검사_v3/정상/Phase00'
s=importlib.util.spec_from_file_location('r8_v3_independent',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def snap(root):return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
before=snap(source);W=O/'targeted_v3';assert not W.exists();results=[]
def mutate(root,rel,fn):
 d=read(root/rel);fn(d);write(root/rel,d);c=read(root/m.CONTEXT);c['files'][rel]=sha(root/rel);write(root/m.CONTEXT,c)
def test(name,expected,fn=None):
 root=W/name/'Phase00';shutil.copytree(source,root)
 if fn:fn(root)
 prior=snap(root);r=m.inspect(root);results.append({'name':name,'expected_valid':expected,'result':r,'expectation_met':r['valid']==expected,'inputs_unchanged':prior==snap(root)})
test('normal',True)
test('empty_errata_records_after_repin',False,lambda r:mutate(r,m.EXTRA[0],lambda e:e.update(records=[])))
test('errata_company_approval_after_repin',False,lambda r:mutate(r,m.EXTRA[0],lambda e:e.update(company_approved=True)))
test('errata_operational_release_after_repin',False,lambda r:mutate(r,m.EXTRA[0],lambda e:e.update(operational_release=True)))
test('duplicate_receipt_tool_after_repin',False,lambda r:mutate(r,m.EXTRA[3],lambda e:e.update(read_checks=[e['read_checks'][0]]*4)))
test('bool_exit_after_repin',False,lambda r:mutate(r,m.EXTRA[3],lambda e:e['read_checks'][0].update(exit_code=False)))
test('missing_required_correction_after_repin',False,lambda r:mutate(r,m.EXTRA[0],lambda e:e['records'].pop()))
test('receipt_permission_claim_after_repin',False,lambda r:mutate(r,m.EXTRA[3],lambda e:e.update(permission_granted=True)))
test('receipt_behavior_claim_after_repin',False,lambda r:mutate(r,m.EXTRA[3],lambda e:e.update(candidate_behavior_evaluated=True)))
test('float_exit_after_repin',False,lambda r:mutate(r,m.EXTRA[3],lambda e:e['read_checks'][0].update(exit_code=0.0)))
def overflow(root):
 p=root/m.CONTEXT;t=p.read_text(encoding='utf-8');p.write_text(t.replace('{','{"unused_numeric_metadata":1e999,',1),encoding='utf-8')
test('overflow_unused_metadata_observation',True,overflow)
summary=read(L/'R8_04_독립검토/후보문맥_자체검사_v3/자체검사_종합.json')
data={'checker_sha256':sha(P),'author_v3_condition_count':len(summary['cases']),'author_v3_checker_matches':summary['checker_sha256']==sha(P),'independent_targeted_cases':results,'all_expectations_met':all(x['expectation_met'] for x in results),'source_v3_normal_unchanged':before==snap(source),'scope':'normal+5 reported flaws+4 related boundaries+1 known nonblocking unused-number observation; model trials0','D_not_written':True}
(O/'06_v3_표적재확인.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'sha256':data['checker_sha256'],'author_conditions':data['author_v3_condition_count'],'independent':len(results),'all_expected':data['all_expectations_met'],'unchanged':data['source_v3_normal_unchanged']},ensure_ascii=False))
