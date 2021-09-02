import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        if(request.form.get("month").isdigit() and request.form.get("day").isdigit() and request.form.get(
                "name") != "" and int(request.form.get("month")) <= 12 and int(request.form.get("day")) <= 31):

            db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?);", request.form.get(
                "name"), request.form.get("month"), request.form.get("day"))

        return redirect("/")

    else:

        birthdays = db.execute("SELECT name, day, month FROM BIRTHDAYS;")

        return render_template("index.html", bdays=birthdays)


@app.route("/delete", methods=["POST"])
def delete():
    db.execute("DELETE FROM birthdays WHERE name = ?;", request.form.get(
        "name"))

    return redirect("/")
