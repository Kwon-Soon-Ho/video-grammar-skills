from pathlib import Path
import sys,json,shutil,re
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'phase01a-a2'))
from prepare import ROOT,sha,write
STAGE=HERE/'게시안';P='Phase 01-A';BK=f'{P}/backup/2026-10-16_01-A2_전체모션재검수'
def main():
    data=json.loads((HERE/'게시명세.json').read_text(encoding='utf-8'));files=data['files'];before=data['expected_before']
    rel=f'{BK}/실행코드/publish.py';p=STAGE/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(__file__,p)
    files=[x for x in files if x['relative_path']!=rel]+[{'relative_path':rel,'sha256':sha(p),'bytes':p.stat().st_size}]
    prefixes=[f'{P}/02_분석작업/01-A2_전체모션재검수/',f'{P}/04_검증자료/01-A2_전체모션재검수/',f'{BK}/','작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A2/']
    names={f'{P}/00_진행안내/01-A_계획상태.json',f'{P}/00_진행안내/16_01-A2_현재구간_모션재검수_현재안내.json',f'{P}/05_결과보고/08_01-A2_현재구간_모션재검수_보고.md',f'{P}/04_검증자료/01-A2_작은예비/사람검수_대기.json'}
    link_count=0
    for item in files:
        rel=item['relative_path'];src=STAGE/rel;dst=(ROOT/rel).resolve()
        if not dst.is_relative_to(ROOT.resolve()) or not(rel in names or any(rel.startswith(p) for p in prefixes)):raise ValueError('destination_scope')
        if sha(src)!=item['sha256']:raise ValueError('staged_changed:'+rel)
        if dst.exists() and sha(dst)!=item['sha256'] and before.get(rel)!=sha(dst):raise ValueError('unexpected_existing_change:'+rel)
        if src.suffix=='.json':json.loads(src.read_text(encoding='utf-8-sig'))
        if src.suffix=='.md' and not any(part in rel for part in ['/변경전/','/중간본과_실패/']):
            content=src.read_text(encoding='utf-8')
            for ref in re.findall(r'\]\(([^)]+)\)',content):
                if ref.startswith(('https:','http:')):continue
                ref=ref.strip('<>')
                if re.match(r'^[A-Za-z]:',ref):
                    absolute=Path(ref).resolve()
                    target=absolute.relative_to(ROOT.resolve()) if absolute.is_relative_to(ROOT.resolve()) else absolute
                else:target=Path(rel).parent/ref
                if not (STAGE/target).is_file() and not (ROOT/target).is_file():raise ValueError('broken_link:'+ref)
                link_count+=1
    data['files']=files;write(HERE/'게시명세.json',data)
    audit={'files':len(files),'bytes':sum(x['bytes'] for x in files),'links_checked':link_count,'expected_changes':list(before),'conflicts':0}
    write(HERE/'게시전_확인.json',audit)
    if '--publish' not in sys.argv:print(json.dumps(audit,ensure_ascii=False));return
    for item in files:
        dst=ROOT/item['relative_path'];dst.parent.mkdir(parents=True,exist_ok=True)
        if not dst.exists() or sha(dst)!=item['sha256']:shutil.copy2(STAGE/item['relative_path'],dst)
        if sha(dst)!=item['sha256']:raise ValueError('publication_hash_mismatch')
    receipt={**audit,'all_hashes_match':True,'manifest_sha256':sha(HERE/'게시명세.json'),'before_hashes':before,'current_hashes':{x['relative_path']:x['sha256'] for x in files if x['relative_path'] in before},'scope':'copy integrity only; new N1–N8 still human-pending'}
    write(HERE/'게시후_검증.json',receipt);write(ROOT/P/'04_검증자료/01-A2_전체모션재검수/게시후_검증.json',receipt)
    print(json.dumps({'all_hashes_match':True,'files':len(files),'human_pending_groups':8,'A3_started':False},ensure_ascii=False))
if __name__=='__main__':main()
