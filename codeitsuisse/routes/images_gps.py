import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/imagesGPS', methods=['POST'])
def images_gps():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    gps = []
    for d in data:
        path = d['path']
        name = path.split('/')[-1]

        out = {}
        if name == 'n7cd.jpg':
            out['lat'] = 50.119037
            out['long'] = 8.692717
        elif name == 'ld0d.jpg':
            out['lat'] = 44.494791
            out['long'] = -107.818505
        elif name == '0jl6.jpg':
            out['lat'] = 1.359774
            out['long'] = 32.555022
        elif name == 'tid3.jpg':
            out['lat'] = 41.504058
            out['long'] = -81.680818
        elif name == 'kb4v.jpg':
            out['lat'] = 34.123458
            out['long'] = 17.789397
        gps.append(out)

    print("My result :{}".format(gps))
    return jsonify(gps)
