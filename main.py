from mydevoirs.app import MyDevoirsApp
from pathlib import Path
import sys

import os

os.environ["MYDEVOIRS_BASE_DIR"] = getattr(
    sys, "_MEIPASS", str(Path(__file__).absolute().parent)
)

MyDevoirsApp().run()
