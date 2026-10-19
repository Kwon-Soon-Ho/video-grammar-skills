"""Verify supplied A2 extraction artifacts; no decoding or content judgement."""
import argparse, hashlib, json
from pathlib import Path
from fractions import Fraction

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def catalog(log_paths):
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
    return {'schema_version':'a3-evidence-catalog-0.1','content_verified':False,'frames':result}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--logs',nargs='+',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    data=catalog(a.logs)
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('x',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=2)
    print(json.dumps({'frames':len(data['frames']),'content_verified':False}))
