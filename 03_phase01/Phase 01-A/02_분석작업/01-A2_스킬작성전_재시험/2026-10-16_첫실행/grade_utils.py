from pathlib import Path
import json,hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
HERE=Path(__file__).resolve().parent
ROOT=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
REF=ROOT/'Phase 01-A/06_도구와계약/01-A2_모션검수절차/스킬작성전_재발시험/채점전용/실패사례와_내용대조기준.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def grade(case,verdicts,claim_reviews,notes):
    ref=json.loads(REF.read_text(encoding='utf-8'));expected=next(c for c in ref['required_known_failure_cases'] if c['case_id']==case)
    seal=json.loads((HERE/'seals'/(case+'.json')).read_text(encoding='utf-8'));raw=Path(seal['source_path']);assert sha(raw)==seal['source_sha256'];assert sha(Path(seal['sealed_copy']))==seal['source_sha256']
    assert len(verdicts)==len(expected['must_check'])
    expectations=[]
    for text,v in zip(expected['must_check'],verdicts):
        assert isinstance(v['passed'],bool) and len(v['evidence'])>15
        expectations.append({'text':text,**v})
    count=sum(e['passed'] for e in expectations)
    result={'case_id':case,'graded_at':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds'),'grader':'parent Codex, source-aware content review; no independent human adjudication','frozen_reference_path':str(REF),'frozen_reference_sha256':sha(REF),'raw_output_sha256':seal['source_sha256'],'expectations':expectations,'summary':{'passed':count,'failed':len(expectations)-count,'total':len(expectations)},'claims':claim_reviews,'notes':notes,'source_review':'selected raw temporal PNGs/native crops and measurements; no audio or full realtime playback claim','scope':'known-case baseline regression, not new skill effectiveness or unseen-source accuracy','case_status':'충족' if count==len(expectations) and not any(c.get('critical_error',False) for c in claim_reviews) else '미충족/보류','executor_tokens':None,'executor_duration_seconds':None,'telemetry_status':'not reported by collaboration tool; not estimated from output length'}
    out=HERE/'evaluation/iteration-1'/('eval-'+case)/'without_skill'
    if (out/'grading.json').exists():raise ValueError('preserve_first_grading')
    write(out/'grading.json',result)
    meta=json.loads((out.parent/'eval_metadata.json').read_text(encoding='utf-8'));meta['assertions']=expected['must_check'];meta['reference_frozen_before_run']=True;write(out.parent/'eval_metadata.json',meta)
    return result
