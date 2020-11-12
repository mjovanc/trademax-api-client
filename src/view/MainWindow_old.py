import sys
import datetime
import pytz as pytz
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QUrl
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QWidget, QStackedWidget, QApplication
from requests import HTTPError

import logging
logging.basicConfig(level=logging.CRITICAL, filename='critical_errors.log')

from model.TrademaxAPI import TrademaxAPI


class AboutWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/about_widget.ui', self)

        self.btn_linkedin.setIcon(QIcon('../../resources/linkedin.png'))

        self.btn_linkedin.clicked.connect(self.open_browser_linkedin)
        self.btn_github.clicked.connect(self.open_browser_github)
        self.btn_facebook.clicked.connect(self.open_browser_facebook)
        self.btn_back.clicked.connect(self.go_back)

    def open_browser_linkedin(self):
        url = QUrl('https://www.linkedin.com/in/marcuscvjeticanin/')
        QDesktopServices.openUrl(url)

    def open_browser_github(self):
        url = QUrl('https://github.com/mjovanc')
        QDesktopServices.openUrl(url)

    def open_browser_facebook(self):
        url = QUrl('https://www.facebook.com/mjovanc')
        QDesktopServices.openUrl(url)


class PurchaseOrderWidget(QStackedWidget):
    def __init__(self, trademax_api, purchase_order_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/purchase_order_widget.ui', self)
        self.trademax_api = trademax_api
        self.order = self.trademax_api.get_purchase_order(purchase_order_id)
        self.purchase_order = self.order[0]
        print(self.purchase_order)

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
        uic.loadUi('view/purchase_orders_widget.ui', self)

        # Use TrademaxAPI object
        self.trademax_api = trademax_api
        self.purchase_orders = self.trademax_api.get_all_purchase_orders()
        self.purchase_order_id = ''

        # Will use this later
        # Use the worker
        # self.thread = QThread(self)
        # self.worker = Worker()
        # self.worker.moveToThread(self.thread)  # worker will be runned in another thread
        # self.worker.done.connect(self.acknowledge_purchase_orders)  # Call load_data_to_tree when worker.done is emitted
        # self.thread.started.connect(self.worker.doWork)  # Call worker.doWork when the thread starts

        # Initialize the list data
        self.set_intial_list_data()
        self.btn_open.clicked.connect(self.open_purchase_order)
        self.btn_acknowledge_all_purchase_orders.clicked.connect(self.acknowledge_purchase_orders)

    def go_to_purchase_order_page(self):
        self.setCurrentIndex(1)

    def set_intial_list_data(self):
        for p in self.purchase_orders:
            self.purchase_orders_list.addItem(QListWidgetItem(p['purchase_order_id']))

    def acknowledge_purchase_orders(self):
        now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))

        for p in self.purchase_orders:
            if p['acknowledged_at'] is None:
                x = self.trademax_api.post_purchase_order_acknowledgement(
                    p['purchase_order_id'],
                    now.strftime("%Y-%m-%dT%H:%M:%S%z"))

        #self.show_popup('Purchase Orders Acknowledged',
        #                'All purchase orders were acknowledged without any problems.')

        testing = self.trademax_api.get_all_purchase_orders()
        for p in testing:
            print(p['acknowledged_at'])

    def open_purchase_order(self):
        self.purchase_order_id = self.purchase_orders_list.currentItem().text()
        self.purchase_order_widget = PurchaseOrderWidget(self.trademax_api, self.purchase_order_id)
        self.addWidget(self.purchase_order_widget)
        self.go_to_purchase_order_page()

    def show_popup(self, title, text):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('view/main_view_stackedwidget.ui', self)

        # Try if the request fails against the API
        try:
            self.trademax_api = TrademaxAPI()
            self.purchase_orders_widget = PurchaseOrdersWidget(self.trademax_api)
            self.addWidget(self.purchase_orders_widget)
        except HTTPError as e:
            # Adding a dummy QWidget to keep the index correct
            self.addWidget(QWidget())

            # Set the Purchase Order button inactive
            self.btn_purchase_orders.setEnabled(False)

            # Adding logging
            now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
            date_and_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            logging.critical('{0}: {1}'.format(date_and_time, e))

        # Adding widgets
        self.about_widget = AboutWidget()
        self.addWidget(self.about_widget)

        # Event listeners
        self.btn_purchase_orders.clicked.connect(self.go_to_purchase_orders_page)
        self.btn_about.clicked.connect(self.go_to_about_page)

    def go_to_purchase_orders_page(self):
        self.setCurrentIndex(1)

    def go_to_about_page(self):
        self.setCurrentIndex(2)

# Look over this if this should be here
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
