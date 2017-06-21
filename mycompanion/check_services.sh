#!/bin/bash

for p in `ps -ef | grep voicecommand | grep -v grep |awk '{print $2}'`
do
    espeak "Voice command service is running"
    break
done

for p in `ps -ef | grep server.py | grep -v grep |awk '{print $2}'`
do
    espeak "Conscious service is running"
    break
done

for p in `ps -ef | grep mycompanion | grep -v grep |awk '{print $2}'`
do
    espeak "JPMC companion service is running"
    break
done
