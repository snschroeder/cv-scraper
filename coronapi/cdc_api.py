from flask import Flask
from json_encoder import JSONEncoder
from pprint import pprint
import mongo_info
import pymongo


app = Flask(__name__)

@app.route('/')
def hello():
	return 'Hello!'

@app.route('/infected_data', methods=['GET'])
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

	# JSON_OUT = JSON.DUMPS(OUTPUT)
	#
	# PPRINT(JSON_OUT)

	# return jsonify(output)
