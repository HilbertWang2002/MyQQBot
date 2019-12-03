# -*- coding:gbk -*-
from splinter import Browser
def fun(fromStation,toStation,y,m,d):
    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome',**executable_path)
    
    fromStation = fromStation+','+get_city(fromStation)
    toStation = toStation+','+get_city(toStation)

    browser.visit(f'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={fromStation}&ts={toStation}&date={y}-{m}-{d}&flag=N,N,Y')
    ticketTable = browser.find_by_id('queryLeftTable')
    ticketList = ticketTable.first.find_by_tag('tr')
    msgs = []
    for i in range(0,int(len(ticketList)/2)):
        temp = ticketList[i*2].find_by_tag('td').first.find_by_tag('div').first
        msgs[i].append(temp.find_by_tag('div').first.find_by_tag('div').first.find_by_tag('a').first.value)
        msgs[i].append(temp.find_by_tag('div')[2].find_by_tag('strong')[0].value+'到'+temp.find_by_tag('div')[2].find_by_tag('strong')[1].value)
        msgs[i].append(temp.find_by_tag('div')[3].find_by_tag('strong')[0].value+'到'+temp.find_by_tag('div')[3].find_by_tag('strong')[1].value)
    browser.quit
    return msgs   

def get_city(city):
    with open('./plugins/ticket/city.txt','r') as code:
        bytes = code.read()
        lists = bytes.split('@')
        a = 0
        cities = []
        for i in lists:
            cities.append(i.split('|'))
            a+=1
    cities.pop(0)
    for i in cities:
        if i[1] == city:
            return i[2]