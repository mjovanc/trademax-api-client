import unittest

from src.model.TrademaxAPI import TrademaxAPI


class APITest(unittest.TestCase):
    def create_token(self):
        self.trademax_api = TrademaxAPI()
        self.assertTrue(type(self.trademax_api.TOKEN) is str)


if __name__ == '__main__':
    unittest.main()
