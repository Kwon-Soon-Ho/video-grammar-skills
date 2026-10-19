"""R4-3 선언한 기하의 계약 검사. 영상변환/추출/추적/사실승인을 수행하지 않는다."""
import json,math,importlib.util
from pathlib import Path
from fractions import Fraction as F
from jsonschema import Draft202012Validator
BASE=Path(__file__).resolve().parents[1]
def q(v):return None if v is None else F(v['num'],v['den'])
def jq(v):return None if v is None else {'num':v.numerator,'den':v.denominator}
def load(p):
 s=importlib.util.spec_from_file_location('sp_dep',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def apply(m,g):
 a,b,c,d,e,f=m;x,y,w,h=g
 if w is None:return (a*x+c*y+e,b*x+d*y+f,None,None)
 pts=[(a*u+c*v+e,b*u+d*v+f) for u,v in [(x,y),(x+w,y),(x,y+h),(x+w,y+h)]]
 xs,ys=zip(*pts);return min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)
def inverse(m):
 a,b,c,d,e,f=m;det=a*d-b*c
 if det==0:raise ValueError('특이행렬')
 return d/det,-b/det,-c/det,a/det,(c*f-d*e)/det,(b*e-a*f)/det
def clip(g,w,h):
 if g is None:return None
 x,y,bw,bh=g
 if bw is None:return g if 0<=x<w and 0<=y<h else None
 a,b=max(F(0),x),max(F(0),y);c,d=min(w,x+bw),min(h,y+bh)
 return None if c<=a or d<=b else (a,b,c-a,d-b)
def validate(data,schema=None):
 if schema is None:schema=json.loads((BASE/'04_기록규격/좌표변환_스키마.json').read_text(encoding='utf-8'))
 Draft202012Validator.check_schema(schema);errors=[];pending=[];results=[];human=[]
 def err(id,msg):errors.append(str(id).encode('utf-8','backslashreplace').decode()+': '+msg)
 def wait(id,msg):pending.append(str(id)+': '+msg)
 def walk(v,path='record'):
  if isinstance(v,str):
   try:v.encode('utf-8')
   except UnicodeEncodeError:err(path,'UTF8 surrogate 금지')
  elif isinstance(v,float) and not math.isfinite(v):err(path,'NaN/Infinity 금지')
  elif isinstance(v,dict):
   for k,x in v.items():
    if not isinstance(k,str):err(path,'JSON key 문자열 필요');continue
    if isinstance(x,(int,float)) and k in ['num','den','width','height','clockwise_degrees','x','y'] and type(x) is not int:err(path,'원본 정수 타입 필요')
    walk(k,path+'.key');walk(x,path+'.'+k.encode('utf-8','backslashreplace').decode())
  elif isinstance(v,list):
   for x in v:walk(x,path)
 def output():return {'valid':not errors,'errors':errors,'unresolved':list(dict.fromkeys(pending)),'mapping_results':results,'human_review_queue':human,'fact_verified':False,'operational_release':False,'company_approved':False}
 walk(data)
 if errors:return output()
 for e in Draft202012Validator(schema).iter_errors(data):err(str(list(e.path)),e.message[:400])
 if errors:return output()
 ec=data['evidence_contract'];evmod=load(BASE/'07_실행도구/근거주장_규격검사.py');er=evmod.validate(ec,schema['properties']['evidence_contract'])
 if not er['valid']:errors.extend('evidence: '+v for v in er['errors']);return output()
 pending.extend('evidence: '+v for v in er['unresolved']);human.extend(er['human_review_queue'])
 mats={v['id']:v for v in ec['materials']};evs={v['id']:v for v in ec['evidence']};targets={v['id']:v for v in ec['targets']};frames={v['id']:v for v in ec['time_contract']['frames']}
 spaces={v['id']:v for v in data['spaces']};trans={v['id']:v for v in data['transforms']};geoms={v['id']:v for v in data['geometries']}
 ids=[v['id'] for k in ['spaces','transforms','geometries','mappings'] for v in data[k]]
 if len(ids)!=len(set(ids)):err('record','공간 ID 중복')
 def ref(r,table,id,hashed=False):
  v=table.get(r['id'])
  if v is None:err(id,'없는 참조 '+r['id']);return None
  if r['version']!=v['version'] or (hashed and r['sha256']!=v['sha256']):err(id,'참조 버전/hash 불일치');return None
  return v
 def same_frame(a,b):
  if a==b:return True
  f,g=frames.get(a),frames.get(b)
  if not f or not g:return False
  if any(v['mapping_state']!='mapped' or v['pts_kind']!='original_pts' or v['source_frame_ordinal'] is None for v in [f,g]):return None
  return (f['timeline_ref'],f['source_frame_ordinal'],f['source_pts'],q(f['time_base']))==(g['timeline_ref'],g['source_frame_ordinal'],g['source_pts'],q(g['time_base']))
 material_spaces=[]
 for s in spaces.values():
  id=s['id'];m=ref(s['material_ref'],mats,id,True)
  material_spaces.append((s['material_ref']['id'],s['frame_ref']))
  if not m or m['kind']!='frame' or m['frame_ref']!=s['frame_ref']:err(id,'공간은 해당 frame 자료에 연결')
  if (s['width'] is None)!=(s['height'] is None):err(id,'해상도 반쪽 입력 금지')
  if s['width'] is None:wait(id,'해상도 미확인')
  if s['sample_aspect_ratio'] is None:wait(id,'픽셀 종횡비 미확인')
  elif q(s['sample_aspect_ratio'])<=0:err(id,'양수 픽셀 종횡비 필요')
  r=s['rotation_metadata']
  if r['clockwise_degrees'] is None or r['applied'] is None:wait(id,'표시회전 메타/적용여부 미확인')
  if m and m['availability']!='present':wait(id,'자료 접근 미확인')
  human.append({'item_id':id,'status':'specimen_only' if ec['record_purpose']=='spec_test' else 'awaiting_human','reason':'해상도·SAR·회전메타/적용 여부가 원본 이미지/도구 기록과 맞는지 사용자 또는 지정 담당자 검수','verified':False})
 if len(material_spaces)!=len(set(material_spaces)):err('record','동일 frame 자료의 중복 raster 공간 금지')
 if errors:return output()
 incoming={};matrices={}
 for t in trans.values():
  id=t['id'];s=ref(t['from_ref'],spaces,id);d=ref(t['to_ref'],spaces,id);p=t['params'];kind=t['kind']
  if not s or not d:continue
  if s['id']==d['id']:err(id,'자기 변환 금지')
  if d['id'] in incoming:err(id,'도착 공간의 중복 변환 경로')
  incoming[d['id']]=s['id']
  dm=mats.get(d['material_ref']['id'])
  if dm and dm['parent_ref']!=s['material_ref']:err(id,'변환 자료의 직접 원본 pin 불일치')
  sf=same_frame(s['frame_ref'],d['frame_ref'])
  if sf is False:err(id,'공간 변환으로 원본 시간/frame identity 변경 금지')
  elif sf is None:wait(id,'frame 별칭 identity 미확인')
  for e in t['evidence_refs']:ref(e,evs,id)
  if not t['evidence_refs']:wait(id,'변환 방법 근거 미확보')
  human.append({'item_id':id,'status':'specimen_only' if ec['record_purpose']=='spec_test' else 'awaiting_human','reason':'effective 변환 수치·적용 순서·근거 내용·회전/SAR 정책을 지정 담당자가 검수','verified':False})
  if kind=='unknown':wait(id,'미지원/미확인 변환');matrices[id]=None;continue
  if None in [s['width'],s['height'],d['width'],d['height']]:wait(id,'해상도 없어 변환 계산 불가');matrices[id]=None;continue
  w,h=F(s['width']),F(s['height']);dw,dh=F(d['width']),F(d['height']);sar=q(s['sample_aspect_ratio']);expected_sar=sar;meta=dict(s['rotation_metadata'])
  if kind=='crop':
   if p['x']+p['width']>w or p['y']+p['height']>h:err(id,'크롭이 원본 범위 밖')
   size=(p['width'],p['height']);m=(F(1),F(0),F(0),F(1),F(-p['x']),F(-p['y']))
  elif kind=='rotate':
   deg=p['clockwise_degrees'];size=(h,w) if deg in [90,270] else (w,h)
   m={90:(0,1,-1,0,h,0),180:(-1,0,0,-1,w,h),270:(0,-1,1,0,0,w)}[deg];m=tuple(F(v) for v in m)
   if deg in [90,270] and sar is not None:expected_sar=1/sar
   if p['reason']=='display_orientation':
    if meta['applied'] is True:err(id,'표시회전 중복 적용 금지')
    elif meta['applied'] is None or meta['clockwise_degrees'] is None:wait(id,'표시회전 적용 근거 미확인')
    elif meta['clockwise_degrees']!=deg:err(id,'표시회전 보정 방향/각도 불일치')
    meta['applied']=True
  elif kind=='resize':
   size=(p['width'],p['height']);m=(dw/w,0,0,dh/h,0,0);m=tuple(F(v) for v in m)
   if p['aspect_policy']=='preserve_display_aspect':expected_sar=None if sar is None else sar*w*dh/(h*dw)
   elif p['aspect_policy']=='square_pixels':
    expected_sar=F(1)
    if sar is None:wait(id,'정방픽셀 보정의 원본 SAR 미확인')
   if p['aspect_policy']!='preserve_display_aspect':
    if sar is not None and expected_sar is not None and w*sar/h!=dw*expected_sar/dh and not p['allow_distortion']:err(id,'비율 왜곡 허용 표시 필요')
   if p['resampling']=='unknown':wait(id,'리샘플링 방법 미확인')
  else:
   size=(p['width'],p['height']);m=(F(1),F(0),F(0),F(1),F(p['x']),F(p['y']))
   if p['x']+w>dw or p['y']+h>dh:err(id,'패딩 canvas보다 원본/offset이 큼')
  if (dw,dh)!=size:err(id,'변환 후 해상도 불일치')
  actual_sar=q(d['sample_aspect_ratio'])
  if actual_sar is None or expected_sar is None:wait(id,'SAR 보존/변환 관계 미확인 — 알려진 값으로 미상을 덮어쓰지 않음')
  elif actual_sar!=expected_sar:err(id,'변환 후 픽셀 종횡비 불일치')
  for k in ['clockwise_degrees','applied']:
   actual=d['rotation_metadata'][k];expected=meta[k]
   if actual is None or expected is None:wait(id,'회전 메타 적용 관계 미확인 — 미상 값을 추정하지 않음')
   elif actual!=expected:err(id,'회전 메타 적용 상태 불일치')
  matrices[id]=m
 for id in incoming:
  seen=set();n=id
  while n in incoming:
   if n in seen:err(id,'공간 변환 순환');break
   seen.add(n);n=incoming[n]
 if errors:return output()
 def pixels(g,s):
  v=g['coordinates'];values=tuple(q(v[k]) for k in ['x','y','width','height'])
  if g['unit']=='normalized':
   if s['width'] is None:return None
   return tuple(v*(s['width'] if i%2==0 else s['height']) if v is not None else None for i,v in enumerate(values))
  return values
 for g in geoms.values():
  id=g['id'];s=ref(g['space_ref'],spaces,id);e=ref(g['evidence_ref'],evs,id);ref(g['target_ref'],targets,id)
  human.append({'item_id':id,'status':'specimen_only' if ec['record_purpose']=='spec_test' else 'awaiting_human','reason':'대상·앵커·가림·ROI/모델 구분·오차 근거의 내용 검수. 계산 통과를 실측 확인으로 승격하지 않음','verified':False})
  if not s:continue
  if g['frame_ref']!=s['frame_ref']:err(id,'geometry frame과 공간 frame 불일치')
  if e and (e['material_ref']!=s['material_ref'] or e['selector']['kind']!='frame' or e['selector']['frame_ref']!=g['frame_ref']):err(id,'geometry의 해당 이미지 frame 근거 필요')
  if e and e['target_ref']!=g['target_ref']:err(id,'geometry 대상과 근거 대상 불일치')
  v=pixels(g,s);u=g['uncertainty']
  if g['kind']=='point':
   if any(g['coordinates'][k] is not None for k in ['width','height']) or g['anchor']=='bounds':err(id,'point 폭/높이/box anchor 혼용 금지');continue
  elif g['anchor']!='bounds' or any(g['coordinates'][k] is None or q(g['coordinates'][k])<=0 for k in ['width','height']):err(id,'box의 양수 폭/높이와 bounds anchor 필요');continue
  if u['kind']=='unknown':
   if any(u[k] is not None for k in ['x','y','width','height']):err(id,'미상 오차는 null')
   wait(id,'공간 오차 미확인')
  else:
   required=['x','y']+(['width','height'] if g['kind']=='box' else [])
   if any(u[k] is None or q(u[k])<0 for k in required):err(id,'동일단위의 0이상 공간 오차 필요')
   if g['kind']=='point' and (u['width'] is not None or u['height'] is not None):err(id,'point 오차의 width/height는 null')
  if v is None:wait(id,'단위 변환 해상도 미확인');continue
  if g['anchor']=='pixel_center' and any((a-F(1,2)).denominator!=1 for a in v[:2]):err(id,'pixel_center는 반픽셀 중심 좌표')
  if s['width'] is not None and g['role']=='roi' and clip(v,s['width'],s['height'])!=v:err(id,'ROI 이미지 범위 밖')
 if errors:return output()
 for query in data['mappings']:
  id=query['id'];g=ref(query['source_ref'],geoms,id);dest=ref(query['target_space_ref'],spaces,id)
  if not g or not dest:continue
  u=g['uncertainty']
  if u['kind']=='unknown' or any(q(u[k]) not in [None,F(0)] for k in ['x','y','width','height']):
   wait(id,'오차 전파/잘림 경계는 별도 검수 — 명목 visibility를 실제 부재/존재로 확정 안 함')
   human.append({'item_id':id,'status':'specimen_only' if ec['record_purpose']=='spec_test' else 'awaiting_human','reason':'outside/null 결과도 오차가 경계를 넘는지 검수. 미상/비영 오차는 자동 판정 금지','verified':False})
  s=spaces[g['space_ref']['id']];full=pixels(g,s);visible=None if full is None or s['width'] is None else clip(full,s['width'],s['height']);current=s;known=full is not None and s['width'] is not None;loss=False;resampled=False
  used=set()
  for p in query['transform_path']:
   t=ref(p,trans,id)
   if not t:known=False;continue
   if t['id'] in used:err(id,'중복 경로 변환');known=False
   used.add(t['id']);rev=query['direction']=='reverse';fr=t['to_ref'] if rev else t['from_ref'];to=t['from_ref'] if rev else t['to_ref']
   if current['id']!=fr['id']:err(id,'변환 경로 순서/연결 불일치');known=False
   current=spaces.get(to['id'],current);m=matrices.get(t['id']);loss=loss or t['kind']=='crop';resampled=resampled or t['kind']=='resize'
   if m is None or not known:known=False;continue
   if rev:m=inverse(m)
   full=apply(m,full);visible=None if visible is None else apply(m,visible)
   visible=clip(visible,current['width'],current['height'])
  if current['id']!=dest['id']:err(id,'경로 도착 공간 불일치')
  r=ref(query['result_ref'],geoms,id) if query['result_ref'] else None
  if not known:
   wait(id,'경로/해상도 미확인 — 좌표 결과 인정 불가')
   if query['declared_visibility']!='unknown' or r is not None:err(id,'미확인 변환은 unknown/null 결과로 보존')
   results.append({'id':id,'formula_checked':False});continue
  visibility='outside' if visible is None else 'visible' if visible==full else 'partial'
  expected=full if query['policy']=='unclipped_geometry' else visible
  if query['declared_visibility']!=visibility:err(id,'관측 가능 영역 visibility 불일치')
  if expected is None:
   if r is not None:err(id,'크롭/패딩 밖에 관측 ROI 생성 금지')
  elif r is None:err(id,'계산 가능한 결과 geometry 누락')
  else:
   if r['space_ref']!=query['target_space_ref'] or r['target_ref']!=g['target_ref'] or same_frame(g['frame_ref'],r['frame_ref']) is False:err(id,'결과 공간/대상/frame 불일치')
   if r['kind']!=g['kind'] or pixels(r,dest)!=expected:err(id,'변환 계산 좌표 불일치')
   if query['policy']=='visible_fragment' and r['role']!='roi':err(id,'관측 부분은 ROI로 구분')
   if query['policy']=='unclipped_geometry' and (g['role']=='model_position' or visibility!='visible') and r['role']!='model_position':err(id,'미관측/모델 전체기하를 ROI로 승격 금지')
  results.append({'id':id,'formula_checked':True,'visibility':visibility,'visibility_basis':'nominal_geometry_only','uncertainty_verified':False,'spatial_clipping_possible':loss,'pixel_resampling':resampled,'inverse_restores_pixels':False})
 return output()
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('record',type=Path);a=p.parse_args();r=validate(json.loads(a.record.read_text(encoding='utf-8')));print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(0 if r['valid'] else 1)
