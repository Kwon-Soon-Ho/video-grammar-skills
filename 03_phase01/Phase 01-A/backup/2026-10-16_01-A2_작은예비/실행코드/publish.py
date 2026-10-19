"""Publish only prepared A2 derivatives and the backed-up current status notice."""
from pathlib import Path
import json,shutil,sys,hashlib,re
from prepare import OUT,ROOT,sha,write
PUB=OUT/'게시안'
P='Phase 01-A';BK=f'{P}/backup/2026-10-16_01-A2_작은예비'
ALLOWED_DIRS=[f'{P}/02_분석작업/01-A2_작은예비/',f'{P}/04_검증자료/01-A2_작은예비/',f'{BK}/','작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A2/']
ALLOWED_FILES={f'{P}/00_진행안내/01-A_계획상태.json',f'{P}/00_진행안내/15_01-A2_실행결과_현재안내.json',f'{P}/05_결과보고/07_01-A2_작은예비분석_보고.md'}
def allowed(rel):return rel in ALLOWED_FILES or any(rel.startswith(x) for x in ALLOWED_DIRS)
def audit():
    # Include this exact publication script in the new archive.
    dest=PUB/BK/'실행코드/publish.py';dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(__file__,dest)
    manifest=[];links=[]
    for src in sorted(PUB.rglob('*')):
        if not src.is_file():continue
        rel=src.relative_to(PUB).as_posix()
        if not allowed(rel):raise ValueError('unexpected_destination:'+rel)
        if src.suffix=='.json':json.loads(src.read_text(encoding='utf-8-sig'))
        if src.suffix=='.md' and '/중간본과_실패/' not in rel:
            for ref in re.findall(r'\]\(([^)]+)\)',src.read_text(encoding='utf-8')):
                if not ref.startswith(('http:','https:','C:','D:')):
                    target=(src.parent/ref).resolve()
                    if not target.is_file():raise ValueError('broken_staged_link:'+ref)
                    links.append({'source':rel,'ref':ref})
        manifest.append({'relative_path':rel,'sha256':sha(src),'bytes':src.stat().st_size})
    old=PUB/BK/'변경전_안내/01-A_계획상태.json'
    conflicts=[]
    for m in manifest:
        dst=(ROOT/m['relative_path']).resolve()
        if not dst.is_relative_to(ROOT.resolve()):raise ValueError('destination_escape')
        if dst.exists() and sha(dst)!=m['sha256']:
            if m['relative_path']!=f'{P}/00_진행안내/01-A_계획상태.json' or sha(dst)!=sha(old):conflicts.append(m['relative_path'])
    if conflicts:raise ValueError('unexpected_existing_differences:'+repr(conflicts))
    write(OUT/'게시명세.json',manifest)
    result={'files':len(manifest),'bytes':sum(m['bytes'] for m in manifest),'links_checked':len(links),'unexpected_conflicts':conflicts,'sources_unchanged_verified_in':'원본과_기준핀_재확인.json'}
    write(OUT/'게시전_검증.json',result);return manifest,result
def main():
    manifest,result=audit()
    if '--publish' not in sys.argv:print(json.dumps(result,ensure_ascii=False));return
    written=0
    for m in manifest:
        src=PUB/m['relative_path'];dst=ROOT/m['relative_path']
        if dst.exists() and sha(dst)==m['sha256']:continue
        dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);written+=1
        if sha(dst)!=m['sha256']:raise ValueError('copy_hash_mismatch:'+m['relative_path'])
    verification=[{'path':m['relative_path'],'matches':sha(ROOT/m['relative_path'])==m['sha256']} for m in manifest]
    if not all(x['matches'] for x in verification):raise ValueError('publication_verification_failed')
    receipt={'all_hashes_match':True,'written':written,'files':len(manifest),'bytes':sum(m['bytes'] for m in manifest),'manifest_sha256':sha(OUT/'게시명세.json'),'checks':verification,'scope':'copy integrity only; no new content approval'}
    write(OUT/'게시후_검증.json',receipt)
    write(ROOT/P/'04_검증자료/01-A2_작은예비/게시후_해시검증.json',receipt)
    print(json.dumps({'all_hashes_match':True,'files':len(manifest),'written':written,'report':str(ROOT/P/'05_결과보고/07_01-A2_작은예비분석_보고.md')},ensure_ascii=False))
if __name__=='__main__':main()
