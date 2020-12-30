import os
import sys

from PyQt5 import QtWidgets, QtCore

from view.main_window import MainWindow

BASE_DIR = os.path.abspath('..')
LOCALES_FILE = os.path.join(os.path.join(BASE_DIR, 'locales'), 'tr_sv')


def main():
    """Starting point of application."""
    app = QtWidgets.QApplication(sys.argv)

    # Internationalization
    translator = QtCore.QTranslator(app)
    translator.load(LOCALES_FILE, os.path.dirname(__file__))
    app.installTranslator(translator)

    # Initializing the MainWindow
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
