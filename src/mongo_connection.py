import pymongo
import sys
from src.environment.enviroment import Config
from bson.json_util import dumps
from flask import Response, json


# Connect to docker container steps.
#  //creates a new instance of mongo
# stop: docker stop scrapper-settings
# start existing container: docker start scrapper-settings
# check running containers: docker ps
# check all containers in local: docker container ls -a //(including stopped ones)
# docker start scrapper-settings //start the container if you already have created it.

class MongoConnection:
    TimeoutResponse = Response(response=json.dumps({'status': 'MongoDB timeout'}),
                               status=408,
                               mimetype='application/json')

    @staticmethod
    def update_bank(bank):
        try:
            databaseRef = MongoConnection.connect_to_database()
            query = {"id": bank.id}
            data = bank.to_JSON()
            if databaseRef.find_one(query):
                databaseRef.find_one_and_replace(query, data)
                return Response(response=json.dumps({'status': 'updated'}),
                                status=200,
                                mimetype='application/json')
            else:
                return MongoConnection.add_bank(bank)
        except Exception as e:
            return MongoConnection.log_and_return_error_response(e)

    @staticmethod
    def delete(bank_id):
        try:
            databaseRef = MongoConnection.connect_to_database()
            query = {"id": bank_id}
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
            return MongoConnection.log_and_return_error_response(e)

    @staticmethod
    def connect_to_database():
        Config.initialize()
        environment = Config.cloud('DATABASE') if (len(sys.argv) > 1 and sys.argv[1] == 'cloud') else Config.dev(
            'DATABASE')
        myClient = pymongo.MongoClient(environment)
        banks_db = myClient["Banks"]
        return banks_db["xpath"]

    @staticmethod
    def add_bank(bank):
        try:
            databaseRef = MongoConnection.connect_to_database()
            data = bank.to_JSON()
            query = {"name": bank.name, "country": bank.country}
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
            return MongoConnection.log_and_return_error_response(e)

    @staticmethod
    def get_banks():
        try:
            data = MongoConnection.connect_to_database().find({}, {"_id": 0, })
            banks = dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(response=banks,
                            status=201,
                            mimetype='application/json')
        except Exception as e:
            return MongoConnection.log_and_return_error_response(e)

    @staticmethod
    def log_and_return_error_response(exception):
        # TODO log exception variable
        print(str(exception))
        return MongoConnection.TimeoutResponse


    # ----------- Szymon's efforts below :) ------

    @staticmethod
    def update_fee(fee):
        try:
            databaseRef = MongoConnection.connect_to_fees_database()
            query = {"id": fee.id}
            data = fee.to_JSON()
            if databaseRef.find_one(query):
                databaseRef.find_one_and_replace(query, data)
                return Response(response=json.dumps({'status': 'fee updated'}),
                                status=200,
                                mimetype='application/json')
            else:
                return MongoConnection.add_bank(fee)
        except Exception as e:
            return MongoConnection.log_and_return_error_response(e)

    @staticmethod
    def delete_fee(fee_id):
        try:
            databaseRef = MongoConnection.connect_to_fees_database()
            query = {"id": fee_id}
            result = databaseRef.find_one(query)
            if result:
                databaseRef.delete_one(query)
                return Response(response=json.dumps({'status': 'deleted'}),
                                status=200,
                                mimetype='application/json')
            else:
                return Response(response=json.dumps({'status': 'fee does not exist'}),
                                status=400,
                                mimetype='application/json')
        except Exception as e:
            return MongoConnection.log_and_return_error_response(e)

    @staticmethod
    def connect_to_fees_database():
        Config.initialize()
        environment = Config.cloud('DATABASE') if (len(sys.argv) > 1 and sys.argv[1] == 'cloud') else Config.dev(
            'DATABASE')
        myClient = pymongo.MongoClient(environment)
        fees_db = myClient["Fees"]
        return fees_db["paymentfees"]

    @staticmethod
    def add_fee(fee):
        try:
            databaseRef = MongoConnection.connect_to_fees_database()
            data = fee.to_JSON()
            query = {"country": fee.country}
            if databaseRef.find_one(query):
                return Response(response=json.dumps({'status': 'country already exists'}),
                                status=400,
                                mimetype='application/json')
            else:
                databaseRef.insert(data)
                return Response(response=json.dumps({'status': 'added'}),
                                status=201,
                                mimetype='application/json')
        except Exception as e:
            return MongoConnection.log_and_return_error_response(e)

    @staticmethod
    def get_fees():
        try:
            data = MongoConnection.connect_to_fees_database().find({}, {"_id": 0, })
            fees = dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(response=fees,
                            status=201,
                            mimetype='application/json')
        except Exception as e:
            return MongoConnection.log_and_return_error_response(e)

