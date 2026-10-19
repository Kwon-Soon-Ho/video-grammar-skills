import pathlib,json,hashlib,shutil,re,datetime,os
from urllib.parse import unquote
W=pathlib.Path(__file__).resolve().parent
P=pathlib.Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
D=P/'Phase 01-A';ST=W/'게시안'
MODE=os.environ.get('DOC_REVIEW_PUBLISH')=='1'
m=json.loads((W/'게시명세.json').read_text('utf-8'))
orig=json.loads((W.parent/'phase01a-prep/게시구성_명세.json').read_text('utf-8'))
idx=json.loads((W/'문서목록과_읽기결과.json').read_text('utf-8'))
def sha_file(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
checks=[]
def check(name,cond,detail=None):
    checks.append({'check':name,'passed':bool(cond),'detail':detail})
    assert cond,(name,detail)
for x in m['targets']:
    rel=x['relative'];target=D/rel
    check('게시 경로 제한',target.resolve().is_relative_to(D.resolve()),rel)
    check('원본 변경 없음/신규 충돌 없음',sha_file(target)==x['expected_before'] if x['expected_before'] else not target.exists(),rel)
    check('게시안 해시 일치',sha_file(ST/rel)==x['after'],rel)
# Read only planning file bytes. MP4 files are inspected with stat only.
sourcechecks=[]
for x in idx['documents']+idx['images']:
    h=sha_file(P/x['path']);check('기획 원본 해시 보존',h==x['sha256'],x['path']);sourcechecks.append({'path':x['path'],'sha256':h})
source_now=[]
for x in sorted((P/'한맥 영상').rglob('*')):
    if x.is_file():source_now.append({'path':x.relative_to(P).as_posix(),'bytes':x.stat().st_size,'mtime_ns':x.stat().st_mtime_ns})
initial={x['path']:(x['bytes'],x['mtime_ns']) for x in orig['source_before']}
now={x['path']:(x['bytes'],x['mtime_ns']) for x in source_now}
check('전체 원본 목록·크기·수정시각 보존',now==initial,{'files':len(now),'video_count':sum(k.lower().endswith('.mp4') for k in now)})
evidence_count=0
for r in m['records']:
    for f in r['facts']:
        check('모든 기록에 근거 있음',bool(f['evidence']),r['id'])
        for e in f['evidence']:
            if e['document_id'].startswith('DOC'):
                doc=json.loads((W/'본문'/f"{e['document_id']}.json").read_text('utf-8'))
                check('원문 위치/인용 일치',any(c['loc']==e['locator'] and c['text']==e['quote'] and e['match'] in c['text'] for c in doc['chunks']),r['id']+' '+e['document_id']+' '+e['locator'])
            else:check('이미지 관측 한계 명시','visual' in e['verification'] and '미검토' in r['scope'],r['id'])
            evidence_count+=1
    check('자동 최종본·대응 승인 없음',not r['final_video_confirmed'] and not r['scenario_pair_confirmed'] and not r['video_analysis_started'],r['id'])
    text=(ST/next(x['relative'] for x in m['targets'] if x['relative'].endswith('00_자료설명.md') and '/'+r['id']+'_' in x['relative'])).read_text('utf-8')
    check('담당자·API 권한 미정 유지','5. 디자인 확인 담당 / 내용 확인 담당: 미정' in text and '6. 외부 AI·API 처리 범위: 확인 필요' in text,r['id'])
linkcount=0
for x in m['targets']:
    if not x['relative'].endswith('.md'):continue
    src=ST/x['relative'];t=src.read_text('utf-8')
    check('문자 깨짐 없음','\ufffd' not in t and not re.search(r'[\u3040-\u30ff]',t),x['relative'])
    for url in re.findall(r'\]\(([^)\n]+)\)',t):
        if '://' in url:continue
        p=(D/x['relative']).parent/unquote(url.split('#')[0]);resolved=p.resolve()
        try:staged=ST/resolved.relative_to(D.resolve())
        except ValueError:staged=None
        check('문서 링크 연결',resolved.exists() or (staged and staged.exists()),{'from':x['relative'],'target':url});linkcount+=1
for sub in ['02_분석작업','03_분석스킬','04_검증자료']:
    files=[p.name for p in (D/sub).rglob('*') if p.is_file()]
    check('분석·스킬·평가 예약 폴더 보존',files==['00_예약폴더_안내.md'],sub)
protected=json.loads((W.parent/'phase00-build/시범운영_20261016/시범_입력과권한.json').read_text('utf-8'))['protected_D_files']
for rel,h in protected.items():check('Phase 00 보호 파일 보존',sha_file(P/'Phase 00'/rel)==h,rel)
# Anything outside explicitly listed current files must remain unchanged after publish.
unchanged={p.relative_to(D).as_posix():sha_file(p) for p in D.rglob('*') if p.is_file() and 'backup' not in p.relative_to(D).parts and p.relative_to(D).as_posix() not in {x['relative'] for x in m['targets']}}
summary={'date':'2026-10-16','mode':'publish' if MODE else 'preflight','checks':checks,'planning_source_hashes':sourcechecks,'passed_checks':len(checks),'evidence_locator_checks':evidence_count,'local_links_checked':linkcount,'video_file_content_opened':False,'source_upload_performed':False,'independent_reviewer_used':False}
(W/'게시전_검증결과.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),'utf-8')
if not MODE:print(json.dumps({k:summary[k] for k in ['mode','passed_checks','evidence_locator_checks','local_links_checked']},ensure_ascii=False));raise SystemExit
B=D/'backup/2026-10-16_기획서검토'
check('백업 폴더 신규',not B.exists(),str(B));B.mkdir(parents=True)
for x in m['targets']:
    p=D/x['relative']
    if x['expected_before']:
        old=B/'변경전'/x['relative'];old.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,old)
        check('변경 전 백업 해시',sha_file(old)==x['expected_before'],x['relative'])
# All preconditions checked again immediately before each individual write.
written=[]
for x in m['targets']:
    p=D/x['relative'];check('저장 직전 동시 수정 점검',sha_file(p)==x['expected_before'] if x['expected_before'] else not p.exists(),x['relative'])
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ST/x['relative']).read_bytes());written.append(x['relative'])
for x in m['targets']:check('저장 후 해시 일치',sha_file(D/x['relative'])==x['after'],x['relative'])
for rel,h in unchanged.items():check('대상 외 기존 파일 보존',sha_file(D/rel)==h,rel)
for rel,h in protected.items():check('저장 후 Phase 00 보존',sha_file(P/'Phase 00'/rel)==h,rel)
summary.update({'checks':checks,'mode':'published','passed_checks':len(checks),'written_files':written,'previous_files_backed_up':sum(bool(x['expected_before']) for x in m['targets']),'unchanged_existing_files_checked':len(unchanged)})
(W/'최종_검증결과.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),'utf-8')
# Local audit copy; source files and 26 GB videos are not duplicated.
for name in ['기획서_본문읽기.py','이미지_읽기준비.py','자료설명_보완안.py','게시와검증.py','문서목록과_읽기결과.json','기록항목과_근거.json','게시명세.json','게시전_검증결과.json','최종_검증결과.json']:
    dst=B/'처리와검토기록'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/name,dst)
for directory in ['본문','이미지확인','의존성_원본']:shutil.copytree(W/directory,B/'처리와검토기록'/directory)
R=P/'작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_기획서검토';R.mkdir(parents=True,exist_ok=False)
for rel,name in [('05_결과보고/01_기획서검토와_자료설명_보완.md','01_작업결과.md'),('00_진행안내/04_사용자확인_모음.md','02_사용자확인_모음.md')]:
    # Archive is a snapshot. Keep local links correct for its different parent.
    content=(D/rel).read_text('utf-8')
    def fix(match):
        raw=match.group(1)
        if '://' in raw:return match.group(0)
        from urllib.parse import quote
        absolute=((D/rel).parent/unquote(raw)).resolve()
        return ']('+quote(os.path.relpath(absolute,R).replace('\\','/'),safe='/._-')+')'
    (R/name).write_text(re.sub(r'\]\(([^)\n]+)\)',fix,content),'utf-8')
shutil.copy2(W/'최종_검증결과.json',R/'03_원본과범위_검증결과.json')
(R/'00_읽는순서.md').write_text('# 기획서 검토 기록\n\n2026-10-16의 사전 검토 기록이다. PDF 추가 제출 요청이 없어 이번에는 문서·JSON으로 남겼다.\n\n1. 01_작업결과.md\n2. 02_사용자확인_모음.md\n3. 03_원본과범위_검증결과.json\n\n추출 본문·정지 이미지 미리보기·도구 버전과 라이선스·변경 전 원문은 Phase 01-A/backup/2026-10-16_기획서검토에 보관한다. 원본/추출문은 동일한 사내 자료로 취급한다.\n','utf-8')
print(json.dumps({k:summary[k] for k in ['mode','passed_checks','evidence_locator_checks','local_links_checked','previous_files_backed_up','unchanged_existing_files_checked']},ensure_ascii=False))
