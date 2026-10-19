from pathlib import Path
import json,hashlib,subprocess,os,base64,importlib.util
L=Path(__file__).parent.resolve();W=L/'R8_시험/video-guidance-reviewer-workspace';IT=W/'iteration-1'
CREATOR=Path('C:/Users/User/.codex/skills/anthropic-skill-creator')
PY=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00/.환경/Scripts/python.exe')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sp=importlib.util.spec_from_file_location('r803_display',L/'R8_01_뷰어작성.py');adapter=importlib.util.module_from_spec(sp);sp.loader.exec_module(adapter)
raw=W/'원문보존/공식뷰어_생성원본.html';raw.parent.mkdir(parents=True,exist_ok=True);assert not raw.exists()
outputs=list(IT.glob('eval-*/*/run-1/outputs'));assert len(outputs)==6 and all((p/'검토결과.md').is_file() for p in outputs)
args=[str(PY),'-B',str(CREATOR/'eval-viewer/generate_review.py'),str(IT),'--skill-name','video-guidance-reviewer','--static',str(raw),'--benchmark',str(IT/'benchmark.json')]
r=subprocess.run(args,env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8'),capture_output=True,text=True,encoding='utf-8',timeout=60)
(W/'공식뷰어_실행기록.json').write_text(json.dumps({'args':args,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'creator_script_sha256':sha(CREATOR/'eval-viewer/generate_review.py'),'template_sha256':sha(CREATOR/'eval-viewer/viewer.html'),'display_adapter_sha256':sha(L/'R8_01_뷰어작성.py'),'mode':'official static only; no server/browser/CU'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert r.returncode==0
display,data,removed=adapter.display_copy(raw.read_text(encoding='utf-8'));byrun={p.parent.relative_to(IT).as_posix().replace('/','-'):p for p in outputs}
assert len(data['runs'])==6
shown=0
for run in data['runs']:
 for f in run['outputs']:
    p=byrun[run['id']]/f['name']
    if f['type']=='text':assert p.read_text(encoding='utf-8')==f['content']
    elif f['type']=='binary':assert p.read_bytes()==base64.b64decode(f['data_uri'].split(';base64,',1)[1])
    else:raise ValueError('unsupported output type')
    shown+=1
target=W/'적용성검토자_출력검토.html';target.write_text('<!-- Anthropic Skill Creator official static viewer display adaptation; Apache-2.0; see 원문보존/LICENSE.txt -->\n'+display,encoding='utf-8')
(W/'원문보존/LICENSE.txt').write_bytes((CREATOR/'LICENSE.txt').read_bytes())
(W/'뷰어_표시검증.json').write_text(json.dumps({'official_raw_sha256':sha(raw),'display_sha256':sha(target),'embedded_run_count':6,'output_files_verified':shown,'decoded_output_content_matches_actual':True,'external_resource_tags':[],'removed_external_tags':removed,'script_boundary_escaping_applied':True,'human_review_performed':False,'limitations':'HTML/data structural check; no browser render/click/visual check'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(str(target))
