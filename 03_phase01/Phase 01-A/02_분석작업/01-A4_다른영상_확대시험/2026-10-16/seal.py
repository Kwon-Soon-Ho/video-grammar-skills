from pathlib import Path
from prepare import sha,write
import datetime,json
B=Path(__file__).resolve().parent
for folder in (B/'company-video-grammar-analyzer-workspace').glob('iteration-*/eval-*/*/outputs'):
 if not (folder/'observations.json').exists() or not (folder/'observations.md').exists():continue
 dest=folder.parent/'output-seal.json'
 if dest.exists():
  seal=json.loads(dest.read_text(encoding='utf-8'))
  assert all(sha(Path(r['path']))==r['sha256'] for r in seal['files']),'sealed output changed'
 else:
  write(dest,{'sealed_at':datetime.datetime.now().astimezone().isoformat(),'files':[{'path':str(p),'sha256':sha(p)} for p in folder.iterdir() if p.is_file()]})
  print(folder.parent)
