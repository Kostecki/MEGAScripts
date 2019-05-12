import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import Adafruit_ADS1x15

cred = credentials.Certificate('../firebaseServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://megaboominator.firebaseio.com/'
})

# Truncate to 2 decimals - no rounding
def truncate(f):
    return math.floor(f * 10 ** 2) / 10 ** 2

#Get data from ADC Port 0 (connected to voltage divider)
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 2/3
VOLTAGE_MULTIPLIER = 0.0001875
PI_VCC = 5 # Ish.. it's good enough
readings = []

for _ in range(50): #Get 50 readings from the battery
  analog_in = adc.read_adc(0, gain=GAIN)
  readings.append(analog_in)

readings_sorted = sorted(readings)
voltage_raw = readings_sorted[len(readings)//2]
voltage_converted = (voltage_raw * VOLTAGE_MULTIPLIER) * PI_VCC
voltage_output = truncate(voltage_converted)

# Get current active battery
# TODO: Next year ¯\_(ツ)_/¯
activeBattery = "n/a"

# Push to firebase
ref = db.reference('/voltages')
ref.push({
    'batteryId': activeBattery,
    'voltage': voltage_output,
    'insertTime': {'.sv': 'timestamp'}
})
