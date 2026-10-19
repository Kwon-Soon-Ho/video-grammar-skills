from pathlib import Path
O=Path(__file__).parent
s=(O/'R7_04_02_초기_독립반례코드.py').read_text(encoding='utf-8-sig')
s=s.replace("'R7_04_02_초기_독립반례결과.json'","'R7_04_02_최종_독립반례결과.json'")
insert="""
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
 for name,raw in [('parser_duplicate',b'{"x":1,"x":2}'),('parser_NaN',b'{"x":NaN}'),('parser_overflow',b'{"x":1e999}'),('parser_surrogate_value',b'{"x":"\\\\ud800"}'),('parser_surrogate_key',b'{"\\\\udfff":1}')]:
  rejected=False
  try:q.parse(raw)
  except (ValueError,UnicodeError):rejected=True
  rows.append({'name':name,'method':'direct_parser_boundary_unit','passed':rejected,'runtime_exception':None})
"""
s=s.replace(' # A source file changes only upon final re-read:',insert+'\n # A source file changes only upon final re-read:')
(O/'R7_04_02_최종_독립반례코드.py').write_text(s,encoding='utf-8')
