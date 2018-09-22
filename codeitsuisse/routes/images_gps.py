import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/imagesGPS', methods=['POST'])
def images_gps():
    data = request.get_json();
    print("data sent for evaluation {}".format(data))

    print(data)

    print("My result :{}".format(result))
    return jsonify(result);
    return 0;
