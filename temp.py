import spidev
import time
import os
spi = spidev.SpiDev()
spi.open(0,0)
def ReadChannel(channel):
adc = spi.xfer2([1,(8+channel)<<4,0])
data = ((adc[1]&3) << 8) + adc[2]
return data
def ConvertVolts(data,places):
volts = (data * 3.3) / float(1023)
volts = round(volts,places)
return volts
def ConvertTemp(data,places):
# ADC Value
# (approx) Temp Volts
# 0 -50 0.00
# 78 -25 0.25
# 155 0 0.50
# 233 25 0.75
# 310 50 1.00
# 465 100 1.50
# 775 200 2.50
# 1023 280 3.30
temp = ((data * 330)/float(1023))-50
temp = round(temp,places)
return temp
light_channel = 0
temp_channel = 1
delay = 5
while True:
light_level = ReadChannel(light_channel)
light_volts = ConvertVolts(light_level,2)
temp_level = ReadChannel(temp_channel)
temp_volts = ConvertVolts(temp_level,2)
temp = ConvertTemp(temp_level,2)
print( "--------------------------------------------")
print("Light: {} ({}V)".format(light_level,light_volts))
print("Temp : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
time.sleep(delay)