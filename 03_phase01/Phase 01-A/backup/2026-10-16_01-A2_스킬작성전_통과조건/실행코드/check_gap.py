from pathlib import Path
import json,importlib.util,copy
ROOT=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증');HERE=Path(__file__).resolve().parent
OP=ROOT/'Phase 01-A/06_도구와계약/01-A2_모션검수절차'
spec=importlib.util.spec_from_file_location('saved_record_validator',OP/'validate.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
reg=json.loads((OP/'01_대상목록.json').read_text(encoding='utf-8'));matrix=json.loads((OP/'02_속성검수표.json').read_text(encoding='utf-8'));controls=json.loads((OP/'04_회귀확인_과거누락.json').read_text(encoding='utf-8'))
tests=[]
for name,id,key,value in [('cursor_false_static','E-cursor','이동','커서는 제자리에 머물며 독립 이동이 전혀 없는 정지 요소다.'),('fragment_wrong_direction','E-hero-middle','이동','오른쪽에서 왼쪽으로 들어와서 정착하는 조각이다.'),('UI_selection_denied','E-ui1-thumb','내부변화','미리보기 선택 대상은 처음부터 끝까지 바뀌지 않고 유지된다.')]:
    mutant=copy.deepcopy(matrix);next(r for r in mutant['rows'] if r['id']==id)['axis_checks'][key]=value
    errors=module.check(reg,mutant,controls,True)
    tests.append({'case':name,'changed_subject':id,'changed_axis':key,'false_text':value,'old_structure_validator_errors':errors,'old_structure_validator_missed_content_error':not errors})
assert all(t['old_structure_validator_missed_content_error'] for t in tests)
result={'kind':'isolated diagnostic of existing validator; not actual model/video replay','original_files_modified':False,'counterexamples':tests,'conclusion':'A populated object/axis/evidence record can still describe the wrong motion. Structural success is not a pre-skill content acceptance result.'}
(HERE/'기존검사_내용오류_반례.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'isolated_counterexamples':len(tests),'content_errors_missed_by_structure_check':sum(not t['old_structure_validator_errors'] for t in tests)},ensure_ascii=False))
