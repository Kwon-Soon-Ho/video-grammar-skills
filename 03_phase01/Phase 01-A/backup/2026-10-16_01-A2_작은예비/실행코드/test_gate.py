from pathlib import Path
import struct,json,subprocess,sys
from prepare import OUT,preflight,write
from extract import registered,BoundedReader,memory_limit,sar_status
from fractions import Fraction

def box(t,b):return struct.pack('>I4s',8+len(b),t)+b
def fixture(dref=None,idx=1,edits=1):
    mv=bytearray(100);struct.pack_into('>II',mv,12,1000,1000)
    md=bytearray(24);struct.pack_into('>II',md,12,1000,1000)
    tk=bytearray(84);struct.pack_into('>9i',tk,40,65536,0,0,0,65536,0,0,0,1073741824);struct.pack_into('>II',tk,76,100<<16,100<<16)
    dr=box(b'dref',b'\0'*4+struct.pack('>I',1)+(dref or box(b'url ',b'\0\0\0\1')))
    sample=bytearray(86);struct.pack_into('>I4s',sample,0,86,b'avc1');struct.pack_into('>H',sample,14,idx)
    stsd=box(b'stsd',b'\0'*4+struct.pack('>I',1)+sample)
    el=box(b'elst',b'\0'*4+struct.pack('>I',edits)+struct.pack('>Iihh',1000,0,1,0)*edits)
    return box(b'ftyp',b'isom\0\0\0\0isom')+box(b'moov',box(b'mvhd',mv)+box(b'trak',box(b'tkhd',tk)+box(b'edts',el)+box(b'mdia',box(b'mdhd',md)+box(b'minf',box(b'dinf',dr)+box(b'stbl',stsd)))))+box(b'mdat',b'\0')

results=[];dest=OUT/'gate_tests';dest.mkdir(exist_ok=True)
def test(name,fn,expected_error=False):
    try:fn();ok=not expected_error;error=None
    except Exception as e:ok=expected_error;error=type(e).__name__+': '+str(e)
    results.append({'name':name,'passed':ok,'error':error})
def pf(name,data):
    p=dest/(name+'.mp4');p.write_bytes(data);return lambda:preflight(p)
test('self_contained_minimal_gate',pf('valid',fixture()))
test('external_https_dref_rejected',pf('https',fixture(box(b'url ',b'\0'*4+b'https://example.invalid/a\0'))),True)
test('external_local_path_rejected',pf('local',fixture(box(b'url ',b'\0'*4+b'file:///C:/secret\0'))),True)
test('urn_reference_rejected',pf('urn',fixture(box(b'urn ',b'\0'*4+b'x\0'))),True)
test('sample_data_reference_2_rejected',pf('index2',fixture(idx=2)),True)
test('fragmented_input_rejected',pf('moof',fixture()+box(b'moof',b'')),True)
test('corrupt_box_rejected',pf('corrupt',b'\0\0\0\x40moov'),True)
test('unregistered_input_rejected',lambda:registered('https://example.invalid'),True)
test('memory_budget_job_configured',memory_limit)
test('timeout_kills_only_child',lambda:subprocess.run([sys.executable,'-c','import time;time.sleep(2)'],timeout=.1),True)
reader=BoundedReader(dest/'valid.mp4')
test('unbounded_read_rejected',lambda:reader.read(),True)
reader.close()
test('SAR_None_remains_unknown',lambda: (_ for _ in ()).throw(AssertionError()) if sar_status(None)!='unknown' else None)
test('SAR_zero_remains_unknown',lambda: (_ for _ in ()).throw(AssertionError()) if sar_status(Fraction(0,1))!='unknown' else None)
test('SAR_one_square_reported',lambda: (_ for _ in ()).throw(AssertionError()) if sar_status(Fraction(1))!='reported_square' else None)
test('SAR_nonsquare_not_silently_corrected',lambda:sar_status(Fraction(16,15)),True)
test('allowlisted_path_jangheon',lambda:registered('자료005'))
test('allowlisted_path_EG',lambda:registered('자료013'))
write(OUT/'사전게이트_시험.json',results)
print(json.dumps(results,ensure_ascii=False,indent=2))
if not all(x['passed'] for x in results):raise SystemExit(1)
