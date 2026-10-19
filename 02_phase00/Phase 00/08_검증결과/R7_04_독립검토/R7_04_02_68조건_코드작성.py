from pathlib import Path
O=Path(__file__).parent;s=(O/'R7_04_02_v0.1.2_65조건이력/R7_04_02_최종_독립반례코드.py').read_text(encoding='utf-8')
s=s.replace('import json,hashlib,importlib.util,copy,sys,tempfile,subprocess','import json,hashlib,importlib.util,copy,sys,tempfile,subprocess,os')
new="""
 memory('missing_review_method',q.FORM,lambda d:d['blank_fields'].pop('review_method'))
 memory('missing_reviewer_role',q.FORM,lambda d:d['blank_fields'].pop('reviewer_role'))
 encenv=dict(os.environ);encenv['PYTHONIOENCODING']='cp949'
 encr=subprocess.run([sys.executable,'-B',str(p),'--base',str(T/'없는입력_😀')],capture_output=True,env=encenv)
 try:encout=json.loads(encr.stdout.decode('ascii'));encok=encr.returncode==1 and encout['valid'] is False and bool(encout['errors'])
 except Exception:encok=False
 rows.append({'name':'CLI_cp949_emoji_missing_path_structured_error','method':'C_missing_path_cp949_subprocess','passed':encok,'exit_code':encr.returncode,'stderr':encr.stderr.decode('cp949',errors='backslashreplace'),'runtime_exception':None})
"""
s=s.replace(' # A source file changes only upon final re-read:',new+'\n # A source file changes only upon final re-read:')
(O/'R7_04_02_최종_독립반례코드.py').write_text(s,encoding='utf-8')
