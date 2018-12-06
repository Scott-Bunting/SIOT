import bme680
import time
import os
from datetime import datetime

sensor = bme680.BME680()

path = "/media/pi/D220-8D3B1/SIOT/data-storage/usb/data_log_usb_2.csv"
file = open(path,"a+")
i=0

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)

sensor.set_filter(bme680.FILTER_SIZE_3)

while True:
    if sensor.get_sensor_data():	
        output = "{0:.2f} C,{1:.2f} hPA,{2:.2f} %RH".format(sensor.data.temperature, sensor.data.pressure, sensor.data.humidity)
	
        if os.stat(path).st_size == 0:
            file.write("datetime,temperature,pressure,humidity\n")

        now = datetime.now()
        now = now.strftime('%Y/%m/%d %H:%M:%S')

        print(now + "," + output)

        file.write(str(now)+"," + output + "\n")
        file.flush()
        time.sleep(1)

file.close()
