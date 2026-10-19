from pathlib import Path
import json,sys
B=Path(__file__).resolve().parent/'company-video-grammar-analyzer-workspace/iteration-1'
for spec in sys.argv[1:]:
    case,mode=spec.split(':');p=B/('eval-'+case)/mode/'outputs/observations.json';d=json.loads(p.read_text(encoding='utf-8'))
    print('\n'+spec)
    print(json.dumps({k:v for k,v in d.items() if k not in ['evidence','files_read','provenance','source','sources','metadata']},ensure_ascii=False,indent=2))
