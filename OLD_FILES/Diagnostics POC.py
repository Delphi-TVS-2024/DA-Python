import csv
from datetime import datetime

path = 'E:/IIOT/Dump/Diagnostics_2024_02_19T16_17_17.csv'

try:
    with open(path, 'r', newline='') as file:
        write_log_csv = csv.reader(file)
        first_row = next(write_log_csv)
        print(first_row)
    with open(path, 'a', newline='') as file1:

        pc_diag_data = ['DataAggregator-PC', 'test', 33.33, datetime.now().date(), first_row[4], first_row[5],first_row[6], datetime.now(),"DA"]

        write_log_csv1 = csv.writer(file1)

        write_log_csv1.writerow(pc_diag_data)

except Exception as e:
    print(e)

    # write_log_csv.writerow(
    #     ['DataAggretor-PC', 'test', 33.33, datetime.now().date(), 'TEAL_DTVS', 'TEAL_DTVS01', 'MNAL01', '2024-02-19T13:18:01',
    #      "DA"])

    #
    # write_log_csv = csv.writer(file)
    # write_log_csv.writerow(['2123-0348-21' , 'test' ,33.33 ,'19-02-2024' ,	'TEAL_DTVS'	,'TEAL_DTVS01',	'MNAL01'	,'2024-02-19T13:18:01',"DA"])
