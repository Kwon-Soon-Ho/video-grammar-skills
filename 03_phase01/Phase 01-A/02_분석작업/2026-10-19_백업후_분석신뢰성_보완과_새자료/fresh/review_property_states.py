"""Correct property-state summaries without replacing any first or detailed record."""
from pathlib import Path
from copy import deepcopy
import json,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import load,check,digest
from render_observations import render
def save(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists(),p;p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
for aid in ('NEW-N','NEW-P'):
 folder=HERE/'detail-results'/aid;original=folder/'observations-detailed.json';d=deepcopy(load(original));fixes=[]
 changed={('caption','text')}
 if aid=='NEW-P':changed|={('policy-panel','color'),('regional-row1','color'),('regional-row2','color'),('regional-link','visibility')}
 for row in d['observation_rows']:
  if (row['object_id'],row['property']) in changed:
   fixes.append({'row':row['id'],'before':row['change'],'after':'changed','reason':'해당 속성에 실제 시간 변화가 기록돼 있음. facet=value/presence라는 이유로 unchanged로 만들 수 없음.'});row['change']='changed'
 if aid=='NEW-N':
  uid='u04';d['unknowns'].append({'id':uid,'object_id':'rear-arcs','question':'먼 끝의 작은 화살표는 어느 시각부터 어떤 강약으로 변하는가?','state':'open','reason':'두 시점의 존재는 확인했지만 해당 작은 ROI를 시간순 연속 대조하지 않아 불변으로 확정할 수 없음','required_basis_kind':'observed','next_probe':'먼 끝 위치를 기준으로 원본 크기 ROI의 전후·중간 강약과 출현 범위를 대조','resolution_claim_ids':[]})
  row=next(r for r in d['observation_rows'] if r['id']=='rear-arcs-visibility');row.update(review_state='unresolved',change='unknown',unknown_ids=[uid],reason='확인한 존재 주장은 보존하고 시간 변화의 미확정은 별도 열린 검수로 연결')
  fixes.append({'row':row['id'],'before':'unchanged','after':'unresolved / unknown','reason':'존재만 기록한 것을 전체 구간 불변으로 확대하지 않음'})
  d['discovery']['unresolved_ids'].append(uid);d['layout']['unresolved_ids'].append(uid)
  for state in d['layout']['states']:state['unresolved_ids'].append(uid)
 d['method']+=' 후속 대상×속성 재대조에서 요약 행의 change를 주장 facet만으로 정하지 않고 실제 시간 변화·미확정에 맞춰 보완했다.'
 errors=check(d,load(folder/'catalog.json'));assert not errors,errors
 dest=folder/'observations-property-reviewed.json';save(dest,d);(folder/'observations-property-reviewed.md').write_text(render(d),encoding='utf-8')
 save(folder/'property-review.json',{'before':{'path':str(original),'sha256':digest(original)},'after':{'path':str(dest),'sha256':digest(dest)},'reviewer':'same AI context','fixes':fixes,'structure_and_provenance_passed':True,'independent_evaluation':False,'whole_video_complete':False,'note':'검사기는 이 의미 불일치를 자동 발견하지 못했다. 직접 속성 검토에서 발견한 작성기 요약 오류 보완.'})
 print(aid,len(fixes),'property summaries corrected; originals preserved')
