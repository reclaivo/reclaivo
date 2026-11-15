#!/bin/bash
# Rebuilds the reel workspace in a fresh cloud session. Safe to re-run.
set -e
P="$(cd "$(dirname "$0")" && pwd)"
mkdir -p /tmp/vid2 /tmp/t3d/char /tmp/vid5 /tmp/tts
cp "$P/vid2/build4.py" /tmp/vid2/; rm -rf /tmp/vid2/img; cp -r "$P/vid2/img" /tmp/vid2/img
cp "$P"/t3d/{audio_t.py,insert.html,ins.py,package.json} /tmp/t3d/; cp "$P/t3d/char/pose5.png" /tmp/t3d/char/
cp "$P"/vid5/{patch7.py,music.py,composem.sh,composep.sh} /tmp/vid5/; chmod +x /tmp/vid5/*.sh
cp "$P/tts/tts2.py" /tmp/tts/
mkdir -p /mnt/user-data/outputs/reclaivo-ima/images; cp "$P"/site-img/*.jpg /mnt/user-data/outputs/reclaivo-ima/images/
pip install -q --break-system-packages sherpa-onnx numpy scipy soundfile pillow playwright 2>&1 | tail -1 || true
if [ ! -f /tmp/tts/kokoro-multi-lang-v1_0/model.onnx ]; then
  cd /tmp/tts && curl -sSL -o m.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-multi-lang-v1_0.tar.bz2 && tar xjf m.tar.bz2 && rm m.tar.bz2
fi
if [ ! -d /tmp/t3d/node_modules/three ]; then cd /tmp/t3d && npm install --silent three@0.160.0; fi
echo SETUP_OK
