from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from model.TrademaxAPI import TrademaxAPI


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.setGeometry(300, 300, 600, 400)
        # self.setWindowTitle("Trademax API Client")
        # self.show()

        t = TrademaxAPI()

        # Get one purchase order
        po = t.get_purchase_order('IO1833064')

        # Acknowledge one purchase order
        t.post_purchase_order_acknowledgement('IO1833064', 'datum här')

        # Response of purchase order

        # Dispatch purchase order


        exit(1)  # just to escape the loop (temporary)


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())

