import sys

from PyQt5 import QtWidgets

from view.MainWindow2 import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

