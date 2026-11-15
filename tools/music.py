import sys,numpy as np,soundfile as sf,scipy.signal as ss
R=sys.argv[1]
m,SR=sf.read(f"{R}/mix.wav");N=len(m)
t=np.arange(N)/SR
ch=[[220,261.63,329.63],[174.61,220,261.63],[261.63,329.63,392],[196,246.94,293.66]]
seg=3.2;pad=np.zeros(N)
for i in range(int(N/SR/seg)+2):
    c=ch[i%4];a=int(i*seg*SR);b=min(N,int((i+1)*seg*SR+1.2*SR))
    if a>=N:break
    tt=t[a:b]-i*seg;env=np.clip(tt/1.2,0,1)*np.clip((seg+1.2-tt)/1.2,0,1)
    for f in c:
        for d in(-0.6,0.6):
            pad[a:b]+=env*(np.sin(2*np.pi*(f+d*0.3)*tt)+0.3*np.sin(2*np.pi*(f*2+d)*tt))
    pad[a:b]+=env*0.8*np.sin(2*np.pi*(c[0]/2)*tt)
bb,aa=ss.butter(2,1800/(SR/2));pad=ss.lfilter(bb,aa,pad)
pad*=1+0.15*np.sin(2*np.pi*0.2*t)
pad/=np.abs(pad).max()
fade=np.clip(t/1.0,0,1)*np.clip((N/SR-t)/1.2,0,1)
vo=np.convolve(np.abs(m),np.ones(int(0.15*SR))/int(0.15*SR),mode='same');vo=np.clip(vo/0.05,0,1)
duck=1-0.45*vo
pad*=0.085*fade*duck
out=m+pad;out/=max(1,np.abs(out).max()/0.95)
sf.write(f'{R}/mixm.wav',out,SR)
