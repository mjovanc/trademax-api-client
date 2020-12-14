import os
from configparser import ConfigParser
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

        # Event listeners
        self.btn_dispatch.clicked.connect(self.dispatch_order)
        self.btn_close.clicked.connect(lambda: parent.close())

        # TODO: Grab correct format of date, time and timezone and send it to response
        # 2020-10-07T14:10:26+02:00 # correct format we need to grab and send
        # print(self.datetimeedit_delivery_date.dateTime().toString('yyyy-MM-ddTh:mm:ss+zzz'))

        self.set_form_data()

    def set_form_data(self):
        """Sets the data in the fields in the QWidget."""
        self.lineedit_po_id.setText(self.po_id)

        for data in ShippingAgent:
            self.combobox_shipping_agent.addItem(data.value)

    def dispatch_order(self):
        # Dispatch the order with api

        # TODO: Need to add validation here
        dispatch_address = {
            'name': self.lineedit_po_da_name, 'phone': self.lineedit_po_da_phone,
            'address': self.lineedit_po_da_address, 'postcode': self.lineedit_po_da_postcode,
            'city': self.lineedit_po_da_city, 'country': self.lineedit_po_da_country,
            'email': self.lineedit_po_da_email, 'country_code': self.lineedit_po_da_countrycode,
        }

        # TODO: Send the dates here (need to be updated)
        # self.trademax_api.post_purchase_order_dispatch(
        #     self.po_obj['id'], self.lineedit_po_dispatch_date.text(),
        #     self.lineedit_po_delivery_date.text(), self.po_obj['lines'],
        #     self.lineedit_po_external_reference.text(), self.lineedit_po_carrier_reference.text(),
        #     self.lineedit_po_shipping_agent.text(), self.lineedit_po_shipping_agent_service.text(),
        #     self.lineedit_po_tracking_code.text(), dispatch_address)
        self.parent.go_to_invoice()

    def add_table_row(self, table, row_data):
        """Adding table rows."""
        row = table.rowCount()
        table.setRowCount(row + 1)
        col = 0
        for item in row_data.values():
            cell = QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1
