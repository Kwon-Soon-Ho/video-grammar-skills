from pathlib import Path
import sys, os, json, hashlib, subprocess, re, difflib, traceback
from datetime import datetime, timezone
RUN=Path(__file__).resolve().parents[1]
BASE=RUN/'inputs'/'Phase00'
OUT=RUN/'outputs'
LOG=RUN/'transcript.md'
A='12_통합기록/통합기록_작업초안.json'
B='작업초안/디자인적용_초안.json'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def emit(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def log(s):
    with LOG.open('a',encoding='utf-8') as f:f.write(s+'\n')
def strict(raw):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d:raise ValueError('duplicate key '+k)
            d[k]=v
        return d
    return json.loads(raw.decode('utf-8-sig'),object_pairs_hook=pairs,parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
def changes(a,b,p=''):
    if type(a)!=type(b):return [{'path':p,'before':a,'after':b}]
    if isinstance(a,dict):
        assert set(a)==set(b),'key shape changed'
        return [x for k in a for x in changes(a[k],b[k],p+'/'+k)]
    if isinstance(a,list):
        assert len(a)==len(b),'array shape changed'
        return [x for i in range(len(a)) for x in changes(a[i],b[i],p+'/'+str(i))]
    return [] if a==b else [{'path':p,'before':a,'after':b}]
def check(stage,name,tool,rel,args):
    cmd=[sys.executable,'-B','-X','utf8',str(BASE/'07_실행도구'/tool),*args,str(BASE/rel)]
    env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1')
    r=subprocess.run(cmd,cwd=BASE,capture_output=True,text=True,encoding='utf-8',env=env)
    (OUT/f'{stage}_{name}.stdout.txt').write_text(r.stdout,encoding='utf-8')
    (OUT/f'{stage}_{name}.stderr.txt').write_text(r.stderr,encoding='utf-8')
    try:result=json.loads(r.stdout)
    except Exception:result={'valid':False,'errors':['검사 JSON 미반환; 원시 출력 참조']}
    entry={'command':cmd,'exit_code':r.returncode,'stdout_file':str(OUT/f'{stage}_{name}.stdout.txt'),'stderr_file':str(OUT/f'{stage}_{name}.stderr.txt'),'result':result}
    emit(f'{stage}_{name}_검사.json',entry)
    log('명령: `'+subprocess.list2cmdline(cmd)+'`\n종료코드: '+str(r.returncode)+'\n원시 stdout/stderr: outputs/'+stage+'_'+name+'.stdout.txt / .stderr.txt\n결과: '+json.dumps(result,ensure_ascii=False))
    return entry
log('# 실제 수행 기록\n\n시작: '+datetime.now(timezone.utc).isoformat()+'\n허용 범위: own task.txt, own inputs/Phase00; 쓰기는 지정 두 초안, backup, outputs, transcript.md. 외부 DB/웹/API/AE/CU 접근 없음. Python -B -X utf8 사용.\n읽은 스킬: inputs/Phase00/실행스킬/video-record-steward/SKILL.md 및 references/작업기준.md. 수행사본_범위.json의 R6/R7 축소 범위를 적용.\n사전 도구 탐색 실패: 디자인적용_검사.py 읽기 종료코드 1(파일 없음). rg로 실제 R5_디자인적용검사.py를 찾아 복구. PowerShell 프로필은 InitializeDefaultDrives 경고를 출력했으나 파일 읽기 성공. 이후 Python으로 검사 수행.\n')
try:
    before={}
    for p in BASE.rglob('*'):
        if p.is_file():
            assert p.resolve().is_relative_to(BASE.resolve()),str(p)
            before[p.relative_to(BASE).as_posix()]=sha(p.read_bytes())
    emit('입력_변경전_해시.json',before)
    raws={r:(BASE/r).read_bytes() for r in [A,B]}
    originals={r:strict(raw) for r,raw in raws.items()}
    target=[x for x in originals[A]['spatial_contract']['evidence_contract']['targets'] if x['id']=='TG-STATE']
    units=[(i,x) for i,x in enumerate(originals[A]['units']) if x['target_ref']['id']=='TG-STATE']
    assert len(target)==len(units)==1
    idx,unit=units[0]
    assert unit['target_ref']['version']=='0.9.9' and target[0]['version']=='0.1.0'
    assert originals[A]['version']=='0.1.0'
    oldlink=originals[B]['linked_r4_record']
    assert oldlink['path']==A and oldlink['record_id']==originals[A]['record_id']
    backup=RUN/'backup'/'2026-10-15_TG-STATE参照修正'
    for rel in [A,B]:
        bp=backup/rel
        bp.parent.mkdir(parents=True,exist_ok=True)
        with bp.open('xb') as f:f.write(raws[rel])
        assert bp.read_bytes()==raws[rel]
    emit('backup_검증.json',[{'source':str(BASE/r),'backup':str(backup/r),'sha256':sha(raws[r]),'byte_identical':True} for r in [A,B]])
    log('변경 전 사본 저장 및 바이트/SHA256 동일 확인: '+str(backup))
    preA=check('변경전','통합기록','자료검증.py',A,['--record'])
    preB=check('변경전','디자인적용','R5_디자인적용검사.py',B,[])
    raw=raws[A]
    raw,n=re.subn(rb'(?m)^(  "version": ")0\.1\.0(",\r?$)',rb'\g<1>0.1.1\2',raw)
    assert n==1
    raw,n=re.subn(rb'("id": "TG-STATE",\s+"version": ")0\.9\.9(")',rb'\g<1>0.1.0\2',raw)
    assert n==1
    da=changes(originals[A],strict(raw))
    assert {x['path'] for x in da}=={'/version',f'/units/{idx}/target_ref/version'}
    assert (BASE/A).read_bytes()==raws[A]
    (BASE/A).write_bytes(raw)
    anew=(BASE/A).read_bytes();anewdata=strict(anew);newhash=sha(anew)
    rb=raws[B]
    start=rb.index(b'  "linked_r4_record": {')
    end=rb.index(b'\n  }',start)+4
    fragment=rb[start:end]
    fragment,n=re.subn(rb'("version": ")0\.1\.0(")',rb'\g<1>0.1.1\2',fragment);assert n==1
    fragment,n=re.subn(rb'("sha256": ")[a-f0-9]{64}(")',lambda m:m[1]+newhash.encode()+m[2],fragment);assert n==1
    bnew=rb[:start]+fragment+rb[end:]
    db=changes(originals[B],strict(bnew))
    assert {x['path'] for x in db}=={'/linked_r4_record/version','/linked_r4_record/sha256'}
    assert (BASE/B).read_bytes()==raws[B]
    (BASE/B).write_bytes(bnew)
    assert (BASE/A).read_bytes()==anew and (BASE/B).read_bytes()==bnew
    newlink=strict(bnew)['linked_r4_record']
    assert newlink['version']==anewdata['version'] and newlink['record_id']==anewdata['record_id'] and newlink['sha256']==sha((BASE/A).read_bytes())
    emit('변경차이.json',{'integrated_record':da,'design_application':db})
    for label,rel in [('통합기록',A),('디자인적용',B)]:
        diff=''.join(difflib.unified_diff(raws[rel].decode('utf-8-sig').splitlines(True),(BASE/rel).read_bytes().decode('utf-8-sig').splitlines(True),fromfile='backup/'+rel,tofile='inputs/Phase00/'+rel))
        (OUT/f'{label}.diff').write_text(diff,encoding='utf-8')
    log('실제 반영: '+json.dumps({'통합기록':da,'디자인적용':db},ensure_ascii=False)+'\n통합기록 실제 저장 파일 SHA256: '+newhash+'\n디자인 초안 자체 version은 요청 범위에 따라 보존. ID/경로 동일.')
    postA=check('변경후','통합기록','자료검증.py',A,['--record'])
    postB=check('변경후','디자인적용','R5_디자인적용검사.py',B,[])
    after={p.relative_to(BASE).as_posix():sha(p.read_bytes()) for p in BASE.rglob('*') if p.is_file()}
    assert set(before)==set(after)
    modified=[p for p in before if before[p]!=after[p]]
    assert set(modified)=={A,B},modified
    checks={'only_two_requested_files_changed':True,'other_inputs_byte_preserved':True,'backup_byte_identical':True,'logical_ids_preserved':True,'new_record_version':'0.1.1','TG_STATE_reference_matches_target':True,'design_link_matches_saved_bytes':True,'semantic_diff_allowlist_pass':True,'integrated_schema_and_semantic_valid':postA['result']['valid'],'design_schema_and_reference_valid':postB['result']['valid']}
    emit('입력_변경후_해시.json',after)
    result={'status':'completed' if postA['result']['valid'] and postB['result']['valid'] else 'edited_with_validation_limitations','scope':'합성 사본의 요청된 두 초안 참조/판본 정리. R6/R7 full 검증·실영상·회사 승인·운영 반영 아님.','modified_files':[str(BASE/r) for r in modified],'backup_dir':str(backup),'saved_integrated_sha256':newhash,'checks':checks,'before':{'integrated':preA['result'],'design':preB['result']},'after':{'integrated':postA['result'],'design':postB['result']},'company_approved':False,'operational_release':False,'human_questions_sent':False,'remaining_review':'기존 unknown/not_assessed/pending 및 검사기의 사람 검수 대기를 그대로 보존. 추가 의미/승인 결정은 수행하지 않음.'}
    emit('결과.json',result)
    explanation='두 초안에 실제 반영했습니다. TG-STATE 단위 참조 0.9.9 → 대상 판본 0.1.0, 통합기록 자체 판본 0.1.0 → 0.1.1로 수정했습니다. 디자인 초안의 연결 판본과 실제 저장 SHA256만 갱신했습니다. 변경 전 사본과 JSON/텍스트 차이, 전후 개별 검사 원시 출력·종료코드를 보존했습니다.\n검사: 통합기록 '+str(postA['result']['valid'])+', 디자인적용 '+str(postB['result']['valid'])+'.\n시간·좌표·수치·회사/색·검수 상태와 다른 입력 파일의 바이트 보존을 확인했습니다. 검사 통과는 합성 구조/참조 범위이며 실제 영상·회사 승인 및 R6/R7 전체 검증이 아닙니다.\n'
    (OUT/'설명.txt').write_text(explanation,encoding='utf-8')
    log('최종 보존 검사: '+json.dumps(checks,ensure_ascii=False)+'\n실패/복구: 사전 잘못된 도구명 탐색 외 쓰기/검사 중단 없음. 검사 한계와 미정은 결과.json에 보존. 완료: '+datetime.now(timezone.utc).isoformat())
    print(json.dumps({'status':result['status'],'checks':checks,'result_path':str(OUT/'결과.json')},ensure_ascii=False))
except Exception:
    detail=traceback.format_exc();log('실패: '+detail)
    emit('실패.json',{'status':'failed','traceback':detail,'note':'완료로 보고하지 않음. 부분 저장 여부와 backup 확인 필요.'})
    print(detail,file=sys.stderr)
    raise
