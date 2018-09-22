import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/tetris', methods=['POST'])
def tetris():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    actions = []
    s = data['tetrominoSequence']

    print(s)


    print("My result :{}".format(actions))
    return jsonify(actions=actions)
