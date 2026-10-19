"""draft.3·iteration-2 정적 읽기/hash/AST 감사. helper·검사기·수행자·채점기는 실행하지 않는다."""
from pathlib import Path
import json,hashlib,ast,re
OUT=Path(__file__).resolve().parent
W=OUT.parent/'R8_시험/video-record-steward-workspace'
D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
hashes={}
def raw(p):
    b=p.read_bytes();hashes[str(p)]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)};return b
def obj(p):return json.loads(raw(p).decode('utf-8-sig'))
def h(p):raw(p);return hashes[str(p)]['sha256']
def fmap(root):return {p.relative_to(root).as_posix():h(p) for p in root.rglob('*') if p.is_file()}
confirm=obj(D/'08_검증결과/R8_02_행동보완확인.json')
candidate_checks={rel:h(D/rel)==expected for rel,expected in confirm['candidate_hashes'].items()}
candidate={rel[len('06_맞춤스킬/재구성후보/video-record-steward/'):]:h(D/rel) for rel in confirm['candidate_hashes']}
r1=raw(D/'00_운영계약/01_보존과버전_계약.md')
helper_rel='06_맞춤스킬/재구성후보/video-record-steward/scripts/판본대조.py'
helper=raw(D/helper_rel);tree=ast.parse(helper.decode('utf-8-sig'))
imports=[]
for node in ast.walk(tree):
    if isinstance(node,ast.Import):imports.extend(alias.name for alias in node.names)
    if isinstance(node,ast.ImportFrom):imports.append(node.module)
attribute_calls=sorted({n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)})
local_source=OUT.parent/'R8_02_판본대조_원문.py'
unit=obj(W/'판본대조_단위검사.json');raw(OUT.parent/'R8_02_판본대조_시험.py')
archive=W/'후보보존/v0.2.0-draft.2';archive_matches={}
for rel,expected in confirm['before_hashes'].items():
    tail=rel[len('06_맞춤스킬/재구성후보/video-record-steward/'):]
    archive_matches[tail]=h(archive/tail)==expected
backup={}
for p in (D/'backup/2026-10-15_R8_02_행동보완').rglob('*'):
    if p.is_file():backup[p.relative_to(D).as_posix()]=h(p)
initial_runs=[]
for run in sorted((W/'iteration-1').glob('eval-*/*/run-1')):
    grade=obj(run/'grading.json')
    initial_runs.append({'run':str(run),'grading_summary':grade.get('summary'),'outputs':fmap(run/'outputs'),'transcript_exists':(run/'transcript.md').exists(),'grading_sha':h(run/'grading.json')})
unused=[]
for run in sorted((W/'시험준비이력/초기후보_미실행과제').rglob('run-1')):
    unused.append({'run':str(run),'dispatch':obj(run/'dispatch.json'),'has_grading':(run/'grading.json').exists()})
viewer=W/'초기후보검토/기록관리자_출력검토.html'
viewer_match=h(viewer)==confirm['initial_viewer_sha256']
raw(W/'초기후보검토/공식뷰어_실행기록.json')
raw(OUT/'채점/steward_draft2_초기4회_채점요약.md')
criteria=obj(W/'평가항목.json');lock=obj(W/'평가기준_고정기록.json')
initial_criteria=obj(W/'iteration-1/시험설계와진행/평가항목.json')
initial_lock=obj(W/'iteration-1/시험설계와진행/평가기준_고정기록.json')
man=obj(W/'수행자료_포함과분리.json');raw(W/'동등조건_확인.json')
sources=man['included_source_hashes'];excluded=man['excluded_evaluation_and_reconstruction_source_hashes']
saved=obj(D/'08_검증결과/R8_02_입력보존.json')['source_hashes']
old14={p:h(D/p)==v for p,v in saved.items() if p.startswith('06_맞춤스킬/') and not p.startswith('06_맞춤스킬/재구성후보/')}
pins=obj(D/'13_품질검수/연결과인계/현재연결_입력고정.json')['pins']
pin_errors=[p['path'] for p in pins if h(D/p['path'])!=p['sha256']]
rows=[];pairs=[]
for ed in sorted((W/'iteration-2').glob('eval-*')):
    data={};tasks={};cross={}
    for arm in ['old_skill','new_skill']:
        run=ed/arm/'run-1';db=run/'inputs/Phase00';before=obj(run/'fixture_before.json')['files'];cur=fmap(db)
        task=raw(run/'task.txt').decode('utf-8-sig');tasks[arm]=task.replace(str(run),'{RUN}')
        dispatch=obj(run/'dispatch.json');pf=obj(run/'fixture_preflight.json')
        loaded={p[len('실행스킬/video-record-steward/'):]:v for p,v in cur.items() if p.startswith('실행스킬/video-record-steward/')}
        expected=candidate if arm=='new_skill' else {p:h(D/'06_맞춤스킬/video-record-steward'/p) for p in ['SKILL.md','references/작업기준.md']}
        previous=W/'iteration-1'/ed.name/arm/'run-1'
        if not previous.is_dir():
            matches=[p for p in (W/'시험준비이력/초기후보_미실행과제').rglob('run-1') if p.parent.name==arm]
            if len(matches)!=1:raise ValueError('initial case3 run ambiguous')
            previous=matches[0]
        prior=obj(previous/'fixture_before.json')['files']
        old_task=raw(previous/'task.txt').decode('utf-8-sig').replace(str(W/'iteration-1'/ed.name/arm/'run-1'),'{RUN}')
        current_non={p:v for p,v in cur.items() if not p.startswith('실행스킬/')};prior_non={p:v for p,v in prior.items() if not p.startswith('실행스킬/')}
        data[arm]=current_non
        forbidden=[p for p in cur if p in excluded or '/evals/' in p or p.startswith('13_품질검수/평가계획/') or p.startswith('14_스킬재구성/') or p.startswith('08_검증결과/')]
        rows.append({'run':str(run),'matches_fixture_before':cur==before,'sources_match':all(cur.get(p)==v for p,v in sources.items()),'forbidden_evaluation_paths':forbidden,'loaded_skill_matches':loaded==expected,'loaded_skill_file_count':len(loaded),'same_non_skill_input_as_initial':current_non==prior_non,'same_task_as_initial_after_original_run_path_normalization':tasks[arm]==old_task,'dispatch_state':dispatch['state'],'task_sha_matches_dispatch':h(run/'task.txt')==dispatch['task_sha256'],'preflight_declaration':pf})
    pairs.append({'eval':ed.name,'non_skill_count':len(data['old_skill']),'same_non_skill_bytes':data['old_skill']==data['new_skill'],'same_normalized_task':tasks['old_skill']==tasks['new_skill']})
report={'scope':__doc__,'candidate_version':confirm['candidate_version'],'candidate_hash_matches':candidate_checks,'helper_imports':imports,'helper_attribute_calls':attribute_calls,'helper_matches_local_source':hashlib.sha256(helper).hexdigest()==h(local_source),'unit_report_matches_helper_sha':unit['script_sha256']==hashlib.sha256(helper).hexdigest(),'unit_report_conditions':unit['conditions'],'unit_report_passed':unit['passed'],'unit_report_is_independent_reexecution':False,'draft2_C_archive_matches':archive_matches,'draft2_D_backup_all_old_hashes_found':all(v in backup.values() for v in confirm['before_hashes'].values()),'draft2_D_backup':backup,'initial_completed_runs':initial_runs,'initial_unused_case3':unused,'initial_viewer_hash_matches':viewer_match,'criteria_case_strings_unchanged':criteria['cases']==initial_criteria['cases'],'criteria_non_metadata_content_unchanged':{k:v for k,v in criteria.items() if k not in ['candidate_version','version']}=={k:v for k,v in initial_criteria.items() if k not in ['candidate_version','version']},'criteria_changed_keys':[k for k in set(criteria)|set(initial_criteria) if criteria.get(k)!=initial_criteria.get(k)],'criteria_current_sha_matches_lock':h(W/'평가항목.json')==lock['criteria_sha256'],'criteria_initial_sha_matches_old_lock':h(W/'iteration-1/시험설계와진행/평가항목.json')==initial_lock['criteria_sha256'],'criteria_lock':lock,'old_canonical_skill_hash_matches':old14,'r7_static_pin_count':len(pins),'r7_static_pin_errors':pin_errors,'fixture_rows':rows,'fixture_pairs':pairs,'read_file_hashes':hashes}
(OUT/'R8_02_draft3_정적근거.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['read_file_hashes','draft2_D_backup','initial_completed_runs','initial_unused_case3','fixture_rows']},ensure_ascii=True))
