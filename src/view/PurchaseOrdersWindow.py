from configparser import ConfigParser

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QListWidgetItem

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
        for x in self.trademax_api.get_all_purchase_orders():
            self.listwidget_purchase_orders.addItem(QListWidgetItem(x['id']))

        # Event listeners
        self.btn_open.clicked.connect(self.toggle_purchase_order_window)
        self.btn_acknowledge.clicked.connect(self.acknowledge_purchase_order)
        self.btn_reject.clicked.connect(self.reject_purchase_order)

    def toggle_purchase_order_window(self, checked):
        self.purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
        self.window_purchase_order = PurchaseOrderWindow(self.purchase_order_id)

        if self.window_purchase_order.isVisible():
            self.window_purchase_order.hide()
        else:
            self.window_purchase_order.show()

    def acknowledge_purchase_order(self):
        """
        Acknowledge a selected Purchase Order.
        """
        self.purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
        self.trademax_api.post_purchase_order_acknowledgement(self.purchase_order_id)

    def reject_purchase_order(self):
        """
        Rejects a selected Purchase Order.
        """
        self.purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
        # Do not work at the moment, need to implement a reject method in Trademax API
        # self.trademax_api.post_reject_purchase_order(self.purchase_order_id)

