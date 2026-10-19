from pathlib import Path
import hashlib,json,shutil
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def main():
    old=ROOT/'internal-video-audit-20261019/candidate/company-video-grammar-analyzer'
    new=OUT/'candidate/company-video-grammar-analyzer'
    pins=[]
    for p in old.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:
            q=new/p.relative_to(old);q.parent.mkdir(parents=True,exist_ok=True)
            if not q.exists(): shutil.copy2(p,q)
            pins.append({'source':str(p),'relative':p.relative_to(old).as_posix(),'sha256':sha(p)})
    frames={
      'N177': ROOT/'case-benchmarks-20261019/extraction/cases/NEW-N/scout/f_05310_177.000.png',
      'N175': ROOT/'case-benchmarks-20261019/extraction/cases/NEW-N/scout/f_05250_175.000.png',
      'P47': ROOT/'analysis-reliability-20261019/fresh/cases/NEW-P/window/f_01410_047.000.png',
      'P53': ROOT/'case-benchmarks-20261019/extraction/cases/NEW-P/scout/f_01590_053.000.png'}
    crops={'N177':{'header':[0,30,1300,255],'label_left':[1250,230,2900,410],'label_right':[5150,230,6750,410],'caption':[2350,1920,5350,2100],'section':[4900,700,6900,1550]},
           'P47':{'police_frame':[170,180,1200,650],'regional_frame':[1430,70,2440,650],'police_card':[340,770,1020,1030],'regional_card':[1580,770,2260,1030],'connector':[1880,590,1960,810]},
           'P53':{'regional_context':[2300,50,3840,1050]}}
    evidence=[]
    for key,p in frames.items():
        im=Image.open(p).convert('RGB')
        e={'id':key,'path':str(p),'sha256':sha(p),'canvas':list(im.size),'seconds':int(key[1:]),'crops':[]}
        for name,box in crops.get(key,{}).items():
            dest=OUT/'inspection'/f'{key}-{name}.png';dest.parent.mkdir(exist_ok=True)
            if not dest.exists(): im.crop(box).save(dest)
            e['crops'].append({'path':str(dest),'sha256':sha(dest),'box_ltrb':box})
        evidence.append(e)
    save(OUT/'inputs.json',{'evidence':evidence,'draft8_source_files':pins,'prior_receipt':{'path':str(ROOT/'case-benchmarks-20261019/publication-receipt.json'),'sha256':sha(ROOT/'case-benchmarks-20261019/publication-receipt.json')}})
    save(OUT/'decision.json',{'question_id':'call_e274b5ae3d0e4e278906ef4a98828352','answer':'① 현재 분류 유지·전체 디자인 기록 보강 (추천): 글자 크기 관계, 영역 비율, 여백, 프레임·선·배경층을 더 구체적으로 적고 재사용에 중요한 수치만 측정합니다.','scope':'두 기준 사례의 기존 번호·분류 유지, 전체 디자인 보강, 반복 적용 지침 보완. 영상 전체 확장·새 패턴 등록·원본 제작 설정 확정은 이번 묶음 밖.','source_review_request':str(ROOT/'case-density-review-20261019/review-request-01.json')})
    print(json.dumps({'frozen_draft8_files':len(pins),'frames':len(evidence),'crops':sum(len(x['crops']) for x in evidence)}))
if __name__=='__main__':main()
