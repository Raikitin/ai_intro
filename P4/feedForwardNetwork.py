import math
import random
import numpy as np
#import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from keras.datasets import mnist  # TODO loo up best way to load training data


class FeedForwardNetwork:
    def __init__(self, input, hidden, output, rate, data):
        self.input = input
        self.hidden = hidden
        self.output = output
        self.rate = rate
        self.data = data

        self.Wih = np.random.randn(self.input, self.hidden)  # input-hidden weight
        self.Who = np.random.randn(self.hidden, self.output)  # hidden-output weight

        (train_x, train_y), (self.test_x, self.test_y) = keras.datasets.mnist.load_data(path="mnist.npz")
        self.train_x = []
        self.train_y = []

        for i in range(self.data):
            self.train_x.append(self.image_convert(np.array(train_x[i], dtype=np.float64).flatten()))

            tmp = np.array([0.01 for i in range(self.output)], dtype=np.float64)
            tmp[train_y[i]] = 0.99
            self.train_y.append(tmp)

        self.train_x = np.array(self.train_x)
        self.train_y = np.array(self.train_y)

    def sigmoid(self, x):
        if(x < 0):
            return 1 / (1 + math.exp(x))
        return 1 / (1 + math.exp(-x))

    def sigmoid_derivative(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def think(self, input):
        hidden = np.dot(input, self.Wih)
        hidden = np.vectorize(self.sigmoid)(hidden)
        output = np.dot(hidden, self.Who)
        output = np.vectorize(self.sigmoid)(output)

        return output, hidden

    def train(self, iteration):
        for i in range(iteration):
            out, hidden = self.think(self.train_x)

            error_output = self.train_y - out

            error_hidden = np.dot(error_output, np.transpose(self.Who))

            #tmp = np.vectorize(self.sigmoid)(out)

            delta_who = np.dot(np.transpose(hidden), (error_output * np.vectorize(self.sigmoid)(out)))

            delta_wih = np.dot(np.transpose(self.train_x), (error_hidden * np.vectorize(self.sigmoid)(hidden)))

            self.Who = self.rate * delta_who
            self.Wih = self.rate * delta_wih

    #def eval(self)

    def image_convert(self, image):
        input = np.zeros(len(image), dtype=np.float64)
        factor = 0.99 / 254

        for i in range(len(image)):
            if (image[i] == np.uint8(0)):
                input[i] = 0.01
            else:
                input[i] = image[i] * factor
        return input

    def scorecard(self, it):
        fails = 0
        for i in range(it):
            input = self.image_convert(np.array(self.test_x[i]).flatten())
            o, h = self.think([input])
            if (np.argmax(o) != self.test_y[i]):
                fails += 1
        print("Iteration count: " + str(it) + ", Accuracy: " + str((it - fails) * 100 / it) + "%")


if __name__ == '__main__':
    number_input_nodes = 784
    number_hidden_nodes = 200
    number_output_nodes = 10
    training_samples = 800
    training_amount = 1000
    test_amount = 1000
    learning_rate = 0.2

    network = FeedForwardNetwork(number_input_nodes, number_hidden_nodes, number_output_nodes, learning_rate,
                                 training_samples)
    network.train(training_amount)
    # score
    network.scorecard(test_amount)
