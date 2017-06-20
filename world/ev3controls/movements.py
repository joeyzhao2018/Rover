from time import sleep
from multiprocessing import Process
import os,json
_json_config=os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.json')
config_json=None
with open(_json_config) as data_file:
    config_json = json.load(data_file)
distance_detect=float(config_json["distance_detect"])
cm_to_rots=float(config_json["cm_to_rots"])
duty_diff=float(config_json["duty_diff"])
import rpyc
conn = rpyc.classic.connect(host=config_json['host'],port=config_json['port']) # host name or IP address of the EV3
ev3 = conn.modules['ev3dev.ev3']      # import ev3dev.ev3 remotely
# import ev3dev.ev3 as ev3

ir = ev3.InfraredSensor()
print(ir.proximity)
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


def turnleft():
    config=config_json['turnLeft']
    motor_l.run_timed(time_sp=float(config['time_sp_l']), speed_sp=float(config['speed']))
    sleep(4)
    motor_r.run_timed(time_sp=float(config['time_sp_r']), speed_sp=0-float(config['speed']))
    wait_till_finish()


def turnright():
    config = config_json['turnRight']
    motor_r.run_timed(time_sp=float(config['time_sp_l']), speed_sp=float(config['speed']))
    sleep(4)
    motor_l.run_timed(time_sp=float(config['time_sp_r']), speed_sp=0-float(config['speed']))
    wait_till_finish()


def turnback():
    turnleft()
    turnleft()
    # config = config_json['turn180']
    # motor_l.run_timed(time_sp=2*float(config['time_sp']), speed_sp=0-float(config['speed']))
    # motor_r.run_timed(time_sp=2*float(config['time_sp']), speed_sp=float(config['speed']))
    wait_till_finish()


def movebackward():
    config = config_json['default']
    for m in _motors:
        m.run_timed(time_sp=config['time_sp'], speed_sp=0-float(config['speed']))
    wait_till_finish()


def backup():
    config=config_json['default']
    for m in _motors:
        m.stop(stop_action='brake')
        m.run_timed(speed_sp=float(config['back_speed']), time_sp=config['back_time'])


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

        if distance > distance_detect:
            # Path is clear, run at full speed.
            print("i can see {} clear in front of me".format(distance))
            dc =float(config_json['default']['full_speed'])
        else:
            print("i notice someting {} in front of me".format(distance))
            # Obstacle ahead, slow down.

            modification = obstacle_handler()
            dc = float(config_json['default']['slow_down'])
        print("setting dc={}".format(dc))

        motor_l.duty_cycle_sp = max(dc-duty_diff,0)
        motor_r.duty_cycle_sp = max(dc,0)
        print("sleeping 0.1")
        sleep(0.1)
    stop()


def fetchCoffee():
    if motor_hand is not None:
        motor_hand.run_to_abs_pos()
    else:
        speak("I don't have hands")

color_sensor=ev3.ColorSensor()
color_sensor.mode='COL-REFLECT'


def ajust(turn_left_sig,turn_right_sig,go_sig,stop_sig):
    while color_sensor.color != go_sig and color_sensor.color != stop_sig:
        print("adjust color {}".format(str(color_sensor.color)))
        if color_sensor.color == turn_left_sig:
            motor_l.speed_sp = 10
            motor_r.speed_sp = -10
        elif color_sensor.color == turn_right_sig:
            motor_r.speed_sp = 10
            motor_l.speed_sp = -10
        sleep(0.1)


def run_by_color(turn_left_sig,turn_right_sig,go_sig,stop_sig):
    print("color {}".format(str(color_sensor.color)))
    motor_l.run_direct(speed_sp=0)
    motor_r.run_direct(speed_sp=0)
    while color_sensor.color !=stop_sig:
        motor_l.speed_sp=50
        motor_r.speed_sp=50
        print("going color {}".format(str(color_sensor.color)))
        if color_sensor.color!=go_sig:
            if color_sensor.color==stop_sig:
                stop()
            else:
                ajust(turn_left_sig,turn_right_sig,go_sig,stop_sig)
        sleep(0.1)
    stop()