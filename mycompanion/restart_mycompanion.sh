#!/bin/bash 

for p in `ps -ef | grep "mycompanion.py" | grep -v grep |awk '{print $2}'`
do
    sudo kill -9 $p 2>/dev/null
done

espeak "Starting JPMC companion service"
export XAUTHORITY=~/.Xauthority
export PYTHONPATH=.:/home/pi/Documents/pyspace

sudo mkdir -p /dev/shm/speech
sudo chmod -R 777 /dev/shm/speech 
cd /home/pi/Documents/pyspace
logfile=`date +%y%m%d_%H%M`
sudo python3 mycompanion.py > /tmp/mycomp_${logfile}.log 2>&1 &
