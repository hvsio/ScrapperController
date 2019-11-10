from flask import Flask, request, jsonify
from flask_cors import CORS
from src.bank_xpath import BankXpath
from src.mongo_connection import MongoConnection

app = Flask(__name__)
CORS(app)


@app.route('/banks', methods=['GET'])
def on_get():
    return MongoConnection.get_banks()


@app.route('/banks', methods=['POST'])
def on_post():
    posted_data = request.get_json()
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
