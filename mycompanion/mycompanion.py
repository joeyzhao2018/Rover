import socket
import os, os.path
import time
import sqlite3
import subprocess as sub
import threading
from threading import Timer
from db import DB
from utils import time_of_day
from roam import Roam
from goto_places import GotoLocation
 
class MyCompanion(object):
    SYNTHNSIZED_NAME = 3
    SID = 0

    def __init__(self, db_file):
        self.db_file = db_file
        self.db = DB(db_file)
        #self.create_tables()
        self.current_user = None

    def _say(self, message):
        sub.call(['sudo', 'tts_companion', message])

    def _get_response(self):
        p = sub.Popen(['sudo', 'speech-recog.sh', '-d', '5', '-o', '/dev/shm/speech'], stdout=sub.PIPE)
        response, err = p.communicate()
        print("response: {}, err: {}".format(response, err))
        return response[1:-1].upper().decode('ascii')

    def identify(self):
        from my_badge import Badge
        badge_reader = Badge()
        self._say("Please show me your badge")
        sid = badge_reader.read_badge()
        print("Identified as: {}".format(sid))
        self.db.insert_current_user(sid)
        info = self.db.fetch_user_info(sid) #self._fetch_user_info(sid)
        print("User info: {}".format(info))
        self.current_user = info[self.SID]
        self.db.update_current_user(info[self.SID], 'identify')
        self._say("Hi! " + info[self.SYNTHNSIZED_NAME] + ". Good " + time_of_day() + "!")
        #self._say("Hi! " + info[self.SYNTHNSIZED_NAME] + ". How can I help you?")
        #user_request = self._get_response()
        #print("User request: {}".format(user_request))

    def start_learning(self):
        pass

    def run_forecast(self):
        current_user = self.db.fetch_current_user()

        if not current_user:
            self._say("Please identify yourself before requesting a run")
            return 
        self._say("For which exercise?")
        exercise = self._get_response()
        self._say("For which scenario?")
        scenario = self._get_response()
 
        try:
            exercise = self.db.fetch_exercise_map(exercise)
        except:
            exercise = 'C CAR 2017'

        try:
            scenario = self.db.fetch_scenario_map(scenario)
        except:
            scenario = 'Baseline'
     
        from forecast.ccar import CCAR
        c = CCAR(self.db, current_user[0])

        self._say("Running forecast for {} {} scenario".format(exercise, scenario))
        pending_approvals = c.run(exercise, scenario)
        if pending_approvals:
            self.db.update_ccar_runs(c.run_id, 'PENDING APPROVAL')
            self._say("Approval needed to continue run. Sending email.")
            approval_timer = Timer(20.0, self.goto_approver, [pending_approvals[0][2]])
            approval_timer.start()

        run_complete_timer = Timer(60.0, self.mark_run_complete, [c.run_id])
        run_complete_timer.start()
  
    def goto_approver(self, sid):
        db = DB(self.db_file)
        user_info = db.fetch_user_info(sid)
        desk = user_info[4]
        self._say("Approval SLA has breached. Walking over to {} to request approval.".format(user_info[self.SYNTHNSIZED_NAME]))
        print("Going to approvers desk {}".format(desk))
        sub.call(['python3', 'world/conscious/client.py', 'go_to_location', desk]) 

    def mark_run_complete(self, run_id):
        db = DB(self.db_file)
        print("Calling DB to mark run completed")
        db.update_ccar_runs(run_id, 'COMPLETE')
  
    def go_to_my_desk(self):
        current_user = self.db.fetch_current_user()

        if not current_user:
            self._say("Please identify yourself before requesting to go to your desk")
            return
        user_info = self.db.fetch_user_info(current_user[0])
        print("Going to users desk {}".format(user_info[4]))
        sub.call(['python3', 'world/conscious/client.py', 'go_to_location', user_info[4]]) 

    
    def review_mevs(self):
        pass

    def review_forecast(self):
        pass

    def approve_forecast(self):
        pass

    def approve_mevs(self):
        pass

    def go_to_conf_room(self):
        print("Going to conference room")
        sub.call(['python3', 'world/conscious/client.py', 'go_to_location', 'MeetingRoom']) 

    def forecast_status(self):
        self._say("Please tell me forecast reference number")
        run_id = self._get_response()

        print("Response received: {}".format(run_id))
        status = self.db.fetch_ccar_runs_status(self.run_id)
        if "IN PROGRESS" == status:
            self._say("Run {} is in progress".format(self.run_id))
        elif "PENDING APPROVAL" == status:
            self._say("Run {} is waiting for approvals".format(self.run_id))
        elif "COMPLETE" == status:
            self._say("Run {} has completed".format(self.run_id))
        

    def logout(self):
        self.db.delete_current_user()
        self._say("It was pleasure to assist you today. Goodbye.")

    def plot_us_gdp(self):
        pass

    def plot_unemp_rate(self):
        pass

    def plot_libor_rate(self):
        pass

    def plot_all_scenarios(self):
        pass

    def approve_mevs(self):
        pass

    def plot_forecast(self):
        pass

    def plot_seasonality(self):
        pass

    def plot_trend(self):
        pass

    def plot_mean_and_stddev(self):
        pass

    def record_summary(self):
        self._say("Please proceed")
        self.summary = self._get_response()
       

    def send_summary(self):
        #email.send(self.summary, address)
        pass

    def presentation_on(self):
        pass

    def presentation_off(self):
        pass

    def record_name(self):
        pass

    def record_desk(self):
        pass

    def record_path(self):
        pass

    def end_learning(self):
        pass


    def process_command(self, command):
        #self.db.insert_current_user('W535148')
        if self.validate_instruction(command):
            print('Processing command...{}'.format(command))
            options = self.db.fetch_activities(command)
            db_conn = sqlite3.connect(self.db_file)
            c = db_conn.cursor()
            c.execute("SELECT ID, NAME, PARENT_ID, PROCESSOR FROM ACTIVITIES WHERE upper(PROCESSOR)='" + command.upper() + "' order by NAME")
            all_rows = c.fetchall()
            if not all_rows:
                print("Found unknown command. Command given: {}".format(command)) 
            else:
                print("executing command instructions...{}".format(all_rows))
                getattr(self, command)()

    def start_roaming(self):
       self.roaming_thread = Roam(1, 'roaming')
       self.roaming_thread.start()

    def stop_roaming(self):
       self.roaming_thread.exit_flag=1
       
    def validate_instruction(self, instruction):
        #db_conn = sqlite3.connect(self.db_file)
        #c = db_conn.cursor()
        try:
            #c.execute("SELECT * FROM CURRENT_USER")
            print("validating instructions")
            current_user = self.db.fetch_current_user()
            if not current_user:
                return True
            print("==== current user ===", current_user)
            user = current_user[0]
            current_menu = current_user[2]
            print("Current User: {}".format(current_user))
            user_info = self.db.fetch_user_info(user) 
            print("User Info: {}".format(user_info))
            if not user_info:
                self._say("Not a registered user !! Please register yourself with mycompanion tech team ")
                return False
            allowed_activities = self.db.fetch_activities(current_user[3])
            print("Allowed activities: {}".format(allowed_activities))
            parent_menu = allowed_activities[0][2]
            if current_menu != parent_menu:
                valid_options = ", ".join([o[1] for o in allowed_activities])
                self._say(instruction + " is not a valid option for this Menu. Valid options are " + valid_options)
                return False
            else:
                return True
        except Exception as e:
            print("ERROR: {}".format(e))
            return False




if os.path.exists( "/tmp/python_unix_sockets_example" ):
  os.remove( "/tmp/python_unix_sockets_example" )
 
print("Opening socket...")
server = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
server.bind("/tmp/python_unix_sockets_example")
db_file = "/var/www/html/database/mycompanion.sqlite"

my_comp = MyCompanion(db_file)

print("Listening...")

my_comp._say("Good " + time_of_day() + "! Your companion at JPMC is active")
#my_comp.start_roaming()

while True:

  print("started listening")
  datagram = server.recv(1024)
  print("datagram", datagram)
  if not datagram:
    break
  else:
    print("-" * 20)
    print(datagram)
    
    #my_comp.stop_roaming()
    try:
        my_comp.process_command(datagram.decode()) 
    except Exception as e:
        print("ERROR: {}".format(e))

    if "DONE" == datagram:
      break
print("-" * 20)
print("Shutting down...")
server.close()
os.remove( "/tmp/python_unix_sockets_example" )
print("Done")

