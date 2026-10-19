from pathlib import Path
from fractions import Fraction
import json,hashlib,re,math,urllib.parse,datetime
B=Path(__file__).resolve().parent
ROOT=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
C=read(B/'contract-v1.json');windows=read(B/'windows.json');runs=read(B/'run-matrix.json')
checks=[]
def check(name,value,detail):
 checks.append({'name':name,'passed':bool(value),'detail':detail})
check('run arithmetic',len(runs)==2*2*2*2==16 and len({x['run_id'] for x in runs})==16,'two project groups; four windows; two repetitions; two conditions')
check('balanced treatment',all(sum(x['case_id']==w['case_id'] and x['repeat']==rep and x['configuration']==mode for x in runs)==1 for w in windows for rep in [1,2] for mode in ['with_skill','without_skill']),'exactly one run per cell')
check('planned attempts',C['comparison']['planned_primary_runs']+C['comparison']['legacy_regression_runs']+C['comparison']['maximum_technical_retries']==21,'16+3+2, not 21 new independent examples')
check('window identity',len({x['project_group'] for x in windows})==2 and sum(x['within_seconds'] for x in windows)==36 and len({x['path'] for x in windows})==3,'2 projects / 3 MP4 / 4 windows / 36 seconds')
base=sum(len(w['base_targets_seconds']) for w in windows)
check('observation arithmetic',base==94 and base+16*48+64+8==934 and 934<=1000,'94 shared base +768 adaptive +64 review +8 diagnostics')
check('review arithmetic',40+32+18==C['review_budget']['review_total_minutes_max']==90 and C['review_budget']['user_active_minutes_max_included_in_review']<=90,'user20 minutes is included, not an additional allowance')
check('resource arithmetic',240+30+30+90==C['overall_resource_budget']['total_task_minutes_max']==390,'390 role-task minutes, not summed overlapping calendar time')
check('no trial performed',all(v in [0,None] for v in C['actual_execution'].values()) and not C['authorization']['A5b'],'zero actual analysis/reference runs; A5b unauthorized')
check('denominator rules',math.ceil(.9*9)==9 and math.floor(.05*19)==0,'integer examples:9/9 detail; one false claim out of19 fails95 percent')
for w in windows:
 lo,hi=w['window_seconds'];m=next(m for m in read(B/'materials-metadata.json') if m['path']==w['path'])
 check(w['case_id']+' bounds and hash',0<=lo<hi<m['container_duration_seconds'] and sha(ROOT/w['path'])==w['sha256'],'metadata-only pin rechecked; no decoder')
 times=list(map(Fraction,w['base_targets_seconds']))
 check(w['case_id']+' base order',times==sorted(set(times)) and times[0]==lo and times[-1]==hi and len(times)<=32,'actual PTS still must be verified at A5b; hi is context_after')
pins=read(B/'candidate-pins.json')
check('skill snapshot unchanged',all(sha(B/'candidate/company-video-grammar-analyzer'/f['relative'])==f['sha256']==sha(ROOT/'Phase 01-A/03_분석스킬/company-video-grammar-analyzer'/f['relative']) for f in pins['snapshot_files']),'7 candidate files unchanged')
protected=read(B/'protected-records.before.json')
check('historical records preserved',all(sha(ROOT/f['path'])==f['sha256'] for f in protected),f'{len(protected)} historical text/JSON/skill records; no claim of re-scoring old videos')
check('no visual artifacts created',not any(p.suffix.lower() in ['.png','.jpg','.jpeg','.webp','.mp4','.wav','.mp3'] for p in B.rglob('*')),'source metadata and design only')
broken=[]
for p in (B/'staged').rglob('*.md'):
 virtual=ROOT/p.relative_to(B/'staged')
 for target in re.findall(r'\]\(<?([^\n)]+?)>?\)',p.read_text(encoding='utf-8')):
  target=target.strip('<>')
  if target.startswith(('http:','https:','thread:','#')):continue
  q=Path(urllib.parse.unquote(target.split('#')[0]))
  if not q.is_absolute():q=virtual.parent/q
  try:rel=q.resolve().relative_to(ROOT.resolve())
  except ValueError:
   if not q.exists():broken.append(str(q))
   continue
  if not q.exists() and not (B/'staged'/rel).exists() and not str(rel).startswith('Phase 01-A\\04_검증자료\\01-A5a_실행설계'):broken.append(str(rel))
check('document links',not broken,broken or 'relative and absolute links resolved against final destinations')
check('staged state',read(B/'staged/Phase 01-A/00_진행안내/01-A_계획상태.json')['current_stage']=='01-A5a','A5a design current; A4 status preserved in historical fields')
result={'at':datetime.datetime.now().astimezone().isoformat(),'type':'A5a design consistency and preservation check; not visual recognition tests','checks':checks,'all_passed':all(x['passed'] for x in checks),'actual_A5b_runs':0,'independent_review_performed':False}
(B/'design-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
assert result['all_passed']
