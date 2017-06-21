from time import sleep
from multiprocessing import Process
import os,json
_json_config=os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.json')
config_json=None
with open(_json_config) as data_file:
    config_json = json.load(data_file)
distance_detect=float(config_json["distance_detect"])
adjusting_dc=float(config_json["adjusting_dc"])
cm_to_rots=float(config_json["cm_to_rots"])
duty_diff=float(config_json["duty_diff"])
# color_mode=True
turn_left_sig=int(config_json["turn_left_color"])
turn_right_sig=int(config_json["turn_right_color"])
go_sig=int(config_json["go_color"])
go_sig_alt=int(config_json["go_color_alter"])
stop_sig=int(config_json["stop_color"])

import rpyc
conn = rpyc.classic.connect(host=config_json['host'],port=config_json['port']) # host name or IP address of the EV3
ev3 = conn.modules['ev3dev.ev3']      # import ev3dev.ev3 remotely
# import ev3dev.ev3 as ev3

ir = ev3.InfraredSensor()
print(ir.proximity)
col = ev3.ColorSensor()
col.mode = 'COL-REFLECT'
print(col.color)
motor_l=ev3.LargeMotor(config_json['motor1'])
motor_r=ev3.LargeMotor(config_json['motor2'])
_motors=[motor_r,motor_l]

try:
    ts = ev3.TouchSensor()
    motor_hand=ev3.MediumMotor(config_json['motor3'])
    motor_hand.run_to_abs_pos(speed_sp=20,position_sp=100)
except:
    motor_hand=None


def wait_till_finish():
    while any([m.state for m in _motors]):
        sleep(0.1)


def turn_adjust(left_or_right):
    config_1 = config_json['default']
    duty_cycle= config_1['duty_cycle_sp']
    if col.color != 1:
        while col.color not in [go_sig,turn_right_sig,left_or_right]:
            print("color is", col.color)
            print("moving to find black")
            if left_or_right=='right':
                motor_r.run_direct(duty_cycle_sp=duty_cycle)
                motor_l.run_direct(duty_cycle_sp=0 - int(duty_cycle))
            else:
                motor_l.run_direct(duty_cycle_sp=duty_cycle)
                motor_r.run_direct(duty_cycle_sp=0 - int(duty_cycle))
            sleep(0.2)
        print("color Found is ", col.color)
        motor_r.duty_cycle_sp=0
        motor_l.duty_cycle_sp=0


def turnleft(color_mode=True):
    config=config_json['turnLeft']
    motor_l.run_timed(time_sp=config['time_sp_l'], speed_sp=config['speed'])
    motor_r.run_timed(time_sp=config['time_sp_r'], speed_sp=0-int(config['speed']))
    wait_till_finish()
    if color_mode:
        turn_adjust('left')


def turnright(color_mode=True):
    config = config_json['turnRight']
    motor_r.run_timed(time_sp=config['time_sp_r'], speed_sp=config['speed'])
    motor_l.run_timed(time_sp=config['time_sp_l'], speed_sp=0-int(config['speed']))
    wait_till_finish()
    if color_mode:
        turn_adjust('right')


def turnback(color_mode=True):
    config = config_json['turn180']
    motor_l.run_timed(time_sp=2*int(config['time_sp_l']), speed_sp=0-int(config['speed']))
    motor_r.run_timed(time_sp=2*int(config['time_sp_r']), speed_sp=int(config['speed']))
    wait_till_finish()
    if color_mode:
        turn_adjust('right')


def movebackward():
    config = config_json['default']
    for m in _motors:
        m.run_timed(time_sp=config['time_sp'], speed_sp=0-float(config['speed']))
    wait_till_finish()


def backup():
    config=config_json['default']
    for m in _motors:
        # m.stop(stop_action='brake')
        m.duty_cycle_sp=float(config['back_speed'])
        # m.run_timed(speed_sp=float(config['back_speed']), time_sp=config['back_time'])


def stop():
    print("I'm stopping")
    for m in _motors:
        m.duty_cycle_sp=0
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
    while distance < distance_detect:
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
        if distance > distance_detect:
            dc =float(config_json['default']['full_speed'])

            print("i can see {} clear in front of me".format(distance))
        else:
            print("i notice someting {} in front of me".format(distance))

            _obstacle_hander_1()
            dc = float(config_json['default']['slow_down'])

        motor_l.duty_cycle_sp = max(dc - duty_diff,0)
        motor_r.duty_cycle_sp = max(dc,0)
        sleep(0.1)


def moveforward():
    starting_posn=motor_l.position
    p = Process(target=run_straight)
    p.start()
    return starting_posn


def run_by_distance(distance, facingDirection):
    distance_float=float(distance)
    starting_posn=motor_l.position
    print(starting_posn)
    distance_converted=distance_float/cm_to_rots
    # modification=0
    start(0)
    while not float(motor_l.position-starting_posn)>distance_converted:

        if col.color not in [go_sig, go_sig_alt]:
            # if col.color==stop_sig:
            #     while col.color==stop_sig:
            #         backup()
            #         sleep(0.4)
            ajust(facingDirection)
        distance = ir.proximity

        if distance > distance_detect:
            # print("i can see {} clear in front of me".format(distance))
            dc =float(config_json['default']['full_speed'])
        else:
            # print("i notice someting {} in front of me".format(distance))
            # Obstacle ahead, slow down.
            _obstacle_hander_1()
            dc = float(config_json['default']['slow_down'])
        # print("setting dc={}".format(dc))

        motor_l.duty_cycle_sp = max(dc-duty_diff,0)
        motor_r.duty_cycle_sp = max(dc,0)

        # print("sleeping 0.1")
    stop()


def fetchCoffee():
    if motor_hand is not None:
        motor_hand.run_to_abs_pos()
    else:
        speak("I don't have hands")


def ajust(facingDirection):
    while col.color not in [go_sig, go_sig_alt, stop_sig]:
        print("adjust color {}".format(str(col.color)))
        if col.color == turn_left_sig:
            if facingDirection in [0,3]:
                motor_l.duty_cycle_sp = adjusting_dc
                motor_r.duty_cycle_sp = 0
            else:
                motor_l.duty_cycle_sp = 0
                motor_r.duty_cycle_sp = adjusting_dc
        elif col.color == turn_right_sig:
            if facingDirection in [0,3]:
                motor_l.duty_cycle_sp = 0
                motor_r.duty_cycle_sp = adjusting_dc
            else:
                motor_l.duty_cycle_sp = adjusting_dc
                motor_r.duty_cycle_sp = 0
    # if col.color==stop_sig:
    #     while col.color==stop_sig:
    #         backup()
    #         sleep(0.4)


# def run_by_color():
#     print("color {}".format(str(col.color)))
#     motor_l.run_direct(duty_cycle_sp=0)
#     motor_r.run_direct(duty_cycle_sp=0)
#     while col.color !=stop_sig:
#         motor_l.duty_cycle_sp=50
#         motor_r.duty_cycle_sp=50
#         print("going color {}".format(str(col.color)))
#         if col.color!=go_sig:
#             if col.color==stop_sig:
#                 stop()
#             else:
#                 ajust()
#         sleep(0.1)
#     stop()