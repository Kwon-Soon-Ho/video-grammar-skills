import json,hashlib,importlib.util,copy,sys,tempfile,subprocess,os
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();dump=lambda x:json.dumps(x,ensure_ascii=False,indent=2).encode('utf-8')
p=B/'07_실행도구/R7_연결확인.py';spec=importlib.util.spec_from_file_location('r7_under_test',p);q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
paths=list(q.EXPECTED_PATHS)+[q.MANIFEST];raws={r:(B/r).read_bytes() for r in paths};before={r:sha(B/r) for r in paths};original_parse=q.parse
rows=[]
def record(name,kind,expect,result,exc=None):
 good=exc is None and result.get('valid') is expect
 rows.append({'name':name,'method':kind,'expected_valid':expect,'actual_valid':None if exc else result.get('valid'),'passed':good,'result':result,'runtime_exception':exc})
def memory(name,path,change,expect=False):
 d=original_parse(raws[path]);change(d)
 def parse(raw):return copy.deepcopy(d) if raw==raws[path] else original_parse(raw)
 q.parse=parse
 try:record(name,'in_memory_parser_return_fault_only_not_hash_bypass',expect,q.inspect(B))
 except Exception as e:record(name,'in_memory_parser_return_fault_only_not_hash_bypass',expect,{},repr(e))
 finally:q.parse=original_parse
record('D_normal_readonly_baseline','real_D_readonly',True,q.inspect(B))
with tempfile.TemporaryDirectory(prefix='R7_04_02_',dir=O) as temp:
 T=Path(temp)
 for r,raw in raws.items():
  d=T/r;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(raw)
 record('C_bytecopy_positive','C_copy_no_repin',True,q.inspect(T))
 def disk(name,path,raw,expect=False):
  (T/path).write_bytes(raw)
  try:record(name,'C_copy_no_repin',expect,q.inspect(T))
  except Exception as e:record(name,'C_copy_no_repin',expect,{},repr(e))
  finally:(T/path).write_bytes(raws[path])
 disk('source_hash_mismatch',q.FORM,raws[q.FORM]+b' ')
 (T/q.FORM).unlink();record('missing_pinned_file','C_copy_no_repin',False,q.inspect(T));(T/q.FORM).write_bytes(raws[q.FORM])
 m=original_parse(raws[q.MANIFEST])
 for name,change in [
 ('missing_pin',lambda d:d['pins'].pop()),('extra_pin',lambda d:d['pins'].append(copy.deepcopy(d['pins'][0]))),('duplicate_pin_same_count',lambda d:d['pins'].__setitem__(0,copy.deepcopy(d['pins'][1]))),('escape_parent',lambda d:d['pins'][0].__setitem__('path','../outside.json')),('absolute_path',lambda d:d['pins'][0].__setitem__('path','C:/outside.json')),('backslash_path',lambda d:d['pins'][0].__setitem__('path','01_공통용어\\분류운영규칙.json')),('wrong_hash_syntax',lambda d:d['pins'][0].__setitem__('sha256',d['pins'][0]['sha256']+'\n')),('wrong_pin_identity',lambda d:d['pins'][0].__setitem__('id','wrong')),('wrong_pin_version',lambda d:d['pins'][0].__setitem__('version','999'))]:
  d=copy.deepcopy(m);change(d);disk(name,q.MANIFEST,dump(d))
 disk('duplicate_JSON_key',q.MANIFEST,b'{"id":1,"id":2}')
 disk('NaN',q.MANIFEST,b'{"id":NaN}')
 disk('Infinity',q.MANIFEST,b'{"id":1e999}')
 disk('invalid_UTF8',q.MANIFEST,b'\xff')
 disk('surrogate_key',q.MANIFEST,b'{"\\ud800":1}')
 disk('oversized_integer',q.MANIFEST,b'{"id":'+b'9'*129+b'}')
 disk('deep_JSON',q.MANIFEST,b'['*105+b'0'+b']'*105)
 cli=subprocess.run([sys.executable,'-B',str(p),'--base',str(T)],capture_output=True,text=True,encoding='utf-8',errors='replace')
 rows.append({'name':'CLI_positive_exit0','method':'C_copy_no_repin','passed':cli.returncode==0,'exit_code':cli.returncode,'runtime_exception':None})
 disk('filled_template_real_file',q.FORM,dump(dict(original_parse(raws[q.FORM]),actual_review_count=1)))
 memory('unknown_criterion',q.MAP,lambda d:d['criteria_links'][0].__setitem__('criterion_ref','UNKNOWN'))
 memory('duplicate_criterion_row',q.MAP,lambda d:d['criteria_links'].__setitem__(0,copy.deepcopy(d['criteria_links'][1])))
 memory('unknown_binding_ref',q.MAP,lambda d:d['criteria_links'][0]['binding_candidates'].append('NOT-A-BINDING'))
 memory('duplicate_binding_id',q.MAP,lambda d:d['bindings'][1].__setitem__('id',d['bindings'][0]['id']))
 memory('nonexistent_field',q.MAP,lambda d:d['bindings'][0].__setitem__('key_path',['missing']))
 memory('fake_actual_evidence',q.MAP,lambda d:d['bindings'][0].__setitem__('actual_evidence',True))
 memory('fake_R7_target',q.MAP,lambda d:d['criteria_links'][0].__setitem__('actual_target_ref',{'id':'X'}))
 memory('fake_R7_result',q.MAP,lambda d:d['criteria_links'][0].__setitem__('actual_review_result','통과'))
 memory('fake_CI_transfer_approval',q.MAP,lambda d:d.__setitem__('R6_context_is_not_R7_approval',False))
 memory('missing_human_role',q.MAP,lambda d:d['criteria_links'][0].__setitem__('human_role',''))
 memory('internal_ref_path',q.PLAN,lambda d:d['metrics_ref'].__setitem__('path','missing.json'))
 memory('internal_ref_hash',q.PLAN,lambda d:d['metrics_ref'].__setitem__('sha256','0'*64))
 memory('internal_ref_version',q.PLAN,lambda d:d['metrics_ref'].__setitem__('version','999'))
 memory('form_filled_outcome',q.FORM,lambda d:d['blank_fields'].__setitem__('outcome','통과'))
 memory('form_fake_company_approval',q.FORM,lambda d:d.__setitem__('company_approved',True))
 memory('missing_required_inventory_field',q.FORM,lambda d:d['blank_fields'].pop('required_criteria_inventory'))
 memory('all_blank_fields_removed',q.FORM,lambda d:d.__setitem__('blank_fields',{}))
 memory('mandatory_omission_rule_false',q.FORM,lambda d:d['template_rules'].__setitem__('applicable_required_items_cannot_be_silently_omitted',False))
 memory('bindings_scope_spoof',q.MAP,lambda d:d['bindings'][0].__setitem__('data_scope','actual_verified_evidence'))
 memory('mapping_kind_actual_claim',q.MAP,lambda d:d.__setitem__('kind','actual_content_approved'))
 memory('form_counts_bool_false',q.FORM,lambda d:d.__setitem__('actual_review_count',False))

 def empty_bindings(d):
  d['bindings']=[]
  for row in d['criteria_links']:row['binding_candidates']=[];row['human_context_candidates']=[]
 memory('empty_binding_inventory',q.MAP,empty_bindings)
 memory('form_allowed_outcomes_company_approved',q.FORM,lambda d:d['template_rules'].__setitem__('allowed_outcomes',['회사승인']))
 memory('form_template_rules_missing',q.FORM,lambda d:d.__setitem__('template_rules',{}))
 memory('map_actual_count_bool',q.MAP,lambda d:d.__setitem__('actual_R7_record_links',False))
 memory('form_count_float_zero',q.FORM,lambda d:d.__setitem__('actual_review_count',0.0))
 memory('form_target_count_bool',q.FORM,lambda d:d.__setitem__('actual_target_count',False))
 memory('true_rule_integer_one',q.FORM,lambda d:d['template_rules'].__setitem__('human_reply_must_not_be_fabricated',1))
 memory('list_blank_as_null',q.FORM,lambda d:d['blank_fields'].__setitem__('evidence_refs',None))
 memory('scalar_blank_as_list',q.FORM,lambda d:d['blank_fields'].__setitem__('outcome',[]))
 memory('empty_row_candidates',q.MAP,lambda d:d['criteria_links'][0].__setitem__('binding_candidates',[]))
 memory('binding_key_path_wrong_type',q.MAP,lambda d:d['bindings'][0].__setitem__('key_path',1))
 memory('row_binding_unhashable',q.MAP,lambda d:d['criteria_links'][0].__setitem__('binding_candidates',[{}]))
 memory('positive_emoji_note_not_content_authentication',q.MAP,lambda d:d['bindings'][0].__setitem__('note','설명 😀'),True)
 memory('positive_binding_order_independent',q.MAP,lambda d:d['bindings'].reverse(),True)
 # C CLI error must exit1 rather than present validity.
 (T/q.MANIFEST).write_bytes(b'{"id":NaN}')
 badcli=subprocess.run([sys.executable,'-B',str(p),'--base',str(T)],capture_output=True,text=True,encoding='utf-8',errors='replace')
 rows.append({'name':'CLI_invalid_exit1','method':'C_copy_no_repin','passed':badcli.returncode==1 and json.loads(badcli.stdout)['valid'] is False,'exit_code':badcli.returncode,'runtime_exception':None})
 (T/q.MANIFEST).write_bytes(raws[q.MANIFEST])
 # Direct parser boundary checks are their own units, not video/evaluator trials.
 for name,raw in [('parser_duplicate',b'{"x":1,"x":2}'),('parser_NaN',b'{"x":NaN}'),('parser_overflow',b'{"x":1e999}'),('parser_surrogate_value',b'{"x":"\\ud800"}'),('parser_surrogate_key',b'{"\\udfff":1}')]:
  rejected=False
  try:q.parse(raw)
  except (ValueError,UnicodeError):rejected=True
  rows.append({'name':name,'method':'direct_parser_boundary_unit','passed':rejected,'runtime_exception':None})


 memory('missing_review_method',q.FORM,lambda d:d['blank_fields'].pop('review_method'))
 memory('missing_reviewer_role',q.FORM,lambda d:d['blank_fields'].pop('reviewer_role'))
 encenv=dict(os.environ);encenv['PYTHONIOENCODING']='cp949'
 encr=subprocess.run([sys.executable,'-B',str(p),'--base',str(T/'없는입력_😀')],capture_output=True,env=encenv)
 try:encout=json.loads(encr.stdout.decode('ascii'));encok=encr.returncode==1 and encout['valid'] is False and bool(encout['errors'])
 except Exception:encok=False
 rows.append({'name':'CLI_cp949_emoji_missing_path_structured_error','method':'C_missing_path_cp949_subprocess','passed':encok,'exit_code':encr.returncode,'stderr':encr.stderr.decode('cp949',errors='backslashreplace'),'runtime_exception':None})

 # A source file changes only upon final re-read: no manifest change/rebaseline.
 original_bytes=q.bytes_at;counts={}
 def change_end(base,path):
  counts[path]=counts.get(path,0)+1;raw=original_bytes(base,path)
  return raw+b' ' if path==q.FORM and counts[path]>=2 else raw
 q.bytes_at=change_end
 try:record('source_changed_at_final_read','in_memory_read_timing_fault',False,q.inspect(T))
 finally:q.bytes_at=original_bytes
 original_bytes=q.bytes_at;counts={}
 def manifest_end(base,path):
  counts[path]=counts.get(path,0)+1;raw=original_bytes(base,path)
  return raw+b' ' if path==q.MANIFEST and counts[path]>=2 else raw
 q.bytes_at=manifest_end
 try:record('manifest_changed_at_final_read','in_memory_read_timing_fault',False,q.inspect(T))
 finally:q.bytes_at=original_bytes
 # Compare named fields against full actual source data and canonical criterion text.
 loaded={r:original_parse(raws[r]) for r in [q.MAP,q.R4,q.R5,q.R6,q.QUALITY]};fm=loaded[q.MAP];cards={x['id']:x for x in loaded[q.QUALITY]['cards']};fieldpaths=[]
 for bind in fm['bindings']:
  value=loaded[bind['structure_reference']]
  for key in bind['key_path']:value=value[key]
  fieldpaths.append({'id':bind['id'],'source':bind['structure_reference'],'key_path':bind['key_path'],'value_type':type(value).__name__,'data_scope':bind['data_scope']})
 criterionlinks=[{'id':x['criterion_ref'],'same':all([x['group']==cards[x['criterion_ref']]['group'],x['required_evidence']==cards[x['criterion_ref']]['required_evidence'],x['hold_when']==cards[x['criterion_ref']]['hold_when'],x['human_role']==cards[x['criterion_ref']]['human_review']['role']])} for x in fm['criteria_links']]
after={r:sha(B/r) for r in paths};result={'scope':'R7-4-2독립구조/고정파일정합성검토. C해시재고정없음. 메모리parse결함주입은입력바이트검사우회가능성증명이아니라구조검사분기검증.','conditions':len(rows),'passed':sum(x['passed'] for x in rows),'failed':[x['name'] for x in rows if not x['passed']],'runtime_exceptions':sum(x.get('runtime_exception') is not None for x in rows),'rows':rows,'field_path_checks':fieldpaths,'criterion_link_checks':criterionlinks,'before_hashes':before,'after_hashes':after,'D_sources_unchanged':before==after,'actual_human_content_review_performed':False,'actual_video_analysis':False}
(O/'R7_04_02_최종_독립반례결과.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:result[k] for k in ['conditions','passed','failed','runtime_exceptions','D_sources_unchanged']},ensure_ascii=True))
