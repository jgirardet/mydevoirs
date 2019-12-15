import locale
import os
import platform
from pathlib import Path

import mydevoirs.app as m_app
from main import *
from mydevoirs.constants import DDB_FILENAME
from mydevoirs.database import init_database as m_init_database
from mydevoirs.utils import get_dir


def test_set_base_dir():
    import sys

    assert not hasattr(sys, "_MEIPASS")

    set_my_devoirs_base_dir()
    assert os.environ["MYDEVOIRS_BASE_DIR"] == str(Path(__file__).parents[1])

    os.environ.pop("MYDEVOIRS_BASE_DIR")

    sys._MEIPASS = "/home/bla"

    set_my_devoirs_base_dir()
    assert os.environ["MYDEVOIRS_BASE_DIR"] == "/home/bla"
    del sys._MEIPASS
    assert not hasattr(sys, "_MEIPASS")


def test_do_import():
    assert do_import() == (m_app, m_init_database)


def test_set_locale_fr():
    if platform.system() == "Linux":
        locale.setlocale(locale.LC_ALL, "en_US.utf8")
    else:
        locale.setlocale(locale.LC_ALL, "english")

    set_locale_fr()

    assert locale.getlocale()[0] == ("fr_FR")

    _reset_locale()


def _reset_locale():
    if platform.system() == "Linux":
        locale.resetlocale()


