# -*- coding: utf-8 -*-
"""지정된 합성 DB 두 초안만 정리. 실행과 검사는 outputs에 보존."""
from pathlib import Path
import copy, difflib, hashlib, json, re, subprocess, sys, traceback
RUN = Path(__file__).resolve().parents[1]
BASE = RUN / "inputs" / "Phase00"
OUT = RUN / "outputs"
PYTHON = Path(r"D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00\.환경\Scripts\python.exe")
R4 = "12_통합기록/통합기록_작업초안.json"
R5 = "작업초안/디자인적용_초안.json"
BACK = RUN / "backup" / "requested-draft-fix"
TRANSCRIPT = RUN / "transcript.md"
assert Path(sys.executable).resolve() == PYTHON.resolve()
assert BASE.resolve().is_relative_to(RUN.resolve())
OUT.mkdir(exist_ok=True)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def dump(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8")
def log(message):
    with TRANSCRIPT.open("a",encoding="utf-8",newline="\n") as f: f.write(message+"\n")
def read_json(raw):
    def unique(pairs):
        obj={}
        for k,v in pairs:
            if k in obj: raise ValueError("중복 JSON 키: "+k)
            obj[k]=v
        return obj
    def nonfinite(value): raise ValueError("비유한 JSON 수: "+value)
    return json.loads(raw.decode("utf-8"),object_pairs_hook=unique,parse_constant=nonfinite)
def snapshot():
    return {p.relative_to(BASE).as_posix():sha(p.read_bytes())
            for p in BASE.rglob("*") if p.is_file()}
commands=[]
def check(label, tool, rel):
    cmd=[str(PYTHON),"-B","-X","utf8",str(BASE/"07_실행도구"/tool)]
    cmd += ["--record",str(BASE/rel)] if tool=="자료검증.py" else [str(BASE/rel)]
    proc=subprocess.run(cmd,cwd=BASE,capture_output=True,encoding="utf-8",errors="strict")
    (OUT/(label+".stdout.txt")).write_text(proc.stdout,encoding="utf-8")
    (OUT/(label+".stderr.txt")).write_text(proc.stderr,encoding="utf-8")
    result=read_json(proc.stdout.encode("utf-8")) if proc.stdout.strip() else None
    if result is not None: dump(OUT/(label+".json"),result)
    entry={"label":label,"argv":cmd,"exit_code":proc.returncode,"stdout":label+".stdout.txt",
           "stderr":label+".stderr.txt","valid":result.get("valid") if result else None}
    commands.append(entry)
    log("검사 실행: "+subprocess.list2cmdline(cmd)+"\n종료코드: "+str(proc.returncode)+
        "\n원시 stdout/stderr: outputs/"+entry["stdout"]+", outputs/"+entry["stderr"]+"\n")
    return result
def differences(a,b,path=""):
    if type(a) is not type(b): return [{"path":path,"before":a,"after":b}]
    if isinstance(a,dict):
        assert set(a)==set(b),"키 추가/삭제 금지"
        return [d for k in a for d in differences(a[k],b[k],path+"/"+k)]
    if isinstance(a,list):
        assert len(a)==len(b),"배열 길이 변경 금지"
        return [d for i,(x,y) in enumerate(zip(a,b)) for d in differences(x,y,path+"/"+str(i))]
    return [] if a==b else [{"path":path,"before":a,"after":b}]
log("""# 실제 수행 기록
- 지정 task.txt, 수행사본_범위.json, 실행스킬/video-record-steward/SKILL.md와 references/작업기준.md를 읽었다.
- DB 안의 두 초안, 보존과버전 계약, 관련 검사 도구를 읽었다. rg --files는 지정 DB 안에서만 실행했다.
- 외부 원본 DB/인터넷/API/AE/CU/외부 앱은 접근하지 않았다. 회사 자산은 검사기의 참조 무결성 해시 확인에만 사용한다.
- 초기 PowerShell 읽기 명령에서 'Attempting to perform the InitializeDefaultDrives operation on the FileSystem provider failed.' 경고가 발생했다. task/skill/DB 읽기는 정상 완료되었다.
- 실제 읽기 실패: Get-Content -LiteralPath '07_실행도구\\R5_디자인적用검사.py' -Raw (exit 1). '用' 오타로 파일이 없었다. 올바른 'R5_디자인적용검사.py'로 다시 읽어 exit 0으로 복구했다. 파일 생성/수정은 하지 않았다.
- 지정 Python에 -B -X utf8를 사용했다. Python -c로 targets와 units의 참조 판본을 확인했다.
- 관측: targets의 TG-STATE 판본 0.1.0, units의 TG-STATE 참조 판본 0.9.9. 통합기록 record_id R8-DEV-STEW-01, version 0.1.0.
- 수정 범위: 통합기록 /units/2/target_ref/version 및 /version. 디자인 /linked_r4_record/version 및 /linked_r4_record/sha256. 디자인 자체 version은 '연결만' 요청에 따라 유지한다.
""")
try:
    initial=snapshot()
    dump(OUT/"입력파일_해시목록.json",initial)
    before={rel:(BASE/rel).read_bytes() for rel in [R4,R5]}
    old={rel:read_json(raw) for rel,raw in before.items()}
    before_r4=check("수정전_통합기록_검사","자료검증.py",R4)
    before_r5=check("수정전_디자인연결_검사","R5_디자인적용검사.py",R5)
    assert BACK.exists() is False,"기존 backup 덮어쓰기 금지"
    for rel,raw in before.items():
        p=BACK/rel
        p.parent.mkdir(parents=True,exist_ok=True)
        with p.open("xb") as f: f.write(raw)
        assert p.read_bytes()==raw
    backup_info={rel:{"backup_path":str(BACK/rel),"sha256":sha(raw),
                      "byte_identical":(BACK/rel).read_bytes()==raw}
                 for rel,raw in before.items()}
    dump(OUT/"변경전_보존확인.json",backup_info)
    log("변경 전 사본: backup/requested-draft-fix 아래 원래 상대경로로 저장. 두 파일 모두 원본과 바이트 및 SHA256 동일.\n")
    data=copy.deepcopy(old[R4])
    targets=data["spatial_contract"]["evidence_contract"]["targets"]
    target=[t for t in targets if t["id"]=="TG-STATE"]
    units=[(i,u) for i,u in enumerate(data["units"]) if u["target_ref"]["id"]=="TG-STATE"]
    assert len(target)==len(units)==1
    i,u=units[0]
    assert data["record_id"]=="R8-DEV-STEW-01" and data["version"]=="0.1.0"
    assert u["target_ref"]["version"]=="0.9.9" and target[0]["version"]=="0.1.0"
    data["version"]="0.1.1";u["target_ref"]["version"]=target[0]["version"]
    # Existing formatting and line endings are preserved; replace only exact spans.
    raw4=before[R4]
    oldhead=b'  "record_id": "R8-DEV-STEW-01",\r\n  "version": "0.1.0"'
    newhead=oldhead.replace(b'"0.1.0"',b'"0.1.1"')
    oldref=b'"id": "TG-STATE",\r\n        "version": "0.9.9"'
    newref=oldref.replace(b'"0.9.9"',b'"0.1.0"')
    assert raw4.count(oldhead)==raw4.count(oldref)==1
    newraw4=raw4.replace(oldhead,newhead).replace(oldref,newref)
    assert read_json(newraw4)==data
    assert (BASE/R4).read_bytes()==before[R4],"입력 경쟁 변경"
    (BASE/R4).write_bytes(newraw4)
    actual4=(BASE/R4).read_bytes()
    assert actual4==newraw4
    newhash=sha(actual4)
    linked=copy.deepcopy(old[R5])
    assert linked["linked_r4_record"]["record_id"]==data["record_id"]
    linked["linked_r4_record"]["version"]=data["version"]
    linked["linked_r4_record"]["sha256"]=newhash
    raw5=before[R5]
    oldlink=json.dumps(old[R5]["linked_r4_record"],ensure_ascii=False,indent=2)
    # Use the exact existing linked block and its indentation/CRLF.
    pattern=rb'("linked_r4_record": \{\r\n(?:.*\r\n)*?  \})'
    matches=list(re.finditer(pattern,raw5))
    assert len(matches)==1
    block=matches[0].group(1)
    assert block.count(b'"version": "0.1.0"')==1
    updatedblock=block.replace(b'"version": "0.1.0"',b'"version": "0.1.1"')
    updatedblock=updatedblock.replace(old[R5]["linked_r4_record"]["sha256"].encode("ascii"),newhash.encode("ascii"))
    newraw5=raw5[:matches[0].start(1)]+updatedblock+raw5[matches[0].end(1):]
    assert read_json(newraw5)==linked
    assert (BASE/R5).read_bytes()==before[R5],"입력 경쟁 변경"
    (BASE/R5).write_bytes(newraw5)
    assert (BASE/R5).read_bytes()==newraw5
    diff4=differences(old[R4],read_json(actual4))
    diff5=differences(old[R5],read_json(newraw5))
    assert {d["path"] for d in diff4}=={"/version",f"/units/{i}/target_ref/version"}
    assert {d["path"] for d in diff5}=={"/linked_r4_record/version","/linked_r4_record/sha256"}
    diff_result={R4:diff4,R5:diff5}
    dump(OUT/"필드별_차이.json",diff_result)
    for rel,raw in [(R4,actual4),(R5,newraw5)]:
        lines=difflib.unified_diff(before[rel].decode("utf-8").splitlines(keepends=True),
                                  raw.decode("utf-8").splitlines(keepends=True),
                                  fromfile="backup/"+rel,tofile="updated/"+rel)
        (OUT/("통합기록.diff" if rel==R4 else "디자인연결.diff")).write_text("".join(lines),encoding="utf-8",newline="")
    log("실제 저장: 통합기록 TG-STATE 참조 0.9.9→0.1.0, 동일 ID의 기록 version 0.1.0→0.1.1. 저장된 바이트 SHA256 "+newhash+
        ". 디자인 연결의 version/sha256만 갱신. 필드 차이 allowlist 네 곳 검사 통과.\n")
    after_r4=check("수정후_통합기록_검사","자료검증.py",R4)
    after_r5=check("수정후_디자인연결_검사","R5_디자인적용검사.py",R5)
    final=snapshot()
    changed=[p for p in initial if final.get(p)!=initial[p]]
    added=[p for p in final if p not in initial]
    deleted=[p for p in initial if p not in final]
    assert set(changed)=={R4,R5} and not added and not deleted
    dump(OUT/"수정후_파일해시목록.json",final)
    preservation={"changed_files":changed,"added_files":added,"deleted_files":deleted,
                  "other_db_files_byte_hash_unchanged":True,"json_diff_allowlist_pass":True,
                  "record_id_preserved":data["record_id"]==old[R4]["record_id"],
                  "linked_record_id_preserved":linked["linked_r4_record"]["record_id"]==old[R5]["linked_r4_record"]["record_id"],
                  "linked_actual_saved_sha256_matches":linked["linked_r4_record"]["sha256"]==sha((BASE/R4).read_bytes()),
                  "linked_version_matches":linked["linked_r4_record"]["version"]==data["version"],
                  "times_coordinates_numbers_company_colors_review_state_preserved":True}
    dump(OUT/"보존과연결_검사.json",preservation)
    result={"task_completed":bool(after_r4 and after_r4["valid"] and after_r5 and after_r5["valid"]),
            "scope":"합성 사본의 두 초안 참조/판본 정리 및 구조/연결 검사",
            "record_id":data["record_id"],"old_version":old[R4]["version"],"new_version":data["version"],
            "saved_record_sha256":newhash,
            "checks":{"before_integrated":before_r4["valid"],"before_design":before_r5["valid"],
                      "after_integrated":after_r4["valid"],"after_design":after_r5["valid"]},
            "backups":backup_info,"changes":diff_result,"preservation":preservation,
            "commands":commands,
            "limitations":["실제 영상·프레임·미디어 해석/생성 미수행","합성 값을 원본 관측/회사 승인으로 승격하지 않음",
                "R6/R7 일부 자료 생략: full 연결 통과를 주장하지 않음. 해당 도구 미실행.",
                "검사 통과는 구조와 참조만 뜻하며 사람 검수/사실성/회사 승인/운영 배포가 아님"],
            "fact_verified":False,"company_approved":False,"operational_release":False}
    dump(OUT/"결과.json",result)
    dump(OUT/"실행명령_종료코드.json",commands)
    remaining={"integrated":after_r4.get("unresolved",[]),"integrated_human_review_queue":after_r4.get("human_review_queue",[]),
               "design_human_review_queue":after_r5.get("human_review_queue",[])}
    dump(OUT/"남은검수.json",remaining)
    text=("두 초안에 실제 반영했습니다.\n통합기록 ID R8-DEV-STEW-01을 유지하고 판본을 0.1.1로 구분했습니다. "
          "TG-STATE 단위 참조를 대상 자체 판본 0.1.0으로 수정했습니다.\n"
          "디자인 초안은 연결 ID/경로를 유지하고 연결 판본과 통합기록 실제 저장 바이트 SHA256만 갱신했습니다.\n"
          "두 기록의 수정후 구조/연결 검사: 통합기록 "+str(after_r4["valid"])+", 디자인 "+str(after_r5["valid"])+".\n"
          "변경 전 사본은 backup/requested-draft-fix, 차이는 outputs의 두 .diff와 필드 차이 JSON에 있습니다.\n"
          "다른 DB 파일의 해시와 시간·좌표·측정 수치·회사·색·검수 상태를 보존했습니다.\n"
          "R6/R7 전체 검증은 수행하지 않았으며 실제 영상 진실성·사람 검수·회사 승인·운영 배포를 뜻하지 않습니다.\n")
    (OUT/"결과설명.txt").write_text(text,encoding="utf-8")
    log("수정후 검사 결과: 통합기록 valid="+str(after_r4["valid"])+", 디자인 valid="+str(after_r5["valid"])+
        ". DB 전체 파일 해시 비교에서 두 초안만 변경, 파일 추가/삭제 없음. 남은 미정/사람검수는 outputs/남은검수.json에 저장.\n"+
        "한계: R6/R7 full 연결, 실제 미디어/관측, 사람/회사 승인은 검사하지 않았다. 시간/token telemetry는 수집하지 않았다.\n"+
        "최종 결과: outputs/결과.json 및 결과설명.txt.\n")
    print(json.dumps({"completed":result["task_completed"],"checks":result["checks"],"changed_files":changed,
                      "sha256":newhash,"result":str(OUT/"결과.json")},ensure_ascii=False,indent=2))
    if not result["task_completed"]: sys.exit(1)
except Exception:
    detail=traceback.format_exc()
    (OUT/"작업실패.log").write_text(detail,encoding="utf-8")
    dump(OUT/"실행명령_종료코드.json",commands)
    log("실패/중단:\n"+detail)
    raise

