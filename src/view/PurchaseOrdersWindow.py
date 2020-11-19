from configparser import ConfigParser

from PyQt5 import uic
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QWidget, QGridLayout, QListView, QAbstractItemView, QPushButton

from model.TrademaxAPI import TrademaxAPI

parser = ConfigParser()
parser.read('settings.ini')

qt_creator_file = 'view/ui/window_purchase_orders.ui'
UIWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class PurchaseOrdersWindow(QWidget, UIWindow):
    def __init__(self):
        super().__init__()
        UIWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(parser.get('default', 'window_title'))

        # self.trademax_api = TrademaxAPI()
        # self.purchase_orders_list = []
        #
        # for x in self.trademax_api.get_all_purchase_orders():
        #     self.purchase_orders_list.append(x['id'])

        # self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        self.listview = QListView()  # create listview object
        self.listview.setEditTriggers(QAbstractItemView.NoEditTriggers) # mask double-click edit listview
        self.stringlistmodel = QStringListModel()  # Create stringlistmodel object
        self.stringlistmodel.setStringList(self.purchase_orders_list)  # assign data to model
        self.listview.setModel(self.stringlistmodel)  # Associate view with model
        self.stringlistmodel.dataChanged.connect(self.save)

        # Buttons
        self.btn_open = QPushButton()
        self.btn_open.setText('Open')
        self.btn_acknowledge_all_orders = QPushButton()
        self.btn_acknowledge_all_orders.setText('Acknowledge purchase orders')

        # Event listeners
        # self.btn_open.clicked.connect(self.open_purchase_order)

        layout.addWidget(self.listview, 0, 0)
        layout.addWidget(self.btn_open, 0, 1)
        layout.addWidget(self.btn_acknowledge_all_orders, 1, 1)
        self.setLayout(layout)

    def save(self):
        self.purchase_orders_list = self.stringlistmodel.stringList()