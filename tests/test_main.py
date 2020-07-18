from unittest.mock import patch

import pytest

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


def test_setup_kivy():
    assert setup_kivy()
    from kivy.config import Config

    assert Config["input"]["mouse"] == "mouse,multitouch_on_demand"
    assert Path(Config["kivy"]["window_icon"]).is_file()


@pytest.mark.skipif(platform.system() == "Linux", reason="only Windows")
def test_setup_kivy_windows():
    setup_kivy()
    assert os.environ.get("KIVY_GL_BACKEND", None) == "angle_sdl2"
    assert os.environ.get("KIVY_NO_CONSOLELOG", None) is None
    with patch.object(sys, "executable", "some\\path\\pythonw.exe"):
        setup_kivy()
        assert os.environ.get("KIVY_NO_CONSOLELOG", None) == "True"
