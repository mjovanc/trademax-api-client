import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui')
UI_FILE = os.path.join(UI_DIR, 'widget_about.ui')


class AboutWidget(QWidget):
    """
    Displays the About Widget.
    """
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi(UI_FILE, self)

        # Event listeners
        self.btn_back.clicked.connect(self.parent().go_to_start)
