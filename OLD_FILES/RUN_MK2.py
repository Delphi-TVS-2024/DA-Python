import DA_MK7 as DA_MK7
import threading
import os

IGNORE_LINE = ['Config', 'HH01']
LINES = []
FOLDER_PATH = 'E:/IIOT/'

for i in os.listdir(FOLDER_PATH):
    if len(i.split('.')) == 1 and i not in IGNORE_LINE:
        LINES.append(i)

for i in LINES:
    globals()['obj_' + str(i)] = DA_MK7.StartSending(
        TOKEN_URL='https://tealdatalogging.azurewebsites.net/api/Values/Check_login?device_id=2123-0377-21',
        TABLE_URL='https://tealdatalogging.azurewebsites.net/api/Values/Insert',
        FILE_DIR=FOLDER_PATH + i + '/',
        table_list=['RawTable', 'CycleTime', 'Alarm', 'Loss', 'Tool', 'CTIndex','Alert'],
        severity_level={
            'INFO': 10,

            'TOKEN_GENERATED': 20,
            'FILE_NOT_FOUND': 30,
            'FILE_DELETED': 40,
            'EXCEPTION': 50
        })

    globals()['obj_' + str(i)].create_json()
    # globals()['obj_' + str(i)].intial_setup()
    globals()['obj_' + str(i)].enable_logs()
    globals()['th_' + str(i)] = threading.Thread(target=globals()['obj_' + str(i)].sequence)
    globals()['th_' + str(i)].start()

# obj.sequence()
