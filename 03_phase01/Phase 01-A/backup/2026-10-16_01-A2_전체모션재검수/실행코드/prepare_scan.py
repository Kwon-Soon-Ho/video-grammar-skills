from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent/'phase01a-a2'
src=(BASE/'extract.py').read_text(encoding='utf-8')
src=src.replace('from prepare import OUT,ROOT,sha,write,preflight',"sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'phase01a-a2'))\nfrom prepare import ROOT,sha,write,preflight\nOUT=Path(__file__).resolve().parent")
src=src.replace("OUT/'입력고정과_컨테이너사전점검.json'","OUT.parent/'phase01a-a2/입력고정과_컨테이너사전점검.json'")
line=next(s for s in src.splitlines() if s.startswith('    targets=('))
src=src.replace(line,"    targets=[Fraction(i*3,4) for i in range(33)] if aid=='자료005' else [Fraction(i,2) for i in range(32)]")
src=src.replace("if phase not in {'initial','detail','initial_retest','detail_retest'}:","if phase not in {'scan','scan_retest'}:")
src=src.replace('    from PIL import Image','    from PIL import Image\n    import numpy as np')
src=src.replace('        ti=0;ordinal=0;packets=0;first_rotation=None',"        ti=0;ordinal=0;packets=0;first_rotation=None\n        proxy_count=sum(t<=targets[-1] for t in expected)\n        track_frames=np.empty((proxy_count,round(cc.height*480/cc.width),480,3),dtype=np.uint8)\n        track_index=[]")
src=src.replace("                if ti<len(targets) and t>=targets[ti]:","                small=f.reformat(width=480,height=round(f.height*480/f.width),format='rgb24',interpolation='BILINEAR')\n                track_frames[ordinal]=small.to_ndarray()\n                track_index.append({'ordinal':ordinal,'reported_pts':str(f.pts),'time_base':str(f.time_base),'seconds':str(t)})\n                if ti<len(targets) and t>=targets[ti]:")
src=src.replace("    result['input_sha256_after']=sha(p)","    data=track_frames[:ordinal]\n    np.savez_compressed(dest/'영상관측_저해상도배열.npz',rgb=data)\n    write(dest/'전프레임_시각색인.json',track_index)\n    result['tracking_proxy']={'file':'영상관측_저해상도배열.npz','sha256':sha(dest/'영상관측_저해상도배열.npz'),'decoded_RGB_sha256':__import__('hashlib').sha256(memoryview(data).cast('B')).hexdigest(),'shape':list(data.shape),'resampling':'PyAV swscale BILINEAR direct resize and RGB24 conversion','purpose':'motion discovery and pixel tracking only; not small-text transcription','every_decoded_frame_in_scope':True}\n    result['executed_script_sha256']=sha(Path(__file__))\n    result['input_sha256_after']=sha(p)")
(HERE/'scan.py').write_text(src,encoding='utf-8')
(HERE/'범위와_변경기록.json').write_text(json.dumps({'base':str(BASE/'extract.py'),'base_sha256':hashlib.sha256((BASE/'extract.py').read_bytes()).hexdigest(),'authorized_scope':{'자료005':[0,24],'자료013':[0,15.5]},'new_path':'separate fullmotion workspace','modifications':['every decoded frame gets 480px RGB tracking proxy, encoded in NPZ without pickle','JH33 coarse snapshots every0.75s; EG32 every0.5s','retained45s/1.5GiB/read/packet/frame/pixel limits','max40 PNG outputs per worker retained','no audio, API, AE/CU, A3 or Phase00 modifications']},ensure_ascii=False,indent=2),encoding='utf-8')
print(HERE/'scan.py')
