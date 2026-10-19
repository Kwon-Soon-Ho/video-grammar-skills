from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import sys, os, json, hashlib, subprocess

sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
LOCAL=OUT.parents[1]
SOURCE=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
DEST=LOCAL/'R8_04_시험/고정문맥_검증전용/Phase00'
PY=SOURCE/'.환경/Scripts/python.exe'
INVENTORY=OUT/'full_R6_R7_copy_set.json'
def extended(p):
    s=str(Path(p).resolve())
    return Path(s if s.startswith('\\\\?\\') else '\\\\?\\'+s)
def raw(p): return extended(p).read_bytes()
def digest(data):return hashlib.sha256(data).hexdigest()
def sha(p):return digest(raw(p))
def write(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

started=datetime.now(timezone.utc).isoformat()
manifest=json.loads(raw(INVENTORY).decode('utf-8'))
if manifest['base']!=str(SOURCE) or manifest['count']!=800 or len(manifest['files'])!=800:raise ValueError('unexpected_source_inventory')
if DEST.resolve().is_relative_to(SOURCE.resolve()):raise ValueError('destination_cannot_be_source')
rows=[]
for pin in manifest['files']:
    parts=PurePosixPath(pin['path'])
    if parts.is_absolute() or '..' in parts.parts or '\\' in pin['path'] or ':' in pin['path']:raise ValueError('unsafe_relative_path')
    src=SOURCE/Path(*parts.parts);dst=DEST/Path(*parts.parts)
    before=raw(src)
    if digest(before)!=pin['sha256'] or len(before)!=pin['bytes']:raise ValueError('source_changed_before_copy: '+pin['path'])
    extended(dst.parent).mkdir(parents=True,exist_ok=True)
    exists=extended(dst).is_file()
    if exists:
        if raw(dst)!=before:raise ValueError('destination_exists_with_other_bytes: '+pin['path'])
    else:
        with extended(dst).open('xb') as handle:handle.write(before)
    after=raw(dst)
    if after!=before:raise ValueError('copy_mismatch: '+pin['path'])
    if sha(src)!=pin['sha256']:raise ValueError('source_changed_during_copy: '+pin['path'])
    rows.append({'path':pin['path'],'expected_sha256':pin['sha256'],'source_before_sha256':digest(before),'copy_sha256':digest(after),'source_after_copy_sha256':sha(src),'bytes':len(before),'created':not exists})
write('full_copy_file_checks.json',{'source':str(SOURCE),'destination':str(DEST),'inventory_sha256':sha(INVENTORY),'started_utc':started,'file_count':len(rows),'rows':rows})

commands=[]
for name in ['R6_출처사용검사.py','R6_사람검수.py','R6_통합조회.py','R7_연결확인.py']:
    script=DEST/'07_실행도구'/name
    args=[str(PY),'-B','-X','utf8',str(script),'--base',str(DEST)]
    result=subprocess.run(args,capture_output=True,encoding='utf-8',env={**os.environ,'PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8','PYTHONDONTWRITEBYTECODE':'1'},timeout=60)
    entry={'args':args,'source_script_sha256':sha(SOURCE/'07_실행도구'/name),'copy_script_sha256':sha(script),'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
    try:entry['parsed']=json.loads(result.stdout)
    except ValueError:pass
    commands.append(entry)
write('full_copy_read_api_commands.json',commands)
source_final=[];copy_final=[]
for pin in manifest['files']:
    parts=PurePosixPath(pin['path']);rel=Path(*parts.parts)
    if sha(SOURCE/rel)!=pin['sha256']:source_final.append(pin['path'])
    if sha(DEST/rel)!=pin['sha256']:copy_final.append(pin['path'])
actual={p.relative_to(extended(DEST)).as_posix() for p in extended(DEST).rglob('*') if p.is_file()}
expected={p['path'] for p in manifest['files']}
receipt={'id':'r8-4-full-fixed-context-structure-receipt','version':'0.1.0','scope':'unchanged_R6_R7_full_copy_structure_query_only','source':str(SOURCE),'copy_base':str(DEST),'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'inventory_sha256':sha(INVENTORY),'copier_script_sha256':sha(Path(__file__)),'file_count':len(rows),'bytes':sum(r['bytes'] for r in rows),'all_source_before_copy_and_after_hashes_match':not source_final,'all_copy_hashes_match':not copy_final,'source_final_mismatches':source_final,'copy_final_mismatches':copy_final,'extra_copy_paths':sorted(actual-expected),'missing_copy_paths':sorted(expected-actual),'source_R6_manifest_sha256':sha(SOURCE/'05_출처와검토/검수와사용범위/통합검수_입력고정.json'),'copy_R6_manifest_sha256':sha(DEST/'05_출처와검토/검수와사용범위/통합검수_입력고정.json'),'source_R7_manifest_sha256':sha(SOURCE/'13_품질검수/연결과인계/현재연결_입력고정.json'),'copy_R7_manifest_sha256':sha(DEST/'13_품질검수/연결과인계/현재연결_입력고정.json'),'read_checks':[{'tool':Path(c['args'][4]).name,'exit_code':c['exit_code'],'valid':c.get('parsed',{}).get('valid',c.get('parsed',{}).get('structural_valid'))} for c in commands],'behavior_performer_read_full_copy':False,'behavior_test_result_linkage':'separate_role_receipt_required','candidate_behavior_evaluated':False,'actual_video_analyzed':False,'content_verified':False,'company_approved':False,'permission_granted':False,'operational_release':False,'limitations':['No atomic snapshot or OS-level isolation proof.','Original absolute host artifact paths are preferred by existing R6 APIs if they exist; the four recorded host paths were absent in this environment.','Structure queries against this copy do not mean a behavior performer read this full context.']}
write('full_copy_structure_receipt.json',receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))
raise SystemExit(0 if all(c['exit_code']==0 for c in commands) and not source_final and not copy_final and actual==expected else 1)
