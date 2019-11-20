from pathlib import Path
import sys

import os

os.environ["MYDEVOIRS_BASE_DIR"] = getattr(
    sys, "_MEIPASS", str(Path(__file__).absolute().parent)
)


from mydevoirs.app import MyDevoirsApp


MyDevoirsApp().run()
