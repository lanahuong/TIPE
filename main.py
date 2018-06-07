from math import exp
from BackProp.NeuralNetwork import *
import csv
import datetime
import random

def is_usable(x):
    n = 'N/A'
    return (x[5]!=n) and (x[6]!=n) and (x[7]!=n) and (x[8]!=n) and (x[9]!=n) and (x[10]!=n)


def get_sets():

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

    learningSet = []
    testingSet = []

    for i in range(2,len(dataSet)):
        if is_usable(dataSet[i-1]) and is_usable(dataSet[i]):
            if int(dataSet[i][0]) <= 2015 and int(dataSet[i][0]) >= 2013:
                learningSet.append([float(k) for k in dataSet[i][:10]]+[float(k) for k in dataSet[i-1][5:]]+[float(dataSet[i][10])])
            elif int(dataSet[i][0]) > 2015:
                testingSet.append([float(k) for k in dataSet[i][:10]]+[float(k) for k in dataSet[i-1][5:]]+[float(dataSet[i][10])])

    learningSet = random.sample(learningSet, k=len(learningSet))

    # make the batches
    learning_batches = []
    batch = []
    for i in range(len(learningSet)):
        batch.append(list(learningSet[i]))
        if i%20 == 0 and i!=0:
            learning_batches.append(batch)
            batch = []

    learning_batches.append(batch)
    return learning_batches, testingSet

# make the network, learn and test
learning_batches, testingSet = get_sets()
def learn():
    description = [(256,17,sigmoid), (16,257,RELu), (8,17, RELu), (1,9,RELu)]
    network = NeuralNetwork(description, 0.01, 0.999)
    network.learn_mini_batches(list(learning_batches))
    network.test_with_set(list(testingSet))
    return network

network = learn()
