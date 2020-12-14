import os
from configparser import ConfigParser
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

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
        # self.po_obj = trademax_a

        # Event listeners
        self.btn_create_invoice.clicked.connect(self.create_invoice)
        self.btn_close.clicked.connect(lambda: parent.close())

        self.set_form_data()

    def set_form_data(self):
        """Sets the data in the fields in the QWidget."""
        self.lineedit_po_id.setText(self.po_id)

        # TODO: Set invoice date here automatically based on system time (due date, manually)

        # Lines Tab
        self.tablewidget_lines.setColumnCount(5)
        self.tablewidget_lines.setHorizontalHeaderLabels(
            [self.tr('Supplier Item Number'), self.tr('Line Number'),
             self.tr('Quantity'), self.tr('Gross Price'), self.tr('Gross Amount')])

        # Adding table rows
        #for line in self.po_obj['lines']:
        #    self.add_table_row(self.tablewidget_lines, dict(line))

    def create_invoice(self):
        popup = Popup(self.tr('Invoice created!'),
                      self.tr('An invoice has been created to Trademax.'))
        popup.show()
        self.btn_create_invoice.setEnabled(False)

    def add_table_row(self, table, row_data):
        """Adding table rows."""
        row = table.rowCount()
        table.setRowCount(row + 1)
        col = 0
        for item in row_data.values():
            cell = QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1
