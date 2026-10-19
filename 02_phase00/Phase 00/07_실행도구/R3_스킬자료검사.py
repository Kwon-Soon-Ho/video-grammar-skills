"""R3-3 자체 자료의 provenance/권한/경계 검사. 외부 SKILL·코드는 실행하지 않는다."""
from pathlib import Path
import json,hashlib,sys
BASE=Path(__file__).resolve().parents[1] if Path(__file__).resolve().parent.name=='07_실행도구' else Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00')
OUT=BASE/'05_출처와검토/스킬심층검토'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(doc,ledger,check_files=True):
 errors=[]
 def check(test,msg):
  if not test:errors.append(msg)
 check(doc['user_decision']['status']=='accepted' and doc['user_decision']['choice']=='A','사용자 A 결정')
 for k in ['upstream_code_executed','global_skill_installation','existing_connections_modified','company_approval_created','custom_skills_changed']:check(doc.get(k) is False,'권한/실행 사실 '+k)
 check(len({c['id'] for c in doc['cards']})==len(doc['cards']),'후보 ID중복')
 check(len(doc['evidence_reports'])>=9,'독립근거수')
 entries_external=[];entries_local=[]
 for c in doc['cards']:
  for key in ['purpose','exclude_or_rewrite','counterexample','license_note','unresolved']:check(bool(c.get(key)),c['id']+' '+key+'누락')
  check(c.get('company_mandatory') is False and c.get('runtime_verified') is False,c['id']+' 근거없는승격')
  check(c.get('upstream_runtime_adoption')=='held',c['id']+' 실행도입')
  check(c.get('direct_upstream_copy_into_custom_skill_or_product_performed') is False,c['id']+' 직접이식')
  if c['id']=='anthropic-pptx':check(c['status']=='excluded_from_direct_or_derivative_reconstruction' and not c['retain_as_proposal'],'PPT제한원본 활용제외')
  if c['source_package'].startswith(('local:','expanded-local:','editorial-local:')):entries_local += [(c['source_package'],x) for x in c['entrypoints']]
  elif not c['source_package'].startswith('host-bundled:'):entries_external += [(c['source_package'],x) for x in c['entrypoints']]
 check(len(set(entries_external))==doc['counts']['external_selected_skill_entrypoints'],'외부본문수량')
 check(len(set(entries_local))==doc['counts']['local_selected_skill_entrypoints'],'로컬본문수량')
 check(len(doc['cards'])==doc['counts']['candidate_groups'],'그룹수량')
 check(doc['counts']['host_bundled_entrypoint_selected_sections']==1,'호스트부분읽기')
 rows=ledger['records'];paths={r['absolute_path'] for r in rows};ct=ledger['counts']
 check(ct['review_rows']==len(rows) and ct['unique_files']==len(paths) and ct['duplicate_review_rows']==len(rows)-len(paths),'중복/고유파일분모')
 check(all(bool(r.get('depth')) and r.get('executed') is False for r in rows),'깊이/실행구분')
 if check_files:
  for r in rows:
   p=Path(r['absolute_path']);check(p.is_file() and sha(p)==r['sha256'],'파일검토해시 '+r['path'])
  for r in doc['evidence_reports']:check((BASE/r['path']).is_file() and sha(BASE/r['path'])==r['sha256'],'독립보고해시 '+r['path'])
 return errors
if __name__=='__main__':
 d=json.loads((OUT/'스킬심층검토정본.json').read_text(encoding='utf-8'));l=json.loads((OUT/'검토파일목록.json').read_text(encoding='utf-8'));errors=validate(d,l)
 print(json.dumps(dict(errors=errors,review_rows=len(l['records']),unique_files=len({r['absolute_path'] for r in l['records']}),scope='저장된검토기록의근거/권한/깊이/수량.실행안전·디자인효과검사아님.'),ensure_ascii=True))
 sys.exit(1 if errors else 0)
