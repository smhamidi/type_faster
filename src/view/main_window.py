from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon

from src.util import init_screen_size
from src import AppState
from src.controller.main_window import Controller
from config.paths import ICON_PATH


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app_state: AppState):
        super().__init__()
        self.icon = QIcon(ICON_PATH)
        self.setWindowIcon(self.icon)
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(self.icon)
        self.tray_icon.show()

        self.app_state = app_state
        (width, height, start_x, start_y) = init_screen_size()

        self.setGeometry(start_x, start_y, width, height)
        self.setMinimumSize(width * 8 // 10, height * 8 // 10)

        self.setWindowTitle(f"Faster Type")

        self.init_ui()

        self.controller = Controller(self, self.app_state)

    def init_ui(self):
        pass
