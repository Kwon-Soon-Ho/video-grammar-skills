"""Publish records and replace only the authorized project development working copy."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,shutil,os
HERE=Path(__file__).resolve().parent
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
CANON=D/'Phase 01-A/03_분석스킬/company-video-grammar-analyzer'
STAGED=D/'Phase 01-A/03_분석스킬/draft7_준비_20261019'
OLD=D/'99_백업/2026-10-19_분석스킬_수정전/원본폴더/company-video-grammar-analyzer_draft3'
CANDIDATE=D/'Phase 01-A/03_분석스킬/수정후보/2026-10-19_draft7/company-video-grammar-analyzer'
RECORDS=D/'Phase 01-A/02_분석작업/2026-10-19_백업후_분석신뢰성_보완과_새자료'
def digest(p):return sha256(Path(p).read_bytes()).hexdigest()
def copy_file(source,dest):
    dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():assert digest(dest)==digest(source),dest
    else:
        with source.open('rb') as incoming,dest.open('xb') as output:shutil.copyfileobj(incoming,output)
    assert digest(dest)==digest(source)
    return {'source':str(source),'destination':str(dest),'sha256':digest(dest)}
for p in (CANON,STAGED,OLD,CANDIDATE,RECORDS):assert p.resolve().is_relative_to(D) and p.resolve()!=D
assert CANON.is_dir() and not STAGED.exists() and not OLD.exists()
protected=json.loads((HERE/'protected-before.json').read_text(encoding='utf-8'))
for item in protected:assert digest(item['path']).lower()==item['sha256'].lower(),item['path']
backup=json.loads((HERE/'backup-publication.json').read_text(encoding='utf-8'))
for item in backup['files']:assert digest(item['backup'])==item['sha256']
operations=[];skill=HERE/'candidate/company-video-grammar-analyzer'
for source in HERE.rglob('*'):
    if not source.is_file() or '__pycache__' in source.parts or source.name in ('working-update.json','publication-receipt.json') or 'backup' in source.relative_to(HERE).parts:continue
    relative=source.relative_to(HERE)
    dest=CANDIDATE/Path(*relative.parts[2:]) if relative.parts[0]=='candidate' else RECORDS/relative
    operations.append(copy_file(source,dest))
newfiles=[]
for source in skill.rglob('*'):
    if not source.is_file() or '__pycache__' in source.parts:continue
    relative=source.relative_to(skill);copy_file(source,STAGED/relative);newfiles.append({'relative':relative.as_posix(),'sha256':digest(source)})
oldfiles=[{'relative':p.relative_to(CANON).as_posix(),'sha256':digest(p)} for p in CANON.rglob('*') if p.is_file()]
OLD.parent.mkdir(parents=True,exist_ok=True)
os.rename(CANON,OLD)
try:os.rename(STAGED,CANON)
except BaseException:
    if not CANON.exists():os.rename(OLD,CANON)
    raise
for item in oldfiles:assert digest(OLD/item['relative'])==item['sha256']
for item in newfiles:assert digest(CANON/item['relative'])==item['sha256']
preserved=[];relocated=[]
for item in protected:
    p=Path(item['path'])
    if p.resolve().is_relative_to(CANON):
        target=OLD/p.resolve().relative_to(CANON);assert digest(target).lower()==item['sha256'].lower();relocated.append({**item,'preserved_at':str(target)})
    else:assert digest(p).lower()==item['sha256'].lower();preserved.append(item)
receipt={'utc':datetime.now(timezone.utc).isoformat(),'authorization':'기존 스킬은 백업하고 수정 작업 계속 진행하자','working_copy':str(CANON),'working_version':'0.1.0-draft.7','prior_original_folder':str(OLD),'candidate_snapshot':str(CANDIDATE),'records':str(RECORDS),'global_skill_installed':False,'whole_research_completed':False,'protected_unchanged':len(preserved),'authorized_working_paths_relocated':len(relocated),'relocated':relocated,'new_working_files':newfiles,'published_files':operations,'published_file_count':len(operations),'preservation_note':'기존 347개 보호 경로 중 기존 본체 7개는 사용자 수정 지시에 따라 원본 폴더를 백업으로 옮겨 바이트를 보존했고, 나머지는 원래 경로에서 동일함. 기존 A5b의 중단·실패·후보를 수정하지 않음.'}
data=json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf-8')
(HERE/'working-update.json').write_bytes(data);(RECORDS/'working-update.json').write_bytes(data)
print(json.dumps({k:v for k,v in receipt.items() if k not in ('published_files','relocated','new_working_files')},ensure_ascii=False))
