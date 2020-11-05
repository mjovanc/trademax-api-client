import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QWidget, QStackedWidget

from model.TrademaxAPI import TrademaxAPI


class AboutWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/about_widget.ui', self)


class PurchaseOrderWidget(QStackedWidget):
    def __init__(self, trademax_api, purchase_order_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/purchase_order_widget.ui', self)
        self.trademax_api = trademax_api
        self.order = self.trademax_api.get_purchase_order(purchase_order_id)
        self.purchase_order = self.order[0]

        self.set_intial_data()

    def set_intial_data(self):
        self.purchase_order_id.setText(self.purchase_order['purchase_order_id'])
        self.created_at.setText(self.purchase_order['created_at'])
        self.acknowledged_at.setText(self.purchase_order['acknowledged_at'])
        self.requested_delivery_from.setText(self.purchase_order['requested_delivery_from'])
        self.requested_delivery_to.setText(self.purchase_order['requested_delivery_to'])
        self.gross_amount.setValue(self.purchase_order['gross_amount'])
        self.tax_amount.setValue(self.purchase_order['tax_amount'])
        self.total_amount.setValue(self.purchase_order['total_amount'])

        # Delivery Address
        self.delivery_address_name.setText(self.purchase_order['delivery_address']['name'])
        self.delivery_address_phone.setText(self.purchase_order['delivery_address']['phone'])
        self.delivery_address_email.setText(self.purchase_order['delivery_address']['email'])
        self.delivery_address_address.setText(self.purchase_order['delivery_address']['address'])
        self.delivery_address_postcode.setText(self.purchase_order['delivery_address']['postcode'])
        self.delivery_address_city.setText(self.purchase_order['delivery_address']['city'])
        self.delivery_address_country.setText(self.purchase_order['delivery_address']['country'])

        # Lines
        self.item_no.setText(self.purchase_order['lines'][0]['item_no'])
        self.lines_line_number.setValue(self.purchase_order['lines'][0]['line_no'])
        self.supplier_item_no.setText(self.purchase_order['lines'][0]['supplier_item_no'])
        self.lines_quantity.setValue(self.purchase_order['lines'][0]['quantity'])
        self.lines_quantity_accepted.setValue(self.purchase_order['lines'][0]['quantity_accepted'])
        self.lines_quantity_dispatched.setValue(self.purchase_order['lines'][0]['quantity_dispatched'])
        self.lines_quantity_received.setValue(self.purchase_order['lines'][0]['quantity_received'])
        self.units.setText(self.purchase_order['lines'][0]['units'])
        self.lines_gross_price.setValue(self.purchase_order['lines'][0]['gross_price'])
        self.lines_tax_percentage.setValue(self.purchase_order['lines'][0]['tax_percentage'])
        self.lines_gross_amount.setValue(self.purchase_order['lines'][0]['gross_amount'])
        self.lines_tax_amount.setValue(self.purchase_order['lines'][0]['tax_amount'])
        self.lines_total_amount.setValue(self.purchase_order['lines'][0]['total_amount'])
        self.confirmed_delivery_from.setText(self.purchase_order['lines'][0]['confirmed_delivery_from'])
        self.confirmed_delivery_to.setText(self.purchase_order['lines'][0]['confirmed_delivery_to'])


class PurchaseOrdersWidget(QStackedWidget):
    def __init__(self, trademax_api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/purchase_orders_stackedwidget.ui', self)
        self.trademax_api = trademax_api

        self.purchase_orders = self.trademax_api.get_all_purchase_orders()
        self.purchase_order_id = ''

        self.set_intial_list_data()
        self.btn_open.clicked.connect(self.open_purchase_order)

    def go_to_purchase_order_page(self):
        self.setCurrentIndex(1)

    def set_intial_list_data(self):
        for p in self.purchase_orders:
            self.purchase_orders_list.addItem(QListWidgetItem(p['purchase_order_id']))

    def open_purchase_order(self):
        # somewhere here I think we have to run the acknowledge the order (or maybe when we are
        # viewing the order details
        self.purchase_order_id = self.purchase_orders_list.currentItem().text()

        self.purchase_order_widget = PurchaseOrderWidget(self.trademax_api, self.purchase_order_id)
        self.addWidget(self.purchase_order_widget)

        self.go_to_purchase_order_page()


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('view/main_view_stackedwidget.ui', self)
        self.trademax_api = TrademaxAPI()

        # Adding widgets to the StackedWidget
        self.purchase_orders_widget = PurchaseOrdersWidget(self.trademax_api)
        self.addWidget(self.purchase_orders_widget)

        self.about_widget = AboutWidget()
        self.addWidget(self.about_widget)

        # Event listeners
        self.btn_purchase_orders.clicked.connect(self.go_to_purchase_orders_page)
        self.btn_about.clicked.connect(self.go_to_about_page)

    def go_to_purchase_orders_page(self):
        self.setCurrentIndex(1)

    def go_to_about_page(self):
        self.setCurrentIndex(2)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
