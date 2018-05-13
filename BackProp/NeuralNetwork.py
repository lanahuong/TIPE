
# -------------------------------
# ----- NeuralNetwork class -----
# -------------------------------


from math import exp
from BackProp.Perceptron import *

def sigmoid(t):
    return 1/(1+exp(-t))

def Id(t):
    return t

class NeuralNetwork:
    def __init__(self, description, alpha=0.5, beta=0.99):
        # description = [(number_of_neuron, number_of_weights, function), (...)]
        # len(description) = number of layers
        self.network = [[perceptron(layer[1], layer[2]) for _ in range(layer[0])] for layer in description]
        self.alpha = alpha
        self.beta = beta
        self.f = description[-1][0]

    def forward(self, X):
        # list to keep track of the activation of each neuron
        V = [[1]+X]
        # for each layer
        for l in range(len(self.network)):
            V.append([1])
            # for each neuron in the layer l
            for p in self.network[l]:
                V[l+1].append(p.evaluate(V[l]))
        return V

    def backprop(self, aSet, prevD):
        dataset = aSet[:]
        # D is the array of cumulated dC/dw
        D = [[[0 for _ in p.coeff]
              for p in layer]
             for layer in self.network]

        for x in dataset:
            y = []
            for i in range(self.f):
                y.append(x.pop())
            # Forward propagation gives the list of activations by layer
            A = self.forward(x)
            # d contains dC/dz by layer
            d = [[]]
            # dC/dz for the last layer
            for i in range(self.f):
                if self.network[-1][i].func == sigmoid :
                    d[0].append((A[-1][-self.f+i]-y[i-1]) * A[-1][-self.f+i] * (1-A[-1][-self.f+i]))
                elif self.network[-1][i].func == Id :
                    d[0].append(A[-1][-self.f+i]-y[i-1])

            # dC/dz for all other layers
            # for each layer going backward
            for l in range(1, len(self.network)):
                d.append([])
                #for each neuron in the layer L-l-1
                for i in range(0, len(self.network[-l-1])):
                    s = 0
                    for k in range(1,len(self.network[-l-1][i].coeff)):
                        s += d[-l-1][k-1]*self.network[-l][k-1].coeff[i+1]

                    d[l].append(s*A[-l-1][i+1]*(1-A[-l-1][i+1]))

            # dC/dw for each weight
            for l in range(len(D)):
                for k in range(len(D[l])):
                    for j in range(len(D[l][k])):
                        D[l][k][j] += d[-l-1][k]*A[l][j] /len(dataset)

        for l in range(len(self.network)):
            for k in range(len(self.network[l])):
                for j in range(len(self.network[l][k].coeff)):
                    self.network[l][k].coeff[j] -= self.alpha*(D[l][k][j] + self.beta*prevD[l][k][j])
                    prevD[l][k][j] = D[l][k][j]


    # the last element of the dataset should be the expected result
    def learn_mini_batches(self, batches):
        prevD = [[[0 for _ in p.coeff] for p in layer] for layer in self.network]
        for b in batches:
            self.backprop(b, prevD)


# test : 500 batches of 100 identical exemples
test_batches = [[[0.05,0.10,0.01,0.99] for _ in range(100)] for _ in range(500)]

# creating the test network : 3 layers of 2 neurons with 3 weights
description = [(2,3,sigmoid) for _ in range(3)]
test_neural_net = NeuralNetwork(description, 0.5, 0.99)
test_neural_net.learn_mini_batches(test_batches)
