import sqlite3

class DB(object):
    def __init__(self, db_file):
        self.db_file = db_file
        self.db_conn = sqlite3.connect(self.db_file)

    def __enter__(self):
        pass
    
    def __exit__(self):
        self.db_conn.commit()
    
    def fetch_current_user(self):
        c = self.db_conn.cursor()
        c.execute("select SID, LOGON_TIME, ACTIVITY_ID, PROCESSOR from current_user u, ACTIVITIES a WHERE u.ACTIVITY_ID=a.ID")
        user_info = c.fetchall()
        print("*** user_info ***")
        print(user_info)
        #db_conn.close()
        return user_info[0]

    def fetch_user_info(self, sid):
        #db_conn = sqlite3.connect(self.db_file)
        c = self.db_conn.cursor()
        c.execute("select * from users where sid='" + sid + "'")
        user_info = c.fetchall()
        #db_conn.close()
        if user_info:
            return user_info[0]
        return None

    def fetch_activities(self, command):
        #db_conn = sqlite3.connect(self.db_file)
        c = self.db_conn.cursor()
        print("Fetching activites for {}".format(command))
        if command:
            c.execute("SELECT ID, NAME, PARENT_ID, PROCESSOR FROM ACTIVITIES WHERE PARENT_ID in (select ID from ACTIVITIES where upper(PROCESSOR)='" + command.upper() + "') order by NAME")
        else:
            c.execute("SELECT ID, NAME, PARENT_ID, PROCESSOR FROM ACTIVITIES WHERE PARENT_ID = -1 order by NAME")
        all_activities = c.fetchall()
        return all_activities

    def fetch_current_activity(self, sid):
        c = self.db_conn.cursor()
        if not sid:
            return None
        c.execute("SELECT ID, NAME, PARENT_ID, PROCESSOR FROM ACTIVITIES WHERE ID = (select current_activity from current_user where sid='" + sid + "')")
        current_activity = c.fetchall()
        if current_activity:
            return current_activity[0]
        return None

    def insert_current_user(self, sid):
        c = self.db_conn.cursor()
        if not sid:
            return -1
        try:
            c.execute("INSERT INTO CURRENT_USER (SID, LOGON_TIME, ACTIVITY_ID) VALUES (sid, current_timestamp, 1)")
            self.db_conn.commit()
            return 1 
        except:
            return 0

    def update_current_user(self, sid, activity):
        c = self.db_conn.cursor()
        if not sid:
            print("Can't update user info. SID is None")
            return -1
        try:
            print("Updating current user info")
            c.execute("UPDATE CURRENT_USER set LOGON_TIME=current_timestamp, ACTIVITY_ID=(select ID from activities where processor='" + activity + "') where SID='" + sid + "'")
            self.db_conn.commit()
            return 1
        except:
            print("Couldn't update user info")
            return 0

    def delete_current_user(self):
        c = self.db_conn.cursor()
        c.execute("DELETE FROM CURRENT_USER")
        self.db_conn.commit()

    def insert_ccar_runs(self, exercise, scenario, sid):
        c = self.db_conn.cursor()
        if not sid:
            return -1
        try:
            r = c.execute("INSERT INTO CCAR_RUNS (ID,EXERCISE,SCENARIO,STARTED_BY,STATUS) VALUES (NULL,'" + exercise + "','" + scenario + "','" + sid + "','IN PROGRESS')")
            self.db_conn.commit()
            print("Run inserted: {}".format(r.lastrowid))
            return r.lastrowid
        except:
            return 0
     
    def update_ccar_runs(self, run_id, status):
        c = self.db_conn.cursor()
        try:
            print("Marking run {} {}".format(run_id, status))
            c.execute("UPDATE CCAR_RUNS SET STATUS='" + status + "' where ID=" + str(run_id))
            self.db_conn.commit()
            return 1
        except Exception as e:
            print("ERROR: {}".format(e))
            return -1
        
    def fetch_ccar_runs_status(self, run_id):
        c = self.db_conn.cursor()
        try:
            print("Fetching run status for {}".format(run_id))
            c.execute("Select status from CCAR_RUNS where ID=" + str(run_id))
            status_l =  c.fetchall()
            if status_l:
                return status_l[0][5]
        except Exception as e:
            print("ERROR: {}".format(e))
        return "IN PROGRESS"

    def fetch_mevs(self):
        c = self.db_conn.cursor()
        try:
            c.execute("SELECT * from MEVS")
            return c.fetchall()
        except:
            return None

    def fetch_unapproved_mevs(self):
        c = self.db_conn.cursor()
        try:
            c.execute("SELECT * from MEVS where approved_on is null")
            return c.fetchall()
        except:
            return None

    def fetch_exercise_map(self, exercise):
        c = self.db_conn.cursor()
        c.execute("SELECT exercise from exercise_map where translated='" + exercise.upper() + "'")
        return c.fetchone()[0]

    def fetch_scenario_map(self, scenario):
        c = self.db_conn.cursor()
        c.execute("SELECT scenario from scenario_map where translated='" + scenario.upper() + "'")
        return c.fetchone()[0]

    def create_tables(self):
        #db_conn = sqlite3.connect(self.db_file)
        c = self.db_conn.cursor()
        try:
            c.execute("SELECT * FROM USERS") 
            user = c.fetchone()
        except:
            # Current User
            c.execute("CREATE TABLE CURRENT_USER ( SID VARCHAR(15), LOGON_TIME DATETIME, ACTIVITY_ID INT)")

            # USERS
            c.execute("CREATE TABLE USERS (SID VARCHAR(15) PRIMARY KEY, FIRST_NAME VARCHAR(15), LAST_NAME VARCHAR(15), SYNTHNSIZED_NAME VARCHAR(15), DESK VARCHAR(2), ROLE VARCHAR(25))")
            # activities
            c.execute("CREATE TABLE ACTIVITIES (ID INT, NAME VARCHAR(126), PARENT_ID INT DEFAULT -1, PROCESSOR VARCHAR(56))")
        
            self.populate_data(c)
        #db_conn.commit()
        #db_conn.close()

    def populate_data(self, c):
        # add users
        c.execute("INSERT OR IGNORE INTO USERS (SID, FIRST_NAME, LAST_NAME, SYNTHNSIZED_NAME, DESK, ROLE) VALUES ('V654950', 'Bharat', 'Patel', 'Bharrat', 'B', 'Forecaster')")

       # add activities
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (1, 'Identify', -1, 'identify')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (2, 'Turn on learning mode', -1, 'start_learning')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (3, 'Run Forecast', 1, 'run_forecast')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (4, 'Review MEVs', 1, 'review_mevs')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (5, 'Review Forecast', 1, 'review_forecast')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (6, 'Approve Forecast', 1, 'approve_forecast')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (7, 'Approve MEVs', 1, 'approve_mevs')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (8, 'Go to conference room', 1, 'go_to_conf_room')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (9, 'Forecast status', 1, 'forecast_status')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (10, 'Logout', 1, 'logout')")

        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (11, 'Plot US GDP', 4, 'plot_us_gdp')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (12, 'Plot Unemployment Rate', 4, 'plot_unemp_rate')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (13, 'Plot Libor Rate', 4, 'plot_libor_rate')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (14, 'Plot all scenarios', 4, 'plot_all_scenarios')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (15, 'Approve', 4, 'approve_mevs')")

        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (16, 'Plot forecast', 5, 'plot_forecast')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (17, 'Plot seasonality', 5, 'plot_seasonality')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (18, 'Plot trend', 5, 'plot_trend')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (19, 'Plot rolling mean and standard deviation', 5, 'plot_mean_and_stddev')")

        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (20, 'Record summary', 8, 'record_summary')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (21, 'Send summary', 8, 'send_summary')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (22, 'Turn presentation mode on', 8, 'presentation_on')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (23, 'Turn presentation mode off', 8, 'presentation_off')")

        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (24, 'Record name', 2, 'record_name')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (25, 'Record desk', 2, 'record_desk')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (26, 'Record path', 2, 'record_path')")
        c.execute("INSERT OR IGNORE INTO ACTIVITIES (ID, NAME, PARENT_ID, PROCESSOR) VALUES (27, 'Turn off learning mode', 2, 'end_learning')")

  
