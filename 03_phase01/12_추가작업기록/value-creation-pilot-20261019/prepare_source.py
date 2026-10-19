from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
D=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
FOLDER=D/'한맥 영상/00_26년 가치창출 영상';OUT=HERE/'extraction'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4*1024**2),b''):h.update(b)
 return h.hexdigest()
def save(p,d):p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
video=FOLDER/'가치창출성과 영상_260923_v3.mp4';scenario=FOLDER/'가치창출 시나리오_v1(260916).pdf'
metadata=json.loads((HERE/'video-metadata.json').read_text(encoding='utf-8'))
decision={'utc':datetime.now(timezone.utc).isoformat(),'prior_choice_question_id':'call_489db710df544799a39b33d9ab93cdfb',
 'accepted_batch':'두 사례의 새 기록+새 브리프 화면안/모션 스토리보드 시범. 현재 스킬 미변경.',
 'steering':'사용자가 원본을00_26년 가치창출 영상으로 교체.노듈러/PG 대신 이 원본 안의대표 장면2개를 선정해 같은 시범을 진행.',
 'scenario_rule':'우측 푸른 글씨가 변경안. 변경 없음은 좌측 기존 시나리오 유지. 편집 지시/예상시간은 내레이션과 구분.',
 'video':{'path':str(video),'sha256':sha(video),'bytes':video.stat().st_size,**metadata},
 'scenario':{'path':str(scenario),'sha256':sha(scenario),'pages':6,'visually_reviewed_pages':[1,2,3,4,5,6]},
 'status':'development pilot, not company approved or independent evaluation','audio':'metadata only; not listened/transcribed',
 'archive_retry':'사용자 선택에 따라 정상승인경로로재시도했으나검토모델용량초과로실행전실패.이경로를우회하지않음.'}
save(HERE/'decision.json',decision)
pages=[]
with pdfplumber.open(str(scenario)) as pdf:
 for i,p in enumerate(pdf.pages):
  left=p.crop((55,58,590,785)).extract_text() or '';right=p.crop((600,58,1155,785)).extract_text() or ''
  changed=i in (1,2,3)
  blue=[x for x in p.chars if x['x0']>600 and x.get('non_stroking_color')==(0,0,1)]
  pages.append({'page':i+1,'decision':'use_right_blue_revision' if changed else 'retain_left_original',
   'left_text':left,'right_text':right,'effective_text':right if changed else left,'blue_char_count':len(blue),
   'editorial_note':'도입부/본문/마무리 예상시간은 PDF 편집 메모이며 실제 영상 타임코드가 아님' if i in (0,4,5) else None})
save(HERE/'effective-scenario.json',{'source':decision['scenario'],'policy':decision['scenario_rule'],'pages':pages,'status':'text extracted by column and visually checked against all6 pages; not an audio transcript'})
(HERE/'effective-scenario.txt').write_text('\n\n'.join(f"=== PAGE {p['page']} / {p['decision']} ===\n"+p['effective_text'] for p in pages),encoding='utf-8')
OUT.mkdir(exist_ok=True);(OUT/'tools').mkdir(exist_ok=True);(OUT/'requests').mkdir(exist_ok=True)
old=ROOT/'internal-video-audit-20261019/source-overview/tools'
s=(old/'prepare.py').read_text(encoding='utf-8').replace(str(ROOT/'internal-video-audit-20261019/source-overview').replace('\\','\\\\'),str(OUT).replace('\\','\\\\'))
(OUT/'tools/prepare.py').write_text(s,encoding='utf-8');shutil.copy2(old/'extract.py',OUT/'tools/extract.py')
save(OUT/'manifest.json',[{'id':'VALUE','path':str(video),'registered_relative_path':video.relative_to(D).as_posix(),'sha256':decision['video']['sha256'],'duration_seconds':'2172/5','previous_exposure':'new source selected by user; development review, no independent holdout claim'}])
save(OUT/'adapter-scope.json',{'files_allowlisted':[str(video)]})
times=list(range(0,433,12))
for i in range(0,len(times),13):save(OUT/'requests'/f'VALUE-overview{i//13+1}.json',[str(t) for t in times[i:i+13]])
print(json.dumps({'video_sha256':decision['video']['sha256'],'duration':metadata['duration_seconds'],'scenario_pages':6,'revision_pages':[2,3,4],'retained_pages':[1,5,6],'overview_samples':len(times)},ensure_ascii=False))
