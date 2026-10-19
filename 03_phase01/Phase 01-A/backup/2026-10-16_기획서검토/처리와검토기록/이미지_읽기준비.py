"""Read-only, bounded PNG band decoder and static PPT illustration previews."""
import pathlib, json, struct, zlib, io, zipfile, hashlib
from PIL import Image, ImageDraw
from xml.etree import ElementTree as ET
W=pathlib.Path(__file__).resolve().parent
P=pathlib.Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
O=W/'이미지확인'; O.mkdir(exist_ok=True)
manifest=json.loads((W/'문서목록과_읽기결과.json').read_text('utf-8'))
def chunk(t,b):return struct.pack('>I',len(b))+t+b+struct.pack('>I',zlib.crc32(t+b)&0xffffffff)
def giant(path,out):
    with path.open('rb') as f:
        assert f.read(8)==b'\x89PNG\r\n\x1a\n'
        n=struct.unpack('>I',f.read(4))[0];assert f.read(4)==b'IHDR'
        ihdr=f.read(n); f.read(4)
        width,height,depth,color,cm,fm,interlace=struct.unpack('>IIBBBBB',ihdr)
        assert (depth,color,interlace)==(8,6,0)
        tw=1800; scale=tw/width; th=round(height*scale)
        overview=Image.new('RGB',(tw,th),'white')
        rowbytes=width*4; stride=rowbytes+1; prev=bytes(rowbytes); pending=bytearray(); y=0
        dec=zlib.decompressobj()
        def consume(final=False):
            nonlocal prev,y,pending
            while len(pending)>=stride*128 or (final and len(pending)>=stride):
                rows=min(128,len(pending)//stride)
                data=b'\0'+prev+bytes(pending[:rows*stride]);del pending[:rows*stride]
                ih=struct.pack('>IIBBBBB',width,rows+1,8,6,0,0,0)
                encoded=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',ih)+chunk(b'IDAT',zlib.compress(data,1))+chunk(b'IEND',b'')
                band=Image.open(io.BytesIO(encoded));band.load()
                prev=band.crop((0,rows,width,rows+1)).tobytes()
                y0,y1=round(y*scale),round((y+rows)*scale)
                if y1>y0:overview.paste(band.crop((0,1,width,rows+1)).convert('RGB').resize((tw,y1-y0),Image.Resampling.LANCZOS),(0,y0))
                y+=rows
        while True:
            h=f.read(8)
            if not h:break
            n,t=struct.unpack('>I4s',h)
            if t==b'IDAT':
                left=n
                while left:
                    b=f.read(min(2048,left));left-=len(b)
                    pending.extend(dec.decompress(b));consume()
            else:f.seek(n,1)
            f.read(4)
            if t==b'IEND':break
        pending.extend(dec.flush());consume(True);assert y==height and not pending
        overview.save(out)
        return {'source':str(path),'preview':str(out),'width':width,'height':height,'preview_width':tw,'scope':'overview only; text too small remains unverified'}
results=[]
for i,path in enumerate(sorted((P/'한맥 영상').rglob('*.png')),1):
    out=O/f'기획보드{i:02}_전체.png'
    if not out.exists():print('giant',i,flush=True); results.append(giant(path,out))
for d in manifest['documents']:
    if d['status']!='no_text' or not d['path'].endswith('.pptx'):continue
    path=P/d['path']; previews=[]
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if not name.startswith('ppt/media/') or not name.lower().endswith(('.png','.jpg','.jpeg')):continue
            try:
                im=Image.open(io.BytesIO(z.read(name)));im.thumbnail((1200,800))
                if im.width<300 or im.height<100:continue
                out=O/f"{d['id']}_{pathlib.Path(name).stem}.jpg";im.convert('RGB').save(out,quality=90)
                previews.append(str(out))
            except Exception as e:print(d['id'],name,type(e).__name__,flush=True)
    results.append({'id':d['id'],'source':str(path),'static_previews':previews})
(O/'이미지읽기_처리기록.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(results,ensure_ascii=False),flush=True)
