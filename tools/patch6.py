import re, json, os, shutil, subprocess
def rep(s,a,b):
    assert a in s, a[:80]
    return s.replace(a,b)
base=open('/tmp/vid2/build4.py').read()
LINESETS={
 'A':["Brand or creator?","Most deals fail before they start.","No payment date, no content plan, no terms.","Write all three down first,","and every deal runs smooth.","Comment DEAL below.","Follow, then D M us or email us."],
 'C':["Ghosted by brands?","Most ghosting starts with a vague brief.","No clear goal, no deadline, no budget.","Agree all three in writing first,","and replies come fast.","Comment DEAL below.","Follow, then D M us or email us."],
 'D':["One video, ten clips?","Most creators post a video once.","One long video holds many strong moments.","So cut each strong moment into its own clip,","and every clip gets a new chance.","Comment CLIP below.","Follow, then D M us or email us."],
 'B':["Great content, zero views?","That is a clip problem.","Your best twenty seconds are buried inside a long video.","So turn your best moment into a short clip,","and post one every single day.","Comment CLIP below.","Follow, then D M us or email us."]}
CFG={
 'C':dict(ad='GHOSTED?',chips=[("BRAND",0.12,150,440,-7),("CREATOR",0.30,560,410,5),("BRIEF",0.48,700,500,8),("NO REPLY",0.62,150,1160,-5)],
          slab="{2}",tag='The 3 basics',src='Agree them first',bg=['way2','work1','work5','studio','growth'],cap3=84,comment='x',narr=False),
 'D':dict(ad='CLIPS?',chips=[("LONG VIDEO",0.12,110,440,-7),("ONE POST",0.30,560,410,5),("MANY CLIPS",0.48,700,490,8),("MORE REACH",0.62,560,1160,-5)],
          slab="{3,4}",tag='The clipping tip',src='One video, many clips',bg=['desk','studio','growth','studio','growth'],cap3=84,comment='x',narr=False),
 'A':dict(ad='DEAL?',chips=[("BRAND",0.12,150,440,-7),("CREATOR",0.30,560,410,5),("CONTRACT",0.48,700,500,8),("PAYMENT",0.62,150,1160,-5)],
          slab="{2}",tag='The 3 gaps',src='Fix them before you sign',bg=['work1','way2','work5','studio','growth'],cap3=84,
          comment='Drop it in the comments',narr=False),
 'B':dict(ad='ZERO?',chips=[("LONG VIDEO",0.12,110,440,-7),("NO HOOK",0.30,560,410,5),("BURIED",0.48,780,490,8),("LOW REACH",0.62,560,1160,-5)],
          slab="{3,4}",tag='The clipping fix',src='Short clips get found',bg=['studio','desk','growth','studio','growth'],cap3=84,
          comment='Drop it in the comments',narr=True)}
KIND={'C':'A','D':'B'}
for R in ('C','D'):
    d=f'/tmp/vid5/{R}'; os.makedirs(d,exist_ok=True)
    # audio script
    a=open('/tmp/t3d/audio_t.py').read(); i=a.index('LINES=['); j=a.index(']',i)+1
    open(f'{d}/audio.py','w').write(a[:i]+'LINES='+json.dumps(LINESETS[R])+a[j:])
    shutil.rmtree(f'{d}/img',ignore_errors=True); shutil.copytree('/tmp/vid2/img',f'{d}/img')
    site='/mnt/user-data/outputs/reclaivo-ima/images'
    for n,f in (('work1','work-1'),('way2','way-2'),('work5','work-5'),('service1','service-1')):
        shutil.copy(f'{site}/{f}-v2.jpg',f'{d}/img/{n}.jpg')
    shutil.copy('/tmp/t3d/char/pose5.png',f'{d}/img/pose5.png')
    c=CFG[R]; s=base
    s=rep(s,"/tmp/vid2/page.html","'+os.getcwd()+'/page.html")if False else s
    s=s.replace("'file:///tmp/vid2/page.html'","'file://'+os.getcwd()+'/page.html'")
    s=rep(s,'" slab" if k>=2 else ""','" slab" if k in '+c['slab']+' else ""')
    s=re.sub(r'\[\("LONG VIDEO".*?\)\]\)',lambda m:'[%s])'%','.join(repr(x) for x in c['chips']),s,count=1,flags=re.S) if False else s
    # chips list
    i=s.index('chips=');j=s.index('\n',i)
    s=s[:i]+"chips=''.join(f'<div class=\"chip\" data-t=\"{t}\" data-r=\"{r}\" style=\"left:{x}px;top:{y}px\">{txt}</div>' for txt,t,x,y,r in "+repr(c['chips'])+")"+s[j:]
    s=rep(s,'>ZERO?</div>','>'+c['ad']+'</div>')
    # backgrounds
    s=rep(s,"</div>','studio')\nb1","</div>','"+c['bg'][0]+"')\nb1")
    s=rep(s,"</div>','desk')\nb3","</div>','"+c['bg'][1]+"')\nb3")
    s=rep(s,"{conf}','growth')","{conf}','"+c['bg'][2]+"')")
    s=rep(s,"Drop it in the comments</div>','studio')","Drop it in the comments</div>'"+("+'<img src=\"img/pose5.png\" style=\"position:absolute!important;right:-130px;bottom:-380px;height:1280px;z-index:1;filter:drop-shadow(0 0 14px rgba(222,251,10,.35)) brightness(1.3)\">'" if c['narr'] else "")+",'"+c['bg'][3]+"')")
    s=rep(s,"</svg>','growth')","</svg>','"+c['bg'][4]+"')")
    # cut 3 slot instead of svg
    s=re.sub(r'<svg id="shield".*?</svg>','<div id="slot" style="height:430px"></div>',s,count=1,flags=re.S)
    s=rep(s,"The clipping fix",c['tag']); s=rep(s,"Short clips get found",c['src'])
    # logo slot
    s=rep(s,"'<div class=\"logo5\" id=\"lg5\" style=\"z-index:2\">'+logo('#DEFB0A',170)+'</div>","'<div class=\"logo5\" id=\"lg5\" style=\"height:330px\"></div>")
    # css
    s=rep(s,".cap{font-size:100px;line-height:1.03;",".cap{font-size:100px;line-height:1.2;")
    s=rep(s,"line-height:1.1;position:relative;z-index:2","line-height:1.18;position:relative;z-index:2")
    s=rep(s,".brand{position:absolute;left:100px;top:372px;",".brand{background:rgba(6,6,6,.78);padding:10px 26px 10px 18px;border-radius:999px;border:2px solid rgba(222,251,10,.35);position:absolute;left:90px;top:366px;")
    s=rep(s,".bar{position:absolute;",".bar{display:none;position:absolute;")
    # extra sfx for inserts
    extra="""
if REEL=='A':
    INS=dict(ticks=[tl[2][0]+0.55,tl[2][0]+1.15,tl[2][0]+1.75])
    for t_ in INS['ticks']: place(sfx,tick(),t_,0.5)
else:
    INS=dict(splitT=tl[2][0]+(tl[2][1]-tl[2][0])*0.62)
    place(sfx,thud(0.5),INS['splitT'],0.6); place(sfx,whoosh(),INS['splitT']-0.1,0.3)
"""
    s=rep(s,"voice=np.zeros(N,np.float32)",extra+"voice=np.zeros(N,np.float32)")
    s=rep(s,"SR=24000;","REEL='"+KIND[R]+"'; SR=24000;")
    # final encode -> silent base + cuts.json
    i=s.index("subprocess.run(['ffmpeg'")
    s=s[:i]+"""subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i','fr/%04d.jpg','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','base.mp4'],check=True)
INS.update(total=TOTAL,c3=list(cutsT[2]),c6=list(cutsT[5]),fps=FPS)
json.dump(INS,open('cuts.json','w'))
print('done')
"""
    open(f'{d}/build5.py','w').write(s)
print('patched')
