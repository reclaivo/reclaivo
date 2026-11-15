import asyncio, os, json, shutil, subprocess, numpy as np, soundfile as sf
SCR='/tmp/claude-0/-home-claude/6c219a89-82c8-5645-9cb8-8b527d1844f4/scratchpad'
head,path=open(SCR+'/logo_path.txt').read().split('\n',1); path=path.strip()
TL=json.load(open('tl.json')); LINES=TL['lines']; tl=TL['tl']; TOTAL=TL['total']+0.30
SR=24000; W,H,FPS=1080,1920,30
# ---------- SFX ----------
rng=np.random.default_rng(3)
def env(n,a=0.005,d=0.2):
    t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-t/d)
def whoosh(dur=0.32):
    n=int(dur*SR); x=rng.normal(0,1,n).astype(np.float32)
    # moving band-pass via cumulative filtering: crude sweep using modulated one-pole lowpass
    out=np.zeros(n,np.float32); y=0
    for i in range(n):
        a=0.03+0.55*(i/n)**1.2; y+=a*(x[i]-y); out[i]=y
    hp=out-np.concatenate([[0],out[:-1]])*0.0
    e=np.sin(np.pi*np.linspace(0,1,n))**1.5
    return (out*e*1.6).astype(np.float32)
def thud(dur=0.5):
    n=int(dur*SR); t=np.arange(n)/SR
    f=70*np.exp(-t*8)+38
    ph=2*np.pi*np.cumsum(f)/SR
    body=np.sin(ph)*np.exp(-t/0.16)
    click=rng.normal(0,1,n)*np.exp(-t/0.012)*0.5
    return (body*1.0+click).astype(np.float32)
def tick(dur=0.22):
    n=int(dur*SR); t=np.arange(n)/SR
    a=np.sin(2*np.pi*1180*t)*np.exp(-t/0.05)+0.5*np.sin(2*np.pi*1770*t)*np.exp(-t/0.04)
    return (a*0.8).astype(np.float32)
def ding(dur=1.0):
    n=int(dur*SR); t=np.arange(n)/SR
    a=(np.sin(2*np.pi*1318*t)+0.5*np.sin(2*np.pi*1976*t)+0.25*np.sin(2*np.pi*2637*t))*np.exp(-t/0.35)
    return (a*0.5*np.minimum(t/0.003,1)).astype(np.float32)
def place(buf,x,t,g):
    i=int(t*SR); j=min(len(buf),i+len(x)); 
    if i<len(buf): buf[i:j]+=x[:j-i]*g
N=int(TOTAL*SR); sfx=np.zeros(N,np.float32)
cuts=[tl[1][0],tl[2][0],tl[3][0],tl[5][0]]       # cut starts
place(sfx,thud(0.5),0.0,0.55)                      # hook hit on frame 0
for c in [tl[1][0],tl[2][0],tl[3][0],tl[5][0],tl[6][0]]: place(sfx,whoosh(),max(0,c-0.12),0.35)
place(sfx,thud(0.5),tl[1][0]+0.30,0.75)           # stamp ON YOU TOO
TICK1=tl[3][1]-0.15; TICK2=tl[4][1]-0.12
place(sfx,tick(),TICK1,0.5); place(sfx,tick(),TICK2,0.5)
place(sfx,ding(),tl[6][0]+0.05,0.4); place(sfx,tick(),tl[5][0]+0.35,0.5)
voice=np.zeros(N,np.float32); v,_=sf.read('voice.wav',dtype='float32'); voice[:len(v)]=v
mix=voice*1.0+sfx*0.30
mix=np.clip(mix,-1,1); sf.write('mix.wav',mix,SR)
# ---------- words timing ----------
words=[]
for (a,b),t in zip(tl,LINES):
    ws=t.replace(',','').replace('?','').replace('.','').split(); wt=[len(w)+1 for w in ws]; tot=sum(wt); x=a
    row=[]
    for w,k in zip(ws,wt):
        d=(b-a)*k/tot; row.append((w,x,x+d)); x+=d
    for k in range(len(row)-1):
        if row[k][0]=='U' and row[k+1][0]=='K':
            row[k:k+2]=[('UK',row[k][1],row[k+1][2])]; break
    for k in range(len(row)-1):
        if row[k][0]=='D' and row[k+1][0]=='M':
            row[k:k+2]=[('DM',row[k][1],row[k+1][2])]; break
    words.append(row)
def span(i,cls=''):
    return ''.join(f'<span class="w {cls}" data-s="{s:.3f}" data-e="{e:.3f}">{w.upper()}</span> ' for w,s,e in words[i])
def logo(fill,h): s=h/434; return f'<svg width="{429*s}" height="{h}" viewBox="0 0 429 434"><path fill="{fill}" fill-rule="evenodd" d="{path}"/></svg>'
cutsT=[(0,tl[1][0]),(tl[1][0],tl[2][0]),(tl[2][0],tl[3][0]),(tl[3][0],tl[5][0]),(tl[5][0],tl[6][0]),(tl[6][0],TOTAL)]
def sec(i,inner,bg=None):
    a,b=cutsT[i]
    bgd=f'<div class="bgp" style="background-image:url(img/{bg}.jpg)"></div><div class="bgs"></div>' if bg else ''
    return f'<section class="sc" data-a="{a:.3f}" data-b="{b:.3f}">{bgd}{inner}</section>'
w2=words[1]
s2=''.join(f'<span class="w{" slab" if k>=2 else ""}" data-s="{s:.3f}" data-e="{e:.3f}">{w.upper()}</span> ' for k,(w,s,e) in enumerate(w2))
CHECK='<svg viewBox="0 0 24 24" fill="none" stroke="#DEFB0A" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 6.5"/></svg>'
chips=''.join(f'<div class="chip" data-t="{t}" data-r="{r}" style="left:{x}px;top:{y}px">{txt}</div>' for txt,t,x,y,r in [("LONG VIDEO",0.12,110,440,-7),("NO HOOK",0.30,560,410,5),("BURIED",0.48,780,490,8),("LOW REACH",0.62,560,1160,-5)])
sparks=''.join(f'<i class="sp" data-a="{k*360/16}"></i>' for k in range(16))
conf=''.join(f'<b class="cf" data-k="{k}"></b>' for k in range(46))
TH=tl[1][0]+0.30
CT=tl[6][0]
T1=TICK1; T2=TICK2; R2S=tl[4][0]
LB=logo('#DEFB0A',58); L5=logo('#DEFB0A',260)
b0=sec(0,f'<div class="ring" id="ring"></div>{chips}<div class="ad" id="ad">ZERO?</div><div class="cap" style="margin-top:26px;font-size:88px">{span(0)}</div>','studio')
b1=sec(1,f'<div class="haz" id="haz"></div><div class="shock" id="shock"></div>{sparks}<div class="cap" style="font-size:170px;line-height:1.1;position:relative;z-index:2">{s2}</div>')
b2=sec(2,f'<svg id="shield" width="400" height="200" viewBox="0 0 100 50" fill="none" stroke="#DEFB0A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:30px"><path pathLength="1" id="sh1" d="M6 10 H94 V40 H6 Z"/><path pathLength="1" id="sh2" style="stroke-width:12" d="M40 25 H64"/></svg><div class="tag" style="margin-bottom:24px">The clipping fix</div><div class="cap" style="font-size:84px">{span(2)}</div><div class="src">Short clips get found</div>','desk')
b3=sec(3,f'<div class="row"><div class="box" id="b1">{CHECK}</div><div class="rt">{span(3)}</div></div><div class="row" id="r2"><div class="box" id="b2">{CHECK}</div><div class="rt">{span(4)}</div></div>{conf}','growth')
BUB='<svg id="bub" width="250" height="230" viewBox="0 0 100 92" fill="none" stroke="#DEFB0A" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" style="margin-bottom:34px"><path pathLength="1" id="bb1" d="M10 8 H90 V60 H44 L24 82 V60 H10 Z"/><circle cx="32" cy="34" r="4" fill="#DEFB0A" class="dot"/><circle cx="50" cy="34" r="4" fill="#DEFB0A" class="dot"/><circle cx="68" cy="34" r="4" fill="#DEFB0A" class="dot"/></svg>'
b4=sec(4,'<div class="ring" id="ring2" style="left:190px;top:440px;width:700px;height:700px"></div>'+BUB+'<div class="cap" style="font-size:112px;z-index:2">'+span(5)+'</div><div class="src" style="color:#DEFB0A">Drop it in the comments</div>','studio')
b5=sec(5,'<div class="logo5" id="lg5" style="z-index:2">'+logo('#DEFB0A',170)+'</div><div class="cap" style="font-size:80px;z-index:2">'+span(6)+'</div><div class="pill" id="pill">Follow</div><div class="ct" id="ct1">DM @RECLAIVO on Instagram</div><div class="ct" id="ct2">hello@reclaivo.com</div><svg class="cur" id="cur" viewBox="0 0 24 24"><path d="M5 3l14 8-6 2 4 7-3 1-4-7-5 4z" fill="#fff" stroke="#0B0B0B" stroke-width="1.4" stroke-linejoin="round"/></svg>','growth')
CSS="""*{margin:0;box-sizing:border-box}body{width:1080px;height:1920px;overflow:hidden;background:#0B0B0B;font-family:Anton;position:relative;color:#fff}
.glow{position:absolute;inset:0;background:radial-gradient(70% 40% at 50% 46%,rgba(222,251,10,.16),transparent 70%)}
.sc{position:absolute;inset:0;padding:390px 130px 620px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;opacity:0;transform-origin:50% 48%}
.bgp{position:absolute;inset:-70px;background-size:cover;background-position:center;filter:brightness(.34) saturate(.9);opacity:1}
.bgs{position:absolute;inset:-70px;background:linear-gradient(180deg,#0B0B0B 0%,rgba(11,11,11,.18) 30%,rgba(11,11,11,.18) 70%,#0B0B0B 100%)}
.sc>*:not(.bgp):not(.bgs){position:relative}
.cap{font-size:100px;line-height:1.03;text-transform:uppercase}
.w{display:inline-block;color:#fff}.w.on{color:#DEFB0A}
.slab{background:#DEFB0A;color:#0B0B0B;padding:0 20px;margin:8px 6px;transform:rotate(-2deg)}.slab.on{color:#0B0B0B}
.ad{font-size:400px;line-height:.82;color:#DEFB0A;position:relative;z-index:2}
.tag{font-family:'Barlow Condensed';font-weight:700;letter-spacing:.24em;text-transform:uppercase;font-size:42px;color:#cfd2c4}
.src{margin-top:44px;font-family:'Barlow Condensed';font-weight:600;letter-spacing:.2em;text-transform:uppercase;font-size:32px;color:#9fa391}
.row{display:flex;align-items:center;gap:30px;width:100%;margin:30px 0;text-align:left}
.box{flex:0 0 108px;height:108px;border:8px solid #DEFB0A;border-radius:24px;position:relative}
.box svg{position:absolute;inset:10px;width:76px;height:76px;opacity:0}
.rt{font-size:74px;line-height:1.05;text-transform:uppercase}
.brand{position:absolute;left:100px;top:372px;display:flex;align-items:center;gap:18px;font-size:40px;letter-spacing:.05em;z-index:9}
.bar{position:absolute;left:130px;right:130px;top:1300px;height:10px;background:rgba(255,255,255,.16);border-radius:10px;overflow:hidden;z-index:9}.bar i{display:block;height:100%;width:0;background:#DEFB0A}
.chip{position:absolute!important;font-family:'Barlow Condensed';font-weight:700;letter-spacing:.14em;font-size:40px;padding:12px 26px;border:4px solid #DEFB0A;color:#DEFB0A;background:rgba(11,11,11,.7);border-radius:999px;opacity:0;z-index:3;white-space:nowrap}
.ring{position:absolute!important;border:10px dashed rgba(222,251,10,.55);border-radius:50%;width:700px;height:700px;left:190px;top:440px;z-index:1}
.haz{position:absolute!important;left:-10%;width:120%;top:640px;height:300px;transform:rotate(-4deg);background:repeating-linear-gradient(45deg,rgba(222,251,10,.20) 0 38px,rgba(11,11,11,0) 38px 76px);z-index:0}
.shock{position:absolute!important;left:240px;top:520px;width:600px;height:600px;border:12px solid #DEFB0A;border-radius:50%;opacity:0;z-index:1}
.sp{position:absolute!important;left:540px;top:770px;width:8px;height:70px;background:#DEFB0A;transform-origin:50% 0;opacity:0;z-index:1}
.cf{position:absolute!important;width:16px;height:16px;background:#DEFB0A;opacity:0;z-index:4;left:0;top:0}
.pill{margin-top:34px;padding:20px 64px;border-radius:999px;font-family:'Barlow Condensed';font-weight:700;font-size:62px;letter-spacing:.12em;background:#DEFB0A;color:#0B0B0B;border:6px solid #DEFB0A;text-transform:uppercase;z-index:2}
.cur{position:absolute!important;left:0;top:0;width:90px;height:90px;z-index:8;opacity:0}
.logo5{margin-bottom:26px}
.ct{font-family:'Barlow Condensed';font-weight:700;letter-spacing:.08em;font-size:50px;color:#fff;margin-top:22px;opacity:0;z-index:2}#ct2{color:#DEFB0A;font-size:56px}"""
html='<!doctype html><meta charset=utf-8><link href="https://fonts.googleapis.com/css2?family=Anton&family=Barlow+Condensed:wght@600;700&display=swap" rel="stylesheet"><style>'+CSS+'</style><body><div class="glow"></div><div class="brand">'+LB+'<span>RECLAIVO</span></div>'+b0+b1+b2+b3+b4+b5+'<div class="bar"><i id="pg"></i></div></body>'
open('page.html','w').write(html)
JS=r'''(t)=>{
 const ease=x=>1-Math.pow(1-x,3), cl=(x)=>Math.min(1,Math.max(0,x)), T=%TOT%, th=%TH%, CT=%CT%;
 let shake=0; if(t>=th&&t<th+0.35){const k=1-(t-th)/0.35; shake=k*k*22} if(t<0.4){shake=Math.max(shake,(1-t/0.4)*14)}
 document.querySelectorAll('.sc').forEach(s=>{
  const a=+s.dataset.a,b=+s.dataset.b,on=t>=a&&t<b; s.style.opacity=on?1:0; if(!on)return;
  const lt=t-a, punch=1+0.10*Math.pow(Math.max(0,1-lt/0.28),2), slow=1+0.045*(lt/(b-a));
  s.style.transform='translate('+(Math.sin(t*90)*shake).toFixed(1)+'px,'+(Math.cos(t*77)*shake).toFixed(1)+'px) scale('+(punch*slow).toFixed(4)+')';
  const bg=s.querySelector('.bgp'); if(bg){const q=lt/(b-a);bg.style.transform='scale('+(1.08+0.14*q).toFixed(3)+') translate('+(-30*q).toFixed(1)+'px,'+(20*q).toFixed(1)+'px)'}
 });
 document.querySelectorAll('.w').forEach(w=>{const s=+w.dataset.s,e=+w.dataset.e,act=t>=s&&t<e;w.classList.toggle('on',act);if(!w.classList.contains('slab'))w.style.transform=act?'scale(1.08)':'none'});
 document.querySelectorAll('.chip').forEach(c=>{const k=cl((t-(+c.dataset.t))/0.25),v=ease(k);c.style.opacity=v;c.style.transform='rotate('+c.dataset.r+'deg) scale('+(0.4+0.6*v+0.12*Math.sin(k*Math.PI)).toFixed(3)+')'});
 const ad=document.getElementById('ad'); if(ad)ad.style.transform='rotate('+(Math.sin(t*14)*3)+'deg) scale('+(1+0.06*Math.sin(t*10))+')';
 const rg=document.getElementById('ring'); if(rg)rg.style.transform='rotate('+(t*60)+'deg)';
 const rg2=document.getElementById('ring2'); if(rg2){const l=t-CT;rg2.style.transform='rotate('+(-l*50)+'deg) scale('+(1+0.04*Math.sin(l*5))+')'}
 const hz=document.getElementById('haz'); if(hz)hz.style.backgroundPosition=((t*180)%76)+'px 0';
 const sh=document.getElementById('shock'); if(sh){const k=cl((t-th)/0.5);sh.style.opacity=(k>0&&k<1)?(1-k)*.9:0;sh.style.transform='scale('+(0.2+k*2.0)+')'}
 document.querySelectorAll('.sp').forEach(sp=>{const k=cl((t-th)/0.45);const a=parseFloat(sp.dataset.a);sp.style.opacity=(k>0&&k<1)?(1-k):0;sp.style.transform='rotate('+a+'deg) translateY('+(150+k*330)+'px) scaleY('+(1-k*0.6)+')'});
 const s1=document.getElementById('sh1'),s2=document.getElementById('sh2'); if(s1){const l=t-%A3%;s1.style.strokeDasharray=1;s1.style.strokeDashoffset=1-cl(l/0.45);s2.style.strokeDasharray=1;s2.style.strokeDashoffset=1-cl((l-0.45)/0.3);document.getElementById('shield').style.transform='scale('+(1+0.08*Math.sin(cl((l-0.7)/0.4)*Math.PI))+')'}
 const r2=document.getElementById('r2'); r2.style.opacity=t>=%R2S%?1:0; r2.style.transform='translateY('+((1-cl((t-%R2S%)/0.3))*50)+'px)';
 [['b1',%T1%],['b2',%T2%]].forEach(([id,tt])=>{const b=document.getElementById(id),sv=b.querySelector('svg'),k=cl((t-tt)/0.18);sv.style.opacity=k;b.style.background=k>0.05?'rgba(222,251,10,'+(0.18*k)+')':'transparent';b.style.transform='scale('+(1+0.15*Math.sin(k*Math.PI))+')'});
 document.querySelectorAll('.cf').forEach(c=>{const k=+c.dataset.k,tt=k%2?%T2%:%T1%,dt=t-tt;if(dt<0||dt>1.4){c.style.opacity=0;return}
  const r1=Math.abs((Math.sin(k*12.9898)*43758.5453)%1),q=Math.abs((Math.sin(k*78.233)*12345.678)%1),vx=r1*900,vy=-500-q*700;
  const bx=150,by=k%2?760:600;
  c.style.opacity=1-dt/1.4;c.style.transform='translate('+(bx+vx*dt)+'px,'+(by+vy*dt+1500*dt*dt)+'px) rotate('+(dt*720*(q>0.5?1:-1))+'deg)';c.style.background=k%3?'#DEFB0A':'#fff'});
 const pill=document.getElementById('pill'),cur=document.getElementById('cur'); if(pill){const l=t-CT;
   const pr=pill.getBoundingClientRect(),tx=pr.left+pr.width*0.62,ty=pr.top+pr.height*0.45,k=cl((l-0.25)/0.55),x=tx+300*(1-ease(k)),y=ty+360*(1-ease(k));
   cur.style.opacity=(l>0.25&&l<1.6)?1:0;
   const tap=cl((l-0.85)/0.12);cur.style.transform='translate('+x+'px,'+y+'px) scale('+(1-0.2*Math.sin(tap*Math.PI))+')';
   const done=l>0.95; pill.textContent=done?'Following':'Follow';
   pill.style.background=done?'transparent':'#DEFB0A';pill.style.color=done?'#DEFB0A':'#0B0B0B';
   pill.style.transform='scale('+(1+0.1*Math.sin(cl((l-0.9)/0.3)*Math.PI))+')'}
 ['ct1','ct2'].forEach((id,n)=>{const e=document.getElementById(id);if(e){const k=cl((t-CT-1.05-n*0.3)/0.25);e.style.opacity=k;e.style.transform='translateY('+((1-ease(k))*30)+'px)'}});
 const bb=document.getElementById('bb1'); if(bb){const l=t-%A5%;bb.style.strokeDasharray=1;bb.style.strokeDashoffset=1-cl(l/0.4);document.querySelectorAll('.dot').forEach((d,n)=>{d.style.opacity=cl((l-0.4-n*0.12)/0.1)});document.getElementById('bub').style.transform='scale('+(1+0.07*Math.sin(cl((l-0.4)/0.5)*Math.PI*2))+')'}
 const lg=document.getElementById('lg5'); if(lg){const l=t-CT;lg.style.transform='scale('+(1+0.12*Math.exp(-l*5)*Math.cos(l*18))+')'}
 document.getElementById('pg').style.width=(t/T*100)+'%';
}'''
JS=JS.replace('%TOT%',str(TOTAL)).replace('%TH%',str(TH)).replace('%CT%',str(CT)).replace('%A3%',str(tl[2][0])).replace('%A5%',str(tl[5][0])).replace('%R2S%',str(R2S)).replace('%T1%',str(T1)).replace('%T2%',str(T2))
from playwright.async_api import async_playwright
async def main():
    shutil.rmtree('fr',ignore_errors=True); os.makedirs('fr')
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':W,'height':H}); await pg.goto('file:///tmp/vid2/page.html'); await pg.wait_for_timeout(1200)
        n=int(TOTAL*FPS)
        for i in range(n):
            await pg.evaluate(JS,i/FPS); await pg.screenshot(path=f'fr/{i:04d}.jpg',type='jpeg',quality=90)
        await b.close(); return n
n=asyncio.run(main()); print('frames',n,'total',round(TOTAL,2))
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i','fr/%04d.jpg','-i','mix.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart','/tmp/vid2/reclaivo-video-04.mp4'],check=True)
print('done')
