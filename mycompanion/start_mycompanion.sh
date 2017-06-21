#!/bin/bash 

export XAUTHORITY=~/.Xauthority
export PYTHONPATH=.:/home/pi/Documents/pyspace

sudo mkdir -p /dev/shm/speech
sudo chmod -R 777 /dev/shm/speech 
cd /home/pi/Documents/pyspace
logfile=`date +%y%m%d_%H%M`
python3 world/conscious/server.py > /tmp/cons_${logfile}.log 2>&1 &
sleep 5
sudo python3 mycompanion.py > /tmp/mycomp_${logfile}.log 2>&1 &
