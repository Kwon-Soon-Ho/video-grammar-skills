from pathlib import Path
import sys, os, json, hashlib, subprocess, base64, difflib
from importlib.metadata import version as package_version
from datetime import datetime, timezone

BASE=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
OUT=Path(__file__).resolve().parent
LOCAL=OUT.parents[1]
PY=BASE/'.환경/Scripts/python.exe'
TOOLS=BASE/'07_실행도구'
sys.path.insert(0,str(TOOLS))
sys.dont_write_bytecode=True
import R6_출처사용검사 as source
import R6_사람검수 as human
import R6_통합조회 as integrated
import R7_연결확인 as r7

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(name,value): (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p): return {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}

observed=set()
rows=[]
def add(p,why,expected=None):
    p=p.resolve(); observed.add(p)
    row={'path':str(p),'relative_to_base':p.relative_to(BASE).as_posix() if p.is_relative_to(BASE) else None,'needed_by':why,'exists':p.is_file(),'expected_sha256':expected}
    if p.is_file():row.update(sha256=sha(p),bytes=p.stat().st_size,expected_hash_match=expected==sha(p) if expected else None)
    rows.append(row)

r6m=read(BASE/integrated.MANIFEST);r7m=read(BASE/r7.MANIFEST)
add(BASE/integrated.MANIFEST,'R6 manifest (not included in its own pins)')
add(BASE/r7.MANIFEST,'R7 manifest (not included in its own pins)')
for p in r6m['pins']:add(BASE/p['path'],'R6 manifest pin',p['sha256'])
for p in r7m['pins']:add(BASE/p['path'],'R7 manifest pin',p['sha256'])
index=read(BASE/source.INDEX)
artifact_selection=[]
for f in index['file_checks']:
    original=Path(f['original_path']) if Path(f['original_path']).is_absolute() else BASE/f['original_path']
    recovery=BASE/f['preserved_snapshot'] if f['preserved_snapshot'] else None
    selected=original if original.is_file() else recovery or original
    add(selected,'R6 artifact '+f['review_pointer']+'; prefer original if present',f['sha256'])
    artifact_selection.append({'review_pointer':f['review_pointer'],'original_path':str(original),'original_exists':original.is_file(),'preserved_snapshot':str(recovery) if recovery else None,'selected_path':str(selected),'selected_sha256':sha(selected),'expected_sha256':f['sha256']})
for a in index['asset_usage']:add(BASE/a['file']['path'],'R6 registered asset '+a['asset_id'],a['file']['sha256'])

additional=[]
for name in ['통합기록_규격검사.py','좌표변환_규격검사.py','근거주장_규격검사.py','시간프레임_규격검사.py','R5_디자인적용검사.py']:
    text=(TOOLS/name).read_text(encoding='utf-8')
    additional.append({'path':str(TOOLS/name),'sha256':sha(TOOLS/name),'imports':[s for s in text.splitlines() if s.startswith(('import ','from '))]})
candidate=[pin(p) for p in sorted((BASE/'06_맞춤스킬/재구성후보').rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
for p in sorted((BASE/'14_스킬재구성').glob('*')):
    if p.is_file(): add(p,'R8 current guide/state')
before={str(p):sha(p) for p in observed if p.is_file()}

commands=[]
for tool in ['R6_출처사용검사.py','R6_사람검수.py','R6_통합조회.py','R7_연결확인.py']:
    args=[str(PY),'-B','-X','utf8',str(TOOLS/tool),'--base',str(BASE)]
    run=subprocess.run(args,capture_output=True,encoding='utf-8',env={**os.environ,'PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8','PYTHONDONTWRITEBYTECODE':'1'},timeout=60)
    row={'args':args,'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'script_sha256':sha(TOOLS/tool)}
    try: row['parsed']=json.loads(run.stdout)
    except ValueError: pass
    commands.append(row)
write('read_api_commands.json',commands)

viewer_results=[]
for skill,folder,name in [('video-knowledge-curator','R8_01_큐레이터','큐레이터_출력검토.html'),('video-record-steward','R8_02_기록관리자','기록관리자_출력검토.html')]:
    home=LOCAL/'R8_시험'/(skill+'-workspace')
    configs=[(BASE/'08_검증결과'/folder/name,'iteration-2')]
    if skill=='video-record-steward':configs.append((BASE/'08_검증결과'/folder/'초기후보검토'/name,'iteration-1'))
    for html,iteration in configs:
        text=html.read_text(encoding='utf-8');data=json.JSONDecoder().raw_decode(text.split('const EMBEDDED_DATA = ',1)[1])[0]
        result={'viewer':pin(html),'iteration':iteration,'runs':[],'previous_outputs':[]}
        rundirs={p.relative_to(home/iteration).as_posix().replace('/','-'):p for p in (home/iteration).glob('eval-*/*/run-1')}
        for run in data['runs']:
            rd=rundirs[run['id']]; metadata=read(rd/'eval_metadata.json'); task=(rd/'task.txt').read_text(encoding='utf-8')
            displayed=run['prompt']; prompt=metadata['prompt']
            row={'run_id':run['id'],'task':pin(rd/'task.txt'),'eval_metadata':pin(rd/'eval_metadata.json'),'display_prompt_sha256':hashlib.sha256(displayed.encode()).hexdigest(),'display_eq_metadata':displayed==prompt,'display_eq_task':displayed==task,'task_eq_metadata':task==prompt,'display_prompt_preview':displayed[:160],'literal_backslash_n_in_metadata':'\\n' in prompt,'literal_backslash_n_in_display':'\\n' in displayed,'output_checks':[]}
            if displayed!=task:row['prompt_diff']=''.join(difflib.unified_diff(task.splitlines(True),displayed.splitlines(True),fromfile='task.txt',tofile='viewer prompt'))
            for f in run['outputs']:
                p=rd/'outputs'/f['name']
                decoded=f['content'].encode('utf-8') if f['type']=='text' else base64.b64decode(f['data_uri'].split(';base64,',1)[1])
                match=(p.read_text(encoding='utf-8')==f['content']) if f['type']=='text' else p.read_bytes()==decoded
                row['output_checks'].append({**pin(p),'viewer_type':f['type'],'matches_actual':match,'decoded_sha256':hashlib.sha256(decoded).hexdigest(),'byte_exact':p.read_bytes()==decoded,'newline_normalized_text_match':p.read_bytes().decode('utf-8').replace('\r\n','\n').replace('\r','\n')==f['content'] if f['type']=='text' else None})
            row['output_name_set_match']=set(f['name'] for f in run['outputs'])==set(p.name for p in (rd/'outputs').iterdir() if p.is_file())
            backup=BASE/'backup'/('2026-10-15_R8_01_시험정리' if skill=='video-knowledge-curator' else '2026-10-15_R8_02_시험정리')/'실행원문'/(skill+'-workspace')/iteration/rd.relative_to(home/iteration)
            row['preserved_backup_checks']=[]
            for local in [rd/'task.txt',rd/'eval_metadata.json']+[rd/'outputs'/f['name'] for f in run['outputs']]:
                bp=backup/local.relative_to(rd)
                row['preserved_backup_checks'].append({'path':str(bp),'exists':bp.is_file(),'local_sha256':sha(local),'backup_sha256':sha(bp) if bp.is_file() else None,'byte_match':bp.is_file() and sha(local)==sha(bp)})
            result['runs'].append(row)
        for rid,files in data.get('previous_outputs',{}).items():
            pdirs={p.relative_to(home/'iteration-1').as_posix().replace('/','-'):p for p in (home/'iteration-1').glob('eval-*/*/run-1')}
            checks=[]
            for f in files:
                p=pdirs[rid]/'outputs'/f['name'];match=p.read_text(encoding='utf-8')==f['content'] if f['type']=='text' else p.read_bytes()==base64.b64decode(f['data_uri'].split(';base64,',1)[1])
                checks.append({'name':f['name'],'matches_actual':match,'sha256':sha(p)})
            result['previous_outputs'].append({'run_id':rid,'checks':checks})
        viewer_results.append(result)
write('viewer_task_output_audit.json',viewer_results)

after={str(p):sha(p) for p in observed if p.is_file()}
core_paths=sorted(set(r['relative_to_base'] for r in rows if not r['needed_by'].startswith('R8')))
write('full_R6_R7_copy_set.json',{'purpose':'Exact selected files required by unchanged current R6/R7 read APIs, not a role performer input whitelist','base':str(BASE),'count':len(core_paths),'files':[{'path':p,'sha256':sha(BASE/p),'bytes':(BASE/p).stat().st_size} for p in core_paths],'artifact_selection':artifact_selection,'fallback_original_absence_must_remain_true':True,'schema_runtime_packages':{n:package_version(n) for n in ['jsonschema','referencing','attrs','jsonschema-specifications','rpds-py']},'no_os_enforced_isolation_claim':True})
write('required_files.json',{'base':str(BASE),'r6_manifest_pin_count':len(r6m['pins']),'r7_manifest_pin_count':len(r7m['pins']),'artifact_rows':len(index['file_checks']),'asset_rows':len(index['asset_usage']),'rows':rows,'unique_required_file_count':len(set(r['path'] for r in rows)),'tool_imports_for_R4_R5_record_checks':additional,'candidates':candidate,'not_copied_or_modified':True})
write('audit_summary.json',{'utc':datetime.now(timezone.utc).isoformat(),'python':str(PY),'python_version':sys.version,'script_sha256':sha(Path(__file__)),'read_checks':[{ 'tool':Path(c['args'][4]).name,'exit_code':c['exit_code'],'valid':c.get('parsed',{}).get('valid',c.get('parsed',{}).get('structural_valid'))} for c in commands],'required_file_count':len(before),'source_endpoint_hashes_unchanged':before==after,'changed_source_paths':[p for p in before if before[p]!=after.get(p)],'candidate_pin_count':len(candidate),'viewer_run_count':sum(len(v['runs']) for v in viewer_results),'viewer_prompt_matches_metadata_count':sum(r['display_eq_metadata'] for v in viewer_results for r in v['runs']),'viewer_prompt_matches_task_count':sum(r['display_eq_task'] for v in viewer_results for r in v['runs']),'all_shown_outputs_match_actual':all(c['matches_actual'] for v in viewer_results for r in v['runs'] for c in r['output_checks']),'limitations':['Read-only API/code/data audit; no model performance test, rendered browser, video effects or human approval.','Before/after SHA does not prove no temporary changes during execution or an atomic snapshot.','External original paths are preferred by R6; copying pinned index alone does not make them local.']})
print(json.dumps(read(OUT/'audit_summary.json'),ensure_ascii=False,indent=2))
