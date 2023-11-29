from flask import Flask
from plant_monitor import PlantMonitor
myMonitor = PlantMonitor()
app = Flask(__name__)
@app.route('/')
def index():
    return 'Temperature: ' + myMonitor.get_temp() + '\nHumidity: ' + myMonitor.get_humidity()
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')