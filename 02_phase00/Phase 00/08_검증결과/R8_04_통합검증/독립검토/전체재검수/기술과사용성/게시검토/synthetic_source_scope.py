from pathlib import Path
import sys,importlib.util,json,hashlib,ast
O=Path(__file__).resolve().parent;L=O.parents[2];sys.path.insert(0,str(L));P=L/'R8_04_최종게시.py';before=P.read_bytes();R=O/'합성_목록범위';assert not R.exists();R.mkdir(parents=True)
s=importlib.util.spec_from_file_location('publication_source_scope_only',P);p=importlib.util.module_from_spec(s);s.loader.exec_module(p);p.L=R;p.W=R/'시험';p.RV=R/'검토'
exclude=['__pycache__','고정문맥_검증전용','isolated','robustness','targeted_v3']
for folder in [p.W,p.RV,R/'전체재검수']:
 folder.mkdir();(folder/'keep.txt').write_bytes(b'own synthetic metadata')
 for name in exclude:
  q=folder/name;q.mkdir();(q/'must_not_read.txt').write_bytes(b'sentinel')
for name in ['R8_04_unit.py','R8_후보연결확인.py','R8_01_뷰어작성.py','공통지원.py','R8_04_최종보고_초안.md']:(R/name).write_bytes(b'synthetic')
original_sha=p.sha
def bounded_sha(q):
 assert 'must_not_read.txt' not in str(q),'Excluded copy content was read'
 return original_sha(q)
p.sha=bounded_sha;rows=p.sources();tree=ast.parse(before.decode('utf-8'));ast.parse((L/'R8_04_최종보고_초안.md').read_text(encoding='utf-8')) if False else None
data={'publication_script_sha256':hashlib.sha256(before).hexdigest(),'draft_sha256':hashlib.sha256((L/'R8_04_최종보고_초안.md').read_bytes()).hexdigest(),'script_unchanged':P.read_bytes()==before,'synthetic_source_count':len(rows),'expected_count':8,'exclude_subtrees_not_hashed':len(rows)==8,'scope':'sources() only after replacing all source roots with own tiny C fixture; main/prepare not called, no real trial outputs opened, no D writes; model trials0','rows':rows}
(O/'05_최종소스범위_정적확정.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(O/'검토본_최종게시.py').write_bytes(before)
(O/'검토본_최종보고_초안.md').write_bytes((L/'R8_04_최종보고_초안.md').read_bytes())
print(json.dumps({k:v for k,v in data.items() if k!='rows'},ensure_ascii=False,indent=2))
