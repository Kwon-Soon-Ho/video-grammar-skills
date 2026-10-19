from pathlib import Path
from PIL import Image
import numpy as np
import json
OUT=Path(__file__).resolve().parent
original=(OUT/'measure.py').read_text(encoding='utf-8')
original=original.replace('from scipy.signal import find_peaks\nfrom scipy.ndimage import label,find_objects\n','')
replacement='''
def find_peaks(line,distance=1,prominence=0):
    inds=np.where((line[1:-1]>=line[:-2])&(line[1:-1]>line[2:]))[0]+1
    inds=[i for i in inds if line[i]-min(line[max(0,i-distance):min(len(line),i+distance+1)])>=prominence]
    keep=[]
    for i in sorted(inds,key=lambda j:line[j],reverse=True):
        if all(abs(i-j)>=distance for j in keep):keep.append(i)
    return np.array(sorted(keep),dtype=int),{}
def label(mask):
    return mask.astype(np.uint8),1
def find_objects(labs):
    # Difference images contain long lines; return each connected horizontal row band.
    active=(labs>0).any(1);starts=np.where(active&~np.r_[False,active[:-1]])[0];ends=np.where(active&~np.r_[active[1:],False])[0]+1
    result=[]
    for y0,y1 in zip(starts,ends):
        xs=np.where((labs[y0:y1]>0).any(0))[0]
        if len(xs):result.append((slice(y0,y1),slice(xs.min(),xs.max()+1)))
    return result
'''
original=original.replace('reads=[]',replacement+'\nreads=[]')
original=original.replace("count=int((labs[sl]==i+1).sum())","count=int((labs[sl]>0).sum())")
original=original.replace('ensure_ascii=False,indent=2','ensure_ascii=False,indent=2,default=lambda v:int(v)')
exec(compile(original,str(OUT/'measure.py'),'exec'))
