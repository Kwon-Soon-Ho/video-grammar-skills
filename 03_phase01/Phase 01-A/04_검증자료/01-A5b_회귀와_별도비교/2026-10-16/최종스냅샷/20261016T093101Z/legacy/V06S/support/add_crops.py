exec((__import__('pathlib').Path('phase01a-a5b/legacy/V06S/support/make_crops.py').read_text('utf-8-sig')).split('spec=[]')[0])
crops=json.loads((run/'support/crops.json').read_text('utf-8'))
for i,(t,box,name) in enumerate([(232,[1100,0,2750,420],'menu'),(232,[50,1650,3750,2110],'scene_text'),(245,[1900,650,3840,1720],'right'),(245.96666666666667,[1900,650,3840,1720],'right')],37):
 f=by[t];p=run/'support'/f'c{i:02}_{name}_{t:.3f}.png';Image.open(f['path']).crop(box).convert('RGB').save(p);crops.append({'path':str(p),'parent_path':f['path'],'crop_xyxy_native_pixels':box,'actual_seconds':f['actual_playback_seconds']})
(run/'support/crops.json').write_text(json.dumps(crops,ensure_ascii=False,indent=2),'utf-8');print(len(crops))
