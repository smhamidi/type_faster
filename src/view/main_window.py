from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QWidget, QVBoxLayout
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QCoreApplication

from src.util import initial_app_size_pos, main_display_size
from src import AppState
from src.controller.main_window import Controller
from config.path import ICON_PATH
from src.view.widget import Statistic
from src.view.widget import TextBlock
from src.view.widget import VirtualKeyboard
from src.const import (
    writable_keys,
    key_to_char,
    normal_keys,
    normal_to_shift,
    char_to_key,
)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app_state: AppState):
        super().__init__()
        self.setWindowTitle(f"Faster Type")

        # App icon
        self.icon = QIcon(ICON_PATH)
        self.setWindowIcon(self.icon)

        # Tray icon
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(self.icon)

        # Tray menu
        self.tray_menu = QMenu(self)
        # Set the menu on the system tray icon
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        self.app_state = app_state
        width, height, start_x, start_y = initial_app_size_pos()
        self.setGeometry(start_x, start_y, width, height)

        self.app_state.main_window_width = width
        self.app_state.main_window_height = height

        display_width, display_height = main_display_size()
        self.setMinimumSize(display_width // 2, display_height // 2)

        self.init_ui()
        self.init_tray_icon_menubar()

        self.installEventFilter(self)  # Required for self.eventFilter

        self.controller = Controller(self, self.app_state)

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Widgets
        self.statistic = Statistic(self.app_state)
        self.text_block = TextBlock(self.app_state)
        self.virtual_keyboard = VirtualKeyboard(self.app_state)

        # Layout
        self.main_layout = QVBoxLayout()

        # Sizing
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addWidget(self.statistic)
        self.main_layout.addWidget(self.text_block)
        self.main_layout.addWidget(self.virtual_keyboard)

        self.main_layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.central_widget.setLayout(self.main_layout)

    def init_tray_icon_menubar(self):
        # Tray icon: Show action
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.showNormal)
        self.tray_menu.addAction(show_action)

        # Tray icon: Hide action
        hide_action = QAction("Hide", self)
        hide_action.triggered.connect(self.showMinimized)
        self.tray_menu.addAction(hide_action)

        # Tray icon: Quit action
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QCoreApplication.instance().quit)
        self.tray_menu.addAction(quit_action)

    def resizeEvent(self, event):
        # Called whenever window size changes
        self.app_state.main_window_width = self.width()
        self.app_state.main_window_height = self.height()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()

            pushed_key_set = set(self.app_state.pushed_keys)
            pushed_key_set.add(key)
            self.app_state.pushed_keys = list(pushed_key_set)

            if key in key_to_char:
                char = key_to_char[key]
                if char in writable_keys or char == "delete" or char == "space":
                    if (
                        char in normal_keys
                        and char_to_key["shift"] in self.app_state.pushed_keys
                    ):
                        self.app_state.last_pushed_button = normal_to_shift[char]
                    else:
                        self.app_state.last_pushed_button = char

            return True
        elif event.type() == QEvent.KeyRelease:
            key = event.key()

            pushed_key_set = set(self.app_state.pushed_keys)
            pushed_key_set.discard(key)
            self.app_state.pushed_keys = list(pushed_key_set)
            return True
        else:
            return super().eventFilter(obj, event)
