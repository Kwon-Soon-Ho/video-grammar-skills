from pathlib import Path
from hashlib import sha256
import json,shutil
HERE=Path(__file__).resolve().parent
DEST=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/99_백업/2026-10-19_분석스킬_수정전')
files=[]
for p in (HERE/'backup').iterdir():
 if not p.is_file():continue
 target=DEST/p.name;h=sha256(p.read_bytes()).hexdigest();target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():assert sha256(target.read_bytes()).hexdigest()==h
 else:
  with p.open('rb') as source,target.open('xb') as output:shutil.copyfileobj(source,output)
 assert sha256(target.read_bytes()).hexdigest()==h
 files.append({'source':str(p),'backup':str(target),'sha256':h})
receipt={'files':files,'verified':True,'default_skill_changed':False}
(HERE/'backup-publication.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
