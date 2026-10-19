from pathlib import Path
import subprocess,json,hashlib,importlib.util
R=Path(__file__).resolve().parent
P=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00')
cmd=[str(P/'.환경/Scripts/python.exe'),'-B','-X','utf8',str(P/'07_실행도구/R6_출처사용검사.py')]
r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
data={'command':cmd,'exit_code':r.returncode,'result':json.loads(r.stdout),'stderr':r.stderr,'scope':'기존 R6의 출처 연결/동일성 검사 재실행. 내용/권리/효과 승인 아님'}
(R/'data/r6-current-source-check.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
spec=importlib.util.spec_from_file_location('lookup',R/'문법색인/조회.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
examples=[('정확 ID 분할',dict(concept='LAYOUT-SPLIT')),('업무 묶음',dict(query='업무 이미지 묶음')),('건물/기단',dict(query='건물 기단')),('수치/도상 시차',dict(query='숫자 도상 시차',motion_only=True)),('정지 화살표를 모션으로 검색',dict(query='134초 화살표 모션',motion_only=True)),('새 시안의 교체 모션',dict(query='가족사별→업무별')),('관련 원칙',dict(concept='MR-08'))]
rows=[]
for name,args in examples:
    out=m.lookup(**args);rows.append({'query':name,'arguments':args,'result':out})
(R/'data/lookup-examples.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 이번 확인과 실제 조회 결과','구조/연결/검색 경계의 자체 검사다. 디자인 의미 정확도·시청자 효과·스킬 일반 성능을 평가한 시험이 아니다.','| 질의 | 반환 | 구분 |','|---|---|---|']
for row in rows:
    md.append('| '+row['query']+' | '+(', '.join(u['id']+' '+u['title'] for u in row['result']['results']) or '관측 결과 없음')+' | '+('원칙 효과 아닌 검토 관련성' if row['arguments'].get('concept')=='MR-08' else '해당 색인 범위')+' |')
v=json.loads((R/'data/validation.json').read_text(encoding='utf-8'))
md += ['\n검사 '+str(v['passed'])+'/'+str(v['total'])+' 통과: ID/연결/원본 보존, 정확ID 분할/분할비교 구분, 미관측/새 제안 제외, 변경된 출처 pin 거부, 새 문서 링크 존재를 확인했다. **시범 corpus13행의 규칙적 조회**이며 실제 사용자가 원문 없이 적절한 사례를 찾는지·유사어/자유 질문 검색 품질은 아직 시험하지 않았다.',
'R6 재검사: 544행의 원문/복구 해시 연결 유효, 내용 검증/권한/회사 승인 false. 첫 직접 경로 검사에서 호스트 캐시4개가 없었지만 기존 R6 복구별칭을 대조한 뒤 모두 해시가 일치했다. 구버전 source 대장은 수정하지 않았다.',
'첫 오류 주입 시험은 sandbox 임시 디렉터리 접근 오류로 중단됐고 작업 폴더의 별도 fixture로 다시 수행했다. 그 실패를 통과 횟수에 넣지 않았다. 오류 fixture에만 잘못된 해시를 넣었으며 정본/실제 pin은 변경하지 않았다.',
'감사 원문·분석기 active10/candidate12의 해시와 보존 원문 일치를 확인했다. 판본/실제 영상의 내용 정확도를 해시로 대체하지 않는다.',
'[기계 검사 결과](data/validation.json) · [실제 조회 JSON](data/lookup-examples.json) · [R6 결과](data/r6-current-source-check.json)',
'조회용 `문법색인/조회.py`는 읽기 전용이다. `build_audit.py`, `inspect_sources.py`, `save_checks.py`, `verify.py`는 이번 작업 재현용 기록이며 지정 C: workspace와 D: 원문에 의존한다. 사용자가 조회할 때 실행할 필요 없다.']
(R/'09_검증과_실제조회.md').write_text(md[0]+'\n\n'+md[1]+'\n\n'+'\n'.join(md[2:])+'\n',encoding='utf-8')
print('saved R6 check and '+str(len(rows))+' lookup examples')
