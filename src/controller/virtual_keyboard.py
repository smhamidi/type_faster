from typing import TYPE_CHECKING, List
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from src import AppState
from src.const import keyboard
from src.util import create_keyboard_key
from config.color import (
    VIRTUAL_KEYBOARD_BUTTON_BACKGROUND,
    VIRTUAL_KEYBOARD_BUTTON_TEXT,
    MAIN_BACKGROUND,
    VIRTUAL_KEYBOARD_BUTTON_PUSHED,
)

if TYPE_CHECKING:
    from src.view.widget import VirtualKeyboard


class Controller(QObject):
    def __init__(self, view: "VirtualKeyboard", app_state: AppState):
        super().__init__()
        self.view = view

        self.app_state = app_state
        self.sensitive_states_ui = {"vk_width", "vk_height", "pushed_keys", None}

        self.app_state.state_changed.connect(self.render_view)
        self.render_view()

    def render_view(self, state_name=None, value=None):

        if state_name not in self.sensitive_states_ui:
            return

        if self.app_state.vk_width == 0 or self.app_state.vk_height == 0:
            return

        self.view.setFixedSize(self.app_state.vk_width, self.app_state.vk_height)

        # Delete old rows
        if hasattr(self, "rows"):
            for row in self.rows:
                self.view.v_layout.removeWidget(row)

        # Create empty initial row widgets
        self.rows: List[QWidget] = []
        for _ in range(5):
            row = QWidget()
            row.setContentsMargins(0, 0, 0, 0)
            self.rows.append(row)

        for row in self.rows:
            self.view.v_layout.addWidget(row)

        for row, inner_dict in keyboard.items():
            # Row layout
            layout = QHBoxLayout()

            # Row keys
            for column, key in inner_dict.items():
                key_width, key_height = self.calculate_size(key["type"])

                # Coloring keys
                if "empty" in key["type"]:
                    bg_color = MAIN_BACKGROUND

                elif list(key['code'])[0] == value:
                    bg_color = VIRTUAL_KEYBOARD_BUTTON_PUSHED

                else:
                    bg_color = VIRTUAL_KEYBOARD_BUTTON_BACKGROUND

                key_widget = create_keyboard_key(
                    char_list=key["text"],
                    bg_color=bg_color,
                    text_color=VIRTUAL_KEYBOARD_BUTTON_TEXT,
                    w=key_width,
                    h=key_height,
                    side=key["side"],
                )

                layout.addWidget(key_widget)

            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(self.app_state.vk_width // 100)

            self.rows[row - 1].setLayout(layout)

        self.view.v_layout.setSpacing(self.app_state.vk_width // 100)

    def calculate_size(self, type: str):
        height = self.app_state.vk_width * 6 // 100
        if type.lower() == "spacing":
            width = self.app_state.vk_width // 100
        elif type.lower() == "square":
            width = self.app_state.vk_width * 6 // 100
        elif type.lower() == "rec-s":
            width = self.app_state.vk_width * 9 // 100
        elif type.lower() == "rec-m":
            width = self.app_state.vk_width * 11 // 100
        elif type.lower() == "rec-l":
            width = self.app_state.vk_width * 29 // 200
        elif type.lower() == "space":
            width = self.app_state.vk_width * 34 // 100
        elif type.lower() == "empty-l-space":
            width = self.app_state.vk_width * 57 // 200
        elif type.lower() == "empty-r-space":
            width = self.app_state.vk_width * 71 // 200
        else:
            raise ValueError(f"Not valid type: {type}")

        return int(width), int(height)
