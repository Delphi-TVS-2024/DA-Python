

import requests




res = requests.get('http://192.168.119.251/iolinkmaster/port[1]/iolinkdevice/pdin/getdata')


print(res.json())