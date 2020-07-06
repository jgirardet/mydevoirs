from mydevoirs import app as m_app
from mydevoirs.database import init_database as m_init_database
from mydevoirs.main import *


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
