# flake8: noqa

import locale
import os
import platform
import sys
from pathlib import Path
import sys


def set_my_devoirs_base_dir():
    os.environ["MYDEVOIRS_BASE_DIR"] = getattr(
        sys, "_MEIPASS", str(Path(__file__).absolute().parent)
    )


def do_import():
    from mydevoirs import app
    from mydevoirs.database import init_database

    return app, init_database


def set_locale_fr():
    if platform.system() == "Linux":
        locale.setlocale(locale.LC_ALL, "fr_FR.utf8")  # pragma: no cover_win
    else:
        locale.setlocale(locale.LC_ALL, "french")  # pragma: no cover_linux


def setup_kivy():
    from kivy.config import Config

    base_dir = os.environ["MYDEVOIRS_BASE_DIR"]
    Config.set("input", "mouse", "mouse,multitouch_on_demand")
    Config.set("kivy", "window_icon", os.path.join(base_dir, "logo.png"))


def setup_start():
    set_my_devoirs_base_dir()
    setup_kivy()
    app, init_database = do_import()
    set_locale_fr()
    return app


if __name__ == "__main__": # pragma: no cover_all
    # covered in check_executable.py
    
    app = setup_start().MyDevoirsApp()
    app.init_database()
    app.run()  
