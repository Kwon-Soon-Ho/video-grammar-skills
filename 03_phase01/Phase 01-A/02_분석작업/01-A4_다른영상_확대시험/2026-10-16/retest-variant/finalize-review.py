import json, hashlib, shutil, subprocess
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
r=Path.cwd(); a=r/'phase01a-a4'; aux=a/'retest-variant'
srcroot=r/'company-video-grammar-analyzer-workspace/iteration-2'
dstroot=a/'company-video-grammar-analyzer-workspace/iteration-2'
crops=json.loads((aux/'crops.json').read_text('utf-8'))
changes=[]
for case in ['V06S','V06W']:
 out=srcroot/('eval-'+case)/'with_skill/outputs'
 p=out/'observations.json'; d=json.loads(p.read_text('utf-8'))
 obs={x['id']:x for x in d['objects']}
 for e in obs['schedule']['events']:
  if e['easing']['classification']=='decelerate':
   old=e['easing'].copy()
   e['easing']['classification']='unknown'
   e['easing']['basis']=('239.2/239.3/239.4/239.6초 y잔량15/6/0/0px. 진행 중 두 0.1초 구간의 변위9/6px은 있으나 차이3px이 위치추적 최소2px 오차 및 혼합 변화에 비해 작다. 상방 이동과 정착은 확인하되 감속을 분리 입증하기 부족하다.' if case=='V06S' else '244.2/244.4/244.6초 y잔량15/0/0px. 이동 중 유효 변화율은 첫0.2초 구간 하나뿐이며 이후는 정지다. 일정속도 후 정지와 진행 중 감속을 구별할 수 없다. 상방 이동 및 정착만 확인한다. 최소2px 위치오차.')
   e['description']='뒤쪽 작업보고 문서가 상방으로 이동한 뒤 정착한다. 진행 중 가감속 곡선은 미확정이다.'
   changes.append(dict(case_id=case,target='schedule_document.position',before=old,after=e['easing']))
 for e in obs['efficiency_connections']['events']:
  e['description']=e['description'].replace('실시간 정보공유로…, 효능감있는 협업환경에서… 문구가 보인다.', '실시간 정보공유로… 및 …협업환경에서…라는 부분 문구가 보인다. 두 번째 말풍선의 앞 수식어는 판독 불확실로 원문 확정하지 않는다.')
 if case=='V06W':
  files=['V06W_247_cards2.png','V06W_248_cards1.png','V06W_247_cards3.png','V06W_249.5_title0.png','V06W_250_title0.png']
  for name in files:
   c=next(c for c in crops if Path(c['path']).name==name)
   par=next(e for e in d['evidence'] if e['path']==c['parent_path'])
   path=Path(c['path']); eid='roi_'+path.stem
   if not any(e['id']==eid for e in d['evidence']):
    d['evidence'].append(dict(id=eid,path=str(path),actual_seconds=par['actual_seconds'],role=par['role'],parent_path=c['parent_path'],crop_xyxy_native_pixels=c['crop_xyxy_native_pixels'],sha256=hashlib.sha256(path.read_bytes()).hexdigest(),view_method='native RGB crop directly viewed; UI may downscale'))
  obs['schedule_inside']['events'][0]['evidence_ids'].append('roi_V06W_247_cards2')
  obs['quality']['events'][1]['evidence_ids'].append('roi_V06W_248_cards1')
  obs['efficiency_connections']['events'][0]['evidence_ids'].append('roi_V06W_247_cards3')
  e=obs['title']['events'][1]
  e['time_seconds']=[247,249.5]
  e['evidence_ids']+=['roi_V06W_249.5_title0','roi_V06W_250_title0']
  e['description']+=' 249.5초 창 내부에서도 밝은 상태다. 경계 다음 문맥250초에서는 다시 어두운 녹색 상태를 확인한다. 250초를 창 내부로 포함하거나 밝음→어두움의 실제 전환 시각을 확정하지 않는다.'
  e['limitations'].append('창 내249.5초 밝음과 context_after250초 어두움만 비교. 그 사이의 반환 시작·완료 시각과 변화 곡선은 미확정.')
  d['coverage']['unresolved'].append('제목의 밝아진 상태249.5→어두운 상태250 사이 전환 시각·곡선:250은 context_after')
 d['review_log']+=['최종 제한 검토: 세 시각의 형식적 충족보다 진행 중 유효 변위 구간을 검사. 정착 프레임만으로 감속 판정하지 않음. 작업보고 문서 S/W의 곡선을 unknown으로 보정.', '유지한 decelerate는 S 안전12/9/5px, 품질13/8/1px, 회의 인물10/4px 및 W 안전23/19/8px의 동일 시간 간격 이동 구간에 한정한 감속 경향. 정확한 보간함수·전체 ease-in-out은 추정하지 않음.']
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf-8')
 lines=[f'# {case} 독립 A4 재관측',f'범위 {d["window_seconds"]}초 반개구간. 원본 SHA-256 `{d["source"]["sha256"]}`.',d['method'],'']
 for ob in d['objects']:
  lines+=['## '+ob['name']]
  for e in ob['events']:
   lines+=['- **'+str(e['time_seconds'])+'초** '+e['description']+' 순서/방향: '+e['direction_order']+' 가감속: '+e['easing']['classification']+' — '+e['easing']['basis']+' 근거: '+', '.join(e['evidence_ids'])+'.'+(' 한계: '+'; '.join(e['limitations']) if e['limitations'] else '')]
 lines+=['## 문서 대조',d['document_comparison']['status']]
 for m in d['document_comparison']['mappings']:
  lines+=['- '+m['loc']+': '+m['relation']]
 lines+=['## 불확실성과 검수 한계',*['- '+x for x in d['coverage']['unresolved']],*['- '+x for x in d['limitations']], '## 최종 판정 보정',*['- '+x for x in d['review_log'][-2:]],'근거 경로·원본 PTS·native crop 좌표·문서 구절·수치 측정은 observations.json에 수록. 자동 검사는 시각 내용 정답 판정이 아니다.']
 (out/'observations.md').write_text('\n\n'.join(lines),'utf-8')
comp=srcroot/'eval-V06S/with_skill/outputs/variant-comparison.md'
comp.write_text(comp.read_text('utf-8')+'\n\n최종 재검토: 작업보고 문서의 상방 이동·정착은 양 판 모두 확인하되 곡선은 unknown이다. W의15/0/0px은 이동 중 한 구간+정지에 불과하며, S의9/6px 구간 차이는 최소2px 위치오차에 비해 작다. S 안전·품질·회의 인물 및 W 안전의 감속은 각 대상의 여러 이동 구간에서 감소하는 변위에 한정한 관측 경향이다. W 제목은249.5초 밝은 상태이나250초 경계 다음 문맥에서는 어두운 상태로 돌아온다. 정확한 반환 시각과 곡선은 미확정이며250초는 창 내부가 아니다.\n','utf-8')
(aux/'final-review-changes.json').write_text(json.dumps(dict(changes=changes,additional=['W title 249.5 within versus 250 context_after explicitly separated','Uncertain speech-bubble adjective no longer transcribed as exact text','Three directly viewed W card native crops linked'],scope='Existing independent evidence only; no additional extraction; no full rerun'),ensure_ascii=False,indent=2),'utf-8')
py=r'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
for case in ['V06S','V06W']:
 out=srcroot/('eval-'+case)/'with_skill/outputs'
 run=subprocess.run([py,'-B','-X','utf8',str(a/'skill-draft3/scripts/check_observations.py'),str(out/'observations.json'),'--catalog',str(aux/'evidence-catalog.json')],capture_output=True,text=True,encoding='utf-8')
 print(case,run.returncode,run.stdout,run.stderr)
 assert run.returncode==0
 report=json.loads(run.stdout); assert report['structure_passed'] and report['evidence_provenance_checked']
 (out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
 dst=dstroot/('eval-'+case)/'with_skill/outputs';dst.mkdir(parents=True,exist_ok=True)
 for f in out.iterdir():
  if f.is_file():
   shutil.copy2(f,dst/f.name)
   assert hashlib.sha256(f.read_bytes()).digest()==hashlib.sha256((dst/f.name).read_bytes()).digest()
manifest=[]
for root in [srcroot,dstroot]:
 for case in ['V06S','V06W']:
  for f in sorted((root/('eval-'+case)/'with_skill/outputs').iterdir()):
   if f.is_file():manifest.append(dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),size=f.stat().st_size))
auxfiles=[dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),size=f.stat().st_size) for f in sorted(aux.iterdir()) if f.is_file() and f.name!='freeze-manifest.json']
(aux/'freeze-manifest.json').write_text(json.dumps(dict(frozen_utc=datetime.now(timezone.utc).isoformat(),outputs=manifest,auxiliary_files=auxfiles,notes='Final post-review files copied and byte-hash verified. No further mutations intended. Manifest excludes itself.'),ensure_ascii=False,indent=2),'utf-8')
print('FROZEN',len(manifest),'output copies',len(auxfiles),'auxiliary files')
