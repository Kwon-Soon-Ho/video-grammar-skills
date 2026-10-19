"""Non-destructive snapshot of the project skill directory and local baselines."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
from zipfile import ZipFile,ZIP_DEFLATED
import json,sys
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
sources=[('D-project-analysis-skills',D/'Phase 01-A/03_분석스킬'),('C-frozen-A5b',WORK/'phase01a-a5b/candidate/company-video-grammar-analyzer'),('C-latest-draft6',WORK/'analyzer-realuse-20261019/candidate/company-video-grammar-analyzer')]
out=HERE/'backup';out.mkdir(parents=True,exist_ok=True)
archive=out/'2026-10-19_분석스킬_수정전_전체백업.zip'
def digest(p):return sha256(Path(p).read_bytes()).hexdigest()
assert not archive.exists(),'Backup already exists; do not overwrite a snapshot'
entries=[]
with ZipFile(archive,'x',compression=ZIP_DEFLATED) as z:
 for label,root in sources:
  assert root.is_dir(),root
  for p in sorted(root.rglob('*')):
   if not p.is_file():continue
   name=label+'/'+p.relative_to(root).as_posix();h=digest(p)
   z.write(p,name);entries.append({'source':str(p),'archive_path':name,'size':p.stat().st_size,'sha256':h})
with ZipFile(archive) as z:
 assert z.testzip() is None
 assert set(z.namelist())=={e['archive_path'] for e in entries}
 for e in entries:
  assert sha256(z.read(e['archive_path'])).hexdigest()==e['sha256']==digest(e['source'])
manifest={'created_utc':datetime.now(timezone.utc).isoformat(),'user_authorization':'기존 스킬은 백업하고 수정 작업 계속 진행하자','scope':'D 프로젝트 분석스킬 디렉터리 전체(기존 본체·이전 작업본·draft4~6 포함), C 동결 A5b 스킬과 최신 draft6 후보. 무관한 전역 스킬은 대상 아님.','archive':str(archive),'archive_sha256':digest(archive),'file_count':len(entries),'all_entries_verified':True,'entries':entries,'restore_note':'별도 빈 폴더에 압축 해제 후 manifest의 개별 SHA-256을 대조한다. 복구할 판본 폴더를 선택하며 현재 스킬 위로 자동 덮어쓰지 않는다.'}
(out/'backup-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in manifest.items() if k!='entries'},ensure_ascii=False))
