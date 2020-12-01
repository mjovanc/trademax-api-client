import os
from configparser import ConfigParser
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parser = ConfigParser()
parser.read(os.path.join(BASE_DIR, 'settings.ini'),)


class InvoiceWindow(QWidget):
    """
    Displays a Invoice Window.
    """
    def __init__(self, po_obj):
        super().__init__()
        uic.loadUi('view/ui/window_invoice.ui', self)
