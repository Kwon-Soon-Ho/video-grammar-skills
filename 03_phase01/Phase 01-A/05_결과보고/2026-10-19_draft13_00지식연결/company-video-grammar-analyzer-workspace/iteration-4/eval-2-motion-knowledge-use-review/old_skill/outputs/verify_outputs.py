from pathlib import Path
import json,hashlib
o=Path(__file__).resolve().parent
j=json.loads((o/"index.json").read_text(encoding="utf-8"))
k=json.loads((o/"knowledge-pins.json").read_text(encoding="utf-8"))
m=json.loads((o/"input-manifest.json").read_text(encoding="utf-8"))
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
copies=all(h(x["path"])==x["sha256"]==h(x["copy"])==x["copy_sha256"] for x in m["inputs"] if "copy" in x)
known={x["id"] for x in k["terms"]}; principles={x["id"] for x in k["principles"]}
assert copies
assert len(j["uses"])==6 and sum(len(e["original_frames"]) for e in json.loads((o/"evidence-manifest.json").read_text(encoding="utf-8")).values())==46
assert all(set(r["properties"]+r["timing"]+r["functions"])<=known for r in j["uses"])
assert all(set(r["principles"])<=principles for r in j["uses"])
assert all(set(f["sequence"])<={r["id"] for r in j["uses"]} for f in j["flows"])
result={"copied_input_hashes_match":copies,"use_count":len(j["uses"]),"flow_count":len(j["flows"]),"frame_refs":46,"taxonomy_refs_resolve":True,"principle_refs_resolve":True,"flow_use_refs_resolve":True,"original_media_rehash":False,"audio_checked":False,"scope":"local structure/reference checks only, not independent content approval"}
(o/"verification.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,ensure_ascii=False))

