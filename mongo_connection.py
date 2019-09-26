import pymongo
from bson.json_util import dumps


# Connect to docker container steps.
#
#  //creates a new instance of mongo
# stop: docker stop scrapper-settings
# start existing container: docker start scrapper-settings
# check running containers: docker ps
# check all containers in local: docker container ls -a //(including stopped ones)
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
