import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/sorting-game', methods=['POST'])
def images_gps():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    result = []
    puzzle = data['puzzle']

    print(puzzle)


    print("My result :{}".format(result))
    return jsonify(result=result)
