from opcua import Client


class test:
    def datachange_notification(self, node, val, data):
        print("Data change detected:")
        print("Node ID:", node.nodeid)
        print("Value:", val)


client = Client("opc.tcp://192.168.119.5:4840")
client.connect()
han = test()
print(han)
sub = client.create_subscription(100, han)

tag = "ns=4;s=Current_Shift"  # Example tag to monitor
node = client.get_node(tag)

print("values is ",node.get_value())

# handle = sub.subscribe_data_change(node)

try:
    while True:
        pass  # Do other stuff while monitoring data changes
finally:
    client.disconnect()
