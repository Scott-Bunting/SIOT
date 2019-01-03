from flask import Flask
from flask_restful import Resource, Api
import requests
import json
import time
import os
from datetime import datetime
import bme680
from functions import all

#create or open csv file
path = "/media/pi/D220-8D3B1/SIOT/data-storage/usb/data_log_combined.csv"
file = open(path, "a+")

#API requirements
api_key = '07bafc834660819c6b0c515fe2a9cac9'

#house coordinates
lat_yel = 51.49
lon_yel = -0.22

#heat loss coefficient
u = 127

#instantiate sensor
sensor = bme680.BME680()
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

#CSV file headers
inside_headers = ['time', 'temp_in', 'press_in', 'hum_in']
outside_headers = ['time_measured', 'temp_out', 'press_out', 'hum_out']
comparison_headers = ['time_diff', 'temp_diff', 'press_diff', 'hum_diff']
metrics_headers = ['power','cost']

headers = ','.join(inside_headers) + ','.join(outside_headers) + ','.join(comparison_headers) \
          + ','.join(metrics_headers)

if os.stat(path).st_size == 0:
    file.write(headers + "\n")
    new = True
else:
    new = False

start = time.time()
tic = time.time()
count = 0
power = 0
while True:

    end = time.time()
    try:
        if sensor.get_sensor_data():
            data_in = data_inside()
        else:
            data_in = [0, 0, 0, 0]

        if end - start > 600 or count == 0:
            data_out = data_outside(api_key, lat_yel, lon_yel)
            start = time.time()

        data_comp = data_in - data_out

        toc = time.time() #in case api takes too long to call
        if new:
            power = data_comp[1]*u
            cost = 0
        else:
            delta_power = power - data_comp[1]*u
            cost = delta_power*(toc-tic)

        metrics = [power, cost]

        output = ','.join(str(x) for x in list_of_ints) + ','.join(str(x) for x in data_out) \
                 + ','.join(str(x) for x in data_comp) + ','.join(str(x) for x in metrics)

        file.write(output + "\n")
        tic = time.time()
        file.flush()
        time.sleep(60)

    except KeyboardInterrupt:
        file.close()

