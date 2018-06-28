import os
import json
import urllib.request
import base64

#API URL
apiUrl = "https://api.mega.re/setstatus"

#Define final object
setStatusData = {}
setStatusData['AvgSpeed'] = {}
setStatusData['DataAmount'] = {}

#Get uptime
uptime = os.popen("awk '{print $1}' /proc/uptime").readline()

#Get data from vnStat
os.system('vnstat -i eth1 --json > /tmp/vnStatData.json')
with open("/tmp/vnStatData.json", "r") as f:
  data = json.load(f)

#Convert data to kilobytes and set upload and download with data from vnStat 
downloadAmount = data['interfaces'][0]['traffic']['total']['rx'] * 1.02400
uploadAmount = data['interfaces'][0]['traffic']['total']['tx'] * 1.02400

#Calculate average download and upload speed
downloadAvgSpeed = float(downloadAmount) / float(uptime)
uploadAvgSpeed = float(uploadAmount) / float(uptime)

#Update final objects with data
setStatusData['DataAmount']['Down'] = round(downloadAmount, 3)
setStatusData['DataAmount']['Up'] = round(uploadAmount, 3)
setStatusData['AvgSpeed']['Down'] = round(downloadAvgSpeed, 3)
setStatusData['AvgSpeed']['Up'] = round(uploadAvgSpeed, 3)

#Post to API
auth = '%s:%s' % (os.environ['API_USER'], os.environ['API_PASSWORD'])
base64string = base64.standard_b64encode(auth.encode('utf-8'))

req = urllib.request.Request(apiUrl)
jsondata = json.dumps(setStatusData)
jsondataasbytes = jsondata.encode('utf-8')
req.add_header('Content-Type', 'application/json; charset=utf-8')
req.add_header('Content-Length', len(jsondataasbytes))
req.add_header('Authorization', 'Basic %s' % base64string.decode('utf-8'))
response = urllib.request.urlopen(req, jsondataasbytes)