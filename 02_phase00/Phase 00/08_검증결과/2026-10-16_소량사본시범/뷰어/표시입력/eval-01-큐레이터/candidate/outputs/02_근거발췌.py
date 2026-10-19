import json
from pathlib import Path

RUN = Path(__file__).resolve().parent.parent
BASE = RUN / 'inputs' / 'Phase00'
OUT = RUN / 'outputs'
terms = ['LAYOUT-PROCESS-LINE', 'FUNCTION-FOCUS', 'PROPERTY-VISIBILITY']
criteria = json.loads((BASE / '01_공통용어/용어판정기준.json').read_text(encoding='utf-8-sig'))
taxonomy = json.loads((BASE / '01_공통용어/공통용어사전.json').read_text(encoding='utf-8-sig'))
layout = json.loads((BASE / '02_원칙과레이아웃/레이아웃지식.json').read_text(encoding='utf-8-sig'))
deep = json.loads((BASE / '02_원칙과레이아웃/레이아웃_심화지식.json').read_text(encoding='utf-8-sig'))
selected = {
    'taxonomy': {'path': '01_공통용어/공통용어사전.json', 'version': taxonomy['version'], 'read_depth': 'three full term records, axes and source metadata', 'records': [t for t in taxonomy['terms'] if t['id'] in terms]},
    'criteria': {'path': '01_공통용어/용어판정기준.json', 'version': criteria['version'], 'interpretation': criteria['interpretation'], 'read_depth': 'three full guide records', 'records': [t for t in criteria['guides'] if t['term_id'] in terms]},
    'layout': {'path': '02_원칙과레이아웃/레이아웃지식.json', 'version': layout['version'], 'read_depth': 'linear process full record', 'records': [t for t in layout['layouts'] if t['term_id'] == terms[0]]},
    'layout_deep': {'path': '02_원칙과레이아웃/레이아웃_심화지식.json', 'version': deep['version'], 'authority': deep['authority'], 'read_depth': 'linear process full card and root authority/approval metadata', 'records': [t for t in deep['layout_cards'] if t['term_id'] == terms[0]]},
}
(OUT / '내용근거_확인절과판본.json').write_text(json.dumps(selected, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(selected, ensure_ascii=False, indent=2))

print('\nCORRECTION RELEVANT TEXT')
for rel in ['04_기록규격/06_통합최소기록_규격_v0.2.md', '08_검증결과/R4_04_보완결과와레드팀.md', '01_공통용어/02_기록단위와분류축.md']:
    text = (BASE / rel).read_text(encoding='utf-8-sig')
    print('\nFILE ' + rel)
    print(text)
contract = json.loads((BASE / '04_기록규격/통합최소기록_설명용_v0.2.json').read_text(encoding='utf-8-sig'))
print('\nJSON CONTRACT SELECTED: /spatial_contract/evidence_contract/targets and /units target_ref/related_state_refs')
print(json.dumps({'targets': contract['spatial_contract']['evidence_contract']['targets'], 'units': [{'target_ref': u['target_ref'], 'related_state_refs': u['related_state_refs']} for u in contract['units']]}, ensure_ascii=False, indent=2))
print('\nSOURCE TOOL ROOT AND ENTRYPOINT EXCERPTS ONLY; NOT EXECUTED')
tool_lines = (BASE / '07_실행도구/자료검증.py').read_text(encoding='utf-8-sig').splitlines()
hits = set()
for i, line in enumerate(tool_lines):
    if ('BASE =' in line or 'def validate_catalogs' in line or 'if __name__' in line):
        hits.update(range(max(0, i-1), min(len(tool_lines), i+15)))
for i in sorted(hits):
    print(f'{i+1}: {tool_lines[i]}')
