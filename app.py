from flask import Flask, request, render_template
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

app = Flask(__name__)

# Store all data, including Pilot & Dev
data = {
    "timestamp": None,
    "data": []  # List to store last 100 lines of CSV data
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
    
    # Generate graphs for Developer Mode
    if data["data"]:
        df = pd.DataFrame(data["data"])

        # Plot the evolution of the state of charge (battery_soc), current A0, and speed
        fig, ax = plt.subplots(3, 1, figsize=(10, 8))

        # Plot Battery SOC
        ax[0].plot(df['timestamp'], df['battery_soc'], label='State of Charge (%)', color='b')
        ax[0].set_title('Battery State of Charge (SOC) Evolution')
        ax[0].set_xlabel('Time')
        ax[0].set_ylabel('SOC (%)')

        # Plot Current A0
        ax[1].plot(df['timestamp'], df['current_a0'], label='Current A0 (A)', color='r')
        ax[1].set_title('Current A0 Evolution')
        ax[1].set_xlabel('Time')
        ax[1].set_ylabel('Current A0 (A)')

        # Plot Speed
        ax[2].plot(df['timestamp'], df['speed'], label='Speed (km/h)', color='g')
        ax[2].set_title('Speed Evolution')
        ax[2].set_xlabel('Time')
        ax[2].set_ylabel('Speed (km/h)')

        # Format the x-axis to avoid cluttering
        for a in ax:
            a.tick_params(axis='x', rotation=45)
            a.legend()

        # Save plot to a BytesIO object and encode it for HTML rendering
        img = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode('utf-8')
        
    else:
        graph_url = None

    return render_template("dev_mode.html", mode="dev", current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data=latest_data, graph_url=graph_url)

@app.route('/update', methods=['POST'])
def update():
    content = request.json
    data.update(content)
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"status": "ok"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
