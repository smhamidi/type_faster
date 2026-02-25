import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    ROOT_DIR = sys._MEIPASS
else:
    ROOT_DIR = str(Path(__file__).resolve().parent.parent)

_STATIC_DIR = os.path.join(ROOT_DIR, "static")
ICON_PATH = os.path.join(_STATIC_DIR, "icon", "TypeFaster.png")
CORPUS_DIR = os.path.join(_STATIC_DIR, "corpus")