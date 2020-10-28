from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from model.TrademaxAPI import TrademaxAPI


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.setGeometry(300, 300, 600, 400)
        # self.setWindowTitle("Trademax API Client")
        # self.show()

        exit(1)  # just to escape the loop (temporary)


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())

