import pymongo
import sys
from src.environment.enviroment import Config
from bson.json_util import dumps
from flask import Response, json
import ccy


class FeesService:
    TimeoutResponse = Response(response=json.dumps({'status': 'MongoDB timeout'}),
                               status=408,
                               mimetype='application/json')

    @staticmethod
    def log_and_return_error_response(exception):
        # TODO log exception variable
        print(str(exception))
        return FeesService.TimeoutResponse

    @staticmethod
    def add_fee(fee):
        try:
            databaseRef = FeesService.connect_to_fees_database()
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
            return FeesService.log_and_return_error_response(e)

    @staticmethod
    def update_fee(fee):
        try:
            databaseRef = FeesService.connect_to_fees_database()
            query = {"id": fee.id}
            data = fee.to_JSON()
            if databaseRef.find_one(query):
                databaseRef.find_one_and_replace(query, data)
                return Response(response=json.dumps({'status': 'fee updated'}),
                                status=200,
                                mimetype='application/json')
            else:
                return FeesService.add_fee(fee)
        except Exception as e:
            return FeesService.log_and_return_error_response(e)

    @staticmethod
    def delete_fee(fee_id):
        try:
            databaseRef = FeesService.connect_to_fees_database()
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
            return FeesService.log_and_return_error_response(e)

    @staticmethod
    def connect_to_fees_database():
        Config.initialize()
        environment = Config.cloud('DATABASE') if (len(sys.argv) > 1 and sys.argv[1] == 'cloud') else Config.dev(
            'DATABASE')
        myClient = pymongo.MongoClient(environment)
        fees_db = myClient["Fees"]
        return fees_db["paymentfees"]


    @staticmethod
    def get_fees(country_iso):
        try:
            if country_iso is None:
                query = {}
            else:
                query = {"country": country_iso}
            data = FeesService.connect_to_fees_database().find(query, {"_id": 0, })
            fees = dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
            fees = json.loads(fees)

            for x in fees:
                x['currency'] = ccy.countryccy(x['country'])

            fees = dumps(fees, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(response=fees, status=201, mimetype='application/json')
        except Exception as e:
            return FeesService.log_and_return_error_response(e)

