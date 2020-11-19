from configparser import ConfigParser

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QMessageBox

from model.Line import Line
from model.PurchaseOrder import PurchaseOrder
from model.TrademaxAPI import TrademaxAPI
from view.PurchaseOrderWindow import PurchaseOrderWindow

parser = ConfigParser()
parser.read('settings.ini')

qt_creator_file = 'view/ui/window_purchase_orders.ui'
UIWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class PurchaseOrdersWindow(QWidget, UIWindow):
    def __init__(self):
        super().__init__()
        UIWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(parser.get('default', 'WINDOW_TITLE'))

        # Windows
        self.window_purchase_order = None

        # Adding list widgets from API
        self.trademax_api = TrademaxAPI()
        for po in self.trademax_api.get_all_purchase_orders():
            self.listwidget_purchase_orders.addItem(QListWidgetItem(po['id']))

        # Event listeners
        self.btn_open.clicked.connect(self.toggle_purchase_order_window)
        self.btn_acknowledge.clicked.connect(self.acknowledge_purchase_order)
        self.btn_reject.clicked.connect(self.reject_purchase_order)

    def toggle_purchase_order_window(self, checked):
        """Toggles the purchase order window."""
        purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
        purchase_order = self.trademax_api.get_purchase_order(purchase_order_id)
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

        self.window_purchase_order = PurchaseOrderWindow(purchase_order_obj)
        if self.window_purchase_order.isVisible():
            self.window_purchase_order.hide()
        else:
            self.window_purchase_order.show()

    def show_popup(self, title, text):
        """Displays a popup."""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def acknowledge_purchase_order(self):
        """Acknowledge a selected Purchase Order."""
        self.purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
        self.trademax_api.post_purchase_order_acknowledgement(self.purchase_order_id)
        self.show_popup('Purchase Order Acknowledged',
                        'The selected purchase order is now acknowledged.')

    def reject_purchase_order(self):
        """Rejects a selected Purchase Order."""
        self.purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
        # Do not work at the moment
        # post_purchase_order_response should be used
        # self.trademax_api.post_purchase_order_response()

