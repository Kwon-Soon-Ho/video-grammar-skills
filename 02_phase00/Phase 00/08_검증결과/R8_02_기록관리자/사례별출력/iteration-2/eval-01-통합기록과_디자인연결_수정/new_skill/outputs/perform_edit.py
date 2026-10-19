from pathlib import Path
import sys, json, hashlib, re, subprocess, difflib, traceback, os, stat
RUN=Path(__file__).resolve().parents[1]
BASE=RUN/'inputs/Phase00'
OUT=RUN/'outputs'
BACK=RUN/'backup/steward-edit-01'
P4=BASE/'12_통합기록/통합기록_작업초안.json'
P5=BASE/'작업초안/디자인적용_초안.json'
log=[]; commands=[]; written={}; snapshots={}; failure=None
report={'status':'started','scope':'합성 사본의 요청된 두 초안 참조·자체 판본 수정. 실제 분석/디자인/회사 승인 아님.','root':str(BASE),'time':None,'tokens':None,'commands':commands}
def sha(b):return hashlib.sha256(b).hexdigest()
def emit(name,value):
    p=OUT/name
    raw=(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8') if not isinstance(value,str) else value.encode('utf-8')
    with p.open('xb') as f:f.write(raw)
def note(s):log.append(s)
def boundary(p):
    assert p.resolve().is_relative_to(RUN),str(p)
    for q in [p,*p.parents]:
        if q==RUN.parent:break
        if q.exists():assert not q.is_symlink() and not bool(q.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT),str(q)
def strict(raw):
    def pairs(xs):
        d={}
        for k,v in xs:
            if k in d:raise ValueError('duplicate key '+k)
            d[k]=v
        return d
    def reject(x):raise ValueError('nonfinite '+x)
    return json.loads(raw.decode('utf-8-sig'),object_pairs_hook=pairs,parse_constant=reject)
def changes(a,b,path=''):
    if type(a)!=type(b):return [{'path':path,'before':a,'after':b,'type_changed':True}]
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        return [v for k in a for v in changes(a[k],b[k],path+'/'+k)]
    if isinstance(a,list):
        assert len(a)==len(b)
        return [v for i in range(len(a)) for v in changes(a[i],b[i],path+'/'+str(i))]
    return [] if a==b else [{'path':path,'before':a,'after':b}]
def cli(label,args):
    cmd=[sys.executable,'-B','-X','utf8',*map(str,args)]
    cp=subprocess.run(cmd,cwd=BASE,capture_output=True,text=True,encoding='utf-8')
    emit(label+'.stdout.txt',cp.stdout);emit(label+'.stderr.txt',cp.stderr)
    parsed=None
    try:parsed=json.loads(cp.stdout)
    except ValueError:pass
    row={'label':label,'argv':cmd,'cwd':str(BASE),'exit_code':cp.returncode,'stdout_path':str(OUT/(label+'.stdout.txt')),'stderr_path':str(OUT/(label+'.stderr.txt')),'result':parsed}
    commands.append(row);note(label+': exit '+str(cp.returncode))
    return row
def ok(row):assert row['exit_code']==0 and row['result']['valid'],row

def atomic_target(p,raw,expect):
    assert p.read_bytes()==expect,'external change '+str(p)
    temp=p.with_name(p.name+'.steward-edit-01.tmp');boundary(temp)
    with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert p.read_bytes()==expect,'external change before replacement'
    os.replace(temp,p);written[p]=raw
    assert p.read_bytes()==raw
    note('저장: '+str(p)+' SHA256='+sha(raw))

try:
    for p in [BASE,OUT,BACK,P4,P5]:boundary(p)
    original_hashes={}
    for p in BASE.rglob('*'):
        boundary(p)
        if p.is_file():original_hashes[str(p.relative_to(BASE))]=sha(p.read_bytes())
    snapshots={p:p.read_bytes() for p in [P4,P5]}
    a4,a5=map(strict,[snapshots[P4],snapshots[P5]])
    targets=a4['spatial_contract']['evidence_contract']['targets']
    target=next(t for t in targets if t['id']=='TG-STATE')
    # Identify only mismatched unit target references, leaving the target catalogue intact.
    hits=[]
    def find(v,path=''):
        if isinstance(v,dict):
            if isinstance(v.get('target_ref'),dict) and v['target_ref'].get('id')=='TG-STATE' and v['target_ref'].get('version')!=target['version']:hits.append((path+'/target_ref/version',v['target_ref']['version']))
            for k,x in v.items():find(x,path+'/'+k)
        elif isinstance(v,list):
            for i,x in enumerate(v):find(x,path+'/'+str(i))
    find(a4)
    assert len(hits)==1,hits
    assert a4['version']==a5['version']=='0.1.0'
    raw4=snapshots[P4]
    raw4,n=re.subn(rb'("version"\s*:\s*)"0\.1\.0"',rb'\g<1>"0.1.1"',raw4,count=1);assert n==1
    pattern=rb'("target_ref"\s*:\s*\{\s*"id"\s*:\s*"TG-STATE",\s*"version"\s*:\s*)"'+re.escape(hits[0][1].encode())+rb'"'
    raw4,n=re.subn(pattern,lambda m:m[1]+json.dumps(target['version']).encode(),raw4);assert n==1
    b4=strict(raw4)
    raw5=snapshots[P5]
    raw5,n=re.subn(rb'("version"\s*:\s*)"0\.1\.0"',rb'\g<1>"0.1.1"',raw5,count=1);assert n==1
    link=a5['linked_r4_record'];assert link['record_id']==a4['record_id'] and (BASE/link['path']).resolve()==P4.resolve()
    start=raw5.index(b'"linked_r4_record"');prefix=raw5[:start];tail=raw5[start:]
    tail,n=re.subn(rb'("version"\s*:\s*)"0\.1\.0"',rb'\g<1>"0.1.1"',tail,count=1);assert n==1
    tail,n=re.subn(rb'("sha256"\s*:\s*)"[0-9a-f]{64}"',lambda m:m[1]+b'"'+sha(raw4).encode()+b'"',tail,count=1);assert n==1
    raw5=prefix+tail;b5=strict(raw5)
    d4=changes(a4,b4);d5=changes(a5,b5)
    assert {d['path'] for d in d4}=={'/version',hits[0][0]}
    assert {d['path'] for d in d5}=={'/version','/linked_r4_record/version','/linked_r4_record/sha256'}
    emit('changes.json',{'R4':d4,'R5':d5})
    for label,old,new in [('R4',snapshots[P4],raw4),('R5',snapshots[P5],raw5)]:
        emit(label+'.diff',''.join(difflib.unified_diff(old.decode('utf-8-sig').splitlines(True),new.decode('utf-8-sig').splitlines(True),fromfile=label+'_before',tofile=label+'_after')))
    c4=OUT/'R4_candidate.json';c5=OUT/'R5_candidate.json'
    with c4.open('xb') as f:f.write(raw4)
    with c5.open('xb') as f:f.write(raw5)
    r4tool=BASE/'07_실행도구/자료검증.py';r5tool=BASE/'07_실행도구/R5_디자인적용검사.py'
    prior4=cli('before_R4',[r4tool,'--record',P4]);prior5=cli('before_R5',[r5tool,P5])
    ok(cli('candidate_R4',[r4tool,'--record',c4]))
    BACK.mkdir(parents=True,exist_ok=True)
    backups={}
    for p in [P4,P5]:
        dest=BACK/p.relative_to(BASE);boundary(dest);dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists():assert dest.read_bytes()==snapshots[p],'backup collision '+str(dest)
        else:
            with dest.open('xb') as f:f.write(snapshots[p])
        assert dest.read_bytes()==snapshots[p]
        backups[p]=dest;note('수정 전 byte 일치 backup: '+str(dest)+' SHA256='+sha(dest.read_bytes()))
    assert all(p.read_bytes()==snapshots[p] for p in snapshots),'concurrent change'
    atomic_target(P4,raw4,snapshots[P4])
    ok(cli('candidate_R5_after_R4',[r5tool,c5]))
    atomic_target(P5,raw5,snapshots[P5])
    final4=cli('after_R4',[r4tool,'--record',P4]);ok(final4)
    final5=cli('after_R5',[r5tool,P5]);ok(final5)
    versiontool=BASE/'실행스킬/video-record-steward/scripts/판본대조.py'
    for label,p in [('R4',P4),('R5',P5)]:ok(cli('version_'+label,[versiontool,'--before',backups[p],'--after',p]))
    assert strict(P5.read_bytes())['linked_r4_record']=={'path':link['path'],'record_id':a4['record_id'],'version':'0.1.1','sha256':sha(P4.read_bytes())}
    final_hashes={str(p.relative_to(BASE)):sha(p.read_bytes()) for p in BASE.rglob('*') if p.is_file()}
    actual_changed=[k for k in original_hashes.keys()|final_hashes.keys() if original_hashes.get(k)!=final_hashes.get(k)]
    assert set(actual_changed)=={str(P4.relative_to(BASE)),str(P5.relative_to(BASE))},actual_changed
    report.update({'status':'applied','records':[{'path':str(p),'id':a.get('record_id',a.get('application_id')),'before_version':a['version'],'after_version':'0.1.1','before_sha256':sha(snapshots[p]),'after_sha256':sha(p.read_bytes()),'backup':str(backups[p]),'backup_byte_match':True} for p,a in [(P4,a4),(P5,a5)]],'actual_changed_input_files':actual_changed,'unchanged_input_files_count':len(original_hashes)-2,'allowed_fields_only':True,'final_r4_r5_link_match':True,'rollback_performed':False,'fact_verified':False,'company_approved':False,'operational_release':False,'R6_full_context_checked':False,'R7_full_link_check_performed':False,'limitations':['R6/R7 전체 고정 자료는 수행 사본에서 일부 생략. full 검증이나 승인으로 보고하지 않음.','R4 unresolved 및 R5 human_review_queue는 원시 검사 결과에 보존.','회사자산은 R5/R1 참조·실파일 SHA 검사만 수행. 미디어 해석/새 디자인/01-A 도구 실행 없음.','여러 파일 저장의 전체 원자성/완전 동시성 제어를 보장하지 않음.'],'human_questions_sent':False,'new_human_decision_needed_for_requested_edit':False})
    emit('input_integrity.json',{'before':original_hashes,'after':final_hashes,'changed':actual_changed})
    emit('결과설명.md','두 초안에 실제 반영했습니다. TG-STATE 단위 참조를 대상 목록의 0.1.0으로 정정하고 R4 자체 판본을 0.1.1로 구분했습니다. R5 연결은 같은 R4 ID·새 판본·실제 저장 bytes SHA256에 맞췄고 R5 자체 판본도 0.1.1로 구분했습니다.\n\n시간·좌표·수치·회사/색·검수 상태 및 나머지 입력 파일은 보존했습니다. byte 일치 변경 전 사본, 필드 차이, unified diff, 전후 검사와 기록별 판본 대조를 남겼습니다. 최종 R4/R5 구조·참조 검사는 통과했으며 미정/사람 검수 대기는 원시 결과에 남아 있습니다.\n\n합성 사본의 제한된 검사입니다. R6/R7 full 검증, 실제 영상 분석, 회사 승인, 운영 반영은 수행하지 않았습니다. 새 사람 판단은 이번 정정에 필요하지 않아 질문을 보내지 않았습니다.\n')
except Exception:
    failure=traceback.format_exc();note('실패 원문:\n'+failure)
    rollback=[]
    for p,raw in reversed(list(written.items())):
        if p.read_bytes()==raw:
            try:atomic_target(p,snapshots[p],raw);rollback.append({'path':str(p),'restored':p.read_bytes()==snapshots[p],'sha256':sha(p.read_bytes())})
            except Exception:rollback.append({'path':str(p),'restored':False,'error':traceback.format_exc()})
        else:rollback.append({'path':str(p),'restored':False,'reason':'external change; not overwritten'})
    report.update({'status':'failed','failure':failure,'rollback':rollback,'operational_release':False})
finally:
    note('PowerShell 초기 읽기에서 InitializeDefaultDrives FileSystem provider 경고가 반복됐으나 명시 경로의 읽기는 exit 0으로 완료. 출력량 큰 목록/검색 결과 일부는 도구에서 잘렸으며 필요한 코드·대상 필드는 후속 한정 읽기로 확인.')
    note('Python 실행은 지정 D 실행파일 -B -X utf8, 입력·스킬·검사기는 own inputs/Phase00만. 웹/API/AE/CU/외부앱·다른 run/운영 DB 접근 없음.')
    emit('result.json',report)
    transcript='# 실제 수행 기록\n\n'+ '\n\n'.join(log)+'\n\n실제 실행 명령/종료와 stdout/stderr 경로는 outputs/result.json의 commands에 저장했습니다. 검사 원시 출력은 outputs/*.stdout.txt와 *.stderr.txt이며 명령 제안과 구분됩니다.\n\n미수집 시간·token: null. 최종 상태: '+report['status']+'\n'
    with (RUN/'transcript.md').open('x',encoding='utf-8') as f:f.write(transcript)
print(json.dumps({'status':report['status'],'output':str(OUT/'result.json'),'failure':failure},ensure_ascii=False))
sys.exit(0 if report['status']=='applied' else 1)
