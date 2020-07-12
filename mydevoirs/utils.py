import os
import sys
import tempfile
from pathlib import Path as PythonPath

import appdirs
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
