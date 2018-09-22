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
            if len(expense['exclude']) == n:
                continue

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
                break

            if p[1] > (-1)*minus[i][1]:
                p[1] += minus[i][1]
                #print("send ", minus[i][0], "from", p[0], "to", minus[i][0])
                transactions.append({
                    "from": p[0],
                    "to": minus[i][0],
                    "amount": "%.2f" % round((-1)*minus[i][1], 2)
                })
                minus[i][1] = 0
                i += 1

            elif p[1] < (-1)*minus[i][1]:
                minus[i][1] += p[1]
                #print("send ", p[1], "from", p[0], "to", minus[i][0])
                transactions.append({
                    "from": p[0],
                    "to": minus[i][0],
                    "amount": "%.2f" % round(p[1]/100, 2)
                })
                p[1] = 0

            else:
                #print("send ", p[1], "from", p[0], "to", minus[i][0])
                transactions.append({
                    "from": p[0],
                    "to": minus[i][0],
                    "amount": "%.2f" % round(p[1]/100, 2)
                })
                p[1] = 0
                minus[i][1] = 0
                i += 1

    print("My result :{}".format(transactions))
    return jsonify(transactions=transactions)



