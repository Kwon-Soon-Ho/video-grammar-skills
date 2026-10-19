from pathlib import Path
import importlib.util,json,shutil,hashlib
O=Path(__file__).resolve().parent;L=O.parents[2];P=L/'R8_후보연결확인.py'
s=importlib.util.spec_from_file_location('r8_independent_robustness',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
W=O/'robustness';assert not W.exists();source=O/'isolated/baseline/Phase00'
rows=[]
def run(name,text):
 r=W/name/'Phase00';shutil.copytree(source,r);p=r/m.CONTEXT;p.write_text(text,encoding='utf-8')
 try:
  result=m.inspect(r);rows.append({'name':name,'valid':result['valid'],'structured_failure':not result['valid'],'exception':None,'result':result})
 except Exception as e:rows.append({'name':name,'valid':None,'structured_failure':False,'exception':type(e).__name__+': '+str(e)})
t=(source/m.CONTEXT).read_text(encoding='utf-8')
run('deep_json1100','['*1100+'0'+']'*1100)
run('overflow_nonfinite_extra',t.replace('{','{"untrusted_numeric_metadata":1e999,',1))
(O/'04_추가입력한계.json').write_text(json.dumps({'checker_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'cases':rows,'scope':'small local malformed-input probes; no rights/model tests'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'name':r['name'],'valid':r['valid'],'exception':r['exception']} for r in rows],ensure_ascii=False))
