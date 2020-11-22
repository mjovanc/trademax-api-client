import datetime
import pytz
import traceback

from configparser import ConfigParser
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from requests import HTTPError

from model.line import Line
from model.purchase_order import PurchaseOrder
from model.trademax_api import TrademaxAPI
from view.dispatch_window import DispatchWindow
from view.invoice_window import InvoiceWindow
from view.popup import Popup
from view.purchase_order_window import PurchaseOrderWindow
from utils.logging import add_logging_critical

parser = ConfigParser()
parser.read('settings.ini')


class PurchaseOrdersWidget(QWidget):
    """
    Displays Purchase Orders Window.
    """

    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('view/ui/widget_purchase_orders.ui', self)

        # Windows
        self.window_purchase_order = None
        self.dispatch_window = None
        self.invoice_window = None

        # Adding list widgets from API
        try:
            self.trademax_api = TrademaxAPI()
            for po in self.trademax_api.get_all_purchase_orders():
                self.listwidget_purchase_orders.addItem(QListWidgetItem(po['id']))

            # Event listeners
            self.btn_open.clicked.connect(self.toggle_purchase_order_window)
            self.btn_acknowledge.clicked.connect(self.acknowledge_purchase_order)
            self.btn_dispatch.clicked.connect(self.toggle_dispatch_window)
            self.btn_invoice.clicked.connect(self.toggle_invoice_window)
            self.btn_back.clicked.connect(self.parent().go_to_start)
        except HTTPError:
            add_logging_critical()

            # Sets buttons disabled
            self.btn_open.setEnabled(False)
            self.btn_acknowledge.setEnabled(False)
            self.btn_dispatch.setEnabled(False)
            self.btn_invoice.setEnabled(False)

    def toggle_purchase_order_window(self, checked):
        """Toggles the purchase order window."""
        try:
            purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
            self.window_purchase_order = PurchaseOrderWindow(self.get_purchase_order(purchase_order_id))

            if self.window_purchase_order.isVisible():
                self.window_purchase_order.hide()
            else:
                self.window_purchase_order.show()
        except AttributeError:
            add_logging_critical()

    def toggle_dispatch_window(self, checked):
        """Toggles the dispatch window."""
        try:
            purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
            self.window_dispatch = DispatchWindow(self.get_purchase_order(purchase_order_id))

            if self.window_dispatch.isVisible():
                self.window_dispatch.hide()
            else:
                self.window_dispatch.show()
        except AttributeError:
            add_logging_critical()

    def toggle_invoice_window(self, checked):
        """Toggles the invoice window."""
        try:
            purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
            self.window_invoice = InvoiceWindow(self.get_purchase_order(purchase_order_id))

            if self.window_invoice.isVisible():
                self.window_invoice.hide()
            else:
                self.window_invoice.show()
        except (AttributeError, HTTPError):
            add_logging_critical()

    def acknowledge_purchase_order(self):
        """Acknowledge a selected Purchase Order."""
        try:
            self.purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
            self.trademax_api.post_purchase_order_acknowledgement(self.purchase_order_id)
            Popup.show(self.tr('Purchase Order Acknowledged'),
                       self.tr('The selected purchase order is now acknowledged.'))
        except AttributeError:
            add_logging_critical()

    def get_purchase_order(self, po_id):
        """Get a PurchaseOrder object by specific ID."""
        purchase_order = self.trademax_api.get_purchase_order(po_id)
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

        return purchase_order_obj
