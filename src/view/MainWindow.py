import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QWidget, QStackedWidget

from model.TrademaxAPI import TrademaxAPI


class AboutWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/about_widget.ui', self)


class PurchaseOrderWidget(QStackedWidget):
    def __init__(self, trademax_api, purchase_order_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/purchase_order_widget.ui', self)

        self.order = trademax_api.get_purchase_order(purchase_order_id)

        print(self.order[0])

        self.purchase_order_id.setText('Name')


class PurchaseOrdersWidget(QStackedWidget):
    def __init__(self, trademax_api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/purchase_orders_stackedwidget.ui', self)
        self.purchase_orders = trademax_api.get_all_purchase_orders()
        self.purchase_order_id = ''

        self.set_intial_list_data()
        self.btn_open.clicked.connect(self.open_purchase_order)

    def go_to_purchase_order_page(self):
        self.setCurrentIndex(1)

    def set_intial_list_data(self):
        for p in self.purchase_orders:
            self.purchase_orders_list.addItem(QListWidgetItem(p['purchase_order_id']))

    def open_purchase_order(self):
        self.purchase_order_widget = PurchaseOrderWidget(self.trademax_api, self.purchase_order_id)
        self.addWidget(self.purchase_order_widget)

        self.purchase_order_id = self.purchase_orders_list.currentItem().text()
        self.go_to_purchase_order_page()


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('view/main_view_stackedwidget.ui', self)
        self.trademax_api = TrademaxAPI()

        # Adding widgets to the StackedWidget
        self.purchase_orders_widget = PurchaseOrdersWidget(self.trademax_api)
        self.addWidget(self.purchase_orders_widget)

        self.about_widget = AboutWidget()
        self.addWidget(self.about_widget)

        # Event listeners
        self.btn_purchase_orders.clicked.connect(self.go_to_purchase_orders_page)
        self.btn_about.clicked.connect(self.go_to_about_page)

    def go_to_purchase_orders_page(self):
        self.setCurrentIndex(1)

    def go_to_about_page(self):
        self.setCurrentIndex(2)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
