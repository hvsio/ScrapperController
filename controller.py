from flask import Flask, request, jsonify
from flask_cors import CORS
from bank_xpath import BankXpath
from mongo_connection import MongoConnection

app = Flask(__name__)
CORS(app)


@app.route('/banks', methods=['GET'])
def on_get():
    try:
        mongo_ref = MongoConnection()
        banks = mongo_ref.get_banks()
        return banks, 200
    except:
        return jsonify({"status": "MongoDB error"}), 408


@app.route('/banks', methods=['POST'])
def on_post():
    posted_data = request.get_json()
    bank = BankXpath(**posted_data)
    errors = bank.validate()
    print(errors)
    if errors:
        print("entering on errors")
        return jsonify({"errors": errors}), 400
    else:
        try:
            mongo_ref = MongoConnection()
            if mongo_ref.add_bank(bank) == 0:
                return jsonify({"status": "added"}), 201
            else:
                return jsonify({"status": "bank already exist"}), 400
        except:
            return jsonify({"status": "MongoDB error"}), 408


@app.route('/banks', methods=['PUT'])
def on_put():
    posted_data = request.get_json()
    bank = BankXpath(**posted_data)
    errors = bank.validate()
    if errors:
        return jsonify({"errors": errors}), 400
    else:
        try:
            mongo_ref = MongoConnection()
            response = mongo_ref.update_bank(bank)
            return jsonify({"status": response}), 201
        except:
            return jsonify({"status": "MongoDB error"}), 408


@app.route('/banks/<string:bank_id>', methods=['DELETE'])
def on_delete(bank_id):
    try:
        mongo_ref = MongoConnection()
        mongo_ref.delete(bank_id)
        return jsonify({"deleted": bank_id}), 200
    except:
        return jsonify({"status": "MongoDB error"}), 408


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
