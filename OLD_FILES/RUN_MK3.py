import DA_MK9 as dataaggregator
import threading
import os

IGNORE_LINE = ['Config', ]
LINES = []
FOLDER_PATH = 'E:/IIOT/'

for i in os.listdir(FOLDER_PATH):
    if len(i.split('.')) == 1 and i not in IGNORE_LINE:
        LINES.append(i)

for i in LINES:
    globals()['obj_' + str(i)] = dataaggregator.StartSending(
        TOKEN_URL='https://tealdatalogging.azurewebsites.net/api/Values/Check_login?device_id=2123-0377-21',
        TABLE_URL='https://tealdatalogging.azurewebsites.net/api/Values/Insert',
        FILE_DIR=FOLDER_PATH + i + '/',
        table_list=['RawTable', 'CycleTime', 'Alarm', 'Loss', 'Tool', 'CTIndex', 'Alert'])

    globals()['obj_' + str(i)].initial_setup()
    globals()['th_' + str(i)] = threading.Thread(target=globals()['obj_' + str(i)].sequence)
    globals()['th_' + str(i)].start()

# obj.sequence()
