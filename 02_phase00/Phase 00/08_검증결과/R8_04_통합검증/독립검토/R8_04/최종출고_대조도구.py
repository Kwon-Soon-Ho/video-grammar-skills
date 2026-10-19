"""Independent final release evidence check. Read D; write one temporary C result only."""
from pathlib import Path
import hashlib,json,re
L=Path(__file__).resolve().parents[1]
D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
def io(p):
    s=str(Path(p).resolve())
    return Path(s if s.startswith('\\\\?\\') else '\\\\?\\'+s)
def sha(p):return hashlib.sha256(io(p).read_bytes()).hexdigest()
def read(p):return json.loads(io(p).read_text(encoding='utf-8-sig'))
def inspect():
    freeze=L/'R8_04_최종게시_입력고정.json';f=read(freeze);rows=[]
    def compare(group,p,expected):
        actual=sha(p) if io(p).is_file() else None
        rows.append({'group':group,'path':str(p),'expected':expected,'actual':actual,'match':actual==expected})
    for r in f['source_files']:compare('C_frozen_source',r['source'],r['sha256'])
    for r,h in f['D_before'].items():compare('D_before',D/r,h)
    for r,h in f['D_read_snapshot'].items():compare('D_read_snapshot',D/r,h)
    for r,h in f['candidate_hashes'].items():compare('D_candidate',D/r,h)
    foundations={'05_출처와검토/검수와사용범위/통합검수_입력고정.json':'257971f59f01c3e834acb4b25ee789e78872dfc7ce29960801551f3052f46a57','13_품질검수/연결과인계/현재연결_입력고정.json':'99cfb91c11ef43d57f5ffc1eb5dc35f67bc4e889e75f9dd515aee3222ceda855'}
    for r,h in foundations.items():compare('historical_foundation',D/r,h)
    for r in read(D/'13_품질검수/연결과인계/현재연결_입력고정.json')['pins']:compare('R7_pin',D/r['path'],r['sha256'])
    for r in read(D/'14_스킬재구성/현재상태_정정표.json')['records']:
        for ref in [r['source']]+r['basis']:compare('errata_source_basis',D/ref['path'],ref['sha256'])
    for i,n in [(1,'큐레이터'),(2,'기록관리자'),(3,'적용성검토자')]:
        folder=D/f'08_검증결과/R8_0{i}_{n}'
        receipt=read(folder/'보존과최종연결_확인.json')
        compare('historical_sealed_report',folder/'00_결과안내.md',receipt.get('reader_report_sha256',receipt.get('report_sha256')))
    ledger=read(L/'R8_04_시험/실행완료_기록.json');runs=[]
    for key,run in ledger['runs'].items():
        p=Path(run['run']);compare('ledger_task',p/'task.txt',run['task_sha256'])
        for rel,h in run['output_hashes'].items():compare('ledger_output',p/rel,h)
        runs.append({'key':key,'status':run['status'],'actual_spawn_observed':run.get('actual_spawn_observed'),'actual_completion_notification_observed':run.get('actual_completion_notification_observed'),'timing':run['timing']})
    scores={}
    for label,rel in [('original','종합채점.json'),('post1','보완후/종합채점.json'),('handoff','순차인계/종합채점.json'),('post2','경로회귀/종합채점.json')]:
        p=L/'R8_04_독립검토/채점'/rel;scores[label]=read(p)['summary']
    cohort5=[]
    for p in sorted((L/'R8_04_시험/5_경로보완회귀').glob('eval-*/candidate')):
        files=[x for x in io(p/'inputs/Phase00/실행스킬').rglob('SKILL.md') if x.is_file()]
        assert len(files)==1, 'Exactly one role skill is expected in cohort5: '+str(p)
        supplied=[]
        for x in files:
            name=x.parent.name;current=D/'06_맞춤스킬/재구성후보'/name/'SKILL.md'
            compare('cohort5_supplied_current_candidate',x,sha(current))
            supplied.append({'skill':name,'version':re.search(r'version: "([^"]+)"',x.read_text(encoding='utf-8')).group(1),'sha256':sha(x)})
        cohort5.append({'case':p.parent.name,'supplied':supplied})
    groups={}
    for r in rows:groups[r['group']]=groups.get(r['group'],0)+1
    return {'publication_script_sha256':sha(L/'R8_04_최종게시.py'),'freeze_sha256':sha(freeze),'check_tool_sha256':sha(Path(__file__)),'comparison_counts':groups,'mismatches':[r for r in rows if not r['match']],'run_count':len(runs),'runs':runs,'scores':scores,'scores_equal_freeze':scores==f['scores'],'cohort5':cohort5,'source_count':len(f['source_files']),'destination_count':len(set(x['destination'] for x in f['source_files'])),'suspicious_restricted_source_paths':[r['source'] for r in f['source_files'] if 'anthropic-pptx' in r['source']],'read_scope':'Hash comparison is not semantic reading or execution; ledger observations are recorded provenance, not independently authenticated spawn events.'}
if __name__=='__main__':
    result=inspect();out=L/'.final_release_checks.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['runs']},ensure_ascii=False,indent=2))
