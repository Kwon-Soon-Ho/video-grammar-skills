from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent
def compact(v):
    if isinstance(v,dict):
        return {k:compact(x) for k,x in v.items() if k not in {'evidence','files_read','frame_sampling','source_frames','all_files_read','provenance','source_access_audit','measurement_evidence','tools_used','source_pngs_read_for_visualization_or_measurement'}}
    if isinstance(v,list):return [compact(x) for x in v]
    return v
for case in sys.argv[1:]:
    seal=json.loads((HERE/'seals'/(case+'.json')).read_text(encoding='utf-8'))
    r=json.loads(Path(seal['sealed_copy']).read_text(encoding='utf-8-sig'))
    print(json.dumps(compact(r),ensure_ascii=False,indent=2))
