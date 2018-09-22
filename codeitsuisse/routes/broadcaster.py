import logging

from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)


def dfs(G, used, v, order):
    used[v] = 1
    if v in G:
        for to in G[v]:
            if to not in used:
                dfs(G, used, to, order)
    order.append(v)


@app.route('/broadcaster/message-broadcast', methods=['POST'])
def broadcaster1():
    data = request.get_json()['data']

    result = []
    tailList = []
    for s in data:
        t = s.split("->")
        head, tail = t[0], t[1]
        if tail in result:
            result.remove(tail)
            tailList.append(tail)
            result.append(head)
        elif head in tailList:
            continue
        else:
            result.append(head)
            tailList.append(tail)

    print("My result :{}".format(result))
    return jsonify(answer=result)


@app.route('/broadcaster/most-connected-node', methods=['POST'])
def broadcaster2():
    data = request.get_json()['data']





    print("My result :{}".format(result))
    return jsonify(answer=result)


@app.route('/broadcaster/fastest-path', methods=['POST'])
def broadcaster3():
    data = request.get_json()['data']





    print("My result :{}".format(result))
    return jsonify(answer=result)
