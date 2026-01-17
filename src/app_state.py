import sys

from PyQt5.QtCore import QObject, pyqtSignal


# Setter and getter logic defined once in this descriptor
class State:
    def __init__(self, default=None):
        self._default = default
        self._name = None

    def __set_name__(self, owner, name):
        # Captures the name automatically from lvalue, e.g. username = State("smhamidi") -> _name = "username"
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self._name, self._default)

    def __set__(self, instance, value):
        current_value = instance.__dict__.get(self._name, self._default)

        if current_value != value:
            instance.__dict__[self._name] = value
            instance.state_changed.emit(self._name, value)


class AppState(QObject):
    # One single generic signal: sends (state_name, new_value)
    state_changed = pyqtSignal(str, object)

    _instantiated = False

    # States defines here

    # Main Window States
    main_window_width: int = State(0)
    main_window_height: int = State(0)

    # Statistic States
    stat_width: int = State(0)
    stat_height: int = State(0)

    # Text Block States
    tb_width: int = State(0)
    tb_height: int = State(0)

    # Virtual Keyboard State
    vk_width: int = State(0)
    vk_height: int = State(0)

    # Virtual Keyboard States
    pushed_keys: set = State(set())

    def __init__(self):
        if AppState._instantiated:
            print("Error: Only one AppState object can be created. Exit...")
            sys.exit(1)
        AppState._instantiated = True
        super().__init__()

    def __setattr__(self, name, value):
        is_defined_in_class = hasattr(type(self), name)
        is_private = name.startswith("_")

        if is_defined_in_class or is_private:
            super().__setattr__(name, value)
        else:
            print(f"Error: new states can not be created outside AppState.")
            sys.exit(1)

    def __getattr__(self, name):
        print(f"Error: state '{name}' does not exist in AppState.")
        sys.exit(1)

    def reset(self):
        for name, attr in type(self).__dict__.items():
            if isinstance(attr, State):
                setattr(self, name, attr._default)
