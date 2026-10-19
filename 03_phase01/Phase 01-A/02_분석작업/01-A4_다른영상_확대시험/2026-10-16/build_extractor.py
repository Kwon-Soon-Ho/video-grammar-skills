from pathlib import Path
B=Path(__file__).resolve().parent
s=(B.parent/'phase01a-a2/extract.py').read_text(encoding='utf-8')
s=s.replace('A2 narrow allowlisted worker.','A4 registered allowlist seek worker; adapted from A2.')
a=s.index('def registered(');b=s.index('def sar_status(')
s=s[:a]+'''def registered(aid):
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    matches=[x for x in manifest if x['id']==aid]
    if len(matches)!=1:raise ValueError('not_allowlisted_id')
    item=matches[0]
    allow=json.loads((OUT/'adapter-scope.json').read_text(encoding='utf-8'))['files_allowlisted']
    if item['path'] not in allow or Path(item['path']).resolve()!=(ROOT/item['registered_relative_path']).resolve():raise ValueError('path_not_allowlisted')
    return item
''' + s[b:]
s=s.replace("'wall_seconds_per_worker':45","'wall_seconds_per_worker':60").replace("'max_output_images':40","'max_output_images':40")
a=s.index('    targets=(');b=s.index('    targets=[Fraction',a)
s=s[:a]+"    targets=json.loads((OUT/'requests'/f'{aid}-{phase}.json').read_text(encoding='utf-8'))\n"+s[b:]
a=s.index('        ti=0;ordinal=0;packets=0;');b=s.index("    result['input_sha256_after']",a)
s=s[:a]+'''        import bisect
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
''' + s[b:]
s=s.replace("'decoded':ordinal","'decoded':decoded")
a=s.index('def main():')
s=s[:a]+'''def main():
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
'''
(B/'extract.py').write_text(s,encoding='utf-8')
