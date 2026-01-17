from PyQt5.QtWidgets import QWidget, QVBoxLayout
from src.app_state import AppState
from src.controller.virtual_keyboard import Controller
from PyQt5.QtCore import Qt


class VirtualKeyboard(QWidget):
    def __init__(self, app_state: AppState):
        super().__init__()
        self.app_state = app_state

        self.init_ui()
        self.controller = Controller(self, self.app_state)

    def init_ui(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.v_layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.setLayout(self.v_layout)
