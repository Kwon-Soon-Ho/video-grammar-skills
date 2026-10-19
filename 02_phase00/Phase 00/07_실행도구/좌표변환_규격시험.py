from pathlib import Path
import json,copy,importlib.util
BASE=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
def load(p):
 s=importlib.util.spec_from_file_location('sp_mod',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def frac(n,d=1):return {'num':n,'den':d}
def ref(v):return {k:v[k] for k in ['id','version']}
def pin(v):return {k:v[k] for k in ['id','version','sha256']}
def fixture():
 ec=json.loads((BASE/'04_기록규격/근거주장_설명용기록.json').read_text(encoding='utf-8'))
 space={'id':'SP-ROOT','version':'0.1.0','material_ref':pin(ec['materials'][2]),'frame_ref':'EX-FRAME','width':1920,'height':1080,'origin':'upper_left_edge','axes':'x_right_y_down','unit':'raster_px','sample_aspect_ratio':frac(1),'rotation_metadata':{'clockwise_degrees':0,'applied':False,'note':'가상 메타 확인. 실제 원본 미검증.'},'limitations':'합성 선언·원본 영상/해상도/픽셀 미검증.'}
 geo={'id':'G-ROOT','version':'0.1.0','space_ref':ref(space),'frame_ref':'EX-FRAME','evidence_ref':ref(ec['evidence'][2]),'target_ref':ref(ec['targets'][-1]),'unit':'raster_px','kind':'point','role':'roi','anchor':'geometric_point','coordinates':{'x':frac(300),'y':frac(250),'width':None,'height':None},'uncertainty':{'kind':'absolute_bound','x':frac(0),'y':frac(0),'width':None,'height':None},'limitations':'가상 geometry. 내용 검수/실측 아님.'}
 x={'contract_version':'0.1.0','evidence_contract':ec,'spaces':[space],'transforms':[],'geometries':[geo],'mappings':[],'notes':'spec_test만 사용. 원본픽셀/사람검수/회사승인 아님.'}
 child(x,'SP-CROP',800,600,'crop',{'x':100,'y':50,'width':800,'height':600})
 child(x,'SP-RESIZE',400,300,'resize',{'width':400,'height':300,'aspect_policy':'preserve_sar','allow_distortion':False,'resampling':'bilinear'})
 result_geo(x,'G-RESULT',100,100)
 x['mappings']=[{'id':'MAP-ONE','source_ref':ref(geo),'result_ref':ref(x['geometries'][-1]),'target_space_ref':ref(x['spaces'][-1]),'direction':'forward','transform_path':[ref(t) for t in x['transforms']],'policy':'visible_fragment','declared_visibility':'visible','limitations':'宣言 기하만 비교하는 합성 예'.replace('宣言','선언')}]
 return x
def child(x,id,w,h,kind,params,parent=None):
 parent=parent or x['spaces'][-1];ec=x['evidence_contract'];m=copy.deepcopy(ec['materials'][2]);m.update(id='MAT-'+id,parent_ref=parent['material_ref'],sha256='2'*64,locator='fixture-only://'+id);ec['materials'].append(m)
 e=copy.deepcopy(ec['evidence'][2]);e.update(id='EV-'+id,material_ref=pin(m));ec['evidence'].append(e)
 s=copy.deepcopy(parent);s.update(id=id,material_ref=pin(m),width=w,height=h);x['spaces'].append(s)
 t={'id':'TR-'+id,'version':'0.1.0','from_ref':ref(parent),'to_ref':ref(s),'kind':kind,'params':params,'evidence_refs':[ref(ec['evidence'][0])],'limitations':'가상 정적 변환. 실제 픽셀 가공 아님.'};x['transforms'].append(t);return s
def result_geo(x,id,px,py,width=None,height=None,role='roi'):
 g=copy.deepcopy(x['geometries'][0]);s=x['spaces'][-1];g.update(id=id,space_ref=ref(s),evidence_ref=ref(x['evidence_contract']['evidence'][-1]),role=role)
 g['coordinates'].update(x=frac(px) if isinstance(px,int) else px,y=frac(py) if isinstance(py,int) else py,width=None if width is None else frac(width),height=None if height is None else frac(height))
 if width is not None:g.update(kind='box',anchor='bounds');g['uncertainty'].update(width=frac(0),height=frac(0))
 x['geometries'].append(g);return g
def cases():
 out=[]
 def add(name,kind,change,needle=None):
  x=fixture();change(x);out.append({'name':name,'kind':kind,'record':x,'expected_error_fragment':needle})
 def G(x):return x['geometries'][0]
 def R(x):return x['geometries'][1]
 def M(x):return x['mappings'][0]
 add('crop100,50→resize0.5の点100,100'.replace('の点',' 지점'),'valid',lambda x:None)
 add('原본offset누락'.replace('原본','원본'),'invalid',lambda x:R(x)['coordinates'].update(x=frac(150),y=frac(125)),'계산 좌표')
 add('정규화단위명시적환산','valid',lambda x:(G(x).update(unit='normalized'),G(x)['coordinates'].update(x=frac(5,32),y=frac(25,108))))
 add('정규화위치를원본px처럼쓰기','invalid',lambda x:G(x).update(unit='normalized'),'ROI 이미지 범위')
 add('기준원점center오용','invalid',lambda x:x['spaces'][0].update(origin='pixel_center'),'schema')
 add('width0거부','invalid',lambda x:x['spaces'][0].update(width=0),'schema')
 add('반쪽해상도거부','invalid',lambda x:x['spaces'][0].update(height=None),'반쪽')
 add('구형spaceversion거부','invalid',lambda x:G(x)['space_ref'].update(version='0.0.1'),'버전/hash')
 add('없는transform거부','invalid',lambda x:M(x)['transform_path'][0].update(id='NONE'),'없는 참조')
 add('경로순서뒤집기거부','invalid',lambda x:M(x)['transform_path'].reverse(),'경로 순서')
 add('경로중복거부','invalid',lambda x:M(x)['transform_path'].append(copy.deepcopy(M(x)['transform_path'][0])),'중복 경로')
 add('다른materialhash거부','invalid',lambda x:x['spaces'][0]['material_ref'].update(sha256='f'*64),'버전/hash')
 add('크롭범위초과거부','invalid',lambda x:x['transforms'][0]['params'].update(x=1500),'원본 범위')
 add('패딩으로원본밖물체되살리지않음','valid',lambda x:padding_outside(x))
 add('부모pin다름거부','invalid',lambda x:x['evidence_contract']['materials'][-1].update(parent_ref=pin(x['evidence_contract']['materials'][2])),'직접 원본')
 add('ROI끝점point는밖','invalid',lambda x:G(x)['coordinates'].update(x=frac(1920)),'ROI 이미지 범위')
 add('model좌표음수는보존','valid',lambda x:outside(x))
 add('밖의model좌표를ROI로오용','invalid',lambda x:(outside(x),G(x).update(role='roi')),'ROI 이미지 범위')
 add('모든화면box끝점허용','valid',lambda x:fullbox(x))
 add('point에boxwidth혼용예외없이거부','invalid',lambda x:G(x)['coordinates'].update(width=frac(1)),'point 폭')
 add('boxheight누락예외없이거부','invalid',lambda x:(G(x).update(kind='box',anchor='bounds'),G(x)['coordinates'].update(width=frac(1))),'양수 폭')
 add('pixel_center반픽셀잘못입력','invalid',lambda x:G(x).update(anchor='pixel_center'),'반픽셀')
 add('sourcepixelcenter리사이즈점은geometric','valid',lambda x:pixel_center(x))
 add('NaN거부','invalid',lambda x:G(x)['coordinates']['x'].update(num=float('nan')),'NaN')
 add('bool정수위장거부','invalid',lambda x:G(x)['coordinates']['x'].update(num=True),'정수 타입')
 add('surrogate문자거부','invalid',lambda x:x.update(notes=chr(0xD800)),'surrogate')
 add('기하오차미상은보존','unresolved',lambda x:G(x).update(uncertainty={'kind':'unknown','x':None,'y':None,'width':None,'height':None}))
 add('box오차전파아직사람검수','unresolved',lambda x:G(x)['uncertainty'].update(x=frac(1)))
 add('미지원변환숫자결과금지','invalid',lambda x:x['transforms'][0].update(kind='unknown',params={'reason':'perspective'}),'unknown/null')
 add('미지원변환미해결보존','unresolved',lambda x:(x['transforms'][0].update(kind='unknown',params={'reason':'perspective'}),M(x).update(result_ref=None,declared_visibility='unknown'),x['geometries'].pop()))
 for degree,px,py in [(90,830,300),(180,1620,830),(270,250,1620)]:
  add('clockwise'+str(degree)+'기하','valid',lambda x,d=degree,a=px,b=py:rotation(x,d,a,b))
 add('회전후해상도swap누락','invalid',lambda x:(rotation(x,90,830,300),x['spaces'][1].update(width=1920,height=1080)),'해상도 불일치')
 add('auto회전중복거부','invalid',lambda x:(rotation(x,90,830,300),x['spaces'][0]['rotation_metadata'].update(clockwise_degrees=90,applied=True),x['spaces'][1]['rotation_metadata'].update(clockwise_degrees=90,applied=True),x['transforms'][0]['params'].update(reason='display_orientation')),'중복 적용')
 add('inversecropoffset복구기하','valid',lambda x:reverse(x))
 add('resize왜곡허용누락','invalid',lambda x:(x['transforms'][1]['params'].update(width=400,height=400),x['spaces'][2].update(height=400)),'왜곡 허용')
 add('resize명시왜곡은수치기하보존','valid',lambda x:(x['transforms'][1]['params'].update(width=400,height=400,allow_distortion=True),x['spaces'][2].update(height=400),R(x)['coordinates'].update(y=frac(400,3))))
 add('SARunknown보존','unresolved',lambda x:[s.update(sample_aspect_ratio=None) for s in x['spaces']])
 add('SAR0거부','invalid',lambda x:x['spaces'][0].update(sample_aspect_ratio=frac(0)),'양수 픽셀')
 add('회전SAR0도예외없이거부','invalid',lambda x:(rotation(x,90,830,300),x['spaces'][0].update(sample_aspect_ratio=frac(0))),'양수 픽셀')
 add('outside결과null에도비영오차보류','unresolved',lambda x:(outside(x),G(x)['uncertainty'].update(x=frac(100))))
 def pad_model(x,role):
  padding_outside(x);r=result_geo(x,'G-PAD-MODEL',20,280,role=role);M(x).update(policy='unclipped_geometry',result_ref=ref(r))
 add('padding후model좌표를ROI로승격금지','invalid',lambda x:pad_model(x,'roi'),'ROI로 승격')
 add('padding후model좌표는보존','valid',lambda x:pad_model(x,'model_position'))
 add('원본SAR미상출력SAR알려진관계는미확인','unresolved',lambda x:x['spaces'][0].update(sample_aspect_ratio=None))
 add('목표SAR미상도추정대입금지','unresolved',lambda x:x['spaces'][-1].update(sample_aspect_ratio=None))
 add('알려진SAR모순은거부','invalid',lambda x:x['spaces'][1].update(sample_aspect_ratio=frac(2)),'픽셀 종횡비 불일치')
 add('회전후SAR역수','valid',lambda x:(rotation(x,90,830,300),x['spaces'][0].update(sample_aspect_ratio=frac(16,15)),x['spaces'][1].update(sample_aspect_ratio=frac(15,16))))
 add('DAR보존resize의SAR계산','valid',lambda x:(x['transforms'][1]['params'].update(height=400,aspect_policy='preserve_display_aspect'),x['spaces'][2].update(height=400,sample_aspect_ratio=frac(4,3)),R(x)['coordinates'].update(y=frac(400,3))))
 def square(x):
  [s.update(sample_aspect_ratio=frac(16,15)) for s in x['spaces']];x['transforms'][1]['params'].update(width=640,height=450,aspect_policy='square_pixels');x['spaces'][2].update(width=640,height=450,sample_aspect_ratio=frac(1));R(x)['coordinates'].update(x=frac(160),y=frac(150))
 add('비정방pixel→square보정resize','valid',square)
 add('원본회전미상출력회전알려진관계는미확인','unresolved',lambda x:x['spaces'][0]['rotation_metadata'].update(clockwise_degrees=None,applied=None))
 add('목표회전미상도추정대입금지','unresolved',lambda x:x['spaces'][-1]['rotation_metadata'].update(clockwise_degrees=None,applied=None))
 add('알려진회전상태모순은거부','invalid',lambda x:x['spaces'][1]['rotation_metadata'].update(applied=True),'회전 메타 적용 상태 불일치')
 return out
def stripped(x):x['spaces']=x['spaces'][:1];x['transforms']=[];x['geometries']=x['geometries'][:1];x['mappings']=[];x['evidence_contract']['materials']=x['evidence_contract']['materials'][:3];x['evidence_contract']['evidence']=x['evidence_contract']['evidence'][:3]
def rotation(x,degree,a,b):
 stripped(x);s=child(x,'SP-ROT',1080 if degree!=180 else 1920,1920 if degree!=180 else 1080,'rotate',{'clockwise_degrees':degree,'reason':'manual'});g=result_geo(x,'G-RESULT',a,b)
 x['mappings']=[{'id':'MAP-ONE','source_ref':ref(x['geometries'][0]),'result_ref':ref(g),'target_space_ref':ref(s),'direction':'forward','transform_path':[ref(x['transforms'][0])],'policy':'visible_fragment','declared_visibility':'visible','limitations':'가상 회전'}]
def reverse(x):
 m=x['mappings'][0];m.update(source_ref=ref(x['geometries'][1]),result_ref=ref(x['geometries'][0]),target_space_ref=ref(x['spaces'][0]),direction='reverse');m['transform_path'].reverse()
def outside(x):
 x['geometries'][0]['coordinates'].update(x=frac(-10));x['geometries'][0]['role']='model_position';x['geometries'].pop();x['mappings'][0].update(result_ref=None,declared_visibility='outside')
def fullbox(x):
 g=x['geometries'][0];g.update(kind='box',anchor='bounds');g['coordinates'].update(x=frac(0),y=frac(0),width=frac(1920),height=frac(1080));g['uncertainty'].update(width=frac(0),height=frac(0))
 r=x['geometries'][1];r.update(kind='box',anchor='bounds');r['coordinates'].update(x=frac(0),y=frac(0),width=frac(400),height=frac(300));r['uncertainty'].update(width=frac(0),height=frac(0));x['mappings'][0]['declared_visibility']='partial'
def pixel_center(x):
 g=x['geometries'][0];g.update(anchor='pixel_center');g['coordinates'].update(x=frac(601,2),y=frac(501,2));x['geometries'][1]['coordinates'].update(x=frac(401,4),y=frac(401,4))
def padding_outside(x):
 stripped(x);g=x['geometries'][0];g.update(role='model_position');g['coordinates'].update(x=frac(-10));s=child(x,'SP-PAD',2000,1200,'pad',{'x':30,'y':30,'width':2000,'height':1200})
 x['mappings']=[{'id':'MAP-ONE','source_ref':ref(g),'result_ref':None,'target_space_ref':ref(s),'direction':'forward','transform_path':[ref(x['transforms'][0])],'policy':'visible_fragment','declared_visibility':'outside','limitations':'원본밖물체를패딩색으로되살리지않음'}]
def run(checker,schema):
 results=[]
 for c in cases():
  try:r=checker.validate(c['record'],schema);exc=None
  except Exception as e:r=None;exc=type(e).__name__+': '+str(e)
  ok=r is not None and (r['valid'] if c['kind']!='invalid' else not r['valid'])
  if ok and c['kind']=='unresolved':ok=bool(r['unresolved'])
  if ok and c['kind']=='valid':ok=not r['unresolved']
  if ok and c['expected_error_fragment']:ok=bool(r['errors']) if c['expected_error_fragment']=='schema' else any(c['expected_error_fragment'] in e for e in r['errors'])
  if r:ok=ok and not r['fact_verified'] and not r['operational_release']
  results.append({k:v for k,v in c.items() if k!='record'}|{'passed':ok,'result':r,'exception':exc})
 return {'count':len(results),'passed':sum(bool(c['passed']) for c in results),'all_passed':all(c['passed'] for c in results),'scope':'합성 기하 계약만. 실제 픽셀 가공/사람검수/영상정확성 아님.','cases':results}
if __name__=='__main__':
 b=Path(__file__).resolve().parents[1];c=load(b/'07_실행도구/좌표변환_규격검사.py');s=json.loads((b/'04_기록규격/좌표변환_스키마.json').read_text(encoding='utf-8'));r=run(c,s);print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(0 if r['all_passed'] else 1)
