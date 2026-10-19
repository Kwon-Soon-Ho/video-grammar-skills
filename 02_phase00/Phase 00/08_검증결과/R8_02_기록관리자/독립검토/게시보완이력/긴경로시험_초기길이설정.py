from pathlib import Path
import ast,hashlib,json,shutil
local=Path(__file__).parent.resolve()
source=local/'R8_02_결과정리.py'
tree=ast.parse(source.read_text(encoding='utf-8'))
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='exact')
base=local/'R8_02_게시도구시험'
base.mkdir(exist_ok=True)
src=base/'복사원문.bin'
src.write_bytes(b'archive-test\r\n\x00\xff')
def safe(p):
    p=Path(p).resolve()
    assert p.is_relative_to(base)
    return p
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
env={'BASE':base,'Path':Path,'safe':safe,'sha':sha,'shutil':shutil,'archived':{}}
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(source),'exec'),env)
dst=base.joinpath(*(['긴경로_보존검사_abcdefghijk']*8),'정확사본.bin')
assert len(str(dst))>280
env['exact'](src,dst)
env['exact'](src,dst)
io_dst=Path('\\\\?\\'+str(dst))
assert io_dst.read_bytes()==src.read_bytes()
assert env['archived']=={dst.relative_to(base).as_posix():sha(src)}
report={'destination_characters':len(str(dst)),'first_copy_and_existing_resume':True,'actual_bytes_and_sha_match':True,'relative_manifest_preserved':True,'production_D_written':False,'publisher_sha256':sha(source),'tests':'archive IO only; not model trials or skill behavior'}
(local/'R8_02_独立.tmp') if False else None
(local/'R8_02_독립검토/게시보완이력/긴경로_복사와재개_시험.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
