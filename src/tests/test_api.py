import unittest

from requests import HTTPError

from src.model.trademax_api import TrademaxAPI


class APITest(unittest.TestCase):
    def test_create_token(self):
        self.trademax_api = TrademaxAPI()
        self.assertTrue(type(self.trademax_api.TOKEN) is str)

    def test_get_purchase_order(self):
        self.trademax_api = TrademaxAPI()

        # Testing a wrong purchase order id
        p1 = self.trademax_api.get_purchase_order('IOT-wrong-id')
        self.assertRaises(p1, HTTPError)

        # Testing a correct purchase order id
        p2 = self.trademax_api.get_purchase_order('IOT1002674')
        self.assertTrue(type(p2) is dict)


