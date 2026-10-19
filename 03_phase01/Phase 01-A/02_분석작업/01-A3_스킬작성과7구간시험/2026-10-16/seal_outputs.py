from pathlib import Path
import json,hashlib,sys,datetime
B=Path(__file__).resolve().parent;W=B/'company-video-grammar-analyzer-workspace'
args=sys.argv[1:];iteration='iteration-1'
if args[0]=='--iteration-2':iteration=args.pop(0)[2:]
mode=args[0]
for case in args[1:]:
    folder=W/iteration/('eval-'+case)/mode/'outputs'
    files={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in folder.iterdir() if f.is_file()}
    assert 'observations.json' in files and 'observations.md' in files
    root=W/'seals' if iteration=='iteration-1' else W/'seals'/iteration
    seal=root/(case+'-'+mode+'.json');seal.parent.mkdir(parents=True,exist_ok=True)
    if seal.exists():assert json.loads(seal.read_text(encoding='utf-8'))['files']==files
    else:
        with seal.open('x',encoding='utf-8') as out:json.dump({'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':files,'grading_feedback_provided':False},out,ensure_ascii=False,indent=2)
    print(case,mode,'sealed')
