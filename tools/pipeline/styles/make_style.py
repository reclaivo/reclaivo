#!/usr/bin/env python3
"""Build one Glass Icons (G) or Software Walkthrough (S) reel.
usage: make_style.py glass|walk WORKDIR OUT.mp4
Prereqs: tools/pipeline/setup.sh done (/tmp/t3d has node_modules, /tmp/tts has Kokoro).
WORKDIR/lines.json = 7 spoken lines: hook, 4 beats, 'Comment DEAL below.' (or CLIP), 'Follow, then D M us or email us.'
Before running, edit the page text (headline, CARD array / NAMES / TXT) for the new topic, see RUNBOOK.md.
"""
import sys,os,json,shutil,subprocess
kind,W,OUT=sys.argv[1],sys.argv[2],sys.argv[3]
H=os.path.dirname(os.path.abspath(__file__));os.makedirs(W,exist_ok=True)
page={'glass':'glass.html','walk':'walk.html'}[kind];tlname={'glass':'glass_tl.json','walk':'walk_tl.json'}[kind]
sh=lambda c:subprocess.run(c,shell=True,check=True)
for f in ('glass.html','walk.html'):
    if os.path.exists(f'{W}/{f}'):shutil.copy(f'{W}/{f}','/tmp/t3d/'+f)
    else:shutil.copy(f'{H}/{f}','/tmp/t3d/'+f)
sh(f'cd {H} && python3 audio.py {W}')
shutil.copy(f'{W}/tl.json','/tmp/t3d/'+tlname)
tl=json.load(open(f'{W}/tl.json'))['tl'];tot=json.load(open(f'{W}/tl.json'))['total']+0.3
assert tot<=15.0,f'too long {tot}'
c=[(0.0,'w')]
if kind=='glass':
    for k in range(1,5):c+=[(tl[k][0]-0.12,'w'),(tl[k][0]+0.3,'p')]
    c+=[(tl[5][0]-0.1,'w'),(tl[5][0]+0.35,'ch'),(tl[6][0],'p2')]
else:
    s=[tl[k][0] for k in range(1,5)]
    for k in range(4):c.append((s[k]-0.1,'w'))
    for t in [s[0]+0.85,s[1]+0.7,s[2]+0.65,s[2]+1.45]:c.append((t,'c'))
    for i in range(0,34,2):c.append((s[1]+0.8+i*(1.4/34),'c'))
    c+=[(s[3]+0.2,'p'),(s[3]+0.25,'ch'),(tl[5][0]-0.1,'w'),(tl[5][0]+0.35,'ch'),(tl[6][0],'p2')]
json.dump(c,open(f'{W}/cues.json','w'))
sh(f'cd {H} && python3 mix.py {W} x && python3 /tmp/vid5/music.py {W}')
sh('pgrep -f "http.server 8123" >/dev/null || (cd /tmp/t3d && nohup python3 -m http.server 8123 >/tmp/srv.log 2>&1 &) ; sleep 1')
fr=f'{W}/fr';shutil.rmtree(fr,ignore_errors=True)
sh(f'cd {H} && python3 render.py http://localhost:8123/{page} {fr} {tot}')
sh(f'ffmpeg -y -loglevel error -framerate 30 -i {fr}/%04d.jpg -i {W}/mixm.wav -af "loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000" -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart {W}/base.mp4')
sh(f'sh /tmp/vid5/add_cover.sh {W}/base.mp4 {OUT} 0.9')
print('DONE',OUT)
