from pathlib import Path
import json,hashlib,datetime,copy
from fractions import Fraction
B=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
assert not list((B/'trials').rglob('observations.json')),'must seal before any candidate answer'
audit=read(B/'reference/audit.json');d=read(B/'reference/reference-draft.json');atoms={a['id']:a for c in d['criteria'] for a in c['atoms']}
atoms['H01-C08']['state_or_direction_or_order']='큰 T 뒤에 놓인 회색 Value of는 오른쪽 일부가 가려진 채 남으며 TOVA 로고/설명은 앞에 유지된다'
atoms['H01-C05']['state_or_direction_or_order']='3.2~4.6초에 완성된 Value of가 어두운 회색으로 약해진 뒤 유지되며 후반에는 큰 T에 일부 가려진다'
atoms['H03-D03']['state_or_direction_or_order']='왼쪽은 세로로 긴, 위에서 내려다본 운동장 사진; 오른쪽은 넓은 사선 항공사진이며 흰 둥근 외곽을 유지한다. 정확한 투영방식은 단정하지 않음'
atoms['H03-D06']['state_or_direction_or_order']='DOC064 장비상세 예정13~21초/취득방법21~27초/실촬영27~61초와 달리 실제25~29.4초는 수신기 비교,29.6초대부터 취득방법으로 전환된다'
h2=d['criteria'][1];h2['unjudgable_properties']=[x for x in h2['unjudgable_properties'] if not x.startswith('기능 설명 마지막')]
h2['unjudgable_properties']=[x.replace('정밀 위치/크기 easing은 같은 특징 추적 없이는 unknown 허용','정확한 AE 곡선/핸들 수치는 미상. 아래 D08의 정성 크기 감속과 구분') for x in h2['unjudgable_properties']]
def add_h2(aid,target,prop,text,times):
 fs=read(B/'cases/A5-A/H02/실행기록.json')['frames']+read(B/'cases/A5-A/REF-H02/실행기록.json')['frames']
 base=copy.deepcopy(h2['atoms'][-1]);base.update(id=aid,target=target,property_or_relation=prop,state_or_direction_or_order=text,time_bracket=[min(times),max(times)],evidence=[])
 for t in times:
  f=next(x for x in fs if Fraction(x['actual_playback_seconds'])==Fraction(str(t)))
  base['evidence'].append({'path':f['path'],'actual_seconds':f['actual_playback_seconds'],'sha256':f['sha256']})
 h2['atoms'].append(base)
add_h2('H02-D07','기능 설명','meaning','대중교통 수단&노선에 따라 기본 요금·거리·추가거리 및 요금·통합환승요금제를 쉽게 적용하도록 설계한다는 설명',[14.6,16.8])
add_h2('H02-D08','새 지도 UI','size_easing','같은 외곽의 진행 중 확대 증가량이 후반에 작아져 정착하는 감속/ease-out 성격. 정성 관찰이며 정확한 함수·원본 AE 곡선 미상',[12.4,12.8,13.2,13.6])
atoms['H04-C05']['boundary_seconds']=[71.4,71.5]
atoms['H04-C05']['boundary_kind']='shot-change bracket; old at71.4,new at71.5'
ledger=read(B/'reference/crops.json');f=next(x for x in read(B/'cases/A5-A/REF-H02/실행기록.json')['frames'] if x['actual_playback_seconds']=='73/5')
ledger.append({'case_id':'H02','path':str(B/'reference/H02-c10.png'),'parent_path':f['path'],'crop_xyxy_native_pixels':[700,1450,1950,1900],'actual_seconds':f['actual_playback_seconds']})
save(B/'reference/crops-final.json',ledger)
h2['native_crop_evidence'].append(ledger[-1])
d.update(version='pretrial-reference-sealed-1',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),independent_audit='audit.json',post_audit_changes={'clarifications':['H01 partial occlusion','H03 projection softened','H03 original planned times expanded'],'added_before_any_primary_output':['H02-D07 readable functional text','H02-D08 judgable qualitative size deceleration'],'atoms_before':55,'atoms_after':57},scope='AI reference with separate raw-source AI audit, not human gold; exact display times and source hashes. Frozen before primary answers. State/event spans are not onset answers.')
save(B/'reference/reference.json',d)
save(B/'reference/seal.json',{'utc':d['sealed_utc'],'primary_outputs_at_seal':0,'human_gold':False,'reference_sha256':hashlib.sha256((B/'reference/reference.json').read_bytes()).hexdigest(),'audit_sha256':hashlib.sha256((B/'reference/audit.json').read_bytes()).hexdigest(),'counts':{c['case_id']:{t:sum(a['tier']==t and a['judgable'] for a in c['atoms']) for t in ['core','detail']} for c in d['criteria']},'extra_native_frames_used':64,'extra_native_frames_left_for_dispute':0,'reference_crops':39})
print('reference sealed: 57 atoms; primary outputs 0')
