from datetime import datetime
import requests
import time
import json

def get_weather(api_key, lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}".format(lat, lon, api_key)
    r = requests.get(url)
    code = r.status_code
    return r.text

def get_code(api_key, lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}".format(lat, lon, api_key)
    r = requests.get(url)
    code = r.status_code
    return code

def data_inside(sensor):
    temp_in = sensor.data.temperature
    press_in = sensor.data.pressure
    hum_in = sensor.data.humidity
    now = datetime.now()
    now = now.strftime('%Y/%m/%d %H:%M:%S')

    return [now, temp_in, press_in, hum_in]

def data_outside(api_key, lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}".format(lat, lon,
                                                                                                       api_key)
    r = requests.get(url)
    data_json = r.text
    data = json.loads(data_json)
    general = data['main']
    temp_out = general['temp']
    press_out = general['pressure']
    hum_out = general['humidity']
    rec = datetime.utcfromtimestamp(data['dt']).strftime('%Y/%m/%d %H:%M:%S')

    return [rec, temp_out, press_out, hum_out]
