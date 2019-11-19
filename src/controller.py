from flask import Flask, request
from flask_cors import CORS
from src.bank_xpath import BankXpath
from src.database.db_country import DatabaseCountry
from src.database.db_fees import DatabaseFees
from src.database.db_currency import DatabaseCurrency
from src.models.allowed_country_object import Country
from src.models.allowed_currency_object import Currency
from src.models.fee_object import Fee
from src.mongo_connection import MongoConnection

app = Flask(__name__)
CORS(app)


@app.route('/banks', methods=['GET'])
def on_get():
    return MongoConnection.get_banks()


@app.route('/banks', methods=['POST'])
def on_post():
    posted_data = request.get_json()
    print(posted_data)
    bank = BankXpath(**posted_data)
    validation = bank.validate()
    if validation:
        return validation
    else:
        return MongoConnection.add_bank(bank)


@app.route('/banks', methods=['PUT'])
def on_put():
    posted_data = request.get_json()
    bank = BankXpath(**posted_data)
    validation = bank.validate()
    if validation:
        return validation
    else:
        return MongoConnection.update_bank(bank)


@app.route('/banks/<string:bank_id>', methods=['DELETE'])
def on_delete(bank_id):
    return MongoConnection.delete(bank_id)


# ----------- FEES ENDPOINTS ------
@app.route('/fees/<string:country_iso>', methods=['GET'])
def get_fees_with_country(country_iso):
    return DatabaseFees.get_fees(country_iso)


@app.route('/fees', methods=['GET'])
def get_fees():
    return DatabaseFees.get_fees(None)


@app.route('/fees', methods=['POST'])
def on_post_fees():
    posted_data = request.get_json()
    print(posted_data)
    fee = Fee(**posted_data)
    validation = fee.validate()
    if validation:
        return validation
    else:
        return DatabaseFees.add_fee(fee)


@app.route('/fees', methods=['PUT'])
def on_put_fees():
    posted_data = request.get_json()
    fee = Fee(**posted_data)
    validation = fee.validate()
    if validation:
        return validation
    else:
        return DatabaseFees.update_fee(fee)


@app.route('/fees/<string:fee_id>', methods=['DELETE'])
def on_delete_fees(fee_id):
    return DatabaseFees.delete_fee(fee_id)


# ----------- COUNTRY ENDPOINTS ------
@app.route('/countries', methods=['GET'])
def on_get_countries():
    return DatabaseCountry.get_countries()


@app.route('/countries', methods=['POST'])
def on_post_countries():
    posted_data = request.get_json()
    country = Country(**posted_data)
    validation = country.validate()
    if validation:
        return validation
    else:
        return DatabaseCountry.add_country(country)


@app.route('/countries', methods=['PUT'])
def on_put_countries():
    posted_data = request.get_json()
    country = Country(**posted_data)
    validation = country.validate()
    if validation:
        return validation
    else:
        return DatabaseCountry.update_country(country)


@app.route('/countries/<string:country_id>', methods=['DELETE'])
def on_delete_countries(country_id):
    return DatabaseCountry.delete(country_id)


# ----------- CURRENCY ENDPOINTS ------
@app.route('/currencies', methods=['GET'])
def on_get_currencies():
    return DatabaseCurrency.get_currency()


@app.route('/currencies', methods=['POST'])
def on_post_currencies():
    posted_data = request.get_json()
    currency = Currency(**posted_data)
    validation = currency.validate()
    if validation:
        return validation
    else:
        return DatabaseCurrency.add_currency(currency)


@app.route('/currencies', methods=['PUT'])
def on_put_currencies():
    posted_data = request.get_json()
    currency = Currency(**posted_data)
    validation = currency.validate()
    if validation:
        return validation
    else:
        return DatabaseCurrency.update_currency(currency)


@app.route('/currencies/<string:currency_id>', methods=['DELETE'])
def on_delete_currencies(currency_id):
    return DatabaseCurrency.delete(currency_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
