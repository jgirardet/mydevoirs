from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from appdirs import user_cache_dir, user_config_dir, user_data_dir
from kivy.utils import rgba

from mydevoirs.constants import APP_NAME
from mydevoirs.utils import *

res = {"Français": (0, 0, 255), "Anglais": (255, 120, 0), "Divers": (232, 120, 221)}


def test_get_matiere_color():
    assert get_matiere_color("Français", res) == rgba((0, 0, 255))
    assert get_matiere_color("Divers", res) == rgba((232, 120, 221))
    assert get_matiere_color("Blalala", res) == rgba((0, 0, 0))


def test_get_dir():
    assert get_dir("config") == Path(user_config_dir(), APP_NAME)
    assert get_dir("cache") == Path(user_cache_dir(), APP_NAME)
    assert get_dir("data") == Path(user_data_dir(), APP_NAME)

    with TemporaryDirectory() as n:
        with patch("mydevoirs.utils.appdirs.user_cache_dir", return_value=n):
            assert not Path(n, APP_NAME).exists()
            get_dir("cache")
            assert Path(n, APP_NAME).is_dir()
