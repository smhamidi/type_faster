from screeninfo import get_monitors


def init_screen_size():
    for monitor in get_monitors():
        if monitor.is_primary:
            SCREEN_HEIGHT = monitor.height * 75 // 100
            SCREEN_WIDTH = monitor.width * 75 // 100
            SCREEN_TOP_X = (monitor.width - SCREEN_WIDTH) // 2
            SCREEN_TOP_Y = (monitor.height - SCREEN_HEIGHT) // 2

    return (SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TOP_X, SCREEN_TOP_Y)
