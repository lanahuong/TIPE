#!/usr/bin/env python3

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as pyplot
import csv

Tk()

class DataPlot(Frame):

    def __init__(self, master=None):
        self.currentFile = ""
        self.xLabel = ""
        self.yLabel = ""
        self.headers = []

        Frame.__init__(self,master)
        self.pack()

        self.chooseFileView()

    def chooseFile(self):
        fileName = askopenfilename()
        self.chosenFileText.set(fileName)

    def clearView(self):
        for w in self.grid_slaves():
            w.grid_remove()
        print(self.grid_slaves())

    def get_headers(self):
        with open(self.currentFile, 'r') as dataFile:
            reader = csv.reader(dataFile, delimiter=' ', quotechar='|')
            self.headers = next(reader)[0].split(',')

    def chooseFileView(self):
        self.clearView()

        self.chosenFileText = StringVar()
        self.chosenFileText.set("No file")
        self.chooseFileLabel = Label(self, text="Choose the file containing your data").grid(row=0, column=0)
        self.chosenFileLabel = Label(self, textvariable=self.chosenFileText).grid(row=1, column=1)
        self.chooseFileButton = Button(self, text="Choose file", command=self.chooseFile).grid(row=1, column=2)
        self.okButton = Button(self, text="Next", command=self.dataView).grid(row=2, column=2)


    def dataView(self):
        self.currentFile = self.chosenFileText.get()
        self.clearView()

        self.get_headers()
        print(self.headers)

        self.abcissaLabel = Label(self, text="Abcissa").grid(row=0, column=0)
        self.abcissaChoice = Combobox(self, values=self.headers).grid(row=0, column=1)
        self.ordinateLabel = Label(self, text="Ordinate").grid(row=1, column=0)
        self.ordinateChoice = Combobox(self, values=self.headers).grid(row=1, column=1)
        self.plotButton = Button(self, text="Plot", command=self.plot).grid(row=2, column=2)

    def plot(self):
        w = self.grid_slaves(column=1)

        self.xLabel = self.headers[w[1].current()]
        self.yLabel = self.headers[w[0].current()]
        print(self.xLabel, self.yLabel)
        X = []
        Y = []
        with open(self.currentFile, 'r') as dataFile:
            reader = csv.DictReader(dataFile)
            for row in reader:
                print(row['date'])
                if row[self.xLabel] != 'N/A' and row[self.yLabel] != 'N/A':
                    X.append(float(row[self.xLabel]))
                    Y.append(float(row[self.yLabel]))

        pyplot.autoscale(enable=True, axis='both', tight=None)
        pyplot.scatter(X,Y)
        pyplot.show()

        return

app = DataPlot()
app.master.title('Data Plot')
app.mainloop()
