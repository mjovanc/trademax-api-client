import datetime
import os
from configparser import ConfigParser

import pytz
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from utils.shipping_agent import ShippingAgent

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parser = ConfigParser()
parser.read(os.path.join(BASE_DIR, 'settings.ini'), )


class DispatchWidget(QWidget):
    """
    Displays a Dispatch Window.
    """
    def __init__(self, parent, po_id, trademax_api):
        super().__init__(parent)
        uic.loadUi('view/ui/widget_dispatch.ui', self)
        self.parent = parent
        self.po_id = po_id
        self.trademax_api = trademax_api
        self.po_obj = trademax_api.get_purchase_order(self.po_id)[0]
        self.dt_format = 'yyyy-MM-ddThh:mm:ss'
        self.dt_dispatch_date = ''
        self.dt_delivery_date = ''
        self.dispatch_lines = self.generate_dispatch_lines(self.po_obj['lines'])

        # Event listeners
        self.btn_dispatch.clicked.connect(self.dispatch_order)
        self.btn_close.clicked.connect(lambda: parent.close())

        self.set_form_data()

    def set_form_data(self):
        """Sets the data in the fields in the QWidget."""
        self.lineedit_po_id.setText(self.po_id)
        self.lineedit_po_external_reference.setText(parser.get('api', 'API_UNIQUE_REFERENCE'))

        for data in ShippingAgent:
            self.combobox_shipping_agent.addItem(data.value)

        # Lines Tab
        self.tablewidget_lines.setColumnCount(4)
        self.tablewidget_lines.setHorizontalHeaderLabels(
            [self.tr('Supplier Item Number'), self.tr('Line Number'),
             self.tr('Quantity'), self.tr('Quantity Outstanding')])

        # Adding table rows
        for line in self.dispatch_lines:
            self.add_table_row(self.tablewidget_lines, dict(line))

    def dispatch_order(self):
        """Dispatch the order."""

        # TODO: Need to add validation here
        dispatch_address = {
            'name': self.lineedit_po_da_name, 'phone': self.lineedit_po_da_phone,
            'address': self.lineedit_po_da_address, 'postcode': self.lineedit_po_da_postcode,
            'city': self.lineedit_po_da_city, 'country': self.lineedit_po_da_country,
            'email': self.lineedit_po_da_email, 'country_code': self.lineedit_po_da_countrycode,
        }

        self.trademax_api.post_purchase_order_dispatch(
             self.po_obj['id'], self.dt_dispatch_date,
             self.dt_delivery_date, self.dispatch_lines,
             self.lineedit_po_external_reference.text(), self.lineedit_po_carrier_reference.text(),
             self.combobox_shipping_agent.currentText(), self.lineedit_shipping_agent_service.text(),
             self.lineedit_po_tracking_code.text(), dispatch_address)

        # Open invoice widget
        self.parent.go_to_invoice()

    def format_datetime(self):
        """
        Formats QDateTimeEdit fields to strings.
        Is used for preparing data to send through API.
        """
        dt_dispatch_date = self.datetimeedit_dispatch_date.dateTime().toString(self.dt_format)
        dt_delivery_date = self.datetimeedit_delivery_date.dateTime().toString(self.dt_format)

        now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
        utc = now.strftime("%z")
        self.dt_dispatch_date = dt_dispatch_date + utc
        self.dt_delivery_date = dt_delivery_date + utc

    def generate_dispatch_lines(self, lines):
        """Generates a new lines list."""
        new_lines = []
        for line in lines:
            print(line)
            new_line = {'supplier_item_no': line['supplier_item_no'], 'line_no': line['line_no'],
                        'quantity': line['quantity'], 'quantity_outstanding': 0}
            new_lines.append(new_line)
        return new_lines

    def add_table_row(self, table, row_data):
        """Adding table rows."""
        row = table.rowCount()
        table.setRowCount(row + 1)
        col = 0
        for item in row_data.values():
            cell = QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1
