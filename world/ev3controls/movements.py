from time import sleep
from multiprocessing import Process
import os,json
_json_config=os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.json')
config_json=None
with open(_json_config) as data_file:
    config_json = json.load(data_file)

cm_to_rots=float(config_json["cm_to_rots"])

import rpyc
conn = rpyc.classic.connect(host=config_json['host'],port=config_json['port']) # host name or IP address of the EV3
ev3 = conn.modules['ev3dev.ev3']      # import ev3dev.ev3 remotely
# import ev3dev.ev3 as ev3

ir = ev3.InfraredSensor()

motor_l=ev3.LargeMotor(config_json['motor1'])
motor_r=ev3.LargeMotor(config_json['motor2'])
_motors=[motor_l,motor_r]

try:
    ts = ev3.TouchSensor()
    motor_hand=ev3.MediumMotor(config_json['motor3'])
    motor_hand.run_to_abs_pos(speed_sp=20,position_sp=100)
except:
    motor_hand=None


def wait_till_finish():
    while any([m.state for m in _motors]):
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
    motor_l.run_timed(time_sp=2*int(config['time_sp']), speed_sp=0-int(config['speed']))
    motor_r.run_timed(time_sp=2*int(config['time_sp']), speed_sp=int(config['speed']))
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
    print("I'm stopping")
    for m in _motors:
        m.stop(stop_action='brake')
    return motor_l.position


def speak(words):
    ev3.Sound.speak(words)


def wait():
    speak("i'm waiting")
    sleep(float(config_json['wait_time']))


def start(duty_cycle_sp):
    if duty_cycle_sp is None:
        duty_cycle_sp=config_json['default']['duty_cycle_sp']
    for m in _motors:
        m.run_direct(duty_cycle_sp=duty_cycle_sp)


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


def cm_to_degrees(length):
    return 20.462778*length

def run_straight():
    start(0)
    distance = ir.proximity
    while distance!=0:
        distance = ir.proximity
        if distance > 60:
            dc =config_json['default']['full_speed']

            print("i can see {} clear in front of me".format(distance))
        else:
            print("i notice someting {} in front of me".format(distance))

            _obstacle_hander_1()
            dc = config_json['default']['slow_down']

        for m in _motors:
            m.duty_cycle_sp = dc
        sleep(0.1)


def moveforward():
    starting_posn=motor_l.position
    p = Process(target=run_straight)
    p.start()
    return starting_posn

def run_by_distance(distance, obstacle_handler=_obstacle_hander_1):
    distance_float=float(distance)
    starting_posn=motor_l.position
    print(starting_posn)
    distance_converted=distance_float/cm_to_rots

    modification=0
    start(0)
    while not float(motor_l.position-starting_posn-modification)>distance_converted:
        print("currently moved: {0}, target: {1}".format(motor_l.position-starting_posn-modification,distance_converted))
        # if ts.is_pressed:
        #     modification=obstacle_handler()

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


def fetchCoffee():
    if motor_hand is not None:
        motor_hand.run_to_abs_pos()
    else:
        speak("I don't have hands")


