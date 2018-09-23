import logging
import networkx as nx
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

    msg_dict = dict()


    for s in data:
        t = s.split("->")
        head, tail = t[0], t[1]
        if head in msg_dict:
            msg_dict[head].append(tail)
        else:
            msg_dict[head] = [tail]
    final = []
    for key in msg_dict.keys():
        for val in msg_dict.values():
            if key in val:
                final.append(key)

    for i in final:
        del msg_dict[i]
    result = list(msg_dict.keys())

    print("My result :{}".format(result))
    return jsonify(answer=result)


@app.route('/broadcaster/most-connected-node', methods=['POST'])
def broadcaster2():
    data = request.get_json()['data']

    def most_connected_path(g):
        d = {}
        for node in nx.topological_sort(g):
            pairs = [(d[v][0]+1,v) for v in g.pred[node]]
            if pairs:
                d[node] = max(pairs)
            else:
                d[node] = (0, node)
        node,(length,_)  = max(d.items(), key=lambda x:x[1])
        path = []
        while length > 0:
            path.append(node)
            length,node = d[node]
        return list(reversed(path))




    graph = dict()
    for s in data:
        t = s.split("->")
        head, tail = t[0], t[1]
        if head in graph:
            graph[head].append(tail)
        else:
            graph[head] = [tail]

    G = nx.DiGraph()
    for k,v in graph.items():
        for vv in v:
            G.add_edge(k, vv)

    result = nx.dag_longest_path(G)[0]



    print("My result :{}".format(result))
    return jsonify(answer=result)


@app.route('/broadcaster/fastest-path', methods=['POST'])
def broadcaster3():
    data = request.get_json()['data']





    print("My result :{}".format(result))
    return jsonify(answer=result)
