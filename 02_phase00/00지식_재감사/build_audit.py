from pathlib import Path
import json,hashlib,collections,shutil,re

R=Path(__file__).resolve().parent
W=Path('C:/Users/User/Documents/ChatGPT/업무@사내 영상 생성기')
P=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00')
A=W/'collection-skill-structure-20261019/candidate/company-video-grammar-analyzer'
ACTIVE=P.parent/'Phase 01-A/03_분석스킬/company-video-grammar-analyzer'
I=R/'문법색인'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.rstrip()+'\n',encoding='utf-8')
def dump(p,s):write(p,json.dumps(s,ensure_ascii=False,indent=2))
def link(p,label=None):return f'[{label or p.name}](<{p.as_posix()}>)'
def md(s):return str(s).replace('|','／').replace('\n',' ')

tax=read(P/'01_공통용어/공통용어사전.json')
motion=read(P/'02_원칙과레이아웃/모션과정보전달원칙.json')['principles']
screen=read(P/'02_원칙과레이아웃/화면설계원칙.json')['principles']
layouts=read(P/'02_원칙과레이아웃/레이아웃지식.json')['layouts']
quality=read(P/'13_품질검수/품질항목_정본.json')['cards']
cards=read(P/'05_출처와검토/스킬심층검토/스킬심층검토정본.json')['cards']
ledger=read(P/'05_출처와검토/스킬심층검토/검토파일목록.json')['records']
integrity=read(R/'data/source-file-integrity.json')
assert len(cards)==40 and len(ledger)==544
assert all(r['resolved_match'] for r in integrity)

# 감사 범위의 파일 고정. 디렉터리 전체/외부 저장소 전체를 읽었다고 표현하지 않는다.
pins=[]
for folder in ['01_공통용어','02_원칙과레이아웃','03_한맥디자인','04_기록규격','05_출처와검토/스킬심층검토','13_품질검수','14_스킬재구성']:
    for f in sorted((P/folder).glob('*')):
        if f.is_file() and f.suffix in ['.json','.md']:
            pins.append({'role':'phase00_reference','path':str(f),'sha256':sha(f),'read_depth':'inventory_pin_not_automatically_full_semantic_review'})
for base,role in [(A,'candidate12'),(ACTIVE,'active10')]:
    for f in sorted(base.rglob('*')):
        if f.is_file():pins.append({'role':role,'path':str(f),'sha256':sha(f)})
dump(R/'data/protected-source-pins.json',pins)

# 이번에 실제 다시 열어 읽은 원문/절. 기존 544행의 정적 검토 이력을 재수행으로 바꾸지 않는다.
full_suffixes=[
 'design-critique/skills/reference-building/library-architecture/SKILL.md',
 'design-critique/skills/reference-building/principle-tagging/SKILL.md',
 'design-critique/skills/analysis/decision-tracing/SKILL.md',
 'lottiefiles/skills/motion-design/director/choreography.md',
 'editorial-information/SKILL.md','editorial-information/references/grid-system.md',
 'graphic-design-suite/skills/layout-composition/SKILL.md',
 'antv-infographic/skills/infographic-syntax-creator/SKILL.md']
partial_suffixes={'design-system/skills/design-system/references/design-tokens.md':'1–125행: 정의·원시/의미 역할',
 'graphic-design-suite/skills/typography/SKILL.md':'1–85행: 현재 context·타입 척도·font pairing'}
new_reads=[]
for row in ledger:
    norm=row['path'].replace('\\','/')
    for suffix in full_suffixes+list(partial_suffixes):
        if norm.endswith(suffix):
            new_reads.append({'path':row['absolute_path'],'sha256':row['sha256'],'this_audit_depth':'full_text_static_reread' if suffix in full_suffixes else 'selected_sections_reread','section':partial_suffixes.get(suffix,'전체 본문'),'executed':False})
dump(R/'data/this-audit-raw-rereads.json',new_reads)

# 의미 대조는 아래 수작업 판단이다. keyword hit 개수를 적용률로 계산하지 않는다.
cap_rows=[
 ('C01','목적·정보 관계·주장','PURPOSE/REL 17개, 레이아웃 심화의 선택 조건','references/collection-record.md','전달 대상/정보 관계','의미 관계는 기록한다. 양방향 서비스 교환·책임·입출력 등은 기존8관계에 강제하기 어렵다. 문서/화면/해석별 관계의 근거와 적용 범위를 구조화해야 한다.'),
 ('C02','구도·격자·정렬·여백','14 레이아웃+심화카드, 편집화면 검토의 별도 격자축','references/design-and-patterns.md','화면비, 전체 구도','전체 배치·정렬은 지침에 있다. 격자/영역 조합을 유형과 분리해서 검색하는 필드는 없다. 실제 화면 판면의 설계 논리가 자유문에 묻힌다.'),
 ('C03','타이포·한국어·텍스트 역할','SCREEN-TYPE-KO·TIME-READ, Q-TEXT 3개','references/design-and-patterns.md','문구·서체 특징·크기 관계','크기 관계/서체 특징은 수집한다. 제목·지표·단위·설명·출처의 역할, 줄바꿈/숫자 정렬/대체 글꼴과 화면비별 제약을 독립 검색하기는 어렵다. 정확 글꼴 미상은 허용한다.'),
 ('C04','색·재질·공간·디자인 언어','표현속성5개, R5 색/역할/CI 분리, 편집화면 source cards','references/collection-record.md','배경/전경','재질·층·위계는 서술한다. 개별 값을 묶는 시각 언어 프로필, 역할 색과 재질/조명/투영의 조합·가변 범위가 공통 조회 구조로 연결되지 않았다.'),
 ('C05','데이터·도표·시각 부호','SCREEN-DATA·Q-SCREEN-05·AntV/Chart 검토','references/source-readback.md','수치','수치/단위/귀속과 중간값 경계는 보강됐다. 어느 데이터 필드가 위치·길이·면적·색으로 표현되는지, 척도·분모·집계·결측을 구분한 전용 기록은 약하다. 큰 숫자를 차트로 분류하면 안 된다.'),
 ('C06','전체 흐름·세부 모션·시간 관계','모션43+심화43, 추가 UX12연결후보, timing13','references/motion-review.md','의미가 관련된 숫자','대상별 순서·중첩·내부/주변·가감속의 관측 지침은 비교적 구체적이다. 공통 사건/상태/안무 단위와 검색은 자유문 중심. 최근2정지 표본에는 실제 모션 근거가 없다.'),
 ('C07','설명 순서·음성/화면의 결합','IP05/06/08/09, 발표/설명 스킬, Q-CAP4','SKILL.md','실제로 듣거나','미청취 음성을 미검수로 둔다. 설명·장면 순서와 문구/음성/시각 공개의 관계를 구조화하는 부분은 부족하다. 분석과 새 시나리오 작성은 구분해야 한다.'),
 ('C08','패턴 정의·조합·사용처·조건','R2 용어, R4 단위, library/tagging·Ponytail 색인 사고','references/pattern-composition.md','포함','정의/판본/현재 근거·차이·묶음은 있다. Phase00 개념에서 실제 언제/어떤 내용/어떤 역할에 사용됐는지 역조회가 없었다. 이번 별도 색인은 이 한정 연결을 추가한다.'),
 ('C09','관측·추론·근거·변환 이력','R4v0.2 시간·공간·주장, R6 출처, data-cleaning·REA','references/evidence-and-records.md','근거','분리는 지침/JSON0.4 일부에 있다. Markdown 기록을 R4통합v0.2로 옮기는 검증된 변환기는 없다. hash와 구조검사 통과는 의미 정확도나 관측을 보증하지 않는다.'),
 ('C10','비평·반례·선택 이유·예외','원칙 심화/충돌, 레이아웃 반례, Q26','references/judgment-handoff.md','condition_candidates','조건/미시험 반례/새 제안은 구별한다. 실제 사례에 어떤 검토 질문을 적용해 무엇을 보류했는지의 항목별 결과는 공통으로 연결되지 않았다. 비평 질문이 있다는 것과 판정 수행은 다르다.'),
 ('C11','브랜드·CI·자산·권한','R1/R5/R6, 8회사/135자산, 원색과 의미역할','references/design-and-patterns.md','색','색·문구·브랜드 승인 구분은 문서에 있다. 현재 관측색에서 승인 프로필/회사별 자산으로 정확히 연결하는 공통 조회는 별도 필요. 유사한 금색을 공식CI로 단정하지 않는다.'),
 ('C12','스킬 재구성·실행 평가','R8 helpers/Anthropic creator 및 iteration2·3','SKILL.md','독립 실행 성능','기존판/후보를 실제 두 과제에 실행했다. 같은 자료 반복·AI 평가·소수 실행이므로 다른 영상 일반화나 전체 source 이식 효과를 입증하지 않는다. 이번은 감사/연결 작업이며 새 성능 실험이 아니다.'),
 ('C13','정본·초안·판정·변경 관리','R1–R8, 3역할 helper, per-item 판정','references/review-ledger.md','검수','초안/보존/회사 승인 구분은 있다. 실제 분석기 경로에서 Phase00 현재 문맥/지식·R7 질문을 가져오는 필수 인계와 누락 점검이 약하다. 본 감사의 연결 안내는 이를 보완하며 기본 스킬은 교체하지 않는다.')]
caps=[]
for key,name,phase,rel,needle,gap in cap_rows:
    f=A/rel;lines=f.read_text(encoding='utf-8-sig').splitlines();matches=[n for n,s in enumerate(lines,1) if needle in s]
    caps.append(dict(id=key,name=name,phase00_location=phase,candidate_path=str(f),candidate_sha256=sha(f),line_matches=matches,match_use='위치 안내만; 자동 의미 채택 판정 아님',assessment='partial_connection',finding=gap))
dump(R/'data/capability-audit.json',caps)

mapping={
'taste-main':['C01','C10'],'taste-redesign':['C03','C11','C13'],'impeccable':['C02','C03','C10'],
'anthropic-frontend':['C01','C04'],'anthropic-canvas':['C02','C04'],'anthropic-brand':['C11'],
'anthropic-creator':['C12'],'lottie':['C06','C07','C10'],'design-system':['C03','C04','C08','C11'],
'authoring':['C11','C13'],'reviewing':['C09','C10','C13'],'critique-suite':['C01','C02','C03','C06','C08','C10'],
'data-cleaning':['C05','C09'],'local-animation-principles':['C06','C10'],
'local-brand-motion-guidelines':['C06','C08','C11'],'local-accessible-animation':['C06','C07','C10'],
'local-shot-composition':['C02','C06'],'local-design-tokens':['C03','C04','C11'],
'anthropic-pptx':[],'presentation-narrative':['C01','C07'],'academic-presentation':['C01','C05','C07'],
'presentation-builder':['C02','C05','C07'],'antv-infographic':['C01','C02','C05','C08'],
'local-creative-brief':['C01','C10'],'local-explainer-video':['C01','C07'],'local-presentation-video':['C06','C07'],
'local-animated-infographic':['C02','C05','C06'],'local-diagram-animation':['C01','C05','C06'],
'local-chart-animation':['C05','C06'],'local-motion-art-direction':['C04','C06'],
'local-visual-qa':['C09','C10'],'local-visual-style-direction':['C01','C04','C11'],
'host-presentations':['C02','C03','C05','C11'],'graphic-suite':['C02','C03','C04','C10','C11'],
'editorial-information':['C01','C02','C05','C09','C10'],'editorial-vision':['C04','C09','C11'],
'swiss-design':['C02','C03'],'graphic-role':['C03','C04','C11'],'local-pixel':['C02','C09'],
'local-drawio':['C01','C08','C09']}
assert set(mapping)=={c['id'] for c in cards}
matrix=[]
for n,c in enumerate(cards):
    cap_ids=mapping[c['id']]
    matrix.append(dict(source_card_id=c['id'],source_package=c['source_package'],name=c['name'],
      original_card_pointer=f'/cards/{n}',source_catalog=str(P/'05_출처와검토/스킬심층검토/스킬심층검토정본.json'),
      retained_candidates=c['retain_as_proposal'],excluded_or_conditional=c['exclude_or_rewrite'],
      source_entrypoints=c.get('entrypoints',[]),capability_refs=cap_ids,
      current_assessment='intentional_non_import' if not cap_ids else 'partial_semantic_connection_not_full_implementation',
      direct_copy_state='held' if c['id'] in ['anthropic-pptx','academic-presentation','local-drawio'] else 'not_performed_by_this_audit',
      source_unresolved=c.get('unresolved',[]),this_audit_method='기존40카드의 선별/제외 항목 전부 대조; 원문 신규 재열람은 별도10파일 목록. 전체 원문 재심사/런타임 검증 아님'))
dump(R/'data/40-source-card-crosswalk.json',matrix)

text=['# 00 조사 스킬 40개 검토 단위 — 실제 연결 감사',
'여기서 40은 스킬 개수가 아니라 기존 심층 검토 카드 수다. 한 카드에 10~11개 entrypoint가 묶이기도 한다. source 원문/참조/코드 전체를 이번에 다시 전수 실행한 것이 아니다. 각 카드의 기존 선별·제외 항목 전부를 현재 후보 지침/실제 수집 구조와 비교했다. 원문 재열람 10파일의 범위와 원문544행의 검토 깊이는 별도 JSON에 남겼다.',
'“연결됨”은 원칙 이름이 문서에 등장한다는 뜻만으로 부여하지 않았다. 지식 보관 → 실행 지침 → 출력 기록 → 검색 → 실제 검수는 각각 다른 수준이다. 대부분 지침/서술 일부는 있으나 전체 사용 연결은 부족하다. 소수 과제 점수로 이식 완료율을 만들지 않는다.',
'[기능별 실제 위치와 결함](03_기능별_연결단절.md) · [원문/해시/검토 깊이](data/source-file-integrity.json) · [이번 재열람](data/this-audit-raw-rereads.json)']
for r in matrix:
    text += [f"## {r['source_card_id']} — {r['name']}",f"기존 카드: {link(Path(r['source_catalog']))} `{r['original_card_pointer']}`. 대응 기능: {', '.join(r['capability_refs']) or '이식 대상 없음'}. 판정: {'의도적 제외' if not r['capability_refs'] else '부분 연결; 전체 반영으로 볼 수 없음'}.",
      '**기존 선별 후보 전체:**\n\n'+'\n'.join('- '+s for s in r['retained_candidates']) if r['retained_candidates'] else '**선별 후보 없음. 해당 직접 이식은 보류.**',
      '**그대로 가져오지 않을 부분:**\n\n'+'\n'.join('- '+s for s in r['excluded_or_conditional']),
      '남은 확인: '+' / '.join(r['source_unresolved'])]
write(R/'02_스킬40묶음_대조.md','\n\n'.join(text))
text=['# 기능별로 본 연결과 실제 단절','대조 대상은 draft.12 개발 후보 지침이다. 실제 사용판 draft.10은 별도로 고정했으며 교체하지 않았다. 아래 line hit는 위치를 찾기 위한 보조이고, 해당 기능 전체가 구현됐다는 자동 판정이 아니다.']
for c in caps:
    f=Path(c['candidate_path']);ln=c['line_matches'][0] if c['line_matches'] else 1
    text += [f"## {c['id']} {c['name']}",f"00 보유: {c['phase00_location']}",f"현재 지침 일부: [{f.name}](<{f.as_posix()}:{ln}>)",f"감사 판단: {c['finding']}"]
write(R/'03_기능별_연결단절.md','\n\n'.join(text))

# 원본에 주석을 쓰지 않는 추가 색인. 판본/정본의 예시 필드가 빈 사실을 그대로 보존한다.
uses=read(W/'grammar-usage-index-20261019/data/uses.json')
shutil.copytree(W/'collection-skill-structure-20261019/records',I/'records',dirs_exist_ok=True)
shutil.copytree(W/'value-creation-collection-20261019',I/'prior',dirs_exist_ok=True)
(I/'evidence').mkdir(exist_ok=True)
for f in (I/'records/evidence').glob('*.png'):shutil.copy2(f,I/'evidence'/f.name)
for f in (I/'prior/evidence').glob('*.jpg'):shutil.copy2(f,I/'evidence'/f.name)
dump(I/'data/uses.json',uses)
catalog=[]
for t in tax['terms']:
    catalog.append({**t,'kind':'term','source_path':str(P/'01_공통용어/공통용어사전.json')})
for k,items,file in [('motion_principle',motion,'모션과정보전달원칙.json'),('screen_principle',screen,'화면설계원칙.json'),('layout_knowledge',layouts,'레이아웃지식.json')]:
    for t in items:catalog.append({**t,'kind':k,'source_path':str(P/'02_원칙과레이아웃'/file)})
for t in quality:catalog.append({**t,'kind':'quality_question','source_path':str(P/'13_품질검수/품질항목_정본.json')})
dump(I/'data/catalog.json',catalog)
dump(I/'data/catalog-source-pins.json',[{'path':p,'sha256':sha(Path(p))} for p in sorted({c['source_path'] for c in catalog})])
deep_sources={
 '격자/편집디자인':str(P/'05_출처와검토/스킬심층검토/07_편집디자인과화면설계_추가검토.md'),
 '모션 심화/반례':str(P/'02_원칙과레이아웃/모션원칙_심화카드.json'),
 '추가 UX 모션12연결후보':str(P/'02_원칙과레이아웃/추가모션체계_연결후보.json'),
 '레이아웃 심화':str(P/'02_원칙과레이아웃/레이아웃_심화지식.json'),
 '표/순환/분기 확장후보':str(P/'02_원칙과레이아웃/레이아웃_확장후보.json')}
dump(I/'data/additional-knowledge-links.json',deep_sources)
observed=[r for r in uses if r['kind'] in ['static','prior_sampled_motion']]
def use_link(r):return f"[{r['id']} {r['title']}](02_사용처.md#{r['id'].lower()})"
toc=['# 문법에서 사용처까지 — 지식 목차',
'이 목차는 정본의 새 판본이 아니라 추가 조회 색인이다. 75개 신규용어와 폐기ID1개, 기본 지식65개, 품질 질문26개를 종류별로 펼친다. 원칙의 검토 관련 링크와 관측된 구성/속성 분류를 구별한다. 사용처 없음은 이 색인에 연결한 범위에서 없다는 뜻이며 사내 영상 전체에 없다는 뜻이 아니다.',
'[사용처 전체](02_사용처.md) · [규격 검토](../04_권장_기록구조.md) · [00 전체 연결](../05_R1-R8_연결과_수집계약.md)']
for ax in tax['axes']:
    toc += [f"## {ax['name_ko']} — {ax['id']}", '| ID | 용어 | 연결한 관측 사용처 |','|---|---|---|']
    for t in tax['terms']:
        if t['axis']!=ax['id']:continue
        hits=[u for u in observed if t['id'] in u['grammar_tags']]
        toc.append(f"| {t['id']} | {t['name_ko']} | {'; '.join(use_link(u) for u in hits) if hits else ('폐기 → '+str(t.get('replaced_by')) if t.get('status')=='deprecated' else '이 색인에 미연결')} |")
for title,items in [('모션·정보 전달 원칙43',motion),('화면 설계 원칙8',screen),('레이아웃 지식14',layouts),('품질 검수 질문26',quality)]:
    toc += [f'## {title}','다음은 검토 시 참고할 지식 연결이다. 실제 원제작자의 적용 의도·좋은 효과 입증·사람 검수 통과를 뜻하지 않는다.','| ID | 이름 | 검토 관련 사용처 |','|---|---|---|']
    for t in items:
        hits=[u for u in observed if t['id'] in u['review_knowledge_refs']]
        toc.append(f"| {t['id']} | {t.get('name_ko',t.get('title',''))} | {'; '.join(use_link(u) for u in hits) if hits else '검토 결과/사용처 미연결'} |")
toc += ['## 65개 밖의 기존 지식',*['- '+link(Path(v),k) for k,v in deep_sources.items()]]
write(I/'01_지식목차.md','\n\n'.join(toc[:3])+'\n\n'+'\n'.join(toc[3:]))
usemd=['# 언제·어떤 내용에서 쓰였는가',
'새로 영상 전체를 관측한 결과가 아니다. 정지 사례5개 색인, 과거 표본 모션6개 색인, 미관측 조사1개, 새 시안 제안 제외1개다. 모두 같은 영상의 제한 범위다. 13행은 13개 독립 설계/반복 확인/정본 패턴을 뜻하지 않는다. 분류는 기록을 근거로 한 분석자의 해석이며 원제작 의도는 미확인이다. 원칙 연결은 검토 관련성이다.']
for u in uses:
    usemd += [f"<a id=\"{u['id'].lower()}\"></a>\n\n## {u['id']} {u['title']}",
      f"종류: `{u['kind']}` / 시각(초): {u['seconds']} / 원본 SHA: `{u['video_sha256']}` / 범위: 해당 상태 또는 표본 창.",
      u['content'], '연결 단위: '+', '.join('`'+s+'`' for s in u['local_units']),
      '관측 기록 기반 분류 해석: '+(', '.join(u['grammar_tags']) or '미부여'),
      '검토 관련 지식: '+(', '.join(u['review_knowledge_refs']) or '없음')+' — 원칙의 적용 효과/사용자 승인 증거 아님.',
      '근거: '+' · '.join(f'[{Path(e.split("#")[0]).name}]({e})' for e in u['evidence']),
      '조건/한계: '+u['limits']]
write(I/'02_사용처.md','\n\n'.join(usemd))
write(I/'00_읽는순서.md', '''# 문법 조회 시범 색인

먼저 [문법별 목차](01_지식목차.md)에서 개념을 찾고 [사용처](02_사용처.md)에서 언제·무엇을 설명했는지 본다. 이어 [사례 요약](records/00_사례요약.md) → 전체 상세 → 근거로 내려간다. 업무 묶음·건물/기단·명찰의 정의와 조합은 [부품 기록](records/01_부품과조합.md)에 있다.

모션은 과거 96–112초/136–150초 중 6개 표본 창의 기록을 연결했다. 최근 134·172초 두 정지 표본에 모션 관측을 새로 부여하지 않는다. 모션 상세·시간 경계·미검수는 [계약](prior/01_계약_수집기록.md), [지원](prior/02_프로젝트지원_수집기록.md), [표본 근거](prior/05_근거와_실행기록.md)를 확인한다. 총 창길이는 연속 관찰량이나 전편 완료율이 아니다.

`조회.py --concept ID`는 정확한 ID를 조회한다. `--query 문구`는 명칭/별칭/명시 색인의 문자열 검색이다. `--motion-only`는 관측 기록이 있는 모션만 반환한다. 미관측/제안은 기본 관측 결과에서 제외하고 `--include-unobserved` 또는 `--include-proposals`로 별도 확인한다. 의미 검색 모델·추천 품질·다른 영상 일반화 시험은 아니다.

정본65지식의 빈 case_refs/company_examples를 수정하지 않았고 원본 기록도 보존했다. 이 색인에서 새 사용처를 부여한 것은 분석 초안이다. 전체 지식의 회사 적용 여부를 판정한 것이 아니다.
''')

coverage={
 'taxonomy_active':sum(t.get('status')!='deprecated' for t in tax['terms']),
 'taxonomy_deprecated':sum(t.get('status')=='deprecated' for t in tax['terms']),
 'motion':len(motion),'screen':len(screen),'layout':len(layouts),'quality':len(quality),
 'empty_motion_case_refs':sum(not t.get('case_refs') for t in motion),
 'empty_screen_case_refs':sum(not t.get('case_refs') for t in screen),
 'empty_layout_company_examples':sum(not t.get('company_examples') for t in layouts),
 'prior_review_cards':len(cards),'prior_file_ledger_rows':len(ledger),
 'direct_hash_match':sum(x['match'] for x in integrity),'recovered_hash_match':sum(not x['match'] and x['resolved_match'] for x in integrity),
 'this_audit_raw_rereads':len(new_reads),'use_counts':dict(collections.Counter(x['kind'] for x in uses)),
 'all_principles_implemented':False,'canonical_db_modified':False,'active_skill_replaced':False,'actual_new_video_observation':False}
dump(R/'data/coverage-facts.json',coverage)

item_review=[]
related={'AP-01':['MP-06'],'AP-02':['MP-04'],'AP-03':['SCREEN-HIERARCHY'],
 'AP-05':['MP-07'],'AP-06':['MP-02'],'AP-07':['MP-05'],'AP-08':['MP-09'],
 'AP-09':['MP-01'],'AP-10':['MP-08'],'AP-12':['MP-10']}
for group,items in [('motion',motion),('screen',screen),('layout',layouts)]:
    for t in items:
        key=t['id'];decision='조건부 참고로 유지'
        reason='원문 개념/프로젝트 해석/관측/효과 판정을 구분하고 해당 사례의 범위와 근거를 연결한다.'
        if key=='AP-04':
            decision='제작 방식 지식으로 위치 명료화';reason='순차/주요 상태 설계는 제작 방법이다. 최종 렌더만으로 원제작의 작업 방식을 확정하지 않는다.'
        elif key in ['AP-11','AP-12','MP-03','MP-10']:
            decision='판단/해석 항목으로 구분';reason='입체 표현/무게감/매력은 실제 제작법·물리 질량·시청자 효과와 다르다. 보이는 특징과 평가 기준을 분리한다.'
        elif key in ['ACC-02','ACC-03']:
            decision='매체 조건부 분리';reason='영상 플레이어/상호작용 조건의 지식이다. MP4 도상의 직접 표현 규칙이나 정지 장면 패턴으로 전역 적용하지 않는다.'
        elif key in ['IP-05','IP-08','IP-10']:
            decision='입력/시청 조건 확인 후 적용';reason='실제 음성·시간 근거 또는 시청자 전문성 정보 없이 동기화/매체 분담/학습 효과를 판정하지 않는다.'
        elif group=='layout':
            decision='구성 유형으로 유지·기하 격자와 분리';reason='전체/하위 구역 범위와 조합을 기록한다. 유형 한 개만 고르거나 표/순환/분기를 억지로 매핑하지 않는다.'
        elif group=='screen':
            decision='상위 검수 질문으로 유지';reason='표현 어휘/패턴/사용처 DB를 대신하지 않는다. 대상·시청조건·근거와 항목별 판정을 연결한다.'
        if key in related:reason+=' 유사 항목은 관련/근접 관계 후보이며 자동 동일 병합/중복 감점하지 않는다.'
        if key.startswith('MP-'):reason+=' Jorge 체계의 공개 항목명과 프로젝트 적용 해석을 보관한 범위이며 유료 상세 강의 원문 검증과 구별한다.'
        item_review.append(dict(id=key,name=t['name_ko'],kind=group,disposition=decision,reason=reason,related_candidates=related.get(key,[]),canonical_changed=False,company_rule=False))
assert len(item_review)==65
dump(R/'data/65-item-review.json',item_review)
write(R/'07_65항목별_유지와_보완.md','# 65항목별 처분 검토\n\n원칙 수의 증감을 목표로 하지 않는다. 아래는 기존ID를 보존하는 분류/적용 검토안이다. 원문 정본이나 회사 승인을 수정한 것이 아니다.\n\n| ID | 항목 | 처분안 | 이유 |\n|---|---|---|---|\n'+'\n'.join(f"| {x['id']} | {md(x['name'])} | {x['disposition']} | {md(x['reason'])} |" for x in item_review))
print(json.dumps(coverage,ensure_ascii=False,indent=2))
