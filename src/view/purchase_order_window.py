import datetime
import os
from configparser import ConfigParser

import pytz
from PyQt5 import uic
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from requests import HTTPError

from utils.logging import add_logging_critical
from utils.status import Status
from view.dispatch_widget import DispatchWidget
from view.invoice_widget import InvoiceWidget
from view.popup import Popup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UI_FILE = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui'), 'window_purchase_order.ui')

parser = ConfigParser()
parser.read(os.path.join(BASE_DIR, 'settings.ini'),)


class PurchaseOrderWindow(QWidget):
    """Displays a Purchase Order Window."""

    def __init__(self, trademax_api, po_obj):
        super().__init__()
        uic.loadUi(UI_FILE, self)
        self.trademax_api = trademax_api
        self.po_id = po_obj.id
        self.po_obj = self.trademax_api.get_purchase_order(self.po_id)[0]
        self.dt_format = 'yyyy-MM-ddThh:mm:ss'
        self.dt_created_at = ''
        self.dt_requested_delivery_from = ''
        self.dt_requested_delivery_to = ''

        # Setting Window Title
        window_title = '{0} - {1}'.format(parser.get('default', 'WINDOW_TITLE'),
                                          self.tr('Purchase Order'))
        self.setWindowTitle(window_title)

        # Set the order ID in label
        self.order_id = self.label_order_id.text()
        self.label_order_id.setText(self.order_id + self.po_id)

        # Widgets
        self.widget_dispatch_order = DispatchWidget(self, self.po_id, self.trademax_api)
        self.widget_create_invoice = InvoiceWidget(self, self.po_id, self.trademax_api)

        # Stacked widgets
        self.widget_dispatch = self.stackedwidget.addWidget(self.widget_dispatch_order)
        self.widget_invoice = self.stackedwidget.addWidget(self.widget_create_invoice)

        # Event listeners
        self.btn_reject.clicked.connect(self.reject_order)
        self.btn_accept_corrections.clicked.connect(self.accept_order_corrections)
        self.btn_accept.clicked.connect(self.accept_order)

        self.set_form_data()

    def set_form_data(self):
        """Sets the data in the fields in the QWidget."""

        # General tab
        self.lineedit_po_id.setText(self.po_obj['purchase_order_id'])

        # Adding datetime from the Purchase Order
        if self.po_obj['created_at'] is not None:
            date_time = self.po_obj['created_at'].split('+', 1)[0]
            date_time_obj = QDateTime.fromString(date_time, self.dt_format)
            self.datetimeedit_created_at.setDateTime(date_time_obj)

        if self.po_obj['requested_delivery_from'] is not None:
            date_time = self.po_obj['requested_delivery_from'].split('+', 1)[0]
            date_time_obj = QDateTime.fromString(date_time, self.dt_format)
            self.datetimeedit_requested_delivery_from.setDateTime(date_time_obj)

        if self.po_obj['requested_delivery_to'] is not None:
            date_time = self.po_obj['requested_delivery_to'].split('+', 1)[0]
            date_time_obj = QDateTime.fromString(date_time, self.dt_format)
            self.datetimeedit_requested_delivery_to.setDateTime(date_time_obj)

        self.lineedit_po_currency.setText(self.po_obj['currency'])
        self.doublespinbox_po_gross_amount.setValue(self.po_obj['gross_amount'])
        self.doublespinbox_po_tax_amount.setValue(self.po_obj['tax_amount'])
        self.doublespinbox_po_total_amount.setValue(self.po_obj['total_amount'])
        self.checkbox_po_partial_delivery.setChecked(self.po_obj['is_partial_delivery'])

        # Sales Order Tab
        if self.po_obj['sales_order'] is not None:
            self.lineedit_po_so_id.setText(self.po_obj['sales_order']['id'])
            self.lineedit_po_so_channel.setText(self.po_obj['sales_order']['channel'])
            self.lineedit_po_so_tentant.setText(self.po_obj['sales_order']['tenant'])

        # Delivery Address Tab
        if self.po_obj['delivery_address'] is not None:
            self.lineedit_po_da_name.setText(self.po_obj['delivery_address']['name'])
            self.lineedit_po_da_phone.setText(self.po_obj['delivery_address']['phone'])
            self.lineedit_po_da_email.setText(self.po_obj['delivery_address']['email'])
            self.lineedit_po_da_address.setText(self.po_obj['delivery_address']['address'])
            self.lineedit_po_da_postcode.setText(self.po_obj['delivery_address']['postcode'])
            self.lineedit_po_da_city.setText(self.po_obj['delivery_address']['city'])
            self.lineedit_po_da_countrycode.setText(self.po_obj['delivery_address']['country_code'])
            self.lineedit_po_da_country.setText(self.po_obj['delivery_address']['country'])

        # Supplier Tab
        if self.po_obj['supplier'] is not None:
            self.lineedit_po_s_supplierid.setText(self.po_obj['supplier']['supplier_id'])
            self.lineedit_po_s_name.setText(self.po_obj['supplier']['name'])

        # Lines Tab
        self.tablewidget_lines.setColumnCount(15)
        self.tablewidget_lines.setHorizontalHeaderLabels(
            [self.tr('Item Number'), self.tr('Supplier Item Number'), self.tr('Line Number'),
             self.tr('Quantity'), self.tr('Quantity Accepted'), self.tr('Quantity Dispatched'),
             self.tr('Quantity Received'), self.tr('Units'), self.tr('Gross Price'),
             self.tr('Tax %'), self.tr('Gross Amount'), self.tr('Tax Amount'), self.tr('Total Amount'),
             self.tr('Confirmed Delivery From'), self.tr('Confirmed Delivery To')])

        # Adding table rows
        for line in self.po_obj['lines']:
            self.add_table_row(self.tablewidget_lines, dict(line))

    def reject_order(self):
        """Rejects a Purchase Order."""
        try:
            # Send a rejected response to Trademax API of the Purchase Order
            self.trademax_api.post_purchase_order_acknowledgement(self.po_id)
            self.trademax_api.post_purchase_order_response(
                self.po_obj['id'], Status.REJECTED.value, 'Rejected.',
                parser.get('api', 'API_UNIQUE_REFERENCE'), self.po_obj['gross_amount'],
                self.po_obj['tax_amount'], self.po_obj['total_amount'],
                self.po_obj['requested_delivery_from'], self.po_obj['requested_delivery_to'],
                self.po_obj['lines'])

            popup = Popup(self.tr('Purchase Order Rejected'),
                          self.tr('The purchase order is now rejected.'))
            popup.show()
        except HTTPError:
            popup = Popup(self.tr('Could not send response to Trademax'),
                          self.tr('The purchase order could not be updated. '
                                  'Contact Trademax or the Developer of the application.'))
            popup.show()
            add_logging_critical()

    def accept_order_corrections(self):
        """Accepts a Purchase Order with corrected information."""
        self.format_datetime()

        # Setting the set datetime to all lines to be the same
        # This could be a feature later on to be able to edit line specific datetime
        for line in self.po_obj['lines']:
            if line['confirmed_delivery_from'] is None:
                line['confirmed_delivery_from'] = self.dt_requested_delivery_from
            if line['confirmed_delivery_to'] is None:
                line['confirmed_delivery_to'] = self.dt_requested_delivery_to

        try:
            # Send a rejected response to Trademax API of the Purchase Order
            # Currently lines is not editable - Feature request
            self.trademax_api.post_purchase_order_acknowledgement(self.po_id)
            self.trademax_api.post_purchase_order_response(
                self.po_obj['id'], Status.CORRECTED.value, 'Corrected.',
                parser.get('api', 'API_UNIQUE_REFERENCE'), self.doublespinbox_po_gross_amount.value(),
                self.doublespinbox_po_tax_amount.value(), self.doublespinbox_po_total_amount.value(),
                self.dt_requested_delivery_from, self.dt_requested_delivery_to,
                self.po_obj['lines'])

            popup = Popup(self.tr('Purchase Order Accepted'),
                          self.tr('The purchase order is now accepted with some corrections.'))
            popup.show()

            # Opens up dispatch widget
            self.go_to_dispatch()
        except HTTPError:
            popup = Popup(self.tr('Could not send response to Trademax'),
                          self.tr('The purchase order could not be updated. '
                                  'Contact Trademax or the Developer of the application.'))
            popup.show()
            add_logging_critical()

    def accept_order(self):
        """Accepting a Purchase Order."""
        self.format_datetime()

        # Setting datetime on all lines of a purchase order
        for line in self.po_obj['lines']:
            if line['confirmed_delivery_from'] is None:
                line['confirmed_delivery_from'] = self.dt_requested_delivery_from
            if line['confirmed_delivery_to'] is None:
                line['confirmed_delivery_to'] = self.dt_requested_delivery_to

        try:
            # Sends the response to API
            self.trademax_api.post_purchase_order_acknowledgement(self.po_id)
            self.trademax_api.post_purchase_order_response(
                self.po_obj['id'], Status.ACCEPTED.value, 'Accepted.',
                parser.get('api', 'API_UNIQUE_REFERENCE'), self.po_obj['gross_amount'],
                self.po_obj['tax_amount'], self.po_obj['total_amount'],
                self.dt_requested_delivery_from, self.dt_requested_delivery_to)

            popup = Popup(self.tr('Purchase Order Accepted'),
                          self.tr('The purchase order is now accepted.'))
            popup.show()

            # Opens up dispatch widget
            self.go_to_dispatch()
        except HTTPError:
            popup = Popup(self.tr('Could not send response to Trademax'),
                          self.tr('The purchase order could not be updated. '
                                  'Contact Trademax or the Developer of the application.'))
            popup.show()
            add_logging_critical()

    def format_datetime(self):
        """Formats QDateTimeEdit fields to strings.

        Is used for preparing data to send through API.
        """
        dt_created_at = self.datetimeedit_created_at.dateTime().toString(self.dt_format)
        dt_requested_delivery_from = self.datetimeedit_requested_delivery_from.dateTime().toString(self.dt_format)
        dt_requested_delivery_to = self.datetimeedit_requested_delivery_to.dateTime().toString(self.dt_format)

        now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
        utc = now.strftime("%z")
        self.dt_created_at = dt_created_at + utc
        self.dt_requested_delivery_from = dt_requested_delivery_from + utc
        self.dt_requested_delivery_to = dt_requested_delivery_to + utc

    def add_table_row(self, table, row_data):
        """Adding table rows."""
        row = table.rowCount()
        table.setRowCount(row + 1)
        col = 0
        for item in row_data.values():
            cell = QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1

    def go_to_dispatch(self):
        """Go to dispatch widget."""
        window_title = '{0} - {1}'.format(parser.get('default', 'WINDOW_TITLE'),
                                          self.tr('Dispatch Purchase Order'))
        self.setWindowTitle(window_title)
        self.stackedwidget.setCurrentIndex(self.widget_dispatch)

    def go_to_invoice(self):
        """Go to invoice widget."""
        window_title = '{0} - {1}'.format(parser.get('default', 'WINDOW_TITLE'),
                                          self.tr('Create Invoice'))
        self.setWindowTitle(window_title)
        self.stackedwidget.setCurrentIndex(self.widget_invoice)
