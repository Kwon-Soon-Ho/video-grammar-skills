import json,importlib.util,copy,hashlib
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent;p=B/'07_실행도구/R7_연결확인.py';spec=importlib.util.spec_from_file_location('r7_more',p);q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q);original=q.parse;rows=[]
def test(name,path,change):
 raw=(B/path).read_bytes();d=original(raw);change(d);q.parse=lambda x:copy.deepcopy(d) if x==raw else original(x)
 try:r=q.inspect(B);rows.append({'name':name,'expected_valid':False,'actual_valid':r['valid'],'passed':r['valid'] is False,'result':r})
 finally:q.parse=original

def empty_bindings(d):
 d['bindings']=[]
 for row in d['criteria_links']:row['binding_candidates']=[];row['human_context_candidates']=[]
test('empty_binding_inventory',q.MAP,empty_bindings)
test('form_allowed_outcomes_company_approved',q.FORM,lambda d:d['template_rules'].__setitem__('allowed_outcomes',['회사승인']))
test('form_template_rules_missing',q.FORM,lambda d:d.__setitem__('template_rules',{}))
test('map_actual_count_bool',q.MAP,lambda d:d.__setitem__('actual_R7_record_links',False))
(O/'R7_04_02_추가초기_독립반례결과.json').write_text(json.dumps({'scope':'메모리구조분기결함주입만.고정해시우회가아님','rows':rows},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'name':x['name'],'valid':x['actual_valid']} for x in rows]))
