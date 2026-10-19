
from pathlib import Path
import json, hashlib, copy
from jsonschema import Draft202012Validator
ROOT=Path(r"C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기\phase00-build\R8_시험\video-knowledge-curator-workspace")
OUT=ROOT.parents[1]/"R8_독립검토"
OUT.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def strict(p):
 def pairs(rows):
  d={}
  for k,v in rows:
   if k in d: raise ValueError("duplicate key: "+k)
   d[k]=v
  return d
 return json.loads(p.read_text(encoding="utf-8-sig"),object_pairs_hook=pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
def diffs(a,b,path=""):
 if type(a)!=type(b): return [{"path":path,"before":a,"after":b}]
 if isinstance(a,dict):
  return [d for k in sorted(a.keys()|b.keys()) for d in ([{"path":path+"/"+k,"before":a.get(k),"after":b.get(k)}] if k not in a or k not in b else diffs(a[k],b[k],path+"/"+k))]
 if isinstance(a,list):
  if len(a)!=len(b): return [{"path":path,"before":a,"after":b}]
  return [d for i,(x,y) in enumerate(zip(a,b)) for d in diffs(x,y,path+"/"+str(i))]
 return [] if a==b else [{"path":path,"before":a,"after":b}]
audit={}
for case in ["1","2","3"]:
 casepath=next((ROOT/"iteration-2").glob("eval-0"+case+"-*"))
 for cond in ["new_skill","old_skill"]:
  run=casepath/cond/"run-1"; db=run/"inputs/Phase00"; before=strict(run/"fixture_before.json")["files"]
  now={p.relative_to(db).as_posix():sha(p) for p in db.rglob("*") if p.is_file()}
  changed={k:{"before":v,"after":now.get(k)} for k,v in before.items() if now.get(k)!=v}
  entry={"run":str(run),"fixture_count":len(before),"current_count":len(now),"changed_inputs":changed,"added_inputs":[k for k in now if k not in before],"json_outputs_parse_errors":[],"timing":strict(run/"timing.json")}
  for p in (run/"outputs").glob("*.json"):
   try: strict(p)
   except Exception as e: entry["json_outputs_parse_errors"].append({"path":str(p),"error":str(e)})
  entry["backup_comparisons"]=[]
  for base in [run/"backup",run/"outputs/backup"]:
   if not base.exists(): continue
   for p in base.rglob("*"):
    if not p.is_file(): continue
    candidates=[k for k in before if Path(k).name==p.name]
    if p.name=="레이아웃지식_초안_v0.1.1.json": candidates=["작업초안/레이아웃지식_초안.json"]
    matches=[k for k in candidates if sha(p)==before[k]]
    entry["backup_comparisons"].append({"path":str(p.relative_to(run)),"sha256":sha(p),"fixture_matching_paths":matches})
  if case=="1":
   result=strict(run/"outputs"/("회의메모_공통지식초안.json" if cond=="new_skill" else "knowledge_draft.json"))
   refs=result.get("evidence_manifest",result.get("reference_registry")); errors=[]
   for ref in refs:
    rel=ref.get("relative_path",ref.get("path")); p=db/rel
    if not p.is_file() or sha(p)!=ref["sha256"]: errors.append({"ref":ref,"error":"path/hash"})
    pointer=ref.get("json_pointer")
    if pointer:
     obj=strict(p)
     for bit in pointer.strip("/").split("/"): obj=obj[int(bit)] if isinstance(obj,list) else obj[bit]
     if obj.get("id",obj.get("candidate_id"))!=ref["id"] or obj.get("version")!=ref.get("version"): errors.append({"ref":ref,"error":"pointer/id/version"})
   entry["reference_count"]=len(refs); entry["reference_errors"]=errors
   if cond=="new_skill":
    ids={}
    for rel,key in [("01_공통용어/공통용어사전.json","terms"),("02_원칙과레이아웃/모션과정보전달원칙.json","principles"),("02_원칙과레이아웃/화면설계원칙.json","principles"),("02_원칙과레이아웃/레이아웃지식.json","layouts"),("03_한맥디자인/한맥디자인정본.json","rules")]:
     ids.update({x["id"]:x for x in strict(db/rel)[key]})
    version_errors=[]
    for card in result["cards"]:
     for field in ["knowledge_versions","term_versions","company_rule_versions"]:
      for ref in card.get(field,[]):
       actual=ids.get(ref["id"])
       if actual is None or actual.get("version")!=ref["version"]: version_errors.append(ref)
    entry["card_reference_version_errors"]=version_errors
   else:
    research={x["id"]:x for rel in ["05_출처와검토/R3_모션_조사기록.json","05_출처와검토/R3_레이아웃_조사기록.json"] for x in strict(db/rel)["sources"]}
    entry["source_read_depth_errors"]=[x["source_id"] for x in result["source_audit"] if research[x["source_id"]]["read_depth"]!=x["prior_recorded_read_depth"] or research[x["source_id"]]["sections"]!=x["prior_recorded_sections"]]
  if case=="2":
   draft=db/"작업초안/레이아웃지식_초안.json"
   backup=next(p for base in [run/"backup",run/"outputs/backup"] if base.exists() for p in base.rglob("레이아웃지식_초안_v0.1.1.json"))
   a=strict(backup); b=strict(draft)
   entry["draft_changes"]=diffs(a,b); entry["backup_fixture_match"]=sha(backup)==before["작업초안/레이아웃지식_초안.json"]
   entry["draft_sha256"]=sha(draft); entry["draft_version"]=b["version"]; entry["other_13_identical"]=a["layouts"][1:]==b["layouts"][1:]
   entry["output_copy_identical"]=any(p.read_bytes()==draft.read_bytes() for p in (run/"outputs").glob("레이아웃지식*.json"))
   entry["layout_schema_errors"]=[e.message for e in Draft202012Validator(strict(db/"04_기록규격/레이아웃지식_스키마.json")).iter_errors(b)]
   entry["parent"]=strict(db/"입력메모.json")["draft_parent"]; entry["parent_actual_hash"]=sha(db/entry["parent"]["path"])
  if case=="3":
   source=db/"02_원칙과레이아웃/레이아웃지식.json"; data=strict(source)
   pin=next(x for x in strict(db/"05_출처와검토/버전목록.json")["entries"] if x["id"]=="layout-guidance")
   entry["initial_injected_source_sha256"]=before["02_원칙과레이아웃/레이아웃지식.json"]
   entry["current_source_sha256"]=sha(source); entry["registered_pin"]=pin
   entry["initial_conflict_already_present"]=before["02_원칙과레이아웃/레이아웃지식.json"]!=pin["sha256"]
   draft=run/"outputs"/("레이아웃지식_단일초점_초안_v0.1.2.json" if cond=="new_skill" else "single_focus_draft.json")
   b=strict(draft); entry["draft_sha256"]=sha(draft); entry["draft_version"]=b["version"]; entry["draft_target_limits"]=b["layouts"][0]["limits"]
   entry["layout_schema_errors"]=[e.message for e in Draft202012Validator(strict(db/"04_기록규격/레이아웃지식_스키마.json")).iter_errors(b)]
   entry["draft_layout_count"]=len(b["layouts"])
   if cond=="new_skill": entry["draft_changes"]=diffs(data,b)
   regpaths=["05_출처와검토/버전목록.json","00_운영계약/정본과표시_연결목록.json","02_원칙과레이아웃/레이아웃_심화지식.json"]
   entry["registered_files_unchanged"]=all(now[k]==before[k] for k in regpaths)
  audit[case+"_"+cond]=entry
(OUT/"R8_01_독립_읽기대조.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:{a:b for a,b in v.items() if a not in ["backup_comparisons","timing","draft_changes"]} for k,v in audit.items()},ensure_ascii=False,indent=2))
