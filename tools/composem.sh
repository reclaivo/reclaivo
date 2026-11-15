#!/bin/sh
R=$1; cd /tmp/vid5/$R
ffmpeg -y -loglevel error -i base.mp4 -framerate 30 -i ins/%04d.png -i mixm.wav -filter_complex "[0:v][1:v]overlay=format=auto:shortest=1[v]" -map "[v]" -map 2:a -af "loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000" -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart final_m.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 final_m.mp4
