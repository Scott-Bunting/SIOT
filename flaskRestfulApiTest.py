# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 20:26:47 2019

@author: pi
"""
from flask import Flask
from flask_restful import Resource, Api
import pyowm

API_key = '07bafc834660819c6b0c515fe2a9cac9'

lat_yel = 51.49
lon_yel = -0.22

owm = pyowm.OWN(API_key)
observation = owm.weather_at_coords(lat_yel, lon_yel)

app = Flask(__name__)
api = Api(app)

class Temperature(Resource):
    def get(self, time):
        if time == 'now':
            w = observation.get_weather()
            temperature = w.get_temperature()
            return {'outdoor temperature': temperature}

api.add_resource(Temperature, '/temperature/<string:time>')

app.run(port=5000)
            