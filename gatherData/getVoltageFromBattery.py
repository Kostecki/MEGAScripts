import os
import json
import urllib.request

#API URL
apiUrl = "https://putsreq.com/13pmCr7IuFD50z8RzzOz"

#Define final object
setVoltageData = {}

#Get data from pi-voltmeter


#Post to API
req = urllib.request.Request(apiUrl)
req.add_header('Content-Type', 'application/json; charset=utf-8')
jsondata = json.dumps(setVoltageData)
jsondataasbytes = jsondata.encode('utf-8')
req.add_header('Content-Length', len(jsondataasbytes))
response = urllib.request.urlopen(req, jsondataasbytes)