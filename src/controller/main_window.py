from typing import TYPE_CHECKING

from PyQt5.QtCore import QObject
from src import AppState

if TYPE_CHECKING:
    from src.view.main_window import MainWindow


class Controller(QObject):
    def __init__(self, view: "MainWindow", app_state: AppState):
        super().__init__()
        self.view = view

        self.app_state = app_state
        self.sensitive_states_ui = {None}

        self.app_state.state_changed.connect(self.render_view)
        self.render_view()

    def render_view(self, state_name=None, value=None):
        if state_name not in self.sensitive_states_ui:
            return

        pass