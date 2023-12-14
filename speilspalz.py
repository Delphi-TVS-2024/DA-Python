import os

log_dir = 'E:/IIOT/HH01/Log_files/'

all_log_file_list = ['2023-11-22', '2023-11-23' , '2023-11-14' , '2023-11-12','2023-11-10', '2023-11-209' , '2023-11-13' , '2023-11-11']
def delete_old_log_files():

    all_log_file_list.sort()
    print(all_log_file_list)
    for i in range(len(all_log_file_list) - 9):
        print(all_log_file_list[i] + '_logfile.csv')

delete_old_log_files()