"""게시 긴 경로 수정만 검토하고 기존 제한 판정의 현재 해시를 갱신한다. D 쓰기/게시 실행 없음."""
from pathlib import Path
import json,hashlib,ast,difflib
HERE=Path(__file__).resolve().parent;O=HERE.parent;C=O.parents[1];L=O.parent;W=L/'R8_시험/video-record-steward-workspace'
D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
prior=read(HERE/'긴경로_수정전/R8_02_최종판정.json');current=read(O/'R8_02_최종판정.json')
publisher=L/'R8_02_결과정리.py';old=HERE/'긴경로_수정전/R8_02_결과정리.py'
assert sha(old)==prior['C_result_hashes']['phase00-build/R8_02_결과정리.py']
assert sha(HERE/'긴경로_수정전/R8_02_최종판정.md')==prior['C_result_hashes']['phase00-build/R8_02_독립검토/R8_02_최종판정.md']
a=old.read_text(encoding='utf-8');b=publisher.read_text(encoding='utf-8');tree=ast.parse(b)
exact=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='exact')
call=next(n for n in ast.walk(exact) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='copy2')
prefix=ast.literal_eval(call.args[1].left)
assert isinstance(call.args[1],ast.BinOp) and isinstance(call.args[1].op,ast.Add) and prefix=='\\\\?\\'
old_tree=ast.parse(a);old_exact=next(n for n in old_tree.body if isinstance(n,ast.FunctionDef) and n.name=='exact')
old_call=next(n for n in ast.walk(old_exact) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='copy2')
# Replacing just the destination AST recovers the already reviewed exact function.
call.args[1]=old_call.args[1]
assert ast.dump(exact,include_attributes=False)==ast.dump(old_exact,include_attributes=False)
patch=list(difflib.unified_diff(a.splitlines(),b.splitlines(),fromfile='긴경로_수정전',tofile='현재',lineterm=''))
(HERE/'긴경로_게시도구.diff').write_text('\n'.join(patch)+'\n',encoding='utf-8')
assert len([x for x in patch if x.startswith('+') and not x.startswith('+++') and x.strip()!='+'])==2
staleD=[p for p,h in prior['D_source_hashes'].items() if sha(D/p)!=h]
staleC=[p for p,h in prior['C_result_hashes'].items() if sha(C/p)!=h]
assert not staleD,staleD
assert set(staleC)=={'phase00-build/R8_02_결과정리.py'},staleC
initial=read(D/'08_검증결과/R8_02_입력보존.json')['source_hashes']
changed=[p for p,h in initial.items() if sha(D/p)!=h]
assert set(changed)=={'00_시작안내.md','01_진행현황.md','14_스킬재구성/진행상태.json','08_검증결과/R8_01_큐레이터/00_결과안내.md'}
root=D/'backup/2026-10-15_R8_02_시험정리/실행원문/video-record-steward-workspace'
copies={};bad=[]
for p in root.rglob('*'):
    if p.is_file():
        rel=p.relative_to(root);v=sha(p);copies[p.relative_to(D).as_posix()]=v
        if not (W/rel).is_file() or sha(W/rel)!=v:bad.append(rel.as_posix())
assert len(copies)==3644 and not bad,(len(copies),bad)
first_missing=None
for p in sorted(W.rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts:
        target=root/p.relative_to(W)
        if not target.is_file():first_missing={'source':p.relative_to(C).as_posix(),'destination':str(target),'destination_length':len(str(target))};break
assert first_missing and first_missing['destination_length']==266,first_missing
assert not (D/'08_검증결과/R8_02_기록관리자/00_결과안내.md').exists()
report={'scope':__doc__,'limited_completion_supported_unchanged':True,'unresolved_blocking_findings':[],'functional_change':'이미 safe()로 검증된 절대 destination에 Windows extended-length prefix만 덧붙여 copy2. 원래 경로/이름·존재 파일 SHA 대조·덮어쓰기 금지·최종 SHA 기록은 유지.','prefix_character_codes':[ord(x) for x in prefix],'exact_function_AST_identical_except_copy_destination':True,'other_change':'게시 보고서에 긴 경로 실패/보완과 모델시행 수 불포함 설명 문단1개 추가.','previous_script_sha256':sha(old),'current_script_sha256':sha(publisher),'initial164_changed_paths_unchanged':changed,'all_prior_D_source_hashes_current':True,'all_prior_C_result_hashes_current_except_publication_script':True,'partial_archive_file_count':len(copies),'partial_archive_sha_mismatches':bad,'partial_archive_sha256':copies,'first_missing':first_missing,'D_result_report_not_written':True,'D_report_and_navigation_not_published_yet':True,'D_write_performed':False,'publication_rerun_performed':False,'model_trial_count_unchanged':10,'requires_post_publication_receipt':True}
(HERE/'긴경로_독립검토.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (O/'R8_02_최종판정.md').open('a',encoding='utf-8') as f:
    f.write('\n\n## 게시 도구 긴 경로 보완 검토\n\n첫 게시가 Windows 대상 경로266자의 copy2 오류로 중단됐다. 이전 게시 도구와 이 판정 원문은 게시보완이력/긴경로_수정전에 보존했다. 이미 복사된3,644파일은 C 원문 SHA와 모두 같으며 D 결과보고서/안내·진행은 아직 게시 전이다. 착수164의 기존 안내/진행4변경 상태와 이전 판정의 D 입력 SHA는 그대로다.\n\n현재 수정은 safe()로 검증한 절대 대상에 Windows 긴 경로 prefix를 더하는 copy2 인자1곳과 보고서 설명1문단이다. 원래 파일명/경로·존재 파일 불일치 거부·SHA 대조·보존 정책은 유지된다. 제한 판정은 같고 현재 게시 도구/이 보완 기록의 C SHA만 갱신했다. D 쓰기나 게시 재실행은 하지 않았으며 실제 재개 성공/게시 후 보존·R6/R7 확인은 별도 영수증이 필요하다.\n')
current['C_result_hashes']['phase00-build/R8_02_결과정리.py']=sha(publisher)
current['publication_review']['windows_extended_length_archive_fix_reviewed']=True
current['publication_review']['partial_archive_copies_independently_hash_checked']=3644
current['publication_review']['post_publication_receipt_still_required']=True
for p in O.rglob('*'):
    if p.is_file() and p.name!='R8_02_최종판정.json':current['C_result_hashes'][p.relative_to(C).as_posix()]=sha(p)
(O/'R8_02_최종판정.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'limited_completion_supported':current['limited_completion_supported'],'unresolved_blocking_findings':current['unresolved_blocking_findings'],'publisher_sha256':sha(publisher),'partial_archive_files_checked':len(copies),'first_missing_destination_length':first_missing['destination_length']},ensure_ascii=True))
