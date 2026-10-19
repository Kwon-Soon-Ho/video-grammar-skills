from pathlib import Path
import json,hashlib,datetime
B=Path(__file__).resolve().parent;W=B/'company-video-grammar-analyzer-workspace'
def grade(case,mode,rows,notes=(),issues=(),iteration='iteration-1'):
    folder=W/iteration/('eval-'+case)/mode
    root=W/'seals' if iteration=='iteration-1' else W/'seals'/iteration
    seal=json.loads((root/(case+'-'+mode+'.json')).read_text(encoding='utf-8'))
    for n,h in seal['files'].items():assert hashlib.sha256((folder/'outputs'/n).read_bytes()).hexdigest()==h
    meta=json.loads((folder.parent/'eval_metadata.json').read_text(encoding='utf-8'));assert len(rows)==len(meta['assertions'])
    expectations=[{'text':t,'passed':bool(p),'evidence':e} for t,(p,e) in zip(meta['assertions'],rows)]
    result={'case_id':case,'condition':mode,'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'grader':'root source/meaning review; not independent human','reference_level':meta['reference_level'],'expectations':expectations,'summary':{'passed':sum(x['passed'] for x in expectations),'failed':sum(not x['passed'] for x in expectations),'total':len(expectations)},'case_status':'requirements_satisfied' if all(x['passed'] for x in expectations) else 'needs_revision','notes':list(notes),'timing':None,'tokens':None,'telemetry_note':'per-run telemetry unavailable; no synthesized averages','eval_feedback':{'suggestions':['Known exposed windows, one run per condition, same agent batches; this is regression evidence, not generalization accuracy.']}}
    result['additional_content_issues']=list(issues)
    if issues:result['case_status']='needs_revision'
    p=folder/'grading.json';assert not p.exists();p.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(case,mode,result['case_status'])

if __name__=='__main__':
    grade('T01','without_skill',[(True,'O3: 서로 어긋난 다섯 수평 구간의 진입과 조립을 기록. T01 board1에서 높이별 경계 차이를 확인.'),(True,'O3: 왼쪽 경계→오른쪽. 3.6/3.9/4.2 프레임과 일치.'),(True,'O4: 4.2→4.5→4.8→5.1에서 이동량이 줄어듦을 관측. 실제 E 외곽 정착과 일치.')],['정확한 키프레임은 가설/미상으로 보존. 스킬 없이도 이 사건을 발견했다.'])
    grade('T02','without_skill',[(True,'O3에서 얇은 사각 선틀과 위/왼쪽 아래 가로 빛띠를 본체 패널 O2와 구분. 원본 0.4~1.4 표본과 일치.'),(True,'빛띠의 존재를 O3에 유지하고 가감속은 따로 확정하지 않음.'),(True,'광선 오버레이는 가설이며 전체 외곽 경로/정확한 이징을 확정하지 않음.')],['빛 통과 방향/정밀 곡선은 자세히 기록하지 않았지만 고정 필수 기준은 존재와 분리이다. 기준을 사후 강화해 실패로 바꾸지 않음.'])
    grade('T03','without_skill',[(True,'O1 십자와 O2/O3 점선 사각 영역을 각각 기록.'),(True,'O2의 위·왼쪽 기준 유지/우·하 경계 확장과 Value of 노출은 1.9~2.4 원본과 일치.'),(True,'O5의 3.1~3.5 경계 축소, 밝은 부분 제거,3.6 흐린 잔존을 원본과 대조.'),(True,'글자 축소로 쓰지 않고 흰 영역 축소로 표현; 실제 매트/opacity 구현은 hypotheses와 미상으로 분리.')],['부제/본문의 정밀 이동곡선은 필수 기준 밖 미세 관측. 추가 미상은 결과에 유지.'])
