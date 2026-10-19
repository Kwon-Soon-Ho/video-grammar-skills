from pathlib import Path
from copy import deepcopy
import hashlib,json,sys,subprocess
from PIL import Image,ImageChops
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
sys.path.insert(0,str(OUT/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import check
from check_design_details import check as check_design
from render_observations import render
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
checks=[]
def ok(name,v):
 checks.append({'name':name,'passed':bool(v)})
 if not v:raise AssertionError(name)
inputs=load(OUT/'inputs.json');catalog=load(ROOT/'case-benchmarks-20261019/evidence-catalog.json')
for code in ['NEW-N','NEW-P']:
 p=OUT/'records'/code/'observations.json';d=load(p);a=load(p.with_name('design-details.json'));base=load(a['base_record']['path'])
 ok(code+' full record/provenance/addendum',not check(d,catalog))
 ok(code+' preserved IDs and definition pins',[(x['id'],x['pattern_id'],x['pattern_sha256'],x['library_sha256']) for x in d['pattern_refs']]==[(x['id'],x['pattern_id'],x['pattern_sha256'],x['library_sha256']) for x in base['pattern_refs']])
 ok(code+' no false content completion',d['review']['claim_denominator_complete'] is False and a['scope']['new_continuous_video_coverage'] is False)
 # Concrete corruptions that would otherwise silently poison reconstruction measurements.
 bad=deepcopy(a);del bad['dimensions']['spacing'];ok(code+' rejects missing spacing',bool(check_design(bad)))
 bad=deepcopy(a);bad['regions'][0]['bbox_ltrb'][2]=99999;ok(code+' rejects wrong canvas coordinates',bool(check_design(bad)))
 bad=deepcopy(a);bad['regions'][0]['normalized_xywh'][2]+=0.2;ok(code+' rejects wrong normalized width',bool(check_design(bad)))
 bad=deepcopy(a);bad['typography'][0]['visible_glyph_height_px']+=10;ok(code+' rejects inconsistent glyph height',bool(check_design(bad)))
 bad=deepcopy(d);bad['design_details']['sha256']='0'*64;ok(code+' rejects changed addendum pin',bool(check(bad,catalog)))
 bad=deepcopy(a);bad['pattern_ids'].append('PAT-TEXT-9999');ok(code+' rejects classification drift',bool(check_design(bad)))
 ok(code+' draft8 retained as historical',bool(check(base,catalog)) and not check(base,catalog,allow_historical=True))
 p.with_suffix('.md').write_text(render(d),encoding='utf-8')
 lines=['# '+code+' 전체 디자인 보강','',a['scope']['limits'],'']
 for k,v in a['dimensions'].items():lines+=['## '+k,'',v['description'],'']
 lines+=['## 수치의 기준','', '가시 경계는 수동 추정, 글자 높이는 선택 ROI 픽셀 측정이다. 원본 폰트 크기·제작 설정이 아니다. 상세 좌표/오차/시점/재사용 이유는 같은 폴더 design-details.json에 있다.','', '## 미확인','']+['- '+v for v in a['unknowns']]
 p.with_name('design-details.md').write_text('\n'.join(lines),encoding='utf-8')
 # Exact crops rather than merely valid files.
 for f in a['frames']:
  im=Image.open(f['path']).convert('RGB')
  ok(f['id']+' native crop pixels',all(ImageChops.difference(im.crop(c['box_ltrb']),Image.open(c['path']).convert('RGB')).getbbox() is None for c in f['crops']))
 for t in a['typography']:
  f=next(x for x in a['frames'] if x['id']==t['frame'])
  ok(t['id']+' glyph crop pixels',ImageChops.difference(Image.open(f['path']).convert('RGB').crop(t['roi_ltrb']),Image.open(t['crop_path']).convert('RGB')).getbbox() is None)
for f in inputs['draft8_source_files']:ok('frozen draft8 '+f['relative'],sha(f['source'])==f['sha256'])
prior=load(ROOT/'case-benchmarks-20261019/publication-receipt.json')
ok('prior415 source and published files preserved',all(sha(x['source'])==x['sha256'] and sha(x['destination'])==x['sha256'] for x in prior['published_files']))
lib=ROOT/'case-benchmarks-20261019/knowledge/pattern-library.json'
ok('library remains18 entries',len(load(lib)['patterns'])==18)
out={'passed':all(x['passed'] for x in checks),'count':len(checks),'checks':checks,'validation_scope':'schema/provenance/geometry consistency/preservation + seeded corruption rejection; NOT video content or independent quality evaluation',
 'current_record_seconds':28,'outside_record_windows_seconds':602.272,'patterns':18,'classification_changed':False,
 'new_unknown':'PG panel resize timing/easing; previous N arrow envelope/source sync still open',
 'skill_version':'0.1.0-draft.9','upstream_whole_skill_adoptions':0}
(OUT/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},ensure_ascii=False))
