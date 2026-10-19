from pathlib import Path
from urllib.parse import unquote
import json,csv,io,re,hashlib,sys,os

W=Path(__file__).parent.resolve();CWD=W.parent
P=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
SRC=P/'한맥 영상';DEST=P/'Phase 01-A';STAGE=W/'게시본'
M=json.loads((W/'게시구성_명세.json').read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def js(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def ext(p):
    s=str(p.resolve());return Path(s if s.startswith('\\\\?\\') else '\\\\?\\'+s)
def new(p,b):
    p=ext(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
def source_snapshot():
    result=[]
    for p in sorted(SRC.rglob('*'),key=lambda p:p.relative_to(SRC).as_posix().casefold()):
        if p.is_file():
            s=p.stat();r=p.relative_to(SRC)
            result.append({'path':p.relative_to(P).as_posix(),'relative':r.as_posix(),'extension':p.suffix.lower(),'bytes':s.st_size,'mtime_ns':s.st_mtime_ns,'backup':any(t.casefold() in {'backup','백업'} for t in r.parts[:-1])})
    return result
def protect():
    pins=json.loads((CWD/'phase00-build/시범운영_20261016/시범_입력과권한.json').read_text(encoding='utf-8'))['protected_D_files']
    assert all(sha(P/'Phase 00'/r)==h for r,h in pins.items())
    return len(pins)
def validate():
    assert source_snapshot()==M['source_before']
    assert {p.relative_to(STAGE).as_posix() for p in STAGE.rglob('*') if p.is_file()}==set(M['files'])
    assert all(sha(STAGE/r)==h for r,h in M['files'].items())
    allvid=[];refs=[]
    for r in M['registry']:
        d=STAGE/r['folder']
        ref=json.loads((d/'02_자료참조.json').read_text(encoding='utf-8'));refs.append(ref)
        assert ref['id']==r['id'] and ref['registration_snapshot'] is True
        assert ref['selected_video'] is None and ref['selected_documents'] is None
        assert ref['analysis_started'] is False and ref['external_ai_permission']=='needs_confirmation'
        for k in ['video_candidates','document_candidates','other_candidates','ancestor_candidates','shared_folders']:
            assert all((P/v).exists() for v in ref[k])
        allvid+=ref['video_candidates']
        text=(d/'00_자료설명.md').read_text(encoding='utf-8')
        assert '自动' not in text and '먼저 적을 여섯 가지' in text
        assert f"프로젝트명 / 자료 ID: {r['source_folder']} / {r['id']}" in text
    assert len(allvid)==len(set(allvid))==M['stats']['video_candidates']
    all_actual={i['path'] for i in M['source_before'] if i['extension']=='.mp4'}
    assert set(allvid)==all_actual
    csvs={}
    for p in STAGE.rglob('*.csv'):
        rows=list(csv.reader(io.StringIO(p.read_text(encoding='utf-8-sig'))))
        assert rows and all(len(r)==len(rows[0]) for r in rows),p
        csvs[p.relative_to(STAGE).as_posix()]=len(rows)-1
    assert csvs['00_진행안내/03_기존자료_파일목록.csv']==M['stats']['source_files']
    assert csvs['01_입력자료/00_기존자료_등록목록.csv']==len(M['registry'])
    link_count=0
    for p in STAGE.rglob('*.md'):
        for url in re.findall(r'\[[^\n]*?\]\(([^ \n]+)\)',p.read_text(encoding='utf-8')):
            assert not url.startswith(('http:','https:'))
            target=((DEST/p.relative_to(STAGE)).parent/unquote(url)).resolve()
            if target.is_relative_to(DEST):
                rel=target.relative_to(DEST).as_posix()
                assert rel in M['files'] or rel in M['empty_folders'],(p,url,rel)
            else:assert target.is_relative_to(SRC) and target.exists(),(p,url)
            link_count+=1
    assert link_count>=len(M['links'])
    for folder in ['02_분석작업','03_분석스킬','04_검증자료']:
        assert [p.name for p in (STAGE/folder).iterdir()]==['00_예약폴더_안내.md']
    assert not list(STAGE.rglob('SKILL.md')) and not list(STAGE.rglob('*.mp4'))
    return {'link_count':link_count,'registered_groups':len(refs),'registered_video_candidates':len(allvid),'source_file_count':len(M['source_before']),'generated_file_count':len(M['files']),'csv_rows':csvs,'phase00_protected_files':protect(),'source_metadata_unchanged':True,'source_content_hashes_not_computed':True,'final_or_scenario_pair_not_assumed':True,'snapshots_distinct_from_editable_human_description':True,'analysis_started':False,'skill_development_started':False,'external_upload_performed':False,'review_method':'root self consistency and adversarial-scenario review; no new independent agent review'}

if '--publish' not in sys.argv:
    qa=validate()
    issues=[
      {'risk':'같은 폴더·최종·v4만 보고 최종본/문서 대응을 확정','resolution':'모두 후보·미확인으로 등록. 실제 선택 필드는 자료 설명에서 사람이 기입한다.'},
      {'risk':'기획 PNG를 문서 없음으로 오해','resolution':'이미지·기타 후보를 별도 표시하고 기획서로 지정할 수 있도록 안내했다.'},
      {'risk':'자동 목록과 사람 기입의 값이 뒤섞임','resolution':'CSV·JSON은 최초등록 스냅샷. 최신 사람 기입은 자료 설명을 읽고 실제 착수 전에 재대조한다.'},
      {'risk':'파일명의 괄호·대괄호로 원본 링크가 깨짐','resolution':'URL 특수문자를 인코딩하고 생성된 실제 Markdown 링크를 역변환하여 전체 참조 경로를 확인했다.'},
      {'risk':'대용량 영상의 불필요한 중복 복사','resolution':'약 26.58GB의 영상 원본은 그대로 두고 경로만 등록했다.'},
      {'risk':'준비 작업이 분석·스킬 개발 착수로 해석','resolution':'분석/스킬/검증 폴더는 예약 안내만 넣고 작업·표본 배정·외부 업로드는 실행하지 않았다.'}]
    qa['issues_and_resolutions']=issues
    new(W/'준비_검토기록.json',js(qa))
    report=f'''# Phase 01-A 자료 준비 결과

2026-10-16. 폴더 구조·자료 설명 양식·기존 자료의 위치 등록만 완료했다. 실제 영상/문서 내용 분석, OCR·전사·프레임 추출·미디어 정보 조회, 스킬 개발·외부 업로드는 하지 않았다.

## 등록한 범위

- 원본 파일 {qa['source_file_count']}개, 영상 후보 {qa['registered_video_candidates']}개, 영상이 든 폴더 {qa['registered_groups']}묶음.
- 이름·폴더·확장자·크기·수정 시각만 목록으로 확인. 영상이나 기획서의 내용은 열지 않았다.
- 같은 폴더의 문서·이미지와 가까운 상위/공유 자료를 후보 경로로만 연결했다.
- 최종 영상, 맞는 시나리오, 최초 분석 대상, 보정/잠금 표본은 미정이다.

## 사용할 파일

먼저 00_먼저읽기.md와 01_입력자료/00_기존자료_등록목록.md를 본다. 각 자료의 00_자료설명.md에서 여섯 항목만 작성한다. CSV·JSON은 자동 목록 스냅샷이며 사용자가 직접 고칠 필요는 없다.

기존 파일은 한맥 영상에 그대로 둔다. 새 프로젝트는 00_진행안내/준비양식/신규영상_폴더양식을 복사해 01_입력자료/02_새자료_접수에 넣는다. 원래 이름·PPT/Word/한글/PDF/Excel/이미지 형식을 유지한다.

## 자체 반대 관점 점검과 보완

최종·버전명만으로 문서 대응을 확정하지 않도록 했다. 기획 이미지를 누락하지 않도록 이미지 후보를 표시했다. 자동 목록과 사람이 입력할 최신 설명을 구분했다. 파일명 특수문자를 인코딩하고 실제 Markdown 링크 {qa['link_count']}개를 경로로 대조했다.

새 독립 에이전트 레드팀을 수행한 보고가 아니라 이번 준비 문서의 자체 구조·참조·예외 점검이다. 모든 단계에 대한 성능 검증이나 사람 내용 승인으로 확대하지 않는다.

## 보존과 경계

원본 파일 목록·크기·수정 시각은 준비 전후 같았다. 원본 파일의 내용 해시를 계산하거나 원본을 복사·이동·이름 변경하지 않았다. Phase 00의 기존 보호 파일 {qa['phase00_protected_files']}개도 SHA 대조에서 보존됐다. 기존 세 후보의 기본 전환 보류·소량 사본 사용 유지 결정은 그대로다.

실제 분석·스킬 개발 착수는 사용자의 별도 후속 지시를 기다린다.
'''
    new(W/'자료준비_결과.md',report.encode('utf-8'))
    print(json.dumps({k:qa[k] for k in ['registered_groups','registered_video_candidates','source_file_count','link_count','analysis_started','skill_development_started']},ensure_ascii=False))
else:
    qa=validate();old=json.loads((W/'준비_검토기록.json').read_text(encoding='utf-8'))
    assert all(old[k]==v for k,v in qa.items())
    assert not DEST.exists(),'Existing Phase 01-A requires review before merging'
    review=P/'작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_자료준비'
    pairs=[(STAGE/rel,DEST/rel,h) for rel,h in M['files'].items()]
    pairs.extend([(W/'자료준비_결과.md',DEST/'05_결과보고/00_자료준비_결과.md',sha(W/'자료준비_결과.md')),(W/'자료준비_결과.md',review/'00_준비검토기록.md',sha(W/'자료준비_결과.md')),(W/'준비_검토기록.json',review/'00_준비검토기록.json',sha(W/'준비_검토기록.json'))])
    for p in W.rglob('*'):
        if p.is_file():pairs.append((p,DEST/'backup/2026-10-16_자료준비'/p.relative_to(W),sha(p)))
    completed=[W/'저장_완료기록.json',DEST/'00_진행안내/자료준비_저장기록.json',review/'저장_완료기록.json']
    targets=[q for p,q,h in pairs]+completed
    assert len({str(q.resolve()).casefold() for q in targets})==len(targets)
    assert all(not ext(q).exists() for q in targets)
    for rel in M['empty_folders']:ext(DEST/rel).mkdir(parents=True,exist_ok=False)
    for p,q,h in pairs:
        assert sha(p)==h
        new(q,p.read_bytes());assert sha(ext(q))==h
    assert all(sha(p)==h and sha(ext(q))==h for p,q,h in pairs)
    assert source_snapshot()==M['source_before'];protect()
    done={'complete':True,'date':'2026-10-16','preparation_only':True,'root':str(DEST),'source_file_count':qa['source_file_count'],'video_candidates':qa['registered_video_candidates'],'registered_groups':qa['registered_groups'],'links_checked':qa['link_count'],'copied_files':len(pairs),'copies':[{'source':str(p),'destination':str(q),'sha256':h} for p,q,h in pairs],'original_media_or_document_files_copied':0,'original_metadata_preserved':True,'analysis_started':False,'skill_development_started':False,'external_upload_performed':False}
    for q in completed:new(q,js(done))
    print(json.dumps({k:v for k,v in done.items() if k!='copies'},ensure_ascii=False))
