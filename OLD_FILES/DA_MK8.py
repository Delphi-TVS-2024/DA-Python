# get the latest files
# logging added
# all tables looped  check url , file format ,
# counter adding completd
# create a log file  automatically and rotate files *
# object creation
# if json file corupted new json will ctrate and logs will update

import requests
import os
import regex as re
import time
from datetime import datetime
import logging
import json


class StartSending:

    def __init__(self, TOKEN_URL, TABLE_URL, FILE_DIR, table_list, severity_level):

        self.TOKEN_URL = TOKEN_URL
        self.TABLE_URL = TABLE_URL
        self.FILE_DIR = FILE_DIR
        self.table_list = table_list
        self.severity_level = severity_level
        self.token = 'x'
        self.line_name = self.FILE_DIR.split('/')[-2]
        self.visualiser_json = self.line_name + '_visual.json'

    def initial_setup(self):

        self.json_creation()
        self.initialise_logs()

    def json_creation(self):
        visualiser_dict = {}
        if os.path.exists(self.visualiser_json):
            pass
        else:
            for i in self.table_list:
                visualiser_dict[i] = [0, 0, 0]
            with open(self.visualiser_json, 'w') as json_file:
                json.dump(visualiser_dict, json_file)

    def update_visualiser(self, table_name):
        try:
            json_file_data = json.loads(open(self.visualiser_json).read())
        except:
            os.remove(self.visualiser_json)
            self.json_creation()
            logging.log(self.severity_level['INFO'], 'JSON , NEW JSON CREATED')
            json_file_data = json.loads(open(self.visualiser_json).read())

        json_file_data[table_name][0] = str(datetime.now())
        json_file_data[table_name][1] = int(json_file_data[table_name][1]) + 1
        with open(self.visualiser_json, 'w') as json_file:
            json.dump(json_file_data, json_file)

    def initialise_logs(self):

        for i, j in self.severity_level.items():
            logging.addLevelName(j, i)
        file_name = self.line_name + '_' + str(datetime.now().date()) + '.csv'
        logging.basicConfig(
            filename=file_name,
            # level=self.severity_level['INFO'],  # Set the default log level
            format='%(asctime)s ,[%(levelname)s] , %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logging.log(self.severity_level['INFO'], 'INFO,LOGGING STARTED')

    def create_logs(self):
        if os.path.exists(self.line_name + '_' + str(datetime.now().date()) + '.csv'):
            pass
        else:

            self.initialise_logs()

    ##### LOGGING #####
    def generate_token(self):
        # global token
        x = requests.post(self.TOKEN_URL)
        self.token = x.json()
        if x.status_code == 200:
            logging.log(self.severity_level['INFO'], 'INFO,TOKEN_GENERATED')
            return x.json()
        return 'token_exception'

    def send_file(self, send_file_path, table_name, ):
        # global token

        send_url = self.TABLE_URL + table_name
        with open(send_file_path, 'r') as file: csv_string_data = file.read()

        bearer_token = self.token + ':2123-0377-21'

        headers = {'Authorization': f'Bearer {bearer_token}'}
        x = requests.post(send_url, headers=headers, data=csv_string_data)
        # logging.log(severity_level['API_RESPONSE'], x.status_code)
        if x.status_code == 401:
            token = self.generate_token()
            print("New token generated : XXXXXXXX")
            bearer_token = token + ':2123-0377-21'
            headers = {'Authorization': f'Bearer {bearer_token}'}
            x = requests.post(send_url, headers=headers, data=csv_string_data)
            # logging.log(severity_level['API_RESPONSE'], x.status_code)
            return x.status_code
        return x.status_code

    def sequence(self):
        while True:
            for table in self.table_list:
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
                                logging.log(self.severity_level[table],
                                            'file sent,' + table + '_' + str(formatted_timestamp) + '.csv')
                                self.update_visualiser(table)
                                print(self.line_name, "|", table + '_' + str(formatted_timestamp) + '.csv', "||", datetime.now())
                                # update json with table as key and timestamp , count

                                os.remove(max_file_path)
                                logging.log(self.severity_level[table],
                                            'file deleted,' + table + '_' + str(formatted_timestamp) + '.csv')
                                # print("file sent successful & deleted", max_file_path, "||", datetime.now())
                        else:
                            # print("no files to send for", folder_path)
                            pass
                        time.sleep(1)
                    except Exception as e:
                        logging.log(self.severity_level['EXCEPTION'], e)
                        print(e)
                else:
                    # print(folder_path, "Not Exists")
                    logging.log(self.severity_level['FILE_NOT_FOUND'], 'FOLDER NOT FOUND' + folder_path)


if __name__ == '__main__':
    obj = StartSending(
        TOKEN_URL='https://tealdatalogging.azurewebsites.net/api/Values/Check_login?device_id=2123-0377-21',
        TABLE_URL='https://tealdatalogging.azurewebsites.net/api/Values/Insert',
        FILE_DIR='F:/IIOT/PRE01/',
        table_list=['RawTable', 'CycleTime', 'Alarm', 'Loss', 'Tool', 'CTIndex'],
        severity_level={
            'INFO': 10,
            'TOKEN_GENERATED': 20,
            'FILE_NOT_FOUND': 30,
            'FILE_DELETED': 40,
            'EXCEPTION': 50
        })

    obj.initial_setup()
    obj.sequence()
