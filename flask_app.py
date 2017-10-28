from flask import Flask
from flask import request
from flask import render_template, redirect, url_for

app = Flask(__name__)
app.config["DEBEUG"] = True

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    data = request.get_json()
    print(data) # print data to log
    return 'Successful: JSON data posted'

