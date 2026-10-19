from pathlib import Path
import sys,subprocess,json,os
P=Path(__file__).resolve().parent
queries=[['--query','업무 이미지 묶음','--out','query_results/work.json'],['--id','RC-COMP-008@v1','--out','query_results/building.json'],['--query','역할판','--out','query_results/role.json'],['--id','RC-COMP-005@v1','--out','query_results/nameplates.json'],['--id','RC-COMP-002@v1','--out','query_results/logos.json'],['--knowledge','IP-04','--out','query_results/knowledge_ip04.json'],['--review','REV-04','--out','query_results/review04.json'],['--case','RC-CASE-002','--out','query_results/case002.json'],['--validate','--out','query_results/validation.json']]
log=[]
env=dict(os.environ,PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
for args in queries:
 cmd=[sys.executable,str(P/'query.py'),*args]
 r=subprocess.run(cmd,cwd=P,capture_output=True,text=True,encoding='utf-8',env=env)
 log.append({'command':cmd,'cwd':str(P),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 if r.returncode:raise RuntimeError(r.stderr or r.stdout)
(P/'query_execution.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
results={p.stem:json.loads(p.read_text(encoding='utf-8')) for p in (P/'query_results').glob('*.json')}
checks=[]
def check(ok,description):
 checks.append({'passed':bool(ok),'description':description})
 if not ok:raise AssertionError(description)
check(results['work']['result_count']==1,'업무 묶음 검색은 RC-COMP-007@v1 한 정의 반환')
check(results['building']['results'][0]['definition']['id']=='RC-COMP-008@v1','건물/기단 정의와 현재 사용처 왕복')
check({x['definition']['id'] for x in results['role']['results']}=={'RC-LAYOUT-001@v1','RC-COMP-003@v1'},'역할판 검색은 전체 배치/헤더 두 범위 반환')
check(results['nameplates']['result_count']==1,'명찰은 건물/기단과 별도 조회')
check(len(results['logos']['results'][0]['occurrences'])==2,'회사 타일은 E1/E2 두 사용처와 차이 보존')
check({x['definition']['id'] for x in results['knowledge_ip04']['results']}=={'RC-COMP-005@v1','RC-COMP-008@v1'},'IP-04에서 건물/기단과 명찰 사용처 반환')
check(any(r['id']=='REV-04' for x in results['review04']['results'] for r in x['reviews']),'실제 검토 ID에서 대상/현재 근거 조회')
check(results['case002']['result_count']==6,'사례002에서 레이아웃·장표식·회사타일·명찰·성과수치·건물의 6개 정의 조회')
check(results['validation']['passed'],'참조/해시/보존/지식 포인터 검사 통과')
for name in ['work','building','role','nameplates','logos','knowledge_ip04','review04','case002']:
 for x in results[name]['results']:
  check(bool(x['occurrences']) and bool(x['evidence']) and bool(x['knowledge']) and bool(x['reviews']),f'{name}/{x["definition"]["id"]}: 사용처·근거·지식·검수 동반')
(P/'query_verification.json').write_text(json.dumps({'scope':'actual lookup result integrity; no grading or visual accuracy automation','checks':checks},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'query_commands':len(log),'returncodes':[x['returncode'] for x in log],'result_counts':{k:v.get('result_count') for k,v in results.items()},'verification_checks':len(checks),'all_passed':all(x['passed'] for x in checks)},ensure_ascii=False))
