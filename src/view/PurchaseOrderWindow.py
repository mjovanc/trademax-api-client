from configparser import ConfigParser

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

parser = ConfigParser()
parser.read('settings.ini')

qt_creator_file = 'view/ui/window_purchase_order.ui'
UIWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class PurchaseOrderWindow(QWidget, UIWindow):
    def __init__(self, purchase_order_id):
        super().__init__()
        UIWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(parser.get('default', 'WINDOW_TITLE'))

        self.order_id = self.label_order_id.text()
        self.label_order_id.setText(self.order_id + purchase_order_id)
