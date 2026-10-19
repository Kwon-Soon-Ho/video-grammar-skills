import pathlib,json,hashlib,re,os,shutil
from urllib.parse import quote,unquote
ROOT=pathlib.Path(__file__).resolve().parent;W=ROOT/'후속정리_20261016';ST=W/'게시안'
P=pathlib.Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증');D=P/'Phase 01-A'
M=json.loads((W/'게시명세.json').read_text('utf-8'));OLD=json.loads((ROOT.parent/'phase01a-prep/게시구성_명세.json').read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def ck(name,value):checks.append({'name':name,'passed':bool(value)});assert value,name
v=[v for c in M['cards'] for v in c['videos']]
originalv={x['path'] for x in OLD['source_before'] if x['extension']=='.mp4'}
ck('영상 41개 각각 정확히 한 묶음에 포함',len(v)==len(set(v))==41 and set(v)==originalv)
ck('프로젝트 23개 포함',len({c['id'] for c in M['cards']})==23)
for c in M['cards']:
    ck(c['id']+' 최종 승인·실제 일치·영상 열람으로 확대 안 함',not c['final_delivery_confirmed'] and not c['video_document_match_confirmed'] and not c['video_content_opened'])
    for rel in c['videos']+c['primary_documents']+c['reference_documents']:ck('원본 파일 존재', (P/rel).is_file())
for x in M['human_record']['documents']:ck('사용자 답변 대상 문서 버전 동일',sha(P/x['path'])==x['sha256'])
for rel in ['02_분석작업','03_분석스킬','04_검증자료']:ck('실제 작업 예약 폴더만 존재',sorted(x.name for x in (D/rel).rglob('*') if x.is_file())==['00_예약폴더_안내.md'])
for x in M['targets']:
    p=D/x['relative'];ck('대상 경로 제한',p.resolve().is_relative_to(D.resolve()));ck('동시 변경·신규 충돌 없음',sha(p)==x['before'] if x['before'] else not p.exists());ck('게시안 일치',sha(ST/x['relative'])==x['after'])
    if x['relative'].endswith('.md'):
        t=(ST/x['relative']).read_text('utf-8');ck('한글 문서 문자 정합성','\ufffd' not in t and not re.search(r'[\u3040-\u30ff]',t))
        for link in re.findall(r'\]\(([^)\n]+)\)',t):
            if '://' in link:continue
            p=((D/x['relative']).parent/unquote(link)).resolve()
            try:staged=ST/p.relative_to(D.resolve())
            except ValueError:staged=None
            ck('문서 링크 존재',p.exists() or (staged and staged.exists()))
for x in OLD['source_before']:
    p=P/x['path'];ck('원본 목록·크기·수정시각 보존',p.exists() and (p.stat().st_size,p.stat().st_mtime_ns)==(x['bytes'],x['mtime_ns']))
protected=json.loads((ROOT.parent/'phase00-build/시범운영_20261016/시범_입력과권한.json').read_text('utf-8'))['protected_D_files']
for rel,h in protected.items():ck('Phase 00 보호파일 보존',sha(P/'Phase 00'/rel)==h)
published=os.environ.get('DOC_REVIEW_PUBLISH')=='1'
if published:
    B=D/'backup/2026-10-16_기획서확인_쉬운정리';ck('백업 경로 신규',not B.exists());B.mkdir(parents=True)
    for x in M['targets']:
        if x['before']:
            b=B/'변경전'/x['relative'];b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(D/x['relative'],b);ck('변경 전 백업 일치',sha(b)==x['before'])
    for x in M['targets']:
        p=D/x['relative'];ck('저장 직전 동일',sha(p)==x['before'] if x['before'] else not p.exists());p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ST/x['relative']).read_bytes());ck('저장 후 일치',sha(p)==x['after'])
result={'date':'2026-10-16','mode':'published' if published else 'preflight','files':len(M['targets']),'previous_files':sum(bool(x['before']) for x in M['targets']),'groups':23,'video_candidates':41,'document_nature_confirmed':7,'human_record_id':M['human_record']['id'],'final_delivery_confirmed':False,'video_content_analyzed':False,'skill_development_started':False,'external_upload_performed':False,'checks':checks,'note':'검사는 자료 연결·버전·파일 보존·기록 범위 확인이다. 실제 영상의 내용 일치 검수가 아니다.'}
rp=W/('게시후_검증결과.json' if published else '게시전_검증결과.json');rp.write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
if published:
    audit=B/'처리기록';audit.mkdir();shutil.copy2(ROOT/'확인표_쉬운정리.py',audit/'확인표_쉬운정리.py');shutil.copy2(ROOT/'확인표_게시검증.py',audit/'확인표_게시검증.py');shutil.copy2(W/'게시명세.json',audit/'게시명세.json');shutil.copy2(rp,audit/rp.name)
    R=P/'작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_추천조합과_사용자답변';R.mkdir(exist_ok=False)
    for rel,name in [('05_결과보고/02_사용자답변과_추천조합_보완.md','01_후속정리_결과.md'),('00_진행안내/06_영상과기획서_추천조합.md','02_영상과기획서_추천조합.md')]:
        text=(D/rel).read_text('utf-8')
        def fix(mt):
            u=mt.group(1)
            if '://' in u:return mt.group(0)
            dest=((D/rel).parent/unquote(u)).resolve()
            return ']('+quote(os.path.relpath(dest,R).replace('\\','/'),safe='/._-')+')'
        (R/name).write_text(re.sub(r'\]\(([^)\n]+)\)',fix,text),'utf-8')
    shutil.copy2(D/'00_진행안내/07_재구성원고_사용자확인.json',R/'03_재구성원고_사용자확인.json');shutil.copy2(rp,R/'04_게시와범위_검증결과.json')
print(json.dumps({k:result[k] for k in ['mode','files','previous_files','groups','video_candidates','document_nature_confirmed']},ensure_ascii=False))
