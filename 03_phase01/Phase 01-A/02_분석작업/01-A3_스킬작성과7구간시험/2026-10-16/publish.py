"""Publish authorized A3 artifacts and update current pointers, preserving history."""
from pathlib import Path
import json,hashlib,shutil,datetime
B=Path(__file__).resolve().parent
R=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
AN=Path('Phase 01-A/02_분석작업/01-A3_스킬작성과7구간시험/2026-10-16')
SD=Path('Phase 01-A/03_분석스킬')
REPORT=Path('Phase 01-A/05_결과보고/13_01-A3_분석스킬_7구간시험_결과.md')
NOTICE=Path('Phase 01-A/00_진행안내/20_01-A3_스킬작성과시험_현재안내.json')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def guard(p):
    q=p.resolve();assert q.is_relative_to(R) and q!=R;return q
result=read(B/'result.json');assert result['authorized_A3'] and result['final_skill_version'] and result['all_requested_cases_tested']
assert not read(B/'execution-audit.json')['errors']
dest=guard(R/AN);assert not dest.exists(),'do not overwrite preserved run'
timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
write(B/'user-authorization.json',{'recorded_at':timestamp,'verbatim':'그럼 A3로 넘어가서 스킬 만들어줘. 이번 6개 항목이랑 빠진 UI 선택 변경 구간까지 그 스킬로 테스트하고, 문제 있으면 보완해줘.','scope':'A3 draft creation + seven-window tests + improvements','A4_started':False})
write(B/'path-mapping.json',{'local_run':str(B),'preserved_run':str(dest),'skill':str(R/SD/'company-video-grammar-analyzer'),'note':'Original outputs retain exact C paths/hashes. Shared six-case inputs remain under phase01a-a2-retest and its already-preserved canonical snapshot. No raw video copies.'})
entries=[{'path':p.relative_to(B).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in B.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ['publication-manifest.json','publication-receipt.json']]
write(B/'publication-manifest.json',{'files':entries,'self_hash_excluded':True})
shutil.copytree(B,dest,ignore=shutil.ignore_patterns('__pycache__','publication-receipt.json'))
for e in entries:assert sha(dest/e['path'])==e['sha256']
for name in ['company-video-grammar-analyzer','company-video-grammar-analyzer-workspace']:
    target=guard(R/SD/name);assert not target.exists();shutil.copytree(B/name,target,ignore=shutil.ignore_patterns('__pycache__'))
backup=guard(R/'Phase 01-A/04_검증자료/01-A3_7구간시험/업데이트전');backup.mkdir(parents=True,exist_ok=False)
mutable=[Path('Phase 01-A/00_진행안내/01-A_계획상태.json'),Path('00기획/07_Phase01-A_진행계획.md'),Path('Phase 01-A/00_진행안내/19_01-A2_스킬작성전_재시험_현재안내.json')]
for rel in mutable:
    target=backup/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(guard(R/rel),target)
state=read(R/mutable[0]);state.update({'version':'1.1','state':'A3_draft_created_seven_window_tested_and_improved','current_stage':'01-A3','A3_started':True,'skill_created':True,'analyzer_implementation_started':True,'user_A3_stage_decision':'authorized','approved_execution_scope':'A3 draft + six known cases and UI selection case tests and fixes; no A4/A5 execution','implementation_scope':'project-local A3 analysis skill and evidence/observation checkers; bounded A2 extraction adapter reused','stage_A3_status':result['status'],'stage_A3_report':REPORT.as_posix(),'stage_A3_current_notice':NOTICE.as_posix(),'stage_A3_skill':str(SD/'company-video-grammar-analyzer/SKILL.md').replace('\\','/'),'stage_A3_skill_version':result['final_skill_version'],'stage_A3_result':str(AN/'result.json').replace('\\','/'),'A4_started':False,'default_skill_promotion':False,'phase00_modified':False,'next_decision':'review A3 report; broader unseen-source A4 validation remains separate','A3_authoring_ready_scope':'historical A2 gate superseded by explicit user A3 authorization','human_content_reviews_pending':0,'human_content_reviews_pending_unit':'no mandatory repeat questions; new AI observations not human-approved'})
write(guard(R/mutable[0]),state)
old=read(R/mutable[2]);old.update({'historical_notice':True,'superseded_by':NOTICE.as_posix(),'superseded_note':'A3 user approval, skill creation and tests recorded in notice20; historical A2 result preserved.'});write(guard(R/mutable[2]),old)
plan=R/mutable[1];plan.write_text('> 최신: 사용자 지시로 01-A3 스킬 작성·7구간 시험·보완을 수행했습니다. 현재 결과는 [A3 결과 보고](../'+REPORT.as_posix()+')와 20번 현재안내를 따릅니다. 아래 A3 미착수/사용자 결정 대기는 당시 이력입니다.\n\n'+plan.read_text(encoding='utf-8'),encoding='utf-8')
notice={'date':timestamp,'state':state['state'],'report':REPORT.as_posix(),'skill':state['stage_A3_skill'],'result':state['stage_A3_result'],'A3_started':True,'skill_created':True,'skill_version':result['final_skill_version'],'A4_started':False,'new_UI_case_reference':'AI source observation, not human-confirmed','questions_to_repeat_to_user':[],'viewer':str(AN/'skill-review.html').replace('\\','/')}
write(guard(R/NOTICE),notice)
guard(R/REPORT).write_text((B/'report.md').read_text(encoding='utf-8'),encoding='utf-8')
important=guard(R/'작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A3');important.mkdir(parents=True,exist_ok=True)
shutil.copy2(B/'report.md',important/'스킬작성_7구간시험_결과.md');shutil.copy2(B/'result.json',important/'결과.json')
receipt={'copied_files':len(entries),'bytes':sum(e['bytes'] for e in entries),'hashes_verified':True,'snapshot':str(dest),'report':str(R/REPORT),'skill':str(R/SD/'company-video-grammar-analyzer/SKILL.md'),'phase00_unchanged':True}
write(B/'publication-receipt.json',receipt);write(dest/'publication-receipt.json',receipt);print(json.dumps(receipt,ensure_ascii=False))
