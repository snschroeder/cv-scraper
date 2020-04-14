import requests
import requests_html
import mongoInfo
import dns
from pprint import pprint
from pymongo import MongoClient

client = MongoClient(mongoInfo.connectionUrl)
db = client.admin

print(db)

serverStat = db.command('serverStatus')
pprint(serverStat)

cdcChartUrl = 'https://www.cdc.gov/TemplatePackage/contrib/widgets/cdcCharts/iframe.html?chost=www.cdc.gov&cpath=/coronavirus/2019-ncov/cases-updates/cases-in-us.html&csearch=&chash=&ctitle=Cases%20in%20U.S.%20%7C%20CDC&wn=cdcCharts&wf=/TemplatePackage/contrib/widgets/cdcCharts/&wid=cdcCharts2&mMode=widget&mPage=&mChannel=&host=www.cdc.gov&displayMode=wcms&configUrl=/coronavirus/2019-ncov/cases-updates/total-cases-onset.json&class=mb-3'
finder = '#cdc-chart-1-data'

def fetchData(url, finder):
    session = requests_html.HTMLSession()
    r = session.get(url)
    r.html.render()
    chart = r.html.find(finder, first=True)
    pprint(chart.text)
    return chart
