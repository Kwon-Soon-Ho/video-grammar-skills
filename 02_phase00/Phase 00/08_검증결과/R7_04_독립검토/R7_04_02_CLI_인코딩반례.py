import os,sys,subprocess,json
from pathlib import Path
p=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00\07_실행도구/R7_연결확인.py');o=Path(__file__).parent
folder=o/'없는입력_😀';env=dict(os.environ);env['PYTHONIOENCODING']='cp949'
r=subprocess.run([sys.executable,'-B',str(p),'--base',str(folder)],capture_output=True,env=env)
try:out=json.loads(r.stdout.decode('cp949'));parsed=True
except Exception:out=None;parsed=False
result={'condition':'CLI invalid missing base path with emoji under cp949','exit_code':r.returncode,'structured_json_output':parsed,'stdout_hex':r.stdout.hex(),'stderr':r.stderr.decode('cp949',errors='backslashreplace'),'actual_video_analysis':False}
(o/'R7_04_02_CLI_인코딩_초기반례.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'exit':r.returncode,'structured':parsed,'unicode_error':b'UnicodeEncodeError' in r.stderr}))
