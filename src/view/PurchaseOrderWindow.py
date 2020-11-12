import datetime
import pytz
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QWidget
from requests import HTTPError
from model.TrademaxAPI import TrademaxAPI

import logging
logging.basicConfig(level=logging.CRITICAL, filename='critical_errors.log')


class TestWidget(QtWidgets.QWidget):
    """
    Widget to display information about the application
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/test_widget.ui', self)


class PurchaseOrderWindow(QtWidgets.QMainWindow):
    """
    The Purchase Order Window.
    """
    WINDOW_TITLE = 'Trademax API Client - Purchase Order'

    def __init__(self, purchase_order_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/purchase_order_window.ui', self)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.stacked_widget = QtWidgets.QStackedWidget()

        print(purchase_order_id)

        try:
            self.trademax_api = TrademaxAPI()
            self.stacked_widget.addWidget(TestWidget())
        except HTTPError as e:
            # Adding a dummy QWidget to keep the index correct
            self.stacked_widget.addWidget(QWidget())

            # Set the Purchase Order button inactive
            self.btn_purchase_orders.setEnabled(False)

            # Adding logging
            now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
            date_and_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            logging.critical('{0}: {1}'.format(date_and_time, e))

        # Event listeners
        self.btn_next.clicked.connect(self.__next_page)
        self.btn_back.clicked.connect(self.__go_back)

        # Setting up layout for switching widgets
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        layout.addWidget(self.btn_next)
        layout.addWidget(self.btn_back)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Adding widgets to the StackedWidget
        self.stacked_widget.addWidget(TestWidget())
        # self.stacked_widget.addWidget(AboutWidget())

        # Setting correct index to start with
        self.stacked_widget.setCurrentIndex(0)

    def __next_page(self):
        """Switches to the next Widget."""
        # could maybe be useful for the purchase orders list page
        idx = self.stacked_widget.currentIndex()
        if idx < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(idx + 1)
        else:
            self.stacked_widget.setCurrentIndex(0)

    def __go_back(self):
        """Switches to previous Widget."""
        idx = self.stacked_widget.currentIndex()
        self.setWindowTitle(self.WINDOW_TITLE)
        if idx > 1:
            idx = idx - 1
            self.stacked_widget.setCurrentIndex(idx)
        else:
            self.btn_back.setEnabled(False)
