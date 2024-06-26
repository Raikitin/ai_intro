import math
import random
import numpy as np


class Perceptron:
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.row = len(input)  # zeile
        self.col = len(input[0])  # spalte
        self.weights = np.array(
            [random.randint(-10, 10) for i in range(self.col)])  # changed synaptic_weights to weights

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def sigmoid_derivative(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def think(self, input):
        result = np.dot(input, self.weights)
        return self.sigmoid(result)

    def train(self, iterations):  # optimized inputs and targets out
        index = 0
        for iteration in range(iterations):
            for input in self.input:
                output = self.think(input)
                error = self.output[index] - output
                dx_sig = self.sigmoid_derivative(output)
                weight = np.dot(error * dx_sig, input)
                self.weights = np.add(self.weights, weight)
                index += 1
            index = 0
        print("Perceptron trained successfully")
        print("Trained Weights: ", self.weights)

    def eval(self):     # evaluation method
        test = np.zeros(self.col)
        while True:
            for i in range(self.col):
                test[i] = input("Input " + str(i + 1) + ": ")
            print("Output: ", self.think(test))

    def static_eval(self, test):
        print("Result of evalutating " + str(test))
        print("Output: ", self.think(test))

if __name__ == "__main__":
    node = Perceptron(
        np.array([[0, 0, 1],
                  [1, 1, 1],
                  [1, 0, 0],
                  [0, 1, 1]]),
        np.array([0, 1, 1, 0])
    )
    node.train(100000)

    test = [0, 1, 0]
    node.static_eval(test)

    node.eval()


