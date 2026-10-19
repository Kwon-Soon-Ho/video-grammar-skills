// JSON 정본 검증 및 파생 표시 생성. 외부 패키지/네트워크 불필요.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const dir = __dirname;
const raw = fs.readFileSync(path.join(dir,'한맥디자인정본.json'),'utf8').replace(/^\uFEFF/,'');
const d = JSON.parse(raw);
const write = (name,text) => fs.writeFileSync(path.join(dir,name),text.trim()+'\n','utf8');
const table = (heads,rows) => '\n| '+heads.join(' | ')+' |\n| '+heads.map(()=>'---').join(' | ')+' |\n'+rows.map(row=>'| '+row.map(x=>String(x ?? '미정').replace(/\|/g,'/').replace(/\n/g,' ')).join(' | ')+' |').join('\n')+'\n';
const sources = new Set(d.sources.map(x=>x.id));
const all = [...d.color_tokens,...d.gradients,...d.references,...d.rules,...d.issues];
assert.equal(new Set(all.map(x=>x.id)).size,all.length,'중복 ID');
assert.equal(d.source_selection.brand_scales,'SB-COLOR');
assert.equal(d.source_selection.accent_and_neutral,'VC');
assert.equal(d.source_selection.ui_mandatory,false);
for(const x of all) {
  for(const ref of [...(x.source_refs||[]),...(x.source_ref?[x.source_ref]:[])]) assert(sources.has(ref),ref);
}
for(const t of d.color_tokens) {
  assert(sources.has(t.selected_source));
  assert(t.observations.some(o=>o.source_ref===t.selected_source),'선택 출처 관측 없음');
  if(t.type==='color') {
    assert.match(t.value,/^#[0-9A-F]{6}$/);
    assert.equal(t.value,t.observations.find(o=>o.source_ref===t.selected_source).value,'선택값 불일치');
  } else {
    assert.equal(t.scope,'optional_color_utility');
    assert(t.value.alpha>=0 && t.value.alpha<=1);
    assert(t.value.rgb.every(v=>Number.isInteger(v)&&v>=0&&v<=255));
  }
}
assert.equal(d.color_tokens.filter(x=>x.scope==='global_color_library').length,30);
assert.equal(d.color_tokens.filter(x=>x.different_between_sources).length,6);
assert.equal(d.gradients.length,18);
assert(d.gradients.every(x=>x.requirement==='reference_only'));
assert(d.references.every(x=>x.requirement==='reference_only'));
const tokens = new Map(d.color_tokens.map(t=>[t.id,t]));
for(const x of d.semantic_roles) assert(tokens.has(x.token_id));
for(const id of Object.values(d.db_contract.scene_contract.palette_role_bindings)) assert(tokens.has(id));
const color = id => {
  const t = tokens.get(id);
  if(t.type==='color') return t.value;
  assert.equal(t.value.alpha,1,'단색 대비에는 불투명 색만 허용');
  return '#'+t.value.rgb.map(x=>x.toString(16).padStart(2,'0')).join('').toUpperCase();
};
const luminance = hex => {
  const c = hex.slice(1).match(/../g).map(x=>parseInt(x,16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);
  return c[0]*.2126+c[1]*.7152+c[2]*.0722;
};
const ratio = (a,b) => {
  const ls=[luminance(a),luminance(b)].sort((a,b)=>b-a);
  return (ls[0]+.05)/(ls[1]+.05);
};
assert.equal(ratio('#000000','#FFFFFF'),21);
assert.equal(ratio('#123328','#123328'),1);
const pairs = [
['Green 主文字','HM-COLOR-NEUTRAL-GREEN-100','HM-COLOR-GREEN-500'],
['Green 補助文字','HM-COLOR-NEUTRAL-GREEN-200','HM-COLOR-GREEN-500'],
['Brown 主文字','HM-COLOR-NEUTRAL-BROWN-100','HM-COLOR-BROWN-500'],
['Brown 補助文字','HM-COLOR-NEUTRAL-BROWN-200','HM-COLOR-BROWN-500'],
['Yellow 강조 / Green','HM-COLOR-YELLOW','HM-COLOR-GREEN-500'],
['강조 Orange / Green','HM-COLOR-ACCENT-ORANGE','HM-COLOR-GREEN-500'],
['강조 Orange / Brown','HM-COLOR-ACCENT-ORANGE','HM-COLOR-BROWN-500'],
['주 중립색 / 기본 Orange','HM-COLOR-NEUTRAL-BROWN-100','HM-COLOR-ORANGE-500'],
['주 중립색 / 강조 Orange','HM-COLOR-NEUTRAL-BROWN-100','HM-COLOR-ACCENT-ORANGE'],
['Yellow / 밝은 중립색','HM-COLOR-YELLOW','HM-COLOR-NEUTRAL-BROWN-100'],
['검정 / 기본 Orange','HM-COLOR-BLACK-800','HM-COLOR-ORANGE-500'],
['검정 / 강조 Orange','HM-COLOR-BLACK-800','HM-COLOR-ACCENT-ORANGE'],
['검정 / Yellow','HM-COLOR-BLACK-800','HM-COLOR-YELLOW']
];
const contrast = pairs.map(([name,fg,bg])=>({name:name.replace('主文字','주 텍스트').replace('補助文字','보조 텍스트'),foreground:fg,background:bg,foreground_hex:color(fg),background_hex:color(bg),ratio:ratio(color(fg),color(bg)),meets_4_5:ratio(color(fg),color(bg))>=4.5,meets_3:ratio(color(fg),color(bg))>=3}));
write('색상대비검토.json',JSON.stringify({derived_from:d.profile_id+'@'+d.version,method:'W3C sRGB relative luminance; opaque solid colors only',rounding:'판정은 반올림 전 숫자로 수행',limitation:'최종 영상/그라데이션/알파합성/시간적 가독성의 통과 선언 아님',pairs:contrast},null,2));

let md = '# 한맥 영상용 컬러 정리\n\nJSON 정본에서 생성: '+d.profile_id+'@'+d.version+' · '+d.retrieved_on+'\n\n브랜드 3색·명암 스케일은 Storybook, 강조색·중립색은 Vercel을 사용한다. 사용자 지정 출처 선택을 반영했다. 전역으로 조회할 수 있는 컬러 라이브러리이며 매 장면의 색 사용량·배치·비율을 강제하지 않는다.\n\n## 브랜드 3색과 명암 스케일\n\n100~800은 우리 DB의 정규화 단계명이다. Storybook 원래 명칭 Light 4~Dark 3을 함께 보존한다. CSS 이름도 영상 시스템 어댑터 이름이며 Storybook이 같은 이름을 정의했다고 주장하지 않는다.\n';
md += table(['단계','Storybook 원래 명칭','Green','Brown','Orange'],Array.from({length:8},(_,i)=>[(i+1)*100,d.color_tokens[i].source_name,...['GREEN','BROWN','ORANGE'].map(f=>color('HM-COLOR-'+f+'-'+(i+1)*100))]));
md += '\n기본색은 Green #123328, Brown #3E3523, Orange #CC5200. 브랜드 설명은 자연·토양의 안정·기술의 성장·새 시작을 연결한다. 이 설명에서 상하 분할 구도·자연 사진·특정 모션을 필수로 도출하지 않는다.\n\n## 강조색·중립색\n';
md += table(['토큰','값','역할','출처'],d.color_tokens.filter(x=>x.selected_source==='VC'&&x.type==='color').map(x=>[x.source_name,x.value,x.role,'Vercel / 사용자 선택']));
md += '\n## 역할로 조회하기\n';
md += table(['역할','토큰 ID','값'],d.semantic_roles.map(x=>[x.role,x.token_id,color(x.token_id)]));
md += '\n텍스트 역할은 해당 어두운 기본 배경을 쓸 때의 후보다. 라이트 배경·사진·밝은 그라데이션 위에 같은 밝은 텍스트를 자동 재사용하지 않는다. 차트의 범주·성공/실패를 브랜드색과 임의 대응시키지 않는다.\n\n## 흑백 알파 유틸리티\n\nVercel 관측 참고값이다. 선택한 브랜드·강조·중립 30색과 별도 로딩한다. Black/White 각각 100~800은 5%, 10%, 25%, 40%, 55%, 70%, 85%, 100% 알파다. 흰색 500은 불투명 흰색이 아니며, 색 알파를 전체 레이어 opacity로 바꾸지 않는다.\n\n## 계산한 색 대비\n\n불투명 sRGB 단색 두 개로만 계산했다. 4.5:1은 일반 텍스트의 참고 문턱, 3:1은 WCAG의 큰 텍스트 기준에 해당한다. 영상의 화면 픽셀 크기만으로 큰 텍스트 여부를 판정하지 않는다. 최종 해상도·시청 크기·최악 배경·그라데이션·압축·움직임을 따로 확인한다. 원색을 자동 변경해서 통과시키지 않는다.\n';
md += table(['전경 / 배경','색 조합','비율','≥4.5','≥3'],contrast.map(x=>[x.name,x.foreground_hex+' / '+x.background_hex,x.ratio.toFixed(2)+':1',x.meets_4_5?'충족':'미달',x.meets_3?'충족':'미달']));
md += '\n특히 강조 Orange·Yellow 위에 밝은 텍스트를 놓는 조합은 표를 확인한다. 필요하면 어두운 중립 텍스트·명확한 배경판·레이아웃 변경을 선택하고 실제 합성 프레임에서 재검토한다.\n\n## 전환·합성 적용 범위\n\nVercel의 Green↔Brown Neutral 경유는 원문 규칙으로 보존하되, 영상 컷·디졸브 전체의 의무로 확장하지 않는다. transparent/rgba 금지는 브랜드 표면 레시피의 참고 제약이며 페이드·마스크·알파 출력의 금지가 아니다.\n\n출처: [Storybook Color](https://design.hmac.kr/?path=/story/foundation-color--all), [Vercel 컬러·Variables](https://hanmac-designsystem.vercel.app/claude_app/index.html), [W3C 대비 기준](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [색만으로 구분하지 않기](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html).\n';
write('01_컬러.md',md);

md = '# 한맥 영상용 타이포그래피·간격 참고\n\nJSON 정본에서 생성. 이 문서의 디지털 제품 수치를 영상 필수 규격으로 사용하지 않는다.\n\n## 서체와 위계\n\n양쪽에서 Noto Sans KR을 확인했다. 기본 후보로 참고하고, Storybook fallback인 맑은 고딕·시스템 sans-serif를 기록한다. 영상 폰트 설치·라이선스·제작 도구 지원은 이번 정리에 포함되지 않았다. 대체 폰트 사용 시 한글·숫자·단위·긴 기술명의 폭과 줄바꿈을 확인한다.\n\nVercel의 타입 역할:\n';
const vcType=d.references.find(x=>x.id==='HM-REF-TYPE-VC').data;
md += table(['역할','웹 크기 px','굵기','행간 배수'],vcType);
md += '\nStorybook은 위와 같은 새 공통 타입 체계를 확정하지 않고 현재 컴포넌트 구현을 제시한다:\n';
md += table(['컴포넌트','px 크기','px 행높이','굵기'],Object.entries(d.references.find(x=>x.id==='HM-REF-TYPE-SB').data).map(([k,v])=>[k,...v]));
md += '\n페이지 설명 400은 현재 계산된 굵기이며 컴포넌트 자체가 별도 weight를 지정했다는 뜻이 아니다. 역할 이름이 비슷해도 Vercel heading 30px와 Storybook page header 28px를 하나의 정답으로 합치지 않는다.\n\n## 간격·레이아웃\n\nVercel 단계:\n';
md += table(['이름','웹 px'],Object.entries(d.references.find(x=>x.id==='HM-REF-SPACE-VC').data));
md += '\nStorybook은 전역 spacing scale/grid가 정의되어 있지 않다고 표시한다. Dashboard 외곽 34px/모바일 20px, 섹션 간 24px, 카드 내부 24px, Page Header 아래 20px, GNB 연결 12px, LNB 연결 18px는 개별 구현 참고다. 같은 수치를 공통 토큰 하나로 합치지 않는다.\n\nDesktop ≥1024px / Mobile ≤1023px는 웹 탐색 구조 경계다. 1280×900·390×844는 QA viewport이며 영상 해상도·세이프존이 아니다.\n\n## 영상에서 결정할 것\n\n1. 핵심 제목·주 설명·보조 주석을 정보 역할로 나눈다.\n2. 화면 비율·최종 표시 크기·요소 수·문구 길이에 맞춰 글자 크기와 여백을 설계한다.\n3. 긴 한국어 사업명, 괄호, 숫자와 단위가 잘리거나 의미가 갈라지지 않는지 본다.\n4. 정보가 완성된 후 읽을 시간을 확보하고 내레이션·이동·줌과 겹쳐 읽기 어려운 구간을 확인한다.\n5. 영상 크기·행간·자막 규격·세이프존·타이밍은 현재 미정으로 둔다. 웹 px를 임의 배율로 확대해 회사 표준으로 등록하지 않는다.\n\n출처: [Storybook Typography](https://design.hmac.kr/?path=/story/foundation-typography--all), [Storybook Layout](https://design.hmac.kr/?path=/story/foundation-layout--all), [Vercel 타입·간격](https://hanmac-designsystem.vercel.app/claude_app/index.html).\n';
write('02_타이포그래피와_간격.md',md);

md='# 한맥 표면·UI 참고 카탈로그\n\nJSON 정본에서 생성. 모든 항목은 reference_only다. 선택하지 않아도 검수 실패가 아니다. 영상 기획의 기본 검색에서는 이 카탈로그를 불러오지 않고, 표면 스타일/제품 UI 설명이 필요한 경우에만 사용한다.\n\n## 그라데이션\n\nVercel에서 확인한 CSS 고유 이름 18개를 보존했다. 설명의 20개와 차이가 있으며 누락값을 만들지 않았다. 두 Z0 항목은 단색이다. 설명의 90deg와 CSS의 180deg 차이 때문에 방향을 의무화하지 않는다. CSS 각도를 AE 각도에 같은 숫자로 대입하지 않고 시작/끝 위치·스톱·보간을 실제 화면과 대조한다.\n';
md+=table(['원문 이름','관측 CSS'],d.gradients.map(x=>[x.source_name,x.value]));
md+='\n## 형태·깊이\n\nVercel 반경 단계는 none 0, xs 2, sm 4, md 6, lg 8, xl 12, 2xl 16, full 9999px다. Storybook의 control/button/input/select/container는 역할별 4px다. 같은 역할의 차이는 출처별로 유지한다. full=9999px는 캡슐/원형 의도를 구현하는 CSS 값이며 영상 도형의 실제 반경으로 복사하지 않는다.\n';
md+=table(['그림자','Vercel CSS'],Object.entries(d.references.find(x=>x.id==='HM-REF-SHADOW').data));
md+='\n그림자·그라데이션은 의미 구분과 분리가 필요할 때 선택한다. 매 장면의 입체감·금속 보더·그라데이션을 강제하지 않는다. UI hover나 z단계가 영상 속도·3D 깊이·카메라 위치를 뜻하지 않는다.\n\n## 컴포넌트의 활용과 제외\n';
md+=table(['항목','필요할 때 참고','영상 공통에서 제외'],[
['버튼·탭','실제 SW 조작 데모, 클릭 대상·선택 상태 설명','화면당 1~2개 CTA, 31/34px 높이, hover/active 색과 120ms 전환의 강제'],
['입력·체크박스·라디오·검색','제품 입력·선택·오류 상태를 설명하는 장면','44px 높이, focus border, 150ms 전환을 영상 등장 규칙으로 사용'],
['카드','독립된 병렬 항목을 묶는 후보','모든 설명을 카드로 구성, 12px radius/24px padding 의무'],
['테이블','동일 기준의 행·열 비교가 필요할 때 재구성','13px 본문/11px 헤더, dense row·hover·uppercase 규칙의 강제'],
['웹 내비게이션·오버레이','해당 제품 화면이 실제 주제일 때 원본 확인','GNB/LNB·모달·메뉴 구조를 설명 영상에 자동 삽입'],
['CENTER 제목','사업명·노선구분·사업노선 4종 조합의 정보 위계','7680×2160, 범위 한정 palette, TBD를 회사 전체 표준으로 승격'],
['조직도·시설·공간 그래픽','주제와 관계가 맞을 때 해당 Story/원본을 추가 확인','부서색·시설별 색·좌표를 브랜드 글로벌 토큰으로 자동 편입']
]);
md+='\nUI 페이지 설명과 CSS가 다를 수 있다. 예를 들어 카드 설명의 흰 배경·Brown hover와 CSS alpha white·accent Orange가 다르다. 실제 제품 재현은 캡처/현재 구현을 먼저 확인한다. 이 카탈로그는 제품 화면의 정확한 최신 재현을 보증하지 않는다.\n\nStorybook의 전체 컴포넌트 변형은 전수 조사하지 않았다. Foundation 3페이지, Title 예시, 조직도 전용 페이지의 존재·범위를 확인했으며, Vercel의 표시 메뉴는 모두 읽고 분류했다. 조직도·시설·공간의 세부 팔레트는 이번 글로벌 컬러 정본에서 제외했다.\n\n출처: [Vercel 표면·컴포넌트](https://hanmac-designsystem.vercel.app/claude_app/index.html), [Storybook Layout](https://design.hmac.kr/?path=/story/foundation-layout--all), [CENTER Title](https://design.hmac.kr/?path=/story/center-graphic-title--compositions).\n';
write('03_표면과_UI_참고.md',md);

md='# 출처 선택·차이·DB 연결\n\nJSON 정본에서 생성. 출처의 최신성은 도메인명으로 추정하지 않고 사용자 지시로 고정했다.\n\n## 채택 기준\n\n브랜드·명암 스케일은 Storybook, 강조색·중립색은 Vercel. 흑백 알파·그라데이션·UI 값은 Vercel 관측 참고이며 자동 필수 규칙이 아니다. 출처 선택 확인은 회사 영상 문법 전체 승인과 별개다.\n\n## 선택 이력을 남긴 6개 컬러\n';
md+=table(['정규화 토큰','Storybook 선택값','Vercel 보존값','현재 처리'],d.color_tokens.filter(x=>x.different_between_sources).map(x=>[x.name,x.value,x.observations.find(o=>o.source_ref==='VC').value,'Storybook 사용 / 사용자 결정']));
md+='\n## 나머지 차이와 미정\n';
md+=table(['ID / 항목','원문에서 확인한 점','처리','상태'],d.issues.filter(x=>x.id!=='HM-ISSUE-COLOR-6').map(x=>[x.id+' / '+x.title,x.evidence,x.handling,x.status]));
md+='\n## 출처 레지스트리\n';
md+=table(['ID','내용 위치','표시 버전','접근'],d.sources.map(x=>[x.id,x.url?'['+x.locator+']('+x.url+')':x.locator,x.version,x.access]));
md+='\n조회일 '+d.retrieved_on+'. 브라우저에서 렌더링된 내용을 수동 전사·정제했다. 원본 배포 커밋/전체 HTML 스냅샷 해시는 미확보다. manifest의 SHA256은 로컬 정본 무결성을 확인하며 원격 소스 전체의 해시를 뜻하지 않는다.\n\n## 기존 DB 명세로 연결\n';
md+=table(['정본 컬렉션','기존 엔터티','키','근거·검수'],d.db_contract.mapping.map(x=>[x.collection,x.entity,x.natural_key,x.evidence+' / '+x.review]));
md+='\nrequirement는 required(사용자 운영 정책), available(사용 가능 컬러), recommended(영상 해석 권고), reference_only(선택 참고)로 구분한다. 기존 required/recommended 이진 필드에 available/reference_only를 required로 변환하지 않는다. 필요하면 requirement=optional과 usage_policy를 별도 컬럼으로 두고 매핑한다.\n\nsource_selection_confirmed는 출처 선택이 확인됐다는 토큰 메타데이터다. 기존 DB의 draft/reviewed/approved 상태에 그대로 넣지 않는다. source_selection 상태를 보조 필드에 저장하고, 회사 문법 승인 Review는 해당 범위·버전·검수자가 있을 때 별도 생성한다. 이 JSON에서 reviewer=null은 미기록을 뜻한다.\n\n## 기본 로딩·기획 흐름\n';
md+=d.db_contract.query_policy.map((x,i)=>(i+1)+'. '+x).join('\n')+'\n';
md+='\n한 장면의 예시 계약:\n\n~~~json\n'+JSON.stringify(d.db_contract.scene_contract,null,2)+'\n~~~\n\n색은 값 복사 대신 token_id로 연결한다. UI가 필요한 장면만 optional_style_refs에 HM-REF-UI 등을 명시한다. 관측 분석의 원본 픽셀값과 추천 색의 차이는 그대로 남긴다.\n\n## 재생성·검증\n\nNode.js에서 이 폴더의 문서생성.cjs를 실행한다. ID 중복, 출처 참조, 사용자 선택값 일치, 역할 연결, 필수/UI 분리, 30개 전역색·16개 선택 알파·18개 표면 레시피를 확인하고 파생 문서·CSS·대비표·manifest를 생성한다. 토큰 변경은 한맥디자인정본.json에서 수행한다. 실제 영상 렌더 검증과 회사 문법 승인 검사는 후속 작업이다.\n\n현재 범위는 디자인 정제 데이터와 DB 입력 기반이다. 전체 Phase 00 운영 DB, SQL 검색 인덱스, 영상 분석 스킬을 구축 완료했다고 기록하지 않는다.\n';
write('04_출처와_DB_연결.md',md);

const fmt=t=>t.type==='color'?t.value:'rgba('+t.value.rgb.join(',')+','+t.value.alpha+')';
const css=(ts,header)=>'/* GENERATED: '+header+'; hanmac-video@'+d.version+' */\n:root {\n'+ts.map(t=>'  '+(t.adapter_css_name||t.source_name)+': '+fmt(t)+';').join('\n')+'\n}\n';
write('공통컬러.css',css(d.color_tokens.filter(x=>x.scope==='global_color_library'),'브랜드 Storybook / 강조·중립 Vercel; UI 규격 미포함').replace('\n}\n','\n  --hm-green: var(--hm-green-500);\n  --hm-brown: var(--hm-brown-500);\n  --hm-orange: var(--hm-orange-500);\n}\n'));
write('선택알파.css',css(d.color_tokens.filter(x=>x.scope==='optional_color_utility'),'Vercel 흑백 알파 선택 유틸리티'));
const files=['한맥디자인정본.json','01_컬러.md','02_타이포그래피와_간격.md','03_표면과_UI_참고.md','04_출처와_DB_연결.md','색상대비검토.json','공통컬러.css','선택알파.css','문서생성.cjs'];
write('자료목록.json',JSON.stringify({profile_id:d.profile_id,version:d.version,retrieved_on:d.retrieved_on,hash_scope:'로컬 정본/파생물. 원격 원문 전체 해시 아님.',files:files.map(name=>({path:name,sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(dir,name))).digest('hex')}))},null,2));
console.log(JSON.stringify({validated:true,global_colors:30,optional_alpha:16,source_differences_resolved:6,optional_surface_recipes:18,contrast_pairs:contrast.length,generated_files:files.length},null,2));

