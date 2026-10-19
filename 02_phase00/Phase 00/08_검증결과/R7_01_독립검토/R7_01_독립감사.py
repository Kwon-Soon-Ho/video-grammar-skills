import json,hashlib,sys,re
from pathlib import Path
BASE=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');OUT=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
AUDIT='08_검증결과/R7_01_착수감사.json';FOLDER='13_품질검수/'
audit=read(BASE/AUDIT);existing=audit['source_hashes'];backup=BASE/'backup/2026-10-15_R7_01_착수/입력정본'
rows=[{'path':r,'expected':h,'actual':sha(BASE/r),'backup':sha(backup/r),'same':h==sha(BASE/r)==sha(backup/r)} for r,h in existing.items()]
newrels=[FOLDER+x for x in ['00_R7_단계별진행안내.md','01_기존자료와_보완목록.md','02_품질판정방식_검토안.md']]+[AUDIT]
newrels.extend(p.relative_to(BASE).as_posix() for p in (BASE/FOLDER).glob('*.json'))
explicitread=['06_맞춤스킬/평가계획.json','08_검증결과/R7_최종반례검사.json','08_검증결과/R4_R5_반례검사.json','08_검증결과/R6_R7_최종레드팀.md','08_검증결과/Phase00_종료재감사.md','09_다음단계인계/R6_검수연결_인계.md','03_한맥디자인/영상전용_미정항목.json','02_원칙과레이아웃/00_지식안내.md','02_원칙과레이아웃/08_화면설계_적용기준과반례.md']
contents={r:(BASE/r).read_text(encoding='utf-8-sig') for r in sorted(set(newrels+explicitread))};hashes={r:sha(BASE/r) for r in contents}
lines={r:[{'line':n,'text':t} for n,t in enumerate(text.splitlines(),1) if any(w in t for w in ['39','13','26','핵심','필수','보류','비적용','사람','자동','승인','검토대기','확정','선택','A (추천)','D |'])] for r,text in contents.items()}
links=[]
for r in newrels:
 if r.endswith('.md'):
  for link in re.findall(r'\]\(([^)]+)\)',contents[r]):
   if not link.startswith(('http:','https:','#')):links.append({'file':r,'link':link,'exists':(BASE/r).parent.joinpath(link.split('#')[0]).resolve().exists()})
legacy13=read(BASE/'08_검증결과/R7_최종반례검사.json');legacy26=read(BASE/'08_검증결과/R4_R5_반례검사.json')
sys.path.insert(0,str(BASE/'07_실행도구'));import R6_통합조회 as q
before={r:sha(BASE/r) for r in set(existing)|set(newrels)|set(q.expected_paths(BASE))|{q.MANIFEST}}
current=q.inspect(BASE)
after={r:sha(BASE/r) for r in before}
result={'scope':'R7-1 static gap audit and existing byte-identity/read-only R6 context check. No quality criteria implementation, no media/meaning/identity/authority verification.','existing_selected_files':len(rows),'existing_current_and_backup_all_same':all(r['same'] for r in rows),'selected_file_checks':rows,'read_depth':{'fully_read_text_files':list(contents),'remaining_selected_files':'bytes/hash only in this R7-1 pass; prior R3-R6 reviews are referenced and not called a new semantic re-review'},'explicit_file_hashes':hashes,'line_evidence':lines,'links':links,'legacy_test_source_facts':{'R7_file':{'test_rows':len(legacy13['tests']),'total':legacy13['total'],'passed':legacy13['passed']},'R4_R5_file':{'test_rows':len(legacy26['tests']),'total':legacy26['total'],'passed':legacy26['passed']},'historical_report_total':legacy13['total']+legacy26['total'],'not_rerun_now':True,'not_current_quality_or_current_flaw_proof':True},'current_R6_query':current,'source_unchanged_during_audit':before==after,'before_hashes':before,'after_hashes':after}
(OUT/'R7_01_최종_원문대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'selected':len(rows),'byte_same':result['existing_current_and_backup_all_same'],'legacy13':legacy13['total'],'legacy26':legacy26['total'],'r6_valid':current['valid'],'unchanged':before==after,'bad_links':[r for r in links if not r['exists']]},ensure_ascii=True))

