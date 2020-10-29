import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget


class PurchaseOrdersWidget(QWidget):
    def __init__(self, parent=None):
        super(PurchaseOrdersWidget, self).__init__(parent)
        uic.loadUi('view/purchase_orders_widget.ui')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('view/main_window.ui', self)

        self.purchaseOrdersWidget = PurchaseOrdersWidget(self)
        self.show()
        self.get_purchase_orders.clicked.connect(self.start_purchase_orders_widget)

    def start_purchase_orders_widget(self):
        self.setWindowTitle(self.windowTitle() + ' - Purchase Orders')
        self.setCentralWidget(self.purchaseOrdersWidget)
        self.show()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

