#!/bin/bash
yt-dlp --embed-thumbnail -S res,ext:mp4:m4a --recode mp4 $1 -N 4 -o './'$2'.%(ext)s'
echo "DONE"




























