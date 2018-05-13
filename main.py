from math import exp
from BackProp.NeuralNetwork import *

def sigmoid(t):
    return 1/(1+exp(-t))

def Id(t):
    return t

