from pathlib import Path
import json,csv,io,os,re,hashlib,collections
from urllib.parse import quote

W=Path(__file__).parent.resolve()
P=Path('D:/00작업/2026-10-02_AI 기반 영상 기획·제작 스킬 체계 개발 및 검증')
SRC=P/'한맥 영상';DEST=P/'Phase 01-A';STAGE=W/'생성본'
assert not STAGE.exists()
VIDEO={'.mp4','.mov','.m4v','.avi','.mkv','.wmv','.webm'}
DOC={'.ppt','.pptx','.doc','.docx','.hwp','.hwpx','.pdf','.xls','.xlsx','.txt','.md','.rtf'}
def inventory():
    data=[]
    for p in sorted(SRC.rglob('*'),key=lambda p:p.relative_to(SRC).as_posix().casefold()):
        if p.is_file():
            assert p.resolve().is_relative_to(SRC.resolve())
            s=p.stat();r=p.relative_to(SRC)
            data.append({'path':p.relative_to(P).as_posix(),'relative':r.as_posix(),'extension':p.suffix.lower(),'bytes':s.st_size,'mtime_ns':s.st_mtime_ns,'backup':any(t.casefold() in {'backup','백업'} for t in r.parts[:-1])})
    return data
items=inventory();byfolder=collections.defaultdict(list)
for i in items:byfolder[Path(i['relative']).parent.as_posix()].append(i)
groups=sorted([k for k,v in byfolder.items() if any(i['extension'] in VIDEO for i in v)],key=str.casefold)
files={};empty=[];links=[]
def put(rel,text):
    p=STAGE/rel;p.parent.mkdir(parents=True,exist_ok=True)
    b=text if isinstance(text,bytes) else text.encode('utf-8')
    with p.open('xb') as f:f.write(b)
    files[str(rel).replace('\\','/')]=hashlib.sha256(b).hexdigest()
def jput(rel,obj):put(rel,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def csvdata(headers,rows):
    s=io.StringIO(newline='');w=csv.writer(s);w.writerow(headers);w.writerows(rows)
    return s.getvalue().encode('utf-8-sig')
def link(label,docrel,target):
    rel=os.path.relpath(target,(DEST/docrel).parent).replace('\\','/')
    label=label.replace('[','\\[').replace(']','\\]')
    links.append({'doc':str(docrel).replace('\\','/'),'target':str(target)})
    return '['+label+']('+quote(rel,safe='/.:_-()')+')'

template='''# 영상 자료 설명

아는 항목만 적으세요. 모르면 미정, 자료가 없으면 없음으로 둡니다.

## 먼저 적을 여섯 가지

1. 프로젝트명 / 자료 ID:
2. 사용할 최종 영상의 파일명·위치: 미정
   - 최종 납품·배포본 확인: 미확인 / 확인됨
   - 영상이 여러 개면 사용할 파일 하나를 지정합니다. 각각 분석할 때는 별도 실행으로 구분합니다.
3. 대응 시나리오·콘티·기획서 파일명·버전: 미정
   - 영상과의 관계: 미확인 / 일치 / 일부 다름 / 없음
   - 여러 문서 중 먼저 볼 문서와 참고·수정 의견을 구분합니다. 원문을 영상에 맞춰 고치지 않습니다.
4. 영상 목적 / 볼 사람 / 시청 환경: 미정
5. 디자인 확인 담당 / 내용 확인 담당: 미정 (한 사람이 겸해도 됩니다)
6. 외부 AI·API 처리 범위: 확인 필요

| 파일·자료 범위 | 가능 / 불가 / 확인 필요 | 근거·확인 담당 |
|---|---|---|
| 선택한 영상 | 확인 필요 | 미정 |
| 선택한 시나리오·기획서 | 확인 필요 | 미정 |

개인 구독 AI나 API에 올려도 되는지는 자료별로 표시합니다. 이 표를 채워도 실제 분석·업로드를 시작하는 것은 아닙니다.

## 있으면 적는 내용

- 제작일·영상 버전·공개/승인 상태: 미정
- 보고 싶은 장면과 이유: 시간을 몰라도 “세 단계 도표가 나오는 부분”처럼 적으면 됩니다.
- 시나리오와 다른 부분 / 수정 의견:
- 내레이션·자막 파일 위치: 미정
- AE 등 프로젝트 원본·연결 자산 위치: 미정
- 정해진 회사·프로젝트 디자인 조건: 미정
- 원본 폴더를 옮겼다면 새 경로:

## 준비 단계의 범위

영상 FPS·시간표·해시·장면 캡처는 직접 만들지 않아도 됩니다. PPT·Word·한글·PDF·Excel·기획 이미지는 원래 이름과 형식 그대로 둡니다. 실제 읽기·변환 방식은 분석 착수 때 확인합니다. 지금은 영상 분석·OCR·전사·스킬 개발·외부 업로드를 하지 않습니다.
'''
put('00_진행안내/준비양식/자료설명_빈양식.md',template)
newbase=Path('00_진행안내/준비양식/신규영상_폴더양식')
put(newbase/'00_자료설명.md',template)
for d in ['01_최종영상','02_시나리오와기획서','03_내레이션과자막','04_프로젝트원본과자산','05_검수메모','06_회사디자인참고','backup']:
    empty.append((newbase/d).as_posix())
registry=[];table=[]
for n,g in enumerate(groups,1):
    gid=f'자료{n:03d}'
    slug=re.sub(r'[<>:"/\\|?*]','_',g).strip(' .')[:78]
    folder=Path('01_입력자료/01_기존자료_등록')/(gid+'_'+slug)
    doc=folder/'00_자료설명.md'
    same=byfolder[g];vids=[i for i in same if i['extension'] in VIDEO]
    docs=[i for i in same if i['extension'] in DOC]
    others=[i for i in same if i['extension'] not in VIDEO|DOC]
    ancestors=[]
    for parent in Path(g).parents:
        if parent.as_posix()=='.':break
        ancestors.extend(i for i in byfolder.get(parent.as_posix(),[]) if i['extension'] not in VIDEO)
    shared=[]
    family='00_26년 가족사 경영보고 영상'
    if g.startswith(family+'/') and Path(g).name!='00초기 기획서':
        shared.append(SRC/family/'00초기 기획서')
    t=f'''# {gid} 자료 설명: {g}

**파일 목록만 확인했습니다. 영상·문서 내용은 읽거나 분석하지 않았습니다.**

- 원본 폴더: {link('한맥 영상 / '+g,doc,SRC/g)}
- 보관 방식: 기존 원본 참조. 영상·기획서를 여기 다시 복사하지 않습니다.
- 사용할 최종 영상 / 대응 문서: 미정
- 최종본·문서 대응: 미확인
- 첫 시험·보정·잠금 표본 배정: 미정

'''
    if '초기' in Path(g).name:t+='폴더명에 “초기”가 있습니다. 이곳의 영상도 최종본으로 확정하지 않고 후보로 보존했습니다.\n\n'
    for heading,seq in [('같은 폴더의 영상 후보',vids),('같은 폴더의 기획·참고 문서 후보',docs),('같은 폴더의 이미지·기타 참고 후보',others)]:
        if not seq and '이미지' in heading:continue
        t+='## '+heading+'\n\n'
        if seq:
            t+='\n'.join('- '+link(Path(i['relative']).name,doc,P/i['path']) for i in seq)+'\n\n'
        else:t+='같은 폴더의 문서 파일 목록에서는 찾지 못했습니다. 다른 곳에 있으면 경로만 적고, 없으면 없음으로 두세요. 새 시나리오를 만들 필요는 없습니다.\n\n'
    if len(vids)>1:t+='영상이 여러 개입니다. 사용할 영상과 각 문서의 대응 관계를 표시해 주세요. 같은 폴더라는 이유로 모든 영상에 문서가 맞는다고 확정하지 않습니다.\n\n'
    if ancestors or shared:
        t+='## 상위·공유 자료 후보\n\n가까운 상위 폴더·공유 폴더의 참고 위치입니다. 이 영상에 맞는 문서인지는 미확인입니다.\n\n'
        t+='\n'.join('- '+link(Path(i['relative']).name,doc,P/i['path']) for i in ancestors)+'\n'
        t+='\n'.join('- '+link('가족사 초기 기획서 모음',doc,p) for p in shared)+'\n\n'
    t+='파일명의 최종·v4·날짜만으로 최종본이나 문서 대응을 확정하지 않았습니다. backup 안의 이전 파일은 전체 목록에 따로 표시했습니다.\n\n---\n\n'+template
    put(doc,t)
    put(folder/'01_원본목록.csv',csvdata(['프로젝트루트기준경로','분류','위치관계','확장자','크기_bytes','최종·대응확인'],[[i['path'],'영상 후보' if i['extension'] in VIDEO else '문서·참고 후보','같은 폴더' if i in same else '상위 공유 후보',i['extension'],i['bytes'],'미확인'] for i in same+ancestors]))
    ref={'id':gid,'unit':'folder_registration_not_analysis_run','source_folder':'한맥 영상/'+g,'video_candidates':[i['path'] for i in vids],'document_candidates':[i['path'] for i in docs],'other_candidates':[i['path'] for i in others],'ancestor_candidates':[i['path'] for i in ancestors],'shared_folders':[p.relative_to(P).as_posix() for p in shared],'selected_video':None,'selected_documents':None,'final_and_pairing_status':'unverified','external_ai_permission':'needs_confirmation','analysis_started':False}
    jput(folder/'02_자료참조.json',ref)
    r={'id':gid,'source_folder':g,'folder':folder.as_posix(),'video_count':len(vids),'document_count':len(docs),'initial_location':'초기' in Path(g).name}
    registry.append(r)
    flags=['최종·대응 미확인']
    if len(vids)>1:flags.append('여러 영상 중 선택')
    if not docs:flags.append('같은 폴더 문서 미발견')
    if r['initial_location']:flags.append('초기 폴더')
    table.append(f"| {gid} | {link(g,Path('01_입력자료/00_기존자료_등록목록.md'),DEST/doc)} | {len(vids)} | {len(docs)} | {' / '.join(flags)} |")
video_count=sum(r['video_count'] for r in registry)
stats={'source_files':len(items),'video_candidates':video_count,'video_folders':len(registry),'extensions':dict(collections.Counter(i['extension'] for i in items)),'video_bytes':sum(i['bytes'] for i in items if i['extension'] in VIDEO)}
put('01_입력자료/00_기존자료_등록목록.md',f'''# 기존 자료 등록목록

2026-10-16 파일 목록 기준: **영상 후보 {video_count}개 / 영상이 든 폴더 {len(registry)}묶음**.
파일명·폴더·크기만 확인했습니다. 폴더명을 누르면 원본 위치와 후보가 적힌 자료 설명을 엽니다. 최종본·문서 대응·첫 분석 대상은 미확정입니다.

| ID | 프로젝트 / 자료 설명 열기 | 영상 수 | 같은 폴더 문서 수 | 표시할 내용 |
|---|---|---|---|---|
'''+ '\n'.join(table)+'\n\n문서 수는 확장자에 따른 파일 수이며 정확히 대응하는 시나리오 수가 아닙니다. backup을 포함한 전체 파일 목록은 00_진행안내/03_기존자료_파일목록.csv에 있습니다.\n')
put('01_입력자료/00_기존자료_등록목록.csv',csvdata(['자료ID','원본폴더_한맥영상기준','등록폴더_Phase01A기준','영상후보수','문서후보수','선택최종영상','대응기획서','최종·대응확인','외부AI처리범위'],[[r['id'],r['source_folder'],r['folder'],r['video_count'],r['document_count'],'미정','미정','미확인','확인 필요'] for r in registry]))
put('00_진행안내/03_기존자료_파일목록.csv',csvdata(['프로젝트루트기준경로','확장자','크기_bytes','backup폴더여부','내용확인'],[[i['path'],i['extension'],i['bytes'],'예' if i['backup'] else '아니오','목록만 확인'] for i in items]))
jput('00_진행안내/03_기존자료_파일목록.json',{'date':'2026-10-16','scope':'filesystem metadata only, no contents parsed','files':items})
how='''# 영상·기획서를 어디에 두면 되나요?

## 이미 모은 자료

한맥 영상을 원본 보관소로 그대로 사용합니다. Phase 01-A/01_입력자료/01_기존자료_등록에는 원래 위치와 설명만 등록했습니다. 큰 영상을 다시 복사하거나 이름을 바꾸지 않아도 됩니다.

1. 01_입력자료/00_기존자료_등록목록.md에서 프로젝트를 고릅니다.
2. 그 자료의 00_자료설명.md에서 사용할 최종 영상 하나와 대응 시나리오·기획서를 지정합니다.
3. 목적·시청자·담당자·외부 AI 처리 범위를 아는 만큼 적습니다. 모르겠으면 미정입니다.

PPT·Word·한글·PDF·Excel·기획 이미지는 원래 이름·형식 그대로 둡니다. 지금 HWP를 변환하거나 PPT를 새로 작성할 필요는 없습니다. 영상과 문서가 여러 버전이어도 지우거나 합치지 말고 어느 버전이 짝인지 표시하면 됩니다.

## 새로 넣는 자료

기존 프로젝트의 추가 파일은 원래 프로젝트 폴더에 넣고 자료 설명에 새 경로를 적어도 됩니다. 등록목록은 현재 시점의 스냅샷이므로 이후 추가 파일은 목록 갱신이 필요합니다.

새 프로젝트라면 00_진행안내/준비양식/신규영상_폴더양식을 통째로 복사해 01_입력자료/02_새자료_접수/영상000_프로젝트명으로 이름을 바꿉니다.

- 00_자료설명.md: 여섯 가지 정보를 먼저 작성
- 01_최종영상: MP4/MOV 등 원래 영상
- 02_시나리오와기획서: PPT·Word·한글·PDF·Excel·기획 이미지
- 03_내레이션과자막: 있을 때만
- 04_프로젝트원본과자산: 선택, AE 등 원래 연결 경로 유지
- 05_검수메모 / 06_회사디자인참고: 있을 때만
- backup: 자료 설명·직접 수정한 새 문서의 이전 버전

## 지금 하지 않아도 되는 일

길이·FPS·해상도·타임코드·해시를 적거나 장면 캡처·OCR·전사·정답표를 만들 필요는 없습니다. 02_분석작업·03_분석스킬·04_검증자료는 예약 폴더입니다. 외부 AI/API 업로드도 아직 하지 않습니다.

## 아직 확인하지 않은 부분

같은 폴더에 있다는 사실만으로 최종본·맞는 시나리오라고 확정하지 않습니다. 초기 기획서 폴더의 영상, 센터 싱글/듀얼처럼 여러 영상이 있는 묶음, 같은 폴더에서 문서가 미발견된 홈페이지 영상은 설명에서 해당 부분만 확인하면 됩니다. 없으면 없음으로 둡니다.

현재는 폴더 단위 접수입니다. 실제 분석 때는 선택한 영상 하나씩 실행을 구분합니다. 최초 시험 대상·보정/잠금 표본은 아직 배정하지 않았습니다.
'''
put('00_진행안내/01_자료넣는방법.md',how)
put('00_진행안내/02_준비체크리스트.md','''# 준비 체크리스트

- [ ] 사용할 영상 하나를 지정했다. 최종본인지 모르면 미확인으로 두었다.
- [ ] 대응 시나리오·기획서 경로와 버전을 적었다. 없으면 없음으로 표시했다.
- [ ] 영상과 문서의 관계를 일치/일부 다름/미확인으로 표시했다.
- [ ] 목적·시청자·환경·확인 담당자를 아는 만큼 적었다.
- [ ] 영상과 문서의 외부 AI·API 처리 범위를 각각 적었다. 모르면 확인 필요다.

체크 완료는 자료 준비 완료이며 실제 분석·외부 업로드의 착수 지시가 아니다. 기술 정보·OCR·전사·장면별 정답표는 지금 작성하지 않아도 된다.
''')
put('01_입력자료/02_새자료_접수/00_추가하는방법.md','# 새 프로젝트 추가\n\n../../00_진행안내/준비양식/신규영상_폴더양식을 이곳에 복사해 이름을 바꿉니다. 이미 한맥 영상에 모은 프로젝트는 다시 옮기지 않고 기존자료 등록의 자료 설명만 채우면 됩니다.\n')
for f,label in [('02_분석작업','실제 영상 분석'),('03_분석스킬','영상 분석 스킬 개발'),('04_검증자료','평가·검증 자료')]:
    put(f+'/00_예약폴더_안내.md',f'# {label} 예약 폴더\n\n자료 준비만 진행했다. 프레임·전사·OCR·관측 기록·새 스킬·평가 정답은 만들지 않았다. 착수 지시 뒤 필요한 구조를 채운다. 보정·잠금 표본 배정도 미정이다.\n')
put('backup/00_보관안내.md','# 백업\n\n이번 구조·양식·목록의 생성 코드와 검토 이력을 날짜별로 보존한다. 원래 영상과 기획서는 한맥 영상에 그대로 두며 여기로 중복 복사하지 않는다.\n')
put('00_먼저읽기.md',f'''# Phase 01-A 자료 준비 - 여기부터 보세요

**폴더·자료 설명·목록만 준비했습니다. 실제 영상 분석과 스킬 개발은 시작하지 않았습니다.**

한맥 영상에서 파일 {len(items)}개와 영상 후보 {video_count}개를 목록으로 확인하고, 영상이 든 {len(registry)}개 폴더를 등록했습니다. 원본은 그대로 두었습니다. 최종본·대응 문서·첫 시험 대상은 미정입니다.

1. [기존 자료 등록목록](01_입력자료/00_기존자료_등록목록.md)에서 프로젝트를 고릅니다.
2. 해당 폴더의 00_자료설명.md에 최종 영상·대응 기획서 등 여섯 항목을 아는 만큼 적습니다.
3. 새 파일을 추가할 때는 [자료 넣는 방법](00_진행안내/01_자료넣는방법.md)을 봅니다.

이미 모은 영상·문서를 다시 옮기거나 변환할 필요는 없습니다. 같은 폴더의 후보를 적어 두었으니 이번에 사용할 버전만 표시하면 됩니다. 모르면 미정, 자료가 없으면 없음입니다.

## 폴더 구조

- 한맥 영상: 기존 실제 원본 보관소
- Phase 01-A/00_진행안내: 넣는 방법·빈 양식·전체 파일 목록
- Phase 01-A/01_입력자료/01_기존자료_등록: 원본 위치와 자료 설명만 등록
- Phase 01-A/01_입력자료/02_새자료_접수: 새 프로젝트를 추가할 때 사용
- Phase 01-A/02_분석작업: 예약, 현재 미실행
- Phase 01-A/03_분석스킬: 예약, 현재 미개발
- Phase 01-A/04_검증자료: 예약, 표본 미배정
- Phase 01-A/05_결과보고: 자료 준비 결과만
- Phase 01-A/backup: 생성 코드·검토 이력

[자료 설명 빈 양식](00_진행안내/준비양식/자료설명_빈양식.md) · [준비 체크리스트](00_진행안내/02_준비체크리스트.md)

Phase 00의 사전·기록 규격·한맥 디자인은 기존 정본을 참조한다. 여기 복사해 별도로 수정하지 않는다. 최신 세 관리용 스킬의 기본 전환 보류·소량 사본 사용 유지 결정도 그대로다.
''')
jput('00_진행안내/준비상태.json',{'date':'2026-10-16','preparation_only':True,'source_file_count':len(items),'video_candidates':video_count,'folder_groups':len(groups),'metadata_registration_complete':True,'final_versions_confirmed':False,'scenario_pairs_confirmed':False,'first_test_selected':False,'calibration_and_locked_samples_assigned':False,'analysis_started':False,'skill_development_started':False,'external_upload_performed':False,'default_skill_promotion':False})
manifest={'source_before':items,'stats':stats,'registry':registry,'files':files,'empty_folders':empty,'links':links,'scope':'names/extensions/sizes/mtime only; no file contents read; no media/doc analysis'}
with (W/'구성_명세.json').open('x',encoding='utf-8') as f:json.dump(manifest,f,ensure_ascii=False,indent=2)
assert inventory()==items
print(json.dumps(dict(stats,generated_files=len(files)),ensure_ascii=False))
