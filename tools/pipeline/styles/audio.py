import sys, json, numpy as np, soundfile as sf
sys.path.insert(0,'/tmp/tts')
from tts2 import make
out=sys.argv[1]; LINES=json.load(open(out+'/lines.json'))
SID=3; SPEED=1.08
lex=set(l.split()[0] for l in open('/tmp/tts/kokoro-multi-lang-v1_0/lexicon-us-en.txt'))
import re
oov=[w for L in LINES for w in re.findall(r"[a-z']+",L.lower()) if w not in lex]
print('OOV',oov)
tts=make(); SR=24000
def trim(x,th=0.012):
    idx=np.where(np.abs(x)>th)[0]
    return x[idx[0]:idx[-1]+1] if len(idx) else x
parts=[];tl=[];t0=0;GAP=int(0.10*SR)
for t in LINES:
    a=np.array(tts.generate(t,sid=SID,speed=SPEED).samples,dtype=np.float32)
    a=trim(a); a/=max(1e-6,np.abs(a).max()); a*=0.9
    f=int(0.01*SR); a[:f]*=np.linspace(0,1,f); a[-f:]*=np.linspace(1,0,f)
    tl.append((t0/SR,(t0+len(a))/SR)); parts+= [a,np.zeros(GAP,np.float32)]; t0+=len(a)+GAP
v=np.concatenate(parts); sf.write(out+'/voice.wav',v,SR)
json.dump({'lines':LINES,'tl':tl,'total':len(v)/SR},open(out+'/tl.json','w'))
print([(round(a,2),round(b,2)) for a,b in tl],'total',round(len(v)/SR,2))
