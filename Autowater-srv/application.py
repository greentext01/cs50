from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3
from passlib.hash import pbkdf2_sha256

from flask.wrappers import Response
from werkzeug.utils import redirect

app = Flask(__name__)
CORS(app)
db = sqlite3.connect("autowater.db", check_same_thread=False)
threshold = "2000"
pass_hash = "$pbkdf2-sha256$29000$Wusdg9D6HyNk7N3buzem1A$2zUxVFXLRdLHPosoXL9K.KyiPEolNe0H9wsdVDUucfU"


def verify(value, password):
    if value == None or password == None:
        return 400

    if value.isdigit():
        if login(password):
            return 200
        else:
            return 403
    else:
        return 400


@app.route("/", methods=["POST"])
def handle_index():
    if request.method == "POST":
        print(request.form)
        status = verify(request.form.get("moisture"),
                        request.form.get("password"))
        if status == 200:

            db.execute("INSERT INTO moisture VALUES (?, ?, ?);",
                       (request.form.get("moisture"), threshold, datetime.now().strftime("%m-%d %H:%M")))
            db.commit()
            return threshold
        return Response(status=status)


@app.route("/api/moisture")
def handle_moisture():
    cur = db.cursor()

    cur.execute(
        "SELECT * FROM (SELECT * FROM moisture ORDER BY time DESC LIMIT 200) ORDER BY time ASC;")

    data = {"moisture": [], "threshold": [], "time": []}

    for item in cur.fetchall():
        data["moisture"].append(item[0])
        data["threshold"].append(item[1])
        data["time"].append(item[2])
    return jsonify(data)


@app.route("/api/threshold", methods=["POST"])
def handle_threshold():
    print(request.data)
    status = verify(request.form.get("threshold"),
                    request.form.get("password"))
    if status == 200:
        global threshold
        threshold = request.form.get("threshold")
    return Response(status=status)


def login(password):
    return pbkdf2_sha256.verify(password, pass_hash)
