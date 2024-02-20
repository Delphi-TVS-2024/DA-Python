# Reading from json
# create seperat thrad for alerts


import DA_MK14 as dataaggregator
from datetime import datetime
import threading
import os, json, time
import sys , psutil
import select
import requests

# import Visualiser_MK2

def run_diagnostics(url, delay_time):
    while True:
        try:
            res = requests.post(url)
            if res.status_code == 200:print(f"::::::::::::::::::::::::::::::::::::  Diagnostics successful at {datetime.now()}")
            else:print(f"::::::::::::::::::::::::::::::::::::::  Diagnostics failed at {datetime.now()}")
        except:print(f":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::  Failed to call Diagnostics at {datetime.now()}")
        time.sleep(int(delay_time))


def one_time_run():
    diag_thread = threading.Thread(target=run_diagnostics, args=(CONFIG['DIAGNOSTICS_URL'], CONFIG['DIAGNOSTICS_CALL']))
    diag_thread.start()


# imported_objects = globals()
HOME_PATH = 'E:/IIOT/Config/RUN_DA.json'
try:
    CONFIG = json.loads(open(HOME_PATH).read())
    if CONFIG['run_status']:
        IGNORE_LINE = CONFIG['IGNORE_LINE']
        LINES = []
        FOLDER_PATH = CONFIG['FOLDER_PATH']

        for i in os.listdir(FOLDER_PATH):
            if len(i.split('.')) == 1 and i not in IGNORE_LINE:
                LINES.append(i)

        for i in LINES:
            globals()['obj_' + str(i)] = dataaggregator.StartSending(
                TOKEN_URL=CONFIG['TOKEN_URL'],
                TABLE_URL=CONFIG['TABLE_URL'],
                FILE_DIR=FOLDER_PATH + i + '/',
                gen_table_list=CONFIG['gen_table_list'],
                swift_table_list=CONFIG['swift_table_list'],
                rotating_logs=CONFIG['rotating_logs'],
                py_diag=CONFIG['py_diag']
            )

            globals()['obj_' + str(i)].initial_setup()
            globals()['gen_th_' + str(i)] = threading.Thread(
                target=lambda: globals()['obj_' + str(i)].sequence(CONFIG['gen_table_list'], 1))
            globals()['swift_th_' + str(i)] = threading.Thread(
                target=lambda: globals()['obj_' + str(i)].sequence(CONFIG['swift_table_list']))
            globals()['gen_th_' + str(i)].start()
            globals()['swift_th_' + str(i)].start()
        one_time_run()
    else:
        print("run_status was not 1")

    # run_diagnostics(CONFIG['DIAGNOSTICS_URL'], CONFIG['DIAGNOSTICS_CALL'])
except Exception as e:
    print("Error:",e)
    print('###### press X to see sample config details ###')
    inp = str(input())
    if inp == 'X':
        example = {
            "IGNORE_LINE": ["Config", "SUB01"],
            "FOLDER_PATH": "E:/IIOT/",
            "TOKEN_URL": "https://tealdatalogging.azurewebsites.net/api/Values/Check_login?device_id=2123-0377-21",
            "TABLE_URL": "https://tealdatalogging.azurewebsites.net/api/Values/Insert",
            "gen_table_list": ["CycleTime", "Alarm", "Loss", "Tool", "CTIndex"],
            "swift_table_list": ["RawTable", "Alert"],
            "rotating_logs": 7,
            "run_status": 1,
            "py_diag": 1
        }
        print(f"Example Json : {example}")
    print("program exited")



