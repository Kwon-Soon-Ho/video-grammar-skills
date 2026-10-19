"""A4 registered allowlist seek worker; adapted from A2. No CLI arbitrary input; no audio decoding."""
from pathlib import Path
import sys,json,time,io,subprocess,traceback
from fractions import Fraction
from prepare import OUT,ROOT,sha,write,preflight

RUNTIME=OUT.parent/'phase01a-a1/후보런타임'
LIMITS={'wall_seconds_per_worker':60,'max_read_bytes':256*1024**2,'max_seeks':20000,'max_packets':4000,'max_frames':1600,'max_pixels':7680*2160,'max_output_images':40,'memory_process_bytes':2048*1024**2}
def registered(aid):
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    matches=[x for x in manifest if x['id']==aid]
    if len(matches)!=1:raise ValueError('not_allowlisted_id')
    item=matches[0]
    allow=json.loads((OUT/'adapter-scope.json').read_text(encoding='utf-8'))['files_allowlisted']
    if item['path'] not in allow or Path(item['path']).resolve()!=(ROOT/item['registered_relative_path']).resolve():raise ValueError('path_not_allowlisted')
    return item
def sar_status(sar):
    if not sar:return 'unknown'
    if sar==Fraction(1):return 'reported_square'
    raise ValueError('non_square_sar_unsupported_in_A2:'+str(sar))
class BoundedReader(io.RawIOBase):
    def __init__(self,p):self.f=open(p,'rb');self.total=0;self.seeks=0
    def readable(self):return True
    def seekable(self):return True
    def read(self,n=-1):
        if n<0 or n>4*1024**2: raise ValueError('read_request_limit')
        self.total+=n
        if self.total>LIMITS['max_read_bytes']:raise ValueError('read_budget')
        return self.f.read(n)
    def seek(self,*args):
        self.seeks+=1
        if self.seeks>LIMITS['max_seeks']:raise ValueError('seek_budget')
        return self.f.seek(*args)
    def tell(self):return self.f.tell()
    def close(self):self.f.close();super().close()
def memory_limit():
    # Worker-only Windows Job object; does not touch app/AE/CU processes.
    import ctypes as C
    from ctypes import wintypes as W
    class BASIC(C.Structure):
        _fields_=[('PerProcessUserTimeLimit',C.c_int64),('PerJobUserTimeLimit',C.c_int64),('LimitFlags',W.DWORD),('MinimumWorkingSetSize',C.c_size_t),('MaximumWorkingSetSize',C.c_size_t),('ActiveProcessLimit',W.DWORD),('Affinity',C.c_size_t),('PriorityClass',W.DWORD),('SchedulingClass',W.DWORD)]
    class IO(C.Structure): _fields_=[(x,C.c_uint64) for x in ['ReadOperationCount','WriteOperationCount','OtherOperationCount','ReadTransferCount','WriteTransferCount','OtherTransferCount']]
    class EXT(C.Structure):_fields_=[('BasicLimitInformation',BASIC),('IoInfo',IO),('ProcessMemoryLimit',C.c_size_t),('JobMemoryLimit',C.c_size_t),('PeakProcessMemoryUsed',C.c_size_t),('PeakJobMemoryUsed',C.c_size_t)]
    k=C.WinDLL('kernel32',use_last_error=True)
    k.CreateJobObjectW.restype=W.HANDLE;k.CreateJobObjectW.argtypes=[C.c_void_p,W.LPCWSTR]
    k.SetInformationJobObject.argtypes=[W.HANDLE,C.c_int,C.c_void_p,W.DWORD]
    k.AssignProcessToJobObject.argtypes=[W.HANDLE,W.HANDLE]
    k.GetCurrentProcess.restype=W.HANDLE
    job=k.CreateJobObjectW(None,None);info=EXT();info.BasicLimitInformation.LimitFlags=0x100;info.ProcessMemoryLimit=LIMITS['memory_process_bytes']
    if not job or not k.SetInformationJobObject(job,9,C.byref(info),C.sizeof(info)) or not k.AssignProcessToJobObject(job,k.GetCurrentProcess()):raise OSError(C.get_last_error(),'worker_memory_limit_failed')
    return job
def worker(aid,phase):
    job=memory_limit()
    info=registered(aid);p=Path(info['path'])
    if sha(p)!=info['sha256']:raise ValueError('input_hash_changed')
    gate=preflight(p)
    sys.path.insert(0,str(RUNTIME));import av
    from PIL import Image
    dest=OUT/'cases'/aid/phase
    if dest.exists():raise ValueError('output_exists_preserve_prior')
    dest.mkdir(parents=True)
    targets=json.loads((OUT/'requests'/f'{aid}-{phase}.json').read_text(encoding='utf-8'))
    targets=[Fraction(str(x)) for x in targets]
    if len(targets)>LIMITS['max_output_images'] or targets!=sorted(set(targets)):raise ValueError('target_count_or_order')
    result={'id':aid,'phase':phase,'input_sha256':info['sha256'],'limits':LIMITS,'tool':{'av':av.__version__,'libraries':str(av.library_versions)},'frames':[],'audio_status':'track_metadata_only_not_decoded_not_listened_not_transcribed','separate_api_calls':0,'genpts_disabled':None,'timing_status':'reported_values_until_sample_table_crosscheck','ai_model_id':'host_not_exposed','ai_internal_resize':'unknown'}
    reader=BoundedReader(p)
    with av.open(reader,mode='r',format='mov',options={'enable_drefs':'0','use_absolute_path':'0','protocol_whitelist':'file','max_pixels':str(LIMITS['max_pixels'])}) as c:
        c.flags &= ~av.container.Flags.gen_pts.value
        result['genpts_disabled']=not bool(c.flags & av.container.Flags.gen_pts.value)
        result['container']={'start_time':c.start_time,'duration':c.duration,'time_unit':'microseconds','format':c.format.name,'metadata':dict(c.metadata),'flags':c.flags}
        result['streams']=[]
        for s in c.streams:
            cc=s.codec_context
            d={'index':s.index,'type':s.type,'codec':cc.name,'time_base':str(s.time_base) if s.time_base else None,'start_time':str(s.start_time) if s.start_time is not None else None,'duration':str(s.duration) if s.duration is not None else None,'frames_reported':s.frames,'metadata':dict(s.metadata)}
            if s.type=='video':
                d.update(width=cc.width,height=cc.height,sample_aspect_ratio=str(s.sample_aspect_ratio),average_rate=str(s.average_rate),has_b_frames=cc.has_b_frames,format=str(cc.format),color_range=str(cc.color_range),colorspace=str(cc.colorspace))
            else:d.update(sample_rate=getattr(cc,'sample_rate',None),layout=str(getattr(cc,'layout',None)))
            result['streams'].append(d)
        vs=list(c.streams.video)
        if len(vs)!=1:raise ValueError('single_video_required')
        s=vs[0];cc=s.codec_context
        if cc.width*cc.height>LIMITS['max_pixels'] or cc.width<=0 or cc.height<=0:raise ValueError('pixel_limit')
        cc.thread_count=1
        video_track=next(t for t in gate['tracks'] if t['tkhd']['width_fixed16']>0)
        if video_track['tkhd']['matrix']!=[65536,0,0,0,65536,0,0,0,1073741824]:raise ValueError('nonidentity_matrix_unsupported_in_A2')
        write(dest/'디코딩전_메타데이터.json',result)
        result['sar_status']=sar_status(s.sample_aspect_ratio)
        if result['sar_status']=='unknown':result['sar_limit']='raw raster resized proportionally; no display-aspect/precise spatial claim'
        edits=video_track.get('edits',[])
        if len(edits)!=1 or edits[0]['rate_integer']!=1 or edits[0]['rate_fraction']!=0 or int(edits[0]['media_time_ticks'])<0:raise ValueError('complex_edit_unsupported')
        media_scale=video_track['media']['timescale'];offset=Fraction(int(edits[0]['media_time_ticks']),media_scale)
        durations=[b for a,b in video_track['stts']['entries'] for _ in range(a)]
        cts=[b for a,b in video_track.get('ctts',{'entries':[[len(durations),0]]})['entries'] for _ in range(a)]
        if len(cts)!=len(durations):raise ValueError('ctts_count')
        raw=[];dts=0
        for duration,co in zip(durations,cts):raw.append(Fraction(dts+co,media_scale)-offset);dts+=duration
        expected=sorted(raw)
        result['timing_mapping']={'basis':'single rate-1 elst, stts+ctts table reconstructed, then compared to displayed decoded PTS','edit_media_offset':str(offset),'playback_zero_movie_ticks':'0','first_expected_presentation':str(expected[0]),'video_media_scale':media_scale,'sample_count':len(expected),'raw_container_cts_of_playback_zero':str(offset*media_scale),'movie_timescale':gate['movie']['timescale'],'container_duration_vs_video_edit_difference_seconds':str(Fraction(int(gate['movie']['duration'])-int(edits[0]['segment_duration_movie_ticks']),gate['movie']['timescale']))}
        import bisect
        ti=0;decoded=0;packets=0;first_rotation=None
        for requested in targets:
            c.seek(int(requested/s.time_base),stream=s,backward=True,any_frame=False)
            selected=False;previous=None
            for packet in c.demux(s):
                packets+=1
                if packets>LIMITS['max_packets']:raise ValueError('packet_limit')
                for f in packet.decode():
                    decoded+=1
                    if decoded>LIMITS['max_frames']:raise ValueError('frame_limit')
                    if f.pts is None or not f.time_base:raise ValueError('missing_frame_time')
                    t=f.pts*f.time_base
                    ordinal=bisect.bisect_left(expected,t)
                    if ordinal>=len(expected) or t!=expected[ordinal]:raise ValueError('sample_table_pts_mismatch')
                    if previous is not None and t<=previous:raise ValueError('nonmonotonic_seek_decode')
                    previous=t
                    if f.width*f.height>LIMITS['max_pixels']:raise ValueError('frame_pixel_limit')
                    if first_rotation is None:first_rotation={'rotation_reported_ccw':f.rotation,'raw_raster':[f.width,f.height],'matrix_basis':'tkhd identity','rotation_applied':False}
                    if t<requested:continue
                    wanted=bisect.bisect_left(expected,requested)
                    if ordinal!=wanted:raise ValueError('seek_skipped_requested_frame')
                    image=f.to_image();raw_size=image.size
                    # Keep native raster so crops retain original thin-line detail.
                    width,height=raw_size
                    fp=dest/f'f_{ordinal:05d}_{float(t):07.3f}.png';image.save(fp)
                    result['frames'].append({'frame_id':aid+'-'+phase+'-'+str(ordinal),'requested_playback_seconds':str(requested),'actual_playback_seconds':str(t),'reported_pts':str(f.pts),'time_base':str(f.time_base),'display_ordinal_zero_based':ordinal,'container_cts_ticks':str((t+offset)*media_scale),'path':str(fp),'sha256':sha(fp),'raster':list(raw_size),'derived_size':[width,height],'transforms':[{'op':'colorspace_to_RGB','method':'PyAV to_image / swscale','range_accuracy_validated':False}],'human_review':'not_requested_AI_observation'})
                    ti+=1;selected=True;break
                if selected:break
            if not selected:raise ValueError('incomplete_targets')
        result.update(decoded_frames=decoded,packets=packets,io_requested_bytes=reader.total,seeks=reader.seeks,orientation=first_rotation,timing_status='all_decoded_frame_pts_match_reconstructed_sample_tables_in_this_window',complete_target_selection=ti==len(targets),selection='seek backward to keyframe, validate every decoded PTS against sample table and select first presentation >= requested')
    result['input_sha256_after']=sha(p)
    if result['input_sha256_after']!=info['sha256']:raise ValueError('source_changed_during_run')
    write(dest/'실행기록.json',result)
    print(json.dumps({'id':aid,'phase':phase,'images':len(result['frames']),'decoded':decoded,'result':str(dest/'실행기록.json')},ensure_ascii=False))
def main():
    if len(sys.argv)==4 and sys.argv[1]=='worker':worker(sys.argv[2],sys.argv[3]);return
    aid,phase=sys.argv[1:3]
    begin=time.monotonic()
    try:
        p=subprocess.run([sys.executable,'-B','-X','utf8',__file__,'worker',aid,phase],capture_output=True,text=True,encoding='utf-8',timeout=LIMITS['wall_seconds_per_worker'])
        r={'id':aid,'phase':phase,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    except subprocess.TimeoutExpired as e:r={'id':aid,'phase':phase,'exit':'timeout','stdout':str(e.stdout),'stderr':str(e.stderr)}
    r['elapsed_seconds']=time.monotonic()-begin
    write(OUT/f'run_{aid}_{phase}.json',r);print(json.dumps(r,ensure_ascii=False))
    if r['exit']!=0:raise SystemExit(1)
if __name__=='__main__':main()
