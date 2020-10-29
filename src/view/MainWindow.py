import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMessageBox, QWidget, QMainWindow, QStackedWidget

from model.TrademaxAPI import TrademaxAPI


class AboutWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/about_widget.ui', self)


class PurchaseOrderWidget(QListWidget):
    def __init__(self, parent=None):
        super(PurchaseOrderWidget, self).__init__(parent)
        uic.loadUi('view/purchase_order_widget.ui')


class PurchaseOrdersWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/purchase_orders_widget.ui', self)
        # self.trademax_api = TrademaxAPI()
        # self.purchase_orders = self.trademax_api.get_all_purchase_orders()
        # self.set_intial_list_data()
        # self.itemClicked.connect(self.open_purchase_order)

    # def set_column_labels(self):
    #     for key, value in self.purchase_orders[0].items():
    #         self.po_data2[str(key)] = []
    #
    # def set_intial_list_data(self):
    #    for p in self.purchase_orders:
    #         self.purchase_orders_widget.addItem(QListWidgetItem(p['purchase_order_id'], self))
    #
    # def open_purchase_order(self, item):
    #     purchase_order_id = item.text()
    #     # change to another scene (class)


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('view/main_view_stackedwidget.ui', self)

        self.purchase_orders_widget = PurchaseOrdersWidget()
        self.addWidget(self.purchase_orders_widget)

        self.about_widget = AboutWidget()
        self.addWidget(self.about_widget)

        self.btn_purchase_orders.clicked.connect(self.go_to_first)
        print(self.btn_purchase_orders)
        self.btn_about.clicked.connect(self.go_to_second)

    def go_to_first(self):
        self.setCurrentIndex(1)

    def go_to_second(self):
        self.setCurrentIndex(2)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
