from django.shortcuts import render

from django.http import HttpResponse
from datetime import datetime
import pytz

import requests
from bs4 import BeautifulSoup
import operator

def hello_world(request):
    return render(request, 'hello_world.html', {
        'current_time': str(datetime.now(pytz.timezone('Asia/Taipei'))),
    })

def frequency(self):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    res = requests.get("http://www.taiwanlottery.com.tw/Info/number/frequency.aspx?GAME=SL638", headers=headers).text
    soup = BeautifulSoup(res, 'html.parser')
    
    numberTagArray = soup.find_all('strong')
    countTagArray = soup.find_all('td', {'class': ['tdA_1', 'tdA_2']})

    numberArray = []
    countArray = []
    number2Array = []
    count2Array = []

    for key in range(len(numberTagArray)):
        if (key + 1) % 4 == 0 and (key + 1) <= 32:
            number2Array.append(numberTagArray[key].text)
        else:
            numberArray.append(numberTagArray[key].text)

    for key in range(len(countTagArray)):
        if (key + 1) % 4 == 0 and (key + 1) <= 32:
            count2Array.append(countTagArray[key].text)
        else:
            countArray.append(countTagArray[key].text)

    firstList = {}
    for number, count in zip(numberArray, countArray):
        firstList[number] = count

    secondList = {}
    for number, count in zip(number2Array, count2Array):
        secondList[number] = count
    
    firstList = sorted(firstList.items(), key=operator.itemgetter(1), reverse=True)
    secondList = sorted(secondList.items(), key=operator.itemgetter(1), reverse=True)

    return render(self, 'frequency.html', {
        'firstList': firstList,
        'secondList': secondList,
    })