import pymongo
import json
from bson.json_util import dumps


# Connect to docker container steps.
# docker run -d -p 27027:27017 --name scrapper-settings mongo //creates a new instance of mongo
# docker start scrapper-settings //start the container if you already have created it.

class MongoConnection:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://127.0.0.1:27027/")
        self.banks_db = self.myclient["Banks"]
        self.xpath_collection = self.banks_db["xpath"]

    def add_bank(self, bank):
        #if self.xpath_collection.find({"name": bank.name}):
        #    return -1
        data = bank.to_JSON()
        self.xpath_collection.insert(data)
        return 0

    def get_banks(self):
        data = self.xpath_collection.find()
        data = dumps(data)[1:-1]
        return json.dumps(data).replace("\\", "")

    def update_bank(self, bank):
        if self.xpath_collection.find({"name": bank.name}):
            data = bank.to_JSON()
            self.xpath_collection.replace_one({"name": bank.name, "country": bank.country}, data)
            return "updated"
        else:
            self.add_bank(bank)
            return "added"
