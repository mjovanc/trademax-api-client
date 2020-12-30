import unittest

from requests import HTTPError

from model.trademax_api import TrademaxAPI


class APITest(unittest.TestCase):
    def setUp(self):
        self.trademax_api = TrademaxAPI()

    def test_create_token(self):
        self.assertTrue(type(self.trademax_api.TOKEN) is str)

    def test_get_wrong_purchase_order(self):
        # Testing a wrong purchase order id
        po = self.trademax_api.get_purchase_order('IOT-wrong-id')
        self.assertRaises(po, HTTPError)

    def test_get_correct_purchase_order(self):
        # Testing a correct purchase order id
        po = self.trademax_api.get_purchase_order('IOT1002674')
        print(po)
        self.assertTrue(type(po) is list)


