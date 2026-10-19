from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import importlib.util,json
HERE=Path(__file__).resolve().parent;WORK=HERE.parent;OUT=HERE/'fresh'
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
OUT.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('oldgate',WORK/'phase01a-a5a/candidate/tool/prepare.py');gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
manifest=[]
for aid,folder in [('NEW-N','노듈러거더 홍보 영상'),('NEW-P','PG 착공식_자율주행영상')]:
 matches=list((D/'한맥 영상'/folder).rglob('*.mp4'));assert len(matches)==1
 p=matches[0];metadata=gate.preflight(p);duration=F(int(metadata['movie']['duration']),metadata['movie']['timescale'])
 manifest.append({'id':aid,'path':str(p),'registered_relative_path':p.relative_to(D).as_posix(),'sha256':gate.sha(p),'duration_seconds':str(duration),'previous_exposure':'자료 등록·기획 문서 검토 이력은 있으나 기존 프레임 분석 결과에서 이 원본을 찾지 못함. 이번 시각 개요 선택 후 새 장면 첫 관측을 고정. 무노출/독립 평가 주장 아님.'})
 (OUT/(aid+'-preflight.json')).write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
 times=[str(duration*F(n,5)) for n in (1,2,3)]
 req=OUT/'requests'/f'{aid}-scout.json';req.parent.mkdir(exist_ok=True);req.write_text(json.dumps(times),encoding='utf-8')
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'adapter-scope.json').write_text(json.dumps({'files_allowlisted':[m['path'] for m in manifest]},ensure_ascii=False,indent=2),encoding='utf-8')
tools=OUT/'tools';tools.mkdir(exist_ok=True)
prep="from pathlib import Path\nimport importlib.util\nROOT=Path("+repr(str(D))+")\nOUT=Path("+repr(str(OUT))+")\nspec=importlib.util.spec_from_file_location('gate_reference',Path("+repr(str(WORK/'phase01a-a5a/candidate/tool/prepare.py'))+"))\nmodule=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)\nsha=module.sha;write=module.write;preflight=module.preflight\n"
(tools/'prepare.py').write_text(prep,encoding='utf-8')
extract=(WORK/'phase01a-a5b/extract.py').read_text(encoding='utf-8').replace("RUNTIME=OUT.parent/'phase01a-a1/후보런타임'","RUNTIME=Path("+repr(str(WORK/'phase01a-a1/후보런타임'))+")")
(tools/'extract.py').write_text(extract,encoding='utf-8')
print(json.dumps([{k:v for k,v in m.items() if k!='previous_exposure'} for m in manifest],ensure_ascii=False))
