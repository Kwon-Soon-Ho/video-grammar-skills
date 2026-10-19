from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;it=R/'company-video-grammar-analyzer-workspace/iteration-4'
for e in it.glob('eval-*'):
    for config in ['with_skill','old_skill']:assert (e/config/'execution.md').is_file()
p=R/'candidate/company-video-grammar-analyzer/evals/evals.json';d=json.loads(p.read_text(encoding='utf-8'))
for e in d['evals']:
    meta=json.loads(next(it.glob(f"eval-{e['id']}-*/eval_metadata.json")).read_text(encoding='utf-8'))
    e['expected_output']='원본/기존 상세와 의미를 보존한 Markdown 수집 기록, 현재 사용처/근거/차이를 찾는 작동 조회, 관련 지식과 실제 판정의 분리'
    e['assertions']=meta['assertions']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
before=json.loads((R/'eval-new-skill-pin.json').read_text(encoding='utf-8'))
changed=[x['path'] for x in before if hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()!=x['sha256']]
assert changed==[str(p)],changed
(R/'eval-freeze-notes.json').write_text(json.dumps({'runtime_files_unchanged_during_runs':True,'metadata_only_finalization':changed,'change':'실행 종료 뒤 동일 prompt/files에 expected_output과 사전 정의한 assertions 추가. SKILL/참조/코드 변경 없음.','timing_and_tokens_available':False,'fresh_context_execution_count':4,'runs_per_prompt_and_variant':1},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('eval metadata finalized; runtime skill files remained pinned during four executions')
