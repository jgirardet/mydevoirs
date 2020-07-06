# flake8: noqa

import locale
import os
import platform
import sys
from pathlib import Path

from mydevoirs.constants import BASE_DIR


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

    # base_dir = str(BASE_DIR)
    Config.set("input", "mouse", "mouse,multitouch_on_demand")
    Config.set("kivy", "window_icon", os.path.join("data", "icons", "logo-512.png"))


def setup_start():
    setup_kivy()
    app, init_database = do_import()
    set_locale_fr()
    return app
