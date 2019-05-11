import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# import Adafruit_ADS1x15

cred = credentials.Certificate('../firebaseServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://megaboominator.firebaseio.com/'
})

#Get data from ADC Port 0 (connected to voltage divider)
# adc = Adafruit_ADS1x15.ADS1115()
# GAIN = 2/3

# readings = []

# for _ in range(50): #Get 50 readings from the battery
#   analog_in = adc.read_adc(0, gain=GAIN)
#   voltage_out = (analog_in * 0.0001875)*4.999 #Pretty excessive, but also seems pretty accurate
#   readings.append(voltage_out)

# readings_sorted = sorted(readings)
# voltage = round(readings_sorted[len(readings)//2], 2)

# Get current battery
current_battery = 'ThunderDuck'

# Push to firebase
ref = db.reference('/voltages')
ref.push({
    'batteryId': current_battery,
    'voltage': 12.3,
    'insertTime': {'.sv': 'timestamp'}
})
