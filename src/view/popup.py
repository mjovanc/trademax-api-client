from PyQt5.QtWidgets import QMessageBox


class Popup:
    def show(self, title, text):
        """Displays a popup."""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
