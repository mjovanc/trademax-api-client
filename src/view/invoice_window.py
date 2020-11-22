from configparser import ConfigParser
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

parser = ConfigParser()
parser.read('settings.ini')


class InvoiceWindow(QWidget):
    """
    Displays a Invoice Window.
    """

    def __init__(self, po_obj):
        super().__init__()
        uic.loadUi('view/ui/window_invoice.ui', self)
