from opcua import Client
import csv, json, os
from datetime import datetime


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
            if os.path.exists(self.instance.file_name):
                with open(self.instance.file_name, 'a', newline='') as file:
                    write_log_csv = csv.writer(file)
                    write_log_csv.writerow(data)
                    print(f"logged {data}")
            else:
                with open(self.instance.file_name, 'w', newline='') as file:
                    print(f"file created {self.instance.file_name}")
                    write_log_csv = csv.writer(file)
                    write_log_csv.writerow(data)
                    print(f"logged {data}")

class initilase:
    def __init__(self, ENDPOINT, CONFIG_DATA, TAGS):
        self.client = None
        self.ENDPOINT = ENDPOINT
        self.CONFIG_DATA = CONFIG_DATA
        self.TAGS = TAGS
        self.test = 'Test'
        self.file_name = CONFIG_DATA['file_name']
        self.connect_server()

    def connect_server(self):
        try:
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




## NOTES

# OPCUA Subscription created *
# get ewon data automatically for shift pdate variant
# timebased moving


