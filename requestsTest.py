# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 20:26:47 2019

@author: pi
"""
from flask import Flask
from flask_restful import Resource, Api
import requests

url = 'http://api.openweathermap.org/data/2.5/weather?'
API_key = '07bafc834660819c6b0c515fe2a9cac9'

lat_yel = '51.49'
lon_yel = '-0.22'

url_input = url + 'appid=' + API_key +'&lat=' + lat_yel + '&lon=' + lon_yel

r = requests.get(url_input)
print(r.status_code)

app = Flask(__name__)
api = Api(app)

class Temperature(Resource):
    def get(self, time):
        if time == 'now':
            temperature = 'test'
            return {'outdoor temperature': temperature}

api.add_resource(Temperature, '/temperature/<string:time>')

app.run(port=5000)
            