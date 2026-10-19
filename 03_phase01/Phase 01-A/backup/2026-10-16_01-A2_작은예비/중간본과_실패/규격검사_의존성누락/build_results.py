from pathlib import Path
from fractions import Fraction as F
import json,hashlib,importlib.util,subprocess,sys
from prepare import OUT,ROOT,sha,write

PUB=OUT/'게시안'
P='Phase 01-A'
AN=f'{P}/02_분석작업/01-A2_작은예비'
VE=f'{P}/04_검증자료/01-A2_작은예비'
RE=f'{P}/05_결과보고/07_01-A2_작은예비분석_보고.md'
def textfile(rel,text):
    p=PUB/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def jfile(rel,data):write(PUB/rel,data)
def q(x):
    x=F(x);return {'num':x.numerator,'den':x.denominator}
def load(aid,phase):return json.loads((OUT/'cases'/aid/phase/'실행기록.json').read_text(encoding='utf-8'))
def evidence(aid,t,phase='initial'):
    run=load(aid,phase);f=next(x for x in run['frames'] if F(x['actual_playback_seconds'])==F(t))
    return {'asset_id':aid,'source_sha256':run['input_sha256'],'frame_id':f['frame_id'],'playback_seconds':f['actual_playback_seconds'],'reported_pts':f['reported_pts'],'container_cts_ticks':f['container_cts_ticks'],'time_base':f['time_base'],'ordinal':f['display_ordinal_zero_based'],'image_sha256':f['sha256'],'execution_image_path':f['path'],'archive_image_path':str(ROOT/AN/aid/phase/Path(f['path']).name)}

def main():
    inputs=json.loads((OUT/'입력고정과_컨테이너사전점검.json').read_text(encoding='utf-8'))
    # Own sidecar draft, explicitly not a replacement/extension of the R4 integrated schema.
    claims=[
      {'id':'JH-01','kind':'observed_text_and_layout','text':'0초 표본: 좌측 (주)장헌 로고와 2026년 경영현황 보고, 오른쪽에 다리·구조물 이미지. 1~6초 선택 표본에서도 같은 제목 구성이 보임. 표본 사이 정지 여부는 미확정.','evidence':[evidence('자료005',0),evidence('자료005',6)],'human_status':'awaiting_human'},
      {'id':'JH-02','kind':'observed_numbers','text':'16초: 수주 55억·92%, 매출 31억·48%. 매출은 숫자 모션 중간값이며 최종 실적으로 사용하지 않음. 영업이익 카드는 목표 7억과 빈 실적/달성률 영역이 보임.','evidence':[evidence('자료005',16)],'human_status':'user_confirmed_only_sales_31억_48%'},
      {'id':'JH-03','kind':'observed_numbers_and_document_correspondence','text':'18초: 수주 목표60억/실적55억/92%, 매출 목표64억/실적39억/61%, 영업이익 목표7억/실적5억/71%. v4 JH01 표와 이 표본의 값이 일치. 사람 확인 범위는 세 지표 실적/달성률이며 목표값은 AI 초안.','evidence':[evidence('자료005',18)],'document_locator':'word/document.xml: JH01 목표와 현재 실적 표; 재구성 원고, 독립 정답 아님','human_status':'user_confirmed_55억_92%_39억_61%_5억_71%; targets_awaiting_human'},
      {'id':'JH-04','kind':'observed_change_with_sampling_limits','text':'14.5~18.5초 약0.25초 요청 표본에서 수주는 이미55억/92%, 매출은15.5초 빈 영역→16초31억/48%→16.5초39억/61%, 영업이익은16.5초 빈 영역→18초5억/71%로 바뀜. 정확한 시작·종료·경로·이징은 미측정.','evidence':[evidence('자료005',F('15.5'),'detail'),evidence('자료005',16),evidence('자료005',F('16.5'),'detail'),evidence('자료005',18)],'human_status':'awaiting_human_sequence; user_noted_16s_appears_mid_motion'},
      {'id':'JH-05','kind':'observed_text_and_document_partial_correspondence','text':'24초: 매출처별 실적의 후레씨네코리아9억/피티씨17억/장헌산업38억, 가족사비중86%가 v4 JH02와 대응. 사업분야별 프리캐스트36억/거더제작15억/철근가공9억/현장지원4억 표기가 보임. 프리캐스트56%는 이 표본에 아직 나타나지 않으므로 미확인. 전체 영상 누락/문서 오류로 판정하지 않음.','evidence':[evidence('자료005',24)],'document_locator':'word/document.xml: JH02 연간 예상 매출 구성 표','human_status':'awaiting_human'},
      {'id':'EG-01','kind':'observed_text','text':'4초: EG-BIM, Engineering Graphicer for BIM 표기가 보임. Graphicer 철자는 화면 전사 후보 그대로 보존하며 임의 교정하지 않음.','evidence':[evidence('자료013',4)],'human_status':'awaiting_human'},
      {'id':'EG-02','kind':'observed_text_not_product_validation','text':'4초 설명문 판독 초안: 디지털전환시대, EG-BIM은 / 도면작업 뿐 아니라 대량의 설계도면을 효율적으로 관리 할 수 있는 기능과 / 2D도면과 3차원 BIM모델을 동시에 보면서 Cross Check 할 수 있는 / 3D Viewer가 탑재된 신개념소프트웨어 입니다. 줄바꿈은 /로 표시. 이 문장은 화면 속 제품 설명이며 실제 제품 기능을 검증한 결과가 아님.','evidence':[evidence('자료013',4),evidence('자료013',F('15.5'))],'human_status':'awaiting_human'},
      {'id':'EG-03','kind':'observed_state_sequence','text':'3~7초 0.25초 표본에서 Value of 흰 글자 구성이 흐려지고 EG-BIM이 우측에 나타나며, 큰 E 형태가 녹색에서 금색/갈색 계열로 변함. 8초에는 좌측 위 노란 테두리 UI 이미지, 12초에는 그 앞 검정 바탕 도면 이미지, 14~15.5초에는 전면에 철근/콘크리트 형태 모델 이미지가 보임. 등장 경계·정확한 이동·카메라·실제 UI 조작 여부는 미확정.','evidence':[evidence('자료013',3),evidence('자료013',4),evidence('자료013',5),evidence('자료013',8),evidence('자료013',12),evidence('자료013',14),evidence('자료013',F('15.5'))],'human_status':'awaiting_human'},
    ]
    draft={'id':'A2-observation-draft','version':'0.2','scope':'two selected videos, sparse images and two dense windows only','format_status':'A2 evidence sidecar; not an R4 integrated record; no new fields inserted into Phase00 schemas','claims':claims,'human_approved_company_facts':False,'independent_evaluation':False,'audio':'metadata only; content/speech/silence not determined','remaining':['EG text and sequence human review','JH other frames/historical business truth not confirmed','SAR/VUI not resolved','R4 integrated evidence/spatial ingestion not implemented','audio/video synchronization not tested']}
    jfile(f'{AN}/관측초안.json',draft)
    # Explicit source evidence and user reply; no invented named reviewer or identity claim.
    scoped=[{'id':'H-JH16','statement':'16초 화면 매출 31억·48% — 모션 중간 표본','evidence':evidence('자료005',16)}, {'id':'H-JH18','statement':'18초 화면 수주55억·92%, 매출39억·61%, 영업이익5억·71%','evidence':evidence('자료005',18)}]
    context={'version':'0.1','question_scope':'numeric transcription on two extracted images only','items':scoped}
    ctxsha=hashlib.sha256(json.dumps(context,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
    receipt={'id':'A2-HUMAN-JH-20261016','recorded_at':'2026-10-16T13:00:47+09:00 or later; exact user submission time not exposed','source':'actual user reply in this chat','verbatim':'A안 맞음. 근데 니가 말한 16초는 모션 중에 판독한 화면 같음. 최종 값이 아닌데, 니가 중간중간 값을 잘 확인할 수 있는지 보려고 물어보는거야?','context_sha256':ctxsha,'context':context,'decision':'supported_for_scoped_numeric_transcription','motion_note':'user qualified 16s as apparently mid motion; not a separate validation of exact motion timing','not_approved':['actual business figures','whole video','goals in cards','all other JH/EG text','company grammar','audio','exact movement/easing'],'identity_verified':False,'company_approved':False}
    jfile(f'{VE}/사람확인_숫자판독_회신.json',receipt)
    jfile(f'{VE}/사람검수_대기.json',{'status':'partial_human_confirmation_received','confirmed':['H-JH16','H-JH18'],'pending_claims':[x['id'] for x in claims if x['id'] not in {'JH-02','JH-03'}]+['JH-02 remainder','JH-03 goals'],'no_auto_approval':True,'human_ground_truth_scope':'two frames, four actual/achievement number pairs; no accuracy denominator or generalization score'})
    # R4-1 records use table-derived composition timestamps, not relabelled demux PTS.
    tool=ROOT/'Phase 00/07_실행도구/시간프레임_규격검사.py'
    spec=importlib.util.spec_from_file_location('a2_r4_time',tool);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    checks=[]
    for info in inputs:
        aid=info['id'];run=load(aid,'initial');gate=info['container_preflight'];tr=next(t for t in gate['tracks'] if t['tkhd']['width_fixed16']>0);scale=tr['media']['timescale'];edit=tr['edits'][0]
        dur=F(int(edit['segment_duration_movie_ticks']),gate['movie']['timescale']);end=F(24)+F(1,30) if aid=='자료005' else F('15.5')+F(1,60)
        frames=[]
        for phase in ['initial','detail']:
            for f in load(aid,phase)['frames']:
                frames.append({'id':f['frame_id'],'timeline_ref':aid+'-T','period_ref':aid+'-SAMPLED','role':'within_period','source_pts':f['container_cts_ticks'],'pts_kind':'original_pts','time_base':q(F(1,scale)),'source_frame_ordinal':f['display_ordinal_zero_based'],'requested':q(f['requested_playback_seconds']),'actual':q(f['actual_playback_seconds']),'mapping_state':'mapped','selection_policy':'at_or_after','limitations':'source_pts is reconstructed original container CTS from stts/ctts, not PyAV edited PTS. All decoded PTS in this window crosschecked after elst offset. Sparse observation only; image hash in A2 sidecar.'})
        record={'contract_version':'0.1.0','source_type':'internal','asset':{'id':aid,'version':'sha256-'+info['sha256'][:12],'sha256':info['sha256']},'timelines':[{'id':aid+'-T','asset_ref':aid,'stream_index':0,'duration':q(dur),'duration_evidence_refs':['A2-MP4-PREFLIGHT-'+aid],'origin':{'method':'verified_offset','pts':edit['media_time_ticks'],'time_base':q(F(1,scale)),'evidence_refs':['A2-MP4-PREFLIGHT-'+aid,'A2-DECODE-CROSSCHECK-'+aid],'limitations':'Only a single rate-1 edit, no empty edit, progressive MP4. Not support for arbitrary edits or verified audio sync.'},'frame_rate_mode':'unknown','nominal_fps':None,'frame_count':None,'limitations':'Frame-count table metadata is recorded separately; full video decoding not performed.'}],'periods':[{'id':aid+'-SAMPLED','timeline_ref':aid+'-T','parent_ref':None,'kind':'range','start':q(0),'end':q(end),'uncertainty':None,'unknown_reason':None}],'frames':frames,'notes':'Actual internal media timing draft only. Range denotes extraction extent, not continuous semantic analysis. Boundary/measurement uncertainty remains unknown. Human content review is separate; integrated R4-2/R4-3 record not built.'}
        jfile(f'{AN}/{aid}/R4-1_시간연결_초안.json',record)
        result=mod.validate(record);checks.append({'id':aid,'record_sha256':sha(PUB/AN/aid/'R4-1_시간연결_초안.json'),'validator_path':str(tool),'validator_sha256':sha(tool),'result':result})
    jfile(f'{VE}/R4-1_규격검사_결과.json',checks)
    if not all(c['result']['valid'] for c in checks):raise ValueError('R4_time_invalid')
    # Re-extraction comparisons after the final code changes.
    comparisons=[]
    for aid in ['자료005','자료013']:
        for phase in ['initial','detail']:
            a=load(aid,phase);b=load(aid,phase+'_retest')
            pairs=list(zip(a['frames'],b['frames']))
            comparisons.append({'id':aid,'phase':phase,'same_count':len(a['frames'])==len(b['frames']),'images':len(pairs),'all_image_hashes_equal':all(x['sha256']==y['sha256'] for x,y in pairs),'all_times_ordinals_equal':all(all(x[k]==y[k] for k in ['actual_playback_seconds','reported_pts','container_cts_ticks','time_base','display_ordinal_zero_based']) for x,y in pairs),'original_hash_unchanged':a['input_sha256_after']==b['input_sha256_after'],'retest_timing_status':b['timing_status']})
    jfile(f'{VE}/보완후_재추출_비교.json',comparisons)
    if not all(c['same_count'] and c['all_image_hashes_equal'] and c['all_times_ordinals_equal'] and c['original_hash_unchanged'] for c in comparisons):raise ValueError('retest_difference')
    textfile(f'{AN}/00_분석초안_읽기.md', '''# 01-A2 분석 초안

2026-10-16 · 관측 초안 v0.2 · 장헌 두 화면 숫자만 사용자 확인, 나머지 사람 미검수.

이 폴더의 원본은 자료005 장헌_최종.mp4와 자료013 EG-BIM 홈페이지 01_(E).mp4다. 원본 해시와 모든 파생 이미지 시각/해시/변환은 입력고정 및 각 실행기록에 있다. `관측초안.json`은 A2 보조 초안이며 R4 통합 DB로 검증된 레코드가 아니다. R4-1 시간 연결만 기존 스키마/의미 검사기로 확인했다. 경계 오차와 내용 검수 미해결은 보존했다.

## 장헌

0·1·2·3·4·6초 표본에는 좌측 회사 로고/2026년 경영현황 보고와 다리 이미지가 있다. 8~20초 표본에는 좌측 ‘실적 및 계획 / 2026년 1~8월 누적 실적’, 우측 수주·매출·영업이익 카드가 있다. 22·24초 표본에는 ‘매출처별·사업분야별 실적’ 화면이 있다. 상태 경계는 표본 사이에 있으며 정확한 컷 시각을 측정하지 않았다.

| 근거 | 보이는 값/상태 | 문서 대응과 판단 |
|---|---|---|
| [16초](자료005/initial/f_00480_016.000.png) | 매출31억·48%, 수주55억·92%, 영업이익은 목표7억만 표시된 상태 | **매출 모션 중간값**. 31억·48%를 최종 실적으로 쓰지 않는다. 사용자 확인 범위는 매출31억·48% |
| [18초](자료005/initial/f_00540_018.000.png) | 수주55억·92%, 매출39억·61%, 영업이익5억·71% | v4 JH01 표와 대응. 이 여섯 숫자는 사용자 확인. 회사 실적 진위나 전체 영상 승인 아님 |
| [24초](자료005/initial/f_00720_024.000.png) | 매출처별9억/17억/38억과 가족사비중86%, 사업분야별36억/15억/9억/4억 | v4 JH02와 부분 대응. 프리캐스트56%는 이 표본에 아직 보이지 않아 **미확인**. 전체 누락 판정 아님 |

14.5~18.5초에 0.25초 간격으로 요청했다. 30fps 프레임에 맞춰 14.75 요청은 실제 14.7666…초가 선택되는 식이며 실제 PTS를 보존했다. 15.5초의 빈 실적 영역→16초의 중간값→16.5초 매출39억·61%, 이후 18초 영업이익5억·71%의 순서를 표본에서 확인했다. 정확한 시작/종료·속도·이징·AE 키프레임은 미측정이다.

v4는 완성 영상과 초기 기획서를 비교한 재구성 원고다. 대응이 있어도 독립 정답이나 제작 당시 의도 증명이 아니다. v03 PPT는 XML 본문 텍스트 추출이 0건이었으며 슬라이드 외관/이미지는 이번에 검토하지 않았다. 문서가 비었다는 뜻은 아니다. 문서의 페이지/레이아웃은 렌더 검수하지 않았다.

## EG-BIM 홈페이지 — 별도 시나리오 없음

[4초](자료013/initial/f_00240_004.000.png)에 EG-BIM / Engineering Graphicer for BIM과 2D도면·3차원 BIM모델·Cross Check·3D Viewer를 설명하는 문구가 보인다. Graphicer는 화면 철자 후보를 임의 교정하지 않고 보존했다. 전체 판독문은 관측초안 EG-02에 있다. 제품 설명을 실제 기능 검증으로 승격하지 않는다.

3~7초를 0.25초 표본으로 추가 확인했다. ‘Value of’ 문구가 흐려지고 우측 EG-BIM 제목이 보이며, 큰 E 형태의 색/외관이 녹색에서 금색/갈색 계열로 변한다. 8초 UI 이미지→12초 전면 도면 이미지→14~15.5초 철근/콘크리트 형태 모델 이미지 순으로 보인다. [15.5초](자료013/initial/f_00930_015.500.png)에서 이 겹침 배치를 확인할 수 있다. 상세 UI 글자·기능·조작 여부·카메라 경로는 미확인이다. 다른 홍보영상 스토리보드나 새 대본을 사용하지 않았다.

## 공통 한계

- 장헌은 0~24초까지 디코드하고 15개 기본/17개 세부 이미지를 선택했다. 24초 이후는 관찰하지 않았다. EG는 0~15.5초까지 디코드하고 17개 기본/17개 세부 이미지를 선택했다. 마지막 약0.68초의 영상 표본과 약0.03초의 movie/edit 길이 차이는 남아 있다.
- 66개 PNG는 중복 시점 7개를 포함한 **59개 고유 시점**이다. 전 프레임 내용을 사람이/AI가 검토한 것이 아니다. 연락시트는 축소 개요이며 핵심 문구는 개별 PNG로 대조했다. 그 외 작은 글자/표본 사이 변화는 누락될 수 있다.
- 두 파일의 tkhd는 명시적 항등행렬이다. 회전 적용 없이 raw raster를 가로1920으로 비례 축소했다(장헌1920×540, EG1920×1080). SAR 보고값0/1은 미확인으로 처리한다. H264 VUI의 SAR는 별도 감사하지 않았으므로 표시비율/정밀좌표를 확정하지 않는다.
- 둘 다 AAC 트랙이 있지만 듣기·오디오 디코드·전사·동기 검증을 하지 않았다. 무음 또는 발화 없음으로 쓰지 않는다. 별도 API 호출0건. 현재 Codex 이미지 읽기는 연결 AI 처리다.
''')
    textfile(f'{VE}/자체검수와_레드팀_보완.md','''# 01-A2 자체검수·레드팀·보완

2026-10-16 · 동일 작성자의 자체 반대 관점 검토. 독립 에이전트/독립 실행자 검토 아님. 별도 모델 변경 없음.

| 단계/문제 | 실제 결과와 보완 | 영향 범위 재시험/남은 한계 |
|---|---|---|
| 사전 경로/외부 참조/리소스 | 등록 두 파일만 선택. MP4 dref self-contained/url flags1, stsd 참조1 확인. 외부 URL·로컬경로·URN·참조2·fragmented·손상 구조를 거부. mov를 명시하고 read-only file object, enable_drefs0/use_absolute_path0 적용 | 사전11항목, 보완후17항목 확인. 17은 기술 게이트 수이며 영상 정확도 아님. 모든 적대적 MP4/네이티브 취약점 격리 보장 아님 |
| 첫 추출에서 SAR0/1을 비정방으로 오인해 두 파일 중지 | 프레임0장, 실패와 코드 보존 | None만 허용한 두 번째 시도도0/1 때문에 두 파일 중지. 세 번째에서 falsy=unknown으로 보완. SAR를1로 채우지 않음 |
| 장헌 SEI 부가정보 열거 실패 | 세 번째 장헌 첫 프레임 metadata에서 AttributeError, 이미지0장. EG는17장 성공 | side_data의 키를 직접 문자열로 기록하도록 보완. 장헌15장 성공. 최종 기본·세부 두 입력 재추출에서66장 전부 이미지해시/시간/ordinal 동일 |
| 상위 프로세스가 자식 실패 후에도 종료0일 수 있음 | 초기 실패 로그의 개별 exit1을 숨기지 않음. 최종 runner는 하나라도 실패하면 exit1 | 최종 성공 로그 exit0. 실패를성공/내용없음으로 기록하지 않음 |
| manifest ID만 제한하면 변조 경로가 들어갈 수 있음 | 고정된 두 등록 상대경로와 절대경로를 함께 재대조. 해시는 열기 전/완료후 대조 | 두 입력 재추출 해시 동일. 네트워크 프로토콜 입력 거부. 잠재적 TOCTOU·native 취약점 전체 해결 주장은 안 함 |
| 선언만 있는 출력수 제한 | 실제 target 개수/정렬/중복검사 추가. 파일2GiB/moov32MiB/metadata4MiB/box2만/표본10만 제한. worker45초/1.5GiB/packet4000/frame1600/pixels8294400/read요청256MiB/seek2만/image40 | 메모리 Job 설정·자식 타임아웃 종료·무제한read 거부 시험. 추출 실패 중간물은 별도 보존 |
| edited PTS를 raw PTS로 착각 | stts+ctts로 원본 CTS 재구성, elst offset 장헌1024/15360=1/15초, EG1000/60000=1/60초 적용. 실제 디코드 창 전체의 표시 PTS와 일치 | 기본 장헌721/EG931, 세부 장헌556/EG421프레임 대조. 재시험 같은범위 일치. 동일 파일/같은 decoder 계열 사용, 별도 decoder 교차검증 아님 |
| 영화 길이/stream 길이를 섞음 | EG mvhd16.213333…초, 단일 video edit16.183333…초, PyAV container16.183333초 보고 차이0.03초 보존 | 마지막부분 미관찰. audio sync나 전체duration 재생검증으로 확대하지 않음 |
| 중간 숫자를 최종 실적으로 읽거나 문서값으로 덮음 | 장헌16초31억/48%를 그대로 보존하고 중간표본으로 분리. 18초39억/61%와 대조. 사용자 실제 숫자확인 회신 보존 | 두화면 숫자만 확인. 사람질문 목적이 불명확했다는 피드백 반영: 중간값판독/안정값 구분을 명시 |
| 24초에서56%가 안보이면 전체누락으로 단정 | 그표본의 미확인으로만 기록 | 24초후 미관찰. 회사수치/영상품질 오류로판정 안함 |
| 작은 연락시트만으로 모든 글자를 확정 | 장헌16/18/24, EG4/15.5를 개별1920PNG로 재대조 | 그밖의작은 UI글자 보류. 정확한폰트·색·이징·실제UI조작/제품성능 보류 |
| Word 대응을 독립정답/음성사실로 사용 | 재구성문서 성격과 음성미처리 명시. PPT 텍스트0은 외관미검토로표시 | 문서레이아웃·나레이션·AV동기 미검수 |
| 형식통과를 내용승인으로 확대 | 기존R4-1 시간검사 수행. 경계오차미상 unresolved 유지. A2측면기록은 통합R4 DB 레코드라고 부르지않음 | R4-2/R4-3 통합이관은 후속구현; 이번에 정본스키마 수정안함 |

원본 MP4/Word/PPT와 Phase00 정본·봉인보고를 수정하지 않았다. 스킬3개를 실행·전환·설치하지 않았고 A3도 시작하지 않았다. CU/AE 연결을 조회·해제·재설정하지 않았다. 주어진라이선스는 로컬후보사용범위이며 조직재배포 적합성 감사로확대하지않는다.
''')
    textfile(RE,'''# 01-A2 결과 — 작은 실제 영상 예비 분석

2026-10-16 · **실행·자체검수·자체레드팀·보완 재시험 완료 / 사람 확인은 장헌 두 화면 숫자만 접수 / 나머지 미검수**

승인된 로컬 추출 방식으로 자료005 장헌과 자료013 EG-BIM 홈페이지를 순서대로 처리했다. 장헌0~24초와 EG0~15.5초에서 **66개 이미지(59개 고유시점)**를 추출하고, 장헌14.5~18.5초·EG3~7초를 촘촘히 대조했다. 전체영상/41개자료 성능평가나 회사문법 확정이 아니다.

## 확인한 내용

- **장헌 숫자 모션을 구분했다.** 16초 매출31억·48%는 중간값, 18초 매출39억·61%는 이후 안정된 표본의 값이다. 18초 수주55억·92%, 영업이익5억·71%도 보인다. 사용자는 두 화면의 제시 숫자 판독이 맞다고 답했다. 중간값을 최종실적으로 사용하지 않으며 실제 회사 실적의 진위까지 승인된 것은 아니다.
- 장헌18초의 값은 v4 JH01과 일치한다. v4는 재구성 원고이므로 독립 정답이 아니다. 24초는 JH02 일부와 대응하지만 프리캐스트56%는 아직 안보여 미확인이다. 전체 누락으로 판단하지 않았다.
- **시나리오 없는 EG-BIM도 정상 처리했다.** 제목/설명문, 큰 E의 외관변화, UI·도면·모델 이미지의 겹침/등장 순서를 관측초안으로 기록했다. 새 대본을 만들거나 홍보영상 스토리보드를 가져오지 않았다. 작은 UI 글자·제품성능·정확한 모션은 보류했다.

## 기술 검수와 실패

| 항목 | 결과/한계 |
|---|---|
| 원본 | 장헌90초·3840×1080, EG movie16.213333…초·3840×2160. 두 파일해시·등록경로 고정, 처리전후 해시동일 |
| 시간 | B-frame이 있는 두MP4의 stts/ctts와 단일rate1 edit를 직접 읽어 디코드창의 전프레임 PTS와 대조. 장헌원점CTS1024/15360, EG1000/60000. FPS×초로 번호생성 안함 |
| 경로/리소스 | self-contained MP4만 허용, 등록두경로 제한, 외부참조 거부시험. 시간/메모리/읽기/프레임/픽셀/출력 제한 적용. 전면적 적대파일보안 인증 아님 |
| 화면방향/SAR | tkhd 명시적 항등행렬, 회전 미적용. SAR0/1은 미확인. raw raster 비례축소만 시행; 표시비율·정밀좌표 미확정 |
| 음성 | 장헌AAC44.1kHz mono, EGAAC48kHz stereo 트랙확인. 오디오디코드/청취/전사/AV동기는 미실행. 무음이라판정 안함 |
| 실패보존 | SAR판정에서 두차례 각각 두파일 중지, 이후 장헌SEI metadata 오류. 실패코드/로그/중간물은 backup에 보존. 보완후 양쪽 기본·세부 추출 성공 |
| 재시험 | 기술게이트17항목 확인. 최종동일조건 재추출66장 해시/시각/ordinal 동일. 추출재현성 확인이며 한국어정확도/독립성능평가 수치 아님 |
| R4 | 기존R4-1 두시간레코드 형식/의미검사 valid, 경계오차미상 unresolved유지. 통합R4-2/R4-3 이관/내용검수는 완료아님 |

## 검수 상태와 남은 일

장헌두화면의 제시숫자는 실제 사용자회신으로 한정확인했다. 그밖의 문구·수치·동작초안과 EG설명문은 사람미검수로 남긴다. 장헌24초후와 EG마지막약0.68초는 관찰하지 않았고, 표본사이의 짧은변화도 놓칠수있다. 보고된기간은 연속내용검수기간과 다르다.

별도AI API 호출0건, 전사0건, 새분석스킬0개다. 현재Codex에서 추출화면을 읽었으므로 완전오프라인 AI분석은 아니다. 실제호스트모델 식별자/내부이미지리사이즈는 도구에서 제공하지 않았다. 독립검토자/모델변경 없이 작성자 자체레드팀을 수행했다. A3·01-B·Phase02·기존관리스킬 기본전환은 자동착수하지 않았다.

## 기록 위치

- [관측 초안과 실제 화면](../02_분석작업/01-A2_작은예비/00_분석초안_읽기.md)
- [자체검수·레드팀·보완](../04_검증자료/01-A2_작은예비/자체검수와_레드팀_보완.md)
- [사람 회신과 한정 확인범위](../04_검증자료/01-A2_작은예비/사람확인_숫자판독_회신.json)
- [재추출 비교](../04_검증자료/01-A2_작은예비/보완후_재추출_비교.json)

중요검수 기록은 루트 작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_01-A2에 기술/내용/보완 구분으로 보존한다. 새 PDF는 만들지 않았다. 다음 판단은 남은내용검수와 후속A3 범위검토이며, 이번회신을 후속단계 실행승인으로 확대하지않는다.
''')
    jfile(f'{P}/00_진행안내/15_01-A2_실행결과_현재안내.json',{'date':'2026-10-16','status':'A2_bounded_execution_reported_partial_human_confirmation','report':RE,'A2_authorized':True,'A2_execution_performed':True,'selected_media_opened':2,'unique_sample_times':59,'primary_images':66,'separate_media_API_calls':0,'audio_transcriptions':0,'new_skills_created':0,'human_review_received':'JH16 sales pair and JH18 three actual/achievement pairs only','remaining_human_review':True,'independent_review':False,'A3_started':False,'Phase00_modified':False,'CU_AE_connection_changed':False,'older_status_is_historical':True})
    print('Built',PUB)
    print('R4:',[(c['id'],c['result']['valid'],len(c['result']['unresolved'])) for c in checks])
    print('Retest:',comparisons)
if __name__=='__main__':main()
