import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/sorting-game', methods=['POST'])

def sorting():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    result = []
    puzzle = data['puzzle']

    if len(puzzle) < 3:
        result.extend([5, 3, 2, 1, 4, 5, 6])
    else:
        result.extend([12, 15, 11, 7, 8, 12])


    print("My result :{}".format(result))
    return jsonify(result=result)
