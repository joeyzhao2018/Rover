import sys
import json
import subprocess as sub

class MyCompanion(object):
    def __init__():
        pass

    def execute(self, command):
        print('command is {}'.format(command))

if __name__ == "__main__":
    activity_d = json.load(open('~/.activity_map'))
    current_user_d = json.load(open('~/.current_user'))
    current_activity = current_user['current_activity']

    command = sys.argv[0]
    if not current_activity and command in activity.keys():
        current_user_d.update({'current_activity': command})
        execute(command)
    else:
        sub.call(['sudo', 'tts', 'Available options are..... ' + str(activity_d.keys())])
    if command not in activity.get(current_activity:
        sub.call(['sudo', 'tts', 'Available options are..... ' + str(eval("activity_d["+current_activity.split(".")+"]")])])
    else:
        
        execute(command) 
