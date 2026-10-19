"""Preserve draft.7 before making a separately reviewable draft.8 candidate."""
from pathlib import Path
import json, hashlib, shutil, zipfile
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'analysis-reliability-20261019/candidate/company-video-grammar-analyzer'
NEW=HERE/'candidate/company-video-grammar-analyzer'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
if NEW.exists():raise SystemExit('candidate already exists')
files=sorted(p for p in OLD.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
backup=HERE/'backup/draft7-before-coverage.zip';backup.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(backup,'x',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(OLD).as_posix())
with zipfile.ZipFile(backup) as z:
    assert z.testzip() is None
    assert all(hashlib.sha256(z.read(p.relative_to(OLD).as_posix())).hexdigest()==sha(p) for p in files)
write(HERE/'backup/manifest.json',{'source':str(OLD),'zip':str(backup),'zip_sha256':sha(backup),'files':[{'relative':p.relative_to(OLD).as_posix(),'sha256':sha(p)} for p in files]})
shutil.copytree(OLD,NEW,ignore=shutil.ignore_patterns('__pycache__'))
for p in NEW.rglob('*'):
    if p.suffix in ('.md','.json','.py'):
        s=p.read_text('utf-8')
        if p.name=='check_record.py':
            s=s.replace("('0.1.0-draft.6','0.1.0-draft.7')","('0.1.0-draft.6','0.1.0-draft.7','0.1.0-draft.8')")
            s=s.replace("d.get('skill_version')=='0.1.0-draft.7'","d.get('skill_version')=='0.1.0-draft.8'")
        else:s=s.replace('0.1.0-draft.7','0.1.0-draft.8')
        p.write_text(s,encoding='utf-8')
skill=NEW/'SKILL.md'
s=skill.read_text('utf-8').replace('## 기록과 종료','## 원본 전체와 구간의 진행 범위\n\n[범위 집계](references/source-coverage.md)에 따라 원본별 개요 표본, 잠정 작업 묶음, 실제 기록 구간을 구분한다. 전체 범위를 훑은 표본 수를 정밀 분석 시간으로 바꾸지 않는다. 구간 기록의 합집합과 미기록 시간·열린 쟁점은 `scripts/source_coverage.py`로 집계한다. 이 도구는 장면 발견이나 정밀 검수 완료를 판정하지 않는다.\n\n## 기록과 종료')
skill.write_text(s,encoding='utf-8')
p=NEW/'references/motion-review.md'
s=p.read_text('utf-8')+'''\n## 공통 변환과 방향 모양의 검증\n\n새 요소가 늘어나 구도가 달라 보여도 지도·배경·기존 카드가 확대/축소되었다고 단정하지 않는다. 서로 떨어진 지속 가시 기준점의 위치·간격을 처음·중간·끝에서 비교한다. 가림·내용 교체·강조로 바뀐 기준점은 비교에서 제외하고 그 이유를 남긴다. 영상의 좌표 안정성과 실제 AE 카메라/부모 리그는 별도 주장이다. 자동 정합 수치와 변환 잔차는 시각 확인의 보조이며 적은 점에 맞춘 낮은 잔차만으로 검증을 통과시키지 않는다.\n\n위·아래를 향하는 화살촉의 형태와 시간에 따라 이동하는 방향을 분리한다. 반복 무늬가 같은 자리로 돌아오는 표본 간격이면 정지처럼 보일 수 있다. 쟁점 ROI를 연속 프레임 또는 다른 간격으로 보강하고 검사한 구간만 판정한다. 강약 변화만 보이면 밝기 변화로 기록하고 이동 방향을 만들지 않는다.\n\n오판을 발견하면 이전 문장을 보존한 채 `rejected`로 표시하고, 새 근거에 맞는 긍정 관측을 추가한다. 흐름·레이아웃 요약과 속성 행에서도 기각된 결론이 계속 사실로 사용되지 않는지 확인한다.\n'''
p.write_text(s,encoding='utf-8')
print(json.dumps({'backup_files':len(files),'backup_sha256':sha(backup),'candidate':str(NEW)},ensure_ascii=False))
