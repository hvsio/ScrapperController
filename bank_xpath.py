import json
import lxml.etree
import validators
from bson import ObjectId
from iso4217 import Currency

from country_codes import CC


class BankXpath:
    def __init__(self, name, country, pageurl, fromcurrency, tocurrencyxpath, buyxpath, sellxpath, unit, *args, **kwargs):
        self.id = ObjectId()
        self.name = name
        self.country = country
        self.pageurl = pageurl
        self.fromCurrency = fromcurrency
        self.toCurrencyXpath = tocurrencyxpath
        self.buyxpath = buyxpath
        self.sellxpath = sellxpath
        self.unit = unit


    def to_JSON(self):
        string = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        return json.loads(string)

    def validate(self):
        errors =[]
        if not CC.__contains__(self.country):
            errors.append("Wrong country ISO code")
        if not self.name:
            errors.append("Wrong bank name")
        if not self.pageurl:
            errors.append("Empty bank URL")
        if not validators.url(self.pageurl):
            errors.append("Wrong bank URL format")
        if not self.unit == "M100" and not self.unit == "M1000" and not self.unit == "exchange" and not self.unit == "percentage":
            errors.append("units valid values [ M100, M1000, exchange, percentage ]")
        try:
            Currency(self.fromCurrency)
        except:
            errors.append("Wrong from currency code ISO")
        try:
            lxml.etree.XPath(self.toCurrencyXpath)
        except:
            errors.append("Wrong ToCurrency XPath")
        try:
            lxml.etree.XPath(self.buyxpath)
        except:
            errors.append("Wrong exchange buy XPath")
        try:
            lxml.etree.XPath(self.toCurrencyXpath)
        except:
            errors.append("Wrong exchange sell XPath")
        return errors


