import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMessageBox

from model.TrademaxAPI import TrademaxAPI

# class AboutWidget(QWidget):
#     def __init__(self, parent=None):
#         super(AboutWidget, self).__init__(parent)
#         uic.loadUi('view/about_widget.ui')


class PurchaseOrderWidget(QListWidget):
    def __init__(self, parent=None):
        super(PurchaseOrderWidget, self).__init__(parent)
        uic.loadUi('view/purchase_order_widget.ui')


class PurchaseOrdersWidget(QListWidget):
    def __init__(self, parent=None):
        super(PurchaseOrdersWidget, self).__init__(parent)
        uic.loadUi('view/purchase_orders_widget.ui')
        self.trademax_api = TrademaxAPI()
        self.set_intial_list_data()

        self.itemClicked.connect(self.open_purchase_order)

    def set_column_labels(self):
        po = self.trademax_api.get_all_purchase_orders()
        for key, value in po[0].items():
            self.po_data2[str(key)] = []

    def set_intial_list_data(self):
        po = self.trademax_api.get_all_purchase_orders()
        for p in po:
            self.addItem(QListWidgetItem(p['purchase_order_id'], self))

    def open_purchase_order(self, item):
        purchase_order_id = item.text()





class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/main_window.ui', self)
        self.show()
        self.btn_purchase_orders.clicked.connect(self.start_purchase_orders_widget)

    def start_purchase_orders_widget(self):
        self.setWindowTitle(self.windowTitle() + ' - Inköpsordrar')
        self.purchaseOrdersWidget = PurchaseOrdersWidget(self)
        self.setCentralWidget(self.purchaseOrdersWidget)
        self.show()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
