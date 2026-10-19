from pathlib import Path
HERE=Path(__file__).resolve().parent
src=(HERE.parent/'phase01a-a2/extract.py').read_text(encoding='utf-8')
src=src.replace('from prepare import OUT,ROOT,sha,write,preflight',"sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'phase01a-a2'))\nfrom prepare import ROOT,sha,write,preflight\nOUT=Path(__file__).resolve().parent")
src=src.replace("OUT/'입력고정과_컨테이너사전점검.json'","OUT.parent/'phase01a-a2/입력고정과_컨테이너사전점검.json'")
line=next(s for s in src.splitlines() if s.startswith('    targets=('))
src=src.replace(line,"    if aid!='자료013':raise ValueError('wrong_asset')\n    targets=[0,.25,.5,.75,1,1.25,1.5,1.75,1.9,2.1,2.4,3.1,3.2,3.3,3.4,3.5]")
src=src.replace('width=1920;height=', 'width=3840;height=')
(HERE/'native.py').write_text(src,encoding='utf-8')
print('native source prepared: 16 fixed times, registered EG-BIM only; existing limits retained')
