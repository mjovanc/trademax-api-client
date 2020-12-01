from PyQt5.QtWidgets import QMessageBox


class Popup:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def show(self):
        """Displays a popup."""
        msg = QMessageBox()
        msg.setWindowTitle(self.title)
        msg.setText(self.text)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
