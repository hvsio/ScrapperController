import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from src.bank_xpath import BankXpath
from src.fees import Fee
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


# ----------- Szymon's efforts below :) ------

@app.route('/fees/get', methods=['GET'])
def on_get_fees():
    return MongoConnection.get_fees()


@app.route('/fees/post', methods=['POST'])
def on_post_fees():
    posted_data = request.get_json()
    print(posted_data)
    fee = Fee(**posted_data)
    validation = fee.validate()
    if validation:
        return validation
    else:
        return MongoConnection.add_fee(fee)


@app.route('/fees/put', methods=['PUT'])
def on_put_fees():
    posted_data = request.get_json()
    fee = Fee(**posted_data)
    validation = fee.validate()
    if validation:
        return validation
    else:
        return MongoConnection.update_fee(fee)


@app.route('/fees/<string:fee_id>/delete', methods=['DELETE'])
def on_delete_fees(fee_id):
    return MongoConnection.delete_fee(fee_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
