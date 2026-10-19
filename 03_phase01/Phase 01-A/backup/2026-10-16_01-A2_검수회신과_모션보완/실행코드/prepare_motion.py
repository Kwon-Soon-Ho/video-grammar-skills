from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'phase01a-a2'
src=(BASE/'extract.py').read_text(encoding='utf-8')
old=next(s for s in src.splitlines() if s.startswith('    targets=('))
src=src.replace(old,"    targets=[Fraction(4)+Fraction(i,20) for i in range(31)]")
src=src.replace("if phase not in {'initial','detail','initial_retest','detail_retest'}:","if phase not in {'motion_review','motion_review_retest'}:")
src=src.replace("    job=memory_limit()","    if aid!='자료013':raise ValueError('motion_review_EG_only')\n    job=memory_limit()")
src=src.replace("from prepare import OUT,ROOT,sha,write,preflight", "sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'phase01a-a2'))\nfrom prepare import OUT,ROOT,sha,write,preflight")
(HERE/'extract_motion.py').write_text(src,encoding='utf-8')
(HERE/'변경범위.json').write_text(json.dumps({'base_script':str(BASE/'extract.py'),'base_sha256':hashlib.sha256((BASE/'extract.py').read_bytes()).hexdigest(),'changes':['EG-only worker','4.0 to5.5s at0.05s request spacing,31 images','separate phase names and outputs','import existing prepare without modifying it'],'retained':['registration/hash','MP4 self-contained gate','sample table time mapping','worker45s/1.5GiB memory','packet/frame/pixel/read/output limits','no audio/API']},ensure_ascii=False,indent=2),encoding='utf-8')
print(HERE/'extract_motion.py')
