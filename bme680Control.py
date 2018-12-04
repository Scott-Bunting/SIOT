import bme680
import time
import os
from datetime import datetime

sensor = bme680.BME680()

path = "/home/pi/SIOT/data_log.csv"
file = open(path,"a+")
i=0

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)

sensor.set_filter(bme680.FILTER_SIZE_3)

while True:
    if sensor.get_sensor_data():	
        output = "{0:.2f} C,{1:.2f} hPA,{2:.2f} %RH".format(sensor.data.temperature, sensor.data.pressure, sensor.data.humidity)
        
        print(output)
	
        now = datetime.now()
        file.write(str(now)+"," + output + "\n")
        file.flush()
        time.sleep(1)
#        file.close()	

#time.sleep(1)

file.close()
