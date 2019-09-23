import json


class BankXpath:
    def __init__(self, name, country, fromcurrency, tocurrencyxpath, buyxpath, sellxpath, *args, **kwargs):
        self.name = name
        self.country = country
        self.fromCurrency = fromcurrency
        self.toCurrencyXpath = tocurrencyxpath
        self.buyxpath = buyxpath
        self.sellxpath = sellxpath

    def to_JSON(self):
        string = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        return json.loads(string)
