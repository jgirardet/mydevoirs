import tempfile
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest
from appdirs import user_cache_dir, user_config_dir, user_data_dir
from kivy.config import ConfigParser
from kivy.utils import rgba

from mydevoirs.constants import APP_NAME
from mydevoirs.utils import DEBUG, get_config, get_dir, get_matiere_color

res = {"Français": (0, 0, 255), "Anglais": (255, 120, 0), "Divers": (232, 120, 221)}


def test_get_matiere_color():
    assert get_matiere_color("Français", res) == rgba((0, 0, 255))
    assert get_matiere_color("Divers", res) == rgba((232, 120, 221))
    assert get_matiere_color("Blalala", res) == rgba((0, 0, 0))


def test_get_dir():
    assert get_dir("config", disable_debug=True) == Path(user_config_dir(), APP_NAME)
    assert get_dir("cache", disable_debug=True) == Path(user_cache_dir(), APP_NAME)
    assert get_dir("data", disable_debug=True) == Path(user_data_dir(), APP_NAME)

    with TemporaryDirectory() as n:
        with patch("mydevoirs.utils.appdirs.user_cache_dir", return_value=n):
            assert not Path(n, APP_NAME).exists()
            get_dir("cache", disable_debug=True)
            assert Path(n, APP_NAME).is_dir()


def test_get_dir_env(monkeypatch):
    monkeypatch.setenv("MYDEVOIRS_DEBUG", "True")
    assert (
        get_dir("config", enable_pytest=False)
        == Path(tempfile.gettempdir()) / "mydevoirs_debug" / "config" / APP_NAME
    )

    # assert get_dir("cache") == Path(user_cache_dir(), APP_NAME)
    # assert get_dir("data") == Path(user_data_dir(), APP_NAME)


@pytest.fixture(scope="module")
def cfp():
    c = ConfigParser()
    c.read_string(
        """[agenda]
lundi = 1
mardi = 1
mercredi = 0
jeudi = 1
vendredi = 1
samedi = 0
dimanche = 0
auto_next_week = 1

[ddb]
path = /tmp/mydevoirs_debug/cache/MyDevoirs/ddb_hard.sqlite
file_config_path = 

[aide]
aide = https://jgirardet.github.io/mydevoirs
"""
    )
    return c


@pytest.mark.parametrize(
    "section, key,  cls, default, res",
    [
        ("agenda", "lundi", None, None, "1"),
        ("agenda", "fauxjour", None, None, ""),
        ("agenda", "lundi", int, None, 1),
        ("agenda", "samedi", None, "bla", "0"),
        ("agenda", "fauxjour", None, "bla", "bla"),
        ("agenda", "lundi", bool, None, True),
        ("agenda", "samedi", bool, None, False),
    ],
)
def test_get_config(
    cfp, section, key, cls, default, res,
):
    class Fapp:
        config = cfp

    args = {}
    if cls is not None:
        args["cls"] = cls
    else:
        cls = str
    if default is not None:
        args["default"] = default
    with patch("mydevoirs.utils.App.get_running_app", side_effect=Fapp):
        value = get_config(section, key, **args)
        assert value == res
        assert isinstance(value, cls)


def test_DEBUG():
    assert DEBUG
