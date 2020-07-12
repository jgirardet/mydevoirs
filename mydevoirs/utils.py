import os
import tempfile
from pathlib import Path as PythonPath

import appdirs
from kivy.app import App
from kivy.config import Config, ConfigParser
from kivy.utils import rgba

from mydevoirs.constants import APP_NAME
from mydevoirs.datas import get_datas

datas = get_datas()


class Path(type(PythonPath())):
    @property
    def aname(self):
        return str(self.absolute())


_temppath = None


def get_dir(key, disable_debug=False):

    global _temppath

    def default():
        return Path(getattr(appdirs, "user_" + key + "_dir")(), APP_NAME)

    if disable_debug:
        dire = default()
    elif os.environ.get("PYTEST_CURRENT_TEST", None):
        # if DEBUG and not disable_debug:
        temppath = _temppath or Path(tempfile.TemporaryDirectory().name)
        _temppath = temppath
        dire = temppath / key / APP_NAME
    elif DEBUG:  # pragma: no cover_all
        _temppath = Path(Path(tempfile.gettempdir()) / "mydevoirs_debug")
        if not _temppath.exists():
            _temppath.mkdir()
        dire = _temppath / key / APP_NAME
    else:  # pragma: no cover_all
        dire = default()

    if not dire.is_dir():
        dire.mkdir(parents=True)
    return dire


def get_matiere_color(nom, matiere):
    try:

        return rgba(matiere[nom])
    except KeyError:
        return rgba((0, 0, 0))


DEBUG = True


def get_config(section, key, cls=str, default=""):
    """
    Récupère une valeur dans la configuration de l'application.

    :param section: str
    :param key: str
    :param cls: type du retour souhaité, default = str
    :param default: fallback. default = ""
    :return: Any or None si la clé n'est pas présente
    """
    if app := App.get_running_app():
        config: ConfigParser = app.config
        # trick pour les tests, ne pas tester
        if not config:  # pragma: no branch
            config = ConfigParser()
            app.build_config(config)
        value = config.getdefault(section, key, default)
        if cls == bool:
            return bool(int(value))
        elif cls == int:
            return int(value)
        else:
            return value  # as string
