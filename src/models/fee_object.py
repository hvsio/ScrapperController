import json
from src.models.country_codes import CC
from src.models.dictionary import ERRORS
from bson import ObjectId
from flask import Response, json


class Fee:
    def __init__(self, country, sepa, intl, currency, *args, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs.get('id')
        else:
            self.id = ObjectId()
        self.country = country
        self.sepa = float(sepa)
        self.intl = float(intl)
        self.currency = currency

    def to_JSON(self):
        string = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        return json.loads(string)

    def validate(self):
        errors = []
        if not CC.__contains__(self.country):
            errors.append(ERRORS["wrong_country_iso"])

        if errors:
            error_message = {"errors": errors}
            return Response(
                response=json.dumps(error_message),
                status=400,
                mimetype='application/json')
        else:
            return None
