from pathlib import Path
import subprocess,json,sys
root=Path(__file__).resolve().parent
tests=[(["--relation","numeric-before-graphic"],["A-M3","B-M3"]),(["--concept","TIME-DELAY"],["A-M3","B-M3"]),(["--id","A-M3"],["A-M3"]),(["--id","LOCAL-FLOW-B-REVIEW-v1"],["B-M1","B-M2","B-M3"]),(["--principle","MR-08"],["A-M3","B-M3"]),(["--id","VC-MOTION-03"],[]),(["--id","VC-MOTION-03","--include-excluded"],[])]
runs=[]
for args,want in tests:
    call=[sys.executable,str(root/"query.py"),*args]
    cp=subprocess.run(call,capture_output=True,text=True,encoding="utf-8",env={**__import__("os").environ,"PYTHONIOENCODING":"utf-8"})
    if cp.returncode: raise RuntimeError(cp.stderr)
    result=json.loads(cp.stdout)
    assert result["ids"]==want,(args,result["ids"],want)
    for r in result["uses"]:
        assert Path(r["definition_source"]).exists()
        assert Path(r["evidence"]["sheet_path"]).exists()
        assert r["definition_version"]["source_sha256"]
        assert r["evidence"]["original_frames"]
        assert r["difference"] and r["unverified_dimensions"]
    runs.append({"command":subprocess.list2cmdline(call),"exit_code":cp.returncode,"result":result,"id_check":"matched expected explicit-filter IDs; not media truth validation"})
(root/"query-results.json").write_text(json.dumps(runs,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
md=["# 실제 조회 실행 결과","","2026-10-19. 아래 명령은 실제 실행했고 전체 반환은 query-results.json에 저장했다. 기대ID 확인은 조회 연결 검사이며 원본 내용/회사 승인/의미검색 성능 검증이 아니다.",""]
for run in runs:
    r=run["result"]
    md+=["~~~powershell",run["command"],"~~~","",f"종료코드 {run['exit_code']}; 관측 반환 {r['count']}건: {', '.join(r['ids']) or '없음'}."]
    if "excluded_proposals" in r: md += ["제외 제안 별도 반환: "+", ".join(x["id"]+" ("+x["status"]+")" for x in r["excluded_proposals"])]
    for use in r["uses"]:
        md += [f"- {use['id']} / {use['case']} / {use['region']}: {use['content']}; 창 {use['window']}; {use.get('boundary','경계 원값 미상')}. 상세 [현재 기록](collection.md#{use['id'].lower()}); 근거 [해시/시각](evidence-manifest.json). 차이: {use['difference']}. 미검증: {'; '.join(use['unverified_dimensions'])}"]
    md+=[""]
md+=["첫 시차 조회의 핵심 반환: A-M3은109.5→110→110.5초0.8→10.8→12.9억원, 끝값 경계(110,110.5]초,111초 시트/112초 prior-only 도상 후속. B-M3은148→148.5→149초44→64→82%,끝값(148.5,149]초,149.5/150초 카드·도넛·막대 후속. 숫자와 모든 도상을 동시완료로 저장하지 않았다.",""]
(root/"query-results.md").write_text("\n".join(md),encoding="utf-8")
print(json.dumps([{"args":a,"returned":w} for a,w in tests],ensure_ascii=False))

