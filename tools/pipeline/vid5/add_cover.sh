#!/bin/sh
# usage: add_cover.sh in.mp4 out.mp4 [cover_time_seconds]
# Makes the very first frame the designed cover (hook fully shown) so Reels uses it as the thumbnail. Also writes out.cover.png
IN=$1; OUT=$2; T=${3:-0.9}
ffmpeg -y -loglevel error -ss $T -i "$IN" -frames:v 1 "${OUT%.mp4}.cover.png"
ffmpeg -y -loglevel error -i "$IN" -i "${OUT%.mp4}.cover.png" -filter_complex "[0:v][1:v]overlay=enable='eq(n,0)'[v]" -map "[v]" -map 0:a -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"
