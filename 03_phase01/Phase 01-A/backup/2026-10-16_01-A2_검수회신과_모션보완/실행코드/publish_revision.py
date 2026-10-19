from pathlib import Path
import sys,json,shutil,re,hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'phase01a-a2'))
from prepare import ROOT,sha,write
STAGE=HERE/'게시안';P='Phase 01-A'
BK=f'{P}/backup/2026-10-16_01-A2_검수회신과_모션보완'
def main():
    data=json.loads((HERE/'게시명세.json').read_text(encoding='utf-8'));files=data['files'];before=data['expected_before']
    # Add this publisher to the preserved source for the exact write operation.
    rel=f'{BK}/실행코드/publish_revision.py';p=STAGE/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(__file__,p)
    files=[x for x in files if x['relative_path']!=rel]+[{'relative_path':rel,'sha256':sha(p),'bytes':p.stat().st_size}]
    allowed=[f'{P}/02_분석작업/01-A2_작은예비/',f'{P}/04_검증자료/01-A2_작은예비/',f'{BK}/','작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A2/']
    direct={f'{P}/00_진행안내/01-A_계획상태.json',f'{P}/00_진행안내/15_01-A2_실행결과_현재안내.json',f'{P}/05_결과보고/07_01-A2_작은예비분석_보고.md'}
    links=0
    for x in files:
        rel=x['relative_path'];src=STAGE/rel;dst=(ROOT/rel).resolve()
        if not dst.is_relative_to(ROOT.resolve()) or not (rel in direct or any(rel.startswith(a) for a in allowed)):raise ValueError('destination_not_allowed')
        if sha(src)!=x['sha256']:raise ValueError('staged_hash_changed')
        if dst.exists() and sha(dst)!=x['sha256'] and before.get(rel)!=sha(dst):raise ValueError('unplanned_existing_change:'+rel)
        if src.suffix=='.json':json.loads(src.read_text(encoding='utf-8-sig'))
        if src.suffix=='.md' and '/변경전/' not in rel:
            for target in re.findall(r'\]\(([^)]+)\)',src.read_text(encoding='utf-8')):
                if target.startswith(('http:','https:')):continue
                target=target.strip('<>');dest=(Path(rel).parent/target)
                if not (STAGE/dest).is_file() and not (ROOT/dest).is_file():raise ValueError('broken_link:'+target)
                links+=1
    data['files']=files;write(HERE/'게시명세.json',data)
    if '--publish' not in sys.argv:print(json.dumps({'files':len(files),'links_checked':links,'conflicts':0},ensure_ascii=False));return
    for x in files:
        src=STAGE/x['relative_path'];dst=ROOT/x['relative_path'];dst.parent.mkdir(parents=True,exist_ok=True)
        if not dst.exists() or sha(dst)!=x['sha256']:shutil.copy2(src,dst)
        if sha(dst)!=x['sha256']:raise ValueError('copy_mismatch')
    receipt={'all_hashes_match':True,'files':len(files),'links_checked':links,'manifest_sha256':sha(HERE/'게시명세.json'),'modified_current_files':list(before),'before_hashes':before,'current_hashes':{x['relative_path']:x['sha256'] for x in files if x['relative_path'] in before},'scope':'this revision copy verification, old publication receipt remains historical'}
    write(HERE/'게시후_검증.json',receipt)
    write(ROOT/P/'04_검증자료/01-A2_작은예비/후속검수_게시후_검증.json',receipt)
    print(json.dumps({'all_hashes_match':True,'files':len(files),'presented_human_reviews_pending':0,'A3_started':False},ensure_ascii=False))
if __name__=='__main__':main()
