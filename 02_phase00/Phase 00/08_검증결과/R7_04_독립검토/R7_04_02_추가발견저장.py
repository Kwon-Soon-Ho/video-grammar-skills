import json,hashlib
from pathlib import Path
O=Path(__file__).parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
j={'stage':'R7-4-2 추가 내용/CLI 발견','findings':[{'id':'F3','priority':'P2','basis':'13_품질검수/03_판정운영기준.md 항목 결과에 필요한 정보: 판단 방법과 담당 역할','affected':'품질검수_작성양식.json blank_fields','finding':'방법/담당 역할 필드가없고 findings에담으라는명시규칙도없음. human_review_scope/state와구분필요','suggestion':'review_method/reviewer_role 빈칸추가 또는 findings의필수하위구조명시; 역할선언은실제신원인증이아님'}, {'id':'F4','priority':'P2','basis':'CLI ensure_ascii=False + FileNotFoundError includes arbitrary base path','input':'nonexistent C base path containing emoji; PYTHONIOENCODING=cp949','actual':'exit1 but UnicodeEncodeError/no JSON output','suggestion':'CLI ensure_ascii=True for serialized diagnostics; do not normalize original source'}],'earlier65conditions':'pass65/65/exception0 at v0.1.2 remains historical structure test, not full final content pass','evidence':[{'path':str(O/n),'sha256':sha(O/n)} for n in ['R7_04_02_최종_독립반례코드.py','R7_04_02_최종_독립반례결과.json','R7_04_02_CLI_인코딩반례.py','R7_04_02_CLI_인코딩_초기반례.json']]}
(O/'R7_04_02_追加_발견사항.json'.replace('追加','추가')).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Freeze the previously passed v0.1.2 65-condition history before later re-run.
for name in ['R7_04_02_최종_독립반례코드.py','R7_04_02_최종_독립반례결과.json']:
 dest=O/'R7_04_02_v0.1.2_65조건이력'/name;dest.parent.mkdir(exist_ok=True);dest.write_bytes((O/name).read_bytes())
print('additional_findings_saved_and_v012_65_preserved')
