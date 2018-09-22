import logging
from datetime import datetime, timedelta

from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)

def toInteger(n):
    return int(n)

@app.route('/airtrafficcontroller', methods=['POST'])
def airtraffic():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    flights = data.get("Flights")
    numOfFlights = len(flights)
    sorted_flights = sorted(flights, key=lambda kv: kv["Time"])
    reservedTime = data.get("Static").ReserveTime
    #result = {"Flights" : []}
    if "Runways" in data.get("Static").keys():
        runways = data.get("Static").Runways
        for counter, flight in enumerate(sorted_flights):
            if(flight.get("Distressed", False)):
                reserved_flight = flight
                flights.remove(flight)
                flights.insert(0, reserved_flight)
                
        #result = {"Flights" : [{ "PlaneId": "TR123", "Time": "0200", "Runway": "A"}]}
    else:
        for i in range(1, numOfFlights):
            before = datetime.strptime(sorted_flights[i-1]["Time"], "%H%M")
            after = datetime.strptime(sorted_flights[i]["Time"], "%H%M")
            if after < before + timedelta(seconds=int(reservedTime)):
                 sorted_flights[i]["Time"] = (before + timedelta(seconds=int(reservedTime))).strftime("%H%M")

    print("My result :{}".format(result))
    return jsonify(sorted_flights)
