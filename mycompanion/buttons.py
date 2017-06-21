import RPi.GPIO as GPIO
import time
import subprocess as sub

GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state_26 = GPIO.input(26)
    input_state_19 = GPIO.input(19)
    input_state_13 = GPIO.input(13)
    input_state_6 = GPIO.input(6)
    try:
        if input_state_26 == False:
            print('Button 2 Pressed')
            sub.call(['/bin/bash', '/home/pi/Documents/pyspace/restart_conscious_server.sh']) 
        if input_state_19 == False:
            print('Button 1 Pressed')
            sub.call(['sudo', '/home/pi/Documents/pyspace/restart_voiceassist.sh']) 
        if input_state_13 == False:
            print('Button 4 Pressed')
            sub.call(['/home/pi/Documents/pyspace/check_services.sh']) 
        if input_state_6 == False:
            print('Button 3 Pressed')
            sub.call(['sudo', '/home/pi/Documents/pyspace/restart_mycompanion.sh']) 
    except Exception as e:
        print("ERROR: {}".format(e))
