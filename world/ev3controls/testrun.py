import os,json
_json_config=os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.json')
config_json=None
with open(_json_config) as data_file:
    config_json = json.load(data_file)

import rpyc
conn = rpyc.classic.connect(host=config_json['host'],port=config_json['port']) # host name or IP address of the EV3
ev3 = conn.modules['ev3dev.ev3']      # import ev3dev.ev3 remotely
# import ev3dev.ev3 as ev3

motor_l=ev3.LargeMotor(config_json['motor1'])
motor_r=ev3.LargeMotor(config_json['motor2'])

motor_l.run_timed(time_sp=2*1048, speed_sp=-400)
motor_r.run_timed(time_sp=2*1048, speed_sp=400)
motor_l.run_timed(time_sp=500, speed_sp=-400)
motor_r.run_timed(time_sp=500, speed_sp=-400)

motor_l.stop(stop_action='brake')
motor_r.stop(stop_action='brake')