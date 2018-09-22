import logging
from datetime import datetime, timedelta

from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)

"""
def flight(sorted_flights, lengthRun):
    for counter, flight in enumerate(sorted_flights):
        if(counter >= lengthRun):
            before = datetime.strptime(sorted_flights[counter-lengthRun]["Time"], "%H%M")
            after = datetime.strptime(sorted_flights[counter]["Time"], "%H%M")
            if after < before + timedelta(seconds=int(reservedTime)):
                 sorted_flights[counter]["Time"] = (before + timedelta(seconds=int(reservedTime))).strftime("%H%M")
        flight["Runway"] = runways[counter%lengthRun]
    return sorted_flights
"""
@app.route('/airtrafficcontroller', methods=['POST'])
def airtraffic():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    flights = data.get("Flights")
    numOfFlights = len(flights)
    sorted_flights = sorted(flights, key=lambda kv: (kv["Time"], kv["PlaneId"]))
    reservedTime = data.get("Static").get("ReserveTime")

    if "Runways" in data.get("Static").keys():
        runways = data.get("Static").get("Runways")
        sorted_runways = sorted(runways)
        lengthRun = len(sorted_runways)

        for flight in sorted_flights:
            if(flight.get("Distressed", False)):
                flight.pop("Distressed")
                reserved_flight = flight
                sorted_flights.remove(flight)
                sorted_flights.insert(0, reserved_flight)
                for counter, flight in enumerate(sorted_flights):
                    if(counter >= lengthRun):
                        before = datetime.strptime(sorted_flights[counter-lengthRun]["Time"], "%H%M")
                        after = datetime.strptime(sorted_flights[counter]["Time"], "%H%M")
                        if after < before + timedelta(seconds=int(reservedTime)):
                             sorted_flights[counter]["Time"] = (before + timedelta(seconds=int(reservedTime))).strftime("%H%M")
                    flight["Runway"] = runways[counter%lengthRun]
                results = {"Flights" : sorted_flights}
                return jsonify(results)

        for counter, flight in enumerate(sorted_flights):
            if(counter >= lengthRun):
                for i in range(lengthRun):
                    before = datetime.strptime(sorted_flights[counter-i-lengthRun]["Time"], "%H%M")
                    after = datetime.strptime(sorted_flights[counter]["Time"], "%H%M")
                    if after > before + timedelta(seconds=int(reservedTime)):
                         sorted_flights[counter]["Time"] = (before + timedelta(seconds=int(reservedTime))).strftime("%H%M")
                    flight["Runway"] = runways[counter%lengthRun]

                if after < before + timedelta(seconds=int(reservedTime)):
                     sorted_flights[counter]["Time"] = (before + timedelta(seconds=int(reservedTime))).strftime("%H%M")
            else:
                flight["Runway"] = sorted_runways[counter%lengthRun]

    else:
        for i in range(1, numOfFlights):
            before = datetime.strptime(sorted_flights[i-1]["Time"], "%H%M")
            after = datetime.strptime(sorted_flights[i]["Time"], "%H%M")
            if after < before + timedelta(seconds=int(reservedTime)):
                 sorted_flights[i]["Time"] = (before + timedelta(seconds=int(reservedTime))).strftime("%H%M")

    print("My result :{}".format(sorted_flights))
    results = {"Flights" : sorted_flights}
    return jsonify(results)
