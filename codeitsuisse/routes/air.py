import logging
from datetime import datetime, timedelta

from heapq import heappush, heappop, heapify
from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)

# """
# def flight(sorted_flights, lengthRun):
#     for counter, flight in enumerate(sorted_flights):
#         if(counter >= lengthRun):
#             before = datetime.strptime(sorted_flights[counter-lengthRun]["Time"], "%H%M")
#             after = datetime.strptime(sorted_flights[counter]["Time"], "%H%M")
#             if after < before + timedelta(seconds=int(reservedTime)):
#                  sorted_flights[counter]["Time"] = (before + timedelta(seconds=int(reservedTime))).strftime("%H%M")
#         flight["Runway"] = runways[counter%lengthRun]
#     return sorted_flights
# """
# @app.route('/airtrafficcontroller', methods=['POST'])
# def airtraffic():
#     data = request.get_json()
#     print("data sent for evaluation {}".format(data))
#
#     flights = data.get("Flights")
#     numOfFlights = len(flights)
#     sorted_flights = sorted(flights, key=lambda kv: (kv["Time"], kv["PlaneId"]))
#     reservedTime = data.get("Static").get("ReserveTime")
#
#     if "Runways" in data.get("Static").keys():
#         runways = data.get("Static").get("Runways")
#         sorted_runways = sorted(runways)
#         lengthRun = len(sorted_runways)
#
#         for flight in sorted_flights:
#             if(flight.get("Distressed", False)):
#                 flight.pop("Distressed")
#                 reserved_flight = flight
#                 sorted_flights.remove(flight)
#                 sorted_flights.insert(0, reserved_flight)
#                 for counter, flight in enumerate(sorted_flights):
#                     if(counter >= lengthRun):
#                         before = datetime.strptime(sorted_flights[counter-lengthRun]["Time"], "%H%M")
#                         after = datetime.strptime(sorted_flights[counter]["Time"], "%H%M")
#                         if after < before + timedelta(seconds=int(reservedTime)):
#                              sorted_flights[counter]["Time"] = (before + timedelta(seconds=int(reservedTime))).strftime("%H%M")
#                     flight["Runway"] = runways[counter%lengthRun]
#                 results = {"Flights" : sorted_flights}
#                 return jsonify(results)
#
#         for counter, flight in enumerate(sorted_flights):
#             if(counter >= lengthRun):
#                 for i in range(lengthRun):
#                     before = datetime.strptime(sorted_flights[counter-i-lengthRun]["Time"], "%H%M")
#                     after = datetime.strptime(sorted_flights[counter]["Time"], "%H%M")
#                     if after > before + timedelta(seconds=int(reservedTime)):
#                          sorted_flights[counter]["Time"] = (before + timedelta(seconds=int(reservedTime))).strftime("%H%M")
#                     flight["Runway"] = runways[counter%lengthRun]
#
#                 if after < before + timedelta(seconds=int(reservedTime)):
#                      sorted_flights[counter]["Time"] = (before + timedelta(seconds=int(reservedTime))).strftime("%H%M")
#             else:
#                 flight["Runway"] = sorted_runways[counter%lengthRun]
#
#     else:
#         for i in range(1, numOfFlights):
#             before = datetime.strptime(sorted_flights[i-1]["Time"], "%H%M")
#             after = datetime.strptime(sorted_flights[i]["Time"], "%H%M")
#             if after < before + timedelta(seconds=int(reservedTime)):
#                  sorted_flights[i]["Time"] = (before + timedelta(seconds=int(reservedTime))).strftime("%H%M")
#
#     print("My result :{}".format(sorted_flights))
#     results = {"Flights" : sorted_flights}
#     return jsonify(results)




def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def cmp(x, y):
    print('fuck', x, y)
    if x['Distressed'] != y['Distressed']:
        return x['Distressed']
    if x['Time'] != y['Time']:
        print(x['Time'], y['Time'], x['Time'] < y['Time'])
        return x['Time'] < y['Time']
    return x['PlaneId'] < y['PlaneId']

@app.route('/airtrafficcontroller', methods=['POST'])
def air():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    flights = data['Flights']
    for i in range(len(flights)):
        flights[i]['Time'] = datetime(1, 1, 1, int(flights[i]['Time']) // 100, int(flights[i]['Time']) % 100, 0)
        if 'Distressed' not in flights[i]:
            flights[i]['Distressed'] = 1
        elif flights[i]['Distressed'] == 'true':
            flights[i]['Distressed'] = 0
        else:
            flights[i]['Distressed'] = 1
    reserve = int(data['Static']['ReserveTime'])

    flights = sorted(flights, key=lambda k: (k['Distressed'], k['Time'], k['PlaneId']))
    print(flights)
    if 'Runways' in data['Static']:
        runways = data['Static']['Runways']
        times = {}

        for i in range(len(runways)):
            times[runways[i]] = datetime(1,1,1,0,0,0)

        response = []
        for flight in flights:
            #time, runway = heappop (runways)
            rw = ''

            flightTime = flight['Time']
            for i in times:
                print(times[i], flightTime)
                if times[i] <= flightTime:
                    if rw == '' or rw > i:
                        rw = i
            if rw == '':
                for i in times:
                    if rw == '' or rw > i:
                        rw = i
            time = times[rw]
            time = max(time, flightTime)
            response.append({'PlaneId': flight['PlaneId'], 'Time': time.strftime("%H%M"), 'Runway': rw})
            time = time + timedelta(0, reserve)
            times[rw] = time
            #heappush(runways, (time, runway))
        return jsonify(Flights=response)
    else:
        response = []
        time = datetime(1,1,1,0,0,0)
        for flight in flights:
            flightTime = flight['Time']
            time = max(time, flightTime)
            response.append({'PlaneId': flight['PlaneId'], 'Time': time.strftime("%H%M")})
            time = time + timedelta(0, reserve)
        return jsonify(Flights=response)


