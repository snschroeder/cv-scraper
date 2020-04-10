import requests
import requests_html
from pprint import pprint

cdcChartUrl = 'https://www.cdc.gov/TemplatePackage/contrib/widgets/cdcCharts/iframe.html?chost=www.cdc.gov&cpath=/coronavirus/2019-ncov/cases-updates/cases-in-us.html&csearch=&chash=&ctitle=Cases%20in%20U.S.%20%7C%20CDC&wn=cdcCharts&wf=/TemplatePackage/contrib/widgets/cdcCharts/&wid=cdcCharts2&mMode=widget&mPage=&mChannel=&host=www.cdc.gov&displayMode=wcms&configUrl=/coronavirus/2019-ncov/cases-updates/total-cases-onset.json&class=mb-3'


session = requests_html.HTMLSession()
r = session.get(cdcChartUrl)
r.html.render()
chart = r.html.find('#cdc-chart-1-data', first=True)
pprint(chart.text)
