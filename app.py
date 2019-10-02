# October 2, 2019
# Check if there was starter code available.
# Import dependencies
from flask import Flask, jsonify

## Routes

## Route 1 / - Home page.
# Function: List all routes that are available.

@app("/")
def home():
    pass

# Route 2
# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app("/api/v1.0/precipitation")
def precipitation():
    pass

# Route 3
# Return a JSON list of stations from the dataset.
@app("/api/v1.0/stations")
def stations():
    pass

# Route 4
# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
@app("/api/v1.0/tobs")
def tobs():
    pass

# Route 5
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app("/api/v1.0/<start>") and
def start():
    pass

# Router 6
@app("/api/v1.0/<start>/<end>")
def startend():
    pass

# app.run
if __name__ == "__main__":
    app.run(debug=True)