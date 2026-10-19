from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];o=r/'outputs';p=o/'result.json';d=json.loads(p.read_text(encoding='utf-8'))
d['preserved_candidates']=[{'path':str(o/'R4_candidate.json'),'state':'검사·실제 반영한 후보 bytes의 보존 사본; 활성 초안은 inputs/Phase00 대상 파일'},{'path':str(o/'R5_candidate.json'),'state':'검사·실제 반영한 후보 bytes의 보존 사본; 활성 초안은 inputs/Phase00 대상 파일'}]
d['temporary_or_partial_files_remaining']=[]
d['preexisting_error']={'record':'R4','exit_code':1,'errors':['TG-STATE: 참조 버전/hash 불일치'],'resolved_by_requested_edit':True}
d['post_save_failure']=None
d['final_review_queue_counts']={'R4':27,'R5':7}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (r/'transcript.md').open('a',encoding='utf-8') as f:
 f.write('\n후속 결과 확인: 변경 전 R4 exit 1의 원인은 TG-STATE 참조 버전/hash 불일치 1건이며 요청 정정 후 해소. 실제 저장/최종 검사 실패는 없고 복구는 필요하지 않았습니다. 최종 R4/R5 valid=true, 기록별 판본 대조 exit 0, R4/R5 연결 SHA 일치. 최종 검사 대기열은 R4 27건·R5 7건이며 검수 상태를 변경하지 않았습니다. JSON 필드 차이는 R4 2곳·R5 3곳뿐이고 나머지 입력 파일 268개 해시 보존을 확인했습니다. R4_candidate.json/R5_candidate.json은 적용 bytes의 보존 사본입니다. 남은 임시/부분 파일 없음.\n')
print('result/transcript supplemented')
