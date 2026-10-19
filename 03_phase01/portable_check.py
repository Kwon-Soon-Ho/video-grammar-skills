"""Relocation smoke check; creates derived outputs only. Not a visual/quality evaluation."""
from pathlib import Path
import argparse,sys,json,subprocess,shutil,hashlib

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--root',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 root=Path(a.root).resolve();out=Path(a.out).resolve()
 if out.exists():raise SystemExit('--out must be a new folder')
 for folder in ['01_skills','02_phase00','03_phase01']:
  if not (root/folder).is_dir():raise SystemExit('missing extracted ZIP folder: '+folder)
 if any(out.is_relative_to(root/x) for x in ['01_skills','02_phase00','03_phase01']):raise SystemExit('output must be outside package folders')
 out.mkdir(parents=True)
 tool=root/'01_skills/analyzer/candidate_draft13/company-video-grammar-analyzer/scripts/knowledge_links.py'
 source=root/'03_phase01/Phase 01-A/05_결과보고/2026-10-19_draft13_00지식연결/pilot'
 shutil.copytree(source,out/'pilot')
 catalog=out/'catalog.json';index=out/'usage-index.json';log=[]
 def run(name,args):
  cmd=[sys.executable,'-B','-X','utf8',str(tool),*map(str,args)]
  r=subprocess.run(cmd,encoding='utf-8',capture_output=True)
  (out/(name+'.stdout.json')).write_text(r.stdout,encoding='utf-8')
  (out/(name+'.stderr.txt')).write_text(r.stderr,encoding='utf-8')
  log.append({'name':name,'argv':cmd,'exit_code':r.returncode})
  (out/'execution.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
  if r.returncode:raise SystemExit(name+' failed; see '+str(out))
  return json.loads(r.stdout) if r.stdout.strip() else None
 run('catalog',['catalog','--phase00',root/'02_phase00/Phase 00','--out',catalog])
 records=[out/'pilot'/f for f in ['case-134.json','case-172.json','motion-windows.json']]
 for n,r in enumerate(records):run('check-'+str(n+1),['check','--catalog',catalog,'--record',r])
 run('index',['index','--catalog',catalog,'--records',*records,'--out',index])
 queries=[('work',['--query','업무 이미지 묶음']),('building',['--query','건물/기단']),('profile',['--query','크림 공간의 입체 정보 무대']),('review',['--id','MR-08']),('motion',['--id','FUNCTION-REVEAL','--motion-only'])]
 results=[]
 for name,q in queries:
  d=run('query-'+name,['query','--catalog',catalog,'--index',index,*q])
  if not d.get('uses'):raise SystemExit('empty query result: '+name)
  results.append({'query':name,'uses':len(d['uses']),'record_ids':sorted({x['record_id'] for x in d['uses']})})
 summary={'status':'passed','scope':'relocated catalog/reference/index/query smoke check only','queries':results,'company_approved':False,'original_packages_modified':False}
 (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
