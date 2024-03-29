## This script is based on https://deeplearningbook.com.br ##

import numpy as np
import random
from util import *

class Network(object):

    def __init__(self, sizes: list):
        """ This step is a class init where "sizes" is a list with the number of
        neurons in the respective layers. The bias and weights are initialized
        randomly"""
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.radn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.radn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

    def feedForward(self, a):
        ## Returns the network output if 'a' is input.
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data = None):
        ## Train the neural network using mini-batch stochastic gradient descent
        training_data = list(training_data)
        n = len(training_data)

        if test_data:
            test_data = list(test_data)
            n_test = len(test_data)
        
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[k:k + mini_batch_size] for k in range(0, n, mini_batch_size)]

            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            
            if test_data:
                print(f"Epoch {j} : {self.evaluate(test_data)} / {n_test}")
            else:
                print(f"Epoch {j} finalizada")
    
    def update_mini_batch(self, mini_batch, eta):
        """ Updates the network weights and bias by applying gradient descent
        using backing propagation for a single mini batch. The 'mini_batch' is 
        a list of tuples, and 'eta' is the learning rate"""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        
        self.weights = [w - (eta / len(mini_batch)) * nw for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - (eta / len(mini_batch)) * nb for b, nb in zip(self.biases, nabla_b)]
    
    def backprop(self, x, y):
        """ Returns a tuple '(nabla_b, nabla_w)' that represents the gradient
        for the cost function C_x."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        ## FeedForward
        activation = x

        ## List to store all activations, layer by layer
        activations = [x]

        ## List to store all z vectors', layer by layer
        zs = []

        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)

        ## Backward pass
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())

        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        
        return (nabla_b, nabla_w)
    
    def evaluate(self, test_data):
        ## Returns the input data that was predicted correctly
        test_results = [(np.argmax(self.feedForward(x)), y) for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)
    
    def cost_derivative(self, output_activations, y):
        ## Return the partial derivatives vector
        return (output_activations - y)
