from configparser import ConfigParser

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

from view.AboutWindow import AboutWindow
from view.PurchaseOrdersWindow import PurchaseOrdersWindow

parser = ConfigParser()
parser.read('settings.ini')

qt_creator_file = 'view/ui/window_main.ui'
UIWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class MainWindow(QMainWindow, UIWindow):
    def __init__(self):
        super().__init__()
        UIWindow.__init__(self)
        self.setupUi(self)

        self.setWindowTitle(parser.get('default', 'window_title'))

        # Windows
        self.window_about = AboutWindow()
        self.window_purchase_orders = PurchaseOrdersWindow()

        # Event listeners
        self.btn_about.clicked.connect(self.toggle_about_window)
        self.btn_purchase_orders.clicked.connect(self.toggle_purchase_orders_window)

    def toggle_about_window(self, checked):
        if self.window_about.isVisible():
            self.window_about.hide()
        else:
            self.window_about.show()

    def toggle_purchase_orders_window(self, checked):
        if self.window_purchase_orders.isVisible():
            self.window_purchase_orders.hide()
        else:
            self.window_purchase_orders.show()
