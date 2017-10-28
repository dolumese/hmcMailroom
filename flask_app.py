from flask import Flask
from flask import request
from flask import render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBEUG"] = True

# MySQL Database Set-up
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="hmcMailroom",
    password="MaiLlIAm",
    hostname="hmcMailroom.mysql.pythonanywhere-services.com",
    databasename="hmcMailroom$doorStatus",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class DoorStatus(db.Model):
    __tablename__ = "doorStatus"

    id = db.Column(db.DateTime, primary_key=True)
    status = db.Column(db.Integer)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    data = request.get_json()
    print(data) # print data to log
    return 'Successful: JSON data posted'

