import logging
from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)


def possiblePrimeArray(num):
    primes = []
    for possiblePrime in range(2, num+1):
    # Assume number is prime until shown it is not.
        isPrime = True
        for num in range(2, possiblePrime):
            if possiblePrime % num == 0:
                isPrime = False
        if isPrime:
            primes.append(possiblePrime)
    return primes

def addList(l):
    addition = 0
    for ele in l:
        addition += ele
    return addition


@app.route('/prime-sum', methods=['POST'])
def evaluatePrimeSum():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input");
    num = inputValue
    primes = possiblePrimeArray(num)
    result = []

    for prime in primes:
        if prime == num:
            ans = [prime]
            return jsonify(ans)
        else:
            i = 0
            temp = []
            temp.append(prime)
            while i < len(primes):
                if primes[i] != prime:
                    if addList(temp) == num:
                        return jsonify(temp)
                    elif (addList(temp) + primes[i])< num:
                        temp.append(primes[i])
                    else:
                        j = i-1
                        while j>=0:
                            if (addList(temp)+primes[i]) > num:
                                temp.remove(min(temp))
                            j-=1
                        temp.append(primes[i])
                i+=1


    logging.info("My result :{}".format(result))
    return jsonify(result);
