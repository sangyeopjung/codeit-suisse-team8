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
def broadcaster():
    data = request.get_json()['data']

    message_dict = dict()

    for s in data:
        t = s.split("->")
        head, tail = t[0], t[1]
        if t[0] in message_dict:
            message_dict[t[0]].append(t[1])
        else:
            message_dict[t[0]] = [t[1]]

    tempKey = ""
    for key in message_dict.keys():
        for val in message_dict.values():
            if key in val:
                tempKey = key
    del message_dict[tempKey]

    result = []
    for key in message_dict:
        result.append(key)



    print("My result :{}".format(result))
    return jsonify(answer=result)
