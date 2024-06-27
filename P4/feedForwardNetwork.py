import math
import random
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist    # TODO loo up best way to load training data

class FeedForwardNetwork:
    def __init__(self, input, hidden, output, rate, data):
        self.input = input
        self.hidden = hidden
        self.output = output
        self.rate = rate
        self.data = data

        self.Wih = np.random.randn(self.input, self.hidden)     # input-hidden weight
        self.Who = np.random.randn(self.hidden, self.output)    # hidden-output weight

        (train_x, train_y), (self.test_x, self.test_y) = mnist.load_data()
        self.train_x = []
        self.train_y = []

        for i in range(self.data):
            self.train_x.append(self) # TODO image conversion in self

            tmp = np.array([0.01 for i in range(self.output)], dtype=float)
            tmp[train_y[i]] = 0.99
            self.train_y.append(tmp)

        self.train_x = np.array(self.train_x)
        self.train_y = np.array(self.train_y)

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def sigmoid_derivative(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def think(self, input):
        hidden = np.dot(input, self.Wih)
        hidden = np.vectorize(self.sigmoid)(hidden)
        output = np.dot(hidden, self.Who)
        output = np.vectorize(self.sigmoid)(output)

        return output, hidden


    #def train(self, iteration):
    #    for i in range(iteration):



    #def eval(self)

    #def scorecard(self)

#if __name__ == '__main__':