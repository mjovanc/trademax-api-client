from configparser import ConfigParser

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

parser = ConfigParser()
parser.read('settings.ini')

qt_creator_file = 'view/ui/window_about.ui'
UIWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class AboutWindow(QWidget, UIWindow):
    def __init__(self):
        super().__init__()
        UIWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(parser.get('default', 'WINDOW_TITLE'))
