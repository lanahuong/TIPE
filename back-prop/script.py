import csv
from datetime import datetime, date, timedelta

# 94730 lines -> 94729

headers = []
data = []
pollutionFile = 'data/pm_2007_21-10-2017.csv'

i = 0
for k in range(2007, 2018):
    currentFile = 'data/weather_'+str(k)+'.csv'
    with open(currentFile, 'r') as readFile:
        reader = csv.reader(readFile, delimiter=',', quotechar='|')
        headers = next(reader)
        for row in reader:
            data.append(row)

with open(pollutionFile, 'r') as readFile:
    reader = csv.DictReader(readFile, delimiter=';')
    next(reader)

    for row in reader:
        if i<len(data):
            time_d, time_h = row['date'].split('/'), row['heure']
            time_d = datetime(int(time_d[2]), int(time_d[1]), int(time_d[0]))
            if time_h == '24' :
                dt = timedelta(1)
                time_d = time_d+dt
                time_h = '0'

            pollutionDate = time_d
            w_date = data[i][0].split('/')
            weatherDate = datetime(int(w_date[2]), int(w_date[1]), int(w_date[0]))

            while time_h != data[i][1]:
                i += 1

            if len(data[i]) != 8 :
                for l in range(8-len(data[i])):
                    data[i].append('N/A')

            if pollutionDate == weatherDate and time_h == data[i][1]:
                if row['PA18'] == 'n/d':
                    data[i].append('N/A')
                else:
                    data[i].append(row['PA18'])
            i+=1

headers.append('pm10_PA18')

with open('data/weather_2007-2017.csv', 'w') as writeFile:
    writer = csv.writer(writeFile, delimiter=',')
    writer.writerow(headers)
    for row in data:
        writer.writerow(row)
