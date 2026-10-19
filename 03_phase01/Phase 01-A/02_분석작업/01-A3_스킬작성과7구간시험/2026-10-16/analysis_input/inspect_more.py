from pathlib import Path
import argparse,json,sys,subprocess
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--case',required=True);p.add_argument('--tag',required=True);p.add_argument('--times',nargs='+',required=True);p.add_argument('--width',type=int,choices=[1920,3840],default=3840);p.add_argument('--out',required=True);a=p.parse_args()
packet=json.loads((HERE/'cases.json').read_text(encoding='utf-8'));case=next(c for c in packet['cases'] if c['case_id']==a.case);lo,hi=map(lambda x:F(str(x)),case['allowed_window_seconds']);times=[F(t) for t in a.times]
if not(1<=len(times)<=40 and times==sorted(set(times)) and all(lo<=t<=hi for t in times)):raise ValueError('times_not_in_case_window')
if not a.tag.isascii() or not a.tag.replace('_','').isalnum():raise ValueError('tag')
out=Path(a.out).resolve();allowed=(HERE.parent/'runs').resolve()
if not out.is_relative_to(allowed):raise ValueError('output_scope')
out.mkdir(parents=True,exist_ok=True);script=out/(a.case+'_'+a.tag+'.py')
if script.exists():raise ValueError('preserve_prior_extra')
src=(HERE/'bounded_base.py').read_text(encoding='utf-8');helpers=(HERE.parent.parent/'phase01a-a2').as_posix();runtime=(HERE.parent.parent/'phase01a-a1/후보런타임').as_posix()
src=src.replace('from prepare import OUT,ROOT,sha,write,preflight',f"sys.path.insert(0,{helpers!r})\nfrom prepare import ROOT,sha,write,preflight\nOUT=Path(__file__).resolve().parent")
src=src.replace("OUT/'입력고정과_컨테이너사전점검.json'",f"Path({str(HERE.parent.parent/'phase01a-a2/입력고정과_컨테이너사전점검.json')!r})")
src=src.replace("OUT.parent/'phase01a-a1/후보런타임'",f'Path({runtime!r})')
line=next(s for s in src.splitlines() if s.startswith('    targets=('));src=src.replace(line,f"    targets=[Fraction(t) for t in {[str(t) for t in times]!r}]")
src=src.replace('width=1920;height=',f'width={a.width};height=')
src=src.replace("if phase not in {'initial','detail','initial_retest','detail_retest'}:",f"if phase!={a.tag!r}:")
src=src.replace("for aid in ([sys.argv[2]] if len(sys.argv)>2 else ['자료005','자료013']):",f"for aid in [{case['asset_id']!r}]:")
script.write_text(src,encoding='utf-8');result=subprocess.run([sys.executable,'-B','-X','utf8',str(script),a.tag],timeout=55);raise SystemExit(result.returncode)
