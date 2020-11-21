import datetime
import pytz
import logging
import traceback

from configparser import ConfigParser
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QMessageBox
from requests import HTTPError

from model.line import Line
from model.purchase_order import PurchaseOrder
from model.trademax_api import TrademaxAPI
from view.popup import Popup
from view.purchase_order_window import PurchaseOrderWindow


logging.basicConfig(level=logging.CRITICAL, filename='critical_errors.log')

parser = ConfigParser()
parser.read('settings.ini')


class PurchaseOrdersWidget(QWidget):
    """
    Displays Purchase Orders Window.
    """

    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('view/ui/window_purchase_orders.ui', self)

        # Windows
        self.window_purchase_order = None

        # Adding list widgets from API
        try:
            self.trademax_api = TrademaxAPI()
            for po in self.trademax_api.get_all_purchase_orders():
                self.listwidget_purchase_orders.addItem(QListWidgetItem(po['id']))
        except HTTPError:
            # Adding logging
            now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
            date_and_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            logging.critical('{0}: {1}'.format(date_and_time, traceback.format_exc()))

            # Sets buttons disabled
            self.btn_open.setEnabled(False)
            self.btn_acknowledge.setEnabled(False)
            self.btn_reject.setEnabled(False)
            self.btn_modify.setEnabled(False)

        # Event listeners
        self.btn_open.clicked.connect(self.toggle_purchase_order_window)
        self.btn_acknowledge.clicked.connect(self.acknowledge_purchase_order)
        self.btn_reject.clicked.connect(self.reject_purchase_order)
        # self.btn_modify.clicked.connect(self.modify_purchase_order)
        self.btn_back.clicked.connect(self.parent().go_to_start)

    def toggle_purchase_order_window(self, checked):
        """Toggles the purchase order window."""
        try:
            purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
            purchase_order = self.trademax_api.get_purchase_order(purchase_order_id)
            purchase_order = purchase_order[0]

            purchase_order_lines = []
            for pol in purchase_order['lines']:
                purchase_order_lines.append(
                    Line(pol['item_no'], pol['supplier_item_no'], pol['line_no'], pol['quantity'],
                         pol['quantity_accepted'], pol['quantity_dispatched'], pol['quantity_received'],
                         pol['units'], pol['gross_price'], pol['tax_percentage'], pol['gross_amount'],
                         pol['tax_amount'], pol['total_amount'], pol['confirmed_delivery_from'],
                         pol['confirmed_delivery_to'])
                )

            purchase_order_obj = PurchaseOrder(
                purchase_order['id'], purchase_order['purchase_order_id'],
                purchase_order['latest'], purchase_order['created_at'],
                purchase_order['acknowledged_at'], purchase_order['requested_delivery_from'],
                purchase_order['requested_delivery_to'], purchase_order['currency'],
                purchase_order['gross_amount'], purchase_order['tax_amount'],
                purchase_order['total_amount'], purchase_order['is_partial_delivery'],
                purchase_order['sales_order'], purchase_order['delivery_address'],
                purchase_order['supplier'], purchase_order_lines
            )

            self.window_purchase_order = PurchaseOrderWindow(purchase_order_obj)
            if self.window_purchase_order.isVisible():
                self.window_purchase_order.hide()
            else:
                self.window_purchase_order.show()
        except AttributeError:
            now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
            date_and_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            logging.critical('{0}: {1}'.format(date_and_time, traceback.format_exc()))

    def acknowledge_purchase_order(self):
        """Acknowledge a selected Purchase Order."""
        try:
            self.purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
            self.trademax_api.post_purchase_order_acknowledgement(self.purchase_order_id)
            Popup.show('Purchase Order Acknowledged',
                            'The selected purchase order is now acknowledged.')
        except AttributeError:
            now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
            date_and_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            logging.critical('{0}: {1}'.format(date_and_time, traceback.format_exc()))

    def reject_purchase_order(self):
        """Rejects a selected Purchase Order."""
        self.purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
        # Do not work at the moment
        # post_purchase_order_response should be used
        # self.trademax_api.post_purchase_order_response()


