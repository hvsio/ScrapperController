import json
import uuid

from bson import ObjectId


class BankXpath:
    def __init__(self, name, country, pageurl, fromcurrency, tocurrencyxpath, buyxpath, sellxpath, *args, **kwargs):
        self.id = ObjectId()
        self.name = name
        self.country = country
        self.pageurl = pageurl
        self.fromCurrency = fromcurrency
        self.toCurrencyXpath = tocurrencyxpath
        self.buyxpath = buyxpath
        self.sellxpath = sellxpath

    def to_JSON(self):
        string = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        return json.loads(string)
