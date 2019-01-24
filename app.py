from ivoox_data_manager import *
from flask import Flask
from flask_restful import Api, Resource, reqparse
from config import *
import logging


class PolesList(Resource):

    def __init__(self):
        self.config = read_config()
        self.data_manager = IvooxDataManager(config['database_env'])

    def get(self):
        poles_list = self.data_manager.get_poles_by_season(self.config['ivoox_podcast_season'])
        poles = []
        for p in poles_list:
            poles.append(p.to_dict())
        return poles, 200


class PolesCount(Resource):

    def __init__(self):
        self.config = read_config()
        self.data_manager = IvooxDataManager(config['database_env'])

    def get(self):
        return self.data_manager.count_poles_by_season(self.config['ivoox_podcast_season']), 200


if __name__ == "__main__":
    logging.basicConfig(filename='app.log',
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    config = read_config()

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(PolesList, "/api/poles/list")
    api.add_resource(PolesCount, "/api/poles/count")

    app.run(debug=True)

