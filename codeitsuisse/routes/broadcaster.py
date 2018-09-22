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

    g = {}

    for s in data:
        t = s.split("->")
        u, v = t[0], t[1]
        if u not in g:
            g[u] = []
        g[u].append(v)

    topSort = []
    used = {}
    for key in g:
        if key not in used:
            order = []
            dfs(g, used, key, order)
            topSort.extend(order)

    result = []
    topSort = topSort[::-1]
    used = {}
    for v in topSort:
        if v not in used:
            result.append(v)
            dfs(g, used, v, [])

    print("My result :{}".format(result))
    return jsonify(answer=result)
