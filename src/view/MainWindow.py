from configparser import ConfigParser

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from view.AboutWindow import AboutWindow
from view.PurchaseOrdersWindow import PurchaseOrdersWindow

parser = ConfigParser()
parser.read('settings.ini')


class MainWindow(QMainWindow):
    """
    Displays the Main Window.
    """

    def __init__(self):
        super().__init__()
        uic.loadUi('view/ui/window_main.ui', self)

        self.setWindowTitle(parser.get('default', 'window_title'))

        # Windows
        self.window_purchase_orders = PurchaseOrdersWindow(self)
        self.window_about = AboutWindow(self)

        # Stacked widgets
        self.widget_po = self.stackedwidget.addWidget(self.window_purchase_orders)
        self.widget_about = self.stackedwidget.addWidget(self.window_about)

        # Event listeners
        self.btn_purchase_orders.clicked.connect(self.go_to_purchase_orders)
        self.btn_about.clicked.connect(self.go_to_about)

    def go_to_start(self):
        self.stackedwidget.setCurrentIndex(0)

    def go_to_purchase_orders(self):
        self.stackedwidget.setCurrentIndex(self.widget_po)

    def go_to_about(self):
        self.stackedwidget.setCurrentIndex(self.widget_about)





    # def toggle_about_window(self, checked):
    #     """Toggles the about window."""
    #     if self.window_about.isVisible():
    #         self.window_about.hide()
    #     else:
    #         self.window_about.show()
    #
    # def toggle_purchase_orders_window(self, checked):
    #     """Toggles the purchase order window."""
    #     if self.window_purchase_orders.isVisible():
    #         self.window_purchase_orders.hide()
    #     else:
    #         self.window_purchase_orders.show()


