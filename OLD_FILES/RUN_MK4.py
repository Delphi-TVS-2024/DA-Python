import DA_MK9 as dataaggregator
import threading
import os, json

try:
    CONFIG = json.loads(open('RUN_DA.json').read())

    IGNORE_LINE = CONFIG['IGNORE_LINE']
    LINES = []
    FOLDER_PATH = CONFIG['FOLDER_PATH']

    for i in os.listdir(FOLDER_PATH):
        if len(i.split('.')) == 1 and i not in IGNORE_LINE:
            LINES.append(i)

    for i in LINES:
        globals()['obj_' + str(i)] = dataaggregator.StartSending(
            TOKEN_URL= CONFIG['TOKEN_URL'],
            TABLE_URL=CONFIG['TABLE_URL'],
            FILE_DIR=FOLDER_PATH + i + '/',
            gen_table_list=CONFIG['table_list'],
            swift_table_list = []

        )

        globals()['obj_' + str(i)].initial_setup()
        globals()['th_' + str(i)] = threading.Thread(target=globals()['obj_' + str(i)].sequence)
        globals()['th_' + str(i)].start()
except Exception as e:
    print(e)

# obj.sequence()
