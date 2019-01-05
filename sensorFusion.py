from flask import Flask
from flask_restful import Resource, Api
import requests
import json
import time
import os
from datetime import datetime
import bme680
from functions import *

#create or open csv file
path = "/media/pi/D220-8D3B1/SIOT/data-storage/usb/data_log_combined.csv"
file = open(path, "a+")

#Api requirements
api_key = '07bafc834660819c6b0c515fe2a9cac9'

#House Coordinates
lat_yel = 51.49
lon_yel = -0.22

#Heat loss coefficient
u = 127

#Price per kwh
p = 2.78

#Sampling frequencies
interval_in = 15 #home.gov states a fire can spread in 30 seconds
interval_out = 600 #recommended samplig rate from OWM

#Instantiate sensor
sensor = bme680.BME680()
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

#CSV file headers
inside_headers = ['time', 'temp_in', 'press_in', 'hum_in']
outside_headers = ['time_measured', 'temp_out', 'press_out', 'hum_out']
comparison_headers = ['time_diff', 'temp_diff', 'press_diff', 'hum_diff']
metrics_headers = ['power','cost_window','cost_predict']

headers = ','.join(inside_headers) + ',' + ','.join(outside_headers) + ',' + \
	 ','.join(comparison_headers) + ','  + ','.join(metrics_headers)

if os.stat(path).st_size == 0:
    file.write(headers + "\n")
    new = True
elif os.stat(path).st_size == 1:
    new = True
else:
    print(os.stat(path).st_size)
    new = False

start = time.time()
tic = time.time()
count = 0
power = 0
while True:

    end = time.time()
    try:
        if sensor.get_sensor_data():
            data_in = data_inside(sensor)
        else:
            data_in = [0, 0, 0, 0]
        print(data_in)
	print('[DEBUG]: before API')
        if end - start > interval_out or count == 0:
	    print('[DEBUG]: API')
	    code = get_code(api_key, lat_yel, lon_yel)
	    count += 1
	    print('API Request:')
	    print(code)
	    if code == 200:
		data_out = data_outside(api_key, lat_yel, lon_yel)
		print(data_out)
                start = time.time()
	    else:
		print(code)
		data_out = ['2019/01/05 12:20:00', 4.09, 1039, 70]
        print(data_out)
        
        data_comp = []
	time_out = datetime.strptime(data_out[0], '%Y/%m/%d %H:%M:%S')
	time_in = datetime.strptime(data_in[0], '%Y/%m/%d %H:%M:%S')
	time_diff = time_in - time_out
	data_comp.append(time_diff)

        if len(data_out) == len(data_in):
            for i in range(len(data_in)-1):
                comp = data_in[i+1] - data_out[i+1]
                data_comp.append(comp)

        toc = time.time() #in case api takes too long to call
        if new:
            power = data_comp[1]*u
            cost = 0
	    cost_hour = 0
	    new = False
        else:
            delta_power = power - data_comp[1]*u
	    power = data_comp[1]*u
	    power_window = power + delta_power/2
            cost = p*power_window*((toc-tic)/3660)/1000
	    cost = round(cost, 3)
	    cost_hour = p*power_window/1000
	    print(cost_hour)
	    cost_hour = round(cost_hour, 2)

        metrics = [power, cost, cost_hour]

        output = ','.join(str(x) for x in data_in) + ',' + ','.join(str(x) for x in data_out) \
                 + ',' + ','.join(str(x) for x in data_comp) + ',' +  ','.join(str(x) for x in metrics)

        file.write(output + "\n")
	print(output)
        tic = time.time()
        file.flush()
        time.sleep(interval_in)

    except KeyboardInterrupt:
        file.close()

