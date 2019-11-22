# flake8: noqa

import locale
import os
import platform
import sys
from importlib import import_module
from pathlib import Path


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
        locale.setlocale(locale.LC_ALL, "fr_FR.utf8")  # pragma: no cover_win
    else:
        locale.setlocale(locale.LC_ALL, "french")  # pragma: no cover_linux


def setup_start():
    set_my_devoirs_base_dir()
    app, database = do_import()
    set_locale_fr()
    database.db_init()
    return app


if __name__ == "__main__":  # pragma: no cover_all
    setup_start().MyDevoirsApp().run()
