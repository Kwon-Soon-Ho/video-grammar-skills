"""Fetch public, pinned source/wheel for static review. No media/API access."""
import pathlib,urllib.request,json,hashlib
W=pathlib.Path(__file__).resolve().parent;O=W/'검토원본';O.mkdir(exist_ok=True)
url='https://pypi.org/pypi/av/19.0.1/json'
data=urllib.request.urlopen(url,timeout=30).read();meta=json.loads(data)
(O/'PyPI_av_19.0.1_출처.json').write_bytes(data)
chosen=[x for x in meta['urls'] if x['filename'] in ['av-19.0.1-cp312-abi3-win_amd64.whl','av-19.0.1.tar.gz']]
assert len(chosen)==2
result=[]
for x in chosen:
    assert x['url'].startswith('https://files.pythonhosted.org/') and pathlib.Path(x['filename']).name==x['filename']
    path=O/x['filename']
    if not path.exists():
        with urllib.request.urlopen(x['url'],timeout=60) as r,path.open('wb') as f:
            for block in iter(lambda:r.read(1048576),b''):f.write(block)
    h=hashlib.sha256(path.read_bytes()).hexdigest();assert h==x['digests']['sha256']
    result.append({'filename':x['filename'],'url':x['url'],'sha256':h,'bytes':path.stat().st_size,'executed':False})
(W/'도구자료_확보목록.json').write_text(json.dumps({'pypi_metadata':url,'files':result,'installed_globally':False,'source_executed':False},ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(result,ensure_ascii=False))
