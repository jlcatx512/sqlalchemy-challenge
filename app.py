# Jadd Cheng
# October 2, 2019

# Import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Flask app instance
app = Flask(__name__)

#################################################
# Routes
#################################################

#################################################
# Route 1 / - Home page.
# Function: List all routes that are available.
#################################################
@app.route("/")
def home():
    return (
        f"<strong>Available Routes:</strong><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&ltstart&gt<br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt<br/>"
    )

#################################################
# Route 2
# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)

#################################################
# Route 3
# Return a JSON list of stations from the dataset.
#################################################
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # """Return a list of all stations"""

    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    df_stations = pd.DataFrame(results)
    all_stations_json = df_stations.to_json(orient='records')

    # Convert list of tuples into normal list
    # all_stations = list(np.ravel(all_stations))
    return jsonify(all_stations_json)

#################################################
# Route 4
# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
#################################################

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d').date()
    first_date = last_date - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date <=last_date, Measurement.date>=first_date).order_by(Measurement.date.desc()).all()
    session.close()

    # Create DataFrame from session query.
    df_tobs = pd.DataFrame(results)
    tobs_json = df_tobs.to_json(orient='records')

    return jsonify(tobs_json)
    
#################################################
# Route 5
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
#################################################
    # """TMIN, TAVG, and TMAX for a list of dates.
    # Args:
    #     start_date (string): A date string in the format %Y-%m-%d
    #     end_date (string): A date string in the format %Y-%m-%d
    # Returns:
    #     TMIN, TAVE, and TMAX
    # """

@app.route("/api/v1.0/<start>")
def calc_temps(start):
    session = Session(engine)
    start = dt.datetime.strptime(start, '%Y-%m-%d').date()
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    
    # df = pd.DataFrame(results)
    # df = df.to_json(orient='records')
    
    return jsonify(results)

# error
# message = "Date wrong"
# return message, 404

#################################################
# Route 6
#################################################
@app.route("/api/v1.0/<start>/<end>")
def calc_temps2(start, end):
    session = Session(engine)
    start = dt.datetime.strptime(start, '%Y-%m-%d').date()
    end = dt.datetime.strptime(end, '%Y-%m-%d').date()
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    results = list(results)    
    return jsonify(results)

# message = jsonify({"error": f"Character with real_name {real_name} not found."})
#     return message, 404
#################################################
# app.run
#################################################
if __name__ == "__main__":
    app.run(debug=True)