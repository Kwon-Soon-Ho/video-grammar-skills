"""First observations of two newly selected company-video windows, authored by AI."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
HERE=Path(__file__).resolve().parent;TASK=HERE.parent
sys.path.insert(0,str(TASK/'candidate/company-video-grammar-analyzer/scripts'))
from check_record import check,load,digest,PROPERTIES
from evidence_catalog import catalog
from render_observations import render
def save(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);assert not path.exists(),path
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
class Case:
    def __init__(self,aid,start,end,ratio):
        self.aid=aid;self.start=start;self.end=end;self.out=HERE/'results'/aid
        item=next(m for m in load(HERE/'manifest.json') if m['id']==aid)
        log=HERE/'cases'/aid/'window/실행기록.json'
        crops=[c for c in load(HERE/'crop-inputs.json') if ('/'+aid+'/') in c['parent_path'].replace('\\','/')]
        self.cat=catalog([log],crops);save(self.out/'catalog.json',self.cat)
        frames=load(log)['frames'];self.lookup={F(f['actual_playback_seconds']):f'f{i:02d}' for i,f in enumerate(frames)}
        evidence=[{'id':self.lookup[F(f['actual_playback_seconds'])],'path':f['path'],'actual_seconds':f['actual_playback_seconds'],'role':'context_after' if F(f['actual_playback_seconds'])>=end else 'within'} for f in frames]
        self.d={'schema_version':'video-observation-0.4','skill_version':'0.1.0-draft.7','case_id':'DEV-'+aid+'-FIRST-20261019','source':{'path':item['path'],'sha256':item['sha256']},'window_seconds':[start,end],'method':'사전에 고정한 새 사내 영상 구간을 0.5초 간격 표본 17장으로 추출. 개요 시트를 시간순·정착 상태 역추적으로 확인하고 선택 native 및 검증된 좌우 분할을 대조했다. 기존 정답/원고는 읽지 않음. 동일 AI 개발 실행, 독립 평가 아님. 끝 경계 프레임은 문맥 근거.','document_mode':'none','audio_reviewed':False,'files_read':[str(log),str(HERE/'selection-plan.json')],'evidence':evidence,'objects':[],'observation_rows':[],'claims':[],'unknowns':[],'discovery':{'forward_evidence_ids':[e['id'] for e in evidence],'reverse_evidence_ids':[e['id'] for e in reversed(evidence)],'unresolved_ids':[]},'layout':{'canvas':{'aspect_ratio':ratio,'coordinate_system':'native raster, 전체 좌표와 하위 영역을 구분. 정확 픽셀 미측정'},'states':[],'unresolved_ids':[]},'motion_groups':[],'pattern_refs':[],'reuse_map':None,'review':{'content_reviewed_claim_ids':[],'claim_denominator_complete':False,'remaining_scope':['동일 AI의 첫 관측. 독립 정답·전수 주장 채점·미발견 요소 분모 없음.']},'handoff':None,'limitations':['정확한 글꼴·색·좌표·키프레임·이징·주기·제작 의도는 미확정.','0.5초 간격 표본 사이 사건·가림·미세 변화가 남을 수 있음.','화면 속 홍보 문구의 기술적·정책적 사실성을 검증한 것이 아님.','선택 표본을 통한 전체 디자인의 정성 기록이며 모든 속성의 연속 측정은 아님.']}
    def refs(self,times):return [self.lookup[F(str(t))] for t in times]
    def target(self,oid,name,shape,props,anchor,parent=None):
        self.d['objects'].append({'id':oid,'name':name,'parent':parent,'shape_description':shape,'required_properties':['identity',*props],'excluded_properties':{p:'별도 변화가 관측된 속성으로 채택하지 않음. 정성 외관은 전체 디자인·형태 설명에 보존하며 미발견 변화가 없다는 판정은 아님.' for p in PROPERTIES-{'identity',*props}},'identity':{'status':'reviewed','label':name,'candidates':[],'claim_ids':[]}})
        cid=self.claim(oid,'identity','identity','visible-form','구간 안에서 관측된 형태: '+shape,[anchor]);self.d['objects'][-1]['identity']['claim_ids']=[cid]
    def claim(self,oid,prop,facet,dim,text,times):
        cid=f'c{len(self.d["claims"])+1:03d}';self.d['claims'].append({'id':cid,'object_id':oid,'property':prop,'facet':facet,'dimension':dim,'time_seconds':[self.start,self.end],'statement':text,'basis_kind':'observed','evidence_ids':self.refs(times),'content_review':'supported'});return cid
    def unknown(self,oid,text,reason):
        uid=f'u{len(self.d["unknowns"])+1:02d}';self.d['unknowns'].append({'id':uid,'object_id':oid,'question':text,'state':'open','reason':reason,'required_basis_kind':'observed','next_probe':'사용 목적에 필요한 부분의 native ROI·시간 표본을 보강하고, 구현값이 필요하면 원본 프로젝트 확인','resolution_claim_ids':[]})
    def finish(self,states,design,flow,detail):
        for obj in self.d['objects']:
            for prop in obj['required_properties']:
                cs=[c for c in self.d['claims'] if c['object_id']==obj['id'] and c['property']==prop];assert cs,(obj['id'],prop)
                self.d['observation_rows'].append({'id':obj['id']+'-'+prop,'object_id':obj['id'],'property':prop,'time_seconds':[self.start,self.end],'review_state':'reviewed','change':'changed' if any(c['facet'] in ('direction','order') for c in cs) else 'unchanged','evidence_ids':sorted({e for c in cs for e in c['evidence_ids']}),'claim_ids':[c['id'] for c in cs],'unknown_ids':[],'reason':'선택 표본에서 확인한 상태·변화. identity 행은 구간 중 출현한 대상의 식별이며 연속 가시성을 뜻하지 않음.'})
        for sid,t,description in states:
            self.d['layout']['states'].append({'id':sid,'time_seconds':[self.start,self.end],'evidence_ids':self.refs([t]),'composition':description,'element_object_ids':[o['id'] for o in self.d['objects']],'claim_ids':[c['id'] for c in self.d['claims']],'design_spec':{k:{'description':v,'basis_kind':'observed','precision':'qualitative','claim_ids':[c['id'] for c in self.d['claims']]} for k,v in design.items()},'unresolved_ids':[u['id'] for u in self.d['unknowns']]})
        self.d['layout']['unresolved_ids']=[u['id'] for u in self.d['unknowns']]
        self.d['motion_groups']=[{'id':'flow','level':'flow','name':flow,'time_seconds':[self.start,self.end],'object_ids':[o['id'] for o in self.d['objects']],'claim_ids':[c['id'] for c in self.d['claims'] if c['property'] in ('visibility','position','size','internal_state')],'pattern_occurrence_ids':[]},{'id':'detail','level':'detail','name':detail,'time_seconds':[self.start,self.end],'object_ids':[o['id'] for o in self.d['objects']],'claim_ids':[c['id'] for c in self.d['claims'] if c['property']!='identity'],'pattern_occurrence_ids':[]}]
        self.d['review']['content_reviewed_claim_ids']=[c['id'] for c in self.d['claims']]
        errors=check(self.d,self.cat);assert not errors,errors
        path=self.out/'first-observations.json';save(path,self.d)
        (self.out/'first-observations.md').write_text(render(self.d),encoding='utf-8')
        save(self.out/'first-seal.json',{'observation_sha256':digest(path),'claims':len(self.d['claims']),'objects':len(self.d['objects']),'structure_and_provenance_passed':True,'content_truth_verified_by_code':False,'fresh_selected_window':True,'independent_or_blind_evaluation':False,'overall_accuracy':None,'notes':'처음 작성한 결과를 그대로 보존. 후속 재관찰·오류가 있으면 별도 판본으로 기록.'})
        print(json.dumps({'case':self.aid,'claims':len(self.d['claims']),'objects':len(self.d['objects']),'first_preserved':True},ensure_ascii=False))

n=Case('NEW-N',166,174,'32:9 (7680x2160)')
n.target('background','초광폭 기술 배경','어두운 남청색 바탕, 좌측 점·망사와 하단 곡선·작은 광점',['color'],166)
n.claim('background','color','value','palette','두 영역에 남청색·청색 빛과 낮은 대비의 선·점이 이어지고 흰 구조물·청록 강조가 대비된다.',[166,170])
n.target('header','좌상단 한맥 로고·섹션 리본','흰 로고 칸과 파란 사선 리본·흰 한글',['text'],170)
n.claim('header','text','value','section','3. 노듈러거더 핵심기술',[170])
n.target('girder','왼쪽 긴 거더 구조','구멍과 철근이 있는 회색 장대 구조물, 앞쪽 단면과 뒤로 이어지는 반복 부재',['position','size'],170)
n.claim('girder','position','direction','screen-view','166초에는 구조물이 왼쪽 아래부터 위쪽으로 크게 뻗고 167~167.5초 앞 단면이 더 드러나는 대각 구도로 정리된다. 171~171.5초에는 구조물의 기울어진 시점도 변한다. 카메라와 물체 변환의 기여는 분리 확정하지 않는다.',[166,167,167.5,171,171.5])
n.claim('girder','size','direction','projected-extent','166초 화면 경계를 벗어나는 구조물에서 167.5초 전면과 길이 방향이 함께 보이는 범위로 바뀐다. 실제 모델 스케일 변경으로 단정하지 않는다.',[166,167,167.5])
n.target('deck','구조물 위 흰 상판 조각','검은 고리 모양 철근을 가진 흰 판들이 길이 방향으로 반복',['position','internal_state'],167,'girder')
n.claim('deck','position','direction','assembly','167초 일부 흰 판이 구조물 위쪽에 분리되어 떠 있는 단계가 보이고 167.5~168초에는 긴 구조물 위를 더 연속으로 덮는 상태가 된다. 정확 이동 곡선·각 판 순서는 미확정.',[166.5,167,167.5,168])
n.claim('deck','internal_state','value','open-versus-covered','166초 위쪽 안쪽이 열린 거더와 뒤 표본의 흰 판이 덮인 거더를 구분한다. 화면 전체 축소만으로 내부 변화 설명을 대체하지 않는다.',[166,167,168])
n.target('front-arcs','왼쪽 거더 앞 단면 주변 청록 곡선 화살표','앞 단면 좌우에 위·아래 화살촉을 가진 굵은 청록 곡선',['visibility','shape'],170,'girder')
n.claim('front-arcs','visibility','direction','draw-and-fade','169초 희미한 곡선이 보이고 169.5~170초 더 선명해진다. 173.5초에는 같은 앞 단면의 화살표가 약해져 있다. 정확 점멸 주기는 미확정.',[168.5,169,169.5,170,173.5])
n.claim('front-arcs','shape','value','paired-arcs','앞 단면 좌우를 감싸는 두 곡선에 양끝 화살촉이 있다. 회전 의미를 암시하지만 실제 힘이나 물체 운동의 물리량은 판정하지 않는다.',[170])
n.target('rear-arcs','왼쪽 거더 먼 끝의 작은 화살표','긴 구조물 뒤쪽 끝 부근에도 작게 보이는 청록 곡선 한 쌍',['visibility'],170,'girder')
n.claim('rear-arcs','visibility','presence','far-end-effect','170초 원본 좌측 영역에는 앞 단면뿐 아니라 먼 뒤쪽 끝에도 작은 청록 곡선·화살표가 보인다. 앞쪽 효과와 별도 대상으로 연결한다.',[170,173.5])
n.target('section','오른쪽 단면 도해','중앙 검은 구멍과 둥근 홈, 위로 넓은 회색 단면',['visibility','position'],170)
n.claim('section','visibility','order','enter','167.5초에는 오른쪽 도해가 아직 뚜렷하지 않고 168초 오른쪽 중앙 아래에 작은 단면이 보인다. 168.5초 이후 단면과 상단 설명이 함께 자리 잡는다.',[167.5,168,168.5,170])
n.claim('section','position','direction','tilt','170초에 비해 171.5초 단면 상단이 오른쪽 위로 기울어져 보이고 172.5초 다시 더 수평에 가까워 보인다. 반복 여부·정확 각도는 미측정.',[170,171.5,172.5])
n.target('section-arcs','오른쪽 단면 청록 곡선 화살표','오른쪽 단면 좌우를 감싸는 굵은 곡선과 양끝 화살촉',['visibility','shape'],170,'section')
n.claim('section-arcs','visibility','direction','enter','168.5초에는 오른쪽 단면 주변 곡선이 뚜렷하지 않고 169초 일부가 보이며 169.5~170초 더 선명하다.',[168.5,169,169.5,170])
n.claim('section-arcs','shape','value','paired-arcs','오른쪽 단면의 좌우에 각각 양끝 화살촉이 달린 청록 호가 있어 좌측 큰 구조물의 강조와 대응한다.',[170])
n.target('right-label','오른쪽 설명 띠와 글자','짙은 반투명 가로 띠, 양끝 청록 세로선, 흰 한글',['text','visibility','size'],170)
n.claim('right-label','text','value','headline','횡방향보강으로 단면 안정성 향상',[170])
n.claim('right-label','visibility','order','reveal','167.5초 짧은 청록 세로선, 168초 가까운 두 선, 168.5초 부분적으로 읽히는 문구, 169~170초 넓은 설명 띠의 순서가 보인다.',[167.5,168,168.5,169,170])
n.claim('right-label','size','direction','width','167.5~169초 양끝 청록선 사이의 가로로 보이는 범위가 커진다. 실제 폭·마스크·다른 리빌 구현 중 무엇인지는 미확정.',[167.5,168,168.5,169])
n.target('left-label','후반 왼쪽 설명 띠','왼쪽 모델 위쪽에 새로 생기는 청록 양끝선·어두운 띠와 문구',['visibility','text'],173.5)
n.claim('left-label','visibility','direction','late-enter','173초 작은 세로선 뒤 173.5초 부분 글자가 있는 띠가 나타난다. 174초 경계 표본은 더 읽히는 문맥이며 구간 밖 완성 과정을 관찰했다고 쓰지 않는다.',[173,173.5,174])
n.claim('left-label','text','value','boundary-copy','174초 경계 문맥에서 캔틸레버 바닥판 시공시 동바리 역할 수행이라는 문구가 읽힌다. 분석 창 안 173.5초에는 아직 부분 판독 상태다.',[173.5,174])
n.target('caption','화면 하단 공통 자막','초광폭 중앙 아래의 짙은 청색 바탕과 흰 한글',['text','visibility'],166)
n.claim('caption','text','value','copy-before','166~167초: 하부 바닥판을 타설하는 습식연결 방식을 가능하게 하는 구성요소이며,',[166,167])
n.claim('caption','text','value','copy-middle','167.5초 이후: 단면의 안정성을 높이는 횡방향 보강격벽이자,',[168.5,170])
n.claim('caption','visibility','order','copy-change','167~167.5초 사이 자막 내용이 바뀐다. 174초 끝 문맥에는 다음 문장으로 교체되므로 전체 영상의 최종 자막이라고 쓰지 않는다.',[167,167.5,173.5,174])
n.unknown('background','배경의 작은 점·선·빛에 독립적인 변화가 있는가?','선택 개요로 외관을 기록했지만 배경 미세 변화는 연속 관찰하지 않음')
n.unknown('front-arcs','화살표의 정확 주기·가감속과 앞뒤 강조의 동기화는?','존재·차이는 보았지만 각 효과를 연속 추적하지 않음')
n.unknown('left-label','왼쪽 설명의 완성 이후 전체 상태와 정확 리빌 방식은?','분석 창 끝에서 등장 중이며 끝 이후 표본은 문맥 1장뿐임')
n.finish([('wide-composite',170,'7680x2160 전체를 하나의 배경으로 사용하되 왼쪽에는 길이 방향 구조, 오른쪽에는 단면·설명을 병렬 배치. 로고 리본은 좌상단, 공통 자막은 전체 중앙 아래. 후반 왼쪽 설명은 기존 오른쪽 설명과 별개로 추가된다.')],{'hierarchy':'좌상단 섹션 표제 → 왼쪽 큰 3D 구조와 오른쪽 단면 → 청록 강조·짧은 설명 → 하단 자막.','alignment':'두 주 콘텐츠는 초광폭의 서로 다른 영역에 배치하고 설명은 각각의 도해 위에 맞춘다.','spacing':'구조물이 대각으로 깊이를 만들고 두 도해 사이에 어두운 여백을 남긴다. 자막은 두 영역 아래 중앙을 잇는다.','typography':'흰 산세리프 한글. 섹션 리본, 도해 설명, 공통 자막의 크기·배경 역할이 다르며 정확 서체·크기 미측정.','color':'남청·청색 배경, 흰/회색 콘크리트·검은 안쪽, 청록 화살표·세로선.','background':'점·선 망과 곡선·푸른 빛이 이어지는 넓은 기술 배경. 미세 배경 모션은 미해결.','shapes':'사선 리본, 단면 구멍과 돌출 날개·철근, 양끝 화살촉 곡선, 세로선 양끝의 설명 띠와 사각 자막.'},'긴 거더 시점·상판 조립 → 오른쪽 단면·설명 등장 → 두 영역 화살표 강조·기울기 → 왼쪽 새 설명 시작','앞·먼 끝·오른쪽 화살표 분리, 단면과 시점 변화 구분, 설명 띠의 중간 상태·자막 교체')

p=Case('NEW-P',40,48,'16:9 (3840x2160)')
p.target('map','지역 지도 배경','어두운 위성 지형, 경계선과 회색 지명, 오른쪽 바다',['size'],40)
p.claim('map','size','direction','global-framing','40초와 48초 사이 지도와 기존 기관·설명 묶음의 보이는 크기·배치가 소폭 달라져 전체 구도가 넓어지는 듯하다. 정확 공통 카메라·부모 스케일 변환은 미확정이며 모든 카드가 고정이라고 단정하지 않는다.',[40,43,48])
p.target('region','횡성 강조 영역','청록색 면과 밝은 외곽·흰 횡성 글자',['text','color'],40,'map')
p.claim('region','text','value','label','횡성',[40,43,47])
p.claim('region','color','value','highlight','어두운 지도 안에서 횡성 영역을 청록색 채움과 밝은 외곽으로 강조한다. 이 색은 정책·기관 설명의 노랑/분홍과 별도다.',[40,43,47])
p.target('police','왼쪽 경찰청 로고 카드','노란 독수리 문양·파란 경찰청 글자, 밝은 사각 면과 가는 모서리 선',['text','visibility'],40)
p.claim('police','text','value','agency','경찰청',[40,43])
p.claim('police','visibility','presence','already-present','40초 구간 시작부터 왼쪽 기관 카드와 위 설명 패널이 보인다. 이 구간만으로 최초 등장 과정을 기록하지 않는다.',[40,43,47])
p.target('policy-panel','왼쪽 정책 설명 패널','노랑·연두 가로 화살촉 띠 두 줄, 반투명 사각 면과 바깥 모서리 선',['text','color'],40)
p.claim('policy-panel','text','value','policy-1','자율주행자동차 운행 안전관리를 위한 도로교통법 개정 추진',[40,43])
p.claim('policy-panel','text','value','policy-2','완전 자율주행시대에 대비한 도로교통안전 추진 전략 수립',[40,43])
p.claim('policy-panel','color','value','row-emphasis','노랑·연두 띠의 밝기와 테두리 강도가 선택 시점에서 달라 보인다. 정확 반복 주기·행별 동기화는 미확정.',[40,43,47])
p.target('police-link','왼쪽 연결선','기관 카드와 위 패널을 잇는 가는 노란 세로선·반복 화살 모양과 원형 접점',['relation'],43)
p.claim('police-link','relation','relation','card-panel-link','경찰청 카드 위쪽에서 노란 연결선이 설명 패널 아래 접점으로 이어져 카드와 위 두 문구의 소속 관계를 시각적으로 묶는다.',[43,47])
p.target('gangwon','중앙 강원특별자치도 카드','분홍·회색 로고 글자와 밝은 사각 면·모서리 선',['text','visibility'],43)
p.claim('gangwon','text','value','agency','강원특별자치도',[43,47])
p.claim('gangwon','visibility','order','logo-assembly','41.5~42초 작은 일부 로고가 보이고 42.5초 좁은 밝은 면과 글자, 43초에는 가로로 펼쳐진 기관 카드가 보인다. 정확 문자별·면별 리빌 방식은 미확정.',[41,41.5,42,42.5,43])
p.target('regional-frame','오른쪽 지역 설명 프레임','분홍 가는 외곽 모서리, 반투명 사각 면과 붉은 가로 띠',['visibility','size'],43)
p.claim('regional-frame','visibility','order','frame-enter','43초 위쪽에 좁고 세로로 긴 반투명 면과 빈 붉은 띠가 보이고 43.5~44초 가로 폭과 첫 줄 문구가 갖춰진다.',[42.5,43,43.5,44])
p.claim('regional-frame','size','direction','frame-width','43초의 좁은 배경 프레임이 44초 더 넓은 사각 범위로 보인다. 실제 레이어 폭·회전·마스크 중 무엇인지는 미확정.',[43,43.5,44])
p.target('regional-row1','지역 설명 첫 줄','붉은 가로 화살촉 띠와 흰 한글',['text','visibility','color'],47,'regional-frame')
p.claim('regional-row1','text','value','copy','강원특별자치도 미래산업글로벌도시 조성',[43.5,47])
p.claim('regional-row1','visibility','order','copy-after-band','43초 빈 붉은 띠 뒤 43.5초 첫 줄 글자가 읽힌다. 배경 면과 글자 완료를 같은 사건으로 뭉치지 않는다.',[43,43.5,44])
p.claim('regional-row1','color','value','red-to-pink','첫 줄 띠는 43초 어둡게 보이다 44~44.5초 더 밝은 분홍 강조가 보이고 47초에는 두 번째 줄보다 어둡다.',[43,44,44.5,47])
p.target('regional-row2','지역 설명 둘째 줄','첫 줄 아래의 분홍 가로 화살촉 띠와 흰 한글',['text','visibility','color'],47,'regional-frame')
p.claim('regional-row2','text','value','copy','미래차 전체 주기 기업지원 생태계 구축',[47,48])
p.claim('regional-row2','visibility','order','second-row-enter','46초에는 첫 줄만 있고 46.5초 둘째 줄의 어두운 띠가 나타나며 47초 문구가 읽힌다. 첫 줄 등장 뒤 두 번째 줄을 추가한다.',[46,46.5,47])
p.claim('regional-row2','color','value','emphasis','47초와 48초 둘째 줄은 첫 줄보다 밝은 분홍으로 강조돼 있다. 행별 강조의 전체 주기는 이 구간만으로 확정하지 않는다.',[47,48])
p.target('regional-link','지역 기관과 설명 연결선','분홍 세로 화살 모양 선·흰 원형 접점',['visibility','relation'],43)
p.claim('regional-link','visibility','presence','visible','43초 이후 중앙 기관 카드에서 위 프레임으로 이어지는 분홍 연결선이 보인다. 선 내부 무늬의 이동 방향은 연속 확인하지 않았다.',[43,47])
p.claim('regional-link','relation','relation','agency-panel-link','분홍 기관 카드와 위 붉은 설명 프레임을 연결한다. 노란 경찰청 설명과 구분되는 소속 묶음이다.',[43,47])
p.target('caption','하단 진행 자막','검은 반투명 가로 면, 회색 문구 중 일부가 흰색으로 밝아짐',['text','color','visibility'],40)
for dim,text,times in [('copy-1','교통사고로부터 안전한 국민의 일상을 만들어가고 있습니다',[40]),('copy-2','강원특별자치도는 5대 첨단산업 클러스터를 조성하여',[43]),('copy-3','전기차, 자율주행차 등 첨단산업의 활성화를 추진하고 있습니다',[48])]:p.claim('caption','text','value',dim,text,times)
p.claim('caption','visibility','order','copy-changes','41.5~42초 사이 첫 문구에서 두 번째로, 46~46.5초 사이 두 번째에서 세 번째로 교체되는 표본이 보인다.',[41.5,42,46,46.5])
p.claim('caption','color','direction','progressive-brightening','42.5초 두 번째 문구의 왼쪽 부분이 더 밝고 뒤는 어두우며 뒤 시점에는 밝은 구간이 늘어난다. 47초 세 번째 문구의 앞부분이 밝고 뒤는 어둡지만 48초 경계에는 더 넓게 밝다. 음성을 듣지 않아 발화와 싱크한다고 판정하지 않는다.',[42.5,43,45,47,48])
p.unknown('map','지도·카드 구도의 공통 변환과 개별 요소의 이동을 어떻게 분리할까?','선택 표본에서 구도 차이는 보이나 같은 기준점의 좌표 추적은 미실행')
p.unknown('regional-link','연결선 내부 화살 무늬가 어느 방향으로 움직이는가?','무늬와 접점은 보이지만 대표 표본만으로 이동 방향을 확정하지 않음')
p.unknown('policy-panel','행별 강조의 정확 주기와 지역 패널 강조와의 동기화는?','강약은 관측했지만 전체 주기·파형은 측정하지 않음')
p.finish([('map-composite',47,'어두운 지형·행정 경계 위 왼쪽 노랑 경찰청 설명 묶음과 중앙 위 분홍 지역 설명 묶음. 횡성은 아래 중앙 청록 강조, 바다는 오른쪽 여백. 하단 검은 자막은 두 설명과 별도.')],{'hierarchy':'지역 지도·횡성 강조를 배경 맥락으로 두고 기관 카드와 연결된 정책 설명을 위에 겹친다. 아래 자막은 별도 정보층.','alignment':'기관별 카드 → 세로 연결선 → 위쪽 설명 프레임. 두 기관 묶음을 나란히 배치하고 각 프레임 안 가로 문구 띠를 수직으로 쌓는다.','spacing':'지도와 지명을 일부 보이게 둔 반투명 패널, 오른쪽 바다의 넓은 여백, 아래 자막과 횡성 강조 사이 간격.','typography':'카드의 기관 로고 서체와 설명·자막의 한글 산세리프를 구분한다. 지도 지명은 어둡고 외곽이 있으며 정확 글꼴·크기 미측정.','color':'어두운 녹갈색 지도·짙은 남청 바다, 횡성 청록, 경찰청 노랑/연두, 지역 설명 붉은색/분홍, 밝은 로고 카드.','background':'위성 지형 질감과 행정 경계·지명. 정보 프레임은 반투명해 지도가 일부 비친다.','shapes':'화살촉 양끝 문구 띠, 직사각 반투명 면, 가는 모서리·프레임, 세로 화살 무늬·원형 접점, 지역 경계 면과 검은 자막 바.'},'기존 경찰청 묶음·횡성 지도 유지 → 지역 로고 카드 전개 → 위 프레임·첫 줄 → 둘째 줄과 강조 → 자막 교체·밝기 진행','기관별 프레임·글자·연결선 분리, 첫째·둘째 줄 순서와 강조 강약, 자막 내용과 밝기 진행 구분')
