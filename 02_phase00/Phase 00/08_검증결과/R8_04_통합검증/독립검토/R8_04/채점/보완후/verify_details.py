from pathlib import Path
import json,hashlib,re
HERE=Path(__file__).resolve().parent
def js(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
audit=js(HERE/'direct_audit.json');rows=[]
for a in audit:
 run=Path(a['run']);db=run/'inputs/Phase00';out=run/'outputs';checks=[];findings=[]
 def ck(n,b,ev):checks.append({'name':n,'passed':bool(b),'evidence':ev})
 # Source/basis existence is separate from availability of the supplied index itself.
 table=db/'14_스킬재구성/현재상태_정정표.json';guidance=db/'14_스킬재구성/R8_현재사용안내.md'
 tablechecks=[]
 for r in js(table)['records']:
  links=[{'kind':'source',**r['source']}]+[{'kind':'basis',**b} for b in r['basis']]
  tablechecks.append({'id':r['id'],'links':[dict(x,exists=(db/x['path']).is_file(),actual_sha256=sha(db/x['path']) if (db/x['path']).is_file() else None) for x in links]})
 # Every structural/version CLI record is checked against raw bytes, not only report summaries.
 command_details=[]
 for p in sorted(out.glob('*.command.json'))+sorted(out.glob('*.execution.json')):
  d=js(p);argv=d.get('argv',d.get('args',[]));label=p.name.removesuffix('.command.json').removesuffix('.execution.json')
  sp=out/(label+'.stdout.txt');ep=out/(label+'.stderr.txt')
  if not sp.exists():continue
  if any('資料' in str(x) or '자료검증.py' in str(x) or 'R5_디자인적용검사.py' in str(x) or '판본대조.py' in str(x) for x in argv):
   res=js(sp);command_details.append({'file':p.name,'argv':argv,'exit':d.get('exit_code',d.get('exit')),'result':res,'stderr_bytes':ep.stat().st_size if ep.exists() else None})
 if a['case']==1:
  cp=js(out/'후보.json');target=js(db/'작업초안/연결설명_지식초안.json');original=js(out/'read__대상_변경전.json')
  ck('same ID separate history and branch preserved',target['records'][0]==original['records'][0] and target['records'][2]==original['records'][2] and target['document_version']==original['document_version'],{'id_versions':[(x['id'],x['version']) for x in target['records']]})
  ck('target actual candidate byte equality',(out/'후보.json').read_bytes()==(db/'작업초안/연결설명_지식초안.json').read_bytes(),sha(out/'후보.json'))
 if a['case']==9:
  w=[x for x in a['events'] if x['request']['op']=='write'];r4=out/'R4_후보.json';r5=out/'R5_후보.json';link=js(r5)['linked_r4_record'];part=out/'R5_실패시점.bytes'
  ck('R5 own version and actual R4 new hash',js(r4)['version']==js(r5)['version']=='0.1.1' and link['version']=='0.1.1' and link['sha256']==sha(r4)==w[0]['service_owned_written_sha256'],link)
  ck('R5 failed bytes exact candidate prefix',part.read_bytes()==r5.read_bytes()[:len(r5.read_bytes())//3] and sha(part)==w[1]['service_owned_written_sha256'],{'bytes':part.stat().st_size,'sha':sha(part)})
 # Do not confuse code enforcement with the agent's observed choice.
 guards={2:('실패복구.py','assert current[\'actual_current_sha256\']==owned==sha(raw)'),6:('run_io.py',"assert sha(current)==write['owned_written_sha256']"),9:('execute.py',"if not ownership.get(rel) or ownership[rel]!=current:"),11:('post_save.py','if owned and sha(current)==owned:')}
 if a['case'] in guards:
  f,needle=guards[a['case']];s=(out/f).read_text(encoding='utf-8-sig');ck('agent executable own byte guard preserved',needle in s,{'path':str(out/f),'guard':needle})
 if a['case']==8:findings.append({'kind':'guard_provenance_limit','text':'작업실행.py는 generic CLI wrapper이고 별도 실행 가능한 restore 소유 비교 assert가 보존되지 않음. 다만 실제 read(sequence5) 후 동일한 이전 owned SHA를 restore expected에 사용했고 transcript가 현재 read→후보소유 일치확인→restore 판단을 명시. 이 실제 관측 결정만 인정.'})
 if a['case']==5:findings.append({'kind':'guidance_lookup_gap','text':'transcript: 현재상태_정정표.json은 DB 루트에서 존재하지 않았다. DB직하 부재는 사실이나 안내가 가리키는14하위에는 존재. 좁은 guidance 변경에 상태 정정을 적용하지 않았으므로 정정 미적용 자체는 적절.'})
 if a['case']==6:findings.append({'kind':'guidance_lookup_gap','text':'결과/기록은 스킬이 안내한 현재상태 정정표를 루트에서 미제공이라고 보고.14하위 제공 파일의 확인 누락. 정정 미적용과 변경안전성은 별도.'})
 if a['case']==9:findings.append({'kind':'false_guidance_absence_claim','text':'결과.json current_guidance 및 execute.py report()는14하위 안내·정정표 모두 없음이라고 명시하나 fixture/current 실제 파일 모두 존재. source/basis 일부 미제공과 다른 오류.'})
 if a['case']==7:findings.append({'kind':'imprecise_status_label','text':'결과.json status=partial_write_external_change_preserved_postsave_validation_failed이지만 write는 정상 후보전체저장이고 partial_or_invalid_json=false. 실제 보고본문은 외부변경/미복구를 정확히 구분하므로 손상JSON을 숨긴 것은 아님.'})
 rows.append({'case':a['case'],'checks':checks,'guidance_files':{'guide_exists':guidance.is_file(),'guide_sha':sha(guidance),'table_exists':table.is_file(),'table_sha':sha(table),'root_table_exists':(db/'현재상태_정정표.json').is_file()},'correction_source_basis':tablechecks,'structural_version_commands':command_details,'findings':findings})
(HERE/'verified_details.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'case':r['case'],'checks':len(r['checks']),'failed':[x for x in r['checks'] if not x['passed']],'findings':r['findings']} for r in rows],ensure_ascii=False,indent=2))
