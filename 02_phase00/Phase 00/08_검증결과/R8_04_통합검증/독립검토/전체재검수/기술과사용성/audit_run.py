from pathlib import Path
import ast, copy, hashlib, importlib.util, json, os, re, shutil, subprocess, sys

D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
OUT=Path(__file__).resolve().parent
C=OUT.parents[1]/'R8_04_시험/고정문맥_검증전용/Phase00'
W=OUT/'isolated/Phase00'
PY=D/'.환경/Scripts/python.exe'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(path):
 spec=importlib.util.spec_from_file_location(path.stem,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def snapshot(base):return {p.relative_to(base).as_posix():sha(p) for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def reject_parse(module):
 try:module.parse(b'{"a":1,"a":2}')
 except ValueError as e:return str(e)
 return 'accepted'

if sys.argv[1:] == ['setup']:
 OUT.mkdir(parents=True,exist_ok=True)
 assert not W.exists()
 before=snapshot(C)
 shutil.copytree(C,W)
 copies=[]
 for folder in ['00_운영계약','01_공통용어','02_원칙과레이아웃','03_한맥디자인','04_기록규격','05_출처와검토','06_맞춤스킬','07_실행도구','09_다음단계인계','11_기록접수함','12_통합기록','13_품질검수','14_스킬재구성']:
  for p in (D/folder).rglob('*'):
   if p.is_file():
    rel=p.relative_to(D);dest=W/rel
    if not dest.exists() or sha(p)!=sha(dest):
     dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);copies.append(rel.as_posix())
 for f in ['00_시작안내.md','01_진행현황.md','02_운영규칙.md']:
  shutil.copy2(D/f,W/f);copies.append(f)
 for f in ['회사목록.json','자산목록.json','CI색상목록.json']:
  assert sha(W/'10_공용자산'/f)==sha(D/'10_공용자산'/f)
 safety=[]
 for p in sorted((D/'07_실행도구').glob('*.py')):
  text=p.read_text(encoding='utf-8-sig');tree=ast.parse(text)
  roots=[{'line':i,'text':s.strip()} for i,s in enumerate(text.splitlines(),1) if re.search(r'BASE\s*=|ROOT\s*=|default=.*parents|add_argument\(.--base',s)]
  writes=[]
  for node in ast.walk(tree):
   if isinstance(node,ast.Call):
    fn=ast.unparse(node.func)
    if any(k in fn for k in ['write_text','write_bytes','mkdir','unlink','rmtree','copy','rename','replace','open']):
     if fn.endswith('copy') or fn.endswith('deepcopy'):continue
     writes.append({'line':node.lineno,'call':ast.unparse(node)[:250]})
  safety.append({'path':p.relative_to(D).as_posix(),'sha256':sha(p),'roots':roots,'write_related_calls':writes})
 save('01_격리와도구안전.json',{'C_original_unchanged':before==snapshot(C),'C_file_count':len(before),'C_sha256_map':before,'D_overlay_files':copies,'tools':safety,'note':'검사기와 import 의존성의 본문/루트/파일 쓰기 호출을 정적 검토. 생성기 main은 실행하지 않음. 좌표시험 BASE 절대 D 경로는 import 후 C로 재지정하여 run API만 사용.'})
 save('02_격리초기해시.json',snapshot(W))
 print(json.dumps({'isolated':str(W),'C_files':len(before),'overlay_count':len(copies),'tools':len(safety)},ensure_ascii=False))

if sys.argv[1:] == ['baseline']:
 os.environ['PYTHONUTF8']='1';sys.dont_write_bytecode=True
 cmds=[['R1_자산검사.py'],['R2_운영자료검사.py'],['R3_모션자료검사.py'],['R3_레이아웃자료검사.py'],['R3_스킬자료검사.py'],['자료검증.py'],['통합기록_규격시험.py'],['시간프레임_규격시험.py'],['근거주장_규격시험.py'],['R5_조회와표시.py'],['R5_디자인적용검사.py','03_한맥디자인/디자인적용_설명용예시.json'],['R6_출처사용검사.py','--base',str(W)],['R6_사람검수.py','--base',str(W)],['R6_통합조회.py'],['R7_연결확인.py','--base',str(W)]]
 before=snapshot(W);results=[]
 for a in cmds:
  p=subprocess.run([str(PY),'-B','-X','utf8',str(W/'07_실행도구'/a[0]),*a[1:]],cwd=W,capture_output=True,text=True,encoding='utf-8',timeout=90)
  log={'args':a,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};results.append(log)
  print(a[0],p.returncode,flush=True)
 save('03_기존검사_실재실행.json',{'runs':results,'isolated_inputs_unchanged':before==snapshot(W),'C_original_unchanged':json.loads((OUT/'01_격리와도구안전.json').read_text(encoding='utf-8'))['C_sha256_map']==snapshot(C)})

if sys.argv[1:] == ['complete']:
 sys.dont_write_bytecode=True;sys.path.insert(0,str(W/'07_실행도구'))
 copied=[]
 deps=['backup/2026-10-14_R3_추가조사/스킬원본/impeccable/skill/reference/layout.md','backup/2026-10-14_R3_추가조사/스킬원본/impeccable/skill/reference/typeset.md','10_공용자산/문서명시_검토목록.json']
 doc=json.loads((D/'05_출처와검토/스킬심층검토/스킬심층검토정본.json').read_text(encoding='utf-8'))
 deps += [r['path'] for r in doc['evidence_reports']]
 for rel in deps:
  assert 'R8_04' not in rel
  p=D/rel;dest=W/rel
  if not dest.exists() or sha(dest)!=sha(p):dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);copied.append({'path':rel,'sha256':sha(p)})
 before=snapshot(W);runs=[]
 for name in ['R3_레이아웃자료검사.py','R3_스킬자료검사.py','R5_조회와표시.py']:
  p=subprocess.run([str(PY),'-B','-X','utf8',str(W/'07_실행도구'/name)],cwd=W,capture_output=True,text=True,encoding='utf-8',timeout=90)
  runs.append({'tool':name,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});print(name,p.returncode,flush=True)
 save('04_격리누락보충_재실행.json',{'copied_missing_dependencies':copied,'runs':runs,'inputs_unchanged':before==snapshot(W),'note':'초기 C 격리 누락은 D 결함이 아님. R3 스킬검사의 옛 설치 presentations 네 경로는 실제 원래 위치 부재이며 R6 recovery 경로 보관본 확인과 별도 구분.'})

 results=[]
 def test(name,call,expect):
  try:r=call();ok=expect(r);results.append({'name':name,'passed':bool(ok),'result':r})
  except Exception as e:results.append({'name':name,'passed':False,'exception':repr(e)})
 r1=load(W/'07_실행도구/R1_자산검사.py')
 co=r1.read('10_공용자산/회사목록.json');assets=r1.read('10_공용자산/자산목록.json');colors=r1.read('10_공용자산/CI색상목록.json')
 def r1derive():
  a=copy.deepcopy(assets);x=next(x for x in a['records'] if x['role']=='derived');x['role']='original';return r1.inspect(co,a,colors,W)
 test('R1 파생을 원본 role로 승격 거부',r1derive,lambda r:not r['valid'])
 def r1official():
  c=copy.deepcopy(colors);x=next(x for x in c['colors'] if x['source_level']=='raster_sample');x['source_level']='official_declared';return r1.inspect(co,assets,c,W)
 test('R1 관측로고 색을 공식색으로 승격 거부',r1official,lambda r:not r['valid'])
 test('R1 기본 팔레트는 미확인 공식색을 비워 둠',lambda:r1.palette(co['companies'][0]['company_id'],co,colors,assets=assets,base=W),lambda r:r['colors']==[])
 r2=load(W/'07_실행도구/R2_운영자료검사.py');data=r2.load()
 def r2weak():
  x=copy.deepcopy(data);g=next(g for g in x[1]['guides'] if g['term_id'].startswith('CURVE-'));g['minimum_evidence']='visible_scope';return r2.validate(*x)
 test('R2 시간곡선 근거를 정지화면으로 낮춤 거부',r2weak,bool)
 def r2state():
  x=copy.deepcopy(data);a=next(a for c in x[3]['cases'] for a in c['annotations'] if a['status']=='not_assessed');a['status']='not_applicable';return r2.validate(*x)
 test('R2 미검토를 비적용으로 바꿔 누락 숨김 거부',r2state,bool)
 r3=load(W/'07_실행도구/R3_레이아웃자료검사.py');rd=lambda p:json.loads((W/p).read_text(encoding='utf-8'))
 kd=rd('02_원칙과레이아웃/레이아웃_심화지식.json');lg=rd('05_출처와검토/R3_레이아웃_조사기록.json');cases=rd('02_원칙과레이아웃/레이아웃_문구와화면비사례.json');ext=rd('02_원칙과레이아웃/레이아웃_확장후보.json')
 def r3equal():
  k=copy.deepcopy(kd);k['layout_cards'][0]['counterexample']=k['layout_cards'][0]['positive_example'];return r3.inspect(k,lg,cases,ext)
 test('R3 레이아웃 예와 반례 동일문구 거부',r3equal,bool)
 def r3depth():
  l=copy.deepcopy(lg);l['sources'][0]['read_depth']='full_source_executed';return r3.inspect(kd,l,cases,ext)
 test('R3 선택절 검토를 전체실행으로 부풀림 거부',r3depth,bool)
 coords=load(W/'07_실행도구/좌표변환_규격시험.py');coords.BASE=W
 test('R4 구형 좌표회귀 BASE를 격리 C로 명시지정',lambda:coords.run(load(W/'07_실행도구/좌표변환_규격검사.py'),rd('04_기록규격/좌표변환_스키마.json')),lambda r:r['all_passed'])
 v=load(W/'07_실행도구/자료검증.py')
 test('R4 구형 fixture는 needs_migration이며 통과 아님',lambda:v.inspect_file(W/'06_맞춤스킬/video-record-steward/evals/files/검사입력.json'),lambda r:r['status']=='needs_migration' and r['valid'] is False)
 intake=load(W/'07_실행도구/기록접수.py');temp=OUT/'isolated/intake_only';temp.mkdir(parents=True,exist_ok=True);(temp/'04_기록규격').mkdir(exist_ok=True)
 shutil.copy2(W/'04_기록규격/기록접수_스키마.json',temp/'04_기록규격/기록접수_스키마.json');fixture=temp/'legacy.json';shutil.copy2(W/'06_맞춤스킬/video-record-steward/evals/files/검사입력.json',fixture)
 def intaketest():
  h=sha(fixture);a=intake.receive(fixture,'독립감사 격리 fixture',temp);s=snapshot(temp);b=intake.receive(fixture,'독립감사 격리 fixture',temp);return {'source_unchanged':h==sha(fixture),'second_run_unchanged':s==snapshot(temp),'same_entry':a==b,'status':a['status'],'analysis_search_allowed':a['analysis_search_allowed']}
 test('R4 명시접수 원문보존·재실행 불변·분석검색 금지',intaketest,lambda r:r['source_unchanged'] and r['second_run_unchanged'] and r['same_entry'] and r['analysis_search_allowed'] is False)
 q=load(W/'07_실행도구/R5_조회와표시.py');cid=co['companies'][0]['company_id']
 test('R5 문자열 false 옵션은 관측색 허용으로 해석하지 않음',lambda:q.query(cid,include_observed='false',base=W),lambda r:r['valid'] is False and r['colors']==[])
 test('R5 정상 기본조회 공식색·선택역할을 발명하지 않음',lambda:q.query(cid,base=W),lambda r:r['valid'] and r['colors']==[] and r['selected_roles']=={} and r['company_approved'] is False)
 import R6_사람검수 as human
 def r6stale():
  d=rd(human.LEDGER);d['events'][0]['context_sha256']='0'*64;return human.inspect(W,d,source_artifacts=False)
 test('R6 다른 회신문맥 대입 거부·답변수 승격 방지',r6stale,lambda r:not r['structural_valid'] and r['queue']==[] and r['recorded_answer_count']==0)
 r7=load(W/'07_실행도구/R7_연결확인.py')
 test('R7 중복키 JSON 거부',lambda:reject_parse(r7),lambda r:r=='duplicate_json_key')
 # 이 반례는 원문/C800/격리기반을 변경하지 않고 별도 최소루트만 생성한다.
 stale=OUT/'isolated/stale_R7';(stale/Path(r7.MANIFEST).parent).mkdir(parents=True,exist_ok=True)
 manifest=rd(r7.MANIFEST);manifest['pins'][0]['sha256']='0'*64;(stale/r7.MANIFEST).write_text(json.dumps(manifest,ensure_ascii=False),encoding='utf-8')
 test('R7 자료누락/오래된 문맥에서 승인 true 생성 안 함',lambda:r7.inspect(stale),lambda r:not r['valid'] and r['company_approved'] is False and r['content_verified'] is False)
 rv=load(W/'06_맞춤스킬/재구성후보/video-record-steward/scripts/판본대조.py')
 b={'record_id':'AUDIT','version':'0.1.0','schema_version':'0.2.0','note':'old'};a={**b,'note':'new'};raw=lambda d:json.dumps(d,ensure_ascii=False).encode('utf-8')
 test('R8 내용변경 자체판본 유지 거부',lambda:rv.inspect_bytes(raw(b),raw(a)),lambda r:not r['valid'])
 test('R8 정확복구는 체크포인트 bytes와 SHA 대조',lambda:rv.inspect_bytes(b'{broken',raw(b),'exact_restore',raw(b),hashlib.sha256(raw(b)).hexdigest()),lambda r:r['valid'] and r['writes_performed'] is False)
 save('05_독립의미반례_새실행.json',{'cases':results,'count':len(results),'all_passed':all(r['passed'] for r in results),'basis_inputs_unchanged':before==snapshot(W),'C_original_unchanged':json.loads((OUT/'01_격리와도구안전.json').read_text(encoding='utf-8'))['C_sha256_map']==snapshot(C),'note':'좌표시험은 원래 D 절대 BASE를 보존하고 import한 격리 module의 BASE만 C로 재지정. 원본 도구/기대값/핀 미수정. R6 stale 반례는 source_artifacts=False이며 앞선 full 기초실행과 구분.'})
 print('semantic',len(results),all(r['passed'] for r in results),flush=True)

def reject_parse(module):
 try:module.parse(b'{"a":1,"a":2}')
 except ValueError as e:return str(e)
 return 'accepted'

