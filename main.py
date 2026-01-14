import sys

from PyQt5 import QtWidgets

from src.view import MainWindow
from src.app_state import AppState


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app_state = AppState()

    ui = MainWindow(app_state)
    ui.show()
    sys.exit(app.exec_())
