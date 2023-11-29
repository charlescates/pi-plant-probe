from flask import Flask, render_template
from plant_monitor import PlantMonitor
myMonitor = PlantMonitor()
app = Flask(__name__)
@app.route('/')
def index():
    temperature = myMonitor.get_temp()
    humidity = myMonitor.get_humidity()
    wetness = myMonitor.get_wetness()
    templateData = {
        'temperature' : temperature,
        'humidity' : humidity,
        'wetness' : wetness
    }
    return render_template('index.html', **templateData)
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')