from main import set_my_devoirs_base_dir, do_import, set_locale_fr
import os
from pathlib import Path
import mydevoirs.app as m_app
import mydevoirs.database.database as m_database
import locale
import platform


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


# def test_set_locale_fr():
#     backup = locale.getlocale()
#     if platform.system() == "Linux":
#         locale.setlocale(locale.LC_ALL, "en_GB.utf8")
#     else:
#         locale.setlocale(locale.LC_ALL, "english")


#     set_locale_fr()

#     assert locale.getlocale() == ('fr_FR', 'UTF-8')

#     # locale.setlocale(*backup)
#     locale.setlocale(locale.LC_ALL, backup[0].lower()+ "." +backup[1].strip('-').lower())
