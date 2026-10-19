import json
from pathlib import Path
BASE=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');OUT=Path(__file__).parent
catalog=json.loads((BASE/'05_출처와검토/R7_02_품질항목_조사기록.json').read_text(encoding='utf-8'));byid={x['id']:x for x in catalog['sources']}
rows=[
 ('WEB-CAP','Does My Media Need Captions?; Automatic Captions; Positioning','무의미한 배경음/무음과 필요한 음성정보를 구분하고 자동자막 오류/부정어 누락을 다룬다.','Q-CAP-01의 조건부 비적용과 필요한 소리 대조는 부합. 요구 미확인을 비적용으로 바꾸면 안 됨.'),
 ('WEB-KO','Status;6.6.1;7.1.1~7.1.4','Group Note Draft 2026-03-21, 한글 글자/어절 줄바꿈 선택 및 수열·첨자 등 분리 제한을 확인.','고정 글자 크기/줄수/모든어절 분리 금지로 만들지 않는 조건부 해석이 적절.'),
 ('WEB-SI','공식소개→영어PDF v4.01;5.4.1 해당 표머리글 부분,5.4.3~4 printed144~145/PDF33~34','단위 분리 공백,평면각 예외,°C,소수점/소수쉼표 문맥,0접두표기,숫자그룹 예외와 표머리글 단위 표현을 확인.','원문 전사보존/담당 검수/소수구분미상을 유지하는 예·반례와 부합. 전체SI/GUM 검토 아님.'),
 ('WEB-CONTRAST','SC/Intent,large-scale threshold,rounding,anti-aliasing','웹 텍스트 대비 기준과 예외,크기 판정 문맥,반올림 금지,실표시 한계를 확인.','Q-SCREEN-03의 계산값·가정/실영상 가독성 구분 필요. 한국어 영상px를 큰글자로 자동판정하지 않음.'),
 ('WEB-NONTEXT','Graphical Objects/essential exception/testing principles','의미이해에 필요한 부분·대체정보·필수 원형 예외와 인접색 검토 조건을 확인.','필수선/장식 구분 및 CI자동재색칠금지,본문에 로고예외전용금지와 부합. 전체WCAG평가 아님.'),
 ('WEB-FLASH','SC/Intent 특히 최대재생46,비sRGB/최고동적범위47~48,loop49; Key Terms','횟수와 면적/일반·적색 조건,최대재생·색공간/동적범위·반복경계 조건을 확인.','초안의 loop/HDR 누락을 지적했으며 보완 후보가 조건을 추가함. 실제섬광도구/인체/안전인증 없음.'),
 ('WEB-CHART','Starting at zero;Gaps in data;Breaks in axes;Time series','막대/면적의0기준 권고와 추세선의 제한범위,결측과 축압축·문서WIP 표기를 확인.','일괄0축/16px·0.5px 전용 금지 적절. 원문의 결측보간 금지와 프로젝트의 명시적 모델 추정 예외는 서로 동일한 원문명령으로 취급하지 않음.'),
 ('WEB-CHOREO','Paths;Composition/Consistency/Continuity/Sequence','원문은 Carbon UI 격자·대각선·stagger 규칙과 UI 의미/공간연속성을 다룸.','영상 기술경로/동시비교에 대각선금지·stagger를 강제하지 않는 전이 한계가 적절. 코드예제실행 없음.'),
 ('WEB-TRANSIENT','Chapter21 title/author/2021 date,Summary,pp268~274/DOI','공개 Summary에서 사라지는 정보와 계속접근 가능한 정보의 대비를 확인.','Q-MOTION-01은 고정정지/모든텍스트유지로 확대하지 않아 범위 적절. 장전문·인용실험은 읽지 않음.'),
 ('WEB-TABLE','When to use/not use;captions;headers;numbers','행열 비교,표제와머리글 의미,숫자열정렬의 HTML컴포넌트 문맥을 확인.','영상에 HTML/grid/반응형 의무로 옮기지 않고 R3후보/내용관계참고로 한정해 적절. 구현코드실행 없음.')]
records=[{'source_id':i,'url':byid[i]['url'],'independent_read_scope':loc,'primary_content_summary':s,'comparison':c,'full_text_review':False,'remote_content_hash':None,'raw_fulltext_archived':False} for i,loc,s,c in rows]
result={'stage':'R7-2 독립 공개원문 부분대조','checked_on':'2026-10-15','scope':'열람한10출처 지정부분의 대조. 작성자의15원문 전체열람/깊이를 인증하거나10실험을 수행했다는 뜻이 아님. 원문복제/재배포권한 판정 없음.','records':records,'catalog_external_count':15,'independently_checked_catalog_sources':10,'not_independently_reopened_source_ids':[r['id'] for r in catalog['sources'] if r['kind']=='external_primary_author_or_publisher' and r['id'] not in {x[0] for x in rows}],'access_notes':[{'source_id':'WEB-SI','initial_exact_URL_attempt':'web open Internal Error','recovery':'BIPM 공식 소개 페이지의 영어PDF link를 click하여 동일제목9th/v4.01 EN/102pages와해당절 확인. 실패를 단독열람완료로 바꾸지 않음.'}],'real_video_test':False,'company_authority':False}
(OUT/'R7_02_공개원문_독립대조.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
