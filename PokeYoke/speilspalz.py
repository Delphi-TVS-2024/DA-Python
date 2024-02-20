from opcua import Client
import csv, json, os
from datetime import datetime


# class onchange_trigger:


# def datalog(self, node, val):
#


#     try:
#         with open(self.logfile_name, 'a', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow([datetime.now(), Type, Event, Msg])
#     except Exception as e:
#         print(e)
#
# try:
#     with open(self.logfile_name, 'r', newline='') as file:
#         csv.reader(file)
# except FileNotFoundError:
#     with open(self.logfile_name, 'w', newline='') as file:
#         write_log_csv = csv.writer(file)
#         write_log_csv.writerow(headers)
#         write_log_csv.writerow([datetime.now(), 'GENERAL', 'CSV', 'LOG_FILE_CREATED:' + str(self.logfile_name)])


class onchange_trigger():
    def __init__(self, instance):
        self.file_name = 'PokeYoke.csv'
        self.instance = instance

    def datachange_notification(self, node, val, data):
        headers = ['Time_Stamp', 'Shift_Id', 'Machine_Code', 'Variant_Code', 'Parameter_Id', 'Status', 'CompanyCode',
                   'PlantCode', 'Line_Code', 'Date']

        # print(f'Data changes for {node.nodeid} and value is {val}')
        tag = str(node.nodeid)[20:-1]
        split_tag = tag.split('_')
        if len(split_tag) == 3:
            data = [datetime.now(), 'S2', split_tag[0], 'V1', tag, val, self.instance.CONFIG_DATA['Company_code'] , self.instance.CONFIG_DATA['plant_code'] , self.instance.CONFIG_DATA['Line_code'] , '2024-02-18']
            if os.path.exists(self.file_name):
                with open(self.file_name, 'a', newline='') as file:
                    write_log_csv = csv.writer(file)
                    write_log_csv.writerow(data)
                    print(f"file logged {self.file_name}")
            else:
                with open(self.file_name, 'w', newline='') as file:
                    print(f"file created {self.file_name}")
                    write_log_csv = csv.writer(file)
                    write_log_csv.writerow(data)
                    print(f"file logged {self.file_name}")

class initilase:
    def __init__(self, ENDPOINT, CONFIG_DATA, TAGS):
        self.client = None
        self.ENDPOINT = ENDPOINT
        self.CONFIG_DATA = CONFIG_DATA
        self.TAGS = TAGS
        self.test = 'Test'
        self.filename = 'PokeYoke'
        self.connect_server()

    def connect_server(self):
        try:
            ewon_tags = ['Current_shoft']
            self.client = Client(self.ENDPOINT)
            self.client.connect()
            event_onchange = self.client.create_subscription(100, onchange_trigger(self))
            print("::::  Connected to end point" + self.ENDPOINT)

            for tag in self.TAGS:
                cmp_tag = 'ns=4;s=' + tag
                try:
                    node = self.client.get_node(cmp_tag)
                    event_onchange.subscribe_data_change(node)
                    print(f'onchange successful   {self.ENDPOINT}-{tag}')
                except Exception as e:
                    print(f'onchange unsuccessful {self.ENDPOINT}-{tag}')
        except Exception as e:
            print(f"::::  not Connected to end point {self.ENDPOINT}")


if __name__ == '__main__':
    CONFIG_DATA = json.loads(open('PKYK_config.json').read())

    for server in CONFIG_DATA:
        globals()[server] = initilase(CONFIG_DATA[server]['ENDPOINT'], CONFIG_DATA[server]['CONFIG_DATA'],
                                      CONFIG_DATA[server]['TAGS'])
