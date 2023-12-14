# Reading from json
# create seperat thrad for alerts


import DA_MK11 as dataaggregator
import threading
import os, json, time

# imported_objects = globals()

try:

    # print("This Program using {lib} as Core".format(lib=str(imported_objects['dataaggregator']).split(' ')[1]))
    print()
    CONFIG = json.loads(open('RUN_DA.json').read())

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
        )

        globals()['obj_' + str(i)].initial_setup()
        globals()['gen_th_' + str(i)] = threading.Thread(
            target=lambda: globals()['obj_' + str(i)].sequence(CONFIG['gen_table_list'], 1))
        globals()['swift_th_' + str(i)] = threading.Thread(
            target=lambda: globals()['obj_' + str(i)].sequence(CONFIG['swift_table_list']))
        globals()['gen_th_' + str(i)].start()
        globals()['swift_th_' + str(i)].start()

except Exception as e:
    print(e)
    time.sleep(200)

