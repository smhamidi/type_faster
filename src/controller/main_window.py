from typing import TYPE_CHECKING

from PyQt5.QtCore import QObject

from src import AppState
from config.color import MAIN_BACKGROUND

if TYPE_CHECKING:
    from src.view.main_window import MainWindow


class Controller(QObject):
    def __init__(self, view: "MainWindow", app_state: AppState):
        super().__init__()
        self.view = view

        self.app_state = app_state
        self.sensitive_states_ui = {"main_window_width", "main_window_height", None}

        self.app_state.state_changed.connect(self.render_view)
        self.render_view()

    def render_view(self, state_name=None, value=None):
        if state_name not in self.sensitive_states_ui:
            return

        if (
            self.app_state.main_window_width == 0
            or self.app_state.main_window_height == 0
        ):
            return

        self.render_style()

        # Calculating Optimal Size for Virtual Keyboard
        VK_H = self.app_state.main_window_height // 3
        VK_W = VK_H * 100 // 34  # Required width

        # if we don't have enough width: Do reverse
        if VK_W > (self.app_state.main_window_width * 95 // 100):
            VK_W = self.app_state.main_window_width * 95 // 100
            VK_H = VK_W * 34 // 100

        self.app_state.vk_width = VK_W
        self.app_state.vk_height = VK_H

        self.app_state.stat_height = self.app_state.main_window_height // 24
        self.app_state.stat_width = self.app_state.vk_width

        self.app_state.tb_height = self.app_state.vk_height
        self.app_state.tb_width = self.app_state.vk_width

        self.view.main_layout.setSpacing(self.app_state.stat_height // 2)

        self.view.statistic.setFixedSize(
            self.app_state.stat_width, self.app_state.stat_height
        )
        self.view.text_block.setFixedSize(
            self.app_state.tb_width, self.app_state.tb_height
        )
        self.view.virtual_keyboard.setFixedSize(
            self.app_state.vk_width, self.app_state.vk_height
        )

    def render_style(self):
        self.view.setStyleSheet(
            f"""
            background-color:{MAIN_BACKGROUND};
            """
        )
