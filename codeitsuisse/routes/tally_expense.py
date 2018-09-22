import logging
from flask import request, jsonify
from codeitsuisse import app
from collections import defaultdict


@app.route('/tally-expense', methods=['POST'])
def tally_expense():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    persons = data.get("persons")
    expenses = data.get("expenses")
    n = len(persons)

    ledger = defaultdict(float)
    for expense in expenses:
        print(expense)
        ledger[expense['paidBy']] += expense['amount']
        if 'exclude' in expense:
            new_persons = [p for p in persons if p not in expense['exclude']]
            per_head = expense['amount']/(n-len(expense['exclude']))
            for p in new_persons:
                ledger[p] -= per_head
                print(p, ledger[p])
        else:
            for p in persons:
                ledger[p] -= expense['amount']/n
                print(p, ledger[p])

    plus = []
    minus = []
    for k, v in ledger.items():
        if v < 0:
            minus.append([k, v])
        else:
            plus.append([k, v])

    print('plus', plus)
    print('minus', minus)

    transactions = []
    i = 0
    for p in plus:
        while p[1] > 0:
            if i >= len(minus):
                print(plus)
                print(minus)
                break

            if p[1] >= (-1)*minus[i][1]:
                p[1] += minus[i][1]
                print("send ", "%.2f" % round((-1)*minus[i][1], 2), "from", minus[i][0], "to", p[0])
                transactions.append({
                    "from": minus[i][0],
                    "to": p[0],
                    "amount": float("%.2f" % round((-1)*minus[i][1], 2))
                })
                minus[i][1] = 0
                i += 1

            else:
                minus[i][1] += p[1]
                print("send ", "%.2f" % round(p[1]/100, 2), "from", minus[i][0], "to", p[0])
                transactions.append({
                    "from": minus[i][0],x
                    "to": p[0],
                    "amount": float("%.2f" % round(p[1], 2))
                })
                p[1] = 0

    print("My result :{}".format(transactions))
    return jsonify(transactions=transactions)



