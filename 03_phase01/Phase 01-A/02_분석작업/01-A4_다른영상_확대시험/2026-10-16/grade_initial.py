from pathlib import Path
import json,datetime
from prepare import write
B=Path(__file__).resolve().parent
W=B/'company-video-grammar-analyzer-workspace'
criteria=json.loads((B/'root-audit/criteria-frozen.json').read_text(encoding='utf-8'))['criteria']
notes={
'V01': ['scene/crane: 배경과 함께 확대, 독립 장비 운동 미확정','title/subtitle: 배너 펼침·되돌림과 문구 순서. with는 외곽 얇은 테두리의 별도 진행도 기록','water: 시점별 수면 변화','DOC063 slide2와 부분 대응, 0–8초 검사창 명시','근거 부족한 곡선/카메라 구현 유보'],
'V02': ['radius: 반경 면·선과 R9.7m 등장','table: 45m열→9.7행→JIS69,000셀 분리','rating: 화살표/정격하중/69ton 등장, 카운트업 단정 없음','DOC063 slide9 85–100초와 actual130–138초 불일치','with는 반경·행 강조의 감속, baseline은 곡선 유보; 안전성 진위 판단 없음'],
'V03': ['copy: with는 첫 행→둘째 행의 하향 교체를 보강98.95/99.05/99.15에서 확인','app: 원·호·십자·속성패널·사선 등장','copy/app: 본문·불릿 순차, 외곽 고정/내부 전환 분리','DOC066 slide12–14와 시간차 기록','실제 입력 행위/정확 곡선 유보'],
'V04': ['tabs: 01→02 활성화 전환 기록. frozen 기준의 지정필터는 작성자 오기이며 화면은 사용자 지정폴더','edit: 선택범위/손·화살표/썸네일 기록','popup: 확대·이동과 뒤쪽 선택행 추가 분리','tabs: 설명 교체와 초록 문구 소멸 기록','with는 팝업 폭의 감속, baseline은 유보; 실제 드래그/토글 단정 없음'],
'V05': ['heading/en/body/G/UI 순서','영문 면/점선/커서 등장과 수축·잔존','G와 보조 원호/십자 분리','좌·우 UI 등장과 설명, 광점','배경 UI 비교, 문서없음·오디오 미검수, 과장 없는 속성별 유보'],
'V06S': ['scene: 시점·주야 전환과 새 배경','target/cards: 가로 제목→안전→품질→공기→효율','카드 내부 그래픽과 종료부 사진 소실/아이콘 잔존','variant-comparison: W 세로판 재배치','파일별 앵커/한계, 한 그룹 변형 비교'],
'V06W': ['scene: 주간/야경 병치와 우측 시점 변화','target/cards: 세로 제목→네 가치 순서','카드 내부 그래픽/빛 변화','variant-comparison: 같은 상태 앵커, 일정 지연 일반화 안함','7680x2160 raster와 창 끝 제한, 곡선 유보']}
failures={('V01','without_skill',1):'배너 색·크기와 문구는 기록했으나 배너 밖 얇은 외곽선이 따로 그려지는 동작은 누락. root V01 1.2/1.6/2/2.4 ROI와 대조.',('V03','without_skill',0):'전체 문구의 교체·혼재만 기록; 상·하 행 순서와 하향 리빌은 미해결로 남김. 보강 시점 확인한 with보다 덜 구체적.',('V05','with_skill',1):'1.4–3.2초 사건에서 확장 뒤 소실로 축약; 2.8초 좌변 수축·옅은 I 잔존 누락. root V05-2.8.png.',('V05','without_skill',1):'영문 녹색 면/연해짐만 기록. 영문 점선 사각형·십자와 수축 동작 누락.',('V06S','without_skill',2):'사진 퇴장/아이콘 잔존은 기록. 내부 통신선·스캔 비교·회의실 표식의 개별 진행은 검사 결과가 부족하여 복합 기준 미충족.',('V06W','without_skill',2):'일반적인 발광/통신 장식과 구성 묶음만 기록. 카드 내부의 별도 변화는 미해결로 남음.'}
caption_text='[추가 발견 기준] 후반 자막 전환의 바로 직전 문구가 4대 핵심가치임을 해당 시각에 연결하며 초기 경관 자막과 혼합하지 않음'
for idx,(cid,cr) in enumerate(criteria.items(),1):
 prompt=f"{cid}: case-plan.json 지정 구간의 화면 구성·문구·정보 관계·모션(이동 방향·등장 순서·가감속, 주변/내부 동작)을 원본 근거와 연결해 분석하고 누락·오분석을 검토한다. 해당 문서가 있으면 영상과 대조하고, V06S/W는 동일 장면 상태 기준으로 변형을 비교한다. AE 키프레임은 제공되지 않는다."
 meta={'eval_id':idx,'eval_name':cid,'prompt':prompt,'prompt_record_kind':'normalized task summary; original dispatch retained in conversation','assertions':cr,'criteria_origin':'root-audit/criteria-frozen.json; human gold 아님'}
 write(W/f'iteration-1/eval-{cid}/eval_metadata.json',meta)
 for mode in ['with_skill','without_skill']:
  folder=W/f'iteration-1/eval-{cid}/{mode}'
  exp=[{'text':c,'passed':(cid,mode,i) not in failures,'evidence':failures.get((cid,mode,i),notes[cid][i])+'; outputs/observations.json 및 원본 ROI 대조'} for i,c in enumerate(cr)]
  if cid in ['V06S','V06W']:
   exp.append({'text':caption_text,'passed':mode=='without_skill','evidence':('subtitle 사건은 경관 문장→프레임워크로 잘못 연결. ' if mode=='with_skill' else 'caption 사건은 핵심가치→프레임워크로 정확히 연결. ')+('S244/244.5' if cid=='V06S' else 'W249/249.5')+' 원본 native 자막 ROI와 대조','post_hoc':True})
  passed=sum(x['passed'] for x in exp)
  write(folder/'grading.json',{'grader':'root inline AI visual review','human_approved':False,'expectations':exp,'summary':{'passed':passed,'failed':len(exp)-passed,'total':len(exp),'pass_rate':passed/len(exp)},'interpretation':'이 기준에 한정된 진단. 일반 정확도·독립표본 합격률 아님. JSON/카탈로그 통과와 내용판정 별개.','eval_feedback':{'overall':'자막 전환 기준은 최초 동결 목록에 없던 실제 오류로 양쪽 결과에 동일하게 사후 추가. V04 기준의 필터 오기는 폴더로 해석. 세밀한 이징 유보는 근거가 부족하면 실패로 강제하지 않음.'}})
  write(folder/'timing.json',{'total_tokens':None,'duration_ms':None,'total_duration_seconds':None,'reason':'subagent host telemetry not exposed; no estimates'})
write(B/'root-audit/initial-grading-summary.json',{'type':'diagnostic-only','initial_runs':14,'frozen_checks_per_mode':35,'post_hoc_caption_checks_per_mode':2,'issues':[{'id':'A4-C01','case':'V05','kind':'exit motion omission','affected':'with_skill and without_skill','retest':'iteration-2/eval-V05'},{'id':'A4-C02','case':['V06S','V06W'],'kind':'wrong prior subtitle state','affected':'with_skill; baseline correct','retest':'iteration-2/eval-V06S and V06W'},{'id':'A4-T01','kind':'validator accepted cross-source/wrong-time fixtures','scope':'helper gap, not an observed agent provenance error','fix':'catalog join and pixel-exact crop validation'}],'quantitative_general_accuracy':None})
print('14 initial run grades saved; no general accuracy claim')
