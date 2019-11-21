# flake8: noqa

from pathlib import Path
import sys
import locale
import platform
import os
from importlib import import_module


def set_my_devoirs_base_dir():
    os.environ["MYDEVOIRS_BASE_DIR"] = getattr(
        sys, "_MEIPASS", str(Path(__file__).absolute().parent)
    )


def do_import():
    app = import_module("mydevoirs.app")
    database = import_module("mydevoirs.database.database")
    return app, database

def set_locale_fr():
    if platform.system() == "Linux":
        locale.setlocale(locale.LC_ALL, "fr_FR.utf8")
    else:
        locale.setlocale(locale.LC_ALL, "french")


def setup_start():
    set_my_devoirs_base_dir()
    app, database = do_import()
    set_locale_fr()
    database.db_init()
    return app


if __name__ == "__main__":
    setup_start().MyDevoirsApp().run()
