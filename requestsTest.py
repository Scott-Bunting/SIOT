# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 20:26:47 2019

@author: pi
"""
from flask import Flask
from flask_restful import Resource, Api
import requests
import json
import time
import os
from datetime import datetime

url = 'http://api.openweathermap.org/data/2.5/weather?'
api_key = '07bafc834660819c6b0c515fe2a9cac9'
path = "C:\Users\Scott\Documents\#Year 4\Sensing and IoT\Coursework\SIOT\data-storage\laptop\data_log_laptop.csv"
record = open(path,"a+")

lat_yel = 51.49
lon_yel = -0.22

def get_weather(api_key, lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}".format(lat, lon, api_key)
    r = requests.get(url)
    return r.text

if os.stat(path).st_size == 0:
    record.write("time_recorded,time_measured,temp_out,pressure_out,humidity_out\n")

start = time.time()
data_json = get_weather(api_key, lat_yel, lon_yel)
data = json.loads(data_json)

general = data['main']  # dictionary with general data
temperature = general['temp']
pressure = general['pressure']
humidity = general['humidity']

measured = datetime.utcfromtimestamp(data['dt']).strftime('%d/%m/%Y %H:%M:%S')
now = datetime.now()
now = now.strftime('%d/%m/%Y %H:%M:%S')

output = "{0}, {1}, {2:.2f}, {3:.2f}, {4:.2f}".format(now, measured, temperature, pressure, humidity)

record.write(output + "\n")
record.flush()
end = time.time()
count = 1
while True:
    if end-start > 60:
        data_json = get_weather(api_key, lat_yel, lon_yel)
        data = json.loads(data_json)

        general = data['main'] #dictionary with general data
        temperature = general['temp']
        pressure = general['pressure']
        humidity = general['humidity']

        measured = datetime.utcfromtimestamp(data['dt']).strftime('%d/%m/%Y %H:%M:%S')
        now = datetime.now()
        now = now.strftime('%d/%m/%Y %H:%M:%S')

        output = "{0}, {1}, {2:.2f}, {3:.2f}, {4:.2f}".format(now, measured, temperature, pressure, humidity)

        record.write(output + "\n")
        record.flush()
        time.sleep(1)
        start = time.time()
        count += 1
        if count > 3:
            print('finished')
            break
    time.sleep(30)
    print('loop')
    end = time.time()



#url_input = url + 'appid=' + API_key +'&lat=' + lat_yel + '&lon=' + lon_yel

# app = Flask(__name__)
# api = Api(app)
#
# class Temperature(Resource):
#     def get(self):
#         if time == 'now':
#             temperature = 'test'
#             return {'outdoor temperature': temperature}
#
# api.add_resource(Temperature, '/temperature/<string:time>')
#
# app.run(port=5000)

# data_json = get_weather(api_key,lat_yel,lon_yel)
# data = json.loads(data_json)
#
# #deleting unnecessary variables
# del data['sys']
# del data['visibility']
# del data['base']
# del data['id']
# print(data)
#
#
# name = data['name'] #name of location
#
# general = data['main'] #dictionary with general data
# temperature = general['temp']
# pressure = general['pressure']
# humidity = general['humidity']
# tim = datetime.utcfromtimestamp(data['dt']).strftime('%d/%m/%Y %H:%M:%S')
# print(tim)
#
# wind = data['wind'] #dictionary for wind data
# wind_speed = wind['speed']#could be used to tell people its probably not as cold as they think
# if len(wind) > 1:
#     wind_deg = wind['deg']
# else:
#     wind_deg = 0