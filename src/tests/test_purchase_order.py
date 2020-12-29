import unittest
from unittest import TestCase

from model.purchase_order import PurchaseOrder


class PurchaseOrderTest(TestCase):
    def setUp(self):
        self.po = PurchaseOrder(id='IO12345', purchase_order_id='IO12345', latest=0, created_at='date',
                                acknowledged_at='date', requested_delivery_from='date', requested_delivery_to='date',
                                currency='SEK', gross_amount=102.5, tax_amount=102.5, total_amount=205.0,
                                is_partial_delivery=False, sales_order={}, delivery_address={}, supplier={}, lines={})

    def test_add_wrong_total_amount(self):
        expected_total_amount = self.po.gross_amount + self.po.tax_amount
        self.assertEqual(expected_total_amount, self.po.total_amount)


if __name__ == '__main__':
    unittest.main()
