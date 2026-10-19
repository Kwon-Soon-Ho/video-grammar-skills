"""Check supplementary design evidence and numeric consistency, not visual truth."""
import argparse,hashlib,json,math
from pathlib import Path
from fractions import Fraction

def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def need(v,msg):
    if not v:raise ValueError(msg)
def box(b,w,h):
    need(isinstance(b,list) and len(b)==4 and all(isinstance(n,(int,float)) and not isinstance(n,bool) and math.isfinite(n) for n in b),'invalid bbox')
    need(0<=b[0]<b[2]<=w and 0<=b[1]<b[3]<=h,'bbox outside native canvas')
def _check(d,record=None):
    need(d['schema_version']=='design-details-0.1','design schema')
    base=load(d['base_record']['path']);need(sha(d['base_record']['path'])==d['base_record']['sha256'],'base record changed')
    need(d['case_id']==base['case_id'] and d['source']==base['source'],'case/source differs from preserved base')
    patterns={x['pattern_id'] for x in base['pattern_refs']}
    need(set(d['pattern_ids'])==patterns,'pattern classification differs from preserved base')
    need(d['scope']['record_window_seconds']==base['window_seconds'],'analysis window changed')
    need(d['scope']['new_continuous_video_coverage'] is False,'design snapshots cannot claim new continuous coverage')
    need(bool(d['scope']['limits']) and bool(d['scope']['content_status']),'scope limits/status missing')
    frames={x['id']:x for x in d['frames']};need(len(frames)==len(d['frames']) and bool(frames),'frame IDs')
    for f in frames.values():
        need(sha(f['path'])==f['sha256'],'frame changed')
        need(any(Path(e['path']).resolve()==Path(f['path']).resolve() and Fraction(str(e['actual_seconds']))==Fraction(str(f['seconds'])) for e in base['evidence']),'frame/time not in preserved case evidence')
        # PNG IHDR reads native dimensions without an imaging dependency.
        data=Path(f['path']).read_bytes()[:24];need(data[:8]==b'\x89PNG\r\n\x1a\n','frame must be pinned PNG')
        need([int.from_bytes(data[16:20],'big'),int.from_bytes(data[20:24],'big')]==f['canvas'],'native canvas mismatch')
        lo,hi=d['scope']['record_window_seconds'];need(lo<=f['seconds']<=hi,'snapshot outside recorded window')
        for c in f['crops']:
            box(c['box_ltrb'],*f['canvas']);need(sha(c['path'])==c['sha256'],'crop changed')
    need(sorted(d['scope']['snapshot_seconds'])==sorted(f['seconds'] for f in frames.values()),'snapshot index differs')
    ids=set()
    for r in d['regions']:
        need(r['id'] not in ids,'duplicate region');ids.add(r['id']);w,h=frames[r['frame']]['canvas'];box(r['bbox_ltrb'],w,h)
        l,t,rr,b=r['bbox_ltrb'];expected=[l/w,t/h,(rr-l)/w,(b-t)/h]
        need(len(r['normalized_xywh'])==4 and all(abs(a-b)<=0.000011 for a,b in zip(expected,r['normalized_xywh'])),'normalized geometry mismatch')
        need(abs(r['bbox_canvas_area_percent']-(rr-l)*(b-t)/(w*h)*100)<0.011,'bbox area mismatch')
        need(r['precision'] in ('estimated','measured') and r['basis_kind'] in ('observed','calculated'),'region precision/basis')
        need(isinstance(r['error_px'],(int,float)) and r['error_px']>=0 and r['method'] and r['reuse_reason'] and r['coordinate_system'],'measurement context missing')
    for t in d['typography']:
        w,h=frames[t['frame']]['canvas'];box(t['roi_ltrb'],w,h);box(t['bbox_ltrb'],w,h)
        l,y,r,b=t['bbox_ltrb'];rl,ry,rr,rb=t['roi_ltrb'];need(rl<=l<r<=rr and ry<=y<b<=rb,'glyph bbox outside ROI')
        need(t['visible_glyph_height_px']==b-y,'glyph height mismatch')
        need(t['text_scope'] and t['method'] and t['error'] and t['precision']=='measured','glyph measurement context')
        need(sha(t['crop_path'])==t['crop_sha256'],'glyph crop changed')
    for r in d['relations']:
        need(set(r['region_ids'])<=ids,'relation unknown region')
        need(r['basis_kind']=='calculated' and r['precision'] in ('estimated','measured') and r['unit'] and r['method'] and r['error'] and r['meaning'],'relation context')
    need(set(d['dimensions'])=={'hierarchy','alignment','spacing','typography','color','background','shapes'},'full design dimensions missing')
    need(all(x['description'] and x['basis_kind'] in ('observed','calculated','inferred') and x['precision'] in ('qualitative','estimated','measured','unknown') for x in d['dimensions'].values()),'dimension description/basis/precision')
    need(d['layers'] and d['unknowns'],'layer/unknown disclosure missing')
    need(all(x['basis_kind']=='inferred' and x['verification_needed'] for x in d['implementation_hypotheses']),'implementation presented as observation')
    if record:
        need(record['case_id']==d['case_id'] and record['source']==d['source'],'current record mismatch')
        need({x['pattern_id'] for x in record['pattern_refs']}==patterns,'current pattern IDs changed')
def check(d,record=None):
    try:_check(d,record);return []
    except (KeyError,TypeError,ValueError,OSError,IndexError,AttributeError) as e:return [str(e)]
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('input');args=a.parse_args()
    try:errors=check(load(args.input))
    except (ValueError,OSError) as e:errors=[str(e)]
    print(json.dumps({'consistency_passed':not errors,'visual_content_verified':False,'errors':errors},ensure_ascii=False));raise SystemExit(bool(errors))
