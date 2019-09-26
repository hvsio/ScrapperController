import pymongo
from bson.json_util import dumps


# Connect to docker container steps.
# docker run -d -p 27027:27017 --name scrapper-settings mongo //creates a new instance of mongo
# docker start scrapper-settings //start the container if you already have created it.

class MongoConnection:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://0.0.0.0:27027/")
        self.banks_db = self.myclient["Banks"]
        self.xpath_collection = self.banks_db["xpath"]

    def add_bank(self, bank):
        data = bank.to_JSON()
        print(data)
        query = {"name": bank.name, "country": bank.country}
        if self.xpath_collection.find_one(query):
            return -1
        else:
            self.xpath_collection.insert(data)
            return 0

    def get_banks(self):
        data = self.xpath_collection.find({}, {"_id": 0, })
        data = dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        return data

    def update_bank(self, bank):
        query = {"name": bank.name, "country": bank.country}
        if self.xpath_collection.find(query):
            data = bank.to_JSON()
            self.xpath_collection.replace_one({"name": bank.name, "country": bank.country}, data)
            return "updated"
        else:
            data = bank.to_JSON()
            self.add_bank(data)
            return "added"

    def delete(self, bank_id):
        query = {"id": bank_id}
        result = self.xpath_collection.delete_one(query)
        print(result)
