import sys

from PyQt5 import QtWidgets, QtGui


from src.view import MainWindow
from src.app_state import AppState
from config.path import ICON_PATH


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app_state = AppState()

    app.setWindowIcon(QtGui.QIcon(ICON_PATH))

    ui = MainWindow(app_state)
    ui.show()
    sys.exit(app.exec_())
