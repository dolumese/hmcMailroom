from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)
app.config["DEBEUG"] = True

@app.route('/')
def index():
    return render_template("index.html")

