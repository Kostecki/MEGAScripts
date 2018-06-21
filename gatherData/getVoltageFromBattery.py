import os
import json
import urllib.request
import base64

#API URL
apiUrl = "https://putsreq.com/13pmCr7IuFD50z8RzzOz"

#Define final object
setVoltageData = {}

#Get data from pi-voltmeter


#Post to API
auth = '%s:%s' % ('', '') #I'm lazy. Just set login here. User/pass
base64string = base64.standard_b64encode(auth.encode('utf-8'))

req = urllib.request.Request(apiUrl)

req = urllib.request.Request(apiUrl)
jsondata = json.dumps(setVoltageData)
jsondataasbytes = jsondata.encode('utf-8')
req.add_header('Content-Type', 'application/json; charset=utf-8')
req.add_header('Content-Length', len(jsondataasbytes))
req.add_header('Content-Type', 'application/json; charset=utf-8')
response = urllib.request.urlopen(req, jsondataasbytes)