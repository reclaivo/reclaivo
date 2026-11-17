import re, json, os, shutil, subprocess
def rep(s,a,b):
    assert a in s, a[:80]
    return s.replace(a,b)
base=open('/tmp/vid2/build4.py').read()
import json as _j
import sys
RE=_j.load(open(sys.argv[1]))
for R in RE:
    d=f'/tmp/vid5/{R}'; os.makedirs(d,exist_ok=True)
    # audio script
    a=open('/tmp/t3d/audio_t.py').read(); i=a.index('LINES=['); j=a.index(']',i)+1
    open(f'{d}/audio.py','w').write(a[:i]+'LINES='+json.dumps([l.replace('Reclaivo','Re clay vee oh') for l in RE[R]['L']])+a[j:])
    shutil.rmtree(f'{d}/img',ignore_errors=True); shutil.copytree('/tmp/vid2/img',f'{d}/img')
    site='/mnt/user-data/outputs/reclaivo-ima/images'
    for n,f in (('work1','work-1'),('way2','way-2'),('work5','work-5'),('service1','service-1')):
        shutil.copy(f'{site}/{f}-v2.jpg',f'{d}/img/{n}.jpg')
    shutil.copy('/tmp/t3d/char/pose5.png',f'{d}/img/pose5.png')
    c=dict(RE[R]); c['narr']=False; c['slab']=c.get('slab') or ('{3,4}' if c['k']=='B' else '{2}'); s=base
    s=rep(s,"/tmp/vid2/page.html","'+os.getcwd()+'/page.html")if False else s
    s=s.replace("'file:///tmp/vid2/page.html'","'file://'+os.getcwd()+'/page.html'")
    s=rep(s,'" slab" if k>=2 else ""','" slab" if k in '+c['slab']+' else ""')
    s=re.sub(r'\[\("LONG VIDEO".*?\)\]\)',lambda m:'[%s])'%','.join(repr(x) for x in c['chips']),s,count=1,flags=re.S) if False else s
    # chips list
    i=s.index('chips=');j=s.index('\n',i)
    s=s[:i]+"chips=''.join(f'<div class=\"chip\" data-t=\"{t}\" data-r=\"{r}\" style=\"left:{x}px;top:{y}px\">{txt}</div>' for txt,t,x,y,r in "+repr(c['chips'])+")"+s[j:]
    s=rep(s,'id="ad">ZERO?</div>','id="ad" style="font-size:%dpx">%s</div>'%(min(400,int(400*5/max(len(c['ad']),5)*0.97)),c['ad']))
    # backgrounds
    s=rep(s,"</div>','studio')\nb1","</div>','"+c['bg'][0]+"')\nb1")
    s=rep(s,"</div>','desk')\nb3","</div>','"+c['bg'][1]+"')\nb3")
    s=rep(s,"{conf}','growth')","{conf}','"+c['bg'][2]+"')")
    s=rep(s,"Drop it in the comments</div>','studio')","Drop it in the comments</div>'"+("+'<img src=\"img/pose5.png\" style=\"position:absolute!important;right:-130px;bottom:-380px;height:1280px;z-index:1;filter:drop-shadow(0 0 14px rgba(222,251,10,.35)) brightness(1.3)\">'" if c['narr'] else "")+",'"+c['bg'][3]+"')")
    s=rep(s,"</svg>','growth')","</svg>','"+c['bg'][4]+"')")
    # cut 3 slot instead of svg
    if c['k']!='P': s=re.sub(r'<svg id="shield".*?</svg>','<div id="slot" style="height:430px"></div>',s,count=1,flags=re.S)
    s=rep(s,"The clipping fix",c['tag']); s=rep(s,"Short clips get found",c['src'])
    # logo slot
    if c['k']!='P': s=rep(s,"'<div class=\"logo5\" id=\"lg5\" style=\"z-index:2\">'+logo('#DEFB0A',170)+'</div>","'<div class=\"logo5\" id=\"lg5\" style=\"height:330px\"></div>")
    # css
    s=rep(s,".cap{font-size:100px;line-height:1.03;",".cap{font-size:100px;line-height:1.2;")
    s=rep(s,"line-height:1.1;position:relative;z-index:2","line-height:1.18;position:relative;z-index:2")
    s=rep(s,".brand{position:absolute;left:100px;top:372px;",".brand{background:rgba(6,6,6,.78);padding:10px 26px 10px 18px;border-radius:999px;border:2px solid rgba(222,251,10,.35);position:absolute;left:90px;top:366px;")
    s=rep(s,".bar{position:absolute;",".bar{display:none;position:absolute;")
    s=rep(s,"            row[k:k+2]=[('DM',row[k][1],row[k+1][2])]; break\n    words.append(row)","            row[k:k+2]=[('DM',row[k][1],row[k+1][2])]; break\n    for k in range(len(row)-3):\n        if [row[k][0],row[k+1][0],row[k+2][0],row[k+3][0]]==['Re','clay','vee','oh']:\n            row[k:k+4]=[('Reclaivo',row[k][1],row[k+3][2])]; break\n    words.append(row)")
    # extra sfx for inserts
    extra="""
INS={}
if REEL=='A':
    INS=dict(ticks=[tl[2][0]+0.55,tl[2][0]+1.15,tl[2][0]+1.75])
    for t_ in INS['ticks']: place(sfx,tick(),t_,0.5)
elif REEL=='B':
    INS=dict(splitT=tl[2][0]+(tl[2][1]-tl[2][0])*0.62)
    place(sfx,thud(0.5),INS['splitT'],0.6); place(sfx,whoosh(),INS['splitT']-0.1,0.3)
"""
    s=rep(s,"voice=np.zeros(N,np.float32)",extra+"voice=np.zeros(N,np.float32)")
    s=rep(s,"SR=24000;","REEL='"+c['k']+"'; SR=24000;")
    # final encode -> silent base + cuts.json
    i=s.index("subprocess.run(['ffmpeg'")
    s=s[:i]+"""subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i','fr/%04d.jpg','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','base.mp4'],check=True)
INS.update(kind=REEL,total=TOTAL,c3=list(cutsT[2]),c6=list(cutsT[5]),fps=FPS)
json.dump(INS,open('cuts.json','w'))
print('done')
"""
    i=s.index("b4=sec(4,");j=s.index("b5=sec(5");seg=s[i:j]
    k=seg.index('<div class="ring" id="ring2"');e=seg.index('</div>',k)+6
    s=s[:i]+seg[:k]+seg[e:]+s[j:]
    open(f'{d}/build5.py','w').write(s)
print('patched')
