import Adafruit_ADS1x15

GAIN = 2/3

#Get data from ADC Port 1 (ammeter)
adc1 = Adafruit_ADS1x15.ADS1115()
analogIn1 = adc1.read_adc(1, gain=GAIN)
voltageRaw1 = (analogIn1 * 0.0001875)

VCC = 5.0
FACTOR = 20.0 / 1000
QOV = 0.5 * VCC
voltage = voltageRaw1 - QOV + 0.007
current = voltage / FACTOR
print ("Current: " current)