from pathlib import Path
import json,hashlib,re,subprocess,sys
O=Path(__file__).resolve().parent
W=next(p for p in O.parents if (p/'AGENTS.md').exists())
S=W/'knowledge-linked-skill-20261019/candidate/company-video-grammar-analyzer'
P=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
paths=[(W/'AGENTS.md','instructions'),(S/'SKILL.md','skill instructions')]
paths += [(S/'references'/n,'skill reference read in full') for n in ['knowledge-connections.md','collection-record.md','design-and-patterns.md','pattern-composition.md','evidence-and-records.md','knowledge-sidecar.md','source-readback.md']]
paths += [(S/'scripts/knowledge_links.py','tool source lines1-180 inspected; CLI executed')]
paths += [(W/'knowledge-linked-skill-20261019/eval-inputs/input.md','provided metadata')]
paths += [(p,'provided prior analysis read in full') for p in (W/'knowledge-linked-skill-20261019/eval-inputs/static').glob('*.md')]
paths += [(p,'provided PNG viewed full and corresponding native-pixel ROIs') for p in (W/'knowledge-linked-skill-20261019/eval-inputs/static/evidence').glob('*.png')]
paths += [(P/n,'context read in full') for n in ['14_스킬재구성/R8_현재사용안내.md','00_분석단계_지식연결_추가안내.md','01_진행현황.md','13_품질검수/03_판정운영기준.md','03_한맥디자인/07_회사CI와_화면역할_연결규칙.md','05_출처와검토/스킬심층검토/07_편집디자인과화면설계_추가검토.md']]
A=P.parent/'Phase 01-A/05_결과보고/2026-10-19_Phase00_지식연결_재감사'
paths += [(A/n,'context read in full; no prior example/results content read') for n in ['00_읽는순서와_현재상태.md','05_R1-R8_연결과_수집계약.md']]
paths += [(P/n,'selective semantic reading: see selected-concept-source; whole file cataloged/pinned') for n in ['01_공통용어/공통용어사전.json','02_원칙과레이아웃/모션과정보전달원칙.json','02_원칙과레이아웃/화면설계원칙.json','02_원칙과레이아웃/레이아웃지식.json','13_품질검수/품질항목_정본.json']]
paths += [(P/'02_원칙과레이아웃/레이아웃_심화지식.json','selected NETWORK/SPLIT/SPACE-CALLOUT cards fully read; initial broad render truncated'),(P/'02_원칙과레이아웃/모션원칙_심화카드.json','selected IP-04/MR-03 cards fully read'),(P/'10_공용자산/자산목록.json','top-level schema/field names only; asset contents not reviewed')]
save('read-manifest.json',[{'path':str(p),'sha256':sha(p),'actual_read_scope':scope} for p,scope in paths])
R=json.loads((O/'knowledge-links.json').read_text(encoding='utf-8'))
units={u['id']:u for u in R['units']}
roundtrips=[]
for q in ['work','building','roleplate','space','tiles','group','question','observed-motion','investigations']:
    data=json.loads((O/f'queries/{q}.json').read_text(encoding='utf-8'))
    for hit in data['uses']:
        u=hit['use']; assert u['definition_id'] in units
        assert u['definition_version']==units[u['definition_id']]['definition_version']
        assert all((O/e['path']).is_file() and sha(O/e['path'])==e['sha256'] for e in hit['evidence'])
        roundtrips.append({'query':q,'definition':u['definition_id'],'version':u['definition_version'],'use':u['id'],'case':u['case_unit_id'],'content':u['content_context'],'evidence':[e['path'] for e in hit['evidence']],'differences':u['differences'],'unverified':u['unverified'],'result':'resolved'})
active=[]
for p in O.glob('0*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if not link.startswith(('http','D:','C:')):
            target=link.split('#')[0]
            if target: active.append({'file':p.name,'target':target,'exists':(O/target).exists()})
assert all(x['exists'] for x in active)
save('roundtrip-verification.json',{'resolved_routes':roundtrips,'active_document_links':active,'scope':'explicit link and file/hash resolution, not semantic correctness'})
cmd=[sys.executable,'-B','-X','utf8',str(S/'scripts/knowledge_links.py'),'check','--catalog',str(O/'knowledge-catalog.json'),'--record',str(O/'knowledge-links.json')]
proc=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');assert proc.returncode==0,proc.stderr
(O/'final-check-result.json').write_text(proc.stdout,encoding='utf-8')
log='''# 실제 실행 기록 — 정지 지식 연결

지정 prompt: 134·172초 원본 PNG/기존 기록을 대조하고 Phase00 지식 연결 DB 수집 및 작동하는 조회 색인을 만들었다. 지정 스킬 draft.13과 제공 입력만을 관측자료로 썼다. 다른 실행/답안/채점/비교 자료는 열람하지 않았다. 최신 안내의 기존 사례/색인 예시 본문과 결과도 읽지 않았다. 작업 범위는 with_skill/outputs와 이 execution.md이며 정본/원본/스킬을 수정하지 않았다.

## 실제 열람

정확 경로·SHA·열람깊이는 outputs/read-manifest.json. 루트 AGENTS, 지정 SKILL, 지식연결/부속색인/수집/디자인/조합/근거/재대조 계약, 입력 input.md 및 static MD5개, PNG2개를 읽었다. PNG전체는2048×576표시로 보고 PIL로 원본픽셀 ROI8개를 잘라 original detail로 열람했다. 좌표/파생해시는 roi-manifest.json. 이전기록의 ‘7개ROI 확인’은 과거이력이며 이번실행은 제공PNG에서 새로8개크롭을 확인했다.

Phase00 R8/최신추가안내/진행현황/CI역할/판정운영/편집디자인 문맥과 최신R1–R8연결을 읽었다. 카탈로그167개/11문맥은파일pin이며 전체의미전수검토가 아니다. 선택 개념27개는 selected-concept-source.json에 보존했고 심화는 NETWORK/SPLIT/SPACE-CALLOUT, IP-04/MR-03을 전문선택열람했다. 자산목록은스키마만확인; 공식로고파일대조는하지않았다. 레이아웃심화 초기넓은출력은잘려 선택카드를다시정확히읽었다. workspace 전체 rg는런타임파일명탐색만했고 다른평가본문을읽지않았다. PowerShell의InitializeDefaultDrives경고가있었으나 실제파일읽기/실행은성공했다.

## 실행 명령

Python: `C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -B -X utf8`. 스크립트는지정스킬/scripts/knowledge_links.py. `catalog --phase00 <공통input의Phase00> --out <outputs/knowledge-catalog.json>`을실행했다. 이후 outputs/prepare.py(입력MD/PNG그대로복사·크롭·선택개념보존), outputs/build.py(수집MD/부속원본·색인·check/query), outputs/finalize.py(열람대장·링크왕복·최종check)를실행했다. 모두 -B/UTF-8을사용하여스킬/정본경로에pycache를만들지않았다.

실제check/index/query 전체argv·종료코드는 outputs/commands.json. 복사해서실행할조회명령은 outputs/run_queries.ps1. build.py는한국어표현과현재MDpin/사용내용연결을보완한후재실행했으며 입력/보존원문은변경하지않았다. 최종check는 outputs/final-check-result.json.

## 실제 결과

기존MD5개바이트동일, PNG해시입력일치. 16단위(사례2·레이아웃2·부품8·미관측조사4),16사용처,50지식연결,14범위별검토행. check/index/10query 모두종료0. 업무이미지1사용처, 건물/기단2검색일치(업무묶음의제외/차이언급도문자열일치), 역할판2검색일치(전체역할판과헤더), 공간주석3, 연결구성1, 타일2, 근접정렬4, Q-SCREEN-01실제2, 관측모션0/미관측조사4. 부분문자열검색의문맥일치와정확개념분류를구별한다.

outputs/roundtrip-verification.json은조회→정의전체ID/판본→현재내용/사례/근거파일해시·차이/미검증의왕복과현재안내MD링크존재를검사했다. 기존prior내과거original/scratch/절대경로는역사이력이며입력에없는원기록을복원/대체하지않았다. 현재활성근거는outputs/evidence와새문서에서연결했다.

## 미상·제한·다음 범위

완료범위는두정지화면의수집연결/자기재대조/읽기전용조회다. 실제MP4/오디오/시나리오/PTS로그/편집자산이없어모션·음성싱크·원제작의도/같은자산·정확효과원값은확정하지않았다. 산정표/공식CI사용형·다른자료/화면비응용은미검수다. pass는표시수치/방향/묶음의정적기록대응에한정하고산정타당성·시간가독성·연속성은hold, CI자산대조는not_reviewed. 새화면/영상/PDF·회사정본등록·실사용스킬교체를하지않았다. 일반화시험/스킬성능채점/회사승인이아니다.
'''
(O.parent/'execution.md').write_text(log,encoding='utf-8')
print(json.dumps({'resolved_routes':len(roundtrips),'active_document_links':len(active),'all_active_links_exist':True,'final_check':json.loads(proc.stdout),'execution':str(O.parent/'execution.md')},ensure_ascii=False,indent=2))
