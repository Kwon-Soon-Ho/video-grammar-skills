from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from fractions import Fraction as F
import sys,json,shutil,hashlib
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
packet=json.loads((HERE/'analysis_input/cases.json').read_text(encoding='utf-8'));assign={'T01':'retest_a','T04':'retest_a','T02':'retest_b','T05':'retest_b','T03':'retest_c','T06':'retest_c'}
seals=HERE/'seals';seals.mkdir(exist_ok=True)
for c in packet['cases']:
    id=c['case_id'];src=HERE/'runs'/assign[id]/(id+'_observations.json')
    if not src.exists() or (seals/(id+'.json')).exists():continue
    result=json.loads(src.read_text(encoding='utf-8-sig'))
    out=HERE/'evaluation/iteration-1'/('eval-'+id)/'without_skill/outputs';out.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,out/'observations.json')
    md=src.with_suffix('.md')
    if md.exists():shutil.copy2(md,out/'observations.md')
    metadata={'eval_id':int(id[1:]),'eval_name':id+' baseline motion analysis','prompt':c['prompt']+' Allowed source window: '+str(c['allowed_window_seconds']),'assertions':[],'new_skill_available':False,'media_sha256':c['media_sha256']}
    (out.parent.parent/'eval_metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    run=json.loads((HERE/'analysis_input/cases'/c['asset_id']/id/'실행기록.json').read_text(encoding='utf-8'));fs=run['frames'];picked=[fs[0],fs[len(fs)//2],fs[-1]];w=640;h=180 if c['asset_id']=='자료005' else 360;font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    preview=Image.new('RGB',(3*w,h+28),'#20242c');draw=ImageDraw.Draw(preview)
    for i,f in enumerate(picked):preview.paste(Image.open(f['path']).resize((w,h)),(i*w,28));draw.text((i*w+5,3),f'{float(F(f["actual_playback_seconds"])):.3f}s',font=font,fill='white')
    preview.save(out/'source_preview.jpg',quality=95)
    seal={'case_id':id,'sealed_at':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds'),'source_path':str(src),'source_sha256':sha(src),'source_modified_time_ns':src.stat().st_mtime_ns,'sealed_copy':str(out/'observations.json'),'copy_sha256':sha(out/'observations.json'),'grader_feedback_before_seal':False,'observations_not_rewritten_after_grading':True}
    (seals/(id+'.json')).write_text(json.dumps(seal,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'sealed':id,'sha256':seal['source_sha256'][:16]}))
print('sealed_count',len(list(seals.glob('T??.json'))))
