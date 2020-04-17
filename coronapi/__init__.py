import os

from flask import Flask
from mongo_info import connection_url

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = connection_url
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)

    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)

    except OSError:
        pass

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

    	pprint(output)

    return app
