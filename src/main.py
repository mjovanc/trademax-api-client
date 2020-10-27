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
        po = t.get_purchase_order('IOT1002674')
        print(po)

        # Acknowledge one purchase order
        poa = t.post_purchase_order_acknowledgement(po[0]['purchase_order_id'], '2039-05-03T12:18:53+02:00')
        print(poa)

        # Get one purchase order again
        # po = t.get_purchase_order('IOT1002674')
        print(po[0])
        print()

        # Values that will be entered in the application and set to these variables
        po_status = 'ACCEPTED'
        po_confirmed_delivery_from = '2039-05-03T12:18:53+02:00'
        po_confirmed_delivery_to = '2039-05-03T12:18:53+02:00'
        po_external_reference_response = 'our_unique_ref1'

        # Our response of an purchase order
        por = t.post_purchase_order_response(
            request_id=po[0]['purchase_order_id'], status=po_status, reason='',
            external_reference=po_external_reference_response, gross_amount=po[0]['gross_amount'],
            tax_amount=po[0]['tax_amount'], total_amount=po[0]['total_amount'],
            confirmed_delivery_from=po_confirmed_delivery_from, confirmed_delivery_to=po_confirmed_delivery_to,
            lines=[
                {
                    'supplier_item_no': po[0]['lines'][0]['supplier_item_no'],
                    'line_no': po[0]['lines'][0]['line_no'],
                    'quantity': po[0]['lines'][0]['quantity'],
                    'gross_price': po[0]['lines'][0]['gross_price'],
                    'tax_percentage': po[0]['lines'][0]['tax_percentage'],
                    'gross_amount': po[0]['lines'][0]['gross_amount'],
                    'tax_amount': po[0]['lines'][0]['tax_amount'],
                    'total_amount': po[0]['lines'][0]['total_amount'],
                    'confirmed_delivery_from': po_confirmed_delivery_from,
                    'confirmed_delivery_to': po_confirmed_delivery_to,
                    'status': po_status,
                }
            ],
        )
        print(por)

        print('Purchase order now: ')
        print(po)

        # Values that will be entered in the application and set to these variables
        po_dispatch_date_dispatch = '2039-05-03T12:18:53+02:00'
        po_delivery_date_dispatch = '2045-05-03T12:18:53+02:00'
        po_supplier_item_no_dispatch = 'unique_own_id1'
        po_line_no_dispatch = 10000
        po_quantity_dispatch = 10
        po_quantity_outstanding_dispatch = 20
        po_external_reference_dispatch = 'our_unique_ref2'
        po_carrier_reference_dispatch = 'carrier_unique_ref1'
        po_shipping_agent_dispatch = 'Shipping agent test'
        po_shipping_agent_service_dispatch = 'DHL'
        po_tracking_code_dispatch = 'HDH22F27831'

        # Dispatch purchase order
        t.post_purchase_order_dispatch(
            purchase_order_id=po[0]['purchase_order_id'], dispatch_date=po_dispatch_date_dispatch,
            delivery_date=po_delivery_date_dispatch,
            lines=[
                {
                    'supplier_item_no': po_supplier_item_no_dispatch,
                    'line_no': po_line_no_dispatch,
                    'quantity': po_quantity_dispatch,
                    'quantity_outstanding': po_quantity_outstanding_dispatch
                }
            ],
            external_reference=po_external_reference_dispatch, carrier_reference=po_carrier_reference_dispatch,
            shipping_agent=po_shipping_agent_dispatch, shipping_agent_service=po_shipping_agent_service_dispatch,
            tracking_code=po_tracking_code_dispatch, dispatch_address={}
        )

        # Do a purchase order invoice

        # t.post_purchase_order_invoice(
        #     purchase_order_id='', lines=[{}], external_reference='', gross_amount=0.0,
        #     total_amount=0.0, tax_amount=0.0, invoice_date='', due_date=''
        # )

        exit(1)  # just to escape the loop (temporary)


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())

