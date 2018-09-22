import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/broadcaster/message-broadcast', methods=['POST'])
def broadcaster():
    data = request.get_json()['data']

    indeg = {}
    outdeg = {}

    all = []
    for s in data:
        t = s.split("->")
        u, v = t[0], t[1]

        if v not in indeg:
            indeg[v] = 0
        if u not in outdeg:
            outdeg[u] = 0

        indeg[v] += 1
        outdeg[u] += 1

        if u not in all:
            all.append(u)
        if v not in all:
            all.append(v)

    res = []
    for node in all:
        if node not in indeg:
            res.append(node)

    print("My result :{}".format(res))
    return jsonify(answer=res)
