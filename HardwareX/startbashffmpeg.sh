#!/bin/bash


sudo raspivid -t 0 -w 680 -h 480 -fps 20 -g 75 -b 200000 -n -rot 90 -o - | ffmpeg  -i - -c:v copy -r 20 -bsf dump_extra -maxrate 100K -bufsize 80K -tune zerolatency -f rtp rtp://127.0.0.1:5004?pkt_size=1300

