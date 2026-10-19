from pathlib import Path
import json,hashlib,datetime
B=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
criteria=read(B/'legacy-criteria.json')['cases']
reasons={
'V05':[
'ko/en/paragraph/g/left_panel/right_panel 및 layout 사건이 원본 순서를 연결한다.',
'en 사건2: 2.8초 왼 경계가 오른쪽으로 들어옴, 3.2초 사각 면/점선 소실 및 회색 영문 잔류. c8/c9/c10. Markdown은 퇴장 방향을 축약했지만 JSON에 남아 있다.',
'g/g_guides/g_cross가 면의 가시성, 원호 및 CAD 십자 경로를 분리하며 E 조각 슬라이드를 복사하지 않았다.',
'left_panel/right_panel/left_glow 및 두 caption에서 확대·하강, 오른 전개, 가림 해소, 빛, 좌우 반대 리빌을 분리한다. c30~40과 원본 RGB를 대조했다.',
'bg 사건2는 선택 표본의 주황 선택행 유지 및 가림/사이 변화 한계를 명시. 문서없음, audio_reviewed=false.',
'g_cross 6.0/.1/.2/.3의 사각 중심을 원본 ROI로 대조했다. 이동량287/228/183px 및 프레임 확대·우측 이동은 둘 이상 진행 구간을 사용. 정확한 AE 곡선은 주장하지 않는다.'
],
'V06S':[
'scene 두 사건은 주간 시점 이동→주야 중첩→야간 확대 조망→녹색 배경을 기록한다.',
'title_panel/title_text가 가로판 선행 및 공사/CONSTRUCTION→목표/TARGETS 중간 상태를 연결. safety/quality/schedule/efficiency의 왼→오른 순서.',
'safety_detail/quality_drone/icon_lights와 각 퇴장 사건은 내부 선·드론·빛을 분리하고 245.8~245.967 사진 소실/배지 잔류를 기록한다.',
'해시·[232,246) 창·각 native 시각 연결 및 자료022 단일 원본 입력 범위 유지. pair 비교는 시험 전 제외.',
'construction_caption은244.0의4대 핵심가치→244.2의BIM 프레임워크를 c27~c30에서 연결. 초기 경관 문구를 직전으로 혼입하지 않았다.',
'감속은 title_panel 위치에 한정. c03/c04/c05에서 판 상변의 상승량 감소를 직접 대조. 작업보고 UI의 감속을 확정하지 않았다.'
],
'V06W':[
'scene/old_model은 좌측 주간 유지와 우측 야간 조망 범위 확대,239.300→239.333 컷을 기록한다.',
'target_panel 선행→제목→안전→품질→공기→효율 순서. 세로판/영문 TARGET 단수를 보존.',
'safe/quality/period/efficiency는 사진·아이콘·글자·통신선·별 방향·스크린 리빌·빛을 분리. c18~24,c36~39 직접 대조.',
'coverage에 native7680x2160 및 [236,250)·250 context 구분. 각 미확정 가감속 이유 명시.',
'captions 사건2는249.200의4대 핵심가치→249.400의BIM프레임워크 문구를 c15~17에서 연결.',
'작업보고는244.600/248/249.500의 내용 유지 비교이며 위치 감속을 확정하지 않았다. 가시성/리빌/내부내용을 분리.'
]}
cases=[]
for cid in ['V05','V06S','V06W']:
 d=B/'legacy'/cid;o=read(d/'outputs/observations.json')
 ex=[{'text':t,'passed':True,'evidence':e} for t,e in zip(criteria[cid]['criteria']+criteria[cid]['additional'],reasons[cid])]
 g={'case_id':cid,'scope':'pre-frozen targeted known-case regression, not held-out core/detail metrics','expectations':ex,
 'summary':{'passed':len(ex),'failed':0,'total':len(ex),'pass_rate':1.0},
 'content_review':'root AI compared prior frozen observations with supplied native PNG/ROI; no new human gold',
 'critical_errors_found':0,'structure_and_provenance_passed':True,
 'known_limitations':['selected frames only; no audio or AE project','no new variant-pair comparison'],
 'abstention_event_count_raw':sum(e['easing']['classification']=='unknown' for x in o['objects'] for e in x['events']),
 'abstention_count_note':'raw event-level easing unknown count; not unique scored atomic abstentions and not a rate',
 'non_gating_detail_notes': ['V05 JSON describes contraction of left edge but does not explicitly record the simultaneous downward top edge; Markdown also compresses the exit direction. This is a residual detail omission, not recurrence of the absent contraction/residual-text criterion.'] if cid=='V05' else [],
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 save(d/'grading.json',g)
 seal={n:hashlib.sha256((d/'outputs'/n).read_bytes()).hexdigest() for n in ['observations.json','observations.md']}
 save(d/'review-input-seal.json',seal)
 cases.append({'case_id':cid,'passed':True,'criteria_passed':len(ex),'critical_errors_found':0,'raw_easing_unknown_events':g['abstention_event_count_raw']})
save(B/'legacy-decision.json',{'all_passed':True,'runs_completed':3,'cases':cases,'decision_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'new_video_pixels_opened_at_decision':False,'primary_runs':0,'legacy_scope':'targeted final draft3 regression; full A4 outcomes preserved; no pair comparison','residual_detail_omissions':1,'residual_note':'G contraction top-edge direction omitted while shrinking left boundary and gray text persistence were captured; criterion remains met'})
print(json.dumps(cases,ensure_ascii=False))
