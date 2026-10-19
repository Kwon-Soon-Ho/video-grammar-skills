from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
OUT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    inputs=json.loads((OUT/'inputs.json').read_text(encoding='utf-8'))
    frames={x['id']:x for x in inputs['evidence']}
    # ROIs exclude frames, logos and adjacent objects. White-pixel envelope is NOT font size.
    rois={
      'N-header':('N177',[350,105,1020,210]),
      'N-label-left':('N177',[1400,265,2750,360]),
      'N-label-right':('N177',[5370,265,6600,360]),
      'N-caption':('N177',[2435,1945,5245,2070]),
      'P-police-row1':('P47',[350,320,1050,370]),
      'P-police-row2':('P47',[350,460,1050,515]),
      'P-regional-row1':('P47',[1650,240,2200,305]),
      'P-regional-row2':('P47',[1650,420,2200,495]),
      'P53-regional-row1':('P53',[2835,290,3500,355]),
      'P53-regional-row2':('P53',[2835,450,3500,520])}
    results=[]
    for ident,(frame,box) in rois.items():
        im=Image.open(frames[frame]['path']).convert('RGB'); a=np.array(im.crop(box)).astype(int)
        mask=(a.min(2)>170)&((a.max(2)-a.min(2))<45)
        ys,xs=np.where(mask)
        if len(xs)==0:raise ValueError(ident)
        bb=[box[0]+int(xs.min()),box[1]+int(ys.min()),box[0]+int(xs.max())+1,box[1]+int(ys.max())+1]
        dest=OUT/'inspection'/f'{ident}-glyphs.png';im.crop(box).save(dest)
        results.append({'id':ident,'frame':frame,'roi_ltrb':box,'bbox_ltrb':bb,'visible_glyph_height_px':bb[3]-bb[1],'selected_glyph_span_px':bb[2]-bb[0],
         'text_scope':'complete visible line' if ident.startswith('N') else 'central glyph sample, not full line width',
         'method':'native RGB: min(R,G,B)>170 and max-min<45; union of selected pixels inside manually isolated text ROI',
         'error':'threshold/antialias envelope approx ±2 px; excludes dark shadow. Not original font size, font family or weight setting.',
         'precision':'measured','crop_path':str(dest),'crop_sha256':sha(dest)})
    (OUT/'glyph-measurements.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ['id','bbox_ltrb','visible_glyph_height_px']} for r in results],ensure_ascii=False))
if __name__=='__main__':main()
