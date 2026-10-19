from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for f in sorted((HERE/'seals').glob('T??.json')):
    r=json.loads(f.read_text(encoding='utf-8'));case=r['case_id'];dst=Path(r['sealed_copy']).parent
    rec=HERE/'seals'/(case+'_narrative.json')
    if rec.exists():continue
    src=Path(r['source_path']).with_name(case+'_narrative.md')
    if not src.exists():src=Path(r['source_path']).with_suffix('.md')
    if not src.exists():src=Path(r['source_path']).with_name(case+'_narrative_ko.txt')
    if not src.exists():continue
    out=dst/'observations.md'
    if not out.exists():shutil.copy2(src,out)
    assert sha(src)==sha(out)
    rec.write_text(json.dumps({'case_id':case,'sealed_at':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds'),'source_path':str(src),'source_sha256':sha(src),'sealed_copy':str(out),'grader_feedback_before_seal':False},ensure_ascii=False,indent=2),encoding='utf-8')
    print('narrative sealed',case)
