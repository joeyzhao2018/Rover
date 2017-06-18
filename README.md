# Rover
A. To start Server
1. cheng the "host" in ev3controls/config.json
2. run "python3 conscious/server.py" to start the server
3. run "python3 conscious/client.py [func] [parameter1] [parameter2] etc" to control the robot

B. Commands
alias jessiemove='python3 world/conscious/client.py'
1. jessiemove start_roaming
2. jessiemove stop_roaming #should always call stop_roaming if it's roaming before other instructions
