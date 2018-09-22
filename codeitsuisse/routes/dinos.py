import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/two-dinosaurs', methods=['POST'])
def dino():
    data = request.get_json()

    print("data sent for evaluation {}".format(data))

    n = data['number_of_types_of_food']
    A = data['calories_for_each_type_for_raphael']
    B = data['calories_for_each_type_for_leonardo']
    Q = data['maximum_difference_for_calories']

    dp1 = [0 for _ in range(400010)]
    dp2 = [0 for _ in range(400010)]
    temp = [0 for _ in range(400010)]

    dp1[0] = 1
    dp2[0] = 1
    temp[0] = 1

    mod = 100000123

    for i in range(len(A)):
        for j in range(400010):
            if dp1[j]:
                temp[j + A[i]] += dp1[j]
                if temp[j + A[i]] >= mod:
                    temp[j + A[i]] -= mod
        dp1, temp = temp, dp1

    temp = [0 for _ in range(400010)]
    temp[0] = 1
    for i in range(len(B)):
        for j in range(400010):
            if dp2[j]:
                temp[j + B[i]] += dp2[j]
                if temp[j + B[i]] >= mod:
                    temp[j + B[i]] -= mod
        dp2, temp = temp, dp2

    le = 0
    ri = Q
    su = 0
    for i in range(Q + 1):
        su += dp2[i]
        if su >= mod:
            su -= mod
    result = 0
    for i in range(400010):
        result += dp1[i] * su % mod
        if result >= mod:
            result -= mod
        if le < i + 1 - Q:
            su = (su - dp2[le] + mod) % mod
            le += 1
        if ri < 400000:
            su = (su + dp2[ri + 1]) % mod
            ri += 1

    print("My result :{}".format(result))
    return jsonify(result=result)

