"""Read-only retrieval audit of this run's explicit index; not a visual quality test."""
import json, hashlib
from pathlib import Path

out=Path(__file__).resolve().parent
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
q=load(out/'query-TIME-DELAY.json')
traces=[]
for hit in q['uses']:
    record=load(hit['record_path'])
    unit=hit['unit']; use=hit['use']
    claims=[c for c in record['claims'] if c['id'] in use['claim_ids']]
    sources=[s for s in record['source_records'] if any(s['id'] in c['source_record_ids'] for c in claims)]
    events=[e for e in record['events'] if e['unit_id']==unit['id']]
    ev_ids={e['id'] for e in events}
    event_links=[e for e in record['event_links'] if e['from'] in ev_ids and e['to'] in ev_ids]
    for pin in sources+hit['evidence']:
        path=Path(pin['path'])
        if not path.is_absolute():path=Path(hit['record_path']).parent/path
        assert sha(path)==pin['sha256'],str(path)
    assert use['definition_version']==unit['definition_version']
    assert any(e['relation']=='continues_after' for e in event_links)
    traces.append({'case':use['case_unit_id'],'region':use['region'],'definition':unit['id'],'definition_version':unit['definition_version'],'query_concept':'TIME-DELAY','content':use['content'],'time':use['time'],'claims':claims,'events':events,'event_links':event_links,'original_records':sources,'current_evidence':hit['evidence'],'actual_reviews':hit['reviews']})
assert {x['definition'] for x in traces}=={'A-M3','B-M3'}
assert not load(out/'query-excluded-proposal.json')['uses']
for hit in load(out/'query-IP-05.json')['uses']:
    assert any(r['criterion_id']=='IP-05' and r['status']=='not_reviewed' for r in hit['reviews'])
for hit in load(out/'query-Q-MOTION-01.json')['uses']:
    assert any(r['criterion_id']=='Q-MOTION-01' and r['status']=='hold' for r in hit['reviews'])
result={'scope':'actual query -> current definition/use -> original prior records and evidence pins -> temporal relation/review audit; no visual truth or company approval','passed':True,'time_delay_hits':[x['definition'] for x in traces],'excluded_proposal_hits':0,'traces':traces}
(out/'roundtrip-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':True,'time_delay_hits':result['time_delay_hits'],'excluded_proposal_hits':0,'output':'roundtrip-result.json'},ensure_ascii=False,indent=2))
