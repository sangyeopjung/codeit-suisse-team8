import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/customers-and-hotel/minimum-distance', methods=['POST'])
def hotel():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    data = sorted(data)
    res = 1000000000000
    for i in range(1, len(data)):
        res = min(res, data[i] - data[i - 1])
    if len(data) == 1:
        res = 0
    print("My result :{}".format(res))
    return jsonify(answer=res)
