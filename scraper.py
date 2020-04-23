import requests
import requests_html
from pprint import pprint

# old link and key finder - no longer getting updated
cdcChartUrl = 'https://www.cdc.gov/TemplatePackage/contrib/widgets/cdcCharts/iframe.html?chost=www.cdc.gov&cpath=/coronavirus/2019-ncov/cases-updates/cases-in-us.html&csearch=&chash=&ctitle=Cases%20in%20U.S.%20%7C%20CDC&wn=cdcCharts&wf=/TemplatePackage/contrib/widgets/cdcCharts/&wid=cdcCharts2&mMode=widget&mPage=&mChannel=&host=www.cdc.gov&displayMode=wcms&configUrl=/coronavirus/2019-ncov/cases-updates/total-cases-onset.json&class=mb-3'
finder = '#cdc-chart-1-data'

# new data source, use this moving forward
json_data = 'https://www.cdc.gov/coronavirus/2019-ncov/json/cumm-total-chart-data.json'

def scrape_json(url):
    session = requests_html.HTMLSession()
    r = session.get(url)
    return r.text

def process_json(data):
    date = []
    infected = []

    filtered_data = data.replace('\r\n', '')
    filtered_data = filtered_data.replace(' ', '')
    filtered_data = filtered_data.replace('"', '')

    data_arr = filtered_data.split(',')
    data_arr = data_arr[1:]

    for val in data_arr:
        if '/' in val:
            if len(val) == 9:
                date.append('0' + val)
            else:
                date.append(val)
        elif val[0] != 'd':
            infected.append(val)

    return date, infected[1:]

# Original url I was scrapping stopped getting update, do not use this method
def scrape_data(url, finder):
    session = requests_html.HTMLSession()
    r = session.get(url)
    r.html.render()
    chart = r.html.find(finder, first=True)

    return 'something went awry' if chart is None else chart.text

# New data source means new way to scrape. New data processing made to accommodate
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
