import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/tetris', methods=['POST'])
def images_gps():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    actions = []
    s = data['tetrominoSequence']




    print("My result :{}".format(actions))
    return jsonify(actions=actions)
