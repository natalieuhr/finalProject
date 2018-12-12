import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import json


# Modified from CS50 finance

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///bird.db")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/honeycreepers")
def honeycreepers():
    return render_template("honeycreepers.html")


@app.route("/tarweeds")
def tarweeds():
    return render_template("tarweeds.html")


@app.route("/input", methods=["GET", "POST"])
def userinput():
    if request.method == "GET":
        # send list of birds to input.html to make drop down box options
        birds = db.execute("SELECT species FROM catalog")
        return render_template("input.html", birds=birds)
    else:
        # store input and check to make sure input is valid
        name = request.form.get("bird")
        lat = request.form.get("latitude")
        lon = request.form.get("longitude")
        if not name or not lat or not lon:
                return redirect("/")
        # insert information into markers database
        db.execute("INSERT INTO markers (name, latitude, longitude) VALUES (:name, :lat, :lon)", name=name, lat=lat, lon=lon)
        return redirect("/heatmap")


@app.route("/heatmap")
def heatmap():
    # select everything from markers to send to heatmap.html
    rows = db.execute("SELECT * FROM markers")
    return render_template("heatmap.html")


@app.route("/catalog")
def catalog():
    # select everything from catalog for catalog.html
    birds = db.execute("SELECT * FROM catalog")
    return render_template("catalog.html", birds=birds)


@app.route("/update", methods=["GET"])
def update():
    # select data from markers and catalog for heatmap
    data = db.execute("SELECT name, latitude, longitude, Time, marker FROM markers INNER JOIN catalog ON markers.name=catalog.species")
    if data:
        return jsonify(data)
