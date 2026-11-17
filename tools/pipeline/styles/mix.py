import sys,json,numpy as np,soundfile as sf,scipy.signal as ss
D=sys.argv[1];kind=sys.argv[2]
T=json.load(open(D+'/tl.json'));tl=T['tl'];SR=24000
v,sr=sf.read(D+'/voice.wav');N=int((T['total']+0.3)*SR)
m=np.zeros(N);m[:len(v)]=v
rng=np.random.default_rng(1)
def whoosh(d=0.3):
    n=int(d*SR);x=rng.standard_normal(n);t=np.linspace(0,1,n)
    b,a=ss.butter(2,[300/(SR/2),3500/(SR/2)],'band');x=ss.lfilter(b,a,x)*np.sin(np.pi*t)**2
    return x/np.abs(x).max()*0.22
def pop(f=900,d=0.18):
    n=int(d*SR);t=np.arange(n)/SR;return np.sin(2*np.pi*f*t)*np.exp(-t*28)*0.28
def click(d=0.05):
    n=int(d*SR);t=np.arange(n)/SR;return rng.standard_normal(n)*np.exp(-t*90)*0.25
def chime():
    n=int(0.6*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*1046*t)+0.6*np.sin(2*np.pi*1568*t))*np.exp(-t*6)*0.2
def put(x,t):
    a=int(t*SR);b=min(N,a+len(x));
    if a<N:m[a:b]+=x[:b-a]
cues=json.load(open(D+'/cues.json'))
for t,k in cues:
    put({'w':whoosh(),'p':pop(),'c':click(),'ch':chime(),'p2':pop(1200)}[k],t)
sf.write(D+'/mix.wav',m,SR)
