import datetime
import os
from configparser import ConfigParser

import pytz
from PyQt5 import uic
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from requests import HTTPError

from utils.logging import add_logging_error
from view.popup import Popup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parser = ConfigParser()
parser.read(os.path.join(BASE_DIR, 'settings.ini'),)


class InvoiceWidget(QWidget):
    """
    Displays a Invoice Window.
    """
    def __init__(self, parent, po_id, trademax_api):
        super().__init__(parent)
        uic.loadUi('view/ui/widget_invoice.ui', self)
        self.po_id = po_id
        self.trademax_api = trademax_api
        self.po_obj = trademax_api.get_purchase_order(self.po_id)[0]
        self.invoice_lines = self.generate_invoice_lines(self.po_obj['lines'])
        self.dt_format = 'yyyy-MM-ddThh:mm:ss'
        self.dt_invoice_date = ''
        self.dt_due_date = ''

        # Event listeners
        self.btn_create_invoice.clicked.connect(self.create_invoice)
        self.btn_close.clicked.connect(lambda: parent.close())

        self.set_form_data()

    def set_form_data(self):
        """Sets the data in the fields in the QWidget."""
        self.lineedit_po_id.setText(self.po_id)
        self.lineedit_po_external_reference.setText(parser.get('api', 'API_UNIQUE_REFERENCE'))

        # Setting system datetime to invoice date
        dt_format = 'yyyy-MM-ddThh:mm:ss'
        now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
        date_and_time = now.strftime("%Y-%m-%dT%H:%M:%S")
        dt_obj = QDateTime.fromString(date_and_time, dt_format)
        self.datetimeedit_invoice_date.setDateTime(dt_obj)

        self.doublespinbox_po_gross_amount.setValue(self.po_obj['gross_amount'])
        self.doublespinbox_po_tax_amount.setValue(self.po_obj['tax_amount'])
        self.doublespinbox_po_total_amount.setValue(self.po_obj['total_amount'])

        # Lines Tab
        self.tablewidget_lines.setColumnCount(5)
        self.tablewidget_lines.setHorizontalHeaderLabels(
            [self.tr('Supplier Item Number'), self.tr('Line Number'),
             self.tr('Quantity'), self.tr('Gross Price'), self.tr('Gross Amount')])

        # Adding table rows
        for line in self.invoice_lines:
            self.add_table_row(self.tablewidget_lines, dict(line))

    def create_invoice(self):
        try:
            popup = Popup(self.tr('Invoice created!'),
                          self.tr('An invoice has been created to Trademax.'))
            popup.show()

            self.format_datetime()

            # Sending new invoice through API.
            self.trademax_api.post_purchase_order_invoice(
                self.po_obj['id'], self.invoice_lines, self.lineedit_po_external_reference.text(),
                self.doublespinbox_po_gross_amount.value(), self.doublespinbox_po_total_amount.value(),
                self.doublespinbox_po_tax_amount.value(), self.dt_invoice_date, self.dt_due_date)

            self.btn_create_invoice.setEnabled(False)
        except HTTPError:
            add_logging_error()

    def format_datetime(self):
        dt_invoice_date = self.datetimeedit_invoice_date.dateTime().toString(self.dt_format)
        dt_due_date = self.datetimeedit_due_date.dateTime().toString(self.dt_format)

        now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
        utc = now.strftime("%z")
        self.dt_invoice_date = dt_invoice_date + utc
        self.dt_due_date = dt_due_date + utc

    def generate_invoice_lines(self, lines):
        """Generates a new lines list."""
        new_lines = []
        for line in lines:
            new_line = {'supplier_item_no': line['supplier_item_no'], 'line_no': line['line_no'],
                        'quantity': line['quantity'], 'gross_price': line['gross_price'],
                        'gross_amount': line['gross_amount']}
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
