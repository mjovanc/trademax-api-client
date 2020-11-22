from configparser import ConfigParser
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

parser = ConfigParser()
parser.read('settings.ini')


class DispatchWindow(QWidget):
    """
    Displays a Dispatch Window.
    """

    def __init__(self, po_obj):
        super().__init__()
        uic.loadUi('view/ui/window_dispatch.ui', self)
