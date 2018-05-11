#! /usr/bin/env python3

# WEATHER UNDERGROUND
# use station : Paris-centre, Paris[I75003PA1]
# no access to history with api need to contact or scrape
# https://www.wunderground.com/personal-weather-station/dashboard?ID=I75003PA1#history/tdata/s20071030/e20071030/mdaily

# METEOCIEL
# tipical adress for Paris-Monsouris
# http://www.meteociel.fr/temps-reel/obs_villes.php?code2=7156&jour2=30&mois2=9&annee2=2007&envoyer=OK

from bs4 import BeautifulSoup
import requests
import csv
import time
from datetime import date, datetime, timedelta

def fixdata(data):
    if [] in data:
        newdata=[]
        i=0
        while data[i]!=[]:
            if data[i][0]==str(23-len(newdata))+' h':
                newdata.append(data[i])
                i+=1
            else:
                newdata.append([str(23-len(newdata))]+['N/A' for _ in range(10)])

        return newdata
    return data

class WeatherScraper():
    base_url = "http://www.meteociel.fr/temps-reel/obs_villes.php?code2=7156"

    def getdata(self,d,m,y):
        url = self.base_url + '&jour2=' + str(d) + '&mois2=' + str(m) + '&annee2=' + str(y) + '&envoyer=OK'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')
        table = soup.find('td', class_='Style1').find_all('center')[4].find_all('table')[1].tbody
        data=[[] for _ in range(24)]
        lines = table.find_all('tr')
        lines.pop(0)
        for i in range(len(lines)):
            line = lines[i].select('td')
            for j in range(len(line)):
                if line[j].get_text()!=[]:
                    data[i].append(line[j].get_text())
        return fixdata(data)

    def gethead(self,d,m,y):
        url = self.base_url + '&jour2=' + str(d) + '&mois2=' + str(m) + '&annee2=' + str(y) + '&envoyer=OK'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')
        table = soup.find('td', class_='Style1').find_all('center')[4].find_all('table')[1].tbody
        headers =[]
        for td in table.tr.select('td') :
            headers.append(td.get_text())

        return headers

def treatheaders(headers):
    headers.pop(1)
    headers.pop(1)
    headers.pop(1)
    headers.pop(3)
    headers[4]=headers[4].split()[0]
    headers[-1]=headers[-1].split()[0]
    #return headers

def treatdata(data):
    for i in range(len(data)):
        #pop useless data
        data[i].pop(8)
        data[i].pop(1)
        data[i].pop(1)
        data[i].pop(1)
        data[i].pop(3)

        #remove units
        data[i][0]=data[i][0].strip(' h')
        data[i][1]=data[i][1].strip(' °C')
        data[i][3]=data[i][3].strip(' °C')
        data[i][2]=data[i][2].strip('% ')
        data[i][4]=data[i][4].split('(')[0].strip(' km/h ')
        data[i][5]=data[i][5].strip(' hPa')

        #handle precipitation
        if data[i][-1]==' aucune':
            data[i][-1] = '0'
        else:
            data[i][-1]=data[i][-1].strip(' mm')

    #return data

def makecsv(headers,y):
    with open('weather_'+str(y)+'.csv', 'w', newline='') as f:
        weatherwriter = csv.writer(f)
        weatherwriter.writerow(['date']+headers)

def addtocsv(data,d,m,y):
    #date = str(d)+'/'+str(m)+'/'+str(y)
    with open('weather_'+str(y)+'.csv', 'a', newline='')as f:
        date = [str(d)+'/'+str(m)+'/'+str(y)]
        weatherwriter = csv.writer(f)
        n=len(data)-1
        for i in range(len(data)):
            weatherwriter.writerow(date+data[n-i])

"""
#Tests

spider = WeatherScraper()
headers, data = spider.gethead(7,0,2007), spider.getdata(7,0,2007)
treatheaders(headers)
fixdata(data)
print(data)
treatdata(data)
makecsv(headers)
addtocsv(data,7,0,2007)
"""

def scrape(sy,sm,sd,delay,end):
    spider = WeatherScraper()
    day = date(sy,sm,sd)
    headers = spider.gethead(day.day,day.month-1,day.year)
    treatheaders(headers)
    makecsv(headers,sy)
    one = timedelta(days=1)

    while (day.year,day.month,day.day)!=end:
        data = spider.getdata(day.day,day.month-1,day.year)
        fixdata(data)
        treatdata(data)
        addtocsv(data,day.day,day.month,day.year)
        day=day+one
        time.sleep(delay)

start = time.perf_counter()
scrape(2008,1,1,1,(2008,12,31))
scrape(2009,1,1,1,(2009,12,31))
scrape(2010,1,1,1,(2010,12,31))
scrape(2011,1,1,1,(2011,12,31))
scrape(2012,1,1,1,(2012,12,31))
scrape(2013,1,1,1,(2013,12,31))
scrape(2014,1,1,1,(2014,12,31))
scrape(2015,1,1,1,(2015,12,31))
scrape(2016,1,1,1,(2016,12,31))
scrape(2017,1,1,1,(2017,10,21))
print(time.perf_counter()-start)

