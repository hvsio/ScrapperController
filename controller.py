import falcon
import json
from bank_xpath import BankXpath
from mongo_connection import MongoConnection
from bson.json_util import dumps
from waitress import serve

#how to run this: waitress-serve --listen=*:8000 controller:api

class BanksResource(object):

    def on_get(self, req, resp):
        mongo_ref = MongoConnection()
        banks = dumps(mongo_ref.get_banks())
        resp.body = banks

    def on_post(self, req, resp):
        posted_data = json.loads(req.stream.read())
        bank = BankXpath(**posted_data)
        mongo_ref = MongoConnection()
        if mongo_ref.add_bank(bank) == 0:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({"status": "added"})
        else:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"status": "bank already exist"})

    def on_put(self, req, resp):
        posted_data = json.loads(req.stream.read())
        bank = BankXpath(**posted_data)
        mongo_ref = MongoConnection()
        response = mongo_ref.update_bank(bank)
        resp.status = falcon.HTTP_201
        resp.body = json.dumps({"status": response})


class ScrapperConfiguration(object):

    def on_get(self, req, resp):
        return {"success"}


api = falcon.API()
banks_endpoints = BanksResource()
api.add_route('/banks', banks_endpoints)
serve(api, host='0.0.0.0', port=8000)
