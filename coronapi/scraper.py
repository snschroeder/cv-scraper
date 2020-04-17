import requests
import requests_html
from pprint import pprint

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
