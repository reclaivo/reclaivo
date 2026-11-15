#!/usr/bin/env python3
"""Usage: python3 make_week.py spec.json OUTDIR   (run setup.sh first)
spec.json: {"NAME": {k:P|A|B, ad, chips, L(7 lines), tag, src, bg(5)}, ...}
Builds each reel (voice, 2D, optional 3D inserts, music) -> OUTDIR/NAME.mp4. Resumable."""
import json,os,subprocess,sys,time,shutil,urllib.request
spec=sys.argv[1]; out=sys.argv[2]; os.makedirs(out,exist_ok=True)
S=json.load(open(spec)); W='/tmp/vid5'
def sh(c,cwd=None,check=True):
    r=subprocess.run(c,shell=True,cwd=cwd,capture_output=True,text=True)
    if check and r.returncode: raise SystemExit(f'FAILED: {c}\n{r.stdout[-800:]}\n{r.stderr[-1500:]}')
    return r
def dur(f): return float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {f}').stdout)
# 0. validation of spec
for n,r in S.items():
    assert r['k'] in 'PAB' and len(r['L'])==7 and len(r['bg'])==5, n
    assert len(r['L'][1].replace('Reclaivo','Re clay vee oh').split())<=7 and len(r['L'][1].split())<=5, n+': line 2 (big stamp) must be max 5 words'
    for l in r['L']: assert '—' not in l and '–' not in l, n
sh(f'python3 /tmp/vid5/patch7.py {spec}')
srv=None
def server():
    global srv
    try: urllib.request.urlopen('http://localhost:8123/insert.html',timeout=3); return
    except Exception: pass
    srv=subprocess.Popen(['python3','-m','http.server','8123'],cwd='/tmp/t3d',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(2)
oov={}
for n in S:                                    # voice + 2D first for all
    d=f'{W}/{n}'
    if os.path.exists(f'{out}/{n}.mp4'): continue
    if not os.path.exists(f'{d}/base.mp4'):
        r=sh('python3 audio.py',d); open(f'{d}/a.log','w').write(r.stdout+r.stderr)
        miss=[l for l in (r.stdout+r.stderr).splitlines() if 'OOV' in l]
        if miss: oov[n]=miss
        else: sh('python3 build5.py',d)
if oov: raise SystemExit('OOV words skipped by the voice (reword those lines in the spec and rerun): '+json.dumps(oov))
for n,r in S.items():
    d=f'{W}/{n}'; fin=f'{out}/{n}.mp4'
    if os.path.exists(fin): continue
    if r['k']=='P':
        sh(f'python3 music.py {n}',W); sh(f'./composep.sh {n}',W)
    else:
        server()
        if not os.path.exists(f'{d}/ins/0000.png') or len(os.listdir(f'{d}/ins'))<10: sh(f'python3 /tmp/t3d/ins.py {n}','/tmp/t3d')
        sh(f'python3 music.py {n}',W); sh(f'./composem.sh {n}',W)
    f=f'{d}/final_m.mp4'; t=dur(f)
    assert 5<t<=15.0, f'{n} duration {t}'
    shutil.copy(f,fin); print('OK',n,round(t,1),flush=True)
if srv: srv.terminate()
print('ALL_DONE')
