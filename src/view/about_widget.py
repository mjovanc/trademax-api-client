from configparser import ConfigParser

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget

parser = ConfigParser()
parser.read('settings.ini')


class AboutWidget(QWidget):
    """
    Displays the About Widget.
    """

    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('view/ui/widget_about.ui', self)

        # Event listeners
        self.btn_back.clicked.connect(self.parent().go_to_start)


