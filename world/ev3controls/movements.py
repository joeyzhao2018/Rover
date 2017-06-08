from time import sleep

import os,json

_json_config=os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.json')
config_json=None
with open(_json_config) as data_file:
    config_json = json.load(data_file)
from ev3dev.ev3 import *


ir = InfraredSensor();assert ir.connected
ts = TouchSensor();assert ts.connected





motor_l=LargeMotor(config_json['motor1'])
motor_r=LargeMotor(config_json['motor2'])
_motors=[motor_l,motor_r]



def wait_till_finish():
    while any(m.state for m in _motors):
        sleep(0.1)


def turnleft():
    config=config_json['turn90']
    motor_l.run_timed(time_sp=config['time_sp'], speed_sp=config['speed'])
    motor_r.run_timed(time_sp=config['time_sp'], speed_sp=0-int(config['speed']))
    wait_till_finish()


def turnright():
    config = config_json['turn90']
    motor_l.run_timed(time_sp=config['time_sp'], speed_sp=0-int(config['speed']))
    motor_r.run_timed(time_sp=config['time_sp'], speed_sp=config['speed'])
    wait_till_finish()


def turnback():
    config = config_json['turn90']
    motor_l.run_timed(time_sp=2*config['time_sp'], speed_sp=0-int(config['speed']))
    motor_r.run_timed(time_sp=2*config['time_sp'], speed_sp=0-int(config['speed']))
    wait_till_finish()


def moveforward():
    config = config_json['default']
    for m in _motors:
        m.run_timed(time_sp=config['time_sp'], speed_sp=config['speed'])
    wait_till_finish()


def movebackward():
    config = config_json['default']
    for m in _motors:
        m.run_timed(time_sp=config['time_sp'], speed_sp=0-int(config['speed']))
    wait_till_finish()


def backup():
    config=config_json['default']
    for m in _motors:
        m.stop(stop_action='brake')
        m.run_timed(speed_sp=config['back_speed'], time_sp=config['back_time'])

def stop():
    for m in _motors:
        m.stop(stop_action='brake')


def wait():
    Sound.speak("i'm waiting")
    sleep(float(config_json['wait_time']))


def start(duty_cycle_sp):
    if duty_cycle_sp is None:
        duty_cycle_sp=config_json['default']['duty_cycle_sp']
    for m in _motors:
        m.run_direct(duty_cycle_sp=duty_cycle_sp)


def run_direct():
    btn = Button()
    while not btn.any():

        if ts.is_pressed:
            # We bumped an obstacle.
            # Back away, turn and go in other direction.
            stop()
            wait()
            start(0)

        # Infrared sensor in proximity mode will measure distance to the closest
        # object in front of it.
        distance = ir.proximity

        if distance > 60:
            # Path is clear, run at full speed.
            dc =config_json['default']['full_speed']
        else:
            # Obstacle ahead, slow down.
            dc = config_json['default']['slow_down']

        for m in _motors:
            m.duty_cycle_sp = dc

        sleep(0.1)


def _obstacle_hander_1():#wait
    stop()
    print("i'm waiting for it to move away")
    distance = ir.proximity
    while distance < 60:
        wait()
        distance=ir.proximity
    start(0)
    return 0


def _obstacle_hander_2(radius=45):#go around
    stop()
    turnleft()
    run_by_distance(radius)
    turnright()
    run_by_distance(radius)
    turnright()
    run_by_distance(radius)
    turnleft()

    start(0)
    return radius


def cm_to_rots(length):
    return length/0.056841


def cm_to_degrees(length):
    return 20.462778*length


def run_by_distance(distance, obstacle_handler=_obstacle_hander_1):
    starting_posn=motor_l.position
    print(starting_posn)
    distance_converted=cm_to_rots(distance)

    modification=0
    start(0)
    while not (motor_l.position-starting_posn-modification)>distance_converted:
        print("currently moved: {0}, target: {1}".format(motor_l.position-starting_posn-modification,distance_converted))
        if ts.is_pressed:
            modification=obstacle_handler()

        # Infrared sensor in proximity mode will measure distance to the closest object in front of it.
        distance = ir.proximity

        if distance > 60:
            # Path is clear, run at full speed.
            print("i can see {} clear in front of me".format(distance))
            dc =config_json['default']['full_speed']
        else:
            print("i notice someting {} in front of me".format(distance))
            # Obstacle ahead, slow down.

            modification = obstacle_handler()
            dc = config_json['default']['slow_down']
        print("setting dc={}".format(dc))

        for m in _motors:
            m.duty_cycle_sp = dc
        print("sleeping 0.1")
        sleep(0.1)
    stop()