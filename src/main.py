from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from model.TrademaxAPI import TrademaxAPI


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.setGeometry(300, 300, 600, 400)
        # self.setWindowTitle("Trademax API Client")
        # self.show()

        t = TrademaxAPI()

        # Get one purchase order
        po = t.get_purchase_order('IO1833064')
        print(po)

        # Acknowledge one purchase order
        t.post_purchase_order_acknowledgement('IO1833064', '2039-05-03T12:18:53+02:00')
        po = t.get_purchase_order('IO1833064')
        print(po)

        # Our response of an purchase order
        t.post_purchase_order_response(
            request_id='IO1833064', status='ACCEPTED', reason='Just a test reason',
            external_reference='Test reference', gross_amount=0.0, tax_amount=0.0,
            total_amount=0.0, confirmed_delivery_from='Test confirmed delivery from', confirmed_delivery_to='Test confirmed delivery to',
            lines={
                'supplier_item_no': '',
                'line_no': 10000,
                'quantity': 2,
                'gross_price': 1000.0,
                'tax_percentage': 1000.0,
                'gross_amount': 100.0,
                'tax_amount': 100.0,
                'total_amount': 100.0,
                'confirmed_delivery_from': '',
                'confirmed_delivery_to': '',
                'status': '',
            }
        )

        # Dispatch purchase order
        t.post_purchase_order_dispatch(
            purchase_order_id='IO1833064', dispatch_date='2039-05-03T12:18:53+02:00',
            delivery_date='2045-05-03T12:18:53+02:00',
            lines={
                'supplier_item_no': 'supplier no test',
                'line_no': 10,
                'quantity': 15,
                'quantity_outstanding': 20
            },
            external_reference='ext ref test', carrier_reference='Carrier ref test', shipping_agent='Shipping agent test',
            shipping_agent_service='Shipping agent service test', tracking_code='Tracking code test',
            dispatch_address={}
        )


        exit(1)  # just to escape the loop (temporary)


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())

