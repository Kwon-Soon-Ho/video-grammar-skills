"""실제 회사 기록/미디어를 사용하지 않는 통합 계약 합성 검사."""
from pathlib import Path
import json,hashlib,importlib.util,copy
BASE=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
def load(p):
 s=importlib.util.spec_from_file_location('integration_test_dep',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def read(p):return json.loads((BASE/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256((BASE/p).read_bytes()).hexdigest()
def ref(v):return {k:v[k] for k in ['id','version']}
def frac(n,d=1):return {'num':n,'den':d}
def fixture():
 core=load(BASE/'07_실행도구/좌표변환_규격시험.py').fixture();ec=core['evidence_contract']
 ec['targets'].append({'id':'TG-BEAT','version':'0.1.0','unit':'beat','asset_ref':ec['targets'][0]['asset_ref'].copy(),'parent_ref':ref(ec['targets'][1]),'period_ref':'EX-SEGMENT','label':'상태를 가로지를 수 있는 합성 동작'})
 taxonomy=read('01_공통용어/공통용어사전.json');d=read('03_한맥디자인/한맥디자인정본.json');rules=read('01_공통용어/분류운영규칙.json')
 taxonomy_ref={'id':taxonomy['taxonomy_id'],'version':taxonomy['version'],'sha256':sha('01_공통용어/공통용어사전.json')};dref={'id':d['profile_id'],'version':d['version'],'sha256':sha('03_한맥디자인/한맥디자인정본.json')}
 units=[]
 for t in ec['targets']:
  if t['unit']=='object':continue
  unit='state' if t['unit']=='screen_state' else t['unit']
  units.append({'target_ref':ref(t),'classifications':[{'axis':a,'state':'not_assessed','term_ids':[],'reason_codes':['not_assessed_yet'],'candidate_text':None,'basis':'not_assessed','claim_ref':None,'note':'合성'.replace('合','합')+' 구조 예시. 실제 내용 분류 미수행.'} for a,u in rules['axis_units'].items() if unit in u],'scenario_refs':[],'sample_frame_refs':['EX-FRAME'] if unit=='state' else [],'related_state_refs':[ref(ec['targets'][2])] if unit=='beat' else [],'limitations':'규격 구조만 설명하는 인위적 예시.'})
 return {'schema_version':'0.2.0','record_id':'EX-INTEGRATED-001','version':'0.1.0','catalog_refs':{'taxonomy':taxonomy_ref,'design_profile':dref,'classification_rules':{'path':'01_공통용어/분류운영규칙.json','sha256':sha('01_공통용어/분류운영규칙.json')}},'spatial_contract':core,'units':units,'coordinate_bindings':[],'cut_markers':[],'asset_metadata':{'container':None,'video_codec':None,'audio_presence':'unknown','language':None,'evidence_refs':[],'limitations':'실제 영상 미제공. 원본 메타 미조사.'},'design':{'profile_ref':dref,'palette_role_bindings':{'background':'HM-COLOR-GREEN-500'},'optional_style_refs':[],'project_overrides':[]},'run':{'mode':'contract_test','status':'not_started','actor':'synthetic-fixture','tool':None,'model':None,'started_at':None,'ended_at':None,'input_refs':[],'output_record_ref':None,'parameters_sha256':None,'limitations':'자동분석 실행이 아닌 합성 계약 설명 예. 값은 실제미디어 근거가 아니다.'},'review_contexts':[],'notes':'운영 DB/회사 문법 검색에서 제외하는 spec_test다. 구형 설명예를 가짜 hash/PTS로 이관한 기록이 아니다.'}
def measured(x):
 ec=x['spatial_contract']['evidence_contract'];c=ec['claims'][0];e=ec['evidence'][2];g=x['spatial_contract']['geometries'][0]
 c.update(support_mode='numerical_estimate',aspect='numeric_value',statement='원본 좌표 x 성분을 연결하는 합성 표본.',measurement={'method':'single_sample_component','quantity':'position_x','unit':'px','sample_unit':'raster_px','value':300,'uncertainty':0,'uncertainty_kind':'absolute_bound','samples':[{'frame_ref':g['frame_ref'],'evidence_ref':ref(e),'target_ref':c['scope']['target_ref'].copy(),'value':300,'coordinate_space_ref':g['space_ref']['id']}],'assumptions':['실제 추적 아님'],'limitations':'구조 연결 합성 예.'})
 # R4-2 표본 단위는 px/normalized. geometry의 raster_px 명칭을 통합에서 명시 대응한다.
 c['measurement']['sample_unit']='px'
 x['coordinate_bindings']=[{'claim_ref':ref(c),'sample_index':0,'geometry_ref':ref(g),'component':'x','mapping_ref':None,'numeric_encoding':{'mode':'exact_decimal','decimal_places':None},'limitations':'명목 성분 연결만 검사.'}]
def classified(x,observation=False):
 ec=x['spatial_contract']['evidence_contract'];c=copy.deepcopy(ec['claims'][0]);c.update(id='CL-LAYOUT',support_mode='rendered_observation' if observation else 'not_observed_example',statement='레이아웃 출처 구분의 합성 예.')
 c['scope']['target_ref']=ref(ec['targets'][2]);ec['claims'].append(c)
 # 상위 state 근거의 경우 object claim도 같은 state를 지지로 쓸 수 있다.
 ec['evidence'][2]['target_ref']=ref(ec['targets'][2])
 for g in x['spatial_contract']['geometries']:
  if g['evidence_ref']['id']==ec['evidence'][2]['id']:g['target_ref']=ref(ec['targets'][2])
 # 변환 결과 geometry도 state로 동일하게 맞춘다.
 for g in x['spatial_contract']['geometries']:g['target_ref']=ref(ec['targets'][2])
 for e in ec['evidence'][3:]:e['target_ref']=ref(ec['targets'][2])
 c['scope']['target_ref']=ref(ec['targets'][2])
 # 기존 object claim/근거 타깃은 모두 state로 맞춘 설명 예다.
 ec['claims'][0]['scope']['target_ref']=ref(ec['targets'][2])
 cl=next(c for c in x['units'][2]['classifications'] if c['axis']=='layout');cl.update(state='classified',term_ids=['LAYOUT-CARD-GROUP'],reason_codes=[],basis='observation' if observation else 'plan',claim_ref=ref(c))
def review(x,checker):
 ec=x['spatial_contract']['evidence_contract'];c=ec['claims'][0]
 c['review_ref']='RV-EX';r={'id':'RV-EX','kind':'specimen','reviewer_id':'SYNTHETIC','reviewed_at':'2026-10-15T00:00:00Z','claim_ref':ref(c),'context_sha256':'0'*64,'outcome':'inconclusive','rationale':'실제 사람 검수 아닌 재검수 계약 합성 예.','conflict_resolution':None};ec['review_records']=[r]
 ev=load(BASE/'07_실행도구/근거주장_규격검사.py');r['context_sha256']=ev.context_hash(ec,c)
 x['review_contexts']=[{'review_ref':r['id'],'claim_ref':ref(c),'context_sha256':checker.context_hash(x,ref(c))}]
def cases(checker):
 out=[]
 def add(name,expected,edit=lambda x:None,needle=None):
  x=fixture();edit(x);out.append({'name':name,'expected':expected,'record':x,'needle':needle})
 def C(x):return x['spatial_contract']['evidence_contract']['claims'][0]
 def M(x):return C(x)['measurement']
 def G(x):return x['spatial_contract']['geometries'][0]
 add('4단위 세 규격 한맥 pin 정상','valid')
 add('schema_version 구형 직접통과 금지','invalid',lambda x:x.update(schema_version='0.1.0'))
 add('없는 원점 근거','invalid',lambda x:x['spatial_contract']['evidence_contract']['time_contract']['timelines'][0]['origin'].update(evidence_refs=['NONE']))
 add('원본PTS와재생시각모순','invalid',lambda x:x['spatial_contract']['evidence_contract']['time_contract']['frames'][0].update(source_pts='360000'))
 add('구간끝프레임 내부근거 금지','invalid',lambda x:x['spatial_contract']['evidence_contract']['time_contract']['frames'][0].update(source_pts='360000',actual=frac(3),requested=frac(3)))
 add('없는 공간 변환 참조','invalid',lambda x:x['spatial_contract']['mappings'][0]['transform_path'][0].update(id='NONE'))
 add('음수 해상도 금지','invalid',lambda x:x['spatial_contract']['spaces'][0].update(width=-1920))
 add('원본hash 변경 pin불일치','invalid',lambda x:x['spatial_contract']['evidence_contract']['materials'][0].update(sha256='f'*64))
 add('taxonomy 구형버전 금지','invalid',lambda x:x['catalog_refs']['taxonomy'].update(version='0.0.1'))
 add('한맥hash 위조 금지','invalid',lambda x:x['design']['profile_ref'].update(sha256='f'*64))
 add('없는 한맥 토큰 금지','invalid',lambda x:x['design']['palette_role_bindings'].update(background='NONE'))
 add('state 누락 금지','invalid',lambda x:x['units'].pop(2))
 add('state 중복 금지','invalid',lambda x:x['units'].append(copy.deepcopy(x['units'][2])))
 add('구간에 layout 오용 금지','invalid',lambda x:x['units'][1]['classifications'].append(copy.deepcopy(next(c for c in x['units'][2]['classifications'] if c['axis']=='layout'))))
 add('미검토 축 누락 금지','invalid',lambda x:x['units'][2]['classifications'].pop())
 add('unknown에분류태그혼용금지','invalid',lambda x:x['units'][2]['classifications'][0].update(state='unknown',term_ids=['PURPOSE-PROCESS']))
 add('unknown 정상 기권','valid',lambda x:x['units'][2]['classifications'][0].update(state='unknown',reason_codes=['ambiguous_visual_evidence']))
 add('other_candidate는 정본ID 없음','valid',lambda x:x['units'][2]['classifications'][0].update(state='other_candidate',reason_codes=['outside_vocabulary'],candidate_text='검토할 새 후보'))
 add('후보에정본ID발명금지','invalid',lambda x:x['units'][2]['classifications'][0].update(state='other_candidate',reason_codes=['outside_vocabulary'],candidate_text='후보',term_ids=['NEW-ID']))
 add('동작의 다른 종류 상태참조 금지','invalid',lambda x:x['units'][3].update(related_state_refs=[ref(x['spatial_contract']['evidence_contract']['targets'][0])] ))
 add('상태표본 없는프레임 금지','invalid',lambda x:x['units'][2].update(sample_frame_refs=['NONE']))
 add('메타에좌표 승인숨기기금지','invalid',lambda x:x['asset_metadata'].update(width=-1,approved=True))
 add('임의실행로그 금지','invalid',lambda x:x.update(run={'approved':True}))
 add('run 미작성은보존','unresolved',lambda x:x.update(run=None))
 add('미실행에실행완료시각금지','invalid',lambda x:x['run'].update(ended_at='2026-10-15T01:00:00Z'))
 add('출력다른버전금지','invalid',lambda x:x['run'].update(status='declared_completed',started_at='2026-10-15T00:00:00Z',ended_at='2026-10-15T01:00:00Z',output_record_ref={'id':x['record_id'],'version':'0.0.1'}))
 add('실행종료역전금지','invalid',lambda x:x['run'].update(status='declared_completed',started_at='2026-10-15T02:00:00Z',ended_at='2026-10-15T01:00:00Z',output_record_ref={'id':x['record_id'],'version':x['version']}))
 add('단일좌표성분 연결 정상','valid',measured)
 add('좌표연결누락 금지','invalid',lambda x:(measured(x),x.update(coordinate_bindings=[])))
 add('좌표연결중복 금지','invalid',lambda x:(measured(x),x['coordinate_bindings'].append(copy.deepcopy(x['coordinate_bindings'][0]))))
 add('표본값 좌표성분 불일치','invalid',lambda x:(measured(x),M(x)['samples'][0].update(value=301),M(x).update(value=301)))
 add('측정결과 표본 불일치','invalid',lambda x:(measured(x),M(x).update(value=1000)))
 add('위치량 y성분 오용','invalid',lambda x:(measured(x),x['coordinate_bindings'][0].update(component='y')))
 add('표본 공간없는ID금지','invalid',lambda x:(measured(x),M(x)['samples'][0].update(coordinate_space_ref='NONE')))
 add('좌표연결모델위치는미관측','unresolved',lambda x:(measured(x),G(x).update(role='model_position')))
 add('오차미상 자동확정금지','unresolved',lambda x:(measured(x),G(x).update(uncertainty={'kind':'unknown','x':None,'y':None,'width':None,'height':None})))
 add('반올림미지정자리수금지','invalid',lambda x:(measured(x),x['coordinate_bindings'][0]['numeric_encoding'].update(mode='rounded_decimal')))
 add('명시된반올림 정수 양성','valid',lambda x:(measured(x),x['coordinate_bindings'][0]['numeric_encoding'].update(mode='rounded_decimal',decimal_places=2)))
 add('통합검수context 정상','valid',lambda x:review(x,checker))
 add('좌표변경후context stale','unresolved',lambda x:(review(x,checker),x['spatial_contract']['geometries'][0].update(limitations='검수후한계변경')))
 add('분류변경후context stale','unresolved',lambda x:(review(x,checker),x['units'][0]['classifications'][0].update(note='검수후수정')))
 add('실행변경후context stale','unresolved',lambda x:(review(x,checker),x['run'].update(limitations='검수후수정')))
 add('구형receipt context없이이전금지','invalid',lambda x:(review(x,checker),x.update(review_contexts=[])))
 add('NaN 금지','invalid',lambda x:(measured(x),M(x).update(value=float('nan'))))
 add('surrogate key예외없이거부','invalid',lambda x:x.update({chr(0xD800):'bad'}))
 add('sample_index bool금지','invalid',lambda x:(measured(x),x['coordinate_bindings'][0].update(sample_index=True)))
 def no_spatial(x):
  x['spatial_contract'].update(spaces=[],transforms=[],geometries=[],mappings=[])
 add('좌표미기록영상은빈공간허용','valid',no_spatial)
 add('RFC3339 소문자t/z 허용','valid',lambda x:x['run'].update(status='declared_completed',started_at='2026-10-15t00:00:00z',ended_at='2026-10-15T01:00:00Z',output_record_ref={'id':x['record_id'],'version':x['version']}))
 def planned_cut(x,second=1):
  ec=x['spatial_contract']['evidence_contract'];p=copy.deepcopy(next(p for p in ec['time_contract']['periods'] if p['id']=='EX-INSTANT'));p.update(id='P-CUT',start=frac(second));ec['time_contract']['periods'].append(p)
  x['cut_markers']=[{'id':'CUT-ONE','period_ref':p['id'],'basis':'planned','claim_ref':ref(ec['claims'][0]),'limitations':'가상 컷 계획 순간. 실제 관측 아님.'}]
 add('같은순간 계획컷은유지','valid',planned_cut)
 add('다른순간을컷근거로사용금지','invalid',lambda x:planned_cut(x,2))
 def observed_cut(x):
  planned_cut(x,2);ec=x['spatial_contract']['evidence_contract'];c=ec['claims'][0]
  c.update(support_mode='rendered_observation',aspect='temporal_change');c['scope'].update(target_ref=ref(ec['targets'][1]),period_ref='EX-SEGMENT',extent='continuous')
  e=copy.deepcopy(ec['evidence'][2]);e.update(id='EV-CUT-CLIP',material_ref={k:ec['materials'][0][k] for k in ['id','version','sha256']},target_ref=ref(ec['targets'][1]));e['selector']={'kind':'clip','frame_ref':None,'period_ref':'EX-SEGMENT','exact':None,'start':None,'end':None};ec['evidence'].append(e);c['evidence_links']=[{'ref':ref(e),'role':'support'}];x['cut_markers'][0]['basis']='observed'
 add('포함범위clip의시간변화 컷양성','valid',observed_cut)
 add('단일정지프레임을관측컷으로승격금지','invalid',lambda x:(planned_cut(x),C(x).update(support_mode='rendered_observation'),x['cut_markers'][0].update(basis='observed')))
 def cross_state(x,beat_kind,beat_start,beat_end,state_kind,state_start,state_end):
  ec=x['spatial_contract']['evidence_contract'];tr=ec['time_contract'];state=copy.deepcopy(ec['targets'][2]);state.update(id='TG-STATE-2',period_ref='P-STATE-2');ec['targets'].append(state)
  for id,kind,start,end in [('P-BEAT',beat_kind,beat_start,beat_end),('P-STATE-2',state_kind,state_start,state_end)]:
   tr['periods'].append({'id':id,'timeline_ref':'EX-TIME','parent_ref':'EX-SEGMENT','kind':kind,'start':frac(start),'end':None if end is None else frac(end),'uncertainty':frac(0),'unknown_reason':None})
  ec['targets'][-2]['period_ref']='P-BEAT';x['units'][3]['related_state_refs']=[ref(state)];unit=copy.deepcopy(x['units'][2]);unit.update(target_ref=ref(state),sample_frame_refs=[]);x['units'].append(unit)
 add('서로다른순간상태동작거부','invalid',lambda x:cross_state(x,'instant',1,None,'instant',2,None))
 add('동작구간내순간상태양성','valid',lambda x:cross_state(x,'range',0,3,'instant',2,None))
 add('상태구간시작동작순간양성','valid',lambda x:cross_state(x,'instant',1,None,'range',1,2))
 add('상태구간제외끝점동작순간거부','invalid',lambda x:cross_state(x,'instant',2,None,'range',1,2))
 add('같은순간상태동작양성','valid',lambda x:cross_state(x,'instant',1,None,'instant',1,None))
 def mapped(x):
  measured(x);m=M(x);m['samples'][0].update(value=100,coordinate_space_ref=x['spatial_contract']['geometries'][1]['space_ref']['id']);m['value']=100;x['coordinate_bindings'][0]['mapping_ref']={'id':'MAP-ONE','version':'0.1.0'}
 add('mapping성분 연결 양성','valid',mapped)
 add('mapping원본오차 결과0으로숨기기보류','unresolved',lambda x:(mapped(x),G(x)['uncertainty'].update(x=frac(1))))
 add('mapping모델원본 관측승격보류','unresolved',lambda x:(mapped(x),G(x).update(role='model_position')))
 add('mapping중간공간 메타미상보류','unresolved',lambda x:(mapped(x),x['spatial_contract']['spaces'][1].update(sample_aspect_ratio=None)))
 return out
def run(checker,schema):
 results=[]
 for case in cases(checker):
  data=case['record'];before=json.dumps(data,ensure_ascii=True,sort_keys=True);exc=None
  try:r=checker.validate(data,schema)
  except Exception as e:r=None;exc=type(e).__name__+': '+str(e)
  ok=r is not None and ((not r['valid']) if case['expected']=='invalid' else r['valid'])
  if ok and case['expected']=='valid':ok=not r['unresolved']
  if ok and case['expected']=='unresolved':ok=bool(r['unresolved'])
  if ok:ok=all(r[k] is False for k in ['fact_verified','human_identity_verified','company_approved','operational_release'])
  unchanged=before==json.dumps(data,ensure_ascii=True,sort_keys=True);ok=bool(ok and unchanged)
  results.append({'name':case['name'],'expected':case['expected'],'passed':ok,'errors':r['errors'] if r else [],'unresolved':r['unresolved'] if r else [],'exception':exc,'input_unchanged':unchanged})
 return {'count':len(results),'passed':sum(r['passed'] for r in results),'all_passed':all(r['passed'] for r in results),'scope':'합성 통합 계약. 실제 영상/추적/사람검수/회사승인 아님.','cases':results}
if __name__=='__main__':
 c=load(BASE/'07_실행도구/통합기록_규격검사.py');r=run(c,read('04_기록규격/통합최소기록_스키마_v0.2.json'));print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(0 if r['all_passed'] else 1)
