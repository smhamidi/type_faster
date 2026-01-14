import os
from pathlib import Path

ROOT_DIR = str(Path(__file__).resolve().parent.parent)

_STATIC_DIR = os.path.join(ROOT_DIR, "static")
ICON_PATH = os.path.join(_STATIC_DIR, "icon", "TypeFaster.png")
CORPUS_DIR = os.path.join(_STATIC_DIR, "corpus")
