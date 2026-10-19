"""긴 경로 IO 일관화만 정적/바이트 확인. 게시·모델·IO 시험을 재실행하지 않는다."""
from pathlib import Path
import ast,json,hashlib,difflib
H=Path(__file__).resolve().parent;O=H.parent;L=O.parent;C=O.parents[1]
D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
prior=read(H/'긴경로_해시보완전/R8_02_최종판정.json');verdict=read(O/'R8_02_최종판정.json')
old=H/'긴경로_해시보완전/R8_02_결과정리.py';new=L/'R8_02_결과정리.py'
assert sha(old)==prior['C_result_hashes']['phase00-build/R8_02_결과정리.py']
a=old.read_text(encoding='utf-8');b=new.read_text(encoding='utf-8');at=ast.parse(a);bt=ast.parse(b)
af=next(n for n in at.body if isinstance(n,ast.FunctionDef) and n.name=='exact');bf=next(n for n in bt.body if isinstance(n,ast.FunctionDef) and n.name=='exact')
patch=list(difflib.unified_diff(a.splitlines(),b.splitlines(),fromfile='해시보완전',tofile='현재',lineterm=''))
(H/'긴경로_해시_게시도구.diff').write_text('\n'.join(patch)+'\n',encoding='utf-8')
# Only exact and one report string literal may differ; all other executable AST is preserved.
different=[]
for i,(x,y) in enumerate(zip(at.body,bt.body)):
    if ast.dump(x,include_attributes=False)!=ast.dump(y,include_attributes=False):different.append((i,type(x).__name__))
assert len(at.body)==len(bt.body) and len(different)==2,different
assert any(isinstance(at.body[i],ast.FunctionDef) and at.body[i].name=='exact' for i,_ in different)
other=[i for i,_ in different if not isinstance(at.body[i],ast.FunctionDef)][0]
assert isinstance(at.body[other],ast.Assign) and [ast.dump(x) for x in at.body[other].targets]==[ast.dump(x) for x in bt.body[other].targets]
assert ast.literal_eval(next(n for n in ast.walk(bf) if isinstance(n,ast.Constant) and isinstance(n.value,str)))=='\\\\?\\'
calls=sorted({n.func.attr for n in ast.walk(bf) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)})
assert calls==['as_posix','copy2','exists','mkdir','relative_to']
unit=read(H/'긴경로_복사와재개_시험.json');assert unit['publisher_sha256']==sha(new)
src=L/'R8_02_게시도구시험/복사원문.bin'
dst=(L/'R8_02_게시도구시험').joinpath(*(['긴경로_보존검사_abcdefghijk']*10),'정확사본.bin')
assert dst.is_relative_to(C) and len(str(dst))==290
io_dst=Path('\\\\?\\'+str(dst));assert io_dst.read_bytes()==src.read_bytes()
staleD=[p for p,h in prior['D_source_hashes'].items() if sha(D/p)!=h]
staleC=[p for p,h in prior['C_result_hashes'].items() if sha(C/p)!=h]
assert not staleD and set(staleC)=={'phase00-build/R8_02_결과정리.py'},(staleD,staleC)
initial=read(D/'08_검증결과/R8_02_입력보존.json')['source_hashes']
changed=[p for p,h in initial.items() if sha(D/p)!=h]
assert set(changed)=={'00_시작안내.md','01_진행현황.md','14_스킬재구성/진행상태.json','08_검증결과/R8_01_큐레이터/00_결과안내.md'}
assert not (D/'08_검증결과/R8_02_기록관리자/00_결과안내.md').exists()
early=H/'긴경로시험_초기길이설정.py';assert early.is_file()
report={'scope':__doc__,'limited_completion_supported_unchanged':True,'unresolved_blocking_findings':[],'publisher_sha256':sha(new),'previous_publisher_sha256':sha(old),'exact_io_review':'safe 검증된 dst로부터 io_dst를 만들고 mkdir/exists/copy2/SHA에 일관 사용. 상대 manifest는 원래 dst.relative_to(BASE)로 유지. 존재 사본 SHA 불일치 거부와 원문/파일명/목적 경계 유지.','AST_differing_top_level_nodes':different,'other_report_change':'이력 문단을 첫 복사 중단+두 번째 SHA 재열기 중단에 맞춰 설명.','actual_290_path_existing_bytes_sha_match':True,'actual_test_source_sha256':sha(src),'actual_test_destination_sha256':sha(io_dst),'test_report_current_code_hash_matches':True,'author_copy_and_resume_test_read_not_independently_rerun':True,'author_initial_length_assert_source_preserved_sha256':sha(early),'prior_D_hashes_unchanged':True,'prior_C_hashes_unchanged_except_publisher':True,'initial164_changed_paths_unchanged':changed,'D_report_not_written':True,'D_write_performed':False,'publication_rerun_performed':False,'model_trials_unchanged':10,'post_publication_preservation_and_R6_R7_receipt_still_required':True}
(H/'긴경로_해시_독립검토.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (O/'R8_02_최종판정.md').open('a',encoding='utf-8') as f:
    f.write('\n\n## 긴 경로 SHA 재열기 보완 검토\n\n두 번째 게시는 긴 대상 복사 뒤 일반 경로로 SHA를 다시 읽는 단계에서 중단됐다. 보고서/진행은 게시 전이고 기존 판정의 D173경로와 C 결과는 게시 도구 외에 같다. 직전 도구/판정 원문은 게시보완이력/긴경로_해시보완전에 보존했다.\n\n현재 exact는 safe() 검증 뒤 만든 같은 io_dst를 폴더 생성·존재 확인·복사·SHA에 일관되게 쓰며, 상대 manifest는 원래 dst 기준을 유지한다. 다른 실행 AST는 그대로이고 이력 설명만 두 중단으로 정확화했다. 작성자의 현재 코드SHA에 연결된290자 신규복사/기존사본재개 시험과 초기 길이설정 실패 원문을 읽었고, 실제 남은290자 사본의 바이트/SHA도 직접 확인했다. 본 검토는 그 IO 시험이나 게시를 재실행한 것이 아니다. 제한 판정은 유지하고 현재 도구/보완 기록 SHA를 갱신했다. 게시 성공/후속 보존·R6/R7 조회는 여전히 별도 영수증이 필요하다.\n')
verdict['C_result_hashes']['phase00-build/R8_02_결과정리.py']=sha(new)
verdict['C_result_hashes']['phase00-build/R8_02_게시도구_긴경로시험.py']=sha(L/'R8_02_게시도구_긴경로시험.py')
verdict['publication_review']['windows_extended_length_all_archive_IO_reviewed']=True
verdict['publication_review']['author_290_path_copy_resume_test_read_actual_bytes_checked']=True
verdict['publication_review']['post_publication_receipt_still_required']=True
for p in O.rglob('*'):
    if p.is_file() and p!=O/'R8_02_최종판정.json':verdict['C_result_hashes'][p.relative_to(C).as_posix()]=sha(p)
(O/'R8_02_최종판정.json').write_text(json.dumps(verdict,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'limited_completion_supported':verdict['limited_completion_supported'],'unresolved_blocking_findings':[],'publisher_sha256':sha(new),'D_existing_hashes_unchanged':True,'actual_long_path_bytes_sha_checked':290},ensure_ascii=True))
