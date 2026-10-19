"""수행 fixture 정적 hash/범위 감사. 도구·시행·채점기를 실행하지 않는다."""
from pathlib import Path
import hashlib,json,re
OUT=Path(__file__).resolve().parent
HOME=OUT.parent/'R8_시험/video-record-steward-workspace'
read_hash={}
def raw(p):
    b=p.read_bytes();read_hash[str(p)]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)};return b
def obj(p):return json.loads(raw(p).decode('utf-8-sig'))
prepared_code=raw(OUT.parent/'R8_02_시험준비.py')
manifest=obj(HOME/'수행자료_포함과분리.json')
declaration=obj(HOME/'동등조건_확인.json')
criteria_raw=raw(HOME/'평가항목.json');criteria=json.loads(criteria_raw.decode('utf-8-sig'))
criteria_fixed=obj(HOME/'평가기준_고정기록.json')
D_review=obj(OUT/'R8_02_읽은D파일hash.json')['D_files_read']
sources=manifest['included_source_hashes']
excluded=manifest['excluded_evaluation_and_reconstruction_source_hashes']
rows=[];pairs=[];leaks=[]
for ed in sorted((HOME/'iteration-1').glob('eval-*')):
    run_data={};task_data={}
    for arm in ['old_skill','new_skill']:
        run=ed/arm/'run-1';db=run/'inputs/Phase00'
        before=obj(run/'fixture_before.json')['files']
        current={p.relative_to(db).as_posix():hashlib.sha256(raw(p)).hexdigest() for p in db.rglob('*') if p.is_file()}
        task=raw(run/'task.txt').decode('utf-8-sig');task_data[arm]=task.replace(str(run),'{RUN}')
        preflight=obj(run/'fixture_preflight.json');dispatch=obj(run/'dispatch.json')
        changed=[p for p in before if before[p]!=current.get(p)]
        extra=sorted(set(current)-set(before))
        source_missing=[p for p in sources if p not in current]
        source_diff=[p for p,h in sources.items() if current.get(p)!=h]
        excluded_present=sorted(set(excluded)&set(current))
        skill_hash_mismatches=[]
        prefix='실행스킬/video-record-steward/'
        canonical=('06_맞춤스킬/재구성후보/' if arm=='new_skill' else '06_맞춤스킬/')+'video-record-steward/'
        for rel,h in current.items():
            if rel.startswith(prefix):
                prior=D_review.get(canonical+rel[len(prefix):])
                if prior is None or prior['sha256']!=h:skill_hash_mismatches.append(rel)
        if arm=='new_skill':
            for p in [db/'05_출처와검토/검수와사용범위/출처와사용범위_연결목록.json']:
                if p.is_file():
                    text=raw(p).decode('utf-8-sig')
                    marker='R8에서 정본 읽기·draft 쓰기·승인 보류를 평가'
                    if marker in text:leaks.append({'run':str(run),'file':p.relative_to(db).as_posix(),'kind':'R3/R8 evaluation design copied inside R6 original_record','marker':marker,'sha256':current[p.relative_to(db).as_posix()]})
        rows.append({'run':str(run),'before_file_count':len(before),'current_file_count':len(current),'before_mismatches':changed,'extra_after_preparation':extra,'source_missing':source_missing,'source_hash_mismatches':source_diff,'excluded_path_intersection':excluded_present,'loaded_skill_hash_mismatches_against_static_review':skill_hash_mismatches,'preflight_declaration':preflight,'dispatch_state':dispatch['state'],'task_sha_matches_dispatch':hashlib.sha256(task.encode('utf-8')).hexdigest()==dispatch['task_sha256']})
        run_data[arm]={p:h for p,h in current.items() if not p.startswith('실행스킬/')}
    pairs.append({'eval':ed.name,'same_non_skill_bytes':run_data['old_skill']==run_data['new_skill'],'non_skill_file_count':len(run_data['old_skill']),'same_task_after_run_path_normalization':task_data['old_skill']==task_data['new_skill']})
history_root=HOME/'시험준비이력/평가문단_간접포함_수정전/iteration-1'
history_runs=list(history_root.glob('eval-*/*/run-1'))
history_markers=[]
for run in history_runs:
    p=run/'inputs/Phase00/05_출처와검토/검수와사용범위/출처와사용범위_연결목록.json'
    if p.is_file():
        history_markers.append({'run':str(run),'marker_present':'R8에서 정본 읽기·draft 쓰기·승인 보류를 평가' in raw(p).decode('utf-8-sig'),'sha256':read_hash[str(p)]['sha256']})
report={'scope':'static fixture/hash audit; no task/tool/checker/grader execution','active_run_count':len(rows),'six_active_runs_observed':len(rows)==6,'included_source_count':len(sources),'excluded_source_count':len(excluded),'all_six_fixtures_match_prepared_hashes':len(rows)==6 and all(not r['before_mismatches'] and not r['extra_after_preparation'] for r in rows),'all_six_included_sources_match_manifest':len(rows)==6 and all(not r['source_missing'] and not r['source_hash_mismatches'] for r in rows),'all_six_excluded_paths_absent':len(rows)==6 and all(not r['excluded_path_intersection'] for r in rows),'all_six_dispatches_prepared_not_executed':len(rows)==6 and all(r['dispatch_state']=='prepared_not_executed' for r in rows),'R6_included_paths':[p for p in sources if p.startswith('05_출처와검토/검수와사용범위/')],'criteria_count':sum(len(v) for v in criteria['cases'].values()),'criteria_hash_matches_fix':hashlib.sha256(criteria_raw).hexdigest()==criteria_fixed['criteria_sha256'],'criteria_hash':hashlib.sha256(criteria_raw).hexdigest(),'criteria_dispatch_count_declared_at_fix':criteria_fixed['actual_executor_dispatches_at_fix'],'historical_initial_run_count':len(history_runs),'historical_indirect_marker_evidence':history_markers,'rows':rows,'pairs':pairs,'indirect_evaluation_design_leaks':leaks,'read_file_hashes':read_hash,'preflight_passes_are_author_reports_not_independent_reexecution':True}
target=OUT/'R8_02_fixture정적근거.json'
if target.exists():
    old=target.read_bytes();history=OUT/('R8_02_fixture정적근거_'+hashlib.sha256(old).hexdigest()[:12]+'.json')
    if not history.exists():history.write_bytes(old)
target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['read_file_hashes','rows']},ensure_ascii=True))
