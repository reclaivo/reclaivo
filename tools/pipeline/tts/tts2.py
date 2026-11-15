import sherpa_onnx, numpy as np, soundfile as sf, sys
D='/tmp/tts/kokoro-multi-lang-v1_0/'
def make():
    cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(model=D+'model.onnx',voices=D+'voices.bin',tokens=D+'tokens.txt',data_dir=D+'espeak-ng-data',lexicon=D+'lexicon-us-en.txt',dict_dir=D+'dict'),num_threads=4,provider='cpu'))
    return sherpa_onnx.OfflineTts(cfg)
if __name__=='__main__':
    tts=make(); print('spk',tts.num_speakers,tts.sample_rate)
    for sid in range(0,11):
        a=tts.generate("Brands, your influencer forgot to label the ad? That is on you too.",sid=sid,speed=1.1)
        if len(a.samples): sf.write(f'w{sid}.wav',np.array(a.samples,dtype=np.float32),int(a.sample_rate)); print(sid,round(len(a.samples)/a.sample_rate,2))
