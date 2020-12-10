from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QInputDialog, QLineEdit
from requests import HTTPError

from model.line import Line
from model.purchase_order import PurchaseOrder
from view.dispatch_widget import DispatchWidget
from view.invoice_widget import InvoiceWidget
from view.popup import Popup
from view.purchase_order_window import PurchaseOrderWindow
from utils.logging import add_logging_critical, add_logging_info


class PurchaseOrdersWidget(QWidget):
    """
    Displays Purchase Orders Window.
    """
    def __init__(self, parent, trademax_api):
        super().__init__(parent)
        uic.loadUi('view/ui/widget_purchase_orders.ui', self)
        self.current_page = 1
        self.trademax_api = trademax_api

        # Windows
        self.window_purchase_order = None
        self.dispatch_window = None
        self.invoice_window = None

        # Adding list widgets from API
        try:
            self.populate_purchase_orders_list(page_no=self.current_page)
            self.pushbutton_page_forward.setEnabled(False)

            # Setting number of pages
            self.label_page_no.setText('Page 1/{0}'.format(self.num_pages))

            # Event listeners
            self.btn_open.clicked.connect(self.toggle_purchase_order_window)
            self.btn_open_po_id.clicked.connect(self.open_purchase_order_with_id)
            self.btn_acknowledge.clicked.connect(self.acknowledge_purchase_order)
            self.btn_back.clicked.connect(self.parent().go_to_start)

            self.pushbutton_page_back.clicked.connect(self.go_page_back)
            self.pushbutton_page_forward.clicked.connect(self.go_page_forward)
        except HTTPError:
            add_logging_critical()

            # Sets buttons disabled
            self.btn_open.setEnabled(False)
            self.btn_acknowledge.setEnabled(False)

    def go_page_back(self):
        if self.current_page != self.num_pages:
            self.current_page = self.current_page + 1
            self.populate_purchase_orders_list(page_no=self.current_page)
            self.label_page_no.setText('Page {0}/{1}'.format(self.current_page, self.num_pages))
        else:
            self.pushbutton_page_back.setEnabled(False)

        if self.current_page > 1:
            self.pushbutton_page_forward.setEnabled(True)

    def go_page_forward(self):
        if self.current_page > 1:
            self.current_page = self.current_page - 1
            self.pushbutton_page_forward.setEnabled(True)
        if self.current_page == 1:
            self.pushbutton_page_forward.setEnabled(False)

        self.populate_purchase_orders_list(page_no=self.current_page)
        self.label_page_no.setText('Page {0}/{1}'.format(self.current_page, self.num_pages))

    def populate_purchase_orders_list(self, page_no):
        # Clear the list widget
        self.listwidget_purchase_orders.clear()

        # Load the purchase orders
        self.purchase_orders, self.num_pages = self.trademax_api.get_purchase_orders(page_no)

        # Add purchase orders to list widget
        for po in self.purchase_orders:
            if po['acknowledged_at'] is None:
                item = '{0}'.format(po['id'])
            else:
                item = '{0} | {1}'.format(po['id'], self.tr('Acknowledged'))
            self.listwidget_purchase_orders.addItem(
                QListWidgetItem(item))

    def toggle_purchase_order_window(self, checked):
        """Toggles the purchase order window."""
        try:
            purchase_order_id = self.listwidget_purchase_orders.currentItem().text().split('|')[0]
            self.window_purchase_order = PurchaseOrderWindow(self.trademax_api, purchase_order_id)

            if self.window_purchase_order.isVisible():
                self.window_purchase_order.hide()
            else:
                self.window_purchase_order.show()
        except AttributeError:
            add_logging_critical()

    def toggle_dispatch_window(self, checked):
        """Toggles the dispatch window."""
        try:
            purchase_order_id = self.listwidget_purchase_orders.currentItem().text().split('|')[0]
            self.window_dispatch = DispatchWidget(self.get_purchase_order(purchase_order_id))

            if self.window_dispatch.isVisible():
                self.window_dispatch.hide()
            else:
                self.window_dispatch.show()
        except AttributeError:
            add_logging_critical()

    def open_purchase_order_with_id(self):
        po_id, ok_pressed = QInputDialog.getText(self, self.tr('Open Purchase Order by ID'),
                                                 self.tr('Enter ID:'), QLineEdit.Normal, '')
        if ok_pressed and po_id != '':
            try:
                self.window_purchase_order = PurchaseOrderWindow(self.get_purchase_order(po_id))
                self.window_purchase_order.show()
            except AttributeError:
                add_logging_critical()
            except HTTPError:
                # The HTTPError will most likely be 404 so the logging level is INFO.
                add_logging_info()

    def toggle_invoice_window(self, checked):
        """Toggles the invoice window."""
        try:
            purchase_order_id = self.listwidget_purchase_orders.currentItem().text().split('|')[0]
            self.window_invoice = InvoiceWidget(self.get_purchase_order(purchase_order_id))

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
            popup = Popup(self.tr('Purchase Order Acknowledged'),
                          self.tr('The selected purchase order is now acknowledged.'))
            popup.show()
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
