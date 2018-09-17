import Adafruit_ADS1x15
import os
import json
import urllib.request
import base64

#Get data from ADC Port 0 (connected to voltage divider)
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 2/3

readings = []

for _ in range(50): #Get 50 readings from the battery
  analogIn = adc.read_adc(0, gain=GAIN)
  voltageOut = (analogIn * 0.0001875)*5
  readings.append(voltageOut)

#Create JSON Object
Voltage = {}
readingsSorted = sorted(readings)
Voltage['Voltage'] = readingsSorted[len(readings)//2]

#Post to API
apiUrl = "https://api.mega.re/setvoltage"

auth = '%s:%s' % (os.environ['API_USER'], os.environ['API_PASSWORD'])
base64string = base64.standard_b64encode(auth.encode('utf-8'))

req = urllib.request.Request(apiUrl)
jsondata = json.dumps(Voltage)
jsondataasbytes = jsondata.encode('utf-8')
req.add_header('Content-Type', 'application/json; charset=utf-8')
req.add_header('Content-Length', len(jsondataasbytes))
req.add_header('Authorization', 'Basic %s' % base64string.decode('utf-8'))
response = urllib.request.urlopen(req, jsondataasbytes)