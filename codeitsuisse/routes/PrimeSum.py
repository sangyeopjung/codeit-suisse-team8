import logging
from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)


# def possiblePrimeArray(num):
#     primes = []
#     for possiblePrime in range(2, num+1):
#     # Assume number is prime until shown it is not.
#         isPrime = True
#         for num in range(2, possiblePrime):
#             if possiblePrime % num == 0:
#                 isPrime = False
#         if isPrime:
#             primes.append(possiblePrime)
#     return primes
#
# def addList(l):
#     addition = 0
#     for ele in l:
#         addition += ele
#     return addition
import math, numpy


def generateJs(i,n):
    j=i**2
    if j<n:
        yield j

    while j+i<=n:
        j+=i
        yield j


def SieveOptimized(n):
    l = list(range(2, n+1))
    isPrime = [True] * (n+1)
    maxChk = math.sqrt(n)

    for q,r in enumerate(l):
        if r>maxChk:
            break

        for z in generateJs(r,n):
           isPrime[z] = False

    return numpy.where(isPrime)[0]



@app.route('/prime-sum', methods=['POST'])
def evaluatePrimeSum():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    input = data.get("input")

    print(input)
    primes = SieveOptimized(input + 10)[2:]

    num = len(primes)
    found = 0
    result = []

    if input in primes:
        result.append(input)

    else:
        if input % 2 == 1:
            input -= 3
            result.append(3)

        for i in range(num):
            for j in range(i + 1, num):
                if primes[i] + primes[j] == input:
                    result.extend([primes[i], primes[j]])
                    found = 1
                    break
            if found:
                break

    result = list(map(int, result))
    logging.info("My result :{}".format(result))
    return jsonify(result)
