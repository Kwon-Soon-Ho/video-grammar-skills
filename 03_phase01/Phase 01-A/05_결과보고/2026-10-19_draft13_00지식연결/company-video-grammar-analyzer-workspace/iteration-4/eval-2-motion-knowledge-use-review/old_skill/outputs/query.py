"""Local explicit-filter query; no semantic recommendation."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--id");p.add_argument("--concept");p.add_argument("--principle");p.add_argument("--relation");p.add_argument("--query")
p.add_argument("--include-excluded",action="store_true")
a=p.parse_args()
root=Path(__file__).resolve().parent
db=json.loads((root/"index.json").read_text(encoding="utf-8"))
uses=db["uses"]
if a.id:
    flow=next((f for f in db["flows"] if f["id"]==a.id),None)
    if flow: uses=[r for r in uses if r["id"] in flow["sequence"]]
    else: uses=[r for r in uses if r["id"]==a.id or r["case"]==a.id]
if a.concept: uses=[r for r in uses if a.concept in r["properties"]+r["timing"]+r["functions"]]
if a.principle: uses=[r for r in uses if a.principle in r["principles"]]
if a.relation: uses=[r for r in uses if any(x["type"]==a.relation for x in r["relations"])]
if a.query: uses=[r for r in uses if a.query.casefold() in json.dumps(r,ensure_ascii=False).casefold()]
result={"mode":"explicit local filters; observations only","count":len(uses),"ids":[r["id"] for r in uses],"uses":uses,"reviews":[v for v in db["reviews"] if set(v["targets"]) & {r["id"] for r in uses}],"excluded_proposal_count":len(db["excluded_proposals"])}
if a.include_excluded:
    result["excluded_proposals"]=[x for x in db["excluded_proposals"] if (not a.id or x["id"]==a.id) and (not a.query or a.query in json.dumps(x,ensure_ascii=False))]
print(json.dumps(result,ensure_ascii=False,indent=2))

