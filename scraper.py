import requests
import requests_html
import mongoInfo
import dns
from pprint import pprint
from pymongo import MongoClient

client = MongoClient(mongoInfo.connectionUrl)
db = client.admin

serverStat = db.command('serverStatus')
pprint(serverStat)

cdcChartUrl = 'https://www.cdc.gov/TemplatePackage/contrib/widgets/cdcCharts/iframe.html?chost=www.cdc.gov&cpath=/coronavirus/2019-ncov/cases-updates/cases-in-us.html&csearch=&chash=&ctitle=Cases%20in%20U.S.%20%7C%20CDC&wn=cdcCharts&wf=/TemplatePackage/contrib/widgets/cdcCharts/&wid=cdcCharts2&mMode=widget&mPage=&mChannel=&host=www.cdc.gov&displayMode=wcms&configUrl=/coronavirus/2019-ncov/cases-updates/total-cases-onset.json&class=mb-3'
finder = '#cdc-chart-1-data'

def fetchData(url, finder):
    session = requests_html.HTMLSession()
    r = session.get(url)
    r.html.render()
    chart = r.html.find(finder, first=True)
    return chart.text

dataset = fetchData(cdcChartUrl, finder)

def processData(data):
    arr = data.split('\n')
    arr.pop(0)
    date = []
    infected = []

    for val in arr:
        if '/' in val:
            date.append(val)
        elif val[0] != 'T':
            infected.append(val)

    return date, infected

def initializeDB(url):
    client = MongoClient(url)
    db = client.covid

    dirtyData = fetchData(cdcChartUrl, finder)
    day, infected = processData(dirtyData)

    for ind, val in enumerate(day):
        dailyData = {
            'day': val,
            'infected': infected[ind]
        }
        pprint(dailyData)
        result = db.daily.insert_one(dailyData)
        print('Created as {0}'.format(result.inserted_id))

initializeDB(mongoInfo.connectionUrl)
