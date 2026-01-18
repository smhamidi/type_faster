from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from src.app_state import AppState
from src.controller.text_block import Controller


class TextBlock(QWidget):
    def __init__(self, app_state: AppState):
        super().__init__()
        self.app_state = app_state

        self.init_ui()
        self.controller = Controller(self, self.app_state)

    def init_ui(self):
        self.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.label = QLabel("")
        self.label.setContentsMargins(0, 0, 0, 0)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        layout.addWidget(self.label)

        self.setLayout(layout)
