import sys

from PyQt5 import QtWidgets

from view.MainWindow import Window


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

