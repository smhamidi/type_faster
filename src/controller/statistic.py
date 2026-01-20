from typing import TYPE_CHECKING

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QFont

from src import AppState
from config.color import STATISTIC_BACKGROUND, STATISTIC_TEXT, STATISTIC_BORDER
from config.style import BORDER_RADIUS


if TYPE_CHECKING:
    from src.view.widget import Statistic


class Controller(QObject):
    def __init__(self, view: "Statistic", app_state: AppState):
        super().__init__()
        self.view = view

        self.app_state = app_state
        self.sensitive_states_ui = {
            "stat_width",
            "stat_height",
            "round_result",
            "start_time",
            None,
        }

        self.app_state.state_changed.connect(self.render_view)
        self.render_view()

    def render_view(self, state_name=None, value=None):
        if state_name not in self.sensitive_states_ui:
            return

        if self.app_state.stat_width == 0 or self.app_state.stat_height == 0:
            return

        if state_name == "round_result":
            self.show_result()

        self.view.setFixedSize(self.app_state.stat_width, self.app_state.stat_height)
        self.render_style()

    def show_result(self):
        self.view.label.setText(
            f'Speed (WPM): {self.app_state.round_result.get("wpm", "")} | Duration: {self.app_state.round_result.get("duration", "")}'
        )

    def render_style(self):
        font = QFont()
        font_size = self.app_state.stat_height // 2
        font.setPixelSize(font_size)
        self.view.label.setFont(font)
        self.view.setStyleSheet(
            f"""
            font-family: "Roboto Mono";
            background-color:{STATISTIC_BACKGROUND};
            color:{STATISTIC_TEXT};
            border: 1px solid {STATISTIC_BORDER};
            border-radius: {BORDER_RADIUS}px;
            """
        )
