from pathlib import Path
import sys,json,shutil
BASE=Path(__file__).resolve().parent
OLD=BASE.parent/'phase01a-a2'
text=(OLD/'prepare.py').read_text(encoding='utf-8').split('def main():')[0]
text=text.replace('size<=2*1024**3','size<=3*1024**3')
(BASE/'prepare.py').write_text(text,encoding='utf-8')
sys.path.insert(0,str(BASE))
from prepare import ROOT,sha,write,preflight
reg=json.loads((ROOT/'Phase 01-A/00_진행안내/09_제공자료_묶음목록.json').read_text(encoding='utf-8-sig'))
selected=[('A4-D','자료010','1.크레인 작업 반경, 물류·인양 안정성 검토.mp4'),('A4-L','자료017','[EG-Bim]소개영상.mp4'),('A4-S','자료022','3. [기술개발센터] 홍보 영상(싱글)-KR(2026.09)-V3.0_한맥가족.mp4'),('A4-W','자료022','1. [기술개발센터] 홍보 영상(듀얼)-KR(2026.09) -V3.0_한맥가족.mp4'),('A4-G','자료013','02_(G).mp4')]
manifest=[]
for uid,aid,name in selected:
 card=next(c for c in reg['cards'] if c['id']==aid)
 matches=[p for p in card['videos'] if Path(p).name==name]
 assert len(matches)==1,(aid,name,matches)
 p=(ROOT/matches[0]).resolve(strict=True)
 assert p.is_relative_to(ROOT.resolve()) and not p.is_symlink()
 gate=preflight(p)
 row={'id':uid,'registration_id':aid,'registered_relative_path':matches[0],'path':str(p),'size':p.stat().st_size,'sha256':sha(p),'container_preflight':gate}
 manifest.append(row)
 print(json.dumps({'id':uid,'duration':int(gate['movie']['duration'])/gate['movie']['timescale'],'tracks':[{'size':[t['tkhd']['width_fixed16']/65536,t['tkhd']['height_fixed16']/65536],'edits':t.get('edits')} for t in gate['tracks']]},ensure_ascii=False),flush=True)
write(BASE/'manifest.json',manifest)
skill=ROOT/'Phase 01-A/03_분석스킬/company-video-grammar-analyzer'
shutil.copytree(skill,BASE/'skill-draft2')
for doc in ['DOC063','DOC066','DOC071']:
 for ext in ['json','txt']:
  p=BASE.parent/'phase01a-docreview/본문'/f'{doc}.{ext}'
  d=BASE/'documents'/p.name;d.parent.mkdir(exist_ok=True);shutil.copy2(p,d)
write(BASE/'adapter-scope.json',{'file_limit_bytes':3*1024**3,'why':'Registered source022 single and dual exceed previous 2 GiB. All other progressive MP4 preflight checks preserved. Decoder and read budget remain bounded.','parser_base_sha256':sha(OLD/'prepare.py'),'files_allowlisted':[r['path'] for r in manifest],'holdout_sources_not_opened':['자료011','자료014']})
