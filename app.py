from flask import Flask, request, render_template
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

app = Flask(__name__)

# Store latest timestamp and the last 100 entries
data = {
    "timestamp": None,
    "data": []  # List of dicts, each representing a CSV row
}

@app.route('/')
def index_redirect():
    return render_template("index.html", mode="pilot", current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data=data)

@app.route('/pilot')
def pilot():
    latest_data = data["data"][-1] if data["data"] else {}
    return render_template("index.html", mode="pilot", current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data=latest_data)

@app.route('/dev')
def dev():
    latest_data = data["data"][-1] if data["data"] else {}

    graph_url = None
    if data["data"]:
        try:
            df = pd.DataFrame(data["data"])

            # Convert numeric columns
            for col in ['battery_soc', 'current_a0', 'speed']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # Plot the evolution of battery_soc, current_a0, and speed
            fig, ax = plt.subplots(3, 1, figsize=(10, 8))

            ax[0].plot(df['timestamp'], df['battery_soc'], label='State of Charge (%)', color='b')
            ax[0].set_title('Battery State of Charge (SOC) Evolution')
            ax[0].set_xlabel('Time')
            ax[0].set_ylabel('SOC (%)')

            ax[1].plot(df['timestamp'], df['current_a0'], label='Current A0 (A)', color='r')
            ax[1].set_title('Current A0 Evolution')
            ax[1].set_xlabel('Time')
            ax[1].set_ylabel('Current A0 (A)')

            ax[2].plot(df['timestamp'], df['speed'], label='Speed (km/h)', color='g')
            ax[2].set_title('Speed Evolution')
            ax[2].set_xlabel('Time')
            ax[2].set_ylabel('Speed (km/h)')

            for a in ax:
                a.tick_params(axis='x', rotation=45)
                a.legend()

            img = io.BytesIO()
            plt.tight_layout()
            plt.savefig(img, format='png')
            img.seek(0)
            graph_url = base64.b64encode(img.getvalue()).decode('utf-8')
        except Exception as e:
            print("Failed to plot:", e)

    return render_template("dev_mode.html", mode="dev", current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data=latest_data, graph_url=graph_url)

@app.route('/update', methods=['POST'])
def update():
    try:
        content = request.get_json()

        # Make sure 'data' exists and is a list
        if "data" in content and isinstance(content["data"], list):
            data["data"] = content["data"][-100:]  # Keep only last 100 rows
        else:
            return {"status": "bad request", "error": "Invalid data format"}, 400

        data["timestamp"] = content.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return {"status": "ok"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
