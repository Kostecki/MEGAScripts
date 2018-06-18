import os
import json
from urllib import request, parse

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
setStatusData['dataAmount']['down'] = downloadAmount
setStatusData['dataAmount']['up'] = uploadAmount
setStatusData['avgSpeed']['down'] = downloadAvgSpeed
setStatusData['avgSpeed']['up'] = uploadAvgSpeed

#Post to API
payload = parse.urlencode(setStatusData).encode()
req = request.Request('https://putsreq.com/13pmCr7IuFD50z8RzzOz', data=payload) # this will make the method "POST"
response = request.urlopen(req)
print(response)