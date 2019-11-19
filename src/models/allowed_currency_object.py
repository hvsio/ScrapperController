import json

import ccy

from src.country_codes import CC
from src.dictionary import ERRORS
from bson import ObjectId
from flask import Response, json


class Currency:
    def __init__(self, name, allowed, *args, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs.get('id')
        else:
            self.id = ObjectId()
        self.name = name
        self.allowed = allowed

    def to_JSON(self):
        string = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        return json.loads(string)

    def validate(self):
        errors = []
        try:
            ccy.currency(self.name)
        except:
            errors.append(ERRORS["wrong_country_iso"])

        if errors:
            error_message = {"errors": errors}
            return Response(
                response=json.dumps(error_message),
                status=400,
                mimetype='application/json')
        else:
            return None
