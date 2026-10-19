from pathlib import Path
from PIL import Image,ImageDraw
import json
from fractions import Fraction
root=Path.cwd(); out=root/'phase01a-a3/runs/with_b'
def panels(aid,tag,roi,times,name,cols=2):
 p=out/'cases'/aid/tag; log=json.loads((p/'실행기록.json').read_text(encoding='utf-8')); frames=log['frames']; selected=[min(frames,key=lambda f:abs(float(Fraction(f['actual_playback_seconds']))-t)) for t in times]
 w,h=roi[2]-roi[0],roi[3]-roi[1]; board=Image.new('RGB',(w*cols,(h+30)*((len(selected)+cols-1)//cols)), '#20252c'); d=ImageDraw.Draw(board); meta=[]
 for i,f in enumerate(selected):
  im=Image.open(f['path']).crop(roi); cp=out/(name+'_'+str(i)+'.png');im.save(cp); x=(i%cols)*w;y=(i//cols)*(h+30);board.paste(im,(x,y+30));d.text((x+3,y+4),f['actual_playback_seconds'],fill='white');meta.append({'path':str(cp),'source':f['path'],'actual_seconds':f['actual_playback_seconds'],'crop_native':roi})
 board.save(out/(name+'.png'));(out/(name+'.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
panels('자료005','graphnative',(1040,345,1835,735),[8,8.1667,8.3333,8.6667,9,9.3333],'T04_order')
panels('자료005','graphnative',(2000,345,2800,735),[15.3333,15.6667,16,16.3333,16.6667,18],'T04_sales')
panels('자료005','graphnative',(2940,345,3760,735),[16.6667,17,17.3333,17.6667,18],'T04_profit')
panels('자료005','blendnative',(0,110,980,700),[6,6.1,6.2,6.3],'T05_titles')
