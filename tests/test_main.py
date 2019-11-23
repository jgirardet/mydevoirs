import locale
import os
import platform
from pathlib import Path

import mydevoirs.app as m_app
import mydevoirs.database.database as m_database
from main import do_import, set_locale_fr, set_my_devoirs_base_dir, setup_start


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
    assert do_import() == (m_app, m_database)


def test_set_locale_fr():
    if platform.system() == "Linux":
        locale.setlocale(locale.LC_ALL, "en_GB.utf8")
    else:
        locale.setlocale(locale.LC_ALL, "english")

    set_locale_fr()

    assert locale.getlocale()[0] == ("fr_FR")

    _reset_locale()


def test_setup_start():
    a = setup_start()
    assert "MYDEVOIRS_BASE_DIR" in os.environ
    assert a == m_app

    if platform.system() == "Linux":
        assert locale.getlocale() == ("fr_FR", "UTF-8")
    else:
        assert locale.getlocale() == ("fr_FR", "cp1252")


def _reset_locale():
    if platform.system() == "Linux":
        locale.resetlocale()
