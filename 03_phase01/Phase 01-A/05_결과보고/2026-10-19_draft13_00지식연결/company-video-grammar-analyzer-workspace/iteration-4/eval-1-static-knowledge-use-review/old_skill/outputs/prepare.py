from pathlib import Path
import json, hashlib, shutil
from PIL import Image

OUT = Path(__file__).resolve().parent
ROOT = next(p for p in OUT.parents if (p / 'knowledge-linked-skill-20261019').is_dir())
INPUT = ROOT / 'knowledge-linked-skill-20261019/eval-inputs'
PHASE = Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name, data):
    (OUT / name).parent.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

manifest=[]
for p in [INPUT/'input.md', *sorted((INPUT/'static').glob('*.md'))]:
    dest=OUT/'preserved'/p.name
    dest.parent.mkdir(exist_ok=True)
    shutil.copyfile(p,dest)
    manifest.append({'path':str(p),'copy':str(dest),'sha256':sha(p),'copy_sha256':sha(dest),'type':'provided_prior_record' if p.name!='input.md' else 'task_input'})
evidence=[]
for n,t in [('134',134),('172',172)]:
    p=INPUT/f'static/evidence/{n}.png'
    im=Image.open(p)
    evidence.append({'id':'E1' if n=='134' else 'E2','path':str(p),'sha256':sha(p),'size':list(im.size),'time_seconds':t,'time_basis':'provided input; MP4/PTS not independently inspected','type':'provided_png'})
rois=[('e1_logos','E1',(1000,1000,2750,1910)),('e1_roles','E1',(4750,660,6700,1380)),('e1_arrows','E1',(2900,930,4700,1740)),('e1_work','E1',(4550,1320,7110,2000)),('e2_logos','E2',(2500,910,4800,1510)),('e2_value','E2',(350,540,2470,840)),('e2_building','E2',(4790,640,7440,1790)),('e2_number','E2',(0,850,2450,1640))]
for name,eid,box in rois:
    parent=next(e for e in evidence if e['id']==eid)
    dest=OUT/f'evidence/{name}.png'; dest.parent.mkdir(exist_ok=True)
    Image.open(parent['path']).crop(box).save(dest)
    evidence.append({'id':name,'path':str(dest),'sha256':sha(dest),'parent':eid,'bbox_ltrb_exclusive':box,'coordinate_system':'parent PNG, top-left, x right/y down, px','transform':'crop only; no resize/color/rotation','size':list(Image.open(dest).size)})

selected={
'01_공통용어/공통용어사전.json':('terms',['REL-SPACE','REL-CORRELATION','REL-PARALLEL','LAYOUT-SPLIT','LAYOUT-NETWORK','LAYOUT-SPACE-CALLOUT','LAYOUT-CARD-GROUP','STYLE-3D','STYLE-DIAGRAM','STYLE-PIP']),
'02_원칙과레이아웃/레이아웃지식.json':('layouts',['KNOW-LAYOUT-SPLIT','KNOW-LAYOUT-SPLIT-COMPARE','KNOW-LAYOUT-NETWORK','KNOW-LAYOUT-SPACE-CALLOUT','KNOW-LAYOUT-CARD-GROUP','KNOW-LAYOUT-UI-ANNOTATION','KNOW-LAYOUT-DATA-CHART']),
'02_원칙과레이아웃/모션과정보전달원칙.json':('principles',['AP-03','IP-02','IP-04','MR-03','MR-07','MR-08','AP-06','MP-02']),
'02_원칙과레이아웃/화면설계원칙.json':('principles',['SCREEN-HIERARCHY','SCREEN-GROUP','SCREEN-DATA','SCREEN-COLOR','SCREEN-TIME-READ']),
'13_품질검수/품질항목_정본.json':('cards',['Q-INFO-02','Q-INFO-03','Q-INFO-04','Q-TEXT-01','Q-SCREEN-01','Q-SCREEN-06','Q-SCREEN-07','Q-MOTION-01','Q-BRAND-01','Q-TRUST-01','Q-TRUST-02'])}
knowledge=[]
for rel,(key,ids) in selected.items():
    p=PHASE/rel; data=json.loads(p.read_text(encoding='utf-8-sig'))
    values=data.get(key)
    if not isinstance(values,list):
        candidates=[(k,v) for k,v in data.items() if isinstance(v,list) and any(isinstance(x,dict) and x.get('id') in ids for x in v)]
        if len(candidates)!=1: raise ValueError((rel,list(data)))
        key,values=candidates[0]
    for i,v in enumerate(values):
        if v.get('id') in ids:
            knowledge.append({'id':v['id'],'source_path':str(p),'source_sha256':sha(p),'source_version':data.get('version'),'json_pointer':f'/{key}/{i}','source_kind':'conditional_knowledge_not_observation','content':v})
    missing=set(ids)-{x['id'] for x in values}
    if missing: raise ValueError((rel,missing))
    manifest.append({'path':str(p),'sha256':sha(p),'type':'phase00_knowledge_read_selected_objects','selected_ids':ids})
save('source_manifest.json',manifest)
save('evidence.json',evidence)
save('knowledge_snapshot.json',knowledge)
print(json.dumps({'preserved_records':len([m for m in manifest if 'copy' in m]),'evidence':len(evidence),'knowledge_objects':len(knowledge),'keys':[k['id'] for k in knowledge]},ensure_ascii=False))
