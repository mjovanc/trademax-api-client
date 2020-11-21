from configparser import ConfigParser
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

parser = ConfigParser()
parser.read('settings.ini')


class PurchaseOrderWindow(QWidget):
    """
    Displays a Purchase Order Window.
    """

    def __init__(self, po_obj):
        super().__init__()
        uic.loadUi('view/ui/window_purchase_order.ui', self)
        self.po_obj = po_obj

        # Set the order ID in label
        self.order_id = self.label_order_id.text()
        self.label_order_id.setText(self.order_id + self.po_obj.purchase_order_id)

        self.set_form_data()

    def set_form_data(self):
        """Sets the data in the fields in the QWidget."""

        # General tab
        self.lineedit_po_id.setText(self.po_obj.purchase_order_id)
        self.lineedit_po_created_at.setText(self.po_obj.created_at)
        self.lineedit_po_acknowledged_at.setText(self.po_obj.acknowledged_at)
        self.lineedit_po_requested_delivery_from.setText(self.po_obj.requested_delivery_from)
        self.lineedit_po_requested_delivery_to.setText(self.po_obj.requested_delivery_to)
        self.lineedit_po_currency.setText(self.po_obj.currency)
        self.doublespinbox_po_gross_amount.setValue(self.po_obj.gross_amount)
        self.doublespinbox_po_tax_amount.setValue(self.po_obj.tax_amount)
        self.doublespinbox_po_total_amount.setValue(self.po_obj.total_amount)
        self.checkbox_po_partial_delivery.setChecked(self.po_obj.is_partial_delivery)

        # Sales Order Tab
        if self.po_obj.sales_order is not None:
            self.lineedit_po_so_id.setText(self.po_obj.sales_order['id'])
            self.lineedit_po_so_channel.setText(self.po_obj.sales_order['channel'])
            self.lineedit_po_so_tentant.setText(self.po_obj.sales_order['tenant'])

        # Delivery Address Tab
        if self.po_obj.delivery_address is not None:
            self.lineedit_po_da_name.setText(self.po_obj.delivery_address['name'])
            self.lineedit_po_da_phone.setText(self.po_obj.delivery_address['phone'])
            self.lineedit_po_da_email.setText(self.po_obj.delivery_address['email'])
            self.lineedit_po_da_address.setText(self.po_obj.delivery_address['address'])
            self.lineedit_po_da_postcode.setText(self.po_obj.delivery_address['postcode'])
            self.lineedit_po_da_city.setText(self.po_obj.delivery_address['city'])
            self.lineedit_po_da_countrycode.setText(self.po_obj.delivery_address['country_code'])
            self.lineedit_po_da_country.setText(self.po_obj.delivery_address['country'])

        # Supplier Tab
        if self.po_obj.supplier is not None:
            self.lineedit_po_s_supplierid.setText(self.po_obj.supplier['supplier_id'])
            self.lineedit_po_s_name.setText(self.po_obj.supplier['name'])

        # TODO:Need to translate these labels below!
        # Lines Tab
        self.tablewidget_lines.setColumnCount(15)
        self.tablewidget_lines.setHorizontalHeaderLabels(
            ['Item Number', 'Supplier Item Number', "Line Number",
             'Quantity', 'Quantity Accepted', 'Quantity Dispatched',
             'Quantity Received', 'Units', 'Gross Price',
             'Tax %', 'Gross Amount', 'Tax Amount', 'Total Amount',
             'Confirmed Delivery From', 'Confirmed Delivery To'])

        # Adding table rows
        for line in self.po_obj.lines:
            self.add_table_row(self.tablewidget_lines, dict(line))

    def add_table_row(self, table, row_data):
        """Adding table rows."""
        row = table.rowCount()
        table.setRowCount(row + 1)
        col = 0
        for item in row_data.values():
            cell = QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1
