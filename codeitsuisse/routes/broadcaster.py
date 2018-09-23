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
    print(data)

    msg_dict = dict()


    for s in data:
        t = s.split("->")
        head, tail = t[0], t[1]
        if head in msg_dict:
            msg_dict[head].append(tail)
        else:
            msg_dict[head] = [tail]

    G = nx.DiGraph()
    for k,v in msg_dict.items():
        for vv in v:
            G.add_edge(k, vv)
    result = []
    for node in G.nodes():
        if G.in_edges(node, data=True):
            continue
        else:
            #print(node)
            result.append(node)


    print("My result :{}".format(result))
    return jsonify(answer=result)


@app.route('/broadcaster/most-connected-node', methods=['POST'])
def broadcaster2():
    data = request.get_json()['data']

    graph = dict()
    for s in data:
        t = s.split("->")
        head, tail = t[0], t[1]
        if head == tail:
            continue

        if head in graph:
            graph[head].append(tail)
        else:
            graph[head] = [tail]

    G = nx.DiGraph()
    for k,v in graph.items():
        for vv in v:
            G.add_edge(k, vv)
    cycleEdge = nx.find_cycle(G)
    G.remove_edge(cycleEdge[0][0],cycleEdge[0][1])

    result = nx.dag_longest_path(G)[0]

    print("My result :{}".format(result))
    return jsonify(answer=result)


@app.route('/broadcaster/fastest-path', methods=['POST'])
def broadcaster3():
    data = request.get_json()['data']
    sender = request.get_json()['sender']
    recipient = request.get_json()['recipient']

    g = nx.DiGraph()

    # edges = []
    for d in data:
        d = d.split(',')
        e, w = d[0], d[1]
        e = e.split('->')
        #edges.append((e[0], e[1], w))
        g.add_edge(e[0], e[1], weight=int(w))

    result = nx.dijkstra_path(g, sender, recipient, weight='weight')

    print("My result :{}".format(result))
    return jsonify(result=result)
