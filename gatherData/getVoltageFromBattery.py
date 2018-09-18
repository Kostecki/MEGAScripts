import Adafruit_ADS1x15
import json
import urllib.request
import base64

#Load credentials.
#This is super janky, but os.env just doesn't fucking work and i can't be bothered anymore..
with open('auth.json') as f:
  authData = json.load(f)

#Get data from ADC Port 0 (connected to voltage divider)
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 2/3

readings = []

for _ in range(50): #Get 50 readings from the battery
  analogIn = adc.read_adc(0, gain=GAIN)
  voltageOut = (analogIn * 0.0001875)*4.999 #Pretty excessive, but also seems pretty accurate
  readings.append(voltageOut)

#Create JSON Object
Voltage = {}
readingsSorted = sorted(readings)
Voltage['Voltage'] = round(readingsSorted[len(readings)//2], 2)

#Post to API
apiUrl = "https://api.mega.re/setvoltage"

auth = '%s:%s' % (authData["apiUser"], authData["apiPass"])
base64string = base64.standard_b64encode(auth.encode('utf-8'))

req = urllib.request.Request(apiUrl)
jsondata = json.dumps(Voltage)
jsondataasbytes = jsondata.encode('utf-8')
req.add_header('Content-Type', 'application/json; charset=utf-8')
req.add_header('Content-Length', len(jsondataasbytes))
req.add_header('Authorization', 'Basic %s' % base64string.decode('utf-8'))
urllib.request.urlopen(req, jsondataasbytes)
