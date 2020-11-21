import os
import sys

from PyQt5 import QtWidgets, QtCore

from view.main_window import MainWindow


def main():
    """Starting point of application."""
    app = QtWidgets.QApplication(sys.argv)
    translator = QtCore.QTranslator(app)
    translator.load('../resources/locales/tr_sv', os.path.dirname(__file__))
    app.installTranslator(translator)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
