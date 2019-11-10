import json
import lxml.etree
import validators
from src.dictionary import ERRORS
from bson import ObjectId
from iso4217 import Currency
from flask import Response, json
from src.country_codes import CC


class BankXpath:
    def __init__(self, name, country, pageurl, fromcurrency, tocurrencyxpath, buyxpath, sellxpath, unit,
                 exchangeunitxpath, iscrossinverted, *args,
                 **kwargs):
        if 'id' in kwargs:
            self.id = kwargs.get('id')
        else:
            self.id = ObjectId()
        self.name = name
        self.country = country
        self.pageurl = pageurl
        self.fromCurrency = fromcurrency
        self.toCurrencyXpath = tocurrencyxpath
        self.buyxpath = buyxpath
        self.sellxpath = sellxpath
        self.unit = unit
        self.exchangeunitxpath = exchangeunitxpath
        self.iscrossinverted = iscrossinverted

    def to_JSON(self):
        string = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        return json.loads(string)

    def validate(self):
        errors = []
        if not CC.__contains__(self.country):
            errors.append(ERRORS["wrong_country_iso"])
        if not self.name:
            errors.append(ERRORS["wrong_bank_name"])
        if not self.pageurl:
            errors.append(ERRORS["empty_url"])
        if not validators.url(self.pageurl):
            errors.append(ERRORS["bank_url_error"])
        if not self.unit == "M100" and not self.unit == "M1000" and not self.unit == "exchange" \
                and not self.unit == "percentage":
            errors.append(ERRORS["wrong_unit"])
        try:
            Currency(self.fromCurrency)
        except:
            errors.append(ERRORS["wrong_from_currency"])
        try:
            lxml.etree.XPath(self.toCurrencyXpath)
        except:
            errors.append(ERRORS["to_currency_xpath"])
        try:
            lxml.etree.XPath(self.buyxpath)
        except:
            errors.append(ERRORS["buy_exchange_xpath"])
        try:
            lxml.etree.XPath(self.toCurrencyXpath)
        except:
            errors.append(ERRORS["sell_exchange_xpath"])
        if errors:
            error_message = {"errors": errors}
            return Response(
                response=json.dumps(error_message),
                status=400,
                mimetype='application/json')
        else:
            return None
