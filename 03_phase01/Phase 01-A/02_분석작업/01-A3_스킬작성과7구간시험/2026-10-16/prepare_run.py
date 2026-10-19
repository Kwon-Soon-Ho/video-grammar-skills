from pathlib import Path
import json,shutil,hashlib,datetime
BASE=Path(__file__).resolve().parent
OLD=BASE.parent/'phase01a-a2-retest/analysis_input'
INP=BASE/'analysis_input';INP.mkdir(exist_ok=True)
def write(p,d):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads((OLD/'cases.json').read_text(encoding='utf-8'))
p.update(version='a3-1',purpose='A3 seven known-window skill regression',new_skill_available=True)
p['cases'].append(dict(p['cases'][0],case_id='T07',allowed_window_seconds=[8.2,10.4]))
prompt='이 영상 구간의 화면과 동작을 분석해 주세요. 눈에 보이는 대상과 시간에 따른 변화를 근거 시점과 함께 기록하고, 관측과 구현 추정을 구분해 주세요. 필요한 추가 원본 확인은 허용 구간 안에서 직접 진행하세요.'
for c in p['cases']:
    c['prompt']=prompt
    if c['case_id']!='T07':c['evidence_folder']=str(OLD/'cases'/c['asset_id']/c['case_id'])
    else:c['evidence_folder']=str(BASE/'runs/setup/cases/자료013/T07')
write(INP/'cases.json',p)
for name in ['bounded_base.py','inspect_more.py']:
    shutil.copy2(OLD/name,INP/name)
workspace=BASE/'company-video-grammar-analyzer-workspace'
write(workspace/'run-plan.json',{'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'user_authorization':'A3 스킬 작성, 기존6항목+UI선택변경 시험과 문제 보완','cases':[c['case_id'] for c in p['cases']],'paired_runs':True,'historical_baseline_reused_as_current':False,'concurrency':3,'scheduling':'four clean-context batches queued within same user turn; withA T01-03, withoutA T01-03, withB T04-07, withoutB T04-07','human_gold':'T01-T06 existing receipts only; T07 AI reference, not user-confirmed','no_unseen_generalization':True,'audio_reviewed':False})
for c in p['cases']:
    name=c['case_id']
    write(workspace/'iteration-1'/('eval-'+name)/'eval_metadata.json',{'eval_id':name,'eval_name':name,'prompt':prompt,'assertions':[]})
write(BASE/'skill-v1-hashes.json',{str(f.relative_to(BASE/'company-video-grammar-analyzer')):sha(f) for f in (BASE/'company-video-grammar-analyzer').rglob('*') if f.is_file()})
shutil.copytree(BASE/'company-video-grammar-analyzer',workspace/'skill-snapshot-v1')
ROOT=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
refs=['Phase 00/01_공통용어/공통용어사전.json','Phase 00/02_원칙과레이아웃/모션과정보전달원칙.json','Phase 00/04_기록규격/02_시간과프레임_기록규격.md','Phase 00/04_기록규격/03_근거와주장_기록규격.md','Phase 01-A/00_진행안내/13_Phase00와_기존스킬_활용표.md']
write(BASE/'knowledge-pins.json',[{'path':str(ROOT/r),'sha256':sha(ROOT/r)} for r in refs])
print('A3 prepared')
