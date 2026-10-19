from pathlib import Path
import json,hashlib,collections
P=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00')
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
ledger=read(P/'05_출처와검토/스킬심층검토/검토파일목록.json')
checks=[]
aliases={r['old_record_path']:r for r in read(P/'05_출처와검토/검수와사용범위/원문경로_복구연결.json')['aliases']}
for row in ledger['records']:
    f=Path(row['absolute_path']); actual=hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None
    alias=aliases.get(row['path']) or aliases.get(row['absolute_path'])
    recovery=P/alias['preserved_snapshot'] if alias else None
    recovered=hashlib.sha256(recovery.read_bytes()).hexdigest() if recovery and recovery.exists() else None
    checks.append(dict(path=row['path'],depth=row['depth'],expected=row['sha256'],actual=actual,match=actual==row['sha256'],recovery_path=str(recovery) if recovery else None,recovery_sha256=recovered,resolved_match=actual==row['sha256'] or recovered==row['sha256']))
(R/'data').mkdir(exist_ok=True)
(R/'data/source-file-integrity.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print('ledger',len(checks),'match',sum(c['match'] for c in checks),'depths',dict(collections.Counter(c['depth'] for c in checks)))
for f in ['공통용어사전.json','모션과정보전달원칙.json','화면설계원칙.json','레이아웃지식.json','모션원칙_심화카드.json','추가모션체계_연결후보.json','품질항목_정본.json']:
    parent='01_공통용어' if f=='공통용어사전.json' else ('13_품질검수' if f=='품질항목_정본.json' else '02_원칙과레이아웃')
    d=read(P/parent/f);print(f,{k:len(v) if isinstance(v,list) else type(v).__name__ for k,v in d.items()})
    if f in ['레이아웃지식.json','화면설계원칙.json']:print(str(d)[:1700])
cards=read(P/'05_출처와검토/스킬심층검토/스킬심층검토정본.json')['cards']
print('CARDS',[(i,c['id'],c['source_package']) for i,c in enumerate(cards)])
for r in ledger['records']:
    if r['path'].endswith('SKILL.md') and any(s in r['path'] for s in ['antv','presentation-narrative']): print('EXTRA',r['absolute_path'])
