"""01-A1 전용 고정 합성 자료 진단. 실제 영상 경로/CLI 인자를 받지 않는다.
이 파일은 영상 분석 스킬이나 범용 추출기가 아니다.
"""
from pathlib import Path
from fractions import Fraction
import hashlib, json, sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '후보런타임'))
import av
from av.container.core import Flags
import numpy as np
from PIL import Image

OUT = ROOT / '합성진단'
OUT.mkdir(exist_ok=True)
checks, observations = [], {}
def check(name, result, details):
    checks.append({'id': name, 'pass': bool(result), 'details': details})
def rational(t):
    return Fraction(t.numerator, t.denominator) if t else None
def q(t):
    return None if t is None else {'num': t.numerator, 'den': t.denominator}

def make_case(name, ticks):
    path = OUT / (name + '.mkv')
    with av.open(str(path), 'w', format='matroska') as c:
        s = c.add_stream('ffv1', rate=25)
        s.width, s.height, s.pix_fmt = 96, 64, 'bgr0'
        s.time_base = Fraction(1,1000)
        s.codec_context.time_base = Fraction(1,1000)
        for i, tick in enumerate(ticks):
            a = np.zeros((64,96,3), dtype=np.uint8)
            a[10:30, 10+i*5:30+i*5] = [240,40,20]
            f = av.VideoFrame.from_ndarray(a, format='rgb24')
            f.pts, f.time_base = tick, Fraction(1,1000)
            for packet in s.encode(f): c.mux(packet)
        for packet in s.encode(): c.mux(packet)
    with av.open(str(path), options={'fflags':'-genpts'}) as c:
        no_genpts = not bool(c.flags & Flags.gen_pts.value)
        audio_streams = len(c.streams.audio)
        frames = list(c.decode(video=0))
        records = []
        for i, f in enumerate(frames):
            tb = rational(f.time_base)
            records.append({
                'display_order': i, 'reported_pts': str(f.pts) if f.pts is not None else None,
                'time_base': q(tb), 'reported_time': q(f.pts*tb) if f.pts is not None and tb else None,
                'rotation_value': f.rotation,
                'display_matrix_present_on_frame': any(sd.type.name == 'DISPLAYMATRIX' for sd in f.side_data),
                'width': f.width, 'height': f.height,
            })
        actual = [Fraction(int(r['reported_pts'])) * Fraction(r['time_base']['num'], r['time_base']['den']) for r in records]
        expected = [Fraction(t,1000) for t in ticks]
        # 디코딩값을 역산해 정답으로 삼지 않고 생성 전에 준 정수를 기준으로 비교한다.
        check(name+'_PTS', actual == expected, {'expected': [q(v) for v in expected], 'actual':[q(v) for v in actual]})
        check(name+'_no_audio', audio_streams == 0, {'audio_streams': audio_streams})
        check(name+'_genpts_flag_disabled', no_genpts, {'does_not_prove_native_timestamp_provenance': True})
        pixel = frames[2].to_ndarray(format='rgb24')
        check(name+'_known_rectangle', bool(np.all(pixel[10:30,20:40] == [240,40,20])) and bool(np.all(pixel[0,0] == 0)), '미리 정한 사각형과 배경을 손실 없이 읽는지 확인')
        if name == 'VFR_offset':
            elapsed = [v-Fraction(1) for v in actual]
            check('VFR_origin_not_zero', actual[0] == 1 and elapsed == [Fraction(0),Fraction(3,100),Fraction(9,100),Fraction(7,50)], {'explicit_synthetic_origin':q(Fraction(1)), 'elapsed':[q(v) for v in elapsed]})
            requested = Fraction(3,50)
            selected = min(range(len(elapsed)), key=lambda i:(abs(elapsed[i]-requested),elapsed[i]))
            check('nearest_tie_lower', selected == 1 and elapsed[selected] != requested, {'requested':q(requested),'actual':q(elapsed[selected]),'policy':'nearest, equal-distance earlier'})
            check('VFR_not_fps_times_seconds', elapsed[1] != Fraction(1,25), {'second_frame_elapsed':q(elapsed[1]), 'nominal_rate_reciprocal':q(Fraction(1,25))})
        observations[name] = records
    return path

files = [make_case('CFR', [0,40,80,120]), make_case('VFR_offset', [1000,1030,1090,1140])]

blank = av.VideoFrame(16,16,'rgb24')
check('unset_time_base', not blank.time_base and blank.time_base is not None and rational(blank.time_base) is None, {'repr':str(blank.time_base)})
check('unset_pts', blank.pts is None, {'reported_pts':blank.pts})
check('rotation_absent_zero_is_not_proof', blank.rotation == 0 and not any(sd.type.name == 'DISPLAYMATRIX' for sd in blank.side_data), {'value':blank.rotation,'presence':False,'decision':'unknown metadata, no official unrotated claim'})

# 미리 정한 픽셀 영역 → 크롭 → 시계방향90 → 정수배 확대 → 패딩.
a = np.zeros((64,96,3),dtype=np.uint8)
a[16:32,24:48] = [255,0,0]
im = Image.fromarray(a)
crop = im.crop((16,8,80,56))
rotated = crop.transpose(Image.Transpose.ROTATE_270)
resized = rotated.resize((96,128), Image.Resampling.NEAREST)
final = Image.new('RGB',(120,150)); final.paste(resized,(8,10))
final.save(OUT/'좌표변환_정답도형.png')
mask = np.asarray(final)[:,:,0] == 255
ys,xs = np.where(mask)
bbox = [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
check('crop_rotate_resize_pad_bbox', bbox == [56,26,88,74], {'expected_edge_bbox':[56,26,88,74],'observed':bbox,'dimensions':list(final.size),'convention':'top-left edge; clockwise90'})
corner = Image.new('RGB',(16,16)); corner.putpixel((0,0),(255,255,255))
corner_crop = corner.crop((8,0,16,16))
pad = Image.new('RGB',(16,16)); pad.paste(corner_crop,(8,0))
check('crop_cannot_restore', not np.asarray(pad).any(), {'deleted_pixel':[0,0],'padding_did_not_restore':True})

damaged = OUT/'이것은_영상이_아님.bin'; damaged.write_bytes(b'01-A1 invalid synthetic media\x00')
try:
    with av.open(str(damaged)) as c: list(c.decode(video=0))
except av.FFmpegError as e:
    check('damaged_file_explicit_error', True, {'error_type':type(e).__name__})
else:
    check('damaged_file_explicit_error', False, 'unexpected success')

result = {
    'scope':'고정 합성 자료 기술 진단. 실제 회사 영상/정답/성능 평가가 아님',
    'company_media_opened':0,'api_calls':0,'analyzer_skill_created':False,
    'runtime_version':av.__version__,
    'checks':checks,'passed':sum(r['pass'] for r in checks),'total':len(checks),
    'observations':observations,
    'assets':[{'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [*files, OUT/'좌표변환_정답도형.png',damaged]],
    'limits':[
        '같은 FFmpeg 기반 생성/디코딩으로 독립 코덱 교차검증 아님',
        '실제 MP4 edit list, B-frame, 음성 동기, 비정방 SAR, 비영 회전 메타데이터 미시험',
        'GENPTS 비트 해제는 네이티브 추론/입력 PTS 진위를 전부 증명하지 않음',
        '픽셀 변환은 Pillow 합성 검증. 모델의 좌표 인식 정확성 검증 아님',
    ],
}
(ROOT/'합성진단_결과.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':result['passed'],'total':len(checks),'failed':[r['id'] for r in checks if not r['pass']], 'company_media_opened':0},ensure_ascii=False))
assert all(r['pass'] for r in checks)
