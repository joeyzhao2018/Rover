# Rover
A. To start Server
1. cheng the "host" in ev3controls/config.json
2. run "python3 conscious/server.py" to start the server
3. run "python3 conscious/client.py [func] [parameter1] [parameter2] etc" to control the robot

B. Commands
alias jessiemove='python3 world/conscious/client.py'
1. jessiemove start_roaming
2. jessiemove stop_roaming #should always call stop_roaming if it's roaming before other instructions
3. jessiemove go_to_location [the name of location in map.cfg]
4. jessiemove turnLeft
5. jessiemove turnRight
6. jessiemove turnBack
7. jessiemove go_straight
8. jessiemove stop
9. jessiemove mark [new location name]

   1,2 roaming have not been test
   3. has tested but changed a little bit
   there are other functions available for example "jessiemove turn east" or "jessiemove facingDirection" but
      commands translated from voices should not worry about those


C. Map2 in ev3control.map.cfg represents map.jpg  NOTE: the measures are not accurate

    __________________________________________        North
    |        |         |                      |        ^
    | Desk_A |         |                *     |  West<   >East
    |        |         |                ^     |        v
    |________|         |     MeetingRoom|     |       South
    |                  |                |     |
    |                  |                25    |
    |                  |__________      |     |
    |                                   |     |
    |                                   v     |
    |      *<----------50-------------->*     |
    |                ^                  ^     |
    |_________       |      _______     |     |
    |                |             |    |     |
    |                25            |    |     |
    |                |             |    |     |
    |                |             |    50    |
    |                v             |    |     |
    |__________      *             |    |     |
    |         |                    |    |     |
    | Desk_B  |                    |    v     |
    |         |                    |    *     |
    |         |                    | Door     |
    |_________|_______________________________|