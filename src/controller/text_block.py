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
from config.style import BORDER_RADIUS

if TYPE_CHECKING:
    from src.view.widget import TextBlock


class Controller(QObject):
    def __init__(self, view: "TextBlock", app_state: AppState):
        super().__init__()
        self.view = view

        self.app_state = app_state
        self.sensitive_states_ui = {
            "tb_width",
            "tb_height",
            "success_round",
            "last_pushed_button",
            "typed_text",
            None,
        }

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
            self.reset()
            self.render_new_words()

        if (
            state_name == "last_pushed_button"
            and self.app_state.last_pushed_button != ""
        ):
            self.handle_last_push()
            self.reset_last_pushed_button()

        if state_name == "typed_text":
            self.render_keyboard()

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
            border-radius: {BORDER_RADIUS}px;
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

    def handle_last_push(self):
        if self.app_state.last_pushed_button == "delete":
            if len(self.app_state.typed_text) > 0:
                self.app_state.typed_text = self.app_state.typed_text[:-1]
        elif self.app_state.last_pushed_button == "space":
            self.app_state.typed_text += " "
        else:
            self.app_state.typed_text = self.app_state.typed_text + str(
                self.app_state.last_pushed_button
            )

    def reset_last_pushed_button(self):
        self.app_state.last_pushed_button = ""

    def render_keyboard(self):
        last_common_idx = self.find_last_common(
            self.app_state.text_block, self.app_state.typed_text
        )
        if last_common_idx == len(self.app_state.text_block):
            # Round is complete
            self.app_state.success_round += 1
            return
        if last_common_idx == len(self.app_state.typed_text):
            correct_so_far = True
        else:
            correct_so_far = False

        if correct_so_far:
            typed_len = len(self.app_state.typed_text)
            self.view.label.setText(
                f'<span style="color:{TEXT_BLOCK_TEXT_PASSED};">{self.app_state.text_block[0:typed_len]}</span>'
                f'<span style="color:{TEXT_BLCOK_TEXT_CURRENT};">{self.app_state.text_block[typed_len]}</span>'
                f'<span style="color:{TEXT_BLOCK_TEXT};">{self.app_state.text_block[typed_len+1:]}</span>'
            )
        else:
            self.view.label.setText(
                f'<span style="color:{TEXT_BLOCK_TEXT_PASSED};">{self.app_state.text_block[0:last_common_idx]}</span>'
                f'<span style="color:{TEXT_BLOCK_TEXT_WRONG};">{self.app_state.typed_text[last_common_idx:]}</span>'
                f'<span style="color:{TEXT_BLOCK_TEXT};">{self.app_state.text_block[last_common_idx:]}</span>'
            )

    def find_last_common(self, target: str, typed: str):
        if len(typed) == 0:
            # Nothing typed yet
            return 0
        for i in range(len(target)):
            if target[i] == typed[i]:
                if i == len(typed) - 1:
                    # Typed is correct so far
                    return len(typed)
                continue
            else:
                return i

        # They fully match
        return i + 1

    def reset(self):
        self.app_state.last_pushed_button = ""
        self.app_state.typed_text = ""
