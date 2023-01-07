from unittest.mock import patch

import pytest
from mydevoirs.main import *
from mydevoirs.constants import VERSION


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
    from mydevoirs.__main__ import configure_env

    with patch.object(sys, "executable", "some\\path\\pythonw.exe"):
        configure_env()
        assert os.environ.get("KIVY_NO_CONSOLELOG", None) == "True"
        os.environ.pop("KIVY_NO_CONSOLELOG")


@pytest.mark.parametrize(
    "texte, exp_ret, file_ver, in_file",
    [
        ("[agenda]\nlundi = 1", 1, None, VERSION),
        ("", 1, None, VERSION),
        ("[aide]\nlundi = 1", 1, None, VERSION),
        ("[aide]\nVersion = 0.1.1", 3, "0.1.1", "0.1.1"),
        ("[aide]\nVersion = 9999", 4, "9999", "9999"),
        (f"[aide]\nVersion = {VERSION}", 2, VERSION, VERSION),
    ],
)
def test_reapply_version(texte, exp_ret, file_ver, in_file):
    app = MyDevoirsApp()
    config = ConfigParser()
    app.build_config(config)
    filep = Path(app.get_application_config())
    filep.write_text(texte)

    ret, ver = reapply_version(app)
    assert ret == exp_ret
    assert ver == file_ver
    config.read(app.get_application_config())
    assert config.get("aide", "version") == in_file


@pytest.mark.parametrize(
    "create, state, exists, res",
    [
        (True, 0, True, True),
        (False, 0, False, None),
        (True, 1, True, True),
        (False, 1, False, None),
        (True, 2, True, None),
        (True, 3, True, None),
        (True, 4, True, None),
    ],
)
def test_reset_database_if_no_version(tmpfilename: Path, create, state, exists, res):
    app = MyDevoirsApp()
    with patch.object(app, "load_config", return_value={"ddb": {"path": tmpfilename}}):
        if create:
            tmpfilename.touch()
        assert get_backup_ddb_path(app, state) == (
            tmpfilename,
            (
                tmpfilename.parent / "mydevoirs_sauvegarde_ancienne_version.ddb"
                if res
                else None
            ),
        )
        assert tmpfilename.is_file() == exists
