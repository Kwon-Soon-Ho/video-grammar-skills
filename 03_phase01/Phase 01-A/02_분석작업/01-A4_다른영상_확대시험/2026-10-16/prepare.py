from pathlib import Path
import hashlib,json,struct,zipfile,xml.etree.ElementTree as ET

ROOT=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
OUT=Path(__file__).resolve().parent
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

# Narrow progressive MP4 gate; this is not a general ISO-BMFF validator.
def preflight(path):
    size=path.stat().st_size
    if not 0<size<=3*1024**3: raise ValueError('file_size_limit')
    result={'size':size,'boxes':[],'tracks':[],'drefs':[],'stsd':[]}
    count=0
    with path.open('rb') as f:
        def walk(start,end,parent='',track=None,depth=0):
            nonlocal count
            if depth>10: raise ValueError('box_depth')
            pos=start
            while pos<end:
                if end-pos<8: raise ValueError('trailing_box_bytes')
                f.seek(pos); header=f.read(8); n,typ=struct.unpack('>I4s',header); hs=8
                typ=typ.decode('latin1'); count+=1
                if count>20000: raise ValueError('box_count')
                if n==1: n=struct.unpack('>Q',f.read(8))[0]; hs=16
                if n==0: n=end-pos
                if n<hs or pos+n>end: raise ValueError('box_bounds')
                loc=parent+'/'+typ; body=pos+hs; length=n-hs
                result['boxes'].append({'path':loc,'offset':pos,'size':n})
                if typ in {'moof','cmov','rmra','rmda','rdrf','sinf','encv','enca','iloc'}: raise ValueError('unsupported_box:'+loc)
                if typ=='moov' and n>32*1024**2: raise ValueError('moov_size_limit')
                if typ in {'moov','trak','mdia','minf','dinf','stbl','edts'}:
                    t=track
                    if typ=='trak':
                        t={}; result['tracks'].append(t)
                    walk(body,pos+n,loc,t,depth+1)
                elif typ in {'mvhd','mdhd','tkhd','elst','dref','stsd','stts','ctts'}:
                    if length>4*1024**2: raise ValueError('metadata_size_limit')
                    f.seek(body); b=f.read(length)
                    v=b[0]
                    if typ in {'mvhd','mdhd','tkhd','elst','ctts'} and v not in {0,1}:raise ValueError('unsupported_fullbox_version')
                    if typ in {'stts','ctts'}:
                        ec=struct.unpack_from('>I',b,4)[0]
                        if ec>100000 or 8+8*ec!=len(b): raise ValueError('timing_table_limit')
                        entries=[struct.unpack_from('>Ii' if typ=='ctts' and v==1 else '>II',b,8+i*8) for i in range(ec)]
                        if sum(a for a,_ in entries)>100000: raise ValueError('sample_count_limit')
                        track[typ]={'version':v,'entries':entries}
                    elif typ in {'mvhd','mdhd'}:
                        o=20 if v==1 else 12; scale=struct.unpack_from('>I',b,o)[0]
                        dur=struct.unpack_from('>Q' if v==1 else '>I',b,o+4)[0]
                        if scale<=0:raise ValueError('zero_timescale')
                        obj={'version':v,'timescale':scale,'duration':str(dur)}
                        if typ=='mvhd': result['movie']=obj
                        else: track['media']=obj
                    elif typ=='tkhd':
                        off=52 if v==1 else 40
                        matrix=list(struct.unpack_from('>9i',b,off))
                        track['tkhd']={'matrix':matrix,'width_fixed16':struct.unpack_from('>I',b,off+36)[0],'height_fixed16':struct.unpack_from('>I',b,off+40)[0]}
                    elif typ=='elst':
                        entries=[]; ec=struct.unpack_from('>I',b,4)[0]
                        if ec>100: raise ValueError('edit_count')
                        fmt='>Qqhh' if v==1 else '>Iihh'; step=struct.calcsize(fmt)
                        if 8+ec*step!=len(b): raise ValueError('edit_length')
                        for i in range(ec):
                            duration,media_time,ri,rf=struct.unpack_from(fmt,b,8+i*step)
                            entries.append({'segment_duration_movie_ticks':str(duration),'media_time_ticks':str(media_time),'rate_integer':ri,'rate_fraction':rf})
                        track['edits']=entries
                    elif typ=='dref':
                        ec=struct.unpack_from('>I',b,4)[0]; p=8; entries=[]
                        if ec!=1: raise ValueError('only_one_self_contained_dref_supported')
                        for _ in range(ec):
                            sn,st=struct.unpack_from('>I4s',b,p)
                            if sn<12 or p+sn>len(b): raise ValueError('dref_bounds')
                            flags=int.from_bytes(b[p+9:p+12],'big')
                            if st!=b'url ' or flags!=1 or sn!=12: raise ValueError('external_or_unknown_dref')
                            entries.append({'type':'url ','flags':flags,'self_contained':True}); p+=sn
                        if p!=len(b): raise ValueError('dref_trailing')
                        result['drefs'].append(entries)
                    elif typ=='stsd':
                        ec=struct.unpack_from('>I',b,4)[0]; p=8; entries=[]
                        if ec>16: raise ValueError('sample_entry_count')
                        for _ in range(ec):
                            sn,st=struct.unpack_from('>I4s',b,p)
                            if sn<16 or p+sn>len(b): raise ValueError('stsd_bounds')
                            if st not in {b'avc1',b'hvc1',b'hev1',b'mp4a'}: raise ValueError('unsupported_sample_entry:'+repr(st))
                            idx=struct.unpack_from('>H',b,p+14)[0]
                            if idx!=1: raise ValueError('sample_reference_not_1')
                            entry={'type':st.decode(),'data_reference_index':idx}
                            if st==b'avc1': entry['width'],entry['height']=struct.unpack_from('>HH',b,p+32)
                            entries.append(entry); p+=sn
                        if p!=len(b): raise ValueError('stsd_trailing')
                        result['stsd'].append(entries)
                pos+=n
        walk(0,size)
    if not result.get('movie') or not result['tracks'] or len(result['drefs'])!=len(result['tracks']) or len(result['stsd'])!=len(result['tracks']): raise ValueError('incomplete_track_gate')
    result['gate']='accepted_narrow_self_contained_progressive_mp4'
    result['limits']='Unknown ancillary boxes not semantically audited; explicit mov demuxer, read-only file object, drefs disabled additionally used. No claim of complete hostile-file sandbox.'
    return result

