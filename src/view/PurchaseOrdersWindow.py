from configparser import ConfigParser

from PyQt5 import uic
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QWidget, QGridLayout, QListView, QAbstractItemView, QPushButton, QListWidgetItem

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
        self.setWindowTitle(parser.get('default', 'window_title'))

        # Windows
        self.window_purchase_order = None

        self.trademax_api = TrademaxAPI()

        for x in self.trademax_api.get_all_purchase_orders():
            self.listwidget_purchase_orders.addItem(QListWidgetItem(x['id']))

        # Event listeners
        self.btn_open.clicked.connect(self.open_purchase_order)

    def toggle_purchase_order_window(self, checked):
        self.purchase_order_id = self.listwidget_purchase_orders.currentItem().text()
        self.window_purchase_order = PurchaseOrderWindow(self.purchase_order_id)
        self.toggle_purchase_order_window()

        if self.window_purchase_order.isVisible():
            self.window_purchase_order.hide()
        else:
            self.window_purchase_order.show()
