# R1 CI 검사와 조회

Phase00의.환경/Scripts/python.exe로실행한다. 환경패키지.txt에jsonschema·날짜검사·PyMuPDF·Pillow등실제버전을고정했다. PyMuPDF는PDF호환AI읽기/미리보기, Pillow는RGBA픽셀대조에사용한다. 별도API키없음.

```powershell
& '.환경/Scripts/python.exe' '07_실행도구/R1_자산검사.py'
& '.환경/Scripts/python.exe' '07_실행도구/R1_자산검사.py' --colors hanmac --include-observed
& '.환경/Scripts/python.exe' '07_실행도구/조회문서생성.py'
```

첫명령은읽기검사만수행한다. 두번째는현재회사CI의관측색을명시적으로조회한다. 관측포함옵션없는기본공식조회는현재빈목록을반환한다. 세번째는정본을바꾸지않고조회MD/팔레트/검사결과를재생성하며이전조회문서를backup에보존한다.

R1_자산검사.py의BASE는실행도구파일의상위Phase00이다. 다른위치에복사해직접실행하면정본경로가달라지므로위경로를사용한다. CI기록규격0.2.0은04_기록규격의영상분석규격과별개다. 검사결과의collection_complete는CI원본/관측색등록조건이며공식CI/전체공용자산/Phase00완료가아니다.

Illustrator를이용한사본정리스크립트와중간결과는backup의R1구축중간자료에보존한다. 생성스크립트는이미존재하는출력을거부한다. 그대로일괄재실행하지말고새작업ID/버전/사본경로와원본해시부터확인한다. AE/ComputerUse설정은변경하지않는다.
