exec((__import__('pathlib').Path(__file__).parent/'make_crops.py').read_text(encoding='utf-8'))
log=json.loads((B/'cases/A5-A/H02-r2-with_skill-extra2/실행기록.json').read_text(encoding='utf-8'))
for f in log['frames']:
 t=float(Fraction(f['actual_playback_seconds']))
 if t not in [13.25,13.35,13.45,13.8,14.2,16.6,16.7,16.9,17.5,17.55,17.65]:continue
 path=D/f'crop-main-{t:.3f}.png'; box=[750,920,1730,1700]
 with Image.open(f['path']) as im:im.crop(box).save(path)
 rows.append(dict(path=str(path),parent_path=f['path'],crop_xyxy_native_pixels=box))
log=json.loads((B/'cases/A5-A/H02/실행기록.json').read_text(encoding='utf-8'))
for f in log['frames']:
 t=float(Fraction(f['actual_playback_seconds']))
 if t not in [13.6,14.4,16.8,17.6]:continue
 path=D/f'crop-secondary-{t:.3f}.png'; box=[2420,1480,3000,1810]
 with Image.open(f['path']) as im:im.crop(box).save(path)
 rows.append(dict(path=str(path),parent_path=f['path'],crop_xyxy_native_pixels=box))
(D/'crops.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(rows))
