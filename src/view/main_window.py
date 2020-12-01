import datetime
import logging
import os
import traceback
import pytz

from configparser import ConfigParser
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from requests import HTTPError

from model.trademax_api import TrademaxAPI
from view.about_widget import AboutWidget
from view.purchase_orders_widget import PurchaseOrdersWidget

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parser = ConfigParser()
parser.read(os.path.join(BASE_DIR, 'settings.ini'),)


class MainWindow(QMainWindow):
    """
    Displays the Main Window.
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('view/ui/window_main.ui', self)
        self.setWindowTitle(parser.get('default', 'window_title'))

        try:
            self.trademax_api = TrademaxAPI()
            api_status = self.label_api_status.text()
            self.label_api_status.setText(api_status + self.tr('Online'))
        except (HTTPError, ConnectionError):
            # Sets API status
            api_status = self.label_api_status.text()
            self.label_api_status.setText(api_status + self.tr('Offline'))

            # Adding logging
            now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
            date_and_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            logging.critical('{0}: {1}'.format(date_and_time, traceback.format_exc()))

            # Sets purchase orders button disabled
            self.btn_purchase_orders.setEnabled(False)

        # Widgets
        self.widget_purchase_orders = PurchaseOrdersWidget(self)
        self.widget_about = AboutWidget(self)

        # Stacked widgets
        self.widget_po = self.stackedwidget.addWidget(self.widget_purchase_orders)
        self.widget_about = self.stackedwidget.addWidget(self.widget_about)

        # Event listeners
        self.btn_purchase_orders.clicked.connect(self.go_to_purchase_orders)
        self.btn_about.clicked.connect(self.go_to_about)

    def go_to_start(self):
        """Go to start widget."""
        self.setWindowTitle(parser.get('default', 'WINDOW_TITLE'))
        self.stackedwidget.setCurrentIndex(0)

    def go_to_purchase_orders(self):
        """Go to purchase orders widget."""
        window_title = '{0} - {1}'.format(parser.get('default', 'WINDOW_TITLE'),
                                          self.tr('Purchase Orders'))
        self.setWindowTitle(window_title)
        self.stackedwidget.setCurrentIndex(self.widget_po)

    def go_to_about(self):
        """Go to about widget."""
        window_title = '{0} - {1}'.format(parser.get('default', 'WINDOW_TITLE'),
                                          self.tr('About'))
        self.setWindowTitle(window_title)
        self.stackedwidget.setCurrentIndex(self.widget_about)
