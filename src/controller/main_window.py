from typing import TYPE_CHECKING

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QCoreApplication

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
        self.init_tray_icon_menubar()
        self.render_view()

    def render_view(self, state_name=None, value=None):
        if state_name not in self.sensitive_states_ui:
            return

        pass

    def init_tray_icon_menubar(self):
        # Tray icon: Show action
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.view.showMaximized)
        self.view.tray_menu.addAction(show_action)

        # Tray icon: Hide action
        hide_action = QAction("Hide", self)
        hide_action.triggered.connect(self.view.showMinimized)
        self.view.tray_menu.addAction(hide_action)

        # Tray icon: Quit action
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QCoreApplication.instance().quit)
        self.view.tray_menu.addAction(quit_action)
