from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return"Home Page"

@app.route("/api/v1.0/precipitation")
def precip():
    Precipitation = session.query(Measurement.prcp, Measurement.date).\
    filter(Measurement.date > '2016-08-23').all()

    prcp_dict = {}
    for row in Precipitation:
        prcp_dict[row[1]]=row[0]
        
    return jsonify(prcp_dict)

if __name__ == "__main__":
    app.run(debug=True)
