# from flask import Flask, request, render_template

# app = Flask(__name__)
# data = {"var1": None, "var2": None}

# @app.route('/')
# def index():
#     return render_template("index.html", var1=data["var1"], var2=data["var2"])

# @app.route('/update', methods=['POST'])
# def update():
#     content = request.json
#     data["var1"] = content.get("var1")
#     data["var2"] = content.get("var2")
#     return {"status": "ok"}, 200





from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

# Initialize with some sample/default values
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
    "weather_description": None
}

@app.route('/')
def index():
    return render_template("index.html", data=data)

@app.route('/update', methods=['POST'])
def update():
    content = request.json
    data.update(content)
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"status": "ok"}, 200
