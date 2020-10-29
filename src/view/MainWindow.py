import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidget

# class AboutWidget(QWidget):
#     def __init__(self, parent=None):
#         super(AboutWidget, self).__init__(parent)
#         uic.loadUi('view/about_widget.ui')

data = {'col1': ['1', '2', '3', '4'],
        'col2': ['1', '2', '1', '3'],
        'col3': ['1', '1', '2', '1']}


class PurchaseOrdersWidget(QTableWidget):
    def __init__(self, parent=None):
        super(PurchaseOrdersWidget, self).__init__(parent)
        uic.loadUi('view/purchase_orders_widget.ui')
        self.data = data
        self.setColumnCount(len(self.data.keys()))
        self.setRowCount(len(self.data.values()))
        # self.setHorizontalHeaderLabels()
        self.set_data()

    def set_data(self):
        hor_headers = []
        # hor_headers_labels = [] will load dynamically this when getting latest purchase orders

        for n, key in enumerate(sorted(self.data.keys())):
            hor_headers.append(key)
            for m, item in enumerate(self.data[key]):
                new_item = QTableWidgetItem(item)
                self.setItem(m, n, new_item)
        self.setHorizontalHeaderLabels(hor_headers)


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
