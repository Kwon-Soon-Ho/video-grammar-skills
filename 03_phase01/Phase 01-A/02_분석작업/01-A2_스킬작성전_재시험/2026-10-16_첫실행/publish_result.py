from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil
HERE=Path(__file__).resolve().parent
ROOT=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
AN=Path('Phase 01-A/02_분석작업/01-A2_스킬작성전_재시험/2026-10-16_첫실행')
PRE=Path('Phase 01-A/06_도구와계약/01-A2_모션검수절차/스킬작성전_재발시험')
REPORT=Path('Phase 01-A/05_결과보고/12_01-A2_스킬작성전_재시험_결과.md')
NOTICE=Path('Phase 01-A/00_진행안내/19_01-A2_스킬작성전_재시험_현재안내.json')
IMPORTANT=Path('작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A2/보완과_재시험')
now=datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def guard(p):
    q=p.resolve();assert q.is_relative_to(ROOT) and q!=ROOT;return q
dest=guard(ROOT/AN);assert not dest.exists(),'Never replace a preserved first-run snapshot'
result=read(HERE/'재시험_결과.json');assert result['known_required_cases_all_satisfied'] and not result['A3_started'] and not result['skill_created']
write(HERE/'사용자_실행지시.json',{'recorded_at':now,'source':'latest human user message in current conversation','verbatim':'재시험 한 다음 결과 보고 a3넘어갈지 판단할게. 진행해','authorized':'run prepared regression and report results','A3_decision':'reserved to user; no skill creation authorized this turn'})
entries=[]
for p in sorted(HERE.rglob('*')):
    if p.is_file() and p.name not in {'보존_파일목록.json','정본_저장결과.json'} and '__pycache__' not in p.parts:entries.append({'path':p.relative_to(HERE).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
write(HERE/'보존_파일목록.json',{'recorded_at':now,'files':entries,'scope':'snapshot files before publication; manifest/receipt self-hashes excluded','snapshot_root':str(dest),'source_root':str(HERE)})
shutil.copytree(HERE,dest,ignore=shutil.ignore_patterns('__pycache__','정본_저장결과.json'))
for item in entries:assert sha(dest/item['path'])==item['sha256']
backup=guard(ROOT/'Phase 01-A/04_검증자료/01-A2_스킬작성전_재시험/업데이트전_기록');backup.mkdir(parents=True,exist_ok=False)
mutable=[Path('Phase 01-A/00_진행안내/01-A_계획상태.json'),PRE/'02_현재판정.json',Path('00기획/07_Phase01-A_진행계획.md'),Path('Phase 01-A/00_진행안내/18_01-A2_스킬작성전_통과조건_현재안내.json'),PRE/'00_스킬작성전_통과조건.md',Path('Phase 01-A/05_결과보고/11_01-A3_작성전_실패재발_통과조건.md')]
backups=[]
for rel in mutable:
    src=guard(ROOT/rel);dst=guard(backup/rel);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);backups.append({'original':rel.as_posix(),'backup':str(dst.relative_to(ROOT)).replace('\\','/'),'sha256':sha(src)})
write(backup/'백업_목록.json',{'recorded_at':now,'files':backups})
notice={'date':now,'state':result['state'],'report':REPORT.as_posix(),'result':(AN/'재시험_결과.json').as_posix(),'viewer':(AN/'재시험_검토화면.html').as_posix(),'decision':(PRE/'02_현재판정.json').as_posix(),'A3_started':False,'skill_created':False,'A3_authoring_ready':True,'A3_authoring_ready_scope':result['A3_authoring_ready_scope'],'new_behavior_replay_run':True,'known_required_cases_all_satisfied':True,'user_stage_decision':'pending','prior_human_confirmations_preserved':True,'questions_to_repeat_to_user':[],'coverage_gaps':result['coverage_gaps']}
write(guard(ROOT/NOTICE),notice)
write(guard(ROOT/PRE/'03_재시험_결과.json'),result)
decision=read(ROOT/PRE/'02_현재판정.json');decision.update({'recorded_at':now,'new_procedure_behavior_replay':'performed_new_outputs_sealed_before_grading','content_grading':'performed; all six known-case requirements satisfied','independent_or_unseen_validation':'not_run','A3_authoring_ready':True,'A3_authoring_ready_scope':result['A3_authoring_ready_scope'],'skill_created':False,'A3_started':False,'reason':'Known-case content gate satisfied. Limited A3 draft recommended; user decides whether to begin. No overall or unseen-source accuracy claim.','next_action':result['recommended_next_step'],'result':(AN/'재시험_결과.json').as_posix(),'coverage_gaps':result['coverage_gaps'],'user_stage_decision':'pending'})
write(ROOT/PRE/'02_현재판정.json',decision)
statep=ROOT/'Phase 01-A/00_진행안내/01-A_계획상태.json';state=read(statep)
state.update({'version':'1.0','state':result['state'],'next_decision':'사용자가 재시험 결과를 보고 A3 초안 작성 착수 여부 결정','stage_A2_status':'스킬 작성 전 중립 실제 재시험6건과 내용 채점 완료. 필수 사건 충족; 정확한 곡선과 UI8.2~10.4초 시험 공백 보존.','stage_A2_report':str(REPORT.relative_to('Phase 01-A')).replace('\\','/'),'stage_A2_current_notice':str(NOTICE.relative_to('Phase 01-A')).replace('\\','/'),'A3_authoring_ready':True,'A3_authoring_ready_scope':result['A3_authoring_ready_scope'],'A3_started':False,'skill_created':False,'current_stage':'01-A2','stage_A2_known_case_regression_cases':6,'stage_A2_known_case_regression_status':'all six mandatory content criteria satisfied; baseline only','stage_A2_known_case_regression_result':(AN/'재시험_결과.json').as_posix(),'stage_A2_regression_fresh_pngs':228,'stage_A2_regression_unique_times':188,'stage_A2_regression_counting_basis':'separate new baseline run;228 selected PNGs,174 base+54 adaptive native,188 unique times within run; not added to previous unique-time totals','human_content_reviews_pending':0,'user_A3_stage_decision':'pending','independent_redteam_performed':False,'pre_skill_acceptance_state':(PRE/'02_현재판정.json').as_posix()})
write(statep,state)
oldnoticep=ROOT/'Phase 01-A/00_진행안내/18_01-A2_스킬작성전_통과조건_현재안내.json';oldnotice=read(oldnoticep);oldnotice['superseded_by']=NOTICE.as_posix();oldnotice['historical_notice']=True;write(oldnoticep,oldnotice)
reportp=guard(ROOT/REPORT);assert not reportp.exists();reportp.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(HERE/'결과보고.md',reportp)
ve=guard(ROOT/'Phase 01-A/04_검증자료/01-A2_스킬작성전_재시험');write(ve/'결과_요약.json',result);shutil.copy2(HERE/'실행감사.json',ve/'실행감사.json');shutil.copy2(HERE/'검토화면_파일확인.json',ve/'검토화면_파일확인.json')
imp=guard(ROOT/IMPORTANT);imp.mkdir(parents=True,exist_ok=True);shutil.copy2(HERE/'결과보고.md',imp/'스킬작성전_재시험_결과.md');write(imp/'스킬작성전_재시험_결과.json',result)
plan=ROOT/'00기획/07_Phase01-A_진행계획.md';old=plan.read_text(encoding='utf-8-sig')
new='> 2026-10-16 현재 상태: 01-A2 스킬 작성 전 중립 재시험6건과 내용 채점을 완료했고 필수 기준을 충족했습니다. **A3 초안 작성은 권고 상태이며, 착수 여부는 사용자 판단 대기입니다. A3/스킬 생성은 미실행입니다.** [재시험 결과](../Phase%2001-A/05_결과보고/12_01-A2_스킬작성전_재시험_결과.md)를 우선 적용합니다. UI8.2~10.4초 선택 변경은 이번 시험 밖이고 정확한 원본 곡선·전체/미노출 검증은 남아 있습니다. 아래 이전 상태 문구는 이력입니다.\n\n'
plan.write_text(new+old,encoding='utf-8')
for rel in [PRE/'00_스킬작성전_통과조건.md',Path('Phase 01-A/05_결과보고/11_01-A3_작성전_실패재발_통과조건.md')]:
    p=ROOT/rel;txt=p.read_text(encoding='utf-8-sig');p.write_text('> 2026-10-16 재시험 후 안내: 아래는 시험 준비 당시의 기록입니다. 현재는6개 필수 기준 내용 대조 완료/충족, A3는 사용자 판단 대기입니다. 최신 결과: '+str(ROOT/REPORT).replace('\\','/')+'\n\n'+txt,encoding='utf-8')
for item in entries:assert sha(dest/item['path'])==item['sha256']
receipt={'saved_at':now,'snapshot':str(dest),'snapshot_files_verified':len(entries),'total_snapshot_bytes':sum(e['bytes'] for e in entries),'report':str(reportp),'notice':str(ROOT/NOTICE),'prior_mutable_records_backed_up':len(backups),'first_outputs_unchanged':True,'A3_started':False,'skill_created':False,'user_A3_decision':'pending'}
write(HERE/'정본_저장결과.json',receipt);write(dest/'정본_저장결과.json',receipt);write(ve/'정본_저장결과.json',receipt)
print(json.dumps(receipt,ensure_ascii=False))
