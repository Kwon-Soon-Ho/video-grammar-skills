from pathlib import Path
import sys,json,zipfile,hashlib,re,struct,zlib,collections
from xml.etree import ElementTree as E
from pypdf import PdfReader
from PIL import Image

W=Path(__file__).parent.resolve();P=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
SRC=P/'한맥 영상';OUT=W/'본문';assert not OUT.exists();OUT.mkdir()
wheel=next((W/'의존성_원본').glob('olefile-0.47-*.whl'));sys.path.insert(0,str(wheel));import olefile
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n' if not isinstance(v,str) else v)
def xml(z,p):return E.fromstring(z.read(p))
def text(el,key):
    return ''.join(n.text or '' for n in el.iter() if n.tag in {key+'t',key+'tab',key+'br'}).strip()
def relation(z,relfile):
    return {n.attrib['Id']:n.attrib['Target'] for n in xml(z,relfile)}
def oox(p):
    chunks=[];detail={}
    with zipfile.ZipFile(p) as z:
        names=z.namelist()
        if p.suffix.lower()=='.docx':
            parts=['word/document.xml']+sorted(n for n in names if re.fullmatch(r'word/(header\d+|footer\d+|footnotes|endnotes|comments)\.xml',n))
            for part in parts:
                root=xml(z,part)
                for i,para in enumerate(root.iter('{'+NS['w']+'}p'),1):
                    t=text(para,'{'+NS['w']+'}')
                    if t:chunks.append({'loc':part+f'/p[{i}]','text':t,'kind':'body' if part.endswith('/document.xml') else 'note_or_header'})
            detail={'parts_read':parts,'embedded_images':len([n for n in names if n.startswith('word/media/')]),'scope':'OOXML paragraph text incl tables; no DOCX page layout rendering; inserted text included, deleted w:delText not current text'}
        elif p.suffix.lower()=='.pptx':
            rels=relation(z,'ppt/_rels/presentation.xml.rels');pres=xml(z,'ppt/presentation.xml');slides=[]
            for sid in pres.findall('p:sldIdLst/p:sldId',NS):
                target=rels[sid.attrib['{'+NS['r']+'}id']]
                slides.append('ppt/'+target if not target.startswith('/') else target.lstrip('/'))
            meta=[]
            for si,part in enumerate(slides,1):
                root=xml(z,part);pic=len(list(root.iter('{'+NS['p']+'}pic')));paras=0
                for pi,pa in enumerate(root.iter('{'+NS['a']+'}p'),1):
                    t=text(pa,'{'+NS['a']+'}')
                    if t:chunks.append({'loc':f'slide[{si}]/p[{pi}]','text':t,'kind':'slide_text'});paras+=1
                relpart=str(Path(part).parent/'_rels'/(Path(part).name+'.rels')).replace('\\','/')
                if relpart in names:
                    for rr in xml(z,relpart):
                        if rr.attrib.get('Type','').endswith('/notesSlide'):
                            import posixpath
                            np=posixpath.normpath(posixpath.join(str(Path(part).parent).replace('\\','/'),rr.attrib['Target']))
                            for ni,pa in enumerate(xml(z,np).iter('{'+NS['a']+'}p'),1):
                                t=text(pa,'{'+NS['a']+'}')
                                if t and not t.isdecimal():chunks.append({'loc':f'slide[{si}]/notes/p[{ni}]','text':t,'kind':'speaker_note'})
                meta.append({'slide':si,'picture_shapes':pic,'text_paragraphs':paras})
            detail={'slides':len(slides),'slide_text_coverage':meta,'scope':'native slide text and notes; image-only contents not OCR; no embedded video opened'}
        elif p.suffix.lower()=='.xlsx':
            ss=[]
            if 'xl/sharedStrings.xml' in names:
                ss=[''.join(n.text or '' for n in si.iter('{'+NS['s']+'}t')) for si in xml(z,'xl/sharedStrings.xml')]
            rels=relation(z,'xl/_rels/workbook.xml.rels');book=xml(z,'xl/workbook.xml');sheets=[]
            for sheet in book.findall('s:sheets/s:sheet',NS):
                import posixpath
                target=rels[sheet.attrib['{'+NS['r']+'}id']]
                part=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
                count=0
                for cell in xml(z,part).iter('{'+NS['s']+'}c'):
                    value=cell.find('s:v',NS);formula=cell.find('s:f',NS);typ=cell.attrib.get('t')
                    if typ=='s' and value is not None:t=ss[int(value.text)]
                    elif typ=='inlineStr':t=''.join(n.text or '' for n in cell.iter('{'+NS['s']+'}t'))
                    else:t=value.text if value is not None else ''
                    if t or formula is not None:
                        chunks.append({'loc':sheet.attrib['name']+'!'+cell.attrib['r'],'text':t or '', 'formula':formula.text if formula is not None else None,'kind':'worksheet_cell'});count+=1
                sheets.append({'name':sheet.attrib['name'],'nonempty_cells':count})
            detail={'sheets':sheets,'scope':'cell values and stored formula strings only; no recalculation or image OCR'}
    return chunks,detail
def hwp(p):
    chunks=[];meta={'scope':'HWP5 paragraph text records only; layout, drawing objects and complex table interpretation not rendered'}
    with olefile.OleFileIO(str(p),write_mode=False) as o:
        header=o.openstream('FileHeader').read();assert header.startswith(b'HWP Document File')
        flags=struct.unpack_from('<I',header,36)[0];meta['flags']=flags
        if flags&6:raise ValueError('encrypted_or_distribution_document_not_processed')
        secs=sorted([x for x in o.listdir() if len(x)==2 and x[0]=='BodyText' and x[1].startswith('Section')],key=lambda x:int(x[1][7:]))
        assert secs
        meta['sections']=[]
        for sec in secs:
            raw=o.openstream(sec).read();raw=zlib.decompress(raw,-15) if flags&1 else raw
            off=0;records=0;paras=0
            while off<len(raw):
                assert off+4<=len(raw)
                h=struct.unpack_from('<I',raw,off)[0];off+=4;tag=h&1023;size=h>>20;level=(h>>10)&1023
                if size==4095:size=struct.unpack_from('<I',raw,off)[0];off+=4
                assert off+size<=len(raw);payload=raw[off:off+size];off+=size;records+=1
                if tag==67:
                    assert len(payload)%2==0
                    units=list(struct.unpack('<'+'H'*(len(payload)//2),payload));keep=[];j=0
                    while j<len(units):
                        u=units[j]
                        if u in set(range(1,10))|{11,12}|set(range(14,24)):
                            keep.append(9 if u==9 else 32);j+=8
                        else:
                            if u in {10,13}:keep.append(10)
                            elif u in {30,31}:keep.append(32)
                            elif u==24:keep.append(45)
                            elif u>=32:keep.append(u)
                            j+=1
                    t=struct.pack('<'+'H'*len(keep),*keep).decode('utf-16le',errors='replace').strip() if keep else ''
                    if t:paras+=1;chunks.append({'loc':'/'.join(sec)+f'/record[{records}]/para[{paras}]','text':t,'kind':'body_paragraph','level':level})
            meta['sections'].append({'name':'/'.join(sec),'records':records,'text_paragraphs':paras,'consumed_bytes':off})
        meta['all_body_sections_processed']=True
    return chunks,meta

exts={'.docx','.pptx','.xlsx','.pdf','.hwp'}
paths=sorted([p for p in SRC.rglob('*') if p.is_file() and p.suffix.lower() in exts],key=lambda p:p.relative_to(SRC).as_posix().casefold())
records=[]
for i,p in enumerate(paths,1):
    did=f'DOC{i:03d}';before=sha(p);status='text_extracted';detail={}
    try:
        if p.suffix.lower() in {'.docx','.pptx','.xlsx'}:chunks,detail=oox(p)
        elif p.suffix.lower()=='.hwp':chunks,detail=hwp(p)
        else:
            reader=PdfReader(p);chunks=[{'loc':f'page[{n}]','text':pg.extract_text() or '', 'kind':'pdf_page'} for n,pg in enumerate(reader.pages,1)]
            detail={'pages':len(reader.pages),'pages_needing_visual_read':[n for n,c in enumerate(chunks,1) if len(c['text'].strip())<30],'scope':'PDF text layer; scans require visual review'}
        if not any(c['text'].strip() for c in chunks):status='no_text_needs_visual_review'
    except Exception as ex:chunks=[];status='read_failed';detail={'error':type(ex).__name__+': '+str(ex)}
    assert sha(p)==before
    rec={'id':did,'path':p.relative_to(P).as_posix(),'sha256':before,'backup':any(v.casefold() in {'backup','백업'} for v in p.parts),'status':status,'chunk_count':len(chunks),'chars':sum(len(c['text']) for c in chunks),'detail':detail}
    write(OUT/(did+'.json'),dict(rec,chunks=chunks))
    write(OUT/(did+'.txt'),rec['path']+'\n'+'\n\n'.join('['+c['loc']+'] '+c['text'] for c in chunks))
    records.append(rec)
images=[]
for p in SRC.rglob('*.png'):
    with Image.open(p) as im:images.append({'path':p.relative_to(P).as_posix(),'size':im.size,'mode':im.mode,'sha256':sha(p)})
write(W/'문서목록과_읽기결과.json',{'documents':records,'images':images,'olefile_wheel_sha256':sha(wheel),'scope':'planning documents only; no MP4 content read, no video analysis or skill development','format_sources':['https://tech.hancom.com/python-hwp-parsing-2/','https://tech.hancom.com/python-hwp-parsing-1/','https://olefile.readthedocs.io/en/stable/License.html']})
with zipfile.ZipFile(wheel) as z:
    for n in z.namelist():
        if 'LICENSE' in n.upper():
            q=W/'의존성_원본'/'olefile_LICENSE.txt'
            if not q.exists():q.write_bytes(z.read(n))
print(json.dumps({'documents':len(records),'statuses':dict(collections.Counter(r['status'] for r in records)),'characters':sum(r['chars'] for r in records),'images':images},ensure_ascii=False))
