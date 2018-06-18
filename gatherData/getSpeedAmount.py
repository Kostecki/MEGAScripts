import os
import json
import urllib.request

#API URL
apiUrl = "https://putsreq.com/13pmCr7IuFD50z8RzzOz"

#Define final object
setStatusData = {}
setStatusData['avgSpeed'] = {}
setStatusData['dataAmount'] = {}

#Get uptime
uptime = os.popen("awk '{print $1}' /proc/uptime").readline()

#Get data from vnStat
os.system('vnstat -i ppp0 --json > /tmp/vnStatData.json')
with open("/tmp/vnStatData.json", "r") as f:
  data = json.load(f)

#Convert data to kilobytes and set upload and download with data from vnStat 
downloadAmount = data['interfaces'][0]['traffic']['total']['rx'] * 1.02400
uploadAmount = data['interfaces'][0]['traffic']['total']['tx'] * 1.02400

#Calculate average download and upload speed
downloadAvgSpeed = float(downloadAmount) / float(uptime)
uploadAvgSpeed = float(uploadAmount) / float(uptime)

#Update final objects with data
setStatusData['dataAmount']['down'] = round(downloadAmount, 3)
setStatusData['dataAmount']['up'] = round(uploadAmount, 3)
setStatusData['avgSpeed']['down'] = round(downloadAvgSpeed, 3)
setStatusData['avgSpeed']['up'] = round(uploadAvgSpeed, 3)

#Post to API
req = urllib.request.Request(apiUrl)
req.add_header('Content-Type', 'application/json; charset=utf-8')
jsondata = json.dumps(setStatusData)
jsondataasbytes = jsondata.encode('utf-8')
req.add_header('Content-Length', len(jsondataasbytes))
response = urllib.request.urlopen(req, jsondataasbytes)