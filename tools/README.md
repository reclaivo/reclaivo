# Reel pipeline (for weekly runs)
- build4.py: 2D template (HTML timeline, Playwright frames, ffmpeg). patch6.py generates per-reel build5.py (edit LINESETS/CFG for new reels, run `python3 patch6.py`, then per reel: `python3 audio.py; python3 build5.py`).
- audio_t.py: Kokoro TTS via sherpa-onnx (models in /tmp/tts, kokoro-multi-lang-v1_0). Words missing from the lexicon are skipped silently: reword them.
- insert.html + ins.py: transparent Three.js 3D inserts (need npm three@0.160 in /tmp/t3d and `python3 -m http.server 8123` there).
- music.py: soft ambient pad ducked under voice. compose.sh / composem.sh: overlay inserts, mix audio.
