import math
import random
import numpy as np

class Perceptron:
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.N = len(input)
        self.M = len(input[0])
        self.weights = np.array([random.randint(-10, 10) for i in range(self.M)])

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def sigmoid_derivative(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def think(self, inputs):
        result = np.dot(input, self.weights)
        return self.sigmoid(result)

    #def train(self, inputs, targets, iterations):

    #def eval(self):
        

if __name__ == "__main__":
    obj = Perceptron(
        np.array([[0, 0, 1],
                     [1, 1, 1],
                     [1, 0, 0],
                     [0, 1, 1]]),
        np.array([0, 1, 1, 0])
    )
    # training
    # eval
