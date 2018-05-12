from math import exp

# scraping 2008 to 21-10-2017 : 10276.784128546002

def sigmoid(t):
    return 1/(1+exp(-t))

def Id(t):
    return t

def perceptron(X, A, f):
    s=0
    for i in range(len(X)):
        s+=X[i]*A[i]
    return f(s)

network = [
    [([1,-1,1,1],sigmoid), # bias and fonction of neuron1
     ([-1,2,1,-2],sigmoid) # bias and fonction of neuron2
    ] #layer2
    # ...
]

test_net = [
    [([0.35,0.15,0.20],sigmoid),
     ([0.35,0.25,0.30],sigmoid)],
    [([0.60,0.40,0.45],sigmoid),
     ([0.60,0.50,0.55],sigmoid)],
    [([0.85,0.65,0.70],sigmoid),
     ([0.85,0.75,0.80],sigmoid)]
]

f=2

def forward(X, network):
    # list to keep track of the activation of each neuron
    V = [[1]+X]
    # for each layer
    for l in range(len(network)):
        V.append([1])
        # for each neuron in the layer l
        for j in range(len(network[l])):
            V[l+1].append(perceptron(V[l], network[l][j][0], network[l][j][1]))
    return V

# f is the number of neuron in the last layer
def backprop(aSet, network, f, alpha):
    dataset = aSet[:]
    # array of cumulated dC/dw
    D = [[[0 for _ in range(len(network[l][i][0]))] for i in range(len(network[l]))] for l in range(len(network))]
    for x in dataset:
        y = []
        for i in range(f):
            y.append(x.pop())
        # Forward propagation gives the list of activations by layer
        A = forward(x, network)
        d = [[]]
        # dC/dz for the last layer
        for i in range(f):
            d[0].append((A[-1][-f+i]-y[i-1]) * A[-1][-f+i] * (1-A[-1][-f+i]))

        # dC/dz for all other layers
        # for each layer going backward
        for l in range(1, len(network)):
            d.append([])
            #for each neuron in the layer L-l-1
            for i in range(0, len(network[-l-1])):
                s = 0
                for k in range(1,len(network[-l-1][i][0])):
                    s += d[-l-1][k-1]*network[-l][k-1][0][i+1]

                d[l].append(s*A[-l-1][i+1]*(1-A[-l-1][i+1]))

        # dC/dw for each weight
        for l in range(len(D)):
            for k in range(len(D[l])):
                for j in range(len(D[l][k])):
                    D[l][k][j] += d[-l-1][k]*A[l][j] /len(dataset)

    for l in range(len(network)):
        for k in range(len(network[l])):
            for j in range(len(network[l][k][0])):
                network[l][k][0][j] -= alpha*D[l][k][j]


def get_data():
    return

# the last element of the dataset should be the expected result
for _ in range(500):
    test_set = [[0.05,0.10,0.01,0.99] for _ in range(100)]
    backprop(test_set, test_net, f, 0.5)

print(forward(test_set[0][:2], test_net))
