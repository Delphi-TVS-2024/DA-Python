# get the latest files
# logging added
# all tables looped  check url , file format ,
# counter adding complete
# create a log file  automatically and rotate files | check again
# object creation
# if json file corrupted new json will create and logs will update
# Creating custom csv file logging
# create separate thread for Alerts
# extra Spaces added while print filename for raw tables
# visualise json to keep in same as log file


import requests
import os
import regex as re
import time
from datetime import datetime
import json, csv


class StartSending:

    def __init__(self, TOKEN_URL, TABLE_URL, FILE_DIR, gen_table_list, swift_table_list, rotating_logs, py_diag):

        self.TOKEN_URL = TOKEN_URL
        self.TABLE_URL = TABLE_URL
        self.FILE_DIR = FILE_DIR
        self.table_list = gen_table_list + swift_table_list
        self.token = 'x'
        self.line_name = self.FILE_DIR.split('/')[-2]
        self.visualiser_json = FILE_DIR + 'log_files/' + self.line_name + '_visual.json'
        self.logfile_name = ''
        self.log_dir = FILE_DIR + 'Log_files/'
        self.log_rotate_count = rotating_logs
        self.swift_table_list = swift_table_list
        self.py_diag = py_diag
        self.xprint(f"{self.line_name} initialised  ")

    def xprint(self, text):
        if self.py_diag: print(text)

    def initial_setup(self):
        self.initialise_logs()
        self.json_creation()

    def json_creation(self):
        visualiser_dict = {}
        if os.path.exists(self.visualiser_json):
            pass
        else:
            for i in self.table_list:
                visualiser_dict[i] = [0, 0, 0]
            with open(self.visualiser_json, 'w') as json_file:
                json.dump(visualiser_dict, json_file)
            self.datalog('GENERAL', 'JSON_CREATED', 'NEW VISUALISER JSON CREATED:' + str(self.visualiser_json))
        self.xprint(f"json initialed for {self.line_name} ")

    def update_visualiser(self, table_name):
        try:
            json_file_data = json.loads(open(self.visualiser_json).read())
        except Exception as e:
            self.datalog('EXCEPTION', 'JSON_READ', e)
            os.remove(self.visualiser_json)
            self.datalog('GENERAL', 'JSON_DELETED', 'NEW VISUALISER JSON DELETED :' + str(self.visualiser_json))
            self.json_creation()

            json_file_data = json.loads(open(self.visualiser_json).read())

        json_file_data[table_name][0] = str(datetime.now())
        json_file_data[table_name][1] = int(json_file_data[table_name][1]) + 1
        with open(self.visualiser_json, 'w') as json_file:
            json.dump(json_file_data, json_file)
            self.xprint(f"data dumped to json file {self.visualiser_json}")

    def initialise_logs(self):
        self.logfile_name = self.log_dir + self.line_name + '_' + str(datetime.now().date()) + '_logfile.csv'
        if not os.path.exists(self.log_dir): os.makedirs(self.log_dir)
        headers = ['Time_stamp', 'Type', 'Event', 'Message']
        try:
            with open(self.logfile_name, 'r', newline='') as file:
                csv.reader(file)
        except FileNotFoundError:
            with open(self.logfile_name, 'w', newline='') as file:
                write_log_csv = csv.writer(file)
                write_log_csv.writerow(headers)
                write_log_csv.writerow([datetime.now(), 'GENERAL', 'CSV', 'LOG_FILE_CREATED:' + str(self.logfile_name)])

    def datalog(self, Type, Event, Msg):
        try:
            with open(self.logfile_name, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([datetime.now(), Type, Event, Msg])
        except Exception as e:
            print(e)

    def log_rotation(self):
        if os.path.exists(self.line_name + '_' + str(datetime.now().date()) + '_logfile.csv'):
            pass
        else:
            self.delete_old_log_files()
            self.initialise_logs()

    def delete_old_log_files(self):
        all_log_file_list = [i.split('_')[-2] for i in os.listdir(self.log_dir) if i.split('.')[-1] == 'csv']
        all_log_file_list.sort()
        for i in range(len(all_log_file_list) - self.log_rotate_count):
            os.remove(self.log_dir + self.line_name + '_' + all_log_file_list[i] + '_logfile.csv')
            self.datalog('GENERAL', 'LOG_FILE_DELETED',
                         self.log_dir + self.line_name + '_' + all_log_file_list[i] + '_logfile.csv')

    def generate_token(self):
        # global token
        x = requests.post(self.TOKEN_URL)
        self.token = x.json()
        if x.status_code == 200:
            self.datalog('GENERAL', 'TOKEN', 'TOKEN_GENERATED')
            return x.json()
        return 'token_exception'

    def send_file(self, send_file_path, table_name, ):
        send_url = self.TABLE_URL + table_name
        with open(send_file_path, 'r') as file: csv_string_data = file.read()
        bearer_token = self.token + ':2123-0377-21'
        headers = {'Authorization': f'Bearer {bearer_token}'}
        x = requests.post(send_url, headers=headers, data=csv_string_data)
        if x.status_code == 401:
            token = self.generate_token()
            # print("New token generated : XXXXXXXX")
            bearer_token = token + ':2123-0377-21'
            headers = {'Authorization': f'Bearer {bearer_token}'}
            x = requests.post(send_url, headers=headers, data=csv_string_data)
            return x.status_code
        return x.status_code

    def sequence(self, table_list, delay=1):
        Z = lambda a: a + " " * (33 - len(a))
        while True:
            self.log_rotation()
            for table in table_list:
                folder_path = self.FILE_DIR + table
                if os.path.exists(folder_path):
                    try:
                        file_list = os.listdir(folder_path)
                        csv_list = [i for i in file_list if i.split('.')[-1] == 'csv']
                        if len(csv_list) > 0:
                            temp_timestamps = []
                            for timestamp in csv_list:  # * check fail case
                                match = re.search(r'\d{4}_\d{2}_\d{2}T\d{2}_\d{2}_\d{2}', timestamp)
                                temp_timestamps.append(match.group(0))

                            date_timestamps = [datetime.strptime(timestamp, "%Y_%m_%dT%H_%M_%S") for timestamp in
                                               temp_timestamps]
                            formatted_timestamp = max(date_timestamps).strftime("%Y_%m_%dT%H_%M_%S")

                            max_file_path = folder_path + '/' + table + '_' + str(formatted_timestamp) + '.csv'

                            if self.send_file(max_file_path, table) == 200:
                                self.datalog(table, 'FILE_SENT', table + '_' + str(formatted_timestamp) + '.csv')
                                self.update_visualiser(table)
                                print("|file_sent:", Z(table + '_' + str(formatted_timestamp) + '.csv'),
                                      " ||  sent at:", datetime.now(), "|", self.line_name)

                                os.remove(max_file_path)
                                self.datalog(table, 'FILE_DELETED', max_file_path)

                        else:
                            self.xprint(f"|no_file   : {Z(table)} ||  check at: {datetime.now()} | {self.line_name}")
                            pass
                        time.sleep(delay)
                    except Exception as e:
                        self.datalog('EXCEPTION', table, e)
                        print(e)
                else:
                    self.datalog('GENERAL', 'FOLDER_NOT_FOUND', folder_path)
