
import requests , time
from opcua import Client , ua


server_url = "opc.tcp://192.168.119.4:4840"
client = Client(server_url)
client.connect()

node = client.get_node("ns=4;s=vibration_vrms")

print(node.get_value())

# dv = ua.DataValue(ua.Variant(119.0, ua.VariantType.Float))
# dv.ServerTimestamp = None
# dv.SourceTimestamp = None
# node.set_value(dv)
# print(node.get_value())


# Disconnect from the OPC UA server

while True:
    try:
        res = requests.get('http://192.168.119.251/iolinkmaster/port[1]/iolinkdevice/pdin/getdata')
        print( res.json()['data']['value'])
        vrms = res.json()['data']['value'][:4]
        dec_vrms = int(vrms , 16)
        value = dec_vrms*0.1
        dv = ua.DataValue(ua.Variant(value, ua.VariantType.Float))
        dv.ServerTimestamp = None
        dv.SourceTimestamp = None
        node.set_value(dv)
        print(node.get_value())

    except  Exception as E:
        print(E)
        pass


    time.sleep(1)
