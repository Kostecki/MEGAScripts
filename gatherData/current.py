import Adafruit_ADS1x15
import json
import urllib.request
import base64
import time

GAIN = 2/3

while 1:
  #Get data from ADC Port 0 (connected to voltage divider)
  adc0 = Adafruit_ADS1x15.ADS1115()
  analogIn0 = adc0.read_adc(0, gain=GAIN)
  voltageRaw0 = (analogIn0 * 0.0001875)*4.999 #Pretty excessive, but also seems pretty accurate
  print("Voltage", voltageRaw0)

  #Get data from ADC Port 0 (connected to voltage divider)
  adc1 = Adafruit_ADS1x15.ADS1115()
  analogIn1 = adc1.read_adc(1, gain=GAIN)
  voltageRaw1 = (analogIn1 * 0.0001875)

  VCC = voltageRaw0
  FACTOR = 20.0 / 1000
  QOV = 0.5 * VCC
  voltage = voltageRaw1 - QOV + 0.007
  current = voltage / FACTOR
  print("Current", current)
  time.sleep(2)
  pass