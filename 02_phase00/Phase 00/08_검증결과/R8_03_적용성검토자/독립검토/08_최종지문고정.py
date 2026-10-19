from pathlib import Path
import json,hashlib
C=Path(r'C:\Users\User\Documents\ChatGPT\업무@사내 영상 생성기')
D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
A=C/'phase00-build/R8_03_독립검토';W=C/'phase00-build/R8_시험/video-guidance-reviewer-workspace';P=W.parent/'video-guidance-reviewer'
def io(p):
    s=str(p.resolve());return Path(s if s.startswith('\\\\?\\') else '\\\\?\\'+s)
def sha(p):return hashlib.sha256(io(p).read_bytes()).hexdigest()
def read(p):return json.loads(io(p).read_text(encoding='utf-8-sig'))
before=read(A/'06_최종기초_독립대조.json');viewer=read(A/'07_집계와뷰어_독립대조.json')
assert before['only_expected4_changes_before_publication'] and not before['initial174_backup_mismatches'] and not before['R7_pin_mismatches'] and not before['old_skill_mismatches'] and not before['candidate_mismatches']
assert all(not r['input_byte_mismatches'] and not r['artifact_receipt_mismatches'] and not r['unexpected_run_files'] and r['strict_output_json_parse_valid'] for r in before['runs'])
assert not viewer['prompt_mismatches'] and viewer['output_files_equal']==12 and viewer['post_execution_display_metadata_minimal_keys_verified_count']==6
assert viewer['totals']=={'new_skill':21,'old_skill':21}
publisher=C/'phase00-build/R8_03_결과정리.py'
assert sha(publisher)=='8ad45109035dc3446adf77c16a3b2d013cd4e0512384fe88402833956ec46fc5'
initial=read(D/'08_검증결과/R8_03_입력보존.json')['source_hashes']
dpaths={D/p for p in initial}
dpaths.update(p for p in (D/'06_맞춤스킬/재구성후보/video-guidance-reviewer').rglob('*') if p.is_file())
dpaths.update(p for p in (D/'14_스킬재구성').rglob('*') if p.is_file())
dpaths.update([D/'08_검증결과/R8_03_입력보존.json',D/'08_검증결과/R8_03_정적보완확인.json',D/'13_품질검수/연결과인계/현재연결_입력고정.json'])
dmap={p.relative_to(D).as_posix():sha(p) for p in sorted(dpaths) if '__pycache__' not in p.parts}
cpaths=set()
for root in [W,P,A]:cpaths.update(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
cpaths.update((C/'phase00-build').glob('R8_03_*.py'))
cpaths.update([C/'phase00-build/공통지원.py',C/'phase00-build/R8_01_뷰어작성.py'])
target=A/'R8_03_최종판정.json';cpaths.discard(target)
cmap={p.relative_to(C).as_posix():sha(p) for p in sorted(cpaths)}
verdict={
 'stage':'R8-3','reviewed_on':'2026-10-15','candidate_version':'0.2.0-draft.2',
 'limited_completion_supported':True,'unresolved_blocking_findings':[],
 'limited_completion_scope':['candidate reconstruction and static revision','six synthetic document-review model runs','independent semantic grading and diagnostic tie aggregation','official static viewer source/data verification after prompt-display repair','pre-publication byte preservation and publisher static review'],
 'result':{'cases':3,'runs_per_case_per_configuration':1,'actual_executor_attempts':6,'new_skill_conditions':{'passed':21,'total':21},'old_skill_conditions':{'passed':21,'total':21},'comparative_improvement_demonstrated':False,'general_equivalence_demonstrated':False,'actual_time_tokens':None},
 'resolved_findings':['S-01 valid earlier R6 reply scope','S-02 actual file state after writing failure','P-01 publication state/failure visibility','P-02 source and destination archive IO','P-03 before/after source-destination hash checks','V-01 six missing viewer prompts'],
 'human_output_feedback_received':False,'human_output_feedback_replaced_by_AI_review':False,
 'candidate_adopted':False,'default_path_switched':False,'unseen_followup_tested':False,'actual_skill_draft_writing_tested':False,'designed_skill_writing_failure_tested':False,'fixture_full_R6_R7_validated':False,'actual_video_analyzed':False,'actual_video_effectiveness_validated':False,'company_approved':False,'R8_4_started':False,'R8_complete':False,'Phase00_complete':False,'phase01a_started':False,'browser_render_or_click_tested':False,
 'publisher_sha256':sha(publisher),'D_source_hashes':dmap,'C_result_hashes':cmap,
 'path_bases':{'D_source_hashes':str(D),'C_result_hashes':str(C)},
 'hash_scope_excludes_self':True,
 'limits':['transcripts are executor-authored summaries, not independent complete raw tool traces','start/end hashes do not prove absence of temporary changes','six display-only metadata files were created after execution/grading; not supplied to performers','static HTML/data checks are not rendered UI review','C auxiliary publisher tests are not model trials, skill-write tests or video performance','D publication and receipt verification are subsequent main actions'],
 'required_followup':['actual R8-3 human output feedback','R8-4 unseen cases and evidence-support/version/context challenges','authorized skill writing/failure behavior if retained in adoption scope','full current context, inter-skill handoff, viewer task/output correspondence and default transition review']
}
assert not target.exists(),'Do not overwrite an issued final verdict automatically'
io(target).write_text(json.dumps(verdict,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all(sha(D/p)==h for p,h in dmap.items()) and all(sha(C/p)==h for p,h in cmap.items())
print(json.dumps({'limited_completion_supported':True,'blocking_findings':0,'D_files':len(dmap),'C_files':len(cmap),'verdict_sha256':sha(target),'publisher_sha256':sha(publisher)},ensure_ascii=True))
