from pathlib import Path
import hashlib,json,re,urllib.parse
D=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
OUT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
files=[D/'00_시작안내.md',D/'01_진행현황.md',D/'02_운영규칙.md']
for folder in ['00_운영계약','01_공통용어','02_원칙과레이아웃','03_한맥디자인','04_기록규격','06_맞춤스킬','07_실행도구','09_다음단계인계','13_품질검수','14_스킬재구성']:
 files.extend((D/folder).rglob('*.md'))
links=[];missing=[]
for p in files:
 text=p.read_text(encoding='utf-8-sig')
 for n,line in enumerate(text.splitlines(),1):
  for match in re.finditer(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',line):
   dest=match[1].strip('<>');parts=urllib.parse.urlsplit(dest)
   if parts.scheme or dest.startswith('#'):continue
   rel=urllib.parse.unquote(parts.path);target=(p.parent/rel).resolve()
   if 'R8_04' in str(target):continue
   r={'source':p.relative_to(D).as_posix(),'line':n,'link':dest,'target':str(target),'exists':target.exists()};links.append(r)
   if not r['exists']:missing.append(r)
(OUT/'06_현행안내_링크실재검사.json').write_text(json.dumps({'documents':len(files),'local_links_checked':len(links),'missing':missing,'links':links,'scope':'현행 경로 목록. 링크 존재는 내용/승인/실영상검증이 아님. R8_04 시험폴더는 열지 않음.'},ensure_ascii=False,indent=2),encoding='utf-8')
receipts=[]
stages=['R8_01_큐레이터','R8_02_기록관리자','R8_03_적용성검토자']
backups=[p for p in (D/'backup').rglob('00_결과안내.md') if not any('R8_04' in part or 'R8-4' in part for part in p.parts)]
# 부모 감사자의 명시 요청: 시험 수행물/기대항목이 아닌 착수 직전 게시보고 원문만 해시 검증.
targeted=D/'backup/2026-10-15_R8_04_착수/변경전/Phase 00/08_검증결과/R8_03_적용성검토자/00_결과안내.md'
if targeted.exists():backups.append(targeted)
for folder in stages:
 base=D/'08_검증결과'/folder;receipt=base/'보존과최종연결_확인.json';report=base/'00_결과안내.md';r=read(receipt)
 # only report SHA/marker fields, no executor trials or expected items
 flat=[]
 def walk(v,prefix=''):
  if isinstance(v,dict):
   for k,x in v.items():
    if ('report' in k or '결과안내' in k) and isinstance(x,(str,bool,type(None))):flat.append({'pointer':prefix+'/'+k,'value':x})
    if k!='archived_hashes':walk(x,prefix+'/'+k)
  elif isinstance(v,list):
   for i,x in enumerate(v):walk(x,prefix+'/'+str(i))
 walk(r)
 expected=[x['value'] for x in flat if isinstance(x['value'],str) and re.fullmatch('[0-9a-f]{64}',x['value'])]
 candidates=[]
 for p in backups:
  if folder not in p.parts:continue
  h=sha(p)
  if h in expected:
   raw=p.read_bytes();now=report.read_bytes();candidates.append({'path':p.relative_to(D).as_posix(),'sha256':h,'byte_length':len(raw),'current_startswith_snapshot':now.startswith(raw),'current_extra_bytes':len(now)-len(raw),'snapshot_tail':raw[-200:].decode('utf-8',errors='replace')})
 marker=base/'게시상태.json';markerdata=read(marker) if marker.exists() else None
 receipts.append({'stage':folder,'report_path':report.relative_to(D).as_posix(),'current_report_sha256':sha(report),'receipt_path':receipt.relative_to(D).as_posix(),'current_receipt_sha256':sha(receipt),'receipt_report_fields':flat,'current_report_matches_expected_hash':sha(report) in expected,'matching_backup_candidates':candidates,'marker':markerdata,'marker_receipt_matches':markerdata.get('receipt_sha256')==sha(receipt) if markerdata else None,'report_tail':report.read_text(encoding='utf-8')[-850:]})
(OUT/'07_R8게시영수증_현재성감사.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'documents':len(files),'local_links':len(links),'missing':missing,'publication':[{'stage':r['stage'],'expected_fields':r['receipt_report_fields'],'report_matches':r['current_report_matches_expected_hash'],'matching_backups':r['matching_backup_candidates'],'marker_receipt_matches':r['marker_receipt_matches'],'tail':r['report_tail']} for r in receipts]},ensure_ascii=False,indent=2))
