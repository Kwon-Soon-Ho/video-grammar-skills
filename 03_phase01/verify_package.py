"""Verify the files listed by a package manifest. Does not execute packaged source."""
from pathlib import Path
import sys,json,hashlib
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 root=Path(sys.argv[1]).resolve();d=json.loads((root/'package-manifest.json').read_text(encoding='utf-8'));bad=[]
 for row in d['files']:
  p=root/row['path']
  if not p.is_relative_to(root) or not p.is_file() or digest(p)!=row['sha256']:bad.append(row['path'])
 print(json.dumps({'checked':len(d['files']),'failed':bad,'scope':'listed included bytes only; manifest itself and extra files are not authenticated'},ensure_ascii=False))
 return bool(bad)
if __name__=='__main__':sys.exit(main())
