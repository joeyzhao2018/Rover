#/bin/bash

for p in `ps -ef | grep "server.py" | grep -v grep |awk '{print $2}'`
do
    sudo kill -9 $p 2>/dev/null
done

espeak "Starting conscious service"
export PYTHONPATH=.:/home/pi/Documents/pyspace
cd /home/pi/Documents/pyspace
logfile=`date +%y%m%d_%H%M`
python3 world/conscious/server.py > /tmp/cons_${logfile}.log 2>&1 &
