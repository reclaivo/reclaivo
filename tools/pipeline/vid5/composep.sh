#!/bin/sh
R=$1; cd /tmp/vid5/$R
ffmpeg -y -loglevel error -i base.mp4 -i mixm.wav -map 0:v -map 1:a -af "loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart final_m.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 final_m.mp4
