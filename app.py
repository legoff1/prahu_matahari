from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Store all data, including Pilot & Dev
data = {
    "timestamp": None,
    "latitude": None,
    "longitude": None,
    "current_a0": None,
    "voltage_a1": None,
    "voltage_batt_mppt": None,
    "current_batt_mppt": None,
    "voltage_solar_mppt": None,
    "power_solar_mppt": None,
    "clouds": None,
    "daytime": None,
    "sunlight_score": None,
    "weather_description": None,
    "speed": None,
    "range_without_sun": None,
    "range_with_sun": None,
    "run_time_left_no_sun": None,
    "run_time_left_with_sun": None,
    "battery_soc": None
}

@app.route('/')
def index_redirect():
    return redirect(url_for('pilot'))

@app.route('/pilot')
def pilot():
    return render_template("index.html", mode="pilot", current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data=data)

@app.route('/dev')
def dev():
    return render_template("index.html", mode="dev", current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data=data)

@app.route('/update', methods=['POST'])
def update():
    content = request.json
    data.update(content)
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"status": "ok"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
