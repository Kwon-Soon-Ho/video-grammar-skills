import json,hashlib
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent;e=json.loads((O/'R7_04_02_초기_독립반례결과.json').read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();old=B/'backup/2026-10-15_R7_04_2_연결확인도구/변경전/Phase 00';evidence=[]
for rel in ['07_실행도구/R7_연결확인.py','13_품질검수/연결과인계/현재연결_입력고정.json']:
 source=old/rel;dest=O/'R7_04_02_정확한초기후보원문'/rel;dest.parent.mkdir(parents=True,exist_ok=True)
 assert sha(source)==e['before_hashes'][rel]
 dest.write_bytes(source.read_bytes());evidence.append({'path':rel,'source_backup':str(source),'sha256':sha(dest),'matches_initial_test':True})
(O/'R7_04_02_초기원문_복구증거.json').write_text(json.dumps({'scope':'초기검사후보완배포되어초기사본에보완중간본이혼합된2개파일은초기성적hash와같은변경전backup에서추가보존.혼합보존본/초기결과는수정하지않음.','restored':evidence},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('recovered_initial_sources',len(evidence))
