#!/bin/bash

for p in `ps -ef | grep voicecommand | grep -v grep |awk '{print $2}'`
do
    sudo kill -9 $p 2>/dev/null
done

espeak "Starting voicecommand service"
sudo voicecommand -c -i &
