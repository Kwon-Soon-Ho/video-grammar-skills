from pathlib import Path
import json,datetime
B=Path(__file__).resolve().parent;A4=B.parent/'phase01a-a4'
criteria=json.loads((A4/'root-audit/criteria-frozen.json').read_text(encoding='utf-8'))['criteria']
result={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'targeted final-candidate regression, not a new A4 all-seven-window/variant-pair test','prior_basis':'A4 frozen criteria, added caption criterion and disclosed easing correction','created_before_reading_new_outputs':True,'cases':{}}
result['cases']['V05']={'criteria':criteria['V05'],'additional':['확정 가감속 주장은 이동 중 같은 대상의 변화율 근거이며 정착만으로 단정하지 않음'],'focus':'A4-C01 English exit contraction and residual text'}
for cid in ['V06S','V06W']:
 result['cases'][cid]={'criteria':[criteria[cid][i] for i in [0,1,2,4]],'additional':['후반 자막의 직전 상태를 4대 핵심가치 문구로 연결하고 초기 경관 문구와 혼입하지 않음','작업보고 문서의 정착을 근거 없는 감속으로 확정하지 않음; 위치·가시성·리빌 속성을 구분'],'focus':'A4-C02 caption association / A4-C03 deceleration evidence','excluded':'A4 variant-pair comparison criterion: regression input is one source per run; no new cross-variant task. Existing A4 variant comparison remains preserved.'}
p=B/'legacy-criteria.json';assert not p.exists();p.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('targeted prior-case criteria sealed before output review')
