from flask import Flask, request
from flask_cors import CORS
from src.models.bank_xpath import BankXpath
from src.services.FeesService import FeesService
from src.models.fee_object import Fee
from src.services.BanksXpathServices import MongoConnection

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
    return FeesService.get_fees(country_iso)


@app.route('/fees', methods=['GET'])
def get_fees():
    return FeesService.get_fees(None)


@app.route('/fees', methods=['POST'])
def on_post_fees():
    posted_data = request.get_json()
    print(posted_data)
    fee = Fee(**posted_data)
    validation = fee.validate()
    if validation:
        return validation
    else:
        return FeesService.add_fee(fee)


@app.route('/fees', methods=['PUT'])
def on_put_fees():
    posted_data = request.get_json()
    fee = Fee(**posted_data)
    validation = fee.validate()
    if validation:
        return validation
    else:
        return FeesService.update_fee(fee)


@app.route('/fees/<string:fee_id>', methods=['DELETE'])
def on_delete_fees(fee_id):
    return FeesService.delete_fee(fee_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
