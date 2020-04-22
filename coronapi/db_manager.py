from pymongo import MongoClient
import scraper
import pymongo
import mongo_info
import dns

# ran first time db was created to seed it. Will not need in the future.
def __initialize_db(url):
    client = MongoClient(url)
    db = client.covid

    dirtyData = scraper.scrape_data(cdcChartUrl, finder)
    day, infected = scraper.process_data(dirtyData)

    for ind, val in enumerate(day):
        dailyData = {
            'day': val,
            'infected': infected[ind]
        }
        result = db.daily.insert_one(dailyData)
        print('Created as {0}'.format(result.inserted_id))

def update_db(db_url, cdc_url):
    dirty_data = scraper.scrape_json(cdc_url)
    date, infected = scraper.process_json(dirty_data)

    client = MongoClient(db_url)
    db = client.covid

    latest = db.daily.find_one({}, sort=[('_id', -1)])

    db_day = latest['day']
    ind = date.index(db_day)

    for i in range(ind + 1, len(date)):
        daily_data = {
            'day': date[i],
            'infected': infected[i]
        }
        result = db.daily.insert_one(daily_data)
        print('Created as {0}'.format(result.inserted_id))

# Old update db method - cdc data changed, created new update method to reflect the different data
def __update_db(db_url, cdc_url, finder):
    dirty_data = scraper.scrape_data(cdc_url, finder)
    day, infected = scraper.process_data(dirty_data)

    client = MongoClient(db_url)
    db = client.covid
    latest = db.daily.find_one({}, sort=[("_id", -1)])
    print(day)

    db_day = latest['day']
    ind = day.index(db_day)

    for i in range(ind + 1, len(day)):
        daily_data = {
            'day': day[i],
            'infected': infected[i]
        }
        result = db.daily.insert_one(daily_data)
        print('Created as {0}'.format(result.inserted_id))

update_db(mongo_info.connection_url, mongo_info.json_data)
