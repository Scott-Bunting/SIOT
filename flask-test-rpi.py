from flask import Flask, jsonify
from time import sleep 
from serial import Serial
from functions import data_inside, data_outside 
import bme680

#Headers from sensing file
inside_headers = ['time', 'temp_in', 'press_in', 'hum_in']
outside_headers = ['time_measured', 'temp_out', 'press_out', 'hum_out']
comparison_headers = ['time_diff', 'temp_diff', 'press_diff', 'hum_diff']
metrics_headers = ['power', 'cost_window', 'cost_predict']

#Creating API
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
    try:
        #Instantiate sensor
        sensor = bme680.BME680()
        sensor.set_humidity_oversample(bme680.OS_2X)
        sensor.set_pressure_oversample(bme680.OS_4X)
        sensor.set_temperature_oversample(bme680.OS_8X)
        sensor.set_filter(bme680.FILTER_SIZE_3)

        data_in = data_inside(sensor)

        return jsonify(datetime = 'test',
                        temp_inside = data_in[1],
			press_inside = data_in[2],
                        humidity_inside = data_in[3])

    except:
        return jsonify({'error': 'Sensor Failed'}), 503

try:
    app.run()
except KeyboardInterrupt:
    print("\nCtrl-C pressed.")
