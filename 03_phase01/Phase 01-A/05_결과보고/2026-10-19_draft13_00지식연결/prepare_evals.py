from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parent;W=R.parent
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
root=R/'eval-inputs';root.mkdir(exist_ok=True)
shutil.copytree(W/'collection-skill-structure-20261019/records',root/'static',dirs_exist_ok=True)
shutil.copytree(W/'value-creation-collection-20261019',root/'motion',dirs_exist_ok=True)
P=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증/Phase 00')
(root/'input.md').write_text(f'''# 공통 입력

Phase 00 루트: `{P}`. 공통 용어/지식/품질과 현재 안내는 이 루트의 정본을 읽는다. 프로젝트 전체 기록은 Markdown 기본이며 사용자가 요청한 조회를 위해 필요한 부속 색인은 함께 만들 수 있다.

원본 파일: 가치창출성과 영상_260923_v3.mp4. 원본 입력에서 제공된 SHA256 be78fc4f2f94c6b3cbd31339a1a1ccc84b91613d56c0e485d5dd1296839f56fa, 434.4초/7680×2160/30fps. 이번 입력은 원본 MP4/오디오/시나리오를 포함하지 않는다.

static: 기존134/172초 기록과 각 PNG. 원기록은 prior analysis이며 실제 보이는 내용은 PNG로 대조할 수 있다. 두 시각 사이의 연속 모션을 관측한 입력은 아니다.
motion: 기존 계약/지원 수집 기록과6개 표본 모음. 모음과 기존기록을 대조할 수 있지만 새로 전편 재생/원본 재추출한 결과가 아니다. 미관측/원값/음성은 미상이다.

기존 의미/번호/근거·상세를 보존하고 새 결과에 필요한 연결을 추가한다. 신규 화면/영상/PDF 제작, 정본 변경/등록, 글로벌 스킬 활성화는 이 과제 범위가 아니다.
''',encoding='utf-8')
evals=[
 {'id':1,'name':'static-knowledge-use-review','prompt':'134·172초 두 화면의 원본과 기존 수집 기록을 확인하고, Phase 00 지식과 연결한 DB 수집 기록 및 조회 색인을 만들어줘. 다음에 업무 이미지 묶음·건물/기단·역할판 구성을 찾아 어느 내용에 쓰였고 현재 무엇이 다른지 근거까지 돌아갈 수 있게 해줘. 관련 지식과 실제 검토 결과를 구분하고, 기존 상세와 번호를 보존해. 새 화면 제작은 필요 없어.','files':['input.md','static/00_사례요약.md','static/01_부품과조합.md','static/02_전체상세.md','static/03_근거와검수.md','static/04_모션조사.md','static/evidence/134.png','static/evidence/172.png']},
 {'id':2,'name':'motion-knowledge-use-review','prompt':'계약·프로젝트 지원의 기존 모션6개 관측 창을 00 지식과 연결해 수집 기록과 조회 색인으로 정리해줘. 전체 흐름·독립 동작·시간 관계를 보존하고, 수치와 도상이 끝나는 시점이 다른 사례를 찾아 어떤 내용에 쓰였는지와 원래 근거까지 조회할 수 있게 해줘. 관련 원칙과 실제 검토/보류를 구분해. 기존 기록 재검토 범위이며 새 원본 연속 관측이나 화면 제작은 하지 않아.','files':['input.md','motion/01_계약_수집기록.md','motion/02_프로젝트지원_수집기록.md','motion/03_재사용단위_색인.md','motion/05_근거와_실행기록.md','motion/evidence/contract-reflow.jpg','motion/evidence/contract-panel.jpg','motion/evidence/contract-number.jpg','motion/evidence/project-reflow.jpg','motion/evidence/project-wipe.jpg','motion/evidence/project-panel.jpg']}]
it=R/'company-video-grammar-analyzer-workspace/iteration-4'
for e in evals:
    e['files']=[str(root/f) for f in e['files']]
    folder=it/f"eval-{e['id']}-{e['name']}";folder.mkdir(parents=True,exist_ok=True)
    save(folder/'eval_metadata.json',{'eval_id':e['id'],'eval_name':e['name'],'prompt':e['prompt'],'files':e['files'],'assertions':[],'baseline':'draft.12','candidate':'draft.13','scope':'same known video/records; fresh-context AI runs; no general holdout'})
save(R/'candidate/company-video-grammar-analyzer/evals/evals.json',{'skill_name':'company-video-grammar-analyzer','evals':evals})
for name,base in [('old',R/'backup/draft12/company-video-grammar-analyzer'),('new',R/'candidate/company-video-grammar-analyzer')]:
    save(R/f'eval-{name}-skill-pin.json',[{'path':str(f),'sha256':sha(f)} for f in sorted(base.rglob('*')) if f.is_file()])
print(str(it))
