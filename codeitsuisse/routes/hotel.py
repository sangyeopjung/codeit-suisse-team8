import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/customers-and-hotel/minimum-distance', methods=['POST'])
def hotel():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    data = sorted(data)
    res = 1000000000000
    for i in range(1, len(data)):
        res = min(res, data[i] - data[i - 1])
    if len(data) == 1:
        res = 0
    print("My result :{}".format(res))
    return jsonify(answer=res)


@app.route('/customers-and-hotel/minimum-camps', methods=['POST'])
def hotel2():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    n = len(data)

    data = sorted(data, key=lambda k: k["pos"])
    pos = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        j = i + 1
        pos[i][i] = 1
        le = data[i]["pos"] - data[i]["distance"]
        ri = data[i]["pos"] + data[i]["distance"]
        while j < n:
            le = max(le, data[j]["pos"] - data[j]["distance"])
            ri = min(ri, data[j]["pos"] + data[j]["distance"])
            if le <= ri:
                pos[i][j] = 1
                j += 1
            else:
                break

    # print(pos)

    dp = [100000000 for _ in range(n)]
    dp[0] = 1
    for i in range(1, n):
        for j in range(i):
            if pos[j + 1][i] == 1:
                dp[i] = min(dp[i], dp[j] + 1)
        if pos[0][i] == 1:
            dp[i] = 1

    print("My result :{}".format(dp[n - 1]))
    return jsonify(answer=dp[n - 1])

