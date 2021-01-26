import unittest

from requests.exceptions import HTTPError

from model.trademax_api import TrademaxAPI


class APITest(unittest.TestCase):
    def setUp(self):
        """Setting up for the test case."""
        self.trademax_api = TrademaxAPI()
        self.purchase_order_id = 'IOT1002674'

    def test_create_token(self):
        """Testing to create a Bearer Token."""
        self.assertTrue(type(self.trademax_api.TOKEN) is str)

    def test_get_wrong_purchase_order(self):
        """Testing a wrong id of an purchase order."""
        with self.assertRaises(HTTPError):
            self.trademax_api.get_purchase_order('IOT-wrong-id')

    def test_get_correct_purchase_order(self):
        """Testing a correct id of an purchase order."""
        po = self.trademax_api.get_purchase_order(self.purchase_order_id)
        self.assertTrue(type(po) is list)

    def test_acknowledge_purchase_order(self):
        """Testing to acknowledge a purchase order."""
        po = self.trademax_api.post_purchase_order_acknowledgement(self.purchase_order_id)
        print(type(po))


