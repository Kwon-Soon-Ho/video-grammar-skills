from pathlib import Path
from PIL import Image, ImageDraw
root=Path('C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기')
base=root/'phase01a-a2-retest/analysis_input/cases/자료013'
out=root/'phase01a-a3/runs/without_a'
specs={
'T01_detail':('T01',[3.6,3.9,4.2,4.5,4.8,5.1],(0,0,2250,2160),(625,600)),
'T02_detail':('T02',[0,0.15,0.25,0.4,0.7,1.4],(0,0,3840,2160),(960,540)),
'T03_detail':('T03',[1.8,1.9,2.0,2.1,2.3,2.6,3.1,3.2,3.3,3.4,3.5,3.6],(450,400,3650,1450),(960,315))
}
for name,(case,times,box,size) in specs.items():
    dst=Image.new('RGB',(size[0]*2,(size[1]+25)*((len(times)+1)//2)),(28,28,28)); d=ImageDraw.Draw(dst)
    for i,t in enumerate(times):
        f=base/case/f'f_{round(t*60):05d}_{t:07.3f}.png'
        im=Image.open(f).crop(box).resize(size,Image.Resampling.LANCZOS)
        x=(i%2)*size[0]; y=(i//2)*(size[1]+25)
        dst.paste(im,(x,y)); d.text((x+5,y+size[1]+5),f'{case} actual {t:.3f}s',fill='white')
    dst.save(out/f'{name}.png')
    print(out/f'{name}.png')
