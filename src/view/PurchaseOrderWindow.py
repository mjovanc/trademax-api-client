from configparser import ConfigParser

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from model.PurchaseOrder import PurchaseOrder
from model.TrademaxAPI import TrademaxAPI

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

        # Delivery Address Tab

        # Supplier Tab

        # Lines