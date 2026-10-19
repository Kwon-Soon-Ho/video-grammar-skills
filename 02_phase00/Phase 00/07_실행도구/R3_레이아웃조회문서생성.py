"""R3-2 지식·출처·사례 JSON에서 조회용 MD·설명도를 생성. 정본·분류·승인은 변경하지 않음."""
from pathlib import Path
import json,hashlib,shutil,html
BASE=Path(__file__).resolve().parents[1]
def read(rel):return json.loads((BASE/rel).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(rel,value):
    p=(BASE/rel).resolve()
    if not p.is_relative_to(BASE.resolve()):raise ValueError('Phase 00 밖 출력')
    raw=(value.rstrip()+'\n').encode('utf-8')
    if p.exists() and p.read_bytes()==raw:return
    if p.exists():
        q=BASE/'backup/R3_레이아웃조회재생성'/rel;q=q.with_name(q.stem+'_'+sha(p)[:10]+q.suffix);q.parent.mkdir(parents=True,exist_ok=True)
        if not q.exists():shutil.copy2(p,q)
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
def views(k,l,c,e):
    src={r['id']:r for r in l['sources']}
    main={r['id']:r for r in read('05_출처와검토/출처목록.json')['sources']}
    def source_links(ids):
        out=[]
        for id in ids:
            s=src.get(id,main.get(id));out.append(f"[{s['title']}]({s['url']})" if s.get('url') else s['title']+' (로컬 원문)')
        return ', '.join(out)
    card_lines=['# 레이아웃별 선택 조건과 반례','','기존14개 ID·정의를 유지했다. 선택 조건·예·반례는 프로젝트가 작성한 설명용 지식이다. 실제 회사 영상·국제표준 분류·검증된 성과가 아니다.','',f"심화지식 v{k['version']} / SHA256 `{sha(BASE/'02_원칙과레이아웃/레이아웃_심화지식.json')}`."]
    labels=[('fit_when','선택 조건'),('reading_order','읽는 순서 후보'),('composition_decisions','구성할 때 판단'),('positive_example','적용 예'),('counterexample','오용 반례'),('acceptable_variation','허용되는 변형·복합'),('alternative_when','다른 구조를 검토할 때'),('korean_text_adjustment','한국어·문구 조정'),('landscape_adjustment','가로 화면'),('portrait_adjustment','세로 화면'),('square_adjustment','정사각 화면'),('temporal_conditions','시간·가림 조건'),('abstain_when','기권 조건')]
    for x in k['layout_cards']:
        card_lines+=['',f"## {x['name_ko']} · {x['term_id']}",'',x['definition']+' — 기존 프로젝트 정의.','',f"관련 정보 관계 후보: {', '.join(x['fit_relation_ids']) or '입력 관계에 따라 달라짐'} · 모양만으로 자동 부여하지 않음."]
        card_lines+=['']+[f"- {label}: {x[field]}" for field,label in labels]
        card_lines+=['', '적용 참고: '+source_links(x['source_refs'])+'. 기존 명칭의 정의 출처는 프로젝트 사전이며 외부 지침이 이14개 명칭을 표준화했다는 뜻은 아니다.']
    sc=['# 화면 설계 기준의 적용 예와 반례','','8개 기준은 프로젝트의 검토 관점이다. 회사 의무 규칙이나 점수표가 아니다. 관측한 원문은 보존하고 표기 정리 제안은 별도로 남긴다.']
    for x in k['screen_cards']:
        sc+=['',f"## {x['name_ko']} · {x['id']}",'',x['project_interpretation'],'',f"- 적용 예: {x['positive_example']}",f"- 반례: {x['counterexample']}",f"- 기권: {x['abstain_when']}",'','참고: '+source_links(x['source_refs'])]
    stress=['# 실제 문구·화면비·가림을 넣어 보는 설명용 사례','','아래12개는 가상 입력·조건을 이용한 설계 판단 사례다. 실제 시청자 검증·회사 영상 분석 결과가 아니다. 숫자는 예시이며 회사 기본값이나 실측 데이터로 쓰지 않는다.']
    for x in c['cases']:
        stress+=['',f"## {x['id']} · {x['name_ko']}",'',f"입력: {x['input_description']}",'',f"- 검토 후보: {', '.join(x['layout_refs'])}",f"- 판단: {x['project_decision']}",f"- 반례: {x['counterexample']}",f"- 기권: {x['abstain_when']}"]
    extra=['# 14개 밖의 레이아웃 지원 지식 후보','','사용자 A 선택으로 표·순환·조건 분기를 별도 후보로 정리했다. candidate_id는 R2 분류ID가 아니다. 기존 정의를 실제로 만족하는 범위만 기존ID에 연결하고, 맞지 않으면 후보/미분류를 유지한다.']
    for x in e['candidates']:
        extra+=['',f"## {x['name_ko']} · {x['candidate_id']}",'']+[f"- {label}: {x[field]}" for field,label in [('fit_when','선택 조건'),('reading_order','읽는 순서'),('composition_decisions','설계 판단'),('positive_example','적용 예'),('counterexample','반례'),('alternative_when','대안'),('existing_id_connection_rule','기존ID 연결 조건'),('unclassified_policy','미분류 처리'),('abstain_when','기권')]]
    research=['# R3-2 레이아웃 조사 범위','','공개 자료12개와 로컬 참고파일3개를 아래 명시 절 범위에서 확인했다. 전수 학술 조사·본문 전체 완독·스킬 심층 검토·실영상 효과 검증이 아니다.','', '| 출처 | 읽은 절·깊이 | 한계 |','|---|---|---|']
    for s in l['sources']:
        link=f"[{s['title']}]({s['url']})" if s.get('url') else s['title']+' (로컬 파일)'
        research.append(f"| {link} | {s['read_depth']} / {'; '.join(s['sections'])} | {'; '.join(s['limits'])} |")
    research+=['','R3-1에서 확인한 Cambridge 정보 관련성·일시 정보 Summary 두 개를 재사용했다. 이번에 학술 장 전체를 새로 읽은 것으로 계산하지 않는다.','', 'W3C KLREQ는2026-03-21 Group Note Draft다. 영상 글자 수·행간·최소px 표준으로 표시하지 않는다. Adobe 안전영역은 편집 도구의 조정 가능한 가이드이며 각 변 여백·서비스 UI 크기를 추정하는 근거로 쓰지 않는다.','', 'Impeccable의2개 참조와shot-composition의entrypoint는 텍스트 대조만 했다. 호출 참조·코드·의존성·라이선스·실행 성능은R3-3에서 별도 검토한다. detector·설치·외부 통신·Computer Use를 실행하지 않았다.']
    return {'02_원칙과레이아웃/07_레이아웃별_선택조건과반례.md':'\n'.join(card_lines),'02_원칙과레이아웃/08_화면설계_적용기준과반례.md':'\n'.join(sc),'02_원칙과레이아웃/09_문구와화면비_검토사례.md':'\n'.join(stress),'02_원칙과레이아웃/10_확장레이아웃_후보와반례.md':'\n'.join(extra),'05_출처와검토/R3_레이아웃_조사범위.md':'\n'.join(research)}
def svg(kind,bad=False):
    out=['<svg viewBox="0 0 400 225" role="img" xmlns="http://www.w3.org/2000/svg"><title>'+html.escape(kind+(' 오용 반례' if bad else '구조 예'))+'</title><rect x="1" y="1" width="398" height="223" fill="#f8fafb" stroke="#c8d0d6"/>']
    def text(x,y,s,size=14):out.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="#23323e" font-family="Malgun Gothic, sans-serif">{html.escape(s)}</text>')
    def box(x,y,w,h,s,fill='#e4ebef'):out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="#758894"/>');text(x+8,y+25,s)
    def line(x,y,a,b,label=''):
        out.append(f'<path d="M{x} {y} L{a} {b}" fill="none" stroke="#637d8d" stroke-width="2"/>')
        if label:text((x+a)/2,(y+b)/2-5,label,11)
    text(18,28,kind,16)
    if kind=='단일 초점':
        box(35,60,330 if not bad else 150,120,'핵심 요점' if not bad else 'A만 크게')
        if bad:box(260,165,90,33,'비교 B')
    elif kind=='분할 비교':
        box(25,50,170,135,'공법 A');box(205,50,170,135,'공법 B')
        text(40,105,'비용 80');text(220,105,'비용 100' if not bad else '내구성 우수');text(40,140,'공기 12');text(220,140,'공기 9' if not bad else '가격 미제공')
    elif kind=='전후 대응':
        box(25,55,160,130,'처리 전 · 부위 X');box(215,55,160,130,'처리 후 · 부위 X' if not bad else '다른 현장 Y');line(185,120,215,120)
    elif kind=='선형 프로세스':
        for i,s in enumerate(['접수','검토','승인']):box(20+i*130,88,95,65,s)
        line(115,120,150,120);line(245,120,280,120)
        text(28,195,'순서가 확인된 절차' if not bad else '보완 분기를 숨긴 직선화')
    elif kind=='시간축':
        line(40,120,360,120)
        for x,s in [(40,'2020'),(104 if not bad else 200,'2021'),(360,'2025')]:line(x,112,x,132);text(x-18,157,s,12)
        text(26,194,'비례 시간축 · 간격 차이' if not bad else '같은 간격인데 비례축으로 주장')
    elif kind=='계층 구성':
        box(143,48,115,52,'부서' if not bad else '한맥기술')
        for x,s in [(30,'팀 A' if not bad else '가족사 A'),(265,'팀 B' if not bad else '가족사 B')]:box(x,145,110,48,s);line(200,100,x+55,145)
        text(25,220,'상하 관계 근거 있음' if not bad else '회사명만으로 종속 관계 생성',11)
    elif kind=='연결 구성':
        for x,y,s in [(25,65,'침투수'),(170,125,'압력'),(280,50,'배수')]:box(x,y,90,45,s)
        line(115,90,170,146,'관계');line(260,146,320,95,'흐름')
        text(23,202,'관계 이름·방향 확인' if not bad else '선만 보고 인과 증명으로 기록')
    elif kind=='전체와 상세':
        box(20,55,150,135,'전체 · 부위 X');box(220,55,160,135,'같은 부위 X' if not bad else '다른 부위 Y');line(160,135,220,115,'선택')
    elif kind=='공간과 설명 표식':
        box(25,60,220,130,'시설 도면');box(275,65,95,43,'시설 X');line(170,117,275,86,'X' if not bad else 'Y에 연결');box(275,148,95,43,'시설 Y');line(120,165,275,170)
    elif kind=='데이터 시각화':
        lower=98 if bad else 0;upper=100;top=82;bottom=182
        def value_y(v):return bottom-(v-lower)/(upper-lower)*(bottom-top)
        line(65,top,65,bottom);line(65,bottom,355,bottom);line(61,top,69,top);text(30,bottom+4,str(lower));text(17,top+4,str(upper))
        box(105,value_y(98),80,bottom-value_y(98),'98' if not bad else '')
        if bad:text(115,170,'98')
        box(245,value_y(100),80,bottom-value_y(100),'100');text(130,203,'A');text(270,203,'B')
        text(150,49,'가상 데이터 · 같은 단위',11)
    elif kind=='실제 UI와 설명':
        box(25,60,235,135,'출처 확인된 UI');box(170,125,70,40,'저장');box(290,85,90,55,'외부 주석');line(238,145,290,115)
        if bad:text(45,193,'없는 기능을 실제 UI로 합성',12)
    elif kind=='카드 그룹':
        for x,s in [(20,'사업 A'),(150,'사업 B'),(280,'사업 C')]:box(x,60,100,120,s)
        text(22,209,'동등 항목·같은 정보 역할' if not bad else '원인·결과를 관계 없이 분리',12)
    elif kind=='분할 구성':
        box(20,60,235,130,'단면도');box(280,60,100,130,'대응 설명' if not bad else '무관한 소개');line(200,130,280,130)
    elif kind=='화면 속 화면':
        box(20,50,360,150,'주 화면 · 제품 시연');box(240,140,105,35,'저장 버튼');box(255,65 if not bad else 130,105,55,'발표자 창');text(35,190,'하단 자막',12)
    out.append('</svg>');return ''.join(out)
def html_view(k):
    items=[]
    for c in k['layout_cards']:
        items.append('<article id="'+html.escape(c['term_id'])+'"><h2>'+html.escape(c['name_ko'])+'</h2><p>'+html.escape(c['fit_when'])+'</p><div class="pair"><figure><figcaption>구조 예</figcaption>'+svg(c['name_ko'])+'</figure><figure><figcaption>오용 반례</figcaption>'+svg(c['name_ko'],True)+'</figure></div><div class="notes"><p><b>적용</b> '+html.escape(c['positive_example'])+'</p><p><b>반례</b> '+html.escape(c['counterexample'])+'</p></div></article>')
    return '''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>레이아웃 선택과 반례 — 설명도</title><style>
*{box-sizing:border-box}body{margin:0;background:#eef2f4;color:#23323e;font-family:'Malgun Gothic',sans-serif;line-height:1.6}main{max-width:1160px;margin:auto;padding:36px 28px}h1{font-size:30px;line-height:1.35}h2{font-size:22px;margin:0}article{background:white;border:1px solid #d6dfe4;padding:24px;margin:24px 0;break-inside:avoid}article>p{margin:6px 0 18px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;min-width:0}figcaption{font-size:13px;margin:0 0 7px;font-weight:700}svg{display:block;width:100%;height:auto}.notes{display:grid;grid-template-columns:1fr 1fr;gap:20px;font-size:14px}.muted{color:#536572}a{color:#1d536a}nav{display:flex;flex-wrap:wrap;gap:9px;font-size:13px}@media(max-width:680px){main{padding:20px 16px}.pair,.notes{grid-template-columns:1fr}.formats{grid-template-columns:1fr!important}.formats>div{max-width:400px}article{padding:16px}}@media print{body{background:white}article{border-color:#aaa}}
</style><main><p class="muted">R3-2 · 프로젝트 설명용 구조도</p><h1>정보에 맞는 레이아웃을 고르는 예</h1><p>각 그림은 구조와 오용을 설명하기 위한 간략도입니다. 실제 회사 영상·실측 자료·최종 템플릿이 아닙니다. 그림의 크기와 색은 회사 규칙으로 사용하지 않습니다.</p><p>읽는 순서: 정보 관계 확인 → 후보·대안 비교 → 문구·단위·가림 확인 → 실제 출력·유지 시간 검수.</p><nav>'''+''.join('<a href="#'+c['term_id']+'">'+html.escape(c['name_ko'])+'</a>' for c in k['layout_cards'])+'</nav>'+''.join(items)+comparison_formats()+'</main></html>'
def comparison_formats():
    def one(w,h):
        # 동일 항목·가상 값의 대응을 보존하는 구조 예. 실제 영상용 픽셀·읽기 시간 규칙이 아니다.
        rows=[('비용','80','100'),('공기','12','9')]
        parts=[f'<svg viewBox="0 0 {w} {h}" role="img"><title>같은 비교 정보의 {w}:{h} 재배치 예</title><rect width="{w}" height="{h}" fill="#f8fafb" stroke="#758894"/>']
        def t(x,y,s,size=14):parts.append(f'<text x="{x}" y="{y}" font-family="Malgun Gothic,sans-serif" font-size="{size}" fill="#23323e">{html.escape(s)}</text>')
        t(15,30,'가상 비교 · 단위/조건은 예시',13)
        if h>w:
            for i,(name,vals) in enumerate([('A',['80','12']),('B',['100','9'])]):
                y=65+i*150;t(15,y,'공법 '+name,18)
                for j,(lab,a,b) in enumerate(rows):t(20,y+38+j*35,lab+' '+vals[j])
        else:
            t(105,70,'공법 A',18);t(w-105,70,'공법 B',18)
            for i,(lab,a,b) in enumerate(rows):y=115+i*45;t(15,y,lab);t(130,y,a);t(w-100,y,b)
        parts.append('</svg>');return ''.join(parts)
    return '<article id="formats"><h2>같은 정보의 화면비별 구조 후보</h2><p>LS-04: A 비용80·공기12, B 비용100·공기9. 숫자는 가상 예이며 실제 단위·비교 조건 확인 전입니다. 재배치해도 대상·항목·값의 대응은 유지합니다.</p><div class="formats" style="display:grid;grid-template-columns:1.4fr .7fr 1fr;gap:20px;align-items:start"><div>'+one(400,225)+'</div><div>'+one(225,400)+'</div><div>'+one(300,300)+'</div></div><p>이 그림만으로 작은 화면의 가독성·안전영역·노출 시간이 검증되지는 않습니다. 실제 문구·글꼴·배포 UI와 유지 구간으로 다시 확인합니다.</p></article>'
def main():
    k=read('02_원칙과레이아웃/레이아웃_심화지식.json');l=read('05_출처와검토/R3_레이아웃_조사기록.json');c=read('02_원칙과레이아웃/레이아웃_문구와화면비사례.json');e=read('02_원칙과레이아웃/레이아웃_확장후보.json')
    for path,value in views(k,l,c,e).items():write(path,value)
    write('02_원칙과레이아웃/11_레이아웃_설명도.html',html_view(k))
if __name__=='__main__':main()
