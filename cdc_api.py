from flask import Flask, jsonify
from pprint import pprint
import mongo_info
import pymongo


app = Flask(__name__)

@app.route('/')
def hello():
	return 'Hello!'

# currently broken, please fix me so I return a useable response
@app.route('/infected_data', methods=['GET'])
def get_infected_info():
	client = pymongo.MongoClient(mongo_info.connection_url)
	db = client.covid.daily
	dataset = db.find({})

	output = []

	for val in dataset:
		output.append(val)

	pprint(output)
	
	# return jsonify(output)