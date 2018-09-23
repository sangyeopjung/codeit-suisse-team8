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





    print("My result :{}".format(result))
    return jsonify(answer=result)


@app.route('/broadcaster/fastest-path', methods=['POST'])
def broadcaster3():
    data = request.get_json()['data']
    sender = request.get_json()['sender']
    recipient = request.get_json()['recipient']

    G = nx.DiGraph()
    #dict_cost = {}
    #list_send_end = []
    dict_name = {}
    for index, d in enumerate(data):
        t = d.split(",")
        path, cost = t[0], t[1]
        print(t[0], t[1])
        #G.add_node
        s = path.split("->")
        #dict_cost[(s[0], s[1])] = cost
        new_index = 2*index
        if (s[0] not in dict_name.keys()):
            dict_name[s[0]] = new_index
            print(s[0], new_index)
            G.add_node(new_index)

        if (s[1] not in dict_name.keys()):
            dict_name[s[1]] = new_index + 1
            G.add_node(new_index + 1)
            print(s[1], new_index + 1)
        #G.add_edge(dict_name[s[0]], dict_name[s[1]], weight = cost)
        G.add_weighted_edges_from([(dict_name[s[0]],dict_name[s[1]],cost)])
        print(cost)

    print(G.nodes())
    print(G.edges())

        #if sender == s[0]:
        #    list_send_end.append(s[1])
    print(dict_name[sender], dict_name[recipient])
    print(G.edges[dict_name[sender], dict_name[recipient]][weight])
    list = nx.dijkstra_path(G, dict_name[sender], dict_name[recipient])


    """
    min_cost = dict_cost.get((sender, recepient), 0)
    minList = [sender, recepient]

    for index, city in enumerate(list_send_end):
        tempList = []
        tempList.append(city)
        for key, value in tempList:
            if
    """

    print("My result :{}".format(list))
    return jsonify(list)
