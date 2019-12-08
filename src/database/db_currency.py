import pymongo
import sys
from src.environment.enviroment import Config
from bson.json_util import dumps
from flask import Response, json


class DatabaseCurrency:
    TimeoutResponse = Response(response=json.dumps({'status': 'MongoDB timeout'}),
                               status=408,
                               mimetype='application/json')

    @staticmethod
    def update_currency(currency):
        try:
            databaseRef = DatabaseCurrency.connect_to_database()
            query = {"id": currency.id}
            data = currency.to_JSON()
            if databaseRef.find_one(query):
                databaseRef.find_one_and_replace(query, data)
                return Response(response=json.dumps({'status': 'updated'}),
                                status=200,
                                mimetype='application/json')
            else:
                return DatabaseCurrency.add_currency(currency)
        except Exception as e:
            return DatabaseCurrency.log_and_return_error_response(e)

    @staticmethod
    def delete(currency_id):
        try:
            databaseRef = DatabaseCurrency.connect_to_database()
            query = {"id": currency_id}
            result = databaseRef.find_one(query)
            if result:
                databaseRef.delete_one(query)
                return Response(response=json.dumps({'status': 'deleted'}),
                                status=200,
                                mimetype='application/json')
            else:
                return Response(response=json.dumps({'status': 'bank does not exist'}),
                                status=400,
                                mimetype='application/json')
        except Exception as e:
            return DatabaseCurrency.log_and_return_error_response(e)

    @staticmethod
    def connect_to_database():
        Config.initialize()
        environment = Config.cloud('DATABASE') if (len(sys.argv) > 1 and sys.argv[1] == 'cloud') else Config.dev(
            'DATABASE')
        myClient = pymongo.MongoClient(environment)
        currency_db = myClient["AllowedCurrencies"]
        return currency_db["allowed"]

    @staticmethod
    def add_currency(currency):
        try:
            databaseRef = DatabaseCurrency.connect_to_database()
            data = currency.to_JSON()
            query = {"name": currency.name, "allowed": currency.allowed}
            if databaseRef.find_one(query):
                return Response(response=json.dumps({'status': 'bank already exist'}),
                                status=400,
                                mimetype='application/json')
            else:
                databaseRef.insert(data)
                return Response(response=json.dumps({'status': 'added'}),
                                status=201,
                                mimetype='application/json')
        except Exception as e:
            return DatabaseCurrency.log_and_return_error_response(e)

    @staticmethod
    def get_currency():
        try:
            data = DatabaseCurrency.connect_to_database().find({}, {"_id": 0, })
            currencies = dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(response=currencies,
                            status=201,
                            mimetype='application/json')
        except Exception as e:
            return DatabaseCurrency.log_and_return_error_response(e)

    @staticmethod
    def log_and_return_error_response(exception):
        # TODO log exception variable
        print(str(exception))
        return DatabaseCurrency.TimeoutResponse
