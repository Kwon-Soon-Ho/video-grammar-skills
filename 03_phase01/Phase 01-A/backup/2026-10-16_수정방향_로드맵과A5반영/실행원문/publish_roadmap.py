from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json, hashlib, os, shutil
from urllib.parse import unquote
import re

WS=Path(__file__).resolve().parents[2]
WORK=WS/'tmp/roadmap-update-20261016'
MANIFEST=WORK/'manifest.json'
m=json.loads(MANIFEST.read_text(encoding='utf-8'))
ROOT=Path(m['project']).resolve()
EXPECTED=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증').resolve()
assert ROOT==EXPECTED
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def safe(relative):
    pp=Path(relative)
    assert not pp.is_absolute() and '..' not in pp.parts
    p=(ROOT/pp).resolve()
    p.relative_to(ROOT)
    return p

allowed={
 '00기획/00_최종_파이프라인_계획.md',
 '00기획/07_Phase01-A_진행계획.md',
 '00기획/00_최신기획_읽는순서.md',
 '00기획/08_수정방향_단계별반영.md',
 'Phase 01-A/00_진행안내/22_01-A5_진행계획.md',
 'Phase 01-A/00_진행안내/23_수정방향과_A5계획_현재안내.json',
 'Phase 01-A/00_진행안내/01-A_계획상태.json',
 'Phase 01-A/00_진행안내/10_01-A_계획_읽는순서.md',
 'Phase 01-A/00_진행안내/새채팅인계/00_새채팅_이어하기.md',
 'Phase 01-A/05_결과보고/15_수정방향_로드맵과_A5계획_반영.md',
 '작업 보고서(pdf)/02_중요검수기록/Phase 01-A/2026-10-16_수정방향_로드맵과A5반영/계획변경_검토기록.md'
}
assert len(m['changes'])==11
assert {c['relative_path'] for c in m['changes']}==allowed
assert not m['link_failures']
for c in m['changes']:
    target=safe(c['relative_path'])
    staged=Path(c['staged_path']).resolve()
    staged.relative_to((WORK/'staged').resolve())
    assert sha(staged)==c['after_sha256']
    if c['action']=='edit': assert target.is_file() and sha(target)==c['expected_before_sha256'], ('source_changed',c['relative_path'])
    else: assert not target.exists(), ('already_exists',c['relative_path'])
for relative,h in m['protected_hashes'].items(): assert sha(safe(relative))==h, ('protected_source_changed',relative)

before_state=json.loads((WORK/'before/Phase 01-A/00_진행안내/01-A_계획상태.json').read_text(encoding='utf-8-sig'))
after_state=json.loads((WORK/'staged/Phase 01-A/00_진행안내/01-A_계획상태.json').read_text(encoding='utf-8'))
for key,value in before_state.items():
    if key not in m['state_fields_allowed_to_change']: assert after_state[key]==value, key
assert after_state['A5_started'] is False and after_state['numeric_thresholds'] is None
assert after_state['locked_sample_sets']==0 and after_state['current_skill_version']=='0.1.0-draft.3'

backup=safe(m['backup_relative'])
assert not backup.exists(), 'backup batch already exists; inspect prior outcome before retrying'
backup.mkdir(parents=True)
# Save exact original bytes for every edited document before changing any original.
for c in m['changes']:
    if c['action']=='edit':
        original=safe(c['relative_path'])
        saved=backup/'변경전'/c['relative_path']
        saved.parent.mkdir(parents=True,exist_ok=True)
        saved.write_bytes(original.read_bytes())
        assert sha(saved)==c['expected_before_sha256']
for source in [Path(__file__),WS/'tmp/plan-revision/update_roadmap.py',MANIFEST,WORK/'review.diff']:
    saved=backup/'실행원문'/source.name
    saved.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,saved)

# Publish navigation and the shared state after the documents they reference.
ordered=sorted(m['changes'],key=lambda c:(
    c['relative_path']=='Phase 01-A/00_진행안내/01-A_계획상태.json',
    c['relative_path'].endswith('읽는순서.md'),c['action']=='edit'))
written=[]
try:
    for c in ordered:
        target=safe(c['relative_path'])
        if c['action']=='edit': assert sha(target)==c['expected_before_sha256']
        else: assert not target.exists()
        target.parent.mkdir(parents=True,exist_ok=True)
        temporary=target.with_name(target.name+'.codex-plan-update.tmp')
        temporary.resolve().relative_to(ROOT)
        assert not temporary.exists()
        temporary.write_bytes(Path(c['staged_path']).read_bytes())
        os.replace(temporary,target)
        assert sha(target)==c['after_sha256']
        written.append(c['relative_path'])

    protected_ok={p:sha(safe(p))==h for p,h in m['protected_hashes'].items()}
    assert all(protected_ok.values())
    link_errors=[]
    for c in m['changes']:
        f=safe(c['relative_path'])
        if f.suffix=='.json': json.loads(f.read_text(encoding='utf-8'))
        if f.suffix!='.md': continue
        text=f.read_text(encoding='utf-8')
        assert '{{' not in text and '\ufffd' not in text
        for match in re.finditer(r'\]\((<[^>]+>|[^)]+)\)',text):
            ref=unquote(match.group(1).strip('<>').split('#')[0])
            if not ref or ref.startswith(('https:','http:','codex:','thread:')): continue
            target=Path(ref) if re.match(r'^[A-Za-z]:[/\\]',ref) else f.parent/ref
            if not target.exists(): link_errors.append(dict(source=c['relative_path'],target=ref))
    assert not link_errors,link_errors
    result={
      'status':'published_and_readback_verified',
      'at':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),
      'changed_files':[{k:c[k] for k in ['relative_path','action','expected_before_sha256','after_sha256']} for c in m['changes']],
      'protected_file_count':len(protected_ok),'protected_hashes_unchanged':protected_ok,
      'historical_state_values_preserved':True,'internal_link_errors':link_errors,
      'json_parse':'passed','A5_started':False,'A5_materials_locked':False,
      'skill_or_past_evaluation_modified':False,'backup':str(backup),
      'review_scope':'author document consistency and file-integrity review; no media analysis or independent redteam'
    }
    report=safe('작업 보고서(pdf)/02_중요검수기록/Phase 01-A/'+m['batch']+'/저장검증.json')
    payload=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    report.write_text(payload,encoding='utf-8')
    (backup/'게시완료.json').write_text(payload,encoding='utf-8')
    (WORK/'publication-receipt.json').write_text(payload,encoding='utf-8')
    print(json.dumps({'status':result['status'],'changed_files':len(written),'protected_files':len(protected_ok),'backup':str(backup),'verification':str(report)},ensure_ascii=False))
except Exception as e:
    failure={'status':'partial_or_failed_inspect_before_retry','written':written,'error':repr(e)}
    (WORK/'publication-failure.json').write_text(json.dumps(failure,ensure_ascii=False,indent=2),encoding='utf-8')
    raise
