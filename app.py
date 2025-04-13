from flask import Flask, request, render_template

app = Flask(__name__)
data = {"var1": None, "var2": None}

@app.route('/')
def index():
    return render_template("index.html", var1=data["var1"], var2=data["var2"])

@app.route('/update', methods=['POST'])
def update():
    content = request.json
    data["var1"] = content.get("var1")
    data["var2"] = content.get("var2")
    return {"status": "ok"}, 200
