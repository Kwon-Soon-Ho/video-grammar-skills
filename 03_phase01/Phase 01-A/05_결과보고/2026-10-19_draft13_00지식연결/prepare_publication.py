from pathlib import Path
import json,hashlib,datetime,importlib.util
R=Path(__file__).resolve().parent;W=R.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def manifest(root):return {f.relative_to(root).as_posix():sha(f) for f in sorted(root.rglob('*')) if f.is_file() and '__pycache__' not in f.parts}
old=R/'backup/draft12/company-video-grammar-analyzer';new=R/'candidate/company-video-grammar-analyzer'
prior=W/'collection-skill-structure-20261019/candidate/company-video-grammar-analyzer'
assert manifest(old)==manifest(prior)
write(R/'backup-manifest.json',{'source':str(prior),'files':manifest(old)})
write(R/'candidate-manifest.json',manifest(new))
write(R/'changed-files.json',[p for p,h in manifest(new).items() if manifest(old).get(p)!=h])
pins=json.loads((W/'phase00-coverage-audit-20261019/data/protected-source-pins.json').read_text(encoding='utf-8'))
assert all(sha(Path(x['path']))==x['sha256'] for x in pins)
write(R/'protected-before.json',pins)
spec=importlib.util.spec_from_file_location('kl',new/'scripts/knowledge_links.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
cat=m.catalog_read(R/'knowledge/catalog.json');queries=[('업무 묶음',{'query_text':'업무 이미지 묶음'}),('건물/기단',{'query_text':'건물/기단'}),('두 화면 표현 가족',{'query_text':'크림 공간의 입체 정보 무대'}),('값 변화 관련 원칙',{'concept_id':'MR-08'}),('관측된 공개 모션',{'concept_id':'FUNCTION-REVEAL','motion_only':True}),('정지 화살표는 모션에서 제외',{'query_text':'요청·지원 방향 라벨','motion_only':True})]
out=[]
for name,args in queries:
    result=m.query(cat,R/'knowledge/catalog.json',R/'pilot/usage-index.json',**args)
    out.append({'name':name,'arguments':args,'result':result})
write(R/'pilot/actual-queries.json',out)
print('backup/candidate pins and six actual pilot queries saved; original active10/candidate12/Phase00 pins unchanged')
