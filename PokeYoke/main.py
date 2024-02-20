from opcua import Client
import csv, json, os


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

class initilase:
    def __init__(self, ENDPOINT, CONFIG_DATA, TAGS):
        self.ENDPOINT = ENDPOINT
        self.CONFIG_DATA = CONFIG_DATA
        self.TAGS = TAGS
        self.filename = 'PokeYoke'
        self.connect_server()

    class onchange_trigger():
        def __init__(self):
            self.file_name = 'PokeYoke.csv'

        def datachange_notification(self, node, val, data):
            headers = ['Time_Stamp', 'Shift_Id', 'Machine_Code', 'Variant_Code', 'Parameter_Id', 'Status',
                       'CompanyCode', 'PlantCode', 'Line_Code', 'Date']

            print(f'Data changes for {node.nodeid} and value is {val}')
            if os.path.exists(self.file_name):
                with open(self.file_name, 'a', newline='') as file:
                    write_log_csv = csv.writer(file)
                    write_log_csv.writerow([node.nodeid, val])
                    print(f"file logged {self.file_name}")
            else:
                with open(self.file_name, 'w', newline='') as file:
                    print(f"file created {self.file_name}")
                    write_log_csv = csv.writer(file)
                    write_log_csv.writerow(headers)
                    write_log_csv.writerow([node.nodeid, val])
                    print(f"file logged {self.file_name}")

    def connect_server(self):
        try:
            client = Client(self.ENDPOINT)
            client.connect()
            event_onchange = client.create_subscription(100, self.onchange_trigger())
            for tag in self.TAGS:
                try:
                    node = client.get_node(tag)
                    event_onchange.subscribe_data_change(node)
                except:
                    print(f'tag wrong for {self.ENDPOINT} for tag {tag}')
        except Exception as e:
            print("Not Connected" + self.ENDPOINT)


if __name__ == '__main__':
    CONFIG_DATA = json.loads(open('PKYK_config.json').read())

    for server in CONFIG_DATA:
        globals()[server] = initilase(CONFIG_DATA[server]['ENDPOINT'], CONFIG_DATA[server]['CONFIG_DATA'],
                                      CONFIG_DATA[server]['TAGS'])
