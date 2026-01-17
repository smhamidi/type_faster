from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


def create_keyboard_key(
    char_list,
    bg_color,
    text_color,
    w,
    h,
    side,
):
    if len(char_list) > 2:
        raise ValueError(
            "create_keyboard_key: Error: Maximum two character can be in a keyboard key"
        )

    label = QLabel("\n".join(char_list))
    label.setFixedWidth(w)
    label.setFixedHeight(h)

    # Decide for font and alignment
    if side:
        if side.lower() == "l" or side.lower() == "left":
            alignment = Qt.AlignLeft | Qt.AlignBottom
            font_size = int(abs(h / 4))

        elif side.lower() == "r" or side.lower() == "right":
            alignment = Qt.AlignRight | Qt.AlignBottom
            font_size = int(abs(h / 4))

        elif side.lower() == "c" or side.lower() == "center":
            alignment = Qt.AlignVCenter | Qt.AlignHCenter
            font_size = int(abs(h / 3))

        else:
            raise ValueError(f"create_keyboard_key: Error: invalid side: {side}.")
    else:
        raise ValueError(f"create_keyboard_key: Error: side not defined.")

    label.setStyleSheet(
        f"""
        QLabel {{
            font-family: "Roboto Mono";
            background-color: {bg_color};
            color: {text_color};
            border: none;
            padding: 0;
            margin: 0;
            text-align: center;
            font-size: {font_size}px;
            padding: 5px;
            border-radius: 5px
        }}
    """
    )
    label.setAlignment(alignment)
    return label
