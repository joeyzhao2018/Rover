from time import sleep
from ev3dev.ev3 import *

import os,json

_json_config=os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.json')

ir = InfraredSensor();assert ir.connected
ts = TouchSensor();assert ts.connected


with open(_json_config) as data_file:
    config_json = json.load(data_file)


motor_l=LargeMotor(config_json['motor1'])
motor_r=LargeMotor(config_json['motor2'])
_motors=[motor_l,motor_r]



def wait_till_finish():
    while any(m.state for m in _motors):
        sleep(0.1)

def turnleft():
    config=config_json['turn90']
    motor_l.run_timed(time_sp=config['time_sp'], speed_sp=config['speed'])
    motor_r.run_timed(time_sp=config['time_sp'], speed_sp=-config['speed'])
    wait_till_finish()

def turnright():
    config = config_json['turn90']
    motor_l.run_timed(time_sp=config['time_sp'], speed_sp=-config['speed'])
    motor_r.run_timed(time_sp=config['time_sp'], speed_sp=config['speed'])
    wait_till_finish()

def turnback():
    config = config_json['turn90']
    motor_l.run_timed(time_sp=2*config['time_sp'], speed_sp=-config['speed'])
    motor_r.run_timed(time_sp=2*config['time_sp'], speed_sp=-config['speed'])
    wait_till_finish()

def moveforward():
    config = config_json['default']
    for m in _motors:
        m.run_timed(time_sp=config['time_sp'], speed_sp=config['speed'])
    wait_till_finish()

def movebackward():
    config = config_json['default']
    for m in _motors:
        m.run_timed(time_sp=config['time_sp'], speed_sp=-config['speed'])
    wait_till_finish()


def stop():
    for m in _motors:
        m.stop(stop_action='brake')

def wait():
    Sound.speak("I am waiting")
    sleep(config_json['wait_time'])
    Sound.speak("I will go now")

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

