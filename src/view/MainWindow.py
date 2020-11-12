import datetime
import pytz
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem, QWidget
from requests import HTTPError
from model.TrademaxAPI import TrademaxAPI

import logging

from view.PurchaseOrderWindow import PurchaseOrderWindow

logging.basicConfig(level=logging.CRITICAL, filename='critical_errors.log')


class AboutWidget(QtWidgets.QWidget):
    """
    Widget to display information about the application
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/about_widget.ui', self)

        self.btn_linkedin.setIcon(QIcon('../../resources/linkedin.png'))

        # Event listeners
        self.btn_linkedin.clicked.connect(self.open_browser_linkedin)
        self.btn_github.clicked.connect(self.open_browser_github)
        self.btn_facebook.clicked.connect(self.open_browser_facebook)

    def open_browser_linkedin(self):
        """Opens the LinkedIn link in default browser of OS."""
        url = QUrl('https://www.linkedin.com/in/marcuscvjeticanin/')
        QDesktopServices.openUrl(url)

    def open_browser_github(self):
        """Opens the GitHub link in default browser of OS."""
        url = QUrl('https://github.com/mjovanc')
        QDesktopServices.openUrl(url)

    def open_browser_facebook(self):
        """Opens the Facebook link in default browser of OS."""
        url = QUrl('https://www.facebook.com/mjovanc')
        QDesktopServices.openUrl(url)


class PurchaseOrderWidget(QtWidgets.QWidget):
    """
    Widget to display a single Purchase Order.
    """
    def __init__(self, trademax_api, purchase_order_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/purchase_order_widget.ui', self)
        self.order = trademax_api.get_purchase_order(purchase_order_id)
        self.purchase_order = self.order[0]
        print(self.purchase_order)

        self.set_intial_data()

    def set_intial_data(self):
        """Sets the intial data to the purchase order fields."""
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


class PurchaseOrdersWidget(QtWidgets.QWidget):
    """
    Widget to display the Purchase Orders.
    """
    def __init__(self, trademax_api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/purchase_orders_widget.ui', self)

        # Use TrademaxAPI object
        self.trademax_api = trademax_api
        self.purchase_orders = self.trademax_api.get_all_purchase_orders()
        self.purchase_order_id = ''

        # Initialize the list data
        self.set_intial_list_data()
        self.btn_open.clicked.connect(self.open_purchase_order)
        self.btn_acknowledge_all_purchase_orders.clicked.connect(self.acknowledge_purchase_orders)

    def set_intial_list_data(self):
        """Sets the initial list data of purchase orders."""
        for p in self.purchase_orders:
            self.purchase_orders_list.addItem(QListWidgetItem(p['purchase_order_id']))

    def acknowledge_purchase_orders(self):
        """Acknowledges all the available purchase orders."""
        now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))

        for p in self.purchase_orders:
            if p['acknowledged_at'] is None:
                self.trademax_api.post_purchase_order_acknowledgement(
                    p['purchase_order_id'],
                    now.strftime("%Y-%m-%dT%H:%M:%S%z"))

        # self.show_popup('Purchase Orders Acknowledged',
        #                'All purchase orders were acknowledged without any problems.')

        testing = self.trademax_api.get_all_purchase_orders()
        for p in testing:
            print(p['acknowledged_at'])

    def open_purchase_order(self):
        """Opens a Purchase Order."""
        self.purchase_order_id = self.purchase_orders_list.currentItem().text()

        w = PurchaseOrderWindow(self.purchase_order_id)
        w.show()

    def show_popup(self, title, text):
        """Displays a popup to the user."""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class StartWidget(QtWidgets.QWidget):
    """
    Widget to display starting page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/start_widget.ui', self)


class Window(QtWidgets.QMainWindow):
    """
    The Main Window.
    """
    WINDOW_TITLE = 'Trademax API Client'

    def __init__(self):
        super().__init__()
        uic.loadUi('view/main_window.ui', self)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.stacked_widget = QtWidgets.QStackedWidget()

        try:
            self.trademax_api = TrademaxAPI()
            self.stacked_widget.addWidget(PurchaseOrdersWidget(self.trademax_api))
        except HTTPError as e:
            # Adding a dummy QWidget to keep the index correct
            self.stacked_widget.addWidget(QWidget())

            # Set the Purchase Order button inactive
            self.btn_purchase_orders.setEnabled(False)

            # Adding logging
            now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
            date_and_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            logging.critical('{0}: {1}'.format(date_and_time, e))

        # Event listeners
        self.btn_purchase_orders.clicked.connect(self.__go_to_purchase_orders)
        self.btn_about.clicked.connect(self.__go_to_about)
        self.btn_back.clicked.connect(self.__go_to_start)

        # Setting up layout for switching widgets
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        layout.addWidget(self.btn_purchase_orders)
        layout.addWidget(self.btn_about)
        layout.addWidget(self.btn_back)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Adding widgets to the StackedWidget
        self.stacked_widget.addWidget(StartWidget())
        self.stacked_widget.addWidget(AboutWidget())

        # Setting correct index to start with
        self.stacked_widget.setCurrentIndex(1)

    def __next_page(self):
        """Switches to the next Purchase Order Widget."""
        # could maybe be useful for the purchase orders list page
        idx = self.stacked_widget.currentIndex()
        if idx < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(idx + 1)
        else:
            self.stacked_widget.setCurrentIndex(0)

    def __go_to_purchase_orders(self):
        """Switches to the Purchase Orders Widget."""
        self.setWindowTitle(self.WINDOW_TITLE + ' - ' + self.btn_purchase_orders.text())
        self.stacked_widget.setCurrentIndex(0)

    def __go_to_about(self):
        """Switches to the About Widget."""
        self.setWindowTitle(self.WINDOW_TITLE + ' - ' + self.btn_about.text())
        self.stacked_widget.setCurrentIndex(2)

    def __go_to_start(self):
        """Switches to the Start Widget."""
        self.setWindowTitle(self.WINDOW_TITLE)
        self.stacked_widget.setCurrentIndex(1)


