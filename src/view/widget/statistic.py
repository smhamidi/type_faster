from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

from src.app_state import AppState
from src.controller.statistic import Controller


class Statistic(QWidget):
    def __init__(self, app_state: AppState):
        super().__init__()
        self.app_state = app_state

        self.init_ui()
        self.controller = Controller(self, self.app_state)

    def init_ui(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.label = QLabel()
        self.label.setText("Speed (WPM):       | Duration: ")
        self.main_layout.addWidget(self.label)

        self.setLayout(self.main_layout)
