import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/airtrafficcontroller', methods=['POST'])
def air_traffic_controller():
    data = request.get_json();
    print("data sent for evaluation {}".format(data))

    flights = data.get("Flights");
    reservedTime = data.get("Static")
    print(flights, flights[0])
    print(reservedTime)

    # print("My result :{}".format(result))
    #return jsonify(result);
    return 0;
