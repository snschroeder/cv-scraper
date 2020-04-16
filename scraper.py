import requests
import requests_html
import mongo_info
import dns
from pprint import pprint
from pymongo import MongoClient
import pymongo

client = MongoClient(mongo_info.connection_url)
db = client.admin

serverStat = db.command('serverStatus')

cdcChartUrl = 'https://www.cdc.gov/TemplatePackage/contrib/widgets/cdcCharts/iframe.html?chost=www.cdc.gov&cpath=/coronavirus/2019-ncov/cases-updates/cases-in-us.html&csearch=&chash=&ctitle=Cases%20in%20U.S.%20%7C%20CDC&wn=cdcCharts&wf=/TemplatePackage/contrib/widgets/cdcCharts/&wid=cdcCharts2&mMode=widget&mPage=&mChannel=&host=www.cdc.gov&displayMode=wcms&configUrl=/coronavirus/2019-ncov/cases-updates/total-cases-onset.json&class=mb-3'
finder = '#cdc-chart-1-data'

def scrape_data(url, finder):
    session = requests_html.HTMLSession()
    r = session.get(url)
    r.html.render()
    chart = r.html.find(finder, first=True)
    return chart.text

def process_data(data):
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

def initialize_db(url):
    client = MongoClient(url)
    db = client.covid

    dirtyData = scrape_data(cdcChartUrl, finder)
    day, infected = process_data(dirtyData)

    for ind, val in enumerate(day):
        dailyData = {
            'day': val,
            'infected': infected[ind]
        }
        pprint(dailyData)
        result = db.daily.insert_one(dailyData)
        print('Created as {0}'.format(result.inserted_id))


def update_db(db_url, cdc_url, finder):
    dirty_data = scrape_data(cdc_url, finder)
    day, infected = process_data(dirty_data)

    client = MongoClient(db_url)
    db = client.covid
    latest = db.daily.find_one({}, sort=[("_id", -1)])

    db_day = latest['day']
    ind = day.index(db_day)

    for i in range(ind + 1, len(day)):
        daily_data = {
            'day': day[i],
            'infected': infected[i]
        }
        result = db.daily.insert_one(daily_data)
        print('Created as {0}'.format(result.inserted_id))

    

# initialize_db(mongoInfo.connectionUrl)

update_db(mongo_info.connection_url, cdcChartUrl, finder)
