from typing import TYPE_CHECKING, List
import random

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QFont

from src import AppState
from config.color import (
    TEXT_BLCOK_TEXT_CURRENT,
    TEXT_BLOCK_BACKGROUND,
    TEXT_BLOCK_BORDER,
    TEXT_BLOCK_TEXT,
    TEXT_BLOCK_TEXT_PASSED,
    TEXT_BLOCK_TEXT_WRONG,
)
from config.corpus import DEFAULT_CORPUS_PATH
from config.text_block import NUM_WORD_FOR_EACH_ROUND

if TYPE_CHECKING:
    from src.view.widget import TextBlock


class Controller(QObject):
    def __init__(self, view: "TextBlock", app_state: AppState):
        super().__init__()
        self.view = view

        self.app_state = app_state
        self.sensitive_states_ui = {"tb_width", "tb_height", "success_round", None}

        self.corpus = None
        self.init_corpus()
        self.render_new_words()

        self.app_state.state_changed.connect(self.render_view)
        self.render_view()

    def render_view(self, state_name=None, value=None):
        if state_name not in self.sensitive_states_ui:
            return

        if self.app_state.tb_width == 0 or self.app_state.tb_height == 0:
            return

        if state_name == "success_round":
            self.render_new_words()

        self.view.setFixedSize(self.app_state.tb_width, self.app_state.tb_height)
        self.view.label.setFixedSize(self.app_state.tb_width, self.app_state.tb_height)

        self.render_style()

    def render_style(self):
        font = QFont()
        font.setPixelSize(self.app_state.tb_height // 12)
        self.view.label.setFont(font)

        self.view.setStyleSheet(
            f"""
            font-family: "Roboto Mono";
            background-color:{TEXT_BLOCK_BACKGROUND};
            color:{TEXT_BLOCK_TEXT};
            border: 1px solid {TEXT_BLOCK_BORDER};
            """
        )

    def init_corpus(self):
        with open(DEFAULT_CORPUS_PATH, "r") as corpus:
            lines: List[str] = corpus.readlines()
            self.corpus = [line.strip() for line in lines]

    def render_new_words(self):
        selected_words = random.choices(self.corpus, k=NUM_WORD_FOR_EACH_ROUND)
        self.app_state.text_block = " ".join(selected_words)

        self.view.label.setText(self.app_state.text_block)
