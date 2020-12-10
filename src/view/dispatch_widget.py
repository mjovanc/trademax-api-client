import os
from configparser import ConfigParser
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parser = ConfigParser()
parser.read(os.path.join(BASE_DIR, 'settings.ini'),)


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

        self.set_form_data()

    def set_form_data(self):
        """Sets the data in the fields in the QWidget."""
        pass

    def dispatch_order(self):
        # Dispatch the order with api
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