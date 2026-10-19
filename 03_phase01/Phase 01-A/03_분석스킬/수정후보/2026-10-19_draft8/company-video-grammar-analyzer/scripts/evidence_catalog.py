"""Verify supplied A2 extraction artifacts; no decoding or content judgement."""
import argparse, hashlib, json
from pathlib import Path
from fractions import Fraction

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def catalog(log_paths, crops=None):
    result=[]
    for p in log_paths:
        log=json.loads(Path(p).read_text(encoding='utf-8'))
        if not log.get('complete_target_selection'): raise ValueError('incomplete extraction')
        if log['input_sha256']!=log['input_sha256_after']: raise ValueError('source changed')
        previous=None
        for f in log['frames']:
            t=Fraction(f['actual_playback_seconds'])
            if t<0 or (previous is not None and t<=previous): raise ValueError('time order/duplicate')
            previous=t
            # This A2 adapter normalizes decoded PTS to playback zero. Raw CTS is separate.
            if Fraction(f['reported_pts'])*Fraction(f['time_base'])!=t: raise ValueError('PTS mapping mismatch for A2 adapter')
            if sha(f['path'])!=f['sha256']: raise ValueError('frame hash mismatch')
            result.append(dict(f, extraction_log=str(Path(p).resolve()), source_sha256=log['input_sha256']))
    if crops:
        from PIL import Image
        parents={str(Path(f['path']).resolve()).casefold():f for f in result}
        for crop in crops:
            parent=parents.get(str(Path(crop['parent_path']).resolve()).casefold())
            if parent is None:raise ValueError('crop parent not in extraction catalog')
            box=crop['crop_xyxy_native_pixels']
            if len(box)!=4 or any(type(v)!=int for v in box):raise ValueError('crop coordinates')
            with Image.open(parent['path']) as original, Image.open(crop['path']) as derived:
                x0,y0,x1,y1=box
                if original.width*original.height>7680*2160 or not 0<=x0<x1<=original.width or not 0<=y0<y1<=original.height:raise ValueError('crop bounds')
                if derived.mode!='RGB' or original.mode!='RGB' or derived.size!=(x1-x0,y1-y0):raise ValueError('crop mode or size')
                if derived.tobytes()!=original.crop(box).tobytes():raise ValueError('crop pixels do not match parent')
            result.append(dict(parent,path=str(Path(crop['path']).resolve()),sha256=sha(crop['path']),parent_path=parent['path'],crop_xyxy_native_pixels=box,derived_size=[x1-x0,y1-y0],transforms=[{'op':'verified_pixel_exact_crop','xyxy':box}]))
    return {'schema_version':'a3-evidence-catalog-0.1','content_verified':False,'frames':result}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--logs',nargs='+',required=True);p.add_argument('--out',required=True);p.add_argument('--crops');a=p.parse_args()
    crops=json.loads(Path(a.crops).read_text(encoding='utf-8')) if a.crops else None
    data=catalog(a.logs,crops)
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('x',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=2)
    print(json.dumps({'frames':len(data['frames']),'content_verified':False}))
