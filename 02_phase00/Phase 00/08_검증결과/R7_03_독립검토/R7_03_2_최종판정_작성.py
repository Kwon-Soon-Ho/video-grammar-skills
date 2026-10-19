import json,hashlib
from pathlib import Path
B=Path(r'D:\00작업\2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증\Phase 00');O=Path(__file__).parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
a=read(O/'R7_03_2_최종_원문대조.json');assert a['all_static_checks_passed'] and a['synthetic_arithmetic_sanity']['passed']==11 and all(sha(B/r)==h for r,h in a['after_hashes'].items())
f=read(O/'R7_03_2_초기_발견사항.json');d=read(B/'13_품질검수/평가계획/지표정의_정본.json');fixes=[]
for x in f['findings']:
 x['status']='fixed';fixes.append(x)
files=['R7_03_2_독립감사.py','R7_03_2_최종_원문대조.json','R7_03_2_초기_발견사항.json','R7_03_2_공개원문_독립대조.json','R7_03_2_초기후보/13_품질검수/평가계획/지표정의_정본.json']
v={'stage':'R7-3-2 지표·분모/보류·미채점 계획','limited_completion_supported':True,'unresolved_blocking_findings':[],'scope':{'included':['R_A/H/U/N과D/A/X/M/F의평가단위/배타분모·null/조건부위험·전체진단','R_H단위기준위반/보류·추출발생/다중집합·중복/파싱실패·시간오차/군집조건의정적설계','110원문/backup·현재R6연결과수치예의독립산술검산'],'excluded':['실제채점기/매칭알고리즘/평가실행·모델·미디어·사람정답/판정','표본/임계값·신뢰구간방법·모집단효과/우월성확정','R7-3-3사람불일치/중재/재시험,R7-4,R8,01-A,전체Phase00완료']},'verification':{'static_review':{'total':a['total'],'passed':a['passed']},'separate_arithmetic_sanity':a['synthetic_arithmetic_sanity'],'counts_are_not_model_trials_or_quality_performance':True,'protected_current_backup_files':110,'source_unchanged':a['checks']['source_unchanged'],'current_R6_query_valid':a['current_R6_query']['valid']},'findings_fixed':fixes,'corrected_definition_evidence':{'version':d['version'],'reference_partition':d['reference_partition'],'invalid_output_policy':d['invalid_output_policy'],'hold_policy':d['hold_policy'],'R_H_rate_unit':d['R_H_rate_unit'],'extraction_multiplicity_policy':d['extraction_multiplicity_policy']},'independent_primary_reading':read(O/'R7_03_2_공개원문_독립대조.json'),'remaining_human_gate':'보류적절성·골드상태·적용성은실제근거로사람검수. 현재입력/답안/시행없음,비율/합격조건수치는예비후별도검토.','actual_human_content_review_performed':False,'actual_evaluator_implemented':False,'actual_model_trials':0,'actual_scores':None,'company_approved':False,'permission_granted':False,'R7_3_complete':False,'Phase00_complete':False,'evidence':[{'path':str(O/x),'sha256':sha(O/x)} for x in files],'after_hashes':a['after_hashes'],'after_hashes_note':'최종재검토초안의시점스냅샷.후속메타/보고/안내변경은별도검증.'}
(O/'R7_03_2_최종판정.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# R7-3-2 독립 검토 판정

**지표·분모/보류·미채점의 설계 범위로 완료를 지지합니다. 차단사항은 없습니다.**

정적35/35와별도설계산술11/11을확인했습니다.110원문·backup일치,R6현재조회정상,검토중원문불변입니다. 문서/산술검산이며채점기·모델·실영상성능시험수가아닙니다.

R_H1항목의다중단정을단위당0/1위반률과별도단정건수로분리하고,올바른보류와근거없는단정혼재는보류성공0으로보완했습니다. 기준4집합의완전분할과모순최종결론F1회처리,출력발생ID목록/다중집합과중복FP·매칭/동률규칙을명시했습니다. A상태는사유타당성과구분합니다.

0분모null,전체양성에보류/누락/실패유지,파싱실패시조건부정밀도한계,매칭된좌표오차와미매칭누락의구분,군집종속성·오류0의한계를확인했습니다. [Google 정의](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall), [선택적분류 논문2절](https://proceedings.neurips.cc/paper/7073-selective-classification-for-deep-neural-networks.pdf), [NIST 비율구간 해설](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm)의지정부분만직접대조했으며논문의보장/실험이나이항구간을이프로젝트에승계하지않았습니다.

실제사람채점·모델/영상·평가시행·임계값/신뢰구간선정은미실시입니다. R7-3-3이후및전체Phase00완료는포함하지않습니다. 초기후보/발견사항과최종근거는별도로보존했습니다.
'''
(O/'R7_03_2_최종판정.md').write_text(md,encoding='utf-8');print(json.dumps({'after_hash_count':len(a['after_hashes']),'hashes':{r:sha(O/r) for r in ['R7_03_2_최종판정.json','R7_03_2_최종판정.md','R7_03_2_최종_원문대조.json','R7_03_2_독립감사.py']}},ensure_ascii=True))
