import requests, time

url = 'http://192.168.119.1:8080//api/Values/Store_Diagnostic'

while True:


    req = requests.post(url)
    print(req.status_code)
    time.sleep(40)
