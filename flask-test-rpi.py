from flask import Flask, jsonify
from time import sleep 
from serial import Serial
from functions import data_inside, data_outside, get_code 
import bme680
import requests
from calendar import monthrange
import json
import sys

#Api requirements
api_key = '07bafc834660819c6b0c515fe2a9cac9'

#House Coordinates
lat_yel = 51.49
lon_yel = -0.22

#Heat loss coefficient
u = 127

#Price per kwh
p = 2.78

#Local Port
url = 'http://127.0.0.1:5000'

#Headers from sensing file
inside_headers = ['time', 'temp_in', 'press_in', 'hum_in']
outside_headers = ['time_measured', 'temp_out', 'press_out', 'hum_out']
comparison_headers = ['time_diff', 'temp_diff', 'press_diff', 'hum_diff']
metrics_headers = ['power', 'cost_window', 'cost_predict']

#Creating AP
app = Flask(__name__)

@app.route('/yeldham_inside', methods=['GET'])
def get_data():
    try:
	#Instantiate sensor
	sensor = bme680.BME680()
	sensor.set_humidity_oversample(bme680.OS_2X)
	sensor.set_pressure_oversample(bme680.OS_4X)
	sensor.set_temperature_oversample(bme680.OS_8X)
	sensor.set_filter(bme680.FILTER_SIZE_3)

	data_in = data_inside(sensor)
	
	return jsonify(datetime = data_in[0],
			temp_inside = data_in[1],
			press_inside = data_in[2],
			humidity_inside = data_in[3])

    except:
	return jsonify({'error': 'Sensor Failed'}), 503

@app.route('/yeldham_outside', methods=['GET'])
def get_data_out():
    global api_key
    global lat_yel
    global lon_yel
    
    try:
        data_out = data_outside(api_key, lat_yel, lon_yel)[0]
        return jsonify(datetime = data_out[0],
                        temp_outside = data_out[1],
			press_outside = data_out[2],
                        humidity_outside = data_out[3])

    except:
        return jsonify({'error': 'OWM API Failed: {}'.format(str(code))}), 503

@app.route('/metrics', methods=['GET'])
def get_metrics():
    global url
    global u
    global p

    try:
        outside_r = requests.get(url+'/yeldham_outside')
        data_out = outside_r.text
        data_out = json.loads(data_out)
    
        inside_r = requests.get(url+'/yeldham_inside')
        data_in = inside_r.text
        data_in = json.loads(data_in)

        delta_temp = float(data_in['temp_inside']) - float(data_out['temp_outside'])
        power = int(delta_temp*u)

        cost_hour = p*power/1000
        cost_hour = round(cost_hour, 2)

        cost_day = (cost_hour*24)/100 #In Sterling Pounds
        cost_day = round(cost_day, 2)
    
        date = data_in['datetime']
        if int(date[5:6]) == 0:
            month = int(date[6])
        else:
            month = int(date[5:6])
        year = int(date[0:3])
        days = monthrange(year, month)
        days = days[1]

        cost_month = cost_day*days 
        cost_month = round(cost_month, 2)

        return jsonify(power = power,
                        hourly_cost = cost_hour,
                        daily_cost = cost_day,
                        monthly_cost = cost_month,
                        temp_in = data_in['temp_inside'],
                        temp_out = data_out['temp_outside'])
    except:
	return jsonify({'error': 'Request failed'}), 503
    
@app.route('/dashboard', methods=['GET'])
def get_dashboard():
    global url

    try:
	metrics_r = requests.get(url+'/metrics')
	data_met = metrics_r.text
	data_met = json.loads(data_met)

        power = data_met['power']
	cost_hour = data_met['hourly_cost']
	cost_day = data_met['daily_cost']
	cost_month = data_met['monthly_cost']
	temp_in = data_met['temp_in']
	temp_out = data_met['temp_out']

        return '''
	<html>
	<body><h1>Yeldham Road Dashboard</h1></body>
	<br>
	<h2>Outside: {:.1f}&deg;<br>Inside: {:.1f}&deg; </h2>
	<br>
	<h2>How much are you spending&quest;</h2>
	<p>Predicted monthly cost: &#163;{:.2f} </p>
	<p>Predicted daily cost: {:.2f}p </p>
	<p>Current hourly cost: {:.2f}p </p>
	<br>
	<h3>Power Consumption: {:.0f}W </h3>
	<br>
	</html>
	'''.format(temp_in, temp_out, cost_month, cost_day, cost_hour, power)
    except:
	print "Unexpected error:", sys.exc_info()[0]
	return jsonify({'error': 'Request failed'}), 503

try:
    app.run()
except KeyboardInterrupt:
    print("\nCtrl-C pressed.")
