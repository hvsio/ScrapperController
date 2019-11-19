import pymongo
import sys
from src.environment.enviroment import Config
from bson.json_util import dumps
from flask import Response, json


class DatabaseCountry:
    TimeoutResponse = Response(response=json.dumps({'status': 'MongoDB timeout'}),
                               status=408,
                               mimetype='application/json')

    @staticmethod
    def update_country(country):
        try:
            databaseRef = DatabaseCountry.connect_to_database()
            query = {"id": country.id}
            data = country.to_JSON()
            if databaseRef.find_one(query):
                databaseRef.find_one_and_replace(query, data)
                return Response(response=json.dumps({'status': 'updated'}),
                                status=200,
                                mimetype='application/json')
            else:
                return DatabaseCountry.add_country(country)
        except Exception as e:
            return DatabaseCountry.log_and_return_error_response(e)

    @staticmethod
    def delete(country_id):
        try:
            databaseRef = DatabaseCountry.connect_to_database()
            query = {"id": country_id}
            result = databaseRef.find_one(query)
            if result:
                databaseRef.delete_one(query)
                return Response(response=json.dumps({'status': 'deleted'}),
                                status=200,
                                mimetype='application/json')
            else:
                return Response(response=json.dumps({'status': 'country does not exist'}),
                                status=400,
                                mimetype='application/json')
        except Exception as e:
            return DatabaseCountry.log_and_return_error_response(e)

    @staticmethod
    def connect_to_database():
        Config.initialize()
        environment = Config.cloud('DATABASE') if (len(sys.argv) > 1 and sys.argv[1] == 'cloud') else Config.dev(
            'DATABASE')
        myClient = pymongo.MongoClient(environment)
        country_db = myClient["AllowedCountries"]
        return country_db["allowed"]

    @staticmethod
    def add_country(country):
        try:
            databaseRef = DatabaseCountry.connect_to_database()
            data = country.to_JSON()
            query = {"country": country.name}
            if databaseRef.find_one(query):
                return Response(response=json.dumps({'status': 'country already exist'}),
                                status=400,
                                mimetype='application/json')
            else:
                databaseRef.insert(data)
                return Response(response=json.dumps({'status': 'added'}),
                                status=201,
                                mimetype='application/json')
        except Exception as e:
            return DatabaseCountry.log_and_return_error_response(e)

    @staticmethod
    def get_countries():
        try:
            data = DatabaseCountry.connect_to_database().find({}, {"_id": 0, })
            countries = dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(response=countries,
                            status=201,
                            mimetype='application/json')
        except Exception as e:
            return DatabaseCountry.log_and_return_error_response(e)

    @staticmethod
    def log_and_return_error_response(exception):
        # TODO log exception variable
        print(str(exception))
        return DatabaseCountry.TimeoutResponse
