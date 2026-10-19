"""R4-4 통합 선언 계약 검사. 미디어·API·AE 접근과 사람/회사 승인을 수행하지 않는다."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext,ROUND_HALF_EVEN
from datetime import datetime
import json,hashlib,importlib.util,math
from jsonschema import Draft202012Validator,FormatChecker
BASE=Path(__file__).resolve().parents[1]
def load(p):
 s=importlib.util.spec_from_file_location('integration_dep',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def read(p):return json.loads((BASE/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256((BASE/p).read_bytes()).hexdigest()
def q(v):return None if v is None else F(v['num'],v['den'])
def pin(v):return {k:v[k] for k in ['id','version','sha256']}
def ref(v):return {k:v[k] for k in ['id','version']}
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')).hexdigest()
CONTEXT_FILES=['04_기록규격/통합최소기록_스키마_v0.2.json','04_기록규격/좌표변환_스키마.json','04_기록규격/근거주장_스키마.json','04_기록규격/시간프레임_스키마.json','07_실행도구/통합기록_규격검사.py','07_실행도구/좌표변환_규격검사.py','07_실행도구/근거주장_규격검사.py','07_실행도구/시간프레임_규격검사.py','01_공통용어/분류운영규칙.json']
def context_hash(data,claim_ref):
 payload={k:v for k,v in data.items() if k!='review_contexts'}
 payload['spatial_contract']=dict(payload['spatial_contract']);ec=dict(payload['spatial_contract']['evidence_contract']);payload['spatial_contract']['evidence_contract']=ec
 ec['review_records']=[{k:v for k,v in r.items() if k!='context_sha256'} for r in ec['review_records']]
 return digest({'record':payload,'claim_ref':claim_ref,'dependencies':{p:sha(p) for p in CONTEXT_FILES}})
def encode_matches(value,exact,encoding):
 if encoding['mode']=='exact_decimal':return encoding['decimal_places'] is None and F(str(value))==exact
 if encoding['decimal_places'] is None:return False
 with localcontext() as ctx:
  ctx.prec=120
  rounded=(Decimal(exact.numerator)/Decimal(exact.denominator)).quantize(Decimal(1).scaleb(-encoding['decimal_places']),rounding=ROUND_HALF_EVEN)
 return Decimal(str(value))==rounded
def validate(data,schema=None):
 if schema is None:schema=read('04_기록규격/통합최소기록_스키마_v0.2.json')
 errors=[];pending=[];queue=[];bindings=[];review_states=[]
 def err(id,msg):errors.append(str(id).encode('utf-8','backslashreplace').decode()+': '+msg)
 def wait(id,msg):pending.append(str(id)+': '+msg)
 def human(id,reason):queue.append({'item_id':id,'status':'specimen_only' if purpose=='spec_test' else 'awaiting_human','reason':reason,'verified':False})
 def output():return {'valid':not errors,'errors':errors,'unresolved':list(dict.fromkeys(pending)),'human_review_queue':queue,'coordinate_bindings':bindings,'integrated_review_states':review_states,'fact_verified':False,'human_identity_verified':False,'company_approved':False,'operational_release':False}
 def walk(v):
  if isinstance(v,str):
   try:v.encode('utf-8')
   except UnicodeEncodeError:err('record','UTF8 surrogate 금지')
  elif isinstance(v,float) and not math.isfinite(v):err('record','NaN/Infinity 금지')
  elif isinstance(v,dict):
   for k,x in v.items():
    if not isinstance(k,str):err('record','JSON key 문자열 필요');continue
    walk(k)
    if k in ['sample_index','decimal_places','num','den'] and isinstance(x,(float,bool)):err(k,'원본 정수 타입 필요')
    walk(x)
  elif isinstance(v,list):
   for x in v:walk(x)
 walk(data)
 if errors:return output()
 Draft202012Validator.check_schema(schema)
 for e in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(data):err(str(list(e.path)),e.message[:350])
 if errors:return output()
 for p,h in schema['x-dependency-hashes'].items():
  if sha(p)!=h:err('dependencies','규격/분류 정본 변경 — 통합 스키마 재검수 필요: '+p)
 if errors:return output()
 spatial=load(BASE/'07_실행도구/좌표변환_규격검사.py');sp=data['spatial_contract'];sr=spatial.validate(sp,schema['properties']['spatial_contract'])
 errors.extend('core: '+e for e in sr['errors']);pending.extend('core: '+p for p in sr['unresolved']);queue.extend(sr['human_review_queue'])
 if errors:return output()
 ec=sp['evidence_contract'];purpose=ec['record_purpose'];tr=ec['time_contract']
 mats={v['id']:v for v in ec['materials']};targets={v['id']:v for v in ec['targets']};claims={v['id']:v for v in ec['claims']};evs={v['id']:v for v in ec['evidence']};periods={v['id']:v for v in tr['periods']};frames={v['id']:v for v in tr['frames']};spaces={v['id']:v for v in sp['spaces']};geoms={v['id']:v for v in sp['geometries']};maps={v['id']:v for v in sp['mappings']}
 def resolve(r,table,id,hashed=False):
  v=table.get(r['id'])
  if not v:err(id,'없는 참조 '+r['id']);return None
  if r['version']!=v['version'] or hashed and r['sha256']!=v['sha256']:err(id,'참조 버전/hash 불일치');return None
  return v
 def contains(p,f):
  if not p or p['kind']=='unknown' or f['actual'] is None:return None
  if p['timeline_ref']!=f['timeline_ref']:return False
  t=q(f['actual']);return t==q(p['start']) if p['kind']=='instant' else q(p['start'])<=t<q(p['end'])
 def overlaps(a,b):
  if not a or not b or a['kind']=='unknown' or b['kind']=='unknown':return None
  if a['timeline_ref']!=b['timeline_ref']:return False
  if a['kind']=='instant':return contains(b,{'timeline_ref':a['timeline_ref'],'actual':a['start']})
  if b['kind']=='instant':return contains(a,{'timeline_ref':b['timeline_ref'],'actual':b['start']})
  return q(a['start'])<q(b['end']) and q(b['start'])<q(a['end'])
 taxonomy=read('01_공통용어/공통용어사전.json');design=read('03_한맥디자인/한맥디자인정본.json');rules=read('01_공통용어/분류운영규칙.json')
 expected={'taxonomy':{'id':taxonomy['taxonomy_id'],'version':taxonomy['version'],'sha256':sha('01_공통용어/공통용어사전.json')},'design_profile':{'id':design['profile_id'],'version':design['version'],'sha256':sha('03_한맥디자인/한맥디자인정본.json')},'classification_rules':{'path':'01_공통용어/분류운영규칙.json','sha256':sha('01_공통용어/분류운영규칙.json')}}
 if data['catalog_refs']!=expected:err('catalog_refs','현행 용어/한맥/분류 규칙 pin 불일치')
 if data['design']['profile_ref']!=expected['design_profile']:err('design','한맥 프로필 pin 불일치')
 colors={v['id']:v for v in design['color_tokens']};styles={v['id'] for v in design['references']+design['gradients']}
 for id in data['design']['palette_role_bindings'].values():
  if id not in colors or colors[id]['scope']!='global_color_library':err('design','없는 전역 한맥 토큰 또는 선택 alpha 오용')
 if len(set(data['design']['optional_style_refs']))!=len(data['design']['optional_style_refs']):err('design','선택 스타일 중복')
 if any(id not in styles for id in data['design']['optional_style_refs']):err('design','없는 선택 스타일')
 if data['design']['palette_role_bindings'] or data['design']['project_overrides']:human('design','토큰 역할·적용 목적·프로젝트 예외 검수. 영상 필수 회사 규칙 승인과 구분')
 root_targets=[v for v in targets.values() if v['unit']=='asset']
 if len(root_targets)!=1:err('units','현재 원본 영상 전체 대상은 하나만 허용')
 unit_ids=[v['target_ref']['id'] for v in data['units']];wanted={v['id'] for v in targets.values() if v['unit'] in ['asset','segment','screen_state','beat']}
 if len(set(unit_ids))!=len(unit_ids) or set(unit_ids)!=wanted:err('units','4단위 대상은 빠짐/중복 없이 각각 한 번 연결')
 terms={v['id']:v for v in taxonomy['terms']};axes={v['id'] for v in taxonomy['axes']}
 for u in data['units']:
  id=u['target_ref']['id'];t=resolve(u['target_ref'],targets,id)
  if not t:continue
  unit='state' if t['unit']=='screen_state' else t['unit'];seen=[]
  if unit=='beat' and (not t['parent_ref'] or targets[t['parent_ref']['id']]['unit']!='segment'):err(id,'통합 beat 소속은 segment; 화면 상태는 related_state_refs로 교차 연결')
  for c in u['classifications']:
   axis=c['axis'];seen.append(axis)
   if axis not in axes or unit not in rules['axis_units'].get(axis,[]):err(id,'분류축을 적용할 수 없는 기록 단위')
   if len(set(c['term_ids']))!=len(c['term_ids']):err(id,'분류 용어 중복')
   if any(r not in rules['reason_codes'] for r in c['reason_codes']):err(id,'없는 분류 이유 코드')
   if c['state']=='classified':
    if not c['term_ids'] or c['candidate_text'] is not None or c['reason_codes']:err(id,'classified는 유효 용어만 사용')
    for term in c['term_ids']:
     if term not in terms or terms[term]['axis']!=axis or terms[term]['status']=='deprecated':err(id,'용어·축·활성 상태 불일치')
    if c['claim_ref'] is None or c['basis']=='not_assessed':err(id,'분류의 출처 주장/관측·계획·추론 구분 필요')
   else:
    if c['term_ids'] or not c['reason_codes']:err(id,'미분류 판정에는 빈 용어와 이유 필요')
    if (c['state']=='other_candidate')!=(c['candidate_text'] is not None):err(id,'후보 문구는 other_candidate에만 필수')
    if c['state']=='not_assessed' and c['basis']!='not_assessed':err(id,'미검토 판정의 출처는 not_assessed')
    required={'other_candidate':'outside_vocabulary','not_applicable':'not_applicable_to_scope','not_assessed':'not_assessed_yet'}
    if c['state'] in required and required[c['state']] not in c['reason_codes']:err(id,'판정 상태별 이유 코드 불일치')
    if c['state']=='unknown' and any(r in ['not_assessed_yet','not_applicable_to_scope','outside_vocabulary'] for r in c['reason_codes']):err(id,'unknown은 미검토/비적용/신규후보와 구분')
   if c['basis']=='not_assessed' and c['claim_ref'] is not None:err(id,'미검토 출처에 확인 주장 연결 금지')
   if c['claim_ref']:
    claim=resolve(c['claim_ref'],claims,id)
    if claim and claim['scope']['target_ref']!=u['target_ref']:err(id,'분류 주장 대상 범위 불일치 — 자동 상속 금지')
    if claim and c['basis']=='observation' and claim['support_mode'] not in ['rendered_observation','numerical_estimate']:err(id,'계획/가설을 관측 분류로 승격 금지')
    if claim and c['basis']=='plan' and claim['support_mode'] not in ['scenario_supported','not_observed_example']:err(id,'계획 분류에는 시나리오/미관측 설명 예 주장 필요')
    if claim and c['basis']=='inference' and claim['support_mode']!='hypothesis':err(id,'추론 분류는 가설 주장으로 구분')
   human(id+'/'+axis,'분류의 대상·근거 충분성·의미 검수. classified는 해당 출처에 대한 태그이며 관측/회사 승인 아님')
  if len(seen)!=len(set(seen)):err(id,'같은 단위의 분류축 중복')
  if set(seen)!={a for a,units in rules['axis_units'].items() if unit in units}:err(id,'단위별 허용축은 5판정으로 빠짐없이 명시')
  if u['sample_frame_refs'] and unit!='state':err(id,'화면 표본 프레임은 state에 연결')
  for fr in u['sample_frame_refs']:
   if fr not in frames:err(id,'없는 화면 표본 프레임');continue
   membership=contains(periods.get(t['period_ref']),frames[fr])
   if membership is False:err(id,'화면 표본이 상태 시간 밖')
   if membership is None:wait(id,'상태/표본 시간 소속 미확인')
  if len(set(u['sample_frame_refs']))!=len(u['sample_frame_refs']):err(id,'상태 표본 프레임 중복')
  if u['related_state_refs'] and unit!='beat':err(id,'상태 교차 참조는 beat에만 연결')
  if len({v['id'] for v in u['related_state_refs']})!=len(u['related_state_refs']):err(id,'관련 상태 중복')
  for r in u['related_state_refs']:
   state=resolve(r,targets,id)
   if state and (state['unit']!='screen_state' or state['parent_ref']!=t['parent_ref']):err(id,'관련 상태는 같은 설명 구간의 화면 상태')
   if state:
    a,b=periods.get(t['period_ref']),periods.get(state['period_ref'])
    related=overlaps(a,b)
    if related is False:err(id,'동작과 관련 상태의 시간이 겹치지 않음')
    if related is None:wait(id,'동작과 상태의 시간 겹침 미확인')
  if u['scenario_refs'] and unit not in ['asset','segment']:err(id,'시나리오 자료는 영상/설명 구간에 연결')
  for r in u['scenario_refs']:
   material=resolve(r,mats,id,True)
   if material and material['kind'] not in ['scenario','transcript','example_description']:err(id,'OCR/이미지를 시나리오 자료로 오용 금지')
  human(id,'설명 구간·화면 상태·동작의 의미 경계, 시나리오 연결, 프레임 표본의 충분성 검수')
 # 시간 메타의 근거 ID도 근거 정본에 연결한다.
 for tl in tr['timelines']:
  for eid in tl['duration_evidence_refs']+tl['origin']['evidence_refs']:
   if eid not in evs:err(tl['id'],'없는 원점/길이 근거')
 for cut in data['cut_markers']:
  c=resolve(cut['claim_ref'],claims,cut['id']);p=periods.get(cut['period_ref'])
  if not p or p['kind']!='instant':err(cut['id'],'컷 표식은 선언된 순간')
  if c and p and p['kind']=='instant':
   cp=periods.get(c['scope']['period_ref']) if c['scope']['period_ref'] else None
   membership=contains(cp,{'timeline_ref':p['timeline_ref'],'actual':p['start']})
   if membership is False:err(cut['id'],'컷 순간이 근거 주장 시간 범위 밖')
   if membership is None:wait(cut['id'],'컷 순간의 주장 시간 소속 미확인')
  if c and cut['basis']=='observed' and c['support_mode']!='rendered_observation':err(cut['id'],'계획/가설을 관측 컷으로 승격 금지')
  if c and cut['basis']=='observed' and c['aspect']!='temporal_change':err(cut['id'],'관측 컷에는 시간 변화 주장 필요 — 정지 프레임은 컷 증거 아님')
  if c and cut['basis']=='planned' and c['support_mode'] not in ['scenario_supported','not_observed_example']:err(cut['id'],'계획 컷 근거 구분 필요')
  human(cut['id'],'컷 발생/계획·시점·주장 범위의 내용 검수. 설명 구간 경계를 자동 생성하지 않음')
 if len({v['id'] for v in data['cut_markers']})!=len(data['cut_markers']):err('cut','컷 표식 ID 중복')
 meta=data['asset_metadata']
 for r in meta['evidence_refs']:resolve(r,evs,'asset_metadata')
 if any(meta[k] is not None for k in ['container','video_codec','language']) or meta['audio_presence']!='unknown':
  if not meta['evidence_refs']:wait('asset_metadata','메타 항목 출처 미확인')
  human('asset_metadata','원본 메타 기록과 내용 대조. 해상도/시간 정본은 spaces/time_contract에만 보관')
 run=data['run']
 if run is None:wait('run','작업 수행 기록 미작성 — 실제 자동분석 실행 증명 없음')
 else:
  for r in run['input_refs']:resolve(r,mats,'run',True)
  if run['output_record_ref'] is not None and run['output_record_ref']!={'id':data['record_id'],'version':data['version']}:err('run','실행 출력 기록 버전 불일치')
  if purpose=='spec_test' and run['mode']!='contract_test':err('run','합성 예의 작업 종류는 contract_test')
  if purpose=='draft_record' and run['mode']=='contract_test':err('run','합성시험 실행을 실제 기록에 승격 금지')
  if run['status']=='not_started' and (run['started_at'] or run['ended_at'] or run['output_record_ref']):err('run','미실행에 실행 시각/출력 선언 금지')
  if run['status']=='declared_completed' and (not run['started_at'] or not run['ended_at'] or not run['output_record_ref']):err('run','실행 완료 선언의 시각·출력 필요')
  if run['started_at'] and run['ended_at']:
   try:
    def instant(s):return datetime.fromisoformat(s.replace('t','T').replace('z','Z').replace('Z','+00:00'))
    if instant(run['ended_at'])<instant(run['started_at']):err('run','실행 종료가 시작보다 빠름')
   except ValueError:err('run','실행 시각은 지원하는 RFC3339 시점으로 해석할 수 있어야 함')
  if run['mode']=='automated_analysis' and run['status']=='declared_completed' and (not run['tool'] or not run['input_refs']):err('run','자동분석 실행 선언에 도구/버전·입력 pin 필요')
  human('run','실행 주체·도구/모델·입출력·설정과 실제 작업 로그를 대조. 선언을 실행 증명으로 보지 않음')
 # 좌표 표본은 새 geometry/변환을 실제로 해석한다. 상위 사람 검수 보류는 그대로 유지한다.
 incoming={v['to_ref']['id']:v for v in sp['transforms']}
 def basis(space):
  path=[];cur=space;seen=set()
  while cur['id'] in incoming:
   if cur['id'] in seen:return None
   seen.add(cur['id']);t=incoming[cur['id']]
   if t['kind']=='unknown':return None
   path.append({'kind':t['kind'],'params':t['params']});cur=spaces[t['from_ref']['id']]
  if cur['width'] is None or cur['sample_aspect_ratio'] is None or None in [cur['rotation_metadata']['clockwise_degrees'],cur['rotation_metadata']['applied']]:return None
  return digest({'root':{k:cur[k] for k in ['width','height','origin','axes','unit','sample_aspect_ratio','rotation_metadata']},'path':list(reversed(path))})
 used=[];groups={}
 for b in data['coordinate_bindings']:
  id=b['claim_ref']['id']+'/'+str(b['sample_index']);c=resolve(b['claim_ref'],claims,id);g=resolve(b['geometry_ref'],geoms,id);key=(b['claim_ref']['id'],b['sample_index']);used.append(key)
  if not c or not g:continue
  measure=c['measurement']
  if c['support_mode']!='numerical_estimate' or measure is None or b['sample_index']>=len(measure['samples']):err(id,'좌표 연결의 측정 주장/표본 없음');continue
  if measure['quantity'] not in ['position_x','position_y','width','height','average_speed','average_acceleration']:err(id,'비공간 측정에 좌표 연결 혼용 금지');continue
  sample=measure['samples'][b['sample_index']];geom=g;mapping=None;ok=True
  native_unc=g['uncertainty']
  if native_unc['kind']=='unknown' or any(q(native_unc[k]) not in [None,F(0)] for k in ['x','y','width','height']):wait(id,'원본 geometry 오차의 변환/측정 전파 미확인');ok=False
  if g['role']!='roi':wait(id,'원본 모델 좌표의 실제 관측 확인 필요');ok=False
  if g['evidence_ref']!=sample['evidence_ref'] or g['target_ref']!=sample['target_ref'] or g['frame_ref']!=sample['frame_ref']:err(id,'geometry의 표본 근거/대상/프레임 불일치')
  if b['mapping_ref']:
   mapping=maps.get(b['mapping_ref']['id'])
   if mapping is None:err(id,'없는 좌표 mapping 참조');continue
   # mapping은 R4-3에서 버전 필드가 없는 쿼리다. 통합에서는 core 계약 버전을 pin한다.
   if b['mapping_ref']['version']!=sp['contract_version']:err(id,'mapping 계약 버전 불일치')
   if mapping['source_ref']!=b['geometry_ref']:err(id,'mapping 입력 geometry 불일치')
   if mapping['result_ref'] is None:wait(id,'관측/변환 결과 없음');ok=False
   else:geom=geoms[mapping['result_ref']['id']]
   if mapping['declared_visibility']!='visible':wait(id,'잘림/밖/미상 표본을 전체 대상 측정으로 확정 금지');ok=False
   path_ids={v['id'] for v in mapping['transform_path']}
   for t in sp['transforms']:
    if t['id'] not in path_ids:continue
    for r in [t['from_ref'],t['to_ref']]:
     space=spaces[r['id']]
     if space['sample_aspect_ratio'] is None or None in [space['rotation_metadata']['clockwise_degrees'],space['rotation_metadata']['applied']]:wait(id,'변환 경로의 SAR/회전 상태 미확인');ok=False
  if sample['coordinate_space_ref']!=geom['space_ref']['id']:err(id,'표본 좌표 공간과 실제 geometry 공간 불일치')
  geometry_unit='px' if geom['unit']=='raster_px' else geom['unit']
  if measure['sample_unit']!=geometry_unit:err(id,'표본 단위와 geometry 단위 불일치')
  if geom['role']!='roi':wait(id,'모델 좌표는 실제 관측 위치로 확정 금지');ok=False
  if measure['quantity'] in ['position_x','position_y'] and b['component']!=measure['quantity'][-1]:err(id,'위치량/좌표 성분 불일치')
  if measure['quantity'] in ['width','height'] and b['component']!=measure['quantity']:err(id,'크기량/좌표 성분 불일치')
  value=geom['coordinates'][b['component']]
  if value is None:err(id,'point에 없는 box 성분 사용');continue
  if not encode_matches(sample['value'],q(value),b['numeric_encoding']):err(id,'표본 값과 좌표 성분/명시 반올림 불일치')
  if b['numeric_encoding']['mode']=='exact_decimal' and b['numeric_encoding']['decimal_places'] is not None:err(id,'exact_decimal의 자리수는 null')
  u=geom['uncertainty']
  if u['kind']=='unknown' or any(q(u[k]) not in [None,F(0)] for k in ['x','y','width','height']):wait(id,'좌표 오차의 측정값 전파·경계는 사람 검수');ok=False
  base=basis(spaces[geom['space_ref']['id']])
  if base is None:wait(id,'프레임 비교 좌표 기준 미확인');ok=False
  groups.setdefault(c['id'],[]).append((b['component'],base))
  bindings.append({'claim_id':c['id'],'sample_index':b['sample_index'],'binding_status':'linked' if ok else 'unresolved','formula_result_verified':False,'observation_verified':False})
  human(id,'대상 추적·앵커/성분·단위·명시 반올림·좌표 기준·측정 계산식/결과·오차를 검수. 좌표 연결만 자동 검사')
 if len(used)!=len(set(used)):err('coordinate_bindings','동일 측정 표본의 좌표 연결 중복')
 needed={(c['id'],i) for c in claims.values() if c['measurement'] and c['measurement']['quantity'] in ['position_x','position_y','width','height','average_speed','average_acceleration'] for i in range(len(c['measurement']['samples']))}
 if set(used)!=needed:err('coordinate_bindings','공간 측정 표본은 누락/여분 없이 연결')
 for c in claims.values():
  m=c['measurement']
  if m is None:continue
  if m['method']=='single_sample_component' and m['quantity'] in ['position_x','position_y','width','height']:
   if len(m['samples'])!=1 or m['unit']!=m['sample_unit'] or F(str(m['value']))!=F(str(m['samples'][0]['value'])):err(c['id'],'단일 성분 측정의 결과/표본/단위 불일치')
  else:wait(c['id'],'측정 계산식·결과·오차는 별도 내용 검수 — 통합 단계는 자동 추적/수치 분석을 수행하지 않음')
 for id,values in groups.items():
  if len({v[0] for v in values})!=1:err(id,'한 축 스칼라 측정에 x/y/폭/높이 혼용 금지')
  if len({v[1] for v in values})!=1:wait(id,'서로 다른 프레임 좌표 기준 혼용 — 원본 기준으로 명시 변환 필요')
 # 구형 receipt만으로 통합 문맥을 확인했다고 재사용할 수 없다.
 bridges={v['review_ref']:v for v in data['review_contexts']};reviews={v['id']:v for v in ec['review_records']}
 if len(bridges)!=len(data['review_contexts']):err('review','통합 검수 context 중복')
 if set(bridges)!=set(reviews):err('review','모든 근거 검수 기록의 통합 context 연결 필요')
 for id,r in reviews.items():
  b=bridges.get(id)
  if not b:continue
  if b['claim_ref']!=r['claim_ref']:err(id,'통합 context 주장 버전 불일치')
  stale=b['context_sha256']!=context_hash(data,r['claim_ref'])
  review_states.append({'review_id':id,'state':'stale' if stale else 'declared_context_matches','human_identity_verified':False})
  if stale:wait(id,'시간/근거/좌표/분류/실행/규격 변경 — 통합 재검수 필요')
  human(id,'통합 context 연결 확인과 실제 검수자/행위 확인. R4-2 공간 supported 차단은 유지하고 R6/R7 권한·내용 검수에 인계')
 return output()
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('record',type=Path);a=p.parse_args();r=validate(json.loads(a.record.read_text(encoding='utf-8')))
 print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(0 if r['valid'] else 1)
