# design tokens 색 기록 지침 검토

R1의가족사CI등록에필요한값·역할분리만선별한다. 로컬design-tokens/SKILL.md전체지침과README전문을읽었다. 해당폴더에별도참조파일/실행코드는없다. 원문은backup에해시와함께보존한다. 공개소스전체의심층검토나맞춤스킬완성으로표기하지않는다.

| 원문 부분 | 판단 | R1에서의사용 |
|---|---|---|
| Color Palette Generation / Semantic Token Mapping | 제한채택 | CI원색의원문값과페이지역할을별도필드로구분 |
| Output Formats | 변형 | 출처·회사ID·CI버전·색공간·관측/제안상태를더한자체JSON으로기록 |
| HSL 50~950 shade생성·dark inversion | 제외 | 공식CI명암규칙없이새색을회사값으로만들지않음 |
| 대비미달이면한단계어둡게변경 | 제외 | CI원색을자동수정하지않고페이지조합을별도검토 |
| Type/Spacing/base4/웹breakpoint | R1미채택 | 자산등록의범위가아님. 영상수치로직접복사하지않음 |
| WCAG 수치표 | 재확인필요 | 원문의large text px표기는공식18pt/14pt bold와혼동소지가있어채택하지않음 |

공식대비문서: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
DTCG형식참고: https://www.designtokens.org/tr/2025.10/format/

DTCG 2025.10은커뮤니티그룹규격이며W3C표준으로표기하지않는다. 색값의색공간과컴포넌트표현을참고했다. 현재자체JSON의DTCG준수는시험하지않았다.

적용예: 공식가이드의RGB를원문·페이지와연결해CI값으로보존하고,페이지배경역할은별도제안으로기록한다.
반례: 로고의대표픽셀색을공식색이라고등록하거나대비를맞추려고CI색을어둡게바꾼다.
기권: 회사정체성·최신CI·원문색공간이확인되지않으면보류하며원문확인없이색을발명하지않는다.

이검토결과는기존design-tokens전역스킬을수정하거나새CI생성스킬로활성화하지않는다. 외부스킬별전체심층검토·변형·평가는R3/R8에서별도진행한다.


Adobe공식로컬예제참조: Illustrator2026/Scripting/Sample Scripts/JavaScript/MultiArtboards/SaveArtboardsAsPDF.jsx와Gradients/MakeLinearGradient.jsx. 외부복사코드는실행하지않고기록/복제용스크립트를별도로작성했다.
