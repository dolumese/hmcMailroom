from flask import Flask
from flask import request
from flask import render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

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

    timestamp = db.Column(db.DateTime, primary_key=True)
    status = db.Column(db.Integer, nullable=False)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        currStat = DoorStatus.query.order_by(DoorStatus.timestamp.desc()).first()
        return render_template("index.html", currentStatus=currStat)

    data = request.get_json()

    status = DoorStatus(timestamp=datetime.now(pytz.UTC).astimezone(pytz.timezone('US/Pacific')), status=data["doorStatus"])
    db.session.add(status)
    db.session.commit()


    # print(data) # print data to log
    return redirect(url_for('index'))

