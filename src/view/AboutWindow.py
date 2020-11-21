from configparser import ConfigParser

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget

parser = ConfigParser()
parser.read('settings.ini')


class AboutWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('view/ui/window_about.ui', self)

        self.setWindowTitle(parser.get('default', 'WINDOW_TITLE') + ' - About')
        self.btn_back.clicked.connect(self.parent().go_to_start)



