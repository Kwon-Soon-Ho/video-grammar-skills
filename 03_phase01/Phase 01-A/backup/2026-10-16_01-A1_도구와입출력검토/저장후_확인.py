"""게시 파일을 다시 읽는 한정 검사. 원본 영상·Phase00 실행 도구 호출 없음."""
from pathlib import Path
from urllib.parse import unquote
import hashlib,json,re
W=Path(__file__).resolve().parent
P=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
M=json.loads((W/'게시명세.json').read_text(encoding='utf-8'))
B=P/'Phase 01-A/backup/2026-10-16_01-A1_도구와입출력검토'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
links=0
for x in M['targets']:
    p=P/x['relative'];assert sha(p)==x['after'],p
    if x['before']: assert sha(B/'변경전'/x['relative'])==x['before'],p
    t=p.read_text(encoding='utf-8')
    if p.suffix=='.json':json.loads(t)
    if p.suffix=='.md':
        for u in re.findall(r'\]\(([^)\n]+)\)',t):
            if re.match(r'https?://',u):continue
            assert (p.parent/unquote(u)).resolve().exists(),(p,u)
            links+=1
for s in M['protected_phase00']:assert sha(P/s['path'])==s['sha256']
for folder in ['02_분석작업','03_분석스킬','04_검증자료']:
    assert [f.name for f in (P/'Phase 01-A'/folder).rglob('*') if f.is_file()]==['00_예약폴더_안내.md']
for item in json.loads((W/'도구자료_확보목록.json').read_text(encoding='utf-8'))['files']:
    assert sha(B/'검토원본'/item['filename'])==item['sha256']
state=json.loads((P/'Phase 01-A/00_진행안내/01-A_계획상태.json').read_text(encoding='utf-8'))
assert state['approved'] and state['approved_choice']=='A' and not state['stage_A2_started']
assert state['actual_media_analysis_runs']==state['media_analysis_api_calls']==0
assert not state['skill_created'] and not state['default_skill_promotion']
out={'date':'2026-10-16','check':'저장 후 실제 파일 재읽기·해시·링크·백업 검사',
 'published_hash_matches':len(M['targets']),'previous_backups_match':sum(bool(x['before']) for x in M['targets']),
 'local_links_resolve':links,'phase00_references_unchanged':len(M['protected_phase00']),
 'public_archives_backup_hashes_match':2,'reserved_folders_unchanged':3,
 'A1_complete_A2_pending':True,'company_video_analysis_runs':0,
 'limitations':'문서·백업·참조 구조 검사. 내용 승인/영상 성능/전체 Phase00 재감사 아님'}
(W/'저장후_재읽기검증.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
