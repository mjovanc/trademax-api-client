import unittest

from src.model.trademax_api import TrademaxAPI


class APITest(unittest.TestCase):
    def test_create_token(self):
        self.trademax_api = TrademaxAPI()
        self.assertTrue(type(self.trademax_api.TOKEN) is str)

    def test_get_purchase_order(self):
        pass

