import unittest
from src.models.bank_xpath import BankXpath
from src.models.dictionary import ERRORS


class TestingBanksModels(unittest.TestCase):

    def test_bank_wrong_iso(self):
        bankObject = create_correct_bank()
        bankObject.fromCurrency = "Danish Krones"
        error = [ERRORS["wrong_from_currency"]]
        self.assertEqual(bankObject.validate().json.get('errors'), error)
        self.assertEqual(bankObject.validate().status_code, 400)

    def test_bank_wrong_name(self):
        bankObject = create_correct_bank()
        bankObject.name = ""
        error = [ERRORS["wrong_bank_name"]]
        self.assertEqual(bankObject.validate().json.get('errors'), error)
        self.assertEqual(bankObject.validate().status_code, 400)

    def test_bank_wrong_URL(self):
        bankObject = create_correct_bank()
        bankObject.pageurl = "www.google.com"
        error = [ERRORS["bank_url_error"]]
        self.assertEqual(bankObject.validate().json.get('errors'), error)
        self.assertEqual(bankObject.validate().status_code, 400)

    def test_bank_empty_URL(self):
        bankObject = create_correct_bank()
        bankObject.pageurl = ''
        error = [ERRORS["empty_url"], ERRORS["bank_url_error"]]
        self.assertEqual(bankObject.validate().json.get('errors'), error)
        self.assertEqual(bankObject.validate().status_code, 400)

    def test_bank_wrong_xpath(self):
        bankObject = create_correct_bank()
        bankObject.toCurrencyXpath = 9
        bankObject.buyxpath = "_html!body"
        bankObject.sellxpath = "www.danskebank.com"
        error = [ERRORS["to_currency_xpath"], ERRORS["buy_exchange_xpath"], ERRORS["sell_exchange_xpath"]]
        self.assertEqual(bankObject.validate().json.get('errors'), error)
        self.assertEqual(bankObject.validate().status_code, 400)

    def test_bank_wrong_units(self):
        bankObject = create_correct_bank()
        bankObject.unit = "%"
        error = [ERRORS["wrong_unit"]]
        self.assertEqual(bankObject.validate().json.get('errors'), error)
        self.assertEqual(bankObject.validate().status_code, 400)

    def test_bank_correct_units(self):
        bankObject = create_correct_bank()
        bankObject.unit = "M100"
        self.assertIsNone(bankObject.validate())
        bankObject.unit = "exchange100"
        self.assertIsNone(bankObject.validate())
        bankObject.unit = "percentage"
        self.assertIsNone(bankObject.validate())
        bankObject.unit = "exchange"
        self.assertIsNone(bankObject.validate())

    def test_valid_bank(self):
        bankObject = create_correct_bank()
        self.assertIsNone(bankObject.validate())


def create_correct_bank():
    return BankXpath("Danske bank", "DK", "http://www.danskebank.com", "DKK",
                     "/html/body/div[1]/div[4]/div/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[1]",
                     "/html/body/div[1]/div[4]/div/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[2]/div/div",
                     "/html/body/div[1]/div[4]/div/div[2]/div[1]/div[2]/table/tbody/tr[8]/td[2]/div/div",
                     "M100",
                     "/html/body/div[1]/div[4]/div/div[2]/div[1]/div[2]/table/tbody/tr[8]/td[2]/div/div",
                     False
                     )
