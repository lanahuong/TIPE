from math import exp
from BackProp.NeuralNetwork import *
import csv
import datetime

#def sigmoid(t):
#    return 1/(1+exp(-t))

#def Id(t):
#    return t

datafile = 'data/weather_2007-2017.csv'

# get data
dataSet = []
with open(datafile, 'r') as readFile:
    reader = csv.DictReader(readFile, delimiter=',')
    for row in reader:
        date = row['date'].split('/')
        date = datetime.datetime(int(date[2]),int(date[1]),int(date[0]))
        d = []
        d.append(date.year)
        d.append(date.month)
        d.append(date.timetuple().tm_yday)
        d.append(date.weekday())
        d.append(row['Heurelocale'])
        d.append(row['Température'])
        d.append(row['Vent'])
        d.append(row['Précip.'])
        d.append(row['Humidité'])
        d.append(row['Pression'])
        d.append(row['pm10_PA18'])
        dataSet.append(d)

# sort usable data
def is_usable(x):
    n = 'N/A'
    return (x[5]!=n) and (x[6]!=n) and (x[7]!=n) and (x[8]!=n) and (x[9]!=n) and (x[10]!=n)

learningSet = []
testingSet = []

for i in range(1,len(dataSet)):
    if is_usable(dataSet[i-1]) and is_usable(dataSet[i]):
        if int(dataSet[i][0]) <= 2008:
            learningSet.append([float(k) for k in dataSet[i][:10]]+[float(k) for k in dataSet[i-1][5:]]+[float(dataSet[i][10])])
        else:
            testingSet.append([float(k) for k in dataSet[i][:10]]+[float(k) for k in dataSet[i-1][5:]]+[float(dataSet[i][10])])

# make the batches
learning_batches = []
batch = []
for i in range(len(learningSet)):
    batch.append(learningSet[i])
    if i%10 == 0 and i!=0:
        learning_batches.append(batch)
        batch = []

learning_batches.append(batch)

# make the network, learn and test
description = [(16,17,sigmoid),(16,17,sigmoid),(16,17,sigmoid),(1,17,Id)]
network = NeuralNetwork(description, 0.003, 0.999)
network.learn_mini_batches(learning_batches)
print(network.test_with_set(testingSet))
