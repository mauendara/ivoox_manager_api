from ivoox_data_manager import *
from flask import Flask
from flask_restful import Api, Resource, reqparse

class Episode(Resource):

    def __init__(self):
        self.data_manager = IvooxDataManager()

    def get(self):
        return self.data_manager.get_episodes(), 200


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Episode, "/api/episodes")

    app.run(debug=True)

