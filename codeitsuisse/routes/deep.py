import logging

import numpy as np
import tensorflow as tf
from sklearn.linear_model import LinearRegression

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/machine-learning/question-1', methods=['POST'])
def deep():
    data = request.get_json()

    print("data sent for evaluation {}".format(data))

    X = np.array(data['input'])
    y = np.array(data['output'])
    print(X)
    print(y)

    regr = LinearRegression()
    regr.fit(X, y)


    question = np.array([data['question']])
    predict = regr.predict(question)
    print(predict)

    print("My result :{}".format(predict[0]))

    return jsonify(answer=predict[0])


@app.route('/machine-learning/question-2', methods=['POST'])
def deeep():
    data = request.get_json()

    print("data sent for evaluation {}".format(data))

    model = tf.keras.models.load_model('my_model.h5')
    X = np.array(data['question']).reshape(-1, 28, 28)
    print(model.predict(X))
