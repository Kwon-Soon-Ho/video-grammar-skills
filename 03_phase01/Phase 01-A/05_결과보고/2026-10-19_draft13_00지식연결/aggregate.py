from pathlib import Path
import json,statistics,datetime
R=Path(__file__).resolve().parent;IT=R/'company-video-grammar-analyzer-workspace/iteration-4';runs=[]
for e in sorted(IT.glob('eval-*')):
    meta=json.loads((e/'eval_metadata.json').read_text(encoding='utf-8'))
    for config in ['with_skill','old_skill']:
        g=json.loads((e/config/'grading.json').read_text(encoding='utf-8'));ex=g['expectations']
        assert [x['text'] for x in ex]==meta['assertions'] and len(ex)==12
        n=sum(x['passed'] is True for x in ex)
        runs.append({'eval_id':meta['eval_id'],'eval_name':meta['eval_name'],'configuration':config,'run_number':1,'result':{'passed':n,'failed':12-n,'total':12,'pass_rate':n/12},'expectations':ex})
summary={}
for c in ['with_skill','old_skill']:
    values=[x['result']['pass_rate'] for x in runs if x['configuration']==c]
    summary[c]={'pass_rate':{'mean':statistics.mean(values),'stddev':statistics.pstdev(values),'min':min(values),'max':max(values)}}
summary['delta']={'pass_rate':f"{summary['with_skill']['pass_rate']['mean']-summary['old_skill']['pass_rate']['mean']:+.2f}"}
notes=[
 'with_skill=draft.13; old_skill=draft.12. Each prompt/version executed once in fresh context; grading by separate AI agents, not blinded or human approval.',
 'New prompts test knowledge-to-record-to-usage-to-review. Previous iteration used different prompts; previous outputs are not joined by reused eval IDs.',
 'Runtime skill files stayed pinned during all four executions. Only eval metadata was finalized afterward; see eval-freeze-notes.json.',
 'Both variants satisfy all 12 criteria for each known-material task. No superiority or broader perception accuracy is established.',
 'Beyond the 12 criteria, new static self-report has two wrong extra-hit descriptions and one overly broad file-version label; old motion overstates unavailability of accessible 112-second evidence. See separate errata/claims.',
 'Review fields/scope do not prove actual guidance applicability: new MR-04 pass is record-fidelity review. Further tests should distinguish that from answering the principle question.',
 'Exact executor model/token/time telemetry is absent; no zeros or character proxies substitute for it. Execution.md is a self-report, not a full raw tool transcript.',
 'Draft13 bundled catalog/check/index/query reduce task-specific helper duplication. Reuse is observed; time/cost savings were not measured.',
 'Parent-edited pilot is separate from scored agent outputs. No canonical registration, active10 replacement, whole-video expansion, PDF or new design production.'
]
data={'metadata':{'skill_name':'company-video-grammar-analyzer','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'evals_run':[1,2],'runs_per_configuration':1,'rubric_version':'phase00-links-1','executor_model':None,'analyzer_model':None},'runs':runs,'run_summary':summary,'notes':notes}
(IT/'benchmark.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 00 지식 연결 — 실제 실행 비교','','| 과제 | 판본 | 수집/연결 기준 |','|---|---|---|']
for r in runs:lines.append(f"| {r['eval_name']} | {'draft.13' if r['configuration']=='with_skill' else 'draft.12'} | {r['result']['passed']}/12 |")
lines+=['','두 과제 모두 동률이다. 이는 같은 알려진 영상/기존 기록의 연결 기능 시험이다. 별도 설명 오류/판정 실질성 문제는 점수 밖 정정표에 남겼다. 숫자만으로 전체 정확도/전문가 판단 완성을 말하지 않는다.','','## 해석 범위','']+['- '+n for n in notes]
(IT/'benchmark.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines[:9]))
