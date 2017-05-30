
from ev3dev.ev3 import *

motor_l=LargeMotor('outB')
motor_r=LargeMotor('outA')


def turnleft():
    motor_l.run_timed(time_sp=1000, speed_sp=500)
    motor_r.run_timed(time_sp=1000, speed_sp=-500)


def turnright():
    motor_l.run_timed(time_sp=1000, speed_sp=-500)
    motor_r.run_timed(time_sp=1000, speed_sp=500)


def turnback():

    motor_l.run_timed(time_sp=2000, speed_sp=500)
    motor_r.run_timed(time_sp=2000, speed_sp=-500)


def moveforward():
    motor_l.run_timed(time_sp=1000, speed_sp=500)
    motor_r.run_timed(time_sp=1000, speed_sp=500)


def movebackward():
    motor_l.run_timed(time_sp=1000, speed_sp=-500)
    motor_r.run_timed(time_sp=1000, speed_sp=-500)