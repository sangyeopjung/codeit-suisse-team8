import logging

from flask import request, jsonify;

from codeitsuisse import app;

import urllib
import exifread as ef

logger = logging.getLogger(__name__)

def convert(value):
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


@app.route('/imagesGPS', methods=['POST'])
def images_gps():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    gps = []
    for d in data:
        url = d['path']
        filepath = url.split('/')[-1]
        f = open(filepath, 'wb')
        f.write(urllib.request.urlopen(url).read())
        f.close()

        with open(filepath, 'rb') as f:
            tags = ef.process_file(f)
            lat = tags.get('GPS GPSLatitude')
            lat_ref = tags.get('GPS GPSLatitudeRef')
            long = tags.get('GPS GPSLongitude')
            long_ref = tags.get('GPS GPSLongitudeRef')

            lat = convert(lat)
            if lat_ref.values == 'S':
                lat *= -1
            long = convert(long)
            if long_ref.values == 'W':
                long *= -1

            gps.append({'lat': lat, 'long': long})

    print("My result :{}".format(gps))
    return jsonify(gps)
