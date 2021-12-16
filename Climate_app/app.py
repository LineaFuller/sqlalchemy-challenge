from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from sqlalchemy.sql.expression import false
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

@app.route("/api/v1.0/stations")
def station():
    station_list: session.query(func.count(Measurement.station)).all()

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    most_active = 'USC00519281'
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    tob = session.query(Measurement.tobs).\
    filter(Measurement.station == most_active).\
    filter(Measurement.date >= query_date).all()

# Loop
    tobs_list = []
    for i in tob:
        tobs_list.append(i[0])

    
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def describe(start, end=False):
    if end: 
        calculations = session.query(func.min(Measurement.tobs), 
                func.max(Measurement.tobs), 
                func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
        session.close()
        # print (calculations)
        # spread operator: isolates tupple and activates spread 
        return jsonify([*calculations[0]])

    else:

        calculations = session.query(func.min(Measurement.tobs), 
                func.max(Measurement.tobs), 
                func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
        session.close()
        # print (calculations)
        # spread operator: isolates tupple and activates spread 
        return jsonify([*calculations[0]])

if __name__ == "__main__":
    app.run(debug=True)
