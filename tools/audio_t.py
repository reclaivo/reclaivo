import sys, json, numpy as np, soundfile as sf
sys.path.insert(0,'/tmp/tts')
from tts2 import make
SID=int(sys.argv[1]) if len(sys.argv)>1 else 3
SPEED=1.08
LINES=["Your content needs to be seen.","Let me show you how."]
tts=make(); SR=24000
def trim(x,th=0.012):
    idx=np.where(np.abs(x)>th)[0]
    return x[idx[0]:idx[-1]+1] if len(idx) else x
clips=[]
for t in LINES:
    a=np.array(tts.generate(t,sid=SID,speed=SPEED).samples,dtype=np.float32)
    a=trim(a); a/=max(1e-6,np.abs(a).max()); a*=0.9
    f=int(0.01*SR); a[:f]*=np.linspace(0,1,f); a[-f:]*=np.linspace(1,0,f)
    clips.append(a)
GAP=int(0.10*SR); t0=0; tl=[]; parts=[]
for a in clips:
    tl.append((t0/SR,(t0+len(a))/SR)); parts.append(a); parts.append(np.zeros(GAP,np.float32)); t0+=len(a)+GAP
voice=np.concatenate(parts)
total=len(voice)/SR
sf.write('voice.wav',voice,SR)
json.dump({'lines':LINES,'tl':tl,'total':total},open('tl.json','w'))
print([ (round(a,2),round(b,2)) for a,b in tl],'total',round(total,2))
