from configparser import ConfigParser

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

parser = ConfigParser()
parser.read('settings.ini')

qt_creator_file = 'view/ui/window_purchase_order.ui'
UIWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class PurchaseOrderWindow(QWidget, UIWindow):
    def __init__(self, po_obj):
        super().__init__()
        UIWindow.__init__(self)
        self.setupUi(self)
        self.po_obj = po_obj

        self.setWindowTitle(parser.get('default', 'WINDOW_TITLE'))

        # Set the order ID in label
        self.order_id = self.label_order_id.text()
        self.label_order_id.setText(self.order_id + self.po_obj.purchase_order_id)

        print(self.po_obj.sales_order)

        self.set_form_data()

    def set_form_data(self):
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

        # Lines
        # Make a table here of Line objects
        self.tablewidget_lines.setRowCount(len(self.po_obj.lines))
        self.tablewidget_lines.setColumnCount(2)

        self.setVerticalHeaderLabels(['Item Number', 'Supplier Item Number', "Cycles / ms",
             'RAM access time', 'Execution Time Model'])

        #for row, line in range(self.po_obj.lines):
        #    self.tablewidget_lines.setItem(row, 0, QTableWidgetItem("Cell (1,1)"))



        if self.po_obj.lines is not None:
            print(self.po_obj.lines)
            # self.lineedit_po_lines_item_number.setText(self.po_obj.lines['country'])
            # self.lineedit_po_lines_supplier_item_number.setText(self.po_obj.lines['country'])
            # self.spinbox_po_lines_line_number.setValue(self.po_obj.lines['country'])
            # self.spinbox_po_lines_quantity.setValue(self.po_obj.lines['country'])
            # self.spinbox_po_lines_quantity_accepted.setValue(self.po_obj.lines['country'])
            # self.spinbox_po_lines_quantity_dispatched.setValue(self.po_obj.lines['country'])
            # self.spinbox_po_lines_quantity_recieved.setValue(self.po_obj.lines['country'])
            # self.lineedit_po_lines_units.setText(self.po_obj.lines['country'])
            # self.doublespinbox_po_lines_price.setValue(self.po_obj.lines['country'])
            # self.doublespinbox_po_lines_tax_percentage.setValue(self.po_obj.lines['country'])
            # self.doublespinbox_po_lines_gross_amount.setValue(self.po_obj.lines['country'])
            # self.doublespinbox_po_lines_tax_amount.setValue(self.po_obj.lines['country'])
            # self.doublespinbox_po_lines_total_amount.setValue(self.po_obj.lines['country'])
            # self.lineedit_po_lines_confirmed_delivery_from.setText(self.po_obj.lines['country'])
            # self.lineedit_po_lines_confirmed_delivery_to.setText(self.po_obj.lines['country'])