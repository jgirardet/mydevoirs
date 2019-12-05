# flake8: noqa

import locale
import os
import platform
import sys
from pathlib import Path

from appdirs import user_cache_dir


APPNAME = "MyDevoirs"
DDB_NAME = "ddb_hard.sqlite"

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


def get_database_location():
    return Path(user_cache_dir(), APPNAME, DDB_NAME).absolute()


def setup_start(**kwargs):
    set_my_devoirs_base_dir()
    setup_kivy()
    app, init_database = do_import()
    set_locale_fr()
    init_database(**kwargs)
    return app


if __name__ == "__main__":

    setup_start(
        provider="sqlite", filename=str(get_database_location()), create_db=True
    ).MyDevoirsApp().run()  # pragma: no cover_all
