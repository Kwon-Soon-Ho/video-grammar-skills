"""공개 wheel의 해시/경로를 확인해 작업 폴더에만 풀고 빌드 정보를 기록한다.
회사 파일을 열거나 전역 패키지를 설치하지 않는다. A1 기술 진단 전용.
"""
from pathlib import Path, PurePosixPath
import hashlib, json, stat, sys, zipfile

ROOT = Path(__file__).resolve().parent
WHEEL = ROOT / '검토원본' / 'av-19.0.1-cp312-abi3-win_amd64.whl'
TARGET = ROOT / '후보런타임'
EXPECTED = '906fc3db09288319a75ea23ffefb59961c7dbe0d1c074601507a89de7d8593d8'
assert hashlib.sha256(WHEEL.read_bytes()).hexdigest() == EXPECTED
TARGET.mkdir(exist_ok=True)
entries = []
with zipfile.ZipFile(WHEEL) as z:
    assert sum(i.file_size for i in z.infolist()) < 250_000_000
    for i in z.infolist():
        p = PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and ':' not in i.filename
        assert not stat.S_ISLNK(i.external_attr >> 16)
        out = TARGET.joinpath(*p.parts).resolve()
        assert out.is_relative_to(TARGET.resolve())
        if i.is_dir():
            out.mkdir(parents=True, exist_ok=True)
            continue
        data = z.read(i)
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            assert out.read_bytes() == data, f'후보 런타임 변경: {i.filename}'
        else:
            out.write_bytes(data)
        entries.append({'file': i.filename, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
sys.path.insert(0, str(TARGET))
import av
import av._core
def clean(x):
    if isinstance(x, bytes): return x.decode('utf-8', errors='replace')
    if isinstance(x, dict): return {k: clean(v) for k,v in x.items()}
    if isinstance(x, (tuple,list)): return [clean(v) for v in x]
    return x
result = {
    'purpose': 'A1 합성 자료 기술 진단용 격리 후보. 기본 도입/재배포 승인 아님',
    'python': sys.version, 'av_version': av.__version__, 'module': av.__file__,
    'ffmpeg_version_info': clean(av._core.ffmpeg_version_info),
    'library_meta': clean(av._core.library_meta),
    'global_install': False, 'company_files_opened': 0,
    'network_requests_in_this_script': 0,
    'archive_sha256': EXPECTED, 'extracted_files': entries,
}
(ROOT / '격리런타임_검토결과.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: result[k] for k in ['av_version','ffmpeg_version_info','global_install','company_files_opened']}, ensure_ascii=False))
print(json.dumps({k: {'version':v['version'],'license':v['license'],'configuration':v['configuration']} for k,v in result['library_meta'].items()}, ensure_ascii=False))
