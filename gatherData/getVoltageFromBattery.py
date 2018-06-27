import serial
import time
import json
import urllib.request
import base64

#API URL
apiUrl = "https://api.mega.re/setvoltage"

#Define final object
Voltage = {}

#Get data from pi-voltmeter
readings = []
ser = serial.Serial('/dev/ttyUSB0',9600)

for i in range(0, 600): #600 is about 5 minutes
  readings.append(ser.readline().rstrip())
ser.close()

Voltage = str(readings[len(readings)//2])

#Post to API
auth = '%s:%s' % ('', '') #I'm lazy. Just set login here. User/pass
base64string = base64.standard_b64encode(auth.encode('utf-8'))

req = urllib.request.Request(apiUrl)
jsondata = json.dumps(Voltage)
jsondataasbytes = jsondata.encode('utf-8')
req.add_header('Content-Type', 'application/json; charset=utf-8')
req.add_header('Content-Length', len(jsondataasbytes))
req.add_header('Authorization', 'Basic %s' % base64string)
response = urllib.request.urlopen(req, jsondataasbytes)