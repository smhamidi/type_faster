from screeninfo import get_monitors


def main_display_size():
    for monitor in get_monitors():
        if monitor.is_primary:
            return (monitor.width, monitor.height)
    return (None, None)


def initial_app_size_pos():
    (SCREEN_WIDTH, SCREEN_HEIGHT) = main_display_size()
    APP_HEIGHT = SCREEN_HEIGHT * 75 // 100
    APP_WIDTH = SCREEN_WIDTH * 75 // 100
    APP_TOP_X = (SCREEN_WIDTH - APP_WIDTH) // 2
    APP_TOP_Y = (SCREEN_HEIGHT - APP_HEIGHT) // 2

    return (APP_WIDTH, APP_HEIGHT, APP_TOP_X, APP_TOP_Y)
