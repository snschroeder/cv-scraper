from flask import Flask
from json_encoder import JSONEncoder
from pprint import pprint
import mongo_info
import pymongo


application = Flask(__name__)

@application.route('/')
def hello():
	return '''Hello! This is an api that scrapes data from the CDC regarding Covid-19. \n
		Please use the /infected_data endpoint to get JSON data with the date and total count of confirmed cases of Covid-19 in the US. \n
		More endpoints will be added in the future. '''

@application.route('/infected_data', methods=['GET'])
def get_infected_info():
	client = pymongo.MongoClient(mongo_info.connection_url)
	db = client.covid.daily
	dataset = db.find({})

	output = []

	for val in dataset:
		output.append(val)


	json_out = JSONEncoder().encode(output)

	pprint(json_out)

	return json_out

if __name__ == "__main__":
	application.debug = True
	application.run()
